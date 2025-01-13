"""Data update coordinator for the Wavespa API."""

import asyncio
from datetime import timedelta
from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .wavespa.api import WavespaApi, WavespaApiResults

_LOGGER = getLogger(__name__)


class WavespaUpdateCoordinator(DataUpdateCoordinator[WavespaApiResults]):
    """Update coordinator that polls the device status for all devices in an account."""

    def __init__(self, hass: HomeAssistant, api: WavespaApi) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Wavespa API",
            update_interval=timedelta(seconds=30),
        )
        self.api = api

    ## fix from https://github.com/cdpuk/ha-bestway/issues/86
    async def _async_update_data(self) -> WavespaApiResults:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        async with asyncio.timeout(10):
            try:
                await self.api.refresh_bindings()
            except Exception as e:
                # Log the error if necessary or just pass to silently ignore
                # You can log it with your logging system like:
                # _LOGGER.error(f"Failed to refresh bindings: {e}")
                pass  # Ignore failures on refresh_bindings

            return await self.api.fetch_data()
