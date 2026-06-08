# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for metrics proto compatibility shim."""

import pytest
from frequenz.api.common.v1alpha8.metrics import bounds_pb2, metrics_pb2
from google.protobuf import timestamp_pb2

from frequenz.client.common.metrics.proto import (
    aggregated_metric_sample_from_proto,
    bounds_from_proto,
    bounds_from_proto_with_issues,
    metric_connection_from_proto_with_issues,
    metric_sample_from_proto_with_issues,
)


def test_bounds_from_proto_shim_warns() -> None:
    """Test the old metrics proto path warns when called."""
    with pytest.deprecated_call():
        bounds_from_proto(bounds_pb2.Bounds(lower=1.0, upper=2.0))


def test_bounds_from_proto_with_issues_shim_warns() -> None:
    """Test the old metrics proto path warns when called."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    with pytest.deprecated_call():
        bounds_from_proto_with_issues(
            bounds_pb2.Bounds(lower=1.0, upper=2.0),
            major_issues=major_issues,
            minor_issues=minor_issues,
        )


def test_metric_connection_from_proto_with_issues_shim_warns() -> None:
    """Test the old metrics proto path warns when called."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    message = metrics_pb2.MetricConnection(
        category=metrics_pb2.METRIC_CONNECTION_CATEGORY_UNSPECIFIED
    )
    with pytest.deprecated_call():
        metric_connection_from_proto_with_issues(
            message, major_issues=major_issues, minor_issues=minor_issues
        )


def test_metric_sample_from_proto_with_issues_shim_warns() -> None:
    """Test the old metrics proto path warns when called."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    message = metrics_pb2.MetricSample(
        metric=metrics_pb2.METRIC_AC_CURRENT,
        sample_time=timestamp_pb2.Timestamp(seconds=1234567890),
    )
    with pytest.deprecated_call():
        metric_sample_from_proto_with_issues(
            message, major_issues=major_issues, minor_issues=minor_issues
        )


def test_aggregated_metric_sample_from_proto_shim_warns() -> None:
    """Test the old metrics proto path warns when called."""
    message = metrics_pb2.AggregatedMetricValue(
        avg_value=1.0, min_value=0.5, max_value=1.5
    )
    with pytest.deprecated_call():
        aggregated_metric_sample_from_proto(message)
