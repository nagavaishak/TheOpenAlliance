from tools.oran_tools import analyze_oran_config, check_compatibility
import json

print("=" * 60)
print("Testing O-RAN Configuration Analysis Tool")
print("=" * 60)

# Test 1: Analyze Vendor A O-DU
print("\n1. Analyzing Vendor A O-DU configuration...")
result1 = analyze_oran_config("sample_configs/vendor_a_odu.json")
print(json.dumps(result1, indent=2))

# Test 2: Analyze Vendor B O-RU
print("\n2. Analyzing Vendor B O-RU configuration...")
result2 = analyze_oran_config("sample_configs/vendor_b_oru.json")
print(json.dumps(result2, indent=2))

# Test 3: Check compatibility
print("\n3. Checking Vendor A O-DU + Vendor B O-RU compatibility...")
result3 = check_compatibility(
    "sample_configs/vendor_a_odu.json",
    "sample_configs/vendor_b_oru.json"
)
print(json.dumps(result3, indent=2))

# Test 4: Check incompatible configuration
print("\n4. Checking Vendor A O-DU + Vendor C O-RU compatibility...")
result4 = check_compatibility(
    "sample_configs/vendor_a_odu.json",
    "sample_configs/incompatible_vendor_c_oru.json"
)
print(json.dumps(result4, indent=2))