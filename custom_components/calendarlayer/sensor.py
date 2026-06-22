from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.util import slugify

from .const import DOMAIN
from .coordinator import CalendarLayerCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    known_entities: set[str] = set()

    @callback
    def build_entities():
        new_entities = []

        for item in coordinator.data or []:
            entity_key = _entity_key(item)

            if entity_key is None or entity_key in known_entities:
                continue

            entity = CalendarLayerSensor(
                coordinator,
                entity_key,
            )

            known_entities.add(entity_key)

            new_entities.append(entity)

        if new_entities:
            async_add_entities(new_entities)

    build_entities()

    entry.async_on_unload(coordinator.async_add_listener(build_entities))


def _entity_key(item: dict[str, Any]) -> str | None:
    entity_key = item.get("id") or item.get("name")

    if entity_key is None:
        return None

    return str(entity_key)


class CalendarLayerSensor(
    CoordinatorEntity,
    SensorEntity,
):
    _attr_has_entity_name = False

    def __init__(
        self,
        coordinator: CalendarLayerCoordinator,
        entity_key: str,
    ) -> None:
        super().__init__(coordinator)

        self.entity_key = entity_key

        self._attr_unique_id = (
            f"calendarlayer_{slugify(entity_key)}"
        )

    def _get_entity_data(self) -> dict[str, Any] | None:
        return next(
            (
                item
                for item in self.coordinator.data or []
                if _entity_key(item) == self.entity_key
            ),
            None,
        )

    @property
    def native_value(self):
        entity = self._get_entity_data()

        if entity is None:
            return None

        return entity.get("state")

    @property
    def name(self):
        entity = self._get_entity_data()

        if entity is None:
            return self.entity_key

        return entity.get(
            "friendlyName",
            entity.get("name", self.entity_key),
        )

    @property
    def icon(self):
        entity = self._get_entity_data()

        if entity is None:
            return "mdi:help"

        return entity.get(
            "icon",
            "mdi:circle",
        )

    @property
    def available(self) -> bool:
        return super().available and self._get_entity_data() is not None

    @property
    def native_unit_of_measurement(self):
        entity = self._get_entity_data()

        if entity is None:
            return None

        return entity.get("unitOfMeasurement") or entity.get("unit")

    @property
    def device_class(self):
        entity = self._get_entity_data()

        if entity is None:
            return None

        return entity.get("deviceClass")

    @property
    def extra_state_attributes(self):
        entity = self._get_entity_data()

        if entity is None:
            return None

        return {
            key: value
            for key, value in entity.items()
            if key
            not in {
                "deviceClass",
                "friendlyName",
                "icon",
                "id",
                "name",
                "state",
                "unit",
                "unitOfMeasurement",
            }
        }
