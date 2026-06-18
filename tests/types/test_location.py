# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the microgrid metadata types."""

import math

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


@pytest.mark.parametrize(
    "latitude, longitude",
    [
        (-90.0, 0.0),
        (90.0, 0.0),
        (0.0, -180.0),
        (0.0, 180.0),
        (-90.0, -180.0),
        (90.0, 180.0),
    ],
    ids=[
        "lat_min_boundary",
        "lat_max_boundary",
        "lon_min_boundary",
        "lon_max_boundary",
        "both_min_boundary",
        "both_max_boundary",
    ],
)
def test_location_boundary_values_accepted(latitude: float, longitude: float) -> None:
    """Test that boundary latitude/longitude values are accepted."""
    location = Location(latitude=latitude, longitude=longitude, country_code=None)
    assert location.latitude == latitude
    assert location.longitude == longitude


@pytest.mark.parametrize(
    "latitude, longitude, match",
    [
        (-90.001, 0.0, "latitude"),
        (90.001, 0.0, "latitude"),
        (0.0, -180.001, "longitude"),
        (0.0, 180.001, "longitude"),
    ],
    ids=[
        "lat_below_min",
        "lat_above_max",
        "lon_below_min",
        "lon_above_max",
    ],
)
def test_location_out_of_range_raises(
    latitude: float, longitude: float, match: str
) -> None:
    """Test that out-of-range latitude/longitude raises ValueError."""
    with pytest.raises(ValueError, match=match):
        Location(latitude=latitude, longitude=longitude, country_code=None)


@pytest.mark.parametrize(
    "latitude, longitude",
    [
        (None, 13.405),
        (52.52, None),
        (None, None),
    ],
    ids=["lat_none", "lon_none", "both_none"],
)
def test_location_partial_none_accepted(
    latitude: float | None, longitude: float | None
) -> None:
    """Test that partial None coordinates are valid."""
    location = Location(latitude=latitude, longitude=longitude, country_code=None)
    assert location.latitude == latitude
    assert location.longitude == longitude


@pytest.mark.parametrize(
    "latitude, longitude, match",
    [
        (math.nan, 0.0, "latitude"),
        (0.0, math.nan, "longitude"),
    ],
    ids=["nan_lat", "nan_lon"],
)
def test_location_nan_raises(latitude: float, longitude: float, match: str) -> None:
    """Test that NaN latitude/longitude raises ValueError."""
    with pytest.raises(ValueError, match=match):
        Location(latitude=latitude, longitude=longitude, country_code=None)
