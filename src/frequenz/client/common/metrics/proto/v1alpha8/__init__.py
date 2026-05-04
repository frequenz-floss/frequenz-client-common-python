# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of Metric from/to protobuf v1alpha8."""

from ._metric import metric_from_proto, metric_to_proto

__all__ = [
    "metric_from_proto",
    "metric_to_proto",
]
