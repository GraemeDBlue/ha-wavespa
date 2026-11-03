"""Data update coordinator for the Wavespa API."""

import asyncio
from collections.abc import Awaitable, Callable
from datetime import timedelta
from logging import getLogger

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .wavespa.api import (
    WavespaApi,
    WavespaApiResults,
    WavespaTokenInvalidException,
)

_LOGGER = getLogger(__name__)


class WavespaUpdateCoordinator(DataUpdateCoordinator[WavespaApiResults]):
    """Update coordinator that polls the device status for all devices in an account."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: WavespaApi,
        token_refresher: Callable[[], Awaitable[WavespaApi]],
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Wavespa API",
            update_interval=timedelta(seconds=30),
            config_entry=entry,
        )
        self.api = api
        self._token_refresher = token_refresher

    async def _async_update_data(self) -> WavespaApiResults:
        """Fetch data from the API endpoint."""
        try:
            return await self._async_fetch_data()
        except WavespaTokenInvalidException:
            _LOGGER.warning("WaveSpa API token is invalid; refreshing authentication")
            try:
                self.api = await self._token_refresher()
                return await self._async_fetch_data()
            except Exception as err:
                _LOGGER.error("WaveSpa update failed after token refresh: %s", err)
                raise UpdateFailed(
                    "WaveSpa authentication refresh failed; reconfigure the integration"
                ) from err
        except Exception as err:
            _LOGGER.error("WaveSpa update failed: %s", err)
            raise UpdateFailed(f"Error communicating with WaveSpa: {err}") from err

    async def _async_fetch_data(self) -> WavespaApiResults:
        """Refresh device bindings and fetch the latest device state."""
        async with asyncio.timeout(10):
            await self.api.refresh_bindings()
            return await self.api.fetch_data()
