# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of metrics enums from/to protobuf v1alpha8."""

from ._metric import metric_from_proto, metric_to_proto
from ._metric_connection_category import (
    metric_connection_category_from_proto,
    metric_connection_category_to_proto,
)

__all__ = [
    "metric_connection_category_from_proto",
    "metric_connection_category_to_proto",
    "metric_from_proto",
    "metric_to_proto",
]
