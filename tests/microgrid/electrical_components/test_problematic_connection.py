# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for problematic electrical component connections."""

from datetime import datetime, timezone

import pytest

from frequenz.client.common.microgrid import Lifetime
from frequenz.client.common.microgrid.electrical_components import (
    BaseElectricalComponentConnection,
    ElectricalComponentConnection,
    ElectricalComponentId,
    ProblematicElectricalComponentConnection,
    SelfReferencingElectricalComponentConnection,
)


def test_abstract_problematic_connection_cannot_be_instantiated() -> None:
    """Test that ProblematicElectricalComponentConnection cannot be instantiated."""
    with pytest.raises(
        TypeError,
        match="Cannot instantiate ProblematicElectricalComponentConnection directly",
    ):
        ProblematicElectricalComponentConnection(
            source_id=ElectricalComponentId(1),
            destination_id=ElectricalComponentId(1),
        )


def test_self_referencing_connection_creation() -> None:
    """Test basic SelfReferencingElectricalComponentConnection creation."""
    now = datetime.now(timezone.utc)
    lifetime = Lifetime(start_time=now)
    connection = SelfReferencingElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(1),
        operational_lifetime=lifetime,
    )

    assert connection.source_id == ElectricalComponentId(1)
    assert connection.destination_id == ElectricalComponentId(1)
    assert connection.operational_lifetime == lifetime


def test_self_referencing_connection_defaults() -> None:
    """Test SelfReferencingElectricalComponentConnection with default lifetime."""
    connection = SelfReferencingElectricalComponentConnection(
        source_id=ElectricalComponentId(42),
        destination_id=ElectricalComponentId(42),
    )

    assert connection.source_id == ElectricalComponentId(42)
    assert connection.destination_id == ElectricalComponentId(42)
    assert connection.operational_lifetime == Lifetime()


def test_self_referencing_connection_rejects_different_ids() -> None:
    """Test that SelfReferencingElectricalComponentConnection rejects different IDs."""
    with pytest.raises(
        ValueError,
        match=(
            "Source and destination components must be the same for a "
            "self-referencing electrical component connection"
        ),
    ):
        SelfReferencingElectricalComponentConnection(
            source_id=ElectricalComponentId(1),
            destination_id=ElectricalComponentId(2),
        )


def test_self_referencing_connection_hierarchy() -> None:
    """Test the class hierarchy of SelfReferencingElectricalComponentConnection."""
    connection = SelfReferencingElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(1),
    )

    assert isinstance(connection, BaseElectricalComponentConnection)
    assert isinstance(connection, ProblematicElectricalComponentConnection)
    assert not isinstance(connection, ElectricalComponentConnection)


def test_self_referencing_connection_str() -> None:
    """Test string representation of SelfReferencingElectricalComponentConnection."""
    connection = SelfReferencingElectricalComponentConnection(
        source_id=ElectricalComponentId(7),
        destination_id=ElectricalComponentId(7),
    )
    assert str(connection) == "CID7->CID7"


def test_self_referencing_connection_equality_and_hash() -> None:
    """Test equality and hashing of the frozen SelfReferencingElectricalComponentConnection."""
    lifetime = Lifetime(start_time=datetime(2025, 1, 1, tzinfo=timezone.utc))
    connection = SelfReferencingElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(1),
        operational_lifetime=lifetime,
    )
    same = SelfReferencingElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(1),
        operational_lifetime=lifetime,
    )
    different = SelfReferencingElectricalComponentConnection(
        source_id=ElectricalComponentId(2),
        destination_id=ElectricalComponentId(2),
        operational_lifetime=lifetime,
    )

    assert connection == same
    assert connection != different
    assert hash(connection) == hash(same)
    assert {connection, same} == {connection}
