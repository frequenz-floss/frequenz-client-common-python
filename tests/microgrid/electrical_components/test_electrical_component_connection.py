# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for ElectricalComponentConnection class and related functionality."""

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

import pytest

from frequenz.client.common.microgrid import (
    InvalidLifetime,
    InvalidLifetimeError,
    Lifetime,
)
from frequenz.client.common.microgrid.electrical_components import (
    BaseElectricalComponentConnection,
    ElectricalComponentConnection,
    ElectricalComponentId,
)


def _make_connection(
    operational_lifetime: Lifetime | InvalidLifetime,
) -> ElectricalComponentConnection:
    """Build a connection with the given operational lifetime."""
    return ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=operational_lifetime,
    )


def test_abstract_base_cannot_be_instantiated() -> None:
    """Test that BaseElectricalComponentConnection cannot be instantiated directly."""
    with pytest.raises(
        TypeError, match="Cannot instantiate BaseElectricalComponentConnection directly"
    ):
        BaseElectricalComponentConnection(
            source_id=ElectricalComponentId(1),
            destination_id=ElectricalComponentId(2),
        )


def test_creation() -> None:
    """Test basic ElectricalComponentConnection creation and validation."""
    now = datetime.now(timezone.utc)
    lifetime = Lifetime(start_time=now)
    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=lifetime,
    )

    assert connection.source_id == ElectricalComponentId(1)
    assert connection.destination_id == ElectricalComponentId(2)
    assert connection.operational_lifetime == lifetime


def test_creation_default_lifetime_is_unbounded() -> None:
    """A connection with no lifetime stores an unbounded lifetime."""
    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
    )

    assert connection.operational_lifetime == Lifetime()


def test_get_operational_lifetime_returns_valid() -> None:
    """`get_operational_lifetime()` returns a valid lifetime unchanged."""
    lifetime = Lifetime()
    connection = _make_connection(lifetime)

    assert connection.get_operational_lifetime() is lifetime


def test_get_operational_lifetime_raises_invalid() -> None:
    """`get_operational_lifetime()` raises with the malformed lifetime attached."""
    invalid = InvalidLifetime(
        start_time=datetime(2025, 2, 1, tzinfo=timezone.utc),
        end_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    connection = _make_connection(invalid)

    with pytest.raises(InvalidLifetimeError) as exc_info:
        connection.get_operational_lifetime()
    assert exc_info.value.lifetime is invalid


def test_is_operational_at_raises_for_invalid_lifetime() -> None:
    """`is_operational_at()` raises when the lifetime is invalid."""
    connection = _make_connection(
        InvalidLifetime(
            start_time=datetime(2025, 2, 1, tzinfo=timezone.utc),
            end_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
    )

    with pytest.raises(InvalidLifetimeError):
        connection.is_operational_at(datetime(2025, 1, 1, tzinfo=timezone.utc))


def test_is_operational_now_raises_for_invalid_lifetime() -> None:
    """`is_operational_now()` raises when the lifetime is invalid."""
    connection = _make_connection(
        InvalidLifetime(
            start_time=datetime(2025, 2, 1, tzinfo=timezone.utc),
            end_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
    )

    with pytest.raises(InvalidLifetimeError):
        connection.is_operational_now()


def test_validation() -> None:
    """Test validation of source and destination electrical components."""
    with pytest.raises(
        ValueError, match="Source and destination components must be different"
    ):
        ElectricalComponentConnection(
            source_id=ElectricalComponentId(1), destination_id=ElectricalComponentId(1)
        )


def test_str() -> None:
    """Test string representation of ElectricalComponentConnection."""
    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1), destination_id=ElectricalComponentId(2)
    )
    assert str(connection) == "CID1->CID2"


def test_equality_and_hash() -> None:
    """Test equality and hashing of the frozen ElectricalComponentConnection."""
    lifetime = Lifetime(start_time=datetime(2025, 1, 1, tzinfo=timezone.utc))
    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=lifetime,
    )
    same = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=lifetime,
    )
    different = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(3),
        operational_lifetime=lifetime,
    )

    assert connection == same
    assert connection != different
    assert hash(connection) == hash(same)
    assert {connection, same} == {connection}


def test_is_operational_at_boundaries() -> None:
    """Test is_operational_at boundary semantics with a concrete lifetime."""
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    end = datetime(2025, 12, 31, tzinfo=timezone.utc)
    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=Lifetime(start_time=start, end_time=end),
    )

    before = start - timedelta(seconds=1)
    middle = datetime(2025, 6, 1, tzinfo=timezone.utc)
    after = end + timedelta(seconds=1)

    assert connection.is_operational_at(before) is False
    assert connection.is_operational_at(start) is True
    assert connection.is_operational_at(middle) is True
    assert connection.is_operational_at(end) is True
    assert connection.is_operational_at(after) is False


@pytest.mark.parametrize(
    "lifetime_active", [True, False], ids=["operational", "not-operational"]
)
def test_is_operational_at(lifetime_active: bool) -> None:
    """Test active_at behavior with lifetime.active values."""
    mock_lifetime = Mock(spec=Lifetime)
    mock_lifetime.is_operational_at.return_value = lifetime_active

    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=mock_lifetime,
    )

    now = datetime.now(timezone.utc)
    assert connection.is_operational_at(now) == lifetime_active
    mock_lifetime.is_operational_at.assert_called_once_with(now)


@patch(
    "frequenz.client.common.microgrid.electrical_components."
    "_electrical_component_connection.datetime"
)
@pytest.mark.parametrize(
    "lifetime_active", [True, False], ids=["operational", "not-operational"]
)
def test_is_operational_now(mock_datetime: Mock, lifetime_active: bool) -> None:
    """Test if the connection is operational at the current time."""
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.side_effect = lambda tz: now.replace(tzinfo=tz)
    mock_lifetime = Mock(spec=Lifetime)
    mock_lifetime.is_operational_at.return_value = lifetime_active

    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=mock_lifetime,
    )

    assert connection.is_operational_now() is lifetime_active
    mock_lifetime.is_operational_at.assert_called_once_with(now)
    mock_datetime.now.assert_called_once_with(timezone.utc)
