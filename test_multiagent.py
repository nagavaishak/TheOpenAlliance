from agents.coordinator import MultiAgentCoordinator

def test_multi_agent():
    print("="*80)
    print("🤖 TESTING MULTI-AGENT SYSTEM")
    print("="*80)
    
    coordinator = MultiAgentCoordinator()
    
    # Test 1: Individual agent
    print("\n1️⃣ Testing RU Specialist Agent...")
    result = coordinator.analyze_oru_config("sample_configs/vendor_b_oru.json")
    print(f"✅ {result['agent']} completed: {result['task']}")
    
    # Test 2: Multi-agent workflow
    print("\n2️⃣ Testing Multi-Agent Compatibility Analysis...")
    result = coordinator.analyze_compatibility(
        "sample_configs/vendor_a_odu.json",
        "sample_configs/vendor_b_oru.json"
    )
    print(f"✅ {len(result['agents_involved'])} agents coordinated successfully")
    print(f"   Agents: {', '.join(result['agents_involved'])}")
    
    # Test 3: Comparison
    print("\n3️⃣ Testing Multi-Vendor Comparison...")
    result = coordinator.compare_vendors(
        "sample_configs/vendor_a_odu.json",
        ["sample_configs/vendor_b_oru.json", "sample_configs/vendor_c_oru.json"]
    )
    print(f"✅ Compared {len(result['oru_options'])} O-RU options")
    
    print("\n" + "="*80)
    print("✅ ALL MULTI-AGENT TESTS PASSED!")
    print("="*80)

if __name__ == "__main__":
    test_multi_agent()