from strands import Agent
from strands_tools import calculator, current_time
from tools.oran_tools import analyze_oran_config, check_compatibility
import sys
from tools.kb_tool import search_oran_specs
from strands.models.bedrock import BedrockModel

# System prompt to give the agent O-RAN expertise
SYSTEM_PROMPT = """You are AutoRAN Advisor, an expert AI assistant specializing in Open RAN (O-RAN) 
multi-vendor integration and interoperability analysis.

IMPORTANT: You have access to authoritative O-RAN specifications via search_oran_specs tool.
When users ask about standards, requirements, or best practices, ALWAYS search the knowledge base
first to provide specification-backed answers.

Your expertise includes:
- O-RAN Alliance specifications (Open Fronthaul, F1, E2, O1, O2 interfaces)
- Multi-vendor integration challenges and best practices
- Timing requirements and synchronization issues
- Configuration validation and compliance checking
- Compatibility assessment between different vendors

When analyzing configurations:
1. Search specifications when discussing standards or requirements
2. Use analyze_oran_config for individual component analysis
3. Use check_compatibility for vendor pairing assessment
4. Cite specific O-RAN documents when making compliance statements
5. Provide actionable recommendations with spec references

Your goal: Help operators deploy multi-vendor O-RAN networks successfully by identifying 
compatibility issues BEFORE costly integration testing begins."""

def create_advisor_agent():
    """Create and configure the AutoRAN Advisor agent"""
    agent = Agent(
        tools=[
            analyze_oran_config,
            check_compatibility,
            search_oran_specs,  # ← ADD THIS LINE
            calculator,
            current_time
        ],
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        system_prompt=SYSTEM_PROMPT
    )
    return agent

def main():
    print("=" * 80)
    print("🤖 AutoRAN Advisor - AI-Powered O-RAN Integration Assistant")
    print("=" * 80)
    print("\nInitializing agent with Claude Sonnet 4.5...\n")
    
    agent = create_advisor_agent()
    
    # Interactive mode
    print("Available sample configurations:")
    print("  - sample_configs/vendor_a_odu.json (O-DU)")
    print("  - sample_configs/vendor_b_oru.json (O-RU)")
    print("  - sample_configs/incompatible_vendor_c_oru.json (O-RU)\n")
    
    print("Example queries:")
    print('  - "Analyze the Vendor A O-DU configuration"')
    print('  - "Can I integrate Vendor A O-DU with Vendor B O-RU?"')
    print('  - "What are the compatibility issues between Vendor A and Vendor C?"')
    print('  - "Compare all three vendors and recommend the best O-RU for Vendor A O-DU"\n')
    
    print("Type 'quit' or 'exit' to end session\n")
    print("-" * 80)
    
    while True:
        try:
            user_input = input("\n🔍 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using AutoRAN Advisor!")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 AutoRAN Advisor is analyzing...\n")
            
            # Get agent response
            response = agent(user_input)
            
            print("=" * 80)
            print(response)
            print("=" * 80)
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Thank you for using AutoRAN Advisor!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again with a different query.\n")

if __name__ == "__main__":
    main()