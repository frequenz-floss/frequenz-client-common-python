# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the Sensor type."""

import dataclasses
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest

from frequenz.client.common.microgrid import (
    InvalidLifetime,
    InvalidLifetimeError,
    Lifetime,
    MicrogridId,
)
from frequenz.client.common.microgrid.sensors import Sensor, SensorId


def _make_sensor(
    *,
    sensor_id: int = 1234,
    microgrid_id: int = 5678,
    name: str = "Test Sensor",
    model: str = "ACME Thermometer",
    operational_lifetime: Lifetime | InvalidLifetime = Lifetime(),
) -> Sensor:
    """Build a Sensor bypassing the construction guard."""
    return Sensor(
        id=SensorId(sensor_id),
        microgrid_id=MicrogridId(microgrid_id),
        name=name,
        model=model,
        operational_lifetime=operational_lifetime,
        _allow_construction=True,
    )


def test_creation() -> None:
    """Test Sensor creation with all fields."""
    lifetime = Lifetime(start_time=datetime(2025, 1, 1, tzinfo=timezone.utc))
    sensor = _make_sensor(operational_lifetime=lifetime)

    assert sensor.id == SensorId(1234)
    assert sensor.microgrid_id == MicrogridId(5678)
    assert sensor.name == "Test Sensor"
    assert sensor.model == "ACME Thermometer"
    assert sensor.operational_lifetime is lifetime


def test_creation_defaults_to_unbounded_lifetime() -> None:
    """The operational lifetime defaults to an unbounded `Lifetime`."""
    sensor = Sensor(
        id=SensorId(1234),
        microgrid_id=MicrogridId(5678),
        name="",
        model="",
        _allow_construction=True,
    )
    assert sensor.operational_lifetime == Lifetime()


def test_direct_construction_raises() -> None:
    """Constructing a Sensor without the gate flag raises TypeError."""
    with pytest.raises(TypeError, match="cannot be constructed directly"):
        Sensor(
            id=SensorId(1234),
            microgrid_id=MicrogridId(5678),
            name="",
            model="",
        )


def test_replace_preserves_construction() -> None:
    """`dataclasses.replace` on a gated instance works."""
    sensor = _make_sensor()
    replaced = dataclasses.replace(sensor, name="renamed")
    assert replaced.name == "renamed"
    assert replaced.id == sensor.id


def test_frozen() -> None:
    """Sensor instances are immutable."""
    sensor = _make_sensor()
    with pytest.raises(dataclasses.FrozenInstanceError):
        sensor.name = "other"  # type: ignore[misc]


@pytest.mark.parametrize(
    "name,expected_str",
    [
        pytest.param("Test Sensor", "SID1234:Test Sensor", id="with-name"),
        pytest.param("", "SID1234", id="empty-name"),
    ],
)
def test_str(name: str, expected_str: str) -> None:
    """Test string representation of Sensor."""
    assert str(_make_sensor(name=name)) == expected_str


def test_get_operational_lifetime_returns_valid() -> None:
    """`get_operational_lifetime()` returns a valid lifetime unchanged."""
    lifetime = Lifetime()
    sensor = _make_sensor(operational_lifetime=lifetime)
    assert sensor.get_operational_lifetime() is lifetime


def test_get_operational_lifetime_raises_invalid() -> None:
    """`get_operational_lifetime()` raises with the malformed lifetime attached."""
    invalid = InvalidLifetime(
        start_time=datetime(2025, 2, 1, tzinfo=timezone.utc),
        end_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    sensor = _make_sensor(operational_lifetime=invalid)

    with pytest.raises(InvalidLifetimeError) as exc_info:
        sensor.get_operational_lifetime()
    assert exc_info.value.lifetime is invalid


def test_get_operational_lifetime_error_is_value_error() -> None:
    """The `InvalidLifetimeError` raised by the accessor is also a `ValueError`."""
    sensor = _make_sensor(operational_lifetime=InvalidLifetime())
    with pytest.raises(ValueError):
        sensor.get_operational_lifetime()


@pytest.mark.parametrize(
    "is_operational", [True, False], ids=["operational", "not-operational"]
)
def test_is_operational_at(is_operational: bool) -> None:
    """`is_operational_at()` delegates to the lifetime."""
    mock_lifetime = Mock(spec=Lifetime)
    mock_lifetime.is_operational_at.return_value = is_operational
    sensor = _make_sensor(operational_lifetime=mock_lifetime)
    timestamp = datetime(2025, 1, 1, tzinfo=timezone.utc)

    assert sensor.is_operational_at(timestamp) is is_operational

    mock_lifetime.is_operational_at.assert_called_once_with(timestamp)


def test_is_operational_at_raises_for_invalid_lifetime() -> None:
    """`is_operational_at()` raises when the lifetime is invalid."""
    sensor = _make_sensor(operational_lifetime=InvalidLifetime())
    with pytest.raises(InvalidLifetimeError):
        sensor.is_operational_at(datetime(2025, 1, 1, tzinfo=timezone.utc))


@patch("frequenz.client.common.microgrid.sensors._sensor.datetime")
def test_is_operational_now(mock_datetime: Mock) -> None:
    """`is_operational_now()` checks the lifetime at the current UTC time."""
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.side_effect = lambda tz: now.replace(tzinfo=tz)
    mock_lifetime = Mock(spec=Lifetime)
    mock_lifetime.is_operational_at.return_value = True
    sensor = _make_sensor(operational_lifetime=mock_lifetime)

    assert sensor.is_operational_now() is True

    mock_lifetime.is_operational_at.assert_called_once_with(now)


def test_is_operational_now_raises_for_invalid_lifetime() -> None:
    """`is_operational_now()` raises when the lifetime is invalid."""
    sensor = _make_sensor(operational_lifetime=InvalidLifetime())
    with pytest.raises(InvalidLifetimeError):
        sensor.is_operational_now()


def test_identity() -> None:
    """The identity is the sensor ID and microgrid ID only."""
    sensor = _make_sensor()

    assert sensor.identity == (SensorId(1234), MicrogridId(5678))
    assert sensor.identity == _make_sensor(name="other", model="other").identity
    assert sensor.identity != _make_sensor(sensor_id=1).identity
    assert sensor.identity != _make_sensor(microgrid_id=1).identity


def test_equality_and_hash() -> None:
    """Equal sensors compare equal and hash the same; the guard is ignored."""
    sensor = _make_sensor()
    same = _make_sensor()
    different = _make_sensor(name="other")

    assert sensor == same
    assert hash(sensor) == hash(same)
    assert sensor != different
