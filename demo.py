from strands import Agent
from tools.oran_tools import analyze_oran_config, check_compatibility
from tools.kb_tool import search_oran_specs

SYSTEM_PROMPT = """You are AutoRAN Advisor, an expert AI assistant specializing in Open RAN (O-RAN) 
multi-vendor integration and interoperability analysis. Provide clear, actionable guidance for 
network operators deploying multi-vendor O-RAN networks."""

def run_demo():
    print("=" * 80)
    print("🎯 AutoRAN Advisor - LIVE DEMO")
    print("   Breaking Barriers in O-RAN Multi-Vendor Integration")
    print("=" * 80)
    
    agent = Agent(
    tools=[analyze_oran_config, check_compatibility, search_oran_specs],  # ← ADD search_oran_specs
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    system_prompt=SYSTEM_PROMPT
)
    
    scenarios = [
        {
            "title": "Scenario 1: Individual Component Analysis",
            "query": "Analyze the O-DU configuration at sample_configs/vendor_a_odu.json and tell me if it's compliant with O-RAN standards"
        },
        {
            "title": "Scenario 2: Compatible Vendor Pairing",
            "query": "Check if Vendor A O-DU (sample_configs/vendor_a_odu.json) is compatible with Vendor B O-RU (sample_configs/vendor_b_oru.json). What issues exist and how can they be resolved?"
        },
        {
            "title": "Scenario 3: Incompatible Vendor Detection",
            "query": "Assess compatibility between Vendor A O-DU and Vendor C O-RU (sample_configs/incompatible_vendor_c_oru.json). Should we proceed with this integration?"
        },
        {
            "title": "Scenario 4: Procurement Decision Support",
            "query": "I'm deploying Vendor A's O-DU. Should I buy Vendor B or Vendor C O-RU? Compare both options and give me a recommendation with technical justification."
        },
        {
            "title": "Scenario 5: Specification Reference",
            "query": "What are the O-RAN specification requirements for PCP configuration? Search the knowledge base and then check if our Vendor A and Vendor B configurations comply."
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n\n{'=' * 80}")
        print(f"📋 {scenario['title']}")
        print(f"{'=' * 80}")
        print(f"\n❓ Query: {scenario['query']}\n")
        
        input("Press ENTER to see AutoRAN Advisor's analysis... ")
        
        print("\n🤖 AutoRAN Advisor Response:\n")
        print("-" * 80)
        
        response = agent(scenario['query'])
        print(response)
        
        print("-" * 80)
        
        if i < len(scenarios):
            input("\n⏭️  Press ENTER for next scenario...")
    
    print("\n\n" + "=" * 80)
    print("✅ Demo Complete!")
    print("=" * 80)
    print("\n💡 Key Benefits Demonstrated:")
    print("   ✓ Automated compliance validation")
    print("   ✓ Proactive compatibility assessment")
    print("   ✓ Clear, actionable recommendations")
    print("   ✓ Reduces integration time from months to days")
    print("   ✓ Prevents costly deployment failures")
    print("\n🎯 AutoRAN Advisor: Breaking Barriers in O-RAN Integration\n")

if __name__ == "__main__":
    run_demo()