# O-RAN Open Fronthaul Interface Specification Overview

## Version 7.0 - Key Requirements

### 1. Interface Architecture

The Open Fronthaul interface connects the O-DU (Open Distributed Unit) to the O-RU (Open Radio Unit). It consists of three planes:

- **Control Plane (C-Plane)**: Real-time control messages
- **User Plane (U-Plane)**: User data transmission  
- **Synchronization Plane (S-Plane)**: Timing and synchronization
- **Management Plane (M-Plane)**: Configuration via NETCONF/YANG

### 2. Transport Requirements

#### 2.1 eCPRI Protocol
- **Version**: eCPRI v2.0 is MANDATORY for O-RAN compliance
- **Transport**: Ethernet-based, typically over 25G or 100G links
- **Message Types**: 
  - Type 0: IQ Data
  - Type 2: Real-time control data
  - Type 5: Link maintenance

#### 2.2 VLAN Configuration
- **VLAN Tagging**: 802.1Q required
- **VLAN ID**: Must be identical on O-DU and O-RU
- **PCP (Priority Code Point)**: 
  - Recommended: PCP=7 for C-Plane (highest priority)
  - Recommended: PCP=6 or 7 for U-Plane
  - PCP mismatch can cause QoS issues and timing problems

### 3. Timing Requirements

Critical timing parameters that MUST be compatible between O-DU and O-RU:

#### 3.1 T2a Timing Window
**T2a** is the maximum time between O-DU transmission and expected O-RU reception of control messages.

- **T2a_max**: Maximum acceptable delay (typically 285 microseconds)
- **T2a_min**: Minimum acceptable delay (typically 70-100 microseconds)
- **Impact of Mismatch**: 
  - If O-RU T2a_max > O-DU T2a_max: CRITICAL FAILURE - Messages will be dropped
  - If O-RU T2a_min < O-DU T2a_min: WARNING - Requires high-performance fronthaul

#### 3.2 Ta3 Timing Window  
**Ta3** is the maximum processing time in the O-RU.

- **Typical Value**: 280-300 microseconds
- **Impact**: Must be within O-DU's expected range

### 4. Functional Split Options

#### 4.1 Split 7-2x (Most Common)
- **DU Processing**: MAC, High-PHY
- **RU Processing**: Low-PHY, RF
- **Bandwidth Requirements**: High (10-100 Gbps depending on configuration)
- **Timing Criticality**: Very high

#### 4.2 Split 8
- **DU Processing**: MAC, High-PHY, Low-PHY  
- **RU Processing**: RF only
- **Bandwidth Requirements**: Lower than 7-2x
- **Timing Criticality**: Moderate

### 5. Bandwidth and Numerology

#### 5.1 Channel Bandwidth Support
- **5G NR Bandwidths**: 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100 MHz
- **Compatibility Rule**: O-RU and O-DU MUST support the same bandwidth
- **Mismatch Impact**: CRITICAL FAILURE - Cannot establish connection

#### 5.2 Numerology (Subcarrier Spacing)
- **Numerology 0**: 15 kHz (FR1 - Sub-6 GHz)
- **Numerology 1**: 30 kHz (FR1 - Sub-6 GHz, FR2 - mmWave)
- **Numerology 2**: 60 kHz (FR2 - mmWave)
- **Numerology 3**: 120 kHz (FR2 - mmWave)

### 6. Beamforming and MIMO

#### 6.1 Beamforming Support
- **Digital Beamforming**: Performed in O-DU
- **Analog/Hybrid Beamforming**: Performed in O-RU
- **Requirement**: O-RU must declare beamforming capabilities

#### 6.2 MIMO Layers
- **Common Configurations**: 2x2, 4x4, 8x8, 64x64 (massive MIMO)
- **Compatibility**: O-DU and O-RU must agree on number of supported layers

### 7. Common Integration Issues

#### 7.1 Version Mismatch
- **Symptom**: Connection failures, protocol errors
- **Root Cause**: Different Open Fronthaul versions (e.g., 6.0 vs 7.0)
- **Resolution**: Upgrade to matching versions - MANDATORY

#### 7.2 eCPRI Version Incompatibility  
- **Symptom**: Frame parsing errors, packet drops
- **Root Cause**: eCPRI 1.0 vs eCPRI 2.0
- **Resolution**: Both components MUST use eCPRI 2.0

#### 7.3 Timing Budget Violations
- **Symptom**: Random packet drops, synchronization loss
- **Root Cause**: T2a_max exceeded, inadequate fronthaul performance
- **Resolution**: 
  - Reduce fronthaul latency (better switches, fiber paths)
  - Adjust timing parameters if vendor allows
  - Consider alternative O-RU with relaxed timing

#### 7.4 QoS Configuration Errors
- **Symptom**: Intermittent performance degradation under load
- **Root Cause**: PCP mismatch, incorrect queue mapping
- **Resolution**: Align PCP values, configure network switches properly

### 8. Compliance Requirements

For O-RAN certification, the following MUST be met:

1. ✅ Open Fronthaul specification version 7.0 or later
2. ✅ eCPRI v2.0 support
3. ✅ VLAN tagging and QoS support (802.1Q)
4. ✅ PTP or SyncE synchronization (G.8275.1 or G.8275.2)
5. ✅ NETCONF/YANG management interface (M-Plane)
6. ✅ Support for required timing windows (T2a, Ta3)
7. ✅ Compatible functional split (7-2x minimum)

### 9. Multi-Vendor Integration Best Practices

#### 9.1 Pre-Integration Validation
Before lab testing:
- Verify specification version alignment (Open Fronthaul, eCPRI)
- Check timing parameter compatibility
- Validate bandwidth and numerology support
- Confirm QoS configuration alignment (VLAN, PCP)

#### 9.2 Integration Testing Phases
1. **Basic Connectivity**: Establish eCPRI connection
2. **Synchronization**: Verify PTP/SyncE lock
3. **C-Plane Testing**: Control message exchange
4. **U-Plane Testing**: IQ data transmission  
5. **Performance Testing**: Throughput, latency, packet loss
6. **Stress Testing**: High load, error conditions

#### 9.3 Common Failure Modes
- **Connection Establishment Failure**: Usually version mismatch
- **Synchronization Loss**: Timing parameter issues, PTP problems
- **Intermittent Packet Loss**: QoS misconfiguration, insufficient bandwidth
- **Performance Degradation**: Timing violations, fronthaul congestion

### 10. Vendor-Specific Considerations

#### 10.1 Parameter Flexibility
Different vendors implement O-RAN specs with varying degrees of configurability:
- **Flexible Vendors**: Allow PCP, timing, VLAN adjustments via M-Plane
- **Rigid Vendors**: Fixed parameters, limited configurability
- **Best Practice**: Prefer vendors with flexible configuration options

#### 10.2 Extensions and Proprietary Features
- Some vendors add proprietary extensions beyond O-RAN specs
- May improve performance but reduce multi-vendor compatibility
- **Recommendation**: Use only standard O-RAN features for multi-vendor deployments

---

## References

- O-RAN Alliance WG4: Open Fronthaul Control, User and Synchronization Plane Specification v07.00
- O-RAN Alliance Architecture Description v05.00
- ETSI TS 138 series: 5G NR specifications
- eCPRI Specification v2.0
- IEEE 802.1Q: VLAN tagging
