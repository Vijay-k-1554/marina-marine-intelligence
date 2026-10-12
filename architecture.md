# MARINA Architecture

## 1. Overview

MARINA (Marine Intelligence Agent Network) is a multi-agent prototype for marine information retrieval and safety-oriented decision support. Neuro-SAN Studio coordinates the agent workflow, while a coded tool retrieves marine forecasts from the Open-Meteo Marine API.

## 2. Components

### MarinaCoordinator

The front-facing agent receives the user's request, coordinates the workflow, and presents the resulting information. It should preserve uncertainty and avoid making unsupported safety claims.

### MarineDataAgent

The marine-data sub-agent handles marine-data retrieval tasks and uses the configured marine data tool. It should request coordinates when they are missing instead of inventing them.

### MarineDataTool

Implemented in `coded_tools/marina/marine_data_tool.py`, this component:

1. Validates the location label and coordinates.
2. Returns explicitly labelled synthetic observations only when sample mode is requested.
3. Queries the Open-Meteo Marine API for hourly wave height, wave direction, wave period, and sea-surface temperature.
4. Selects a forecast time and records its timestamp.
5. Returns values with units, requested and model coordinates, source details, retrieval time, and missing-field information.
6. Reports unavailable data when retrieval or response validation fails.

### Language model configuration

`config/llm_config.hocon` configures the Groq-hosted `openai/gpt-oss-120b` model. The API key is supplied through the local environment and must not be committed to version control.

## 3. Data flow

1. The user asks for marine conditions.
2. MarinaCoordinator delegates the marine-data task.
3. MarineDataAgent requests the tool output.
4. MarineDataTool validates inputs and retrieves forecast data, or returns a controlled error.
5. The result is passed back through the agent workflow.
6. The coordinator presents the forecast with its provenance and limitations.

## 4. Data provenance

Live responses identify Open-Meteo as the source and include the source URL, retrieval timestamp, forecast timestamp, requested coordinates, model coordinates, measurement units, and missing fields.

Synthetic samples are clearly identified as development data. They are not substituted for live data when the API fails.

## 5. Error handling and evaluation

The test suite checks synthetic mode, missing location, missing coordinates, invalid coordinates, network failure, and empty API responses.

The evaluation scripts check input handling, synthetic-data labelling, and live-response metadata. These tests do not measure forecast accuracy or prove operational safety.

## 6. Safety limitations

Marine forecasts are model outputs and may not represent exact local coastal conditions. MARINA is a prototype, not a certified navigation or emergency-response system. Its output must not be interpreted as navigation clearance or used as the sole basis for a marine safety decision.
