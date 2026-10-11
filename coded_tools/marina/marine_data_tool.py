
"""Marine observation tool for MARINA.

This first version uses explicitly simulated data for development.
It does not retrieve live weather or marine observations.
"""

import asyncio
from datetime import datetime, timezone
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool


class MarineDataTool(CodedTool):
    """Return clearly labelled simulated marine observations."""

    def invoke(
        self, args: dict[str, Any], sly_data: dict[str, Any]
    ) -> dict[str, Any]:
        location = str(args.get("location", "")).strip()

        if not location:
            return {
                "status": "error",
                "error": "A location is required.",
                "simulated": True,
            }

        # This sample is deliberately synthetic. It is not a live forecast.
        use_sample_data = args.get("use_sample_data", False)

        if use_sample_data is not True:
            return {
                "status": "unavailable",
                "location": location,
                "source": None,
                "observed_at": None,
                "simulated": False,
                "observations": None,
                "message": (
                    "Live marine data retrieval is not implemented. "
                    "No real-world conditions can be inferred."
                ),
            }

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
                "Synthetic test values only. These values do not describe "
                "actual conditions and must not be used to make real "
                "navigation or safety decisions."
            ),
        }

    async def async_invoke(
        self, args: dict[str, Any], sly_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Run the tool without blocking the async event loop."""
        return await asyncio.to_thread(self.invoke, args, sly_data)
