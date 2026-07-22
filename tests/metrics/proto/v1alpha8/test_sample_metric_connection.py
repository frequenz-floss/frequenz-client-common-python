# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for MetricConnection protobuf conversion."""

import warnings

from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from frequenz.client.common.metrics import MetricConnectionCategory
from frequenz.client.common.metrics.proto.v1alpha8 import (
    metric_connection_category_to_proto,
    metric_connection_from_proto,
    metric_connection_from_proto_with_issues,
)


def test_with_unspecified_category() -> None:
    """Test conversion with unspecified category stores int 0 and reports it.

    The conversion must store the raw int ``0`` (not the deprecated member) and
    must not emit any ``DeprecationWarning`` of its own.
    """
    proto = metrics_pb2.MetricConnection(
        category=metrics_pb2.MetricConnectionCategory.METRIC_CONNECTION_CATEGORY_UNSPECIFIED,
        name="some_connection",
    )

    major_issues: list[str] = []
    minor_issues: list[str] = []

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        connection = metric_connection_from_proto_with_issues(
            proto, major_issues=major_issues, minor_issues=minor_issues
        )

    assert connection.category == 0
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
    assert not connection.name
    assert not major_issues
    assert not minor_issues


def test_from_proto_unspecified_category() -> None:
    """An unspecified category is stored as the raw int 0 without warning."""
    proto = metrics_pb2.MetricConnection(
        category=metrics_pb2.MetricConnectionCategory.METRIC_CONNECTION_CATEGORY_UNSPECIFIED,
        name="some_connection",
    )

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        connection = metric_connection_from_proto(proto)

    assert connection.category == 0
    assert connection.name == "some_connection"


def test_from_proto_unrecognized_category() -> None:
    """An unrecognized category is preserved as its raw int value."""
    proto = metrics_pb2.MetricConnection(
        category=9999,  # type: ignore[arg-type]
        name="unknown_connection",
    )

    connection = metric_connection_from_proto(proto)

    assert connection.category == 9999
    assert connection.name == "unknown_connection"


def test_from_proto_valid_category() -> None:
    """A valid category is resolved to its member."""
    proto = metrics_pb2.MetricConnection(
        category=metric_connection_category_to_proto(MetricConnectionCategory.BATTERY),
        name="dc_battery_0",
    )

    connection = metric_connection_from_proto(proto)

    assert connection.category == MetricConnectionCategory.BATTERY
    assert connection.name == "dc_battery_0"


def test_from_proto_empty_name() -> None:
    """An empty name is preserved."""
    proto = metrics_pb2.MetricConnection(
        category=metric_connection_category_to_proto(MetricConnectionCategory.PV),
        name="",
    )

    connection = metric_connection_from_proto(proto)

    assert connection.category == MetricConnectionCategory.PV
    assert not connection.name
