# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Location type."""

import dataclasses
import math

import pytest

from frequenz.client.common.types import (
    InvalidCountryCode,
    InvalidLatitude,
    InvalidLongitude,
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
    [-90.001, 90.001, math.nan, float("inf"), float("-inf")],
    ids=["below_min", "above_max", "nan", "inf", "neg_inf"],
)
def test_construction_rejects_plain_invalid_latitude(latitude: float) -> None:
    """A plain `float` latitude outside `[-90, 90]` is rejected at construction."""
    with pytest.raises(ValueError, match=r"latitude .* is outside \[-90, 90\]"):
        Location(latitude=latitude, longitude=13.405, country_code="DE")


@pytest.mark.parametrize(
    "longitude",
    [-180.001, 180.001, math.nan, float("inf"), float("-inf")],
    ids=["below_min", "above_max", "nan", "inf", "neg_inf"],
)
def test_construction_rejects_plain_invalid_longitude(longitude: float) -> None:
    """A plain `float` longitude outside `[-180, 180]` is rejected at construction."""
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
