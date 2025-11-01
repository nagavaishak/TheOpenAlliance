from strands import tool
import boto3
import json

# Initialize Bedrock Agent Runtime client
bedrock_agent = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

# Your Knowledge Base ID - REPLACE THIS!
KNOWLEDGE_BASE_ID = "C1EBOCHSX5"

@tool
def search_oran_specs(query: str) -> str:
    """
    Search O-RAN specifications and compatibility guidelines from the knowledge base.
    Use this to find authoritative information about O-RAN standards, timing requirements,
    version compatibility, and best practices.
    
    Args:
        query: Natural language question about O-RAN specifications
        
    Returns:
        Relevant excerpts from O-RAN documentation with citations
    """
    try:
        response = bedrock_agent.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={
                'text': query
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 5
                }
            }
        )
        
        # Extract and format results
        results = []
        for i, result in enumerate(response['retrievalResults'], 1):
            content = result['content']['text']
            # Get source information
            location = result.get('location', {})
            if 's3Location' in location:
                source = location['s3Location'].get('uri', 'Unknown source')
            else:
                source = 'O-RAN Specifications'
            
            score = result.get('score', 0)
            
            results.append(
                f"**[Source {i}]** (Relevance: {score:.2f})\n"
                f"From: {source}\n\n"
                f"{content}\n"
            )
        
        if not results:
            return "No relevant information found in O-RAN specifications knowledge base."
        
        formatted_results = "\n" + "="*80 + "\n"
        formatted_results += "📚 O-RAN Specification References:\n"
        formatted_results += "="*80 + "\n\n"
        formatted_results += "\n---\n\n".join(results)
        
        return formatted_results
        
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}\n\nNote: Ensure Knowledge Base ID is correct and you have proper IAM permissions."