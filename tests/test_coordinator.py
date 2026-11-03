"""Test WaveSpa update coordination."""

from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
import pytest

from custom_components.wavespa.coordinator import WavespaUpdateCoordinator
from custom_components.wavespa.const import DOMAIN
from custom_components.wavespa.wavespa.api import (
    WavespaTokenInvalidException,
    WavespaApiResults,
)


async def test_invalid_token_refreshes_and_retries(hass: HomeAssistant) -> None:
    """Test that an invalid token is refreshed and the update is retried."""
    old_api = AsyncMock()
    old_api.refresh_bindings.side_effect = WavespaTokenInvalidException()

    expected = WavespaApiResults(devices={})
    new_api = AsyncMock()
    new_api.fetch_data.return_value = expected
    token_refresher = AsyncMock(return_value=new_api)

    coordinator = WavespaUpdateCoordinator(
        hass, MockConfigEntry(domain=DOMAIN), old_api, token_refresher
    )

    assert await coordinator._async_update_data() is expected
    token_refresher.assert_awaited_once()
    new_api.refresh_bindings.assert_awaited_once()
    new_api.fetch_data.assert_awaited_once()


async def test_update_failure_is_visible(hass: HomeAssistant) -> None:
    """Test that a polling failure is reported to Home Assistant."""
    api = AsyncMock()
    api.refresh_bindings.side_effect = RuntimeError("API unavailable")
    token_refresher = AsyncMock()
    coordinator = WavespaUpdateCoordinator(
        hass, MockConfigEntry(domain=DOMAIN), api, token_refresher
    )

    with pytest.raises(UpdateFailed, match="Error communicating with WaveSpa"):
        await coordinator._async_update_data()

    token_refresher.assert_not_awaited()
