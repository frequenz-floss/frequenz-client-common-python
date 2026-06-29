# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of MetricConnectionCategory to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from ....proto import enum_from_proto
from ..._sample import MetricConnectionCategory


def metric_connection_category_from_proto(
    message: metrics_pb2.MetricConnectionCategory.ValueType,
) -> MetricConnectionCategory | int:
    """Convert a protobuf `MetricConnectionCategory` value to an enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding MetricConnectionCategory enum member, or the raw `int` if
            the protobuf value is not recognized.
    """
    return enum_from_proto(message, MetricConnectionCategory)


def metric_connection_category_to_proto(
    category: MetricConnectionCategory,
) -> metrics_pb2.MetricConnectionCategory.ValueType:
    """Convert a `MetricConnectionCategory` enum member to a protobuf value.

    Args:
        category: A MetricConnectionCategory enum member.

    Returns:
        The corresponding protobuf `MetricConnectionCategory` value.
    """
    return metrics_pb2.MetricConnectionCategory.ValueType(category.value)
