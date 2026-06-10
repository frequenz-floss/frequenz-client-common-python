# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Microgrid protobuf conversion."""

from dataclasses import dataclass
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from frequenz.api.common.v1alpha8.grid import delivery_area_pb2
from frequenz.api.common.v1alpha8.microgrid import microgrid_pb2

from frequenz.client.common.grid import DeliveryArea, EnergyMarketCodeType
from frequenz.client.common.microgrid import EnterpriseId, MicrogridId, MicrogridStatus
from frequenz.client.common.microgrid.proto.v1alpha8 import (
    microgrid_from_proto,
    microgrid_status_from_proto,
    microgrid_status_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest
from frequenz.client.common.types import Location


class TestMicrogridStatusParity(EnumParityTest):
    """Parity tests for the `MicrogridStatus` enum."""

    python_enum = MicrogridStatus
    proto_enum = microgrid_pb2.MicrogridStatus
    name_prefix = "MICROGRID_STATUS_"
    from_proto = staticmethod(microgrid_status_from_proto)
    to_proto = staticmethod(microgrid_status_to_proto)


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

    status: MicrogridStatus | int
    """The status to set in the protobuf message."""

    expected_log: tuple[str, str] | None = None
    """Whether to expect a log during conversion (level, message)."""


@pytest.mark.parametrize(
    "case",
    [
        _ProtoConversionTestCase(
            name="full",
            has_delivery_area=True,
            has_location=True,
            has_name=True,
            status=MicrogridStatus.ACTIVE,
        ),
        _ProtoConversionTestCase(
            name="no_delivery_area",
            has_delivery_area=False,
            has_location=True,
            has_name=True,
            status=MicrogridStatus.ACTIVE,
            expected_log=(
                "WARNING",
                "Found issues in microgrid: delivery_area is missing",
            ),
        ),
        _ProtoConversionTestCase(
            name="no_location",
            has_delivery_area=True,
            has_location=False,
            has_name=True,
            status=MicrogridStatus.ACTIVE,
            expected_log=("WARNING", "Found issues in microgrid: location is missing"),
        ),
        _ProtoConversionTestCase(
            name="empty_name",
            has_delivery_area=True,
            has_location=True,
            has_name=False,
            status=MicrogridStatus.ACTIVE,
            expected_log=("DEBUG", "Found minor issues in microgrid: name is empty"),
        ),
        _ProtoConversionTestCase(
            name="unspecified_status",
            has_delivery_area=True,
            has_location=True,
            has_name=True,
            status=MicrogridStatus.UNSPECIFIED,
            expected_log=(
                "WARNING",
                "Found issues in microgrid: status is unspecified",
            ),
        ),
        _ProtoConversionTestCase(
            name="unrecognized_status",
            has_delivery_area=True,
            has_location=True,
            has_name=True,
            status=999,  # Unknown status value
            expected_log=(
                "WARNING",
                "Found issues in microgrid: status is unrecognized",
            ),
        ),
    ],
    ids=lambda case: case.name,
)
@patch(
    "frequenz.client.common.microgrid.proto.v1alpha8._microgrid.delivery_area_from_proto"
)
@patch("frequenz.client.common.microgrid.proto.v1alpha8._microgrid.location_from_proto")
@patch(
    "frequenz.client.common.microgrid.proto.v1alpha8._microgrid.microgrid_status_from_proto"
)
@patch("frequenz.client.common.microgrid.proto.v1alpha8._microgrid.datetime_from_proto")
# pylint: disable-next=too-many-arguments,too-many-positional-arguments,too-many-branches
def test_from_proto(
    mock_datetime_from_proto: Mock,
    mock_microgrid_status_from_proto: Mock,
    mock_location_from_proto: Mock,
    mock_delivery_area_from_proto: Mock,
    caplog: pytest.LogCaptureFixture,
    case: _ProtoConversionTestCase,
) -> None:
    """Test conversion from protobuf message to Microgrid."""
    now = datetime.now(timezone.utc)
    mock_datetime_from_proto.return_value = now

    mock_microgrid_status_from_proto.return_value = case.status

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

    proto_status = microgrid_pb2.MicrogridStatus.ValueType(
        case.status.value if isinstance(case.status, MicrogridStatus) else case.status
    )

    proto = microgrid_pb2.Microgrid(
        id=1234,
        enterprise_id=5678,
        name="Test Grid" if case.has_name else "",
        status=proto_status,
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
    with caplog.at_level("DEBUG"):
        info = microgrid_from_proto(proto)

    # Verify the result
    assert info.id == MicrogridId(1234)
    assert info.enterprise_id == EnterpriseId(5678)
    assert info.create_timestamp == now

    if case.has_name:
        assert info.name == "Test Grid"
    else:
        assert info.name is None

    # Verify mock calls
    mock_datetime_from_proto.assert_called_once_with(proto.create_timestamp)
    mock_microgrid_status_from_proto.assert_called_once_with(proto.status)

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

    # Verify logging behavior
    if case.expected_log:
        expected_level, expected_message = case.expected_log
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == expected_level
        assert expected_message in caplog.records[0].message
    else:
        assert len(caplog.records) == 0
