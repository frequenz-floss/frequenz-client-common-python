# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Location type."""

import dataclasses
import math

import pytest
from frequenz.core.typing import FloatInt

from frequenz.client.common._exception import MissingFieldError
from frequenz.client.common.types import (
    InvalidCountryCode,
    InvalidCountryCodeError,
    InvalidLatitude,
    InvalidLatitudeError,
    InvalidLongitude,
    InvalidLongitudeError,
    Location,
)

# ============================================================
# Construction
# ============================================================


def test_construction_valid() -> None:
    """`Location(...)` with well-formed values stores each field verbatim."""
    location = Location(latitude=52.52, longitude=13.405, country_code="DE")
    assert location.latitude == pytest.approx(52.52)
    assert location.longitude == pytest.approx(13.405)
    assert location.country_code == "DE"


def test_construction_none_country_code() -> None:
    """`Location(country_code=None)` succeeds."""
    location = Location(latitude=52.52, longitude=13.405, country_code=None)
    assert location.country_code is None


def test_construction_wrapped_invalid_latitude() -> None:
    """`Location(latitude=InvalidLatitude(...))` stores the wrapper."""
    invalid = InvalidLatitude(value=91.0)
    location = Location(latitude=invalid, longitude=13.405, country_code="DE")
    assert location.latitude == invalid


def test_construction_wrapped_invalid_longitude() -> None:
    """`Location(longitude=InvalidLongitude(...))` stores the wrapper."""
    invalid = InvalidLongitude(value=181.0)
    location = Location(latitude=52.52, longitude=invalid, country_code="DE")
    assert location.longitude == invalid


def test_construction_wrapped_invalid_country_code() -> None:
    """`Location(country_code=InvalidCountryCode(...))` stores the wrapper."""
    invalid = InvalidCountryCode(value="DEU")
    location = Location(latitude=52.52, longitude=13.405, country_code=invalid)
    assert location.country_code == invalid


@pytest.mark.parametrize(
    "latitude",
    [-90.001, 90.001, math.nan, float("inf"), float("-inf"), -91, 91],
    ids=["below_min", "above_max", "nan", "inf", "neg_inf", "int_below", "int_above"],
)
def test_construction_rejects_plain_invalid_latitude(latitude: FloatInt) -> None:
    """A plain latitude number outside `[-90, 90]` is rejected at construction."""
    with pytest.raises(ValueError, match=r"latitude .* is outside \[-90, 90\]"):
        Location(latitude=latitude, longitude=13.405, country_code="DE")


@pytest.mark.parametrize(
    "longitude",
    [-180.001, 180.001, math.nan, float("inf"), float("-inf"), -181, 181],
    ids=["below_min", "above_max", "nan", "inf", "neg_inf", "int_below", "int_above"],
)
def test_construction_rejects_plain_invalid_longitude(longitude: FloatInt) -> None:
    """A plain longitude number outside `[-180, 180]` is rejected at construction."""
    with pytest.raises(ValueError, match=r"longitude .* is outside \[-180, 180\]"):
        Location(latitude=52.52, longitude=longitude, country_code="DE")


@pytest.mark.parametrize(
    "country_code",
    ["", "D", "DEU", "DEUT"],
    ids=["empty", "1_char", "3_chars", "4_chars"],
)
def test_construction_rejects_plain_invalid_country_code(country_code: str) -> None:
    """A plain `str` country code not exactly 2 characters is rejected at construction."""
    with pytest.raises(
        ValueError, match=r"country_code .* is not exactly 2 characters"
    ):
        Location(latitude=52.52, longitude=13.405, country_code=country_code)


def test_dataclasses_replace_valid() -> None:
    """`dataclasses.replace` with a valid value returns an updated instance."""
    original = Location(latitude=52.52, longitude=13.405, country_code="DE")
    replaced = dataclasses.replace(original, country_code="FR")
    assert replaced.country_code == "FR"
    assert replaced.latitude == pytest.approx(52.52)
    assert replaced.longitude == pytest.approx(13.405)


def test_dataclasses_replace_enforces_invariant() -> None:
    """`dataclasses.replace` with an out-of-invariant plain value is rejected."""
    original = Location(latitude=52.52, longitude=13.405, country_code="DE")
    with pytest.raises(ValueError):
        dataclasses.replace(original, country_code="DEU")


# ============================================================
# Accessors: get_latitude
# ============================================================


@pytest.mark.parametrize(
    "latitude",
    [-90.0, 0.0, 90.0, -90, 45, 90],
    ids=["min_boundary", "middle", "max_boundary", "int_min", "int_middle", "int_max"],
)
def test_get_latitude_returns_valid(latitude: FloatInt) -> None:
    """`get_latitude()` returns the stored number when well-formed."""
    location = Location(latitude=latitude, longitude=13.405, country_code="DE")
    assert location.get_latitude() == pytest.approx(latitude)


def test_get_latitude_returns_int_untouched() -> None:
    """An `int` latitude is returned as is, without coercion to `float`."""
    location = Location(latitude=45, longitude=13.405, country_code="DE")
    result = location.get_latitude()
    assert result == 45
    assert type(result) is int  # pylint: disable=unidiomatic-typecheck


