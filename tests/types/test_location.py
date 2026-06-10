# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the microgrid metadata types."""

import pytest

from frequenz.client.common.types import Location


@pytest.mark.parametrize("latitude", [None, 52.52], ids=str)
@pytest.mark.parametrize("longitude", [None, 13.405], ids=str)
@pytest.mark.parametrize("country_code", [None, "DE"], ids=str)
def test_location_initialization(
    latitude: float | None,
    longitude: float | None,
    country_code: str | None,
) -> None:
    """Test location initialization with different combinations of parameters."""
    location = Location(
        latitude=latitude, longitude=longitude, country_code=country_code
    )

    assert location.latitude == latitude
    assert location.longitude == longitude
    assert location.country_code == country_code
