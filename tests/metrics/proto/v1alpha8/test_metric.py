# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for Metric to/from protobuf v1alpha8 conversion."""

from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from frequenz.client.common.metrics import Metric
from frequenz.client.common.metrics.proto.v1alpha8 import (
    metric_from_proto,
    metric_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestMetricParity(EnumParityTest):
    """Parity tests for the `Metric` enum."""

    python_enum = Metric
    proto_enum = metrics_pb2.Metric
    name_prefix = "METRIC_"
    from_proto = staticmethod(metric_from_proto)
    to_proto = staticmethod(metric_to_proto)
