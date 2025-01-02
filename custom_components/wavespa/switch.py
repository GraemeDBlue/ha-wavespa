"""Switch platform support."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WavespaUpdateCoordinator
from .wavespa.api import WavespaApi
from .wavespa.model import WavespaDeviceStatus, WavespaDeviceType
from .const import DOMAIN, Icon
from .entity import WavespaEntity


@dataclass(frozen=True)
class SwitchFunctionsMixin:
    """Functions for spa devices."""

    value_fn: Callable[[WavespaDeviceStatus], bool]
    turn_on_fn: Callable[[WavespaApi, str], Awaitable[None]]
    turn_off_fn: Callable[[WavespaApi, str], Awaitable[None]]


@dataclass(frozen=True)
class WavespaSwitchEntityDescription(SwitchEntityDescription, SwitchFunctionsMixin):
    """Entity description for wavespa spa switches."""


_AIRJET_SPA_POWER_SWITCH = WavespaSwitchEntityDescription(
    key="spa_heater",
    name="Spa Heater",
    icon=Icon.POWER,
    value_fn=lambda s: bool(s.attrs["Heater"]),
    turn_on_fn=lambda api, device_id: api.airjet_spa_set_power(device_id, True),
    turn_off_fn=lambda api, device_id: api.airjet_spa_set_power(device_id, False),
)

_AIRJET_SPA_FILTER_SWITCH = WavespaSwitchEntityDescription(
    key="spa_filter_power",
    name="Spa Filter",
    icon=Icon.FILTER,
    value_fn=lambda s: bool(s.attrs["Filter"]),
    turn_on_fn=lambda api, device_id: api.airjet_spa_set_filter(device_id, True),
    turn_off_fn=lambda api, device_id: api.airjet_spa_set_filter(device_id, False),
)

_AIRJET_SPA_BUBBLES_SWITCH = WavespaSwitchEntityDescription(
    key="spa_bubbles_power",
    name="Spa Bubbles",
    icon=Icon.BUBBLES,
    value_fn=lambda s: bool(s.attrs["bubble"]),
    turn_on_fn=lambda api, device_id: api.airjet_spa_set_bubbles(device_id, True),
    turn_off_fn=lambda api, device_id: api.airjet_spa_set_bubbles(device_id, False),
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch entities."""
    coordinator: WavespaUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[WavespaEntity] = []

    for device_id, device in coordinator.api.devices.items():
        if device.device_type == WavespaDeviceType.AIRJET_SPA:
            entities.extend(
                [
                    WavespaSwitch(
                        coordinator,
                        config_entry,
                        device_id,
                        _AIRJET_SPA_POWER_SWITCH
                    ),
                    WavespaSwitch(
                        coordinator,
                        config_entry,
                        device_id,
                        _AIRJET_SPA_FILTER_SWITCH,
                    ),
                    WavespaSwitch(
                        coordinator,
                        config_entry,
                        device_id,
                        _AIRJET_SPA_BUBBLES_SWITCH,
                    ),
                ]
            )

    async_add_entities(entities)


class WavespaSwitch(WavespaEntity, SwitchEntity):
    """Wavespa switch entity."""

    entity_description: WavespaSwitchEntityDescription

    def __init__(
        self,
        coordinator: WavespaUpdateCoordinator,
        config_entry: ConfigEntry,
        device_id: str,
        description: WavespaSwitchEntityDescription,
    ) -> None:
        """Initialize switch."""
        super().__init__(coordinator, config_entry, device_id)
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        if status := self.status:
            return self.entity_description.value_fn(status)

        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.entity_description.turn_on_fn(self.coordinator.api, self.device_id)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.entity_description.turn_off_fn(self.coordinator.api, self.device_id)
        await self.coordinator.async_refresh()
