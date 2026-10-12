
"""Marine forecast tool for MARINA.

Supports explicitly labelled synthetic samples and public Open-Meteo forecasts.
Forecasts are informational, not direct measurements or navigation clearance.
"""

import asyncio
import math
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from neuro_san.interfaces.coded_tool import CodedTool


API_URL = "https://marine-api.open-meteo.com/v1/marine"
TIMEOUT_SECONDS = 12

MARINE_FIELDS = [
    "wave_height",
    "wave_direction",
    "wave_period",
    "sea_surface_temperature",
]


class MarineDataTool(CodedTool):
    def invoke(
        self, args: dict[str, Any], sly_data: dict[str, Any]
    ) -> dict[str, Any]:
        location = str(args.get("location", "")).strip()

        if not location:
            return {
                "status": "error",
                "error": "A location label is required.",
                "simulated": False,
            }

        # Synthetic data is returned only when explicitly requested.
        if args.get("use_sample_data") is True:
            return {
                "status": "simulated",
                "location": location,
                "source": "MARINA development sample (synthetic)",
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "simulated": True,
                "observations": {
                    "wind_speed_kmh": 18,
                    "wave_height_m": 1.2,
                    "visibility_km": 8,
                },
                "message": (
                    "Synthetic test values only. They do not describe actual "
                    "conditions and must not be used for navigation or safety."
                ),
            }

        latitude = self._coordinate(args.get("latitude"), -90, 90)
        longitude = self._coordinate(args.get("longitude"), -180, 180)

        if latitude is None or longitude is None:
            return {
                "status": "error",
                "location": location,
                "simulated": False,
                "observations": None,
                "message": (
                    "Valid latitude and longitude are required for live "
                    "marine forecasts. No conditions were assessed."
                ),
            }

        query = urlencode({
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(MARINE_FIELDS),
            "forecast_days": 1,
            "timezone": "GMT",
            "length_unit": "metric",
        })

        request = Request(
            f"{API_URL}?{query}",
            headers={"User-Agent": "MARINA-Hackathon/1.0"},
        )

        try:
            with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (
            HTTPError, URLError, TimeoutError, OSError,
            json.JSONDecodeError,
        ) as exc:
            return self._unavailable(
                location, latitude, longitude,
                f"Marine forecast retrieval failed: {exc}",
            )

        hourly = payload.get("hourly")
        units = payload.get("hourly_units", {})
        times = hourly.get("time") if isinstance(hourly, dict) else None

        if not isinstance(times, list) or not times:
            return self._unavailable(
                location, latitude, longitude,
                "The API returned no hourly forecast timestamps.",
            )

        # Select the first forecast hour that has not already passed.
        now_hour = datetime.now(timezone.utc).replace(
            minute=0, second=0, microsecond=0
        )
        target_time = now_hour.strftime("%Y-%m-%dT%H:%M")

        index = next(
            (i for i, value in enumerate(times)
             if isinstance(value, str) and value >= target_time),
            None,
        )

        if index is None:
            return self._unavailable(
                location, latitude, longitude,
                "No upcoming forecast hour was available in the API response.",
            )

        observations = {}
        missing_fields = []

        for field in MARINE_FIELDS:
            values = hourly.get(field)
            value = values[index] if isinstance(values, list) and index < len(values) else None

            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                missing_fields.append(field)
                continue

            observations[field] = {
                "value": value,
                "unit": units.get(field, "unknown"),
            }

        if not observations:
            return self._unavailable(
                location, latitude, longitude,
                "No valid marine forecast values were returned.",
            )

        return {
            "status": "forecast",
            "location": location,
            "source": "Open-Meteo Marine API",
            "source_url": "https://open-meteo.com/en/docs/marine-weather-api",
            "simulated": False,
            "forecast_for": times[index],
            "timezone": "GMT",
            "requested_coordinates": {
                "latitude": latitude,
                "longitude": longitude,
            },
            "model_coordinates": {
                "latitude": payload.get("latitude"),
                "longitude": payload.get("longitude"),
            },
            "observations": observations,
            "missing_fields": missing_fields,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "limitations": [
                "These are model forecasts, not direct measurements.",
                "Forecasts may not represent exact local coastal conditions.",
                "Do not use this output as navigation clearance or as the sole "
                "basis for a marine safety decision.",
            ],
        }

    async def async_invoke(
        self, args: dict[str, Any], sly_data: dict[str, Any]
    ) -> dict[str, Any]:
        return await asyncio.to_thread(self.invoke, args, sly_data)

    @staticmethod
    def _coordinate(value: Any, minimum: float, maximum: float):
        if isinstance(value, bool) or value is None:
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        if not math.isfinite(number) or not minimum <= number <= maximum:
            return None
        return number

    @staticmethod
    def _unavailable(
        location: str,
        latitude: float,
        longitude: float,
        message: str,
    ) -> dict[str, Any]:
        return {
            "status": "unavailable",
            "location": location,
            "source": "Open-Meteo Marine API",
            "simulated": False,
            "requested_coordinates": {
                "latitude": latitude,
                "longitude": longitude,
            },
            "observations": None,
            "message": message,
            "limitations": [
                "Marine conditions could not be assessed from this request.",
                "Do not interpret unavailable data as safe conditions.",
            ],
        }
