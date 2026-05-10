from datetime import timedelta
import logging

import aiohttp

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

API_URL = (
    "https://calendar.thundiii.de"
    "/api/backend/external/entities"
)


class CalendarLayerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_key):
        super().__init__(
            hass,
            _LOGGER,
            name="CalendarLayer",
            update_interval=timedelta(seconds=30),
        )

        self.api_key = api_key

    async def _async_update_data(self):
        params = {
            "token": self.api_key,
        }
        headers = {
            "X-Platform": "homeassistant",
            "X-Integration-Version": "0.0.1",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_URL,
                params=params,
                headers=headers,
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(
                        f"API Error: {response.status}"
                    )

                return await response.json()