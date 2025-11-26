# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Metrics objects to proto conversion functions."""

from ._bounds import bounds_from_proto, bounds_from_proto_with_issues
from ._sample import (
    aggregated_metric_sample_from_proto,
    metric_connection_from_proto_with_issues,
    metric_sample_from_proto_with_issues,
)

__all__ = [
    "aggregated_metric_sample_from_proto",
    "bounds_from_proto",
    "bounds_from_proto_with_issues",
    "metric_connection_from_proto_with_issues",
    "metric_sample_from_proto_with_issues",
]
