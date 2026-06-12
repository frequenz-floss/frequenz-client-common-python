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

from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentConnection,
    ElectricalComponentId,
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
            ["missing operational lifetime, considering it always operational"],
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
    assert connection.source == ElectricalComponentId(
        proto_data["source_electrical_component_id"]
    )
    assert connection.destination == ElectricalComponentId(
        proto_data["destination_electrical_component_id"]
    )


def test_error_same_ids() -> None:
    """Test proto conversion with the same source and destination returns None."""
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

    assert conn is None
    assert major_issues == [
        "connection ignored: source and destination are the same (CID1)"
    ]
    assert not minor_issues


@patch(
    "frequenz.client.common.microgrid.electrical_components.proto.v1alpha8."
    "_electrical_component_connection.lifetime_from_proto",
    autospec=True,
)
def test_invalid_lifetime(mock_lifetime_from_proto: Mock) -> None:
    """Test proto conversion with invalid lifetime data."""
    mock_lifetime_from_proto.side_effect = ValueError("Invalid lifetime")

    proto = electrical_components_pb2.ElectricalComponentConnection(
        source_electrical_component_id=1, destination_electrical_component_id=2
    )
    now = datetime.now(timezone.utc)
    start_time = timestamp_pb2.Timestamp()
    start_time.FromDatetime(now)
    lifetime = lifetime_pb2.Lifetime()
    lifetime.start_timestamp.CopyFrom(start_time)
    proto.operational_lifetime.CopyFrom(lifetime)

    major_issues: list[str] = []
    minor_issues: list[str] = []
    connection = electrical_component_connection_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert connection is not None
    assert connection.source == ElectricalComponentId(1)
    assert connection.destination == ElectricalComponentId(2)
    assert major_issues == [
        "invalid operational lifetime (Invalid lifetime), considering it as missing "
        "(i.e. always operational)"
    ]
    assert not minor_issues
    mock_lifetime_from_proto.assert_called_once_with(proto.operational_lifetime)


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

    # mypy needs the explicit return
    def _fake_from_proto_with_issues(  # pylint: disable=useless-return
        _: electrical_components_pb2.ElectricalComponentConnection,
        *,
        major_issues: list[str],
        minor_issues: list[str],
    ) -> ElectricalComponentConnection | None:
        """Fake function to simulate conversion and logging."""
        major_issues.append("fake major issue")
        minor_issues.append("fake minor issue")
        return None

    mock_from_proto_with_issues.side_effect = _fake_from_proto_with_issues

    mock_proto = Mock(
        name="proto", spec=electrical_components_pb2.ElectricalComponentConnection
    )
    connection = electrical_component_connection_from_proto(mock_proto)

    assert connection is None
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
