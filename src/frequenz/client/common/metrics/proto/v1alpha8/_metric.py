# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Coversion of Metric to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from ....proto import enum_from_proto
from ..._metric import Metric


def metric_from_proto(message: metrics_pb2.Metric.ValueType) -> Metric | int:
    """Convert a protobuf Metric message to a Metric enum member.

    Args:
        message: A protobuf Metric message.

    Returns:
        The corresponding Metric enum member.
    """
    return enum_from_proto(message, Metric)


def metric_to_proto(metric: Metric) -> metrics_pb2.Metric.ValueType:
    """Convert a Metric enum member to a protobuf Metric message.

    Args:
        metric: A Metric enum member.

    Returns:
        The corresponding protobuf Metric message.
    """
    return metrics_pb2.Metric.ValueType(metric.value)
