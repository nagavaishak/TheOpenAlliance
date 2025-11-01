from strands import tool
import json
from typing import Dict, List

@tool
def analyze_oran_config(config_path: str) -> Dict:
    """
    Analyzes an O-RAN component configuration file for compliance and compatibility.
    
    Args:
        config_path: Path to the JSON configuration file
        
    Returns:
        Dictionary containing analysis results with compatibility issues and warnings
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        issues = []
        warnings = []
        compliance_score = 100
        
        # Check Open Fronthaul interface
        if 'interfaces' in config and 'open_fronthaul' in config['interfaces']:
            oh = config['interfaces']['open_fronthaul']
            
            # Version check
            if 'version' in oh:
                version = float(oh['version'])
                if version < 7.0:
                    issues.append(f"Open Fronthaul version {oh['version']} is outdated. Recommended: 7.0+")
                    compliance_score -= 20
                elif version > 7.0:
                    warnings.append(f"Using newer Open Fronthaul {oh['version']} - ensure backward compatibility")
            
            # eCPRI version check
            if 'ecpri_version' in oh:
                ecpri = oh['ecpri_version']
                if ecpri != "2.0":
                    issues.append(f"eCPRI version {ecpri} may cause interoperability issues. Standard: 2.0")
                    compliance_score -= 15
            
            # Timing parameters check
            if 'timing' in oh:
                timing = oh['timing']
                
                # T2a timing window check
                if 't2a_max' in timing and 't2a_min' in timing:
                    t2a_window = timing['t2a_max'] - timing['t2a_min']
                    if t2a_window < 200:
                        warnings.append(f"Narrow T2a timing window ({t2a_window}μs) may limit vendor compatibility")
                    
                    # Check against typical requirements
                    if timing['t2a_max'] > 285:
                        issues.append(f"T2a_max ({timing['t2a_max']}μs) exceeds typical O-DU expectations (285μs)")
                        compliance_score -= 10
                    
                    if timing['t2a_min'] < 70:
                        warnings.append(f"Very tight T2a_min ({timing['t2a_min']}μs) requires high-performance fronthaul")
        
        # Check F1 interface (for O-DU)
        if 'interfaces' in config and 'F1' in config['interfaces']:
            f1 = config['interfaces']['F1']
            
            if 'protocol_version' in f1:
                version = f1['protocol_version']
                if version < "15.0.0":
                    issues.append(f"F1 protocol version {version} is outdated. Recommended: 15.4.0+")
                    compliance_score -= 15
        
        # Check capabilities
        if 'capabilities' in config:
            caps = config['capabilities']
            
            # Beamforming check
            if 'beamforming' in caps and not caps['beamforming']:
                warnings.append("Beamforming not supported - may limit 5G performance")
            
            # Bandwidth check
            if 'bandwidth' in caps:
                bw = caps['bandwidth']
                if '50MHz' in bw:
                    warnings.append("Limited to 50MHz bandwidth - consider 100MHz for better performance")
        
        result = {
            "vendor": config.get('vendor', 'Unknown'),
            "component": config.get('component', 'Unknown'),
            "compliance_score": compliance_score,
            "status": "PASS" if compliance_score >= 70 else "FAIL",
            "issues": issues,
            "warnings": warnings,
            "config_summary": {
                "fronthaul_version": config.get('interfaces', {}).get('open_fronthaul', {}).get('version', 'N/A'),
                "supported_bandwidth": config.get('capabilities', {}).get('bandwidth', 'N/A')
            }
        }
        
        return result
        
    except FileNotFoundError:
        return {"error": f"Configuration file not found: {config_path}"}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON format in: {config_path}"}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


@tool
def check_compatibility(odu_config_path: str, oru_config_path: str) -> Dict:
    """
    Checks compatibility between O-DU and O-RU configurations.
    
    Args:
        odu_config_path: Path to O-DU configuration JSON file
        oru_config_path: Path to O-RU configuration JSON file
        
    Returns:
        Dictionary with compatibility assessment and specific issues
    """
    try:
        with open(odu_config_path, 'r') as f:
            odu = json.load(f)
        with open(oru_config_path, 'r') as f:
            oru = json.load(f)
        
        compatibility_issues = []
        compatibility_score = 100
        
        # Check Open Fronthaul compatibility
        odu_oh = odu.get('interfaces', {}).get('open_fronthaul', {})
        oru_oh = oru.get('interfaces', {}).get('open_fronthaul', {})
        
        # Version compatibility
        odu_version = odu_oh.get('version', 'N/A')
        oru_version = oru_oh.get('version', 'N/A')
        
        if odu_version != oru_version:
            compatibility_issues.append(
                f"CRITICAL: Open Fronthaul version mismatch - O-DU: {odu_version}, O-RU: {oru_version}"
            )
            compatibility_score -= 30
        
        # eCPRI compatibility
        odu_ecpri = odu_oh.get('ecpri_version', 'N/A')
        oru_ecpri = oru_oh.get('ecpri_version', 'N/A')
        
        if odu_ecpri != oru_ecpri:
            compatibility_issues.append(
                f"CRITICAL: eCPRI version mismatch - O-DU: {odu_ecpri}, O-RU: {oru_ecpri}"
            )
            compatibility_score -= 25
        
        # VLAN compatibility
        odu_vlan = odu_oh.get('vlan_id', None)
        oru_vlan = oru_oh.get('vlan_id', None)
        
        if odu_vlan and oru_vlan and odu_vlan != oru_vlan:
            compatibility_issues.append(
                f"WARNING: VLAN ID mismatch - O-DU: {odu_vlan}, O-RU: {oru_vlan}. Must be configured identically."
            )
            compatibility_score -= 15
        
        # Priority Code Point (PCP) check
        odu_pcp = odu_oh.get('pcp', None)
        oru_pcp = oru_oh.get('pcp', None)
        
        if odu_pcp and oru_pcp and odu_pcp != oru_pcp:
            compatibility_issues.append(
                f"WARNING: PCP mismatch - O-DU: {odu_pcp}, O-RU: {oru_pcp}. May cause QoS issues."
            )
            compatibility_score -= 10
        
        # Timing window overlap check
        odu_timing = odu_oh.get('timing', {})
        oru_timing = oru_oh.get('timing', {})
        
        if 't2a_max' in odu_timing and 't2a_max' in oru_timing:
            if oru_timing['t2a_max'] > odu_timing['t2a_max']:
                compatibility_issues.append(
                    f"CRITICAL: O-RU T2a_max ({oru_timing['t2a_max']}μs) exceeds O-DU expectations ({odu_timing['t2a_max']}μs)"
                )
                compatibility_score -= 20
        
        # Bandwidth compatibility
        odu_bw = odu.get('capabilities', {}).get('bandwidth', 'N/A')
        oru_bw = oru.get('capabilities', {}).get('bandwidth', 'N/A')
        
        if odu_bw != oru_bw and odu_bw != 'N/A' and oru_bw != 'N/A':
            compatibility_issues.append(
                f"WARNING: Bandwidth mismatch - O-DU: {odu_bw}, O-RU: {oru_bw}"
            )
            compatibility_score -= 10
        
        result = {
            "odu_vendor": odu.get('vendor', 'Unknown'),
            "oru_vendor": oru.get('vendor', 'Unknown'),
            "compatibility_score": compatibility_score,
            "status": "COMPATIBLE" if compatibility_score >= 70 else "INCOMPATIBLE",
            "issues": compatibility_issues,
            "recommendation": (
                "Integration is feasible with minor configuration adjustments." 
                if compatibility_score >= 70 
                else "Significant compatibility issues detected. Consider alternative vendor pairing."
            )
        }
        
        return result
        
    except Exception as e:
        return {"error": f"Compatibility check failed: {str(e)}"}