def test_get_latitude_raises_for_wrapper() -> None:
    """`get_latitude()` raises `InvalidLatitudeError` when latitude is wrapped."""
    location = Location(
        latitude=InvalidLatitude(value=91.0),
        longitude=13.405,
        country_code="DE",
    )
    with pytest.raises(InvalidLatitudeError) as exc_info:
        location.get_latitude()
    assert exc_info.value.attr_name == "latitude"
    assert exc_info.value.value == pytest.approx(91.0)


# ============================================================
# Accessors: get_longitude
# ============================================================


@pytest.mark.parametrize(
    "longitude",
    [-180.0, 0.0, 180.0, -180, 90, 180],
    ids=["min_boundary", "middle", "max_boundary", "int_min", "int_middle", "int_max"],
)
def test_get_longitude_returns_valid(longitude: FloatInt) -> None:
    """`get_longitude()` returns the stored number when well-formed."""
    location = Location(latitude=52.52, longitude=longitude, country_code="DE")
    assert location.get_longitude() == pytest.approx(longitude)


def test_get_longitude_returns_int_untouched() -> None:
    """An `int` longitude is returned as is, without coercion to `float`."""
    location = Location(latitude=52.52, longitude=90, country_code="DE")
    result = location.get_longitude()
    assert result == 90
    assert type(result) is int  # pylint: disable=unidiomatic-typecheck


def test_get_longitude_raises_for_wrapper() -> None:
    """`get_longitude()` raises `InvalidLongitudeError` when longitude is wrapped."""
    location = Location(
        latitude=52.52,
        longitude=InvalidLongitude(value=181.0),
        country_code="DE",
    )
    with pytest.raises(InvalidLongitudeError) as exc_info:
        location.get_longitude()
    assert exc_info.value.attr_name == "longitude"
    assert exc_info.value.value == pytest.approx(181.0)


# ============================================================
# Accessors: get_country_code / get_country_code_or_none
# ============================================================


def test_get_country_code_returns_valid() -> None:
    """`get_country_code()` returns the stored `str` when well-formed."""
    location = Location(latitude=52.52, longitude=13.405, country_code="DE")
    assert location.get_country_code() == "DE"


def test_get_country_code_raises_missing_for_none() -> None:
    """`get_country_code()` raises `MissingFieldError` when country_code is `None`."""
    location = Location(latitude=52.52, longitude=13.405, country_code=None)
    with pytest.raises(MissingFieldError) as exc_info:
        location.get_country_code()
    assert exc_info.value.attr_name == "country_code"


def test_get_country_code_raises_invalid_for_wrapper() -> None:
    """`get_country_code()` raises `InvalidCountryCodeError` when wrapped."""
    location = Location(
        latitude=52.52,
        longitude=13.405,
        country_code=InvalidCountryCode(value="DEU"),
    )
    with pytest.raises(InvalidCountryCodeError) as exc_info:
        location.get_country_code()
    assert exc_info.value.attr_name == "country_code"
    assert exc_info.value.value == "DEU"


def test_get_country_code_or_none_returns_valid() -> None:
    """`get_country_code_or_none()` returns the stored `str` when well-formed."""
    location = Location(latitude=52.52, longitude=13.405, country_code="DE")
    assert location.get_country_code_or_none() == "DE"


def test_get_country_code_or_none_returns_none_for_missing() -> None:
    """`get_country_code_or_none()` returns `None` when country_code is `None`."""
    location = Location(latitude=52.52, longitude=13.405, country_code=None)
    assert location.get_country_code_or_none() is None


def test_get_country_code_or_none_raises_for_wrapper() -> None:
    """`get_country_code_or_none()` still raises `InvalidCountryCodeError` when wrapped."""
    location = Location(
        latitude=52.52,
        longitude=13.405,
        country_code=InvalidCountryCode(value="DEU"),
    )
    with pytest.raises(InvalidCountryCodeError) as exc_info:
        location.get_country_code_or_none()
    assert exc_info.value.attr_name == "country_code"
    assert exc_info.value.value == "DEU"


# ============================================================
# __str__
# ============================================================


@pytest.mark.parametrize(
    "latitude, longitude, country_code, expected",
    [
        (52.52, 13.405, "DE", "DE(52.52,13.40)"),
        (52.52, 13.405, None, "(52.52,13.40)"),
        (
            52.52,
            13.405,
            InvalidCountryCode(value="DEU"),
            "<invalid:'DEU'>(52.52,13.40)",
        ),
        (
            InvalidLatitude(value=91.0),
            13.405,
            "DE",
            "DE(<invalid:91.00>,13.40)",
        ),
        (
            52.52,
            InvalidLongitude(value=181.0),
            "DE",
            "DE(52.52,<invalid:181.00>)",
        ),
        (
            InvalidLatitude(value=91.0),
            InvalidLongitude(value=181.0),
            InvalidCountryCode(value="DEU"),
            "<invalid:'DEU'>(<invalid:91.00>,<invalid:181.00>)",
        ),
        (45, 90, "DE", "DE(45.00,90.00)"),
    ],
    ids=[
        "valid",
        "none_country",
        "invalid_country",
        "invalid_lat",
        "invalid_lon",
        "all_invalid",
        "int_lat_lon",
    ],
)
def test_str(
    latitude: FloatInt | InvalidLatitude,
    longitude: FloatInt | InvalidLongitude,
    country_code: str | InvalidCountryCode | None,
    expected: str,
) -> None:
    """The string representation of a Location renders each field distinctly."""
    location = Location(
        latitude=latitude, longitude=longitude, country_code=country_code
    )
    assert str(location) == expected
