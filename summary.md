# MARINA — Project Summary

## Problem

Small fishing operators may benefit from accessible marine information when considering conditions at sea. However, raw forecast data can be difficult to interpret, and an AI system that omits provenance or uncertainty could create a misleading impression of safety.

## Proposed solution

MARINA (Marine Intelligence Agent Network) is a multi-agent marine intelligence and safety decision-support prototype built with Neuro-SAN Studio. A coordinating agent works with a marine-data agent and a coded tool to retrieve public marine forecasts and present them with explicit source information and safety limitations.

## Implementation

The prototype uses a Groq-hosted language model for agent coordination and the Open-Meteo Marine API for live marine forecasts. The tool retrieves hourly wave height, wave direction, wave period, and sea-surface temperature.

Responses include forecast and retrieval timestamps, source details, requested and model coordinates, units, and a list of missing fields. Synthetic observations are available only through an explicit development-sample option. Missing or invalid coordinates and API failures are handled without silently substituting synthetic data.

## Evaluation

The current implementation passed:

- **6 automated tool tests** covering synthetic mode, missing inputs, invalid coordinates, network failures, and empty API responses.
- **7 deterministic evaluation checks** for input validation and explicit synthetic-data labelling.
- **10 live-response metadata checks** for the tested Open-Meteo response, including source, timestamps, coordinates, observations, limitations, and non-synthetic status.

These results demonstrate basic implementation and data-handling behaviour. They do not demonstrate forecast accuracy, improvements in fishing outcomes, or readiness for operational deployment.

## Safety and limitations

The system reports model forecasts, not direct measurements. Forecast conditions may differ from conditions at a particular coastal location. MARINA does not provide navigation clearance and must not be treated as a certified marine safety system or as the sole basis for a safety decision.

## Future work

Potential improvements include broader automated testing, evaluation against independent observed marine data, improved handling of forecast timing and missing values, comparison of agent responses against a structured evaluation set, and usability testing with representative users.

## Conclusion

MARINA demonstrates a multi-agent workflow that integrates a public marine data source with explicit provenance, error handling, and safety-oriented reporting. The current prototype establishes a foundation for further evaluation; additional validation is required before any real-world safety use.
