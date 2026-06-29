# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of Metric to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from ....proto import enum_from_proto
from ..._metric import Metric


def metric_from_proto(message: metrics_pb2.Metric.ValueType) -> Metric | int:
    """Convert a protobuf `Metric` message to a [`Metric`][....Metric] enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`Metric`][....Metric] enum member, or the raw [`int`][]
            if the protobuf value is not recognized.
    """
    return enum_from_proto(message, Metric)


def metric_to_proto(metric: Metric) -> metrics_pb2.Metric.ValueType:
    """Convert a [`Metric`][....Metric] enum member to a protobuf `Metric` value.

    Args:
        metric: The enum member to convert.

    Returns:
        The corresponding protobuf `Metric` value.
    """
    return metrics_pb2.Metric.ValueType(metric.value)
