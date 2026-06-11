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


@pytest.mark.parametrize(
    "latitude, longitude, country_code, expected",
    [
        (52.52, 13.405, "DE", "DE:(52.52, 13.40)"),
        (None, None, "DE", "DE"),
        (52.52, None, "DE", "DE:(52.52, ?)"),
        (None, 13.405, "DE", "DE:(?, 13.40)"),
        (52.52, 13.405, None, "<NO COUNTRY CODE>:(52.52, 13.40)"),
        (None, None, None, "<NO COUNTRY CODE>"),
    ],
)
def test_location_str(
    latitude: float | None,
    longitude: float | None,
    country_code: str | None,
    expected: str,
) -> None:
    """Test the string representation of a Location."""
    location = Location(
        latitude=latitude, longitude=longitude, country_code=country_code
    )
    assert str(location) == expected
