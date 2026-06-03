# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for MetricConnection protobuf conversion."""

from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from frequenz.client.common.metrics import MetricConnectionCategory
from frequenz.client.common.metrics.proto.v1alpha8 import (
    metric_connection_category_to_proto,
    metric_connection_from_proto_with_issues,
)


def test_with_unspecified_category() -> None:
    """Test conversion with UNSPECIFIED category reports major issue."""
    proto = metrics_pb2.MetricConnection(
        category=metric_connection_category_to_proto(
            MetricConnectionCategory.UNSPECIFIED
        ),
        name="some_connection",
    )

    major_issues: list[str] = []
    minor_issues: list[str] = []

    connection = metric_connection_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert connection.category == MetricConnectionCategory.UNSPECIFIED
    assert connection.name == "some_connection"
    assert major_issues == ["unspecified category"]
    assert not minor_issues


def test_with_unrecognized_category() -> None:
    """Test conversion with unrecognized category reports minor issue."""
    proto = metrics_pb2.MetricConnection(
        category=9999,  # type: ignore[arg-type]
        name="unknown_connection",
    )

    major_issues: list[str] = []
    minor_issues: list[str] = []

    connection = metric_connection_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert connection.category == 9999
    assert connection.name == "unknown_connection"
    assert not major_issues
    assert minor_issues == ["unrecognized category 9999"]


def test_with_valid_category() -> None:
    """Test conversion with valid category does not report issues."""
    proto = metrics_pb2.MetricConnection(
        category=metric_connection_category_to_proto(MetricConnectionCategory.BATTERY),
        name="dc_battery_0",
    )

    major_issues: list[str] = []
    minor_issues: list[str] = []

    connection = metric_connection_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert connection.category == MetricConnectionCategory.BATTERY
    assert connection.name == "dc_battery_0"
    assert not major_issues
    assert not minor_issues


def test_with_empty_name() -> None:
    """Test conversion with empty name becomes None."""
    proto = metrics_pb2.MetricConnection(
        category=metric_connection_category_to_proto(MetricConnectionCategory.PV),
        name="",
    )

    major_issues: list[str] = []
    minor_issues: list[str] = []

    connection = metric_connection_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert connection.category == MetricConnectionCategory.PV
    assert connection.name is None
    assert not major_issues
    assert not minor_issues
