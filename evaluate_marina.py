"""Lightweight evaluation checks for MARINA marine data responses."""

from coded_tools.marina.marine_data_tool import MarineDataTool

tool = MarineDataTool()
passed = 0


def check(name, condition):
    global passed
    if not condition:
        raise AssertionError(f"FAIL: {name}")
    passed += 1
    print(f"PASS: {name}")


# Evaluation 1: Missing coordinates must not produce a forecast.
result = tool.invoke({"location": "Chennai"}, {})

check("Missing coordinates are rejected", result.get("status") == "error")
check("Missing coordinates produce no observations",
      result.get("observations") is None)
check("Missing coordinates are not marked simulated",
      result.get("simulated") is False)


# Evaluation 2: Synthetic data must be explicitly requested and labelled.
sample = tool.invoke(
    {"location": "Evaluation Sample", "use_sample_data": True}, {}
)

check("Sample mode is explicitly labelled",
      sample.get("status") == "simulated"
      and sample.get("simulated") is True)
check("Sample source is identified",
      sample.get("source") == "MARINA development sample (synthetic)")


# Evaluation 3: Invalid coordinates must not trigger a live request.
result = tool.invoke(
    {"location": "Chennai", "latitude": 200, "longitude": 80}, {}
)

check("Out-of-range coordinates are rejected",
      result.get("status") == "error")
check("Invalid coordinates return no observations",
      result.get("observations") is None)


print(f"\nEvaluation complete: {passed} checks passed.")
