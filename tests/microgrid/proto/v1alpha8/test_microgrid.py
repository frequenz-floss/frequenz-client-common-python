# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Microgrid protobuf conversion."""

from dataclasses import dataclass
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from frequenz.api.common.v1alpha8.grid import delivery_area_pb2
from frequenz.api.common.v1alpha8.microgrid import microgrid_pb2

# pylint: disable-next=no-name-in-module
from google.protobuf.timestamp_pb2 import Timestamp

from frequenz.client.common import (
    InvalidDatetime,
    InvalidDatetimeError,
    UnrecognizedEnumValueError,
    UnspecifiedEnumValueError,
)
from frequenz.client.common.grid import DeliveryArea, EnergyMarketCodeType
from frequenz.client.common.microgrid import EnterpriseId, Microgrid, MicrogridId
from frequenz.client.common.microgrid.proto.v1alpha8 import microgrid_from_proto
from frequenz.client.common.types import Location


@dataclass(frozen=True, kw_only=True)
class _ProtoConversionTestCase:
    """Test case for protobuf conversion."""

    name: str
    """Description of the test case."""

    has_delivery_area: bool
    """Whether to include delivery area in the protobuf message."""

    has_location: bool
    """Whether to include location in the protobuf message."""

    has_name: bool
    """Whether to include name in the protobuf message."""

    status: int
    """The raw protobuf `MICROGRID_STATUS_*` value to set in the message."""

    expected_active: bool | int
    """The expected `_active` value after conversion.

    `True`/`False` for recognized statuses, the raw `int` `0` when the status
    is unspecified, or any other raw `int` when the status is unrecognized.
    """


def _assert_active(info: Microgrid, expected_active: bool | int) -> None:
    """Assert that ``info._active`` matches ``expected_active`` and the accessor agrees."""
    active = info._active  # pylint: disable=protected-access
    assert active == expected_active
    assert type(active) is type(expected_active)
    match expected_active:
        case bool() as expected_bool:
            assert info.is_active() is expected_bool
        case 0:
            with pytest.raises(UnspecifiedEnumValueError):
                info.is_active()
        case int() as expected_int:
            with pytest.raises(UnrecognizedEnumValueError) as exc_info:
                info.is_active()
            assert exc_info.value.value == expected_int


