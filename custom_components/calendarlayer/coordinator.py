from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import API_URL, INTEGRATION_VERSION

_LOGGER = logging.getLogger(__name__)


class CannotConnect(Exception):
    """Raised when CalendarLayer cannot be reached."""


class InvalidAuth(Exception):
    """Raised when the CalendarLayer API token is invalid."""


async def async_fetch_entities(
    hass: HomeAssistant,
    api_key: str,
) -> list[dict]:
    session = async_get_clientsession(hass)
    params = {
        "token": api_key,
    }
    headers = {
        "X-Platform": "homeassistant",
        "X-Integration-Version": INTEGRATION_VERSION,
    }

    try:
        async with asyncio.timeout(10):
            async with session.get(
                API_URL,
                params=params,
                headers=headers,
            ) as response:
                if response.status in (401, 403):
                    raise InvalidAuth

                if response.status != 200:
                    raise CannotConnect(f"API returned HTTP {response.status}")

                data = await response.json()
    except InvalidAuth:
        raise
    except (
        aiohttp.ClientError,
        asyncio.TimeoutError,
        ValueError,
    ) as err:
        raise CannotConnect from err

    if not isinstance(data, list) or not all(
        isinstance(item, dict)
        for item in data
    ):
        raise CannotConnect("API returned an unexpected response")

    return data


class CalendarLayerCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="CalendarLayer",
            update_interval=timedelta(seconds=30),
        )

        self.api_key = api_key

    async def _async_update_data(self):
        try:
            return await async_fetch_entities(
                self.hass,
                self.api_key,
            )
        except InvalidAuth as err:
            raise UpdateFailed("Invalid CalendarLayer API token") from err
        except CannotConnect as err:
            raise UpdateFailed(f"CalendarLayer API error: {err}") from err
