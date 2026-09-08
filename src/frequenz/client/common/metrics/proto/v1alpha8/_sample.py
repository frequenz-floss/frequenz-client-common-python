# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Loading of MetricSample and AggregatedMetricValue objects from protobuf messages."""

import warnings

from frequenz.api.common.v1alpha8.metrics import metrics_pb2
from typing_extensions import deprecated

from ....proto import datetime_from_proto
from ..._metric import Metric
from ..._sample import (
    AggregatedMetricValue,
    MetricConnection,
    MetricConnectionCategory,
    MetricSample,
)
from ._bounds import bounds_set_from_proto
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


def metric_connection_from_proto(
    message: metrics_pb2.MetricConnection,
) -> MetricConnection:
    """Convert a protobuf message to a [`MetricConnection`][....MetricConnection] object.

    An unspecified category is preserved as the raw integer `0` and an
    unrecognized one as its raw integer value in the `category` field (typed
    `MetricConnectionCategory | int`), so malformed input is surfaced through
    the returned type rather than a side channel.

    Args:
        message: The protobuf message to convert.

    Returns:
        The resulting [`MetricConnection`][....MetricConnection] object.
    """
    raw = message.category
    category: MetricConnectionCategory | int = (
        raw if raw == 0 else metric_connection_category_from_proto(raw)
    )

    return MetricConnection(
        category=category,
        name=message.name,
    )


def metric_sample_from_proto(
    message: metrics_pb2.MetricSample,
) -> MetricSample:
    """Convert a protobuf message to a [`MetricSample`][....MetricSample] object.

    Malformed or forward-incompatible input is surfaced through the returned
    type rather than a side channel: an unspecified metric is preserved as the
    raw integer `0` and an unrecognized one as its raw integer value in the
    `metric` field (typed `Metric | int`), and malformed bounds as an
    `InvalidBoundsSet` in `bounds_set`.

    Args:
        message: The protobuf message to convert.

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
            case None:
                # No metric_value_variant is set, so value stays None.
                pass

    bounds_set = bounds_set_from_proto(message.bounds)

    connection = None
    if message.HasField("connection"):
        connection = metric_connection_from_proto(message.connection)

    return MetricSample(
        sample_time=sample_time,
        metric=metric,
        value=value,
        bounds_set=bounds_set,
        connection=connection,
    )


@deprecated(
    "`metric_connection_from_proto_with_issues` is deprecated; use "
    "`metric_connection_from_proto` and inspect the returned type instead."
)
def metric_connection_from_proto_with_issues(
    message: metrics_pb2.MetricConnection,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> MetricConnection:
    """Convert a protobuf message to a [`MetricConnection`][....MetricConnection] object.

    Warning: Deprecated
        Use [`metric_connection_from_proto`][..metric_connection_from_proto]
        instead and inspect the returned type. The new converter encodes an
        unspecified or unrecognized category in the returned
        `MetricConnection.category` field (`MetricConnectionCategory | int`)
        rather than routing it through a side-channel string list.

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
        name=message.name,
    )


@deprecated(
    "`metric_sample_from_proto_with_issues` is deprecated; use "
    "`metric_sample_from_proto` and inspect the returned type instead."
)
def metric_sample_from_proto_with_issues(
    message: metrics_pb2.MetricSample,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> MetricSample:
    """Convert a protobuf message to a [`MetricSample`][....MetricSample] object.

    Warning: Deprecated
        Use [`metric_sample_from_proto`][..metric_sample_from_proto] instead
        and inspect the returned type. The new converter encodes an
        unspecified or unrecognized `metric` (`Metric | int`) and malformed
        bounds (`InvalidBoundsSet`) in the returned `MetricSample` rather than
        routing them through a side-channel string list.

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
            case None:
                # No metric_value_variant is set, so value stays None.
                pass

    bounds_set = bounds_set_from_proto(message.bounds)

    connection = None
    if message.HasField("connection"):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            connection = metric_connection_from_proto_with_issues(
                message.connection, major_issues=major_issues, minor_issues=minor_issues
            )

    return MetricSample(
        sample_time=sample_time,
        metric=metric,
        value=value,
        bounds_set=bounds_set,
        connection=connection,
    )
