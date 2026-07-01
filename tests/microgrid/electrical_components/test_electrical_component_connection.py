# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for ElectricalComponentConnection class and related functionality."""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, Mock, patch

import pytest
from frequenz.core.math import Interval

from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentConnection,
    ElectricalComponentId,
)


def test_creation() -> None:
    """Test basic ElectricalComponentConnection creation and validation."""
    now = datetime.now(timezone.utc)
    lifetime = Interval[datetime | None](now, None)
    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=lifetime,
    )

    assert connection.source_id == ElectricalComponentId(1)
    assert connection.destination_id == ElectricalComponentId(2)
    assert connection.operational_lifetime == lifetime


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
    lifetime = Interval[datetime | None](
        datetime(2025, 1, 1, tzinfo=timezone.utc), None
    )
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
        operational_lifetime=Interval[datetime | None](start, end),
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
    mock_lifetime = MagicMock(spec=Interval)
    mock_lifetime.__contains__.return_value = lifetime_active

    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=mock_lifetime,
    )

    now = datetime.now(timezone.utc)
    assert connection.is_operational_at(now) == lifetime_active
    mock_lifetime.__contains__.assert_called_once_with(now)


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
    mock_lifetime = MagicMock(spec=Interval)
    mock_lifetime.__contains__.return_value = lifetime_active

    connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=mock_lifetime,
    )

    assert connection.is_operational_now() is lifetime_active
    mock_lifetime.__contains__.assert_called_once_with(now)
    mock_datetime.now.assert_called_once_with(timezone.utc)
