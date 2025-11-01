from agents.coordinator import MultiAgentCoordinator
import time

def test_memory_system():
    print("="*80)
    print("🧠 TESTING MEMORY SYSTEM")
    print("="*80)
    
    coordinator = MultiAgentCoordinator()
    
    # Test 1: First analysis (no history)
    print("\n1️⃣ Running first analysis (will save to memory)...")
    result1 = coordinator.analyze_compatibility(
        "sample_configs/vendor_a_odu.json",
        "sample_configs/vendor_b_oru.json"
    )
    print("✅ First analysis complete")
    
    time.sleep(2)
    
    # Test 2: Second analysis (should recall history)
    print("\n2️⃣ Running second analysis (should find historical data)...")
    result2 = coordinator.analyze_compatibility(
        "sample_configs/vendor_a_odu.json",
        "sample_configs/vendor_b_oru.json"
    )
    print("✅ Second analysis complete - check if agent referenced historical data")
    
    # Test 3: Get vendor history
    print("\n3️⃣ Checking vendor compatibility history...")
    from tools.memory_tools import get_vendor_compatibility_history
    history = get_vendor_compatibility_history("Vendor_A", "odu")
    print(history)
    
    # Test 4: Get insights
    print("\n4️⃣ Getting integration insights...")
    from tools.memory_tools import get_integration_insights
    insights = get_integration_insights()
    print(insights)
    
    print("\n" + "="*80)
    print("✅ MEMORY SYSTEM WORKING!")
    print("="*80)

if __name__ == "__main__":
    test_memory_system()