@pytest.mark.parametrize(
    "case",
    [
        _ProtoConversionTestCase(
            name="active",
            has_delivery_area=True,
            has_location=True,
            has_name=True,
            status=microgrid_pb2.MICROGRID_STATUS_ACTIVE,
            expected_active=True,
        ),
        _ProtoConversionTestCase(
            name="inactive",
            has_delivery_area=True,
            has_location=True,
            has_name=True,
            status=microgrid_pb2.MICROGRID_STATUS_INACTIVE,
            expected_active=False,
        ),
        _ProtoConversionTestCase(
            name="no_delivery_area",
            has_delivery_area=False,
            has_location=True,
            has_name=True,
            status=microgrid_pb2.MICROGRID_STATUS_ACTIVE,
            expected_active=True,
        ),
        _ProtoConversionTestCase(
            name="no_location",
            has_delivery_area=True,
            has_location=False,
            has_name=True,
            status=microgrid_pb2.MICROGRID_STATUS_ACTIVE,
            expected_active=True,
        ),
        _ProtoConversionTestCase(
            name="empty_name",
            has_delivery_area=True,
            has_location=True,
            has_name=False,
            status=microgrid_pb2.MICROGRID_STATUS_ACTIVE,
            expected_active=True,
        ),
        _ProtoConversionTestCase(
            name="unspecified_status",
            has_delivery_area=True,
            has_location=True,
            has_name=True,
            status=microgrid_pb2.MICROGRID_STATUS_UNSPECIFIED,
            expected_active=0,
        ),
        _ProtoConversionTestCase(
            name="unrecognized_status",
            has_delivery_area=True,
            has_location=True,
            has_name=True,
            status=999,  # Unknown status value
            expected_active=999,
        ),
    ],
    ids=lambda case: case.name,
)
@patch(
    "frequenz.client.common.microgrid.proto.v1alpha8._microgrid.delivery_area_from_proto2"
)
@patch("frequenz.client.common.microgrid.proto.v1alpha8._microgrid.location_from_proto")
@patch(
    "frequenz.client.common.microgrid.proto.v1alpha8._microgrid.datetime_from_proto2"
)
def test_from_proto(
    mock_datetime_from_proto2: Mock,
    mock_location_from_proto: Mock,
    mock_delivery_area_from_proto: Mock,
    case: _ProtoConversionTestCase,
) -> None:
    """Test conversion from protobuf message to Microgrid."""
    now = datetime.now(timezone.utc)
    mock_datetime_from_proto2.return_value = now

    mock_location = (
        Location(
            latitude=52.52,
            longitude=13.405,
            country_code="DE",
        )
        if case.has_location
        else None
    )
    mock_location_from_proto.return_value = mock_location

    mock_delivery_area = (
        DeliveryArea(
            code="DE123",
            code_type=EnergyMarketCodeType.EUROPE_EIC,
        )
        if case.has_delivery_area
        else None
    )
    mock_delivery_area_from_proto.return_value = mock_delivery_area

    proto = microgrid_pb2.Microgrid(
        id=1234,
        enterprise_id=5678,
        name="Test Grid" if case.has_name else "",
        status=microgrid_pb2.MicrogridStatus.ValueType(case.status),
    )

    # Add optional fields if needed
    if case.has_delivery_area:
        proto.delivery_area.code = "DE123"
        proto.delivery_area.code_type = (
            delivery_area_pb2.EnergyMarketCodeType.ENERGY_MARKET_CODE_TYPE_EUROPE_EIC
        )

    if case.has_location:
        proto.location.latitude = 52.52
        proto.location.longitude = 13.405
        proto.location.country_code = "DE"

    # Run the conversion
    info = microgrid_from_proto(proto)

    # Verify the result
    assert info.id == MicrogridId(1234)
    assert info.enterprise_id == EnterpriseId(5678)
    assert info.create_time == now

    if case.has_name:
        assert info.name == "Test Grid"
    else:
        assert info.name == ""

    _assert_active(info, case.expected_active)

    # Verify mock calls
    mock_datetime_from_proto2.assert_called_once_with(proto.create_timestamp)

    if case.has_delivery_area:
        mock_delivery_area_from_proto.assert_called_once_with(proto.delivery_area)
        assert info.delivery_area == mock_delivery_area
    else:
        mock_delivery_area_from_proto.assert_not_called()
        assert info.delivery_area is None

    if case.has_location:
        mock_location_from_proto.assert_called_once_with(proto.location)
        assert info.location == mock_location
    else:
        mock_location_from_proto.assert_not_called()
        assert info.location is None


@pytest.mark.parametrize(
    "create_timestamp",
    [
        pytest.param(Timestamp(seconds=253402300800), id="year-10000"),
        pytest.param(Timestamp(seconds=0, nanos=1000000000), id="a-whole-second"),
        pytest.param(Timestamp(seconds=0, nanos=-1), id="negative-nanos"),
    ],
)
def test_from_proto_unrepresentable_create_time(create_timestamp: Timestamp) -> None:
    """An unrepresentable creation time is preserved instead of raising."""
    proto = microgrid_pb2.Microgrid(
        id=1234,
        enterprise_id=5678,
        name="Test Grid",
        status=microgrid_pb2.MICROGRID_STATUS_ACTIVE,
        create_timestamp=create_timestamp,
    )

    info = microgrid_from_proto(proto)

    assert info.create_time == InvalidDatetime(
        seconds=create_timestamp.seconds, nanos=create_timestamp.nanos
    )
    with pytest.raises(InvalidDatetimeError):
        info.get_create_time()
