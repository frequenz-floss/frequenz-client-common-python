# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests conversion from protobuf messages to ElectricalComponentConnection."""

from datetime import datetime, timezone
from typing import Any

import pytest
from frequenz.api.common.v1alpha8.microgrid import lifetime_pb2
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)
from google.protobuf import timestamp_pb2

from frequenz.client.common.microgrid import InvalidLifetime, Lifetime
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentId,
    SelfReferencingElectricalComponentConnection,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_connection_from_proto,
)


@pytest.mark.parametrize(
    "proto_data",
    [
        pytest.param(
            {
                "source_electrical_component_id": 1,
                "destination_electrical_component_id": 2,
                "has_lifetime": True,
            },
            id="full",
        ),
        pytest.param(
            {
                "source_electrical_component_id": 1,
                "destination_electrical_component_id": 2,
                "has_lifetime": False,
            },
            id="no_lifetime",
        ),
    ],
)
def test_success(proto_data: dict[str, Any]) -> None:
    """Test successful conversion to ElectricalComponentConnection."""
    proto = electrical_components_pb2.ElectricalComponentConnection(
        source_electrical_component_id=proto_data["source_electrical_component_id"],
        destination_electrical_component_id=proto_data[
            "destination_electrical_component_id"
        ],
    )

    if proto_data["has_lifetime"]:
        now = datetime.now(timezone.utc)
        start_time = timestamp_pb2.Timestamp()
        start_time.FromDatetime(now)
        lifetime = lifetime_pb2.Lifetime()
        lifetime.start_timestamp.CopyFrom(start_time)
        proto.operational_lifetime.CopyFrom(lifetime)

    connection = electrical_component_connection_from_proto(proto)

    assert connection is not None
    assert connection.source_id == ElectricalComponentId(
        proto_data["source_electrical_component_id"]
    )
    assert connection.destination_id == ElectricalComponentId(
        proto_data["destination_electrical_component_id"]
    )
    if proto_data["has_lifetime"]:
        assert isinstance(connection.operational_lifetime, Lifetime)
        assert connection.operational_lifetime.start_time is not None
    else:
        assert connection.operational_lifetime == Lifetime()


def test_empty_lifetime_is_unbounded() -> None:
    """A present but empty protobuf lifetime becomes an unbounded `Lifetime`."""
    proto = electrical_components_pb2.ElectricalComponentConnection(
        source_electrical_component_id=1,
        destination_electrical_component_id=2,
        operational_lifetime=lifetime_pb2.Lifetime(),
    )

    assert proto.HasField("operational_lifetime")
    connection = electrical_component_connection_from_proto(proto)

    assert connection.operational_lifetime == Lifetime()


def test_self_referencing_same_ids() -> None:
    """Test proto conversion with the same source and destination returns a self-ref."""
    proto = electrical_components_pb2.ElectricalComponentConnection(
        source_electrical_component_id=1, destination_electrical_component_id=1
    )

    conn = electrical_component_connection_from_proto(proto)

    assert isinstance(conn, SelfReferencingElectricalComponentConnection)
    assert conn.source_id == ElectricalComponentId(1)
    assert conn.destination_id == ElectricalComponentId(1)


def test_invalid_lifetime() -> None:
    """Test proto conversion with invalid lifetime data."""
    proto = electrical_components_pb2.ElectricalComponentConnection(
        source_electrical_component_id=1, destination_electrical_component_id=2
    )
    start_time = timestamp_pb2.Timestamp()
    start_time.FromDatetime(datetime(2025, 2, 1, tzinfo=timezone.utc))
    end_time = timestamp_pb2.Timestamp()
    end_time.FromDatetime(datetime(2025, 1, 1, tzinfo=timezone.utc))
    proto.operational_lifetime.CopyFrom(
        lifetime_pb2.Lifetime(
            start_timestamp=start_time,
            end_timestamp=end_time,
        )
    )

    connection = electrical_component_connection_from_proto(proto)

    assert connection is not None
    assert connection.source_id == ElectricalComponentId(1)
    assert connection.destination_id == ElectricalComponentId(2)
    assert isinstance(connection.operational_lifetime, InvalidLifetime)
    assert connection.operational_lifetime.start_time == datetime(
        2025, 2, 1, tzinfo=timezone.utc
    )
    assert connection.operational_lifetime.end_time == datetime(
        2025, 1, 1, tzinfo=timezone.utc
    )
