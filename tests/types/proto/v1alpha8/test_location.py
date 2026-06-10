# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Location protobuf conversion."""

from dataclasses import dataclass

import pytest
from frequenz.api.common.v1alpha8.types import location_pb2

from frequenz.client.common.types.proto.v1alpha8 import location_from_proto


@dataclass(frozen=True, kw_only=True)
class _ProtoConversionTestCase:  # pylint: disable=too-many-instance-attributes
    """Test case for protobuf conversion."""

    name: str
    """The description of the test case."""

    latitude: float
    """The latitude to set in the protobuf message."""

    longitude: float
    """The longitude to set in the protobuf message."""

    country_code: str
    """The country code to set in the protobuf message."""

    expected_none_latitude: bool = False
    """The latitude is expected to be None."""

    expected_none_longitude: bool = False
    """The longitude is expected to be None."""

    expected_none_country_code: bool = False
    """The country code is expected to be None."""

    expect_warning: bool = False
    """Whether to expect a warning during conversion."""


@pytest.mark.parametrize(
    "case",
    [
        _ProtoConversionTestCase(
            name="valid",
            latitude=52.52,
            longitude=13.405,
            country_code="DE",
        ),
        _ProtoConversionTestCase(
            name="boundary_latitude",
            latitude=90.0,
            longitude=13.405,
            country_code="DE",
        ),
        _ProtoConversionTestCase(
            name="boundary_longitude",
            latitude=52.52,
            longitude=180.0,
            country_code="DE",
        ),
        _ProtoConversionTestCase(
            name="invalid_latitude",
            latitude=91.0,
            longitude=13.405,
            country_code="DE",
            expected_none_latitude=True,
            expect_warning=True,
        ),
        _ProtoConversionTestCase(
            name="invalid_longitude",
            latitude=52.52,
            longitude=181.0,
            country_code="DE",
            expected_none_longitude=True,
            expect_warning=True,
        ),
        _ProtoConversionTestCase(
            name="empty_country_code",
            latitude=52.52,
            longitude=13.405,
            country_code="",
            expected_none_country_code=True,
            expect_warning=True,
        ),
        _ProtoConversionTestCase(
            name="all_invalid",
            latitude=-91.0,
            longitude=181.0,
            country_code="",
            expected_none_latitude=True,
            expected_none_longitude=True,
            expected_none_country_code=True,
            expect_warning=True,
        ),
    ],
    ids=lambda case: case.name,
)
def test_from_proto(
    caplog: pytest.LogCaptureFixture, case: _ProtoConversionTestCase
) -> None:
    """Test conversion from protobuf message to Location."""
    proto = location_pb2.Location(
        latitude=case.latitude,
        longitude=case.longitude,
        country_code=case.country_code,
    )
    with caplog.at_level("WARNING"):
        location = location_from_proto(proto)

    if case.expected_none_latitude:
        assert location.latitude is None
    else:
        assert location.latitude == pytest.approx(case.latitude)

    if case.expected_none_longitude:
        assert location.longitude is None
    else:
        assert location.longitude == pytest.approx(case.longitude)

    if case.expected_none_country_code:
        assert location.country_code is None
    else:
        assert location.country_code == case.country_code

    if case.expect_warning:
        assert len(caplog.records) > 0
        assert "Found issues in location:" in caplog.records[0].message
    else:
        assert len(caplog.records) == 0
