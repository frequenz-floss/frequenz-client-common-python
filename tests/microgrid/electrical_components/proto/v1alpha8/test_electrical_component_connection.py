# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests conversion from protobuf messages to ElectricalComponentConnection."""

import logging
from datetime import datetime, timezone
from typing import Any
from unittest.mock import Mock, patch

import pytest
from frequenz.api.common.v1alpha8.microgrid import lifetime_pb2
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)
from google.protobuf import timestamp_pb2

from frequenz.client.common.microgrid import InvalidLifetime, Lifetime
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentConnection,
    ElectricalComponentId,
    SelfReferencingElectricalComponentConnection,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_connection_from_proto,
    electrical_component_connection_from_proto_with_issues,
)


@pytest.mark.parametrize(
    "proto_data, expected_minor_issues",
    [
        pytest.param(
            {
                "source_electrical_component_id": 1,
                "destination_electrical_component_id": 2,
                "has_lifetime": True,
            },
            [],
            id="full",
        ),
        pytest.param(
            {
                "source_electrical_component_id": 1,
                "destination_electrical_component_id": 2,
                "has_lifetime": False,
            },
            [],
            id="no_lifetime",
        ),
    ],
)
def test_success(proto_data: dict[str, Any], expected_minor_issues: list[str]) -> None:
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

    major_issues: list[str] = []
    minor_issues: list[str] = []
    connection = electrical_component_connection_from_proto_with_issues(
        proto,
        major_issues=major_issues,
        minor_issues=minor_issues,
    )

    assert connection is not None
    assert not major_issues
    assert minor_issues == expected_minor_issues
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
    major_issues: list[str] = []
    minor_issues: list[str] = []

    assert proto.HasField("operational_lifetime")
    connection = electrical_component_connection_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert connection.operational_lifetime == Lifetime()
    assert not major_issues
    assert not minor_issues


def test_self_referencing_same_ids() -> None:
    """Test proto conversion with the same source and destination returns a self-ref."""
    proto = electrical_components_pb2.ElectricalComponentConnection(
        source_electrical_component_id=1, destination_electrical_component_id=1
    )

    major_issues: list[str] = []
    minor_issues: list[str] = []
    conn = electrical_component_connection_from_proto_with_issues(
        proto,
        major_issues=major_issues,
        minor_issues=minor_issues,
    )

    assert isinstance(conn, SelfReferencingElectricalComponentConnection)
    assert conn.source_id == ElectricalComponentId(1)
    assert conn.destination_id == ElectricalComponentId(1)
    assert major_issues == [
        "self-referencing connection: source and destination are the same (CID1)"
    ]
    assert not minor_issues


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

    major_issues: list[str] = []
    minor_issues: list[str] = []
    connection = electrical_component_connection_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

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
    assert not major_issues
    assert not minor_issues


@patch(
    "frequenz.client.common.microgrid.electrical_components.proto.v1alpha8."
    "_electrical_component_connection."
    "electrical_component_connection_from_proto_with_issues",
    autospec=True,
)
def test_issues_logging(
    mock_from_proto_with_issues: Mock, caplog: pytest.LogCaptureFixture
) -> None:
    """Test collection and logging of issues during proto conversion."""
    caplog.set_level("DEBUG")  # Ensure we capture DEBUG level messages

    fake_connection = ElectricalComponentConnection(
        source_id=ElectricalComponentId(1),
        destination_id=ElectricalComponentId(2),
    )

    def _fake_from_proto_with_issues(
        _: electrical_components_pb2.ElectricalComponentConnection,
        *,
        major_issues: list[str],
        minor_issues: list[str],
    ) -> ElectricalComponentConnection:
        """Fake function to simulate conversion and logging."""
        major_issues.append("fake major issue")
        minor_issues.append("fake minor issue")
        return fake_connection

    mock_from_proto_with_issues.side_effect = _fake_from_proto_with_issues

    mock_proto = Mock(
        name="proto", spec=electrical_components_pb2.ElectricalComponentConnection
    )
    connection = electrical_component_connection_from_proto(mock_proto)

    assert connection is fake_connection
    assert caplog.record_tuples == [
        (
            "frequenz.client.common.microgrid.electrical_components.proto.v1alpha8."
            "_electrical_component_connection",
            logging.WARNING,
            "Found issues in electrical component connection: fake major issue | "
            f"Protobuf message:\n{mock_proto}",
        ),
        (
            "frequenz.client.common.microgrid.electrical_components.proto.v1alpha8."
            "_electrical_component_connection",
            logging.DEBUG,
            "Found minor issues in electrical component connection: fake minor issue | "
            f"Protobuf message:\n{mock_proto}",
        ),
    ]
