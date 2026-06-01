# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for MetricConnectionCategory to/from protobuf v1alpha8 conversion."""

from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from frequenz.client.common.metrics import MetricConnectionCategory
from frequenz.client.common.metrics.proto.v1alpha8 import (
    metric_connection_category_from_proto,
    metric_connection_category_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestMetricConnectionCategoryParity(EnumParityTest):
    """Parity tests for the `MetricConnectionCategory` enum."""

    python_enum = MetricConnectionCategory
    proto_enum = metrics_pb2.MetricConnectionCategory
    name_prefix = "METRIC_CONNECTION_CATEGORY_"
    from_proto = staticmethod(metric_connection_category_from_proto)
    to_proto = staticmethod(metric_connection_category_to_proto)
