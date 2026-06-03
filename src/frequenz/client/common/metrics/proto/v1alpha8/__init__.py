# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of metrics enums from/to protobuf v1alpha8."""

from ._bounds import bounds_from_proto, bounds_from_proto_with_issues
from ._metric import metric_from_proto, metric_to_proto
from ._metric_connection_category import (
    metric_connection_category_from_proto,
    metric_connection_category_to_proto,
)
from ._sample import (
    aggregated_metric_sample_from_proto,
    metric_connection_from_proto_with_issues,
    metric_sample_from_proto_with_issues,
)

__all__ = [
    "aggregated_metric_sample_from_proto",
    "bounds_from_proto",
    "bounds_from_proto_with_issues",
    "metric_connection_category_from_proto",
    "metric_connection_category_to_proto",
    "metric_connection_from_proto_with_issues",
    "metric_from_proto",
    "metric_sample_from_proto_with_issues",
    "metric_to_proto",
]
