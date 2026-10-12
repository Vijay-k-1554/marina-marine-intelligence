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

- Python 3.14 (tested development environment; project metadata permits Python 3.11+)
- Neuro-SAN / Neuro-SAN Studio
- Groq-hosted language model (`openai/gpt-oss-120b`)
- Open-Meteo Marine API
- `uv` for dependency management

## Setup

Prerequisites: Python 3.11 or later and `uv`. The currently verified development environment uses Python 3.14.6.

1. Clone the repository:

   ```powershell
   git clone https://github.com/Vijay-k-1554/marina-marine-intelligence.git
   cd marina-marine-intelligence
   ```

2. Install the locked dependencies:

   ```powershell
   uv sync --locked
   ```

3. Create your local environment file from the template:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Open `.env` and replace the placeholder with your own Groq API key:

   ```text
   GROQ_API_KEY=your_groq_api_key_here
   ```

   Never commit `.env` or publish API keys. The `.env.example` file contains only a placeholder.

## Run the checks

```powershell
uv run python test_marine_data_tool.py
uv run python evaluate_marina.py
uv run python evaluate_live_forecast.py
```

The first two scripts test tool behaviour and input handling. The live evaluation requires internet access and a reachable Open-Meteo API; it may fail temporarily if the service is unavailable.

## Run the agent

In PowerShell, from the repository root:

```powershell
$env:AGENT_TOOL_PATH = "coded_tools"
$env:AGENT_TOOL_PATH_ONLY = "true"
$env:PYTHONPATH = "$PWD"
uv run ns chat marina --one-shot
```

Ask the agent to assess marine conditions for a location. Live forecasts require valid latitude and longitude; do not assume that a place name alone is sufficient.

## Project documents

- `architecture.md` — components and data flow.
- `summary.md` — project overview and evaluation results.

## Data integrity and safety

- Synthetic observations are returned only when explicitly requested.
- API failures do not silently fall back to synthetic observations.
- Forecasts are model outputs, not direct measurements.
- Model coordinates may differ from requested coordinates.
- Local coastal conditions may differ from forecast values.
- MARINA does not provide navigation clearance and must not be the sole basis for marine safety decisions.

## Evaluation results

The current development version passed:

- Six marine-tool tests.
- Seven deterministic evaluation checks.
- Ten live-response metadata checks for the tested Open-Meteo response.

These checks validate software behaviour and response metadata, not the predictive accuracy of marine forecasts.
