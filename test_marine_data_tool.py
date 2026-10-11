
import json

from coded_tools.marina.marine_data_tool import MarineDataTool

tool = MarineDataTool()

# Test 1: explicitly requested synthetic observations
sample = tool.invoke(
    {"location": "Test Coastal Area", "use_sample_data": True}, {}
)
print("SAMPLE TEST:")
print(json.dumps(sample, indent=2))

assert sample["status"] == "simulated"
assert sample["simulated"] is True
assert sample["source"] == "MARINA development sample (synthetic)"

# Test 2: live data was not requested, so no conditions are invented
unavailable = tool.invoke(
    {"location": "Test Coastal Area"}, {}
)
print("\nMISSING DATA TEST:")
print(json.dumps(unavailable, indent=2))

assert unavailable["status"] == "unavailable"
assert unavailable["observations"] is None

# Test 3: missing location is rejected
invalid = tool.invoke({}, {})
assert invalid["status"] == "error"

print("\nAll three tests passed.")
