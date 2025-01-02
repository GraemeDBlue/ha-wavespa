"""Select platform."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.wavespa.wavespa.api import WavespaApi

from .wavespa.model import (
    BubblesLevel,
)
from .entity import WavespaEntity

_BUBBLES_OPTIONS = {
    BubblesLevel.OFF: "OFF",
    BubblesLevel.MEDIUM: "MEDIUM",
    BubblesLevel.MAX: "MAX",
}


@dataclass(frozen=True)
class BubblesRequiredKeys:
    """Mixin for required keys."""

    set_fn: Callable[[WavespaApi, str, BubblesLevel], Awaitable[None]]
    get_fn: Callable[[int], BubblesLevel]


@dataclass(frozen=True)
class BubblesSelectEntityDescription(SelectEntityDescription, BubblesRequiredKeys):
    """Describes bubbles selection."""


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select entities."""

    entities: list[WavespaEntity] = []

    async_add_entities(entities)
