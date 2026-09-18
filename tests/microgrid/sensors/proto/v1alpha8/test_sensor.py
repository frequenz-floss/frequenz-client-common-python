# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the Sensor protobuf conversion."""

from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from frequenz.api.common.v1alpha8.microgrid import lifetime_pb2
from frequenz.api.common.v1alpha8.microgrid.sensors import sensors_pb2

# pylint: disable-next=no-name-in-module
from google.protobuf.timestamp_pb2 import Timestamp

from frequenz.client.common.microgrid import (
    InvalidLifetime,
    InvalidLifetimeError,
    Lifetime,
    MicrogridId,
)
from frequenz.client.common.microgrid.sensors import Sensor, SensorId
from frequenz.client.common.microgrid.sensors.proto.v1alpha8 import (
    sensor_from_proto,
)


def test_from_proto_all_fields() -> None:
    """Every wire field is converted into the wrapper."""
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    proto = sensors_pb2.Sensor(
        id=1234,
        microgrid_id=5678,
        name="Test Sensor",
        model="ACME Thermometer",
        operational_lifetime=lifetime_pb2.Lifetime(
            start_timestamp=Timestamp(seconds=int(start.timestamp()))
        ),
    )

    sensor = sensor_from_proto(proto)

    assert isinstance(sensor, Sensor)
    assert sensor.id == SensorId(1234)
    assert sensor.microgrid_id == MicrogridId(5678)
    assert sensor.name == "Test Sensor"
    assert sensor.model == "ACME Thermometer"
    assert sensor.operational_lifetime == Lifetime(start_time=start)
    assert sensor.get_operational_lifetime() == Lifetime(start_time=start)


def test_from_proto_empty_strings() -> None:
    """Unset string fields are kept as empty strings."""
    sensor = sensor_from_proto(sensors_pb2.Sensor(id=1, microgrid_id=2))

    assert sensor.name == ""
    assert sensor.model == ""


def test_from_proto_missing_lifetime_is_unbounded() -> None:
    """A missing operational lifetime becomes an unbounded `Lifetime`."""
    sensor = sensor_from_proto(sensors_pb2.Sensor(id=1, microgrid_id=2))

    assert sensor.operational_lifetime == Lifetime()
    assert sensor.is_operational_now() is True


def test_from_proto_empty_lifetime_is_unbounded() -> None:
    """A present but empty operational lifetime becomes an unbounded `Lifetime`."""
    proto = sensors_pb2.Sensor(
        id=1, microgrid_id=2, operational_lifetime=lifetime_pb2.Lifetime()
    )

    sensor = sensor_from_proto(proto)

    assert sensor.operational_lifetime == Lifetime()


@patch(
    "frequenz.client.common.microgrid.sensors.proto.v1alpha8._sensor.lifetime_from_proto"
)
def test_from_proto_delegates_lifetime(mock_lifetime_from_proto: Mock) -> None:
    """The lifetime conversion is delegated to `lifetime_from_proto`."""
    lifetime = Lifetime()
    mock_lifetime_from_proto.return_value = lifetime
    proto = sensors_pb2.Sensor(
        id=1, microgrid_id=2, operational_lifetime=lifetime_pb2.Lifetime()
    )

    sensor = sensor_from_proto(proto)

    mock_lifetime_from_proto.assert_called_once_with(proto.operational_lifetime)
    assert sensor.operational_lifetime is lifetime


@patch(
    "frequenz.client.common.microgrid.sensors.proto.v1alpha8._sensor.lifetime_from_proto"
)
def test_from_proto_missing_lifetime_skips_delegation(
    mock_lifetime_from_proto: Mock,
) -> None:
    """A missing lifetime does not call `lifetime_from_proto`."""
    sensor_from_proto(sensors_pb2.Sensor(id=1, microgrid_id=2))

    mock_lifetime_from_proto.assert_not_called()


@pytest.mark.parametrize(
    "lifetime",
    [
        pytest.param(
            lifetime_pb2.Lifetime(
                start_timestamp=Timestamp(seconds=200),
                end_timestamp=Timestamp(seconds=100),
            ),
            id="reversed-range",
        ),
        pytest.param(
            lifetime_pb2.Lifetime(start_timestamp=Timestamp(seconds=0, nanos=-1)),
            id="negative-nanos",
        ),
    ],
)
def test_from_proto_malformed_lifetime_is_preserved(
    lifetime: lifetime_pb2.Lifetime,
) -> None:
    """A malformed operational lifetime is preserved as an `InvalidLifetime`."""
    proto = sensors_pb2.Sensor(id=1, microgrid_id=2, operational_lifetime=lifetime)

    sensor = sensor_from_proto(proto)

    assert isinstance(sensor.operational_lifetime, InvalidLifetime)
    with pytest.raises(InvalidLifetimeError) as exc_info:
        sensor.get_operational_lifetime()
    assert exc_info.value.lifetime is sensor.operational_lifetime
