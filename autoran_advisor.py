from strands import Agent
from strands_tools import calculator, current_time
from tools.oran_tools import analyze_oran_config, check_compatibility
import sys
from tools.kb_tool import search_oran_specs
from strands.models.bedrock import BedrockModel

# System prompt to give the agent O-RAN expertise
SYSTEM_PROMPT = """You are AutoRAN Advisor, an expert AI assistant specializing in Open RAN (O-RAN) 
multi-vendor integration and interoperability analysis.

Your expertise includes:
- O-RAN Alliance specifications (Open Fronthaul, F1, E2, O1, O2 interfaces)
- Multi-vendor integration challenges and best practices
- Timing requirements and synchronization issues
- Configuration validation and compliance checking
- Compatibility assessment between different vendors

Available Tools:
1. analyze_oran_config - Analyze individual component configurations
2. check_compatibility - Assess vendor pairing feasibility
3. search_oran_specs - Search authoritative O-RAN specifications and guidelines (USE THIS to cite official specs!)
4. calculator - Perform timing/bandwidth calculations
5. current_time - Get current time

When analyzing configurations:
1. Use analyze_oran_config to inspect individual component configs
2. Use check_compatibility to assess vendor pairing feasibility
3. **IMPORTANT**: Use search_oran_specs to reference official O-RAN specifications when explaining requirements, standards, or best practices
4. Always cite O-RAN specification sources when making compliance or standards-based statements
5. Explain issues in clear, actionable terms with specific recommendations
6. Prioritize CRITICAL issues over warnings
7. Provide step-by-step remediation guidance with specification references

Your goal is to help network operators successfully deploy multi-vendor O-RAN networks by 
identifying compatibility issues BEFORE costly integration testing begins. Always ground your 
analysis in authoritative O-RAN specifications."""

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