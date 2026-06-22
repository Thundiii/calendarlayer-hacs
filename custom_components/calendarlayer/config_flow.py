from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .coordinator import CannotConnect, InvalidAuth, async_fetch_entities

_LOGGER = logging.getLogger(__name__)


class CalendarLayerConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ) -> FlowResult:
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()

            try:
                await async_fetch_entities(
                    self.hass,
                    user_input[CONF_API_KEY],
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected error during CalendarLayer setup")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="CalendarLayer",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
            }),
            errors=errors,
        )

    async def async_step_reconfigure(
        self,
        user_input=None,
    ) -> FlowResult:
        entry = self._get_reconfigure_entry()
        errors = {}

        if user_input is not None:
            try:
                await async_fetch_entities(
                    self.hass,
                    user_input[CONF_API_KEY],
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception(
                    "Unexpected error during CalendarLayer reconfiguration"
                )
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    entry,
                    data_updates=user_input,
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_API_KEY,
                    default=entry.data.get(CONF_API_KEY, ""),
                ): str,
            }),
            errors=errors,
        )

    async def async_step_reauth(
        self,
        user_input=None,
    ) -> FlowResult:
        return await self.async_step_reauth_confirm(user_input)

    async def async_step_reauth_confirm(
        self,
        user_input=None,
    ) -> FlowResult:
        errors = {}

        if user_input is not None:
            existing_entry = self._get_reauth_entry()

            try:
                await async_fetch_entities(
                    self.hass,
                    user_input[CONF_API_KEY],
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception(
                    "Unexpected error during CalendarLayer reauthentication"
                )
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    existing_entry,
                    data_updates=user_input,
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
            }),
            errors=errors,
        )
