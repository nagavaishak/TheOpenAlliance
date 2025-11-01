import json
from agents.coordinator import MultiAgentCoordinator

# Initialize coordinator (cold start)
coordinator = None

def lambda_handler(event, context):
    """
    AWS Lambda handler for AutoRAN Advisor
    
    Event format:
    {
        "action": "analyze_compatibility",
        "odu_path": "sample_configs/vendor_a_odu.json",
        "oru_path": "sample_configs/vendor_b_oru.json"
    }
    """
    global coordinator
    
    # Initialize on cold start
    if coordinator is None:
        coordinator = MultiAgentCoordinator()
    
    try:
        action = event.get('action')
        
        if action == 'analyze_compatibility':
            odu_path = event.get('odu_path')
            oru_path = event.get('oru_path')
            
            result = coordinator.analyze_compatibility(odu_path, oru_path)
            
            return {
                'statusCode': 200,
                'body': json.dumps(result, default=str),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        elif action == 'analyze_oru':
            config_path = event.get('config_path')
            result = coordinator.analyze_oru_config(config_path)
            
            return {
                'statusCode': 200,
                'body': json.dumps(result, default=str),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        elif action == 'analyze_odu':
            config_path = event.get('config_path')
            result = coordinator.analyze_odu_config(config_path)
            
            return {
                'statusCode': 200,
                'body': json.dumps(result, default=str),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Unknown action: {action}'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
