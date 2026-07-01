# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Loading of MetricSample and AggregatedMetricValue objects from protobuf messages."""

from collections.abc import Sequence

from frequenz.api.common.v1alpha8.metrics import bounds_pb2, metrics_pb2
from frequenz.core.math import Interval

from ....proto import datetime_from_proto
from ..._metric import Metric
from ..._sample import (
    AggregatedMetricValue,
    MetricConnection,
    MetricConnectionCategory,
    MetricSample,
)
from ._bounds import bounds_from_proto2
from ._metric import metric_from_proto
from ._metric_connection_category import metric_connection_category_from_proto


def aggregated_metric_sample_from_proto(
    message: metrics_pb2.AggregatedMetricValue,
) -> AggregatedMetricValue:
    """Convert a protobuf message to an [`AggregatedMetricValue`][....AggregatedMetricValue] object.

    Args:
        message: The protobuf message to convert.

    Returns:
        The resulting [`AggregatedMetricValue`][....AggregatedMetricValue] object.
    """
    return AggregatedMetricValue(
        avg=message.avg_value,
        min=message.min_value if message.HasField("min_value") else None,
        max=message.max_value if message.HasField("max_value") else None,
        raw=message.raw_values,
    )


def metric_connection_from_proto_with_issues(
    message: metrics_pb2.MetricConnection,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> MetricConnection:
    """Convert a protobuf message to a [`MetricConnection`][....MetricConnection] object.

    Args:
        message: The protobuf message to convert.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The resulting [`MetricConnection`][....MetricConnection] object.
    """
    raw = message.category
    category: MetricConnectionCategory | int = (
        raw if raw == 0 else metric_connection_category_from_proto(raw)
    )

    if raw == 0:
        major_issues.append("unspecified category")
    elif isinstance(category, int):
        minor_issues.append(f"unrecognized category {category}")

    return MetricConnection(
        category=category,
        name=message.name or None,
    )


def metric_sample_from_proto_with_issues(
    message: metrics_pb2.MetricSample,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> MetricSample:
    """Convert a protobuf message to a [`MetricSample`][....MetricSample] object.

    Args:
        message: The protobuf message to convert.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The resulting [`MetricSample`][....MetricSample] object.
    """
    sample_time = datetime_from_proto(message.sample_time)

    raw_metric = message.metric
    metric: Metric | int = (
        raw_metric if raw_metric == 0 else metric_from_proto(raw_metric)
    )

    value: float | AggregatedMetricValue | None = None
    if message.HasField("value"):
        match message.value.WhichOneof("metric_value_variant"):
            case "simple_metric":
                value = message.value.simple_metric.value
            case "aggregated_metric":
                value = aggregated_metric_sample_from_proto(
                    message.value.aggregated_metric
                )

    bounds = _metric_bounds_from_proto(
        metric, message.bounds, major_issues=major_issues, minor_issues=minor_issues
    )

    connection = None
    if message.HasField("connection"):
        connection = metric_connection_from_proto_with_issues(
            message.connection, major_issues=major_issues, minor_issues=minor_issues
        )

    return MetricSample(
        sample_time=sample_time,
        metric=metric,
        value=value,
        bounds=bounds,
        connection=connection,
    )


def _metric_bounds_from_proto(
    metric: Metric | int,
    messages: Sequence[bounds_pb2.Bounds],
    *,
    major_issues: list[str],
    minor_issues: list[str],  # pylint:disable=unused-argument
) -> list[Interval[float | None]]:
    """Convert a sequence of bounds messages to a list of [`Interval`][frequenz.core.math.Interval].

    Args:
        metric: The metric for which the bounds are defined, used for logging issues.
        messages: The sequence of bounds messages.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The resulting list of [`Interval`][frequenz.core.math.Interval].
    """
    bounds: list[Interval[float | None]] = []
    for pb_bound in messages:
        try:
            bound = bounds_from_proto2(pb_bound)
        except ValueError as exc:
            metric_name = metric if isinstance(metric, int) else metric.name
            major_issues.append(
                f"bounds for {metric_name} is invalid ({exc}), ignoring these bounds"
            )
            continue
        bounds.append(bound)

    return bounds
