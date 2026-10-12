# MARINA — Marine Intelligence Agent Network

MARINA is a multi-agent marine intelligence and safety decision-support prototype for small fishing operators. It retrieves public marine forecast data and presents observations with their source, timestamps, units, coordinates, and limitations.

## Key features

- Multi-agent workflow built with Neuro-SAN Studio.
- Public marine forecasts from the Open-Meteo Marine API.
- Explicitly labelled synthetic data for development and demonstrations.
- Input validation and handling of unavailable or malformed API responses.
- Safety-oriented output that distinguishes model forecasts from direct observations.
- Automated tool tests and evaluation scripts.

## Technology stack

- Python
- Neuro-SAN / Neuro-SAN Studio
- Groq-hosted language model (`openai/gpt-oss-120b`)
- Open-Meteo Marine API
- `uv` for Python environment and dependency management

## Setup

1. Install Python and `uv`.
2. Clone this repository and enter its directory.
3. Install dependencies:

   ```powershell
   uv sync
   ```

4. Create a local `.env` file containing your Groq API key:

   ```text
   GROQ_API_KEY=your_groq_api_key
   ```

   Never commit `.env` or publish API keys.

## Run the checks

```powershell
uv run python test_marine_data_tool.py
uv run python evaluate_marina.py
uv run python evaluate_live_forecast.py
```

The live evaluation requires internet access and a reachable Open-Meteo API. It may fail temporarily if the service is unavailable.

## Run the agent

In PowerShell, from the repository root:

```powershell
$env:AGENT_TOOL_PATH = "coded_tools"
$env:AGENT_TOOL_PATH_ONLY = "true"
$env:PYTHONPATH = "$PWD"
uv run ns chat marina --one-shot
```

Ask the agent to assess marine conditions for a location. Live forecasts require valid latitude and longitude; do not assume that a place name alone is sufficient.

## Data integrity and safety

- Synthetic observations are returned only when explicitly requested.
- API failures do not silently fall back to synthetic observations.
- Forecasts are model outputs, not direct measurements.
- Model coordinates may differ from requested coordinates.
- Local coastal conditions may differ from forecast values.
- MARINA does not provide navigation clearance and must not be the sole basis for marine safety decisions.

## Project documents

- `architecture.md` — components and data flow.
- `summary.md` — project overview and evaluation results.

## Current evaluation results

- Six marine-tool tests passed.
- Seven deterministic evaluation checks passed.
- Ten live-response metadata checks passed for the tested Open-Meteo response.

These checks validate software behaviour and response metadata, not the predictive accuracy of the marine forecast.
