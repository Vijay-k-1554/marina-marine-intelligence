import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from coded_tools.marina.marine_data_tool import MarineDataTool

tool = MarineDataTool()


# Test 1: Explicitly requested synthetic observations
sample = tool.invoke(
    {"location": "Test Coastal Area", "use_sample_data": True}, {}
)

assert sample["status"] == "simulated"
assert sample["simulated"] is True
assert sample["source"] == "MARINA development sample (synthetic)"
print("PASS: Explicit synthetic sample")


# Test 2: Live data requested without coordinates
missing_coords = tool.invoke(
    {"location": "Test Coastal Area"}, {}
)

assert missing_coords["status"] == "error"
assert missing_coords["observations"] is None
assert missing_coords["simulated"] is False
print("PASS: Missing coordinates rejected")


# Test 3: Missing location
missing_location = tool.invoke({}, {})
assert missing_location["status"] == "error"
print("PASS: Missing location rejected")


# Test 4: Invalid coordinates must be rejected before API access
with patch(
    "coded_tools.marina.marine_data_tool.urlopen"
) as mock_urlopen:
    invalid_coords = tool.invoke(
        {
            "location": "Test Coastal Area",
            "latitude": 200,
            "longitude": 80,
        },
        {},
    )

    assert invalid_coords["status"] == "error"
    assert invalid_coords["observations"] is None
    mock_urlopen.assert_not_called()

print("PASS: Invalid coordinates rejected without API access")


# Test 5: Network/API failure must not create fake observations
with patch(
    "coded_tools.marina.marine_data_tool.urlopen",
    side_effect=URLError("Simulated network failure"),
):
    api_failure = tool.invoke(
        {
            "location": "Test Coastal Area",
            "latitude": 13.0827,
            "longitude": 80.2707,
        },
        {},
    )

assert api_failure["status"] == "unavailable"
assert api_failure["observations"] is None
assert api_failure["simulated"] is False
print("PASS: API failure handled safely")


# Test 6: Malformed or empty API response
mock_response = MagicMock()
mock_response.read.return_value = b"{}"

mock_context = MagicMock()
mock_context.__enter__.return_value = mock_response
mock_context.__exit__.return_value = False

with patch(
    "coded_tools.marina.marine_data_tool.urlopen",
    return_value=mock_context,
):
    malformed_response = tool.invoke(
        {
            "location": "Test Coastal Area",
            "latitude": 13.0827,
            "longitude": 80.2707,
        },
        {},
    )

assert malformed_response["status"] == "unavailable"
assert malformed_response["observations"] is None
assert malformed_response["simulated"] is False
print("PASS: Empty API response handled safely")


print("\nAll six tests passed.")
