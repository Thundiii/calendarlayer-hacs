from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    known_entities = {}

    def build_entities():
        new_entities = []

        for item in coordinator.data:
            entity_name = item["name"]

            if entity_name in known_entities:
                continue

            entity = CalendarLayerSensor(
                coordinator,
                entity_name,
            )

            known_entities[entity_name] = entity

            new_entities.append(entity)

        if new_entities:
            async_add_entities(new_entities)

    build_entities()

    coordinator.async_add_listener(
        build_entities,
    )


class CalendarLayerSensor(
    CoordinatorEntity,
    SensorEntity,
):
    def __init__(
        self,
        coordinator,
        entity_name,
    ):
        super().__init__(coordinator)

        self.entity_name = entity_name

        self._attr_unique_id = (
            f"calendarlayer_{entity_name}"
        )

    def _get_entity_data(self):
        return next(
            (
                item
                for item in self.coordinator.data
                if item["name"] == self.entity_name
            ),
            None,
        )

    @property
    def native_value(self):
        entity = self._get_entity_data()

        if entity is None:
            return None

        return entity["state"]

    @property
    def name(self):
        entity = self._get_entity_data()

        if entity is None:
            return self.entity_name

        return entity.get(
            "friendlyName",
            self.entity_name,
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
    def has_entity_name(self):
        return True    