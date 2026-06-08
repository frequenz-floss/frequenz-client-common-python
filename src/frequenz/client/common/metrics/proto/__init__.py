# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Deprecated compatibility shim for metrics proto conversion functions."""

from frequenz.api.common.v1alpha8.metrics import bounds_pb2, metrics_pb2
from typing_extensions import deprecated

from .._bounds import Bounds
from .._sample import AggregatedMetricValue, MetricConnection, MetricSample
from . import v1alpha8

_DEPRECATED_MESSAGE = (
    "frequenz.client.common.metrics.proto is deprecated. "
    "Use frequenz.client.common.metrics.proto.v1alpha8 instead."
)


@deprecated(_DEPRECATED_MESSAGE)
def bounds_from_proto(message: bounds_pb2.Bounds) -> Bounds:
    """Create a `Bounds` object from a protobuf message.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding `Bounds` object.
    """
    return v1alpha8.bounds_from_proto(message)


@deprecated(_DEPRECATED_MESSAGE)
def bounds_from_proto_with_issues(
    message: bounds_pb2.Bounds,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> Bounds | None:
    """Create a `Bounds` object from a protobuf message, collecting issues.

    Args:
        message: The protobuf message to convert.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The corresponding `Bounds` object.
    """
    return v1alpha8.bounds_from_proto_with_issues(
        message, major_issues=major_issues, minor_issues=minor_issues
    )


@deprecated(_DEPRECATED_MESSAGE)
def aggregated_metric_sample_from_proto(
    message: metrics_pb2.AggregatedMetricValue,
) -> AggregatedMetricValue:
    """Convert a protobuf message to a `AggregatedMetricValue` object.

    Args:
        message: The protobuf message to convert.

    Returns:
        The resulting `AggregatedMetricValue` object.
    """
    return v1alpha8.aggregated_metric_sample_from_proto(message)


@deprecated(_DEPRECATED_MESSAGE)
def metric_connection_from_proto_with_issues(
    message: metrics_pb2.MetricConnection,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> MetricConnection:
    """Convert a protobuf message to a `MetricConnection` object.

    Args:
        message: The protobuf message to convert.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The resulting `MetricConnection` object.
    """
    return v1alpha8.metric_connection_from_proto_with_issues(
        message, major_issues=major_issues, minor_issues=minor_issues
    )


@deprecated(_DEPRECATED_MESSAGE)
def metric_sample_from_proto_with_issues(
    message: metrics_pb2.MetricSample,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> MetricSample:
    """Convert a protobuf message to a `MetricSample` object.

    Args:
        message: The protobuf message to convert.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The resulting `MetricSample` object.
    """
    return v1alpha8.metric_sample_from_proto_with_issues(
        message, major_issues=major_issues, minor_issues=minor_issues
    )


__all__ = [
    "aggregated_metric_sample_from_proto",
    "bounds_from_proto",
    "bounds_from_proto_with_issues",
    "metric_connection_from_proto_with_issues",
    "metric_sample_from_proto_with_issues",
]
