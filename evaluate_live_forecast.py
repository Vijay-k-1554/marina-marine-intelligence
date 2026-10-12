from coded_tools.marina.marine_data_tool import MarineDataTool

tool = MarineDataTool()

result = tool.invoke(
    {
        "location": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
    },
    {},
)

if result.get("status") != "forecast":
    print("LIVE CHECK UNAVAILABLE")
    print("Status:", result.get("status"))
    print("Message:", result.get("message", result.get("error", "No details")))
    raise SystemExit(0)

checks = {
    "Source identified": bool(result.get("source")),
    "Source URL present": bool(result.get("source_url")),
    "Forecast timestamp present": bool(result.get("forecast_for")),
    "Retrieval timestamp present": bool(result.get("retrieved_at")),
    "Requested coordinates present": bool(result.get("requested_coordinates")),
    "Model coordinates present": bool(result.get("model_coordinates")),
    "Observations are a dictionary": isinstance(result.get("observations"), dict),
    "Missing fields explicitly listed": isinstance(result.get("missing_fields"), list),
    "Safety limitations documented": bool(result.get("limitations")),
    "Live response not marked synthetic": result.get("simulated") is False,
}

for name, passed in checks.items():
    print(f'{"PASS" if passed else "FAIL"}: {name}')

print("\nForecast fields:")
print("Observations:", result.get("observations"))
print("Limitations:", result.get("limitations"))

failed = [name for name, passed in checks.items() if not passed]
if failed:
    raise SystemExit(f"\n{len(failed)} live metadata check(s) failed.")

print(f"\nAll {len(checks)} live metadata checks passed.")
