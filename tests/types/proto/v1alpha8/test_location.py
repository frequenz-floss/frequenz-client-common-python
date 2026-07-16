# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Location protobuf conversion."""

from dataclasses import dataclass

import pytest
from frequenz.api.common.v1alpha8.types import location_pb2

from frequenz.client.common.types import (
    InvalidCountryCode,
    InvalidLatitude,
    InvalidLongitude,
)
from frequenz.client.common.types.proto.v1alpha8 import location_from_proto


@dataclass(frozen=True, kw_only=True)
class _ProtoConversionTestCase:
    """Test case for protobuf conversion."""

    name: str
    """The description of the test case."""

    latitude: float
    """The latitude to set in the protobuf message."""

    longitude: float
    """The longitude to set in the protobuf message."""

    country_code: str
    """The country code to set in the protobuf message."""

    expected_latitude: float | InvalidLatitude
    """The expected `latitude` on the resulting `Location`."""

    expected_longitude: float | InvalidLongitude
    """The expected `longitude` on the resulting `Location`."""

    expected_country_code: str | InvalidCountryCode | None
    """The expected `country_code` on the resulting `Location`.

    An empty `country_code` on the wire is normalized to `None`; a
    non-empty `country_code` that is not exactly 2 characters is wrapped
    in `InvalidCountryCode`.
    """


@pytest.mark.parametrize(
    "case",
    [
        _ProtoConversionTestCase(
            name="valid",
            latitude=52.52,
            longitude=13.405,
            country_code="DE",
            expected_latitude=52.52,
            expected_longitude=13.405,
            expected_country_code="DE",
        ),
        _ProtoConversionTestCase(
            name="boundary_latitude",
            latitude=90.0,
            longitude=13.405,
            country_code="DE",
            expected_latitude=90.0,
            expected_longitude=13.405,
            expected_country_code="DE",
        ),
        _ProtoConversionTestCase(
            name="boundary_longitude",
            latitude=52.52,
            longitude=180.0,
            country_code="DE",
            expected_latitude=52.52,
            expected_longitude=180.0,
            expected_country_code="DE",
        ),
        _ProtoConversionTestCase(
            name="invalid_latitude",
            latitude=91.0,
            longitude=13.405,
            country_code="DE",
            expected_latitude=InvalidLatitude(value=91.0),
            expected_longitude=13.405,
            expected_country_code="DE",
        ),
        _ProtoConversionTestCase(
            name="invalid_longitude",
            latitude=52.52,
            longitude=181.0,
            country_code="DE",
            expected_latitude=52.52,
            expected_longitude=InvalidLongitude(value=181.0),
            expected_country_code="DE",
        ),
        _ProtoConversionTestCase(
            name="empty_country_code",
            latitude=52.52,
            longitude=13.405,
            country_code="",
            expected_latitude=52.52,
            expected_longitude=13.405,
            expected_country_code=None,
        ),
        _ProtoConversionTestCase(
            name="long_country_code",
            latitude=52.52,
            longitude=13.405,
            country_code="DEU",
            expected_latitude=52.52,
            expected_longitude=13.405,
            expected_country_code=InvalidCountryCode(value="DEU"),
        ),
        _ProtoConversionTestCase(
            name="all_invalid",
            latitude=-91.0,
            longitude=181.0,
            country_code="",
            expected_latitude=InvalidLatitude(value=-91.0),
            expected_longitude=InvalidLongitude(value=181.0),
            expected_country_code=None,
        ),
    ],
    ids=lambda case: case.name,
)
def test_from_proto(case: _ProtoConversionTestCase) -> None:
    """Wire values become plain values or Invalid* wrappers per invariant."""
    proto = location_pb2.Location(
        latitude=case.latitude,
        longitude=case.longitude,
        country_code=case.country_code,
    )
    location = location_from_proto(proto)

    if isinstance(case.expected_latitude, float):
        assert isinstance(location.latitude, float)
        assert location.latitude == pytest.approx(case.expected_latitude)
    else:
        assert location.latitude == case.expected_latitude
    if isinstance(case.expected_longitude, float):
        assert isinstance(location.longitude, float)
        assert location.longitude == pytest.approx(case.expected_longitude)
    else:
        assert location.longitude == case.expected_longitude
    assert location.country_code == case.expected_country_code
