"""Number platform support."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WavespaUpdateCoordinator
from .const import DOMAIN
from .entity import WavespaEntity

_POOL_FILTER_TIME = NumberEntityDescription(
    key="pool_filter_time",
    name="Pool Filter Timer",
    icon="mdi:image-filter-tilt-shift",
    native_unit_of_measurement=UnitOfTime.HOURS,
    native_max_value=24,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities."""
    entities: list[WavespaEntity] = []

    async_add_entities(entities)


class PoolFilterTimeNumber(WavespaEntity, NumberEntity):
    """Pool filter entity representing the number of hours to stay on for."""

    def __init__(
        self,
        coordinator: WavespaUpdateCoordinator,
        config_entry: ConfigEntry,
        device_id: str,
        description: NumberEntityDescription,
    ) -> None:
        """Initialize number."""
        super().__init__(coordinator, config_entry, device_id)
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def native_value(self) -> float | None:
        """Get the number of hours to stay on for."""
        if self.status is not None:
            hours = self.status.attrs["time"]
            if isinstance(hours, int):
                return hours
        return None

    # async def async_set_native_value(self, value: float) -> None:
    #     """Update the current value."""
    #     await self.coordinator.api.pool_filter_set_time(self.device_id, int(value))
