from strands import tool
import boto3
from datetime import datetime
import json
import hashlib
from typing import Dict, List

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('AutoRAN-CompatibilityHistory')

def _generate_analysis_id(vendor_pair: str) -> str:
    """Generate unique ID for vendor pair"""
    return hashlib.md5(vendor_pair.encode()).hexdigest()[:16]

@tool
def save_compatibility_analysis(
    odu_vendor: str,
    oru_vendor: str,
    compatibility_score: int,
    status: str,
    issues: str,
    recommendations: str
) -> str:
    """
    Save compatibility analysis results to persistent memory (DynamoDB).
    This allows the system to learn from past analyses and build a knowledge base
    of vendor compatibility patterns.
    
    Args:
        odu_vendor: O-DU vendor name
        oru_vendor: O-RU vendor name
        compatibility_score: Score from 0-100
        status: COMPATIBLE or INCOMPATIBLE
        issues: Description of compatibility issues
        recommendations: Integration recommendations
        
    Returns: Confirmation message with analysis ID
    """
    try:
        vendor_pair = f"{odu_vendor}_{oru_vendor}"
        analysis_id = _generate_analysis_id(vendor_pair)
        timestamp = int(datetime.now().timestamp())
        
        item = {
            'analysis_id': analysis_id,
            'timestamp': timestamp,
            'vendor_pair': vendor_pair,
            'odu_vendor': odu_vendor,
            'oru_vendor': oru_vendor,
            'compatibility_score': compatibility_score,
            'status': status,
            'issues': issues,
            'recommendations': recommendations,
            'analysis_date': datetime.now().isoformat()
        }
        
        table.put_item(Item=item)
        
        return f"✅ Saved analysis for {vendor_pair} (Score: {compatibility_score}, ID: {analysis_id})"
        
    except Exception as e:
        return f"❌ Failed to save analysis: {str(e)}"

@tool
def recall_compatibility_analysis(odu_vendor: str, oru_vendor: str) -> str:
    """
    Retrieve past compatibility analysis from memory for the given vendor pair.
    Uses historical data to provide informed recommendations based on previous integrations.
    
    Args:
        odu_vendor: O-DU vendor name
        oru_vendor: O-RU vendor name
        
    Returns: Historical analysis data or message if not found
    """
    try:
        vendor_pair = f"{odu_vendor}_{oru_vendor}"
        analysis_id = _generate_analysis_id(vendor_pair)
        
        # Query for most recent analysis
        response = table.query(
            KeyConditionExpression='analysis_id = :id',
            ExpressionAttributeValues={':id': analysis_id},
            ScanIndexForward=False,  # Most recent first
            Limit=1
        )
        
        if response['Items']:
            item = response['Items'][0]
            return f"""
📊 **Historical Analysis Found**

**Vendor Pair**: {item['vendor_pair']}
**Previous Score**: {item['compatibility_score']}/100
**Status**: {item['status']}
**Analysis Date**: {item['analysis_date']}

**Previous Issues**: {item['issues']}

**Previous Recommendations**: {item['recommendations']}

💡 This historical data can inform current integration decisions.
            """
        else:
            return f"📭 No historical analysis found for {vendor_pair}. This is a new vendor combination."
            
    except Exception as e:
        return f"❌ Failed to recall analysis: {str(e)}"

@tool
def get_vendor_compatibility_history(vendor_name: str, role: str = "any") -> str:
    """
    Get compatibility history for a specific vendor across all pairings.
    Helps identify vendors with consistent compatibility issues or successes.
    
    Args:
        vendor_name: Vendor name to search for
        role: "odu", "oru", or "any" to filter by role
        
    Returns: Summary of vendor's compatibility history
    """
    try:
        # Scan table for vendor (note: expensive, use sparingly)
        if role == "odu":
            filter_expr = 'odu_vendor = :vendor'
        elif role == "oru":
            filter_expr = 'oru_vendor = :vendor'
        else:
            filter_expr = 'odu_vendor = :vendor OR oru_vendor = :vendor'
        
        response = table.scan(
            FilterExpression=filter_expr,
            ExpressionAttributeValues={':vendor': vendor_name},
            Limit=10  # Last 10 analyses
        )
        
        if not response['Items']:
            return f"📭 No compatibility history found for vendor: {vendor_name}"
        
        items = response['Items']
        avg_score = sum(item['compatibility_score'] for item in items) / len(items)
        compatible_count = sum(1 for item in items if item['status'] == 'COMPATIBLE')
        
        summary = f"""
📊 **Vendor Compatibility History: {vendor_name}**

**Total Analyses**: {len(items)}
**Average Compatibility Score**: {avg_score:.1f}/100
**Successful Integrations**: {compatible_count}/{len(items)}
**Success Rate**: {(compatible_count/len(items)*100):.1f}%

**Recent Pairings**:
"""
        for item in items[:5]:
            summary += f"\n- {item['vendor_pair']}: {item['compatibility_score']}/100 ({item['status']})"
        
        return summary
        
    except Exception as e:
        return f"❌ Failed to retrieve vendor history: {str(e)}"

@tool
def get_integration_insights() -> str:
    """
    Analyze all compatibility data to provide insights and patterns.
    Identifies common issues, best practices, and vendor trends.
    
    Returns: Analysis insights from historical data
    """
    try:
        # Scan recent analyses
        response = table.scan(Limit=50)
        
        if not response['Items']:
            return "📭 No historical data available yet. Start analyzing configurations to build insights!"
        
        items = response['Items']
        
        # Calculate statistics
        total = len(items)
        avg_score = sum(item['compatibility_score'] for item in items) / total
        compatible = sum(1 for item in items if item['status'] == 'COMPATIBLE')
        
        # Find most compatible pairs
        top_pairs = sorted(items, key=lambda x: x['compatibility_score'], reverse=True)[:3]
        
        insights = f"""
🧠 **Integration Insights from {total} Analyses**

**Overall Statistics**:
- Average Compatibility Score: {avg_score:.1f}/100
- Success Rate: {(compatible/total*100):.1f}%
- Compatible Pairs: {compatible}/{total}

**Top Compatible Vendor Pairs**:
"""
        for i, pair in enumerate(top_pairs, 1):
            insights += f"\n{i}. {pair['vendor_pair']}: {pair['compatibility_score']}/100"
        
        insights += "\n\n💡 **Recommendation**: Focus on vendor pairs with proven compatibility history to reduce integration risk."
        
        return insights
        
    except Exception as e:
        return f"❌ Failed to generate insights: {str(e)}"