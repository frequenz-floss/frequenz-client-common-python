# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for Metric to/from protobuf v1alpha8 conversion.

These tests ensure that, for this version, all enum members are correctly matched by
name and value between the Python `Metric` enum and the protobuf `Metric` enum.
"""

import pytest
from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from frequenz.client.common.metrics import Metric
from frequenz.client.common.metrics.proto.v1alpha8 import (
    metric_from_proto,
    metric_to_proto,
)

PB_NAMES: list[str] = [m.name for m in metrics_pb2.Metric.DESCRIPTOR.values]

UNKNOWN_PB_VALUE = metrics_pb2.Metric.ValueType(max(m.value for m in Metric) + 1)


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_proto_enum_matches_enum_name(pb_name: str) -> None:
    """Test that all known protobuf enum names have a matching Metric enum member."""
    pb_value = metrics_pb2.Metric.Value(pb_name)
    try:
        metric = Metric[pb_name.removeprefix("METRIC_")]
        assert metric.value == pb_value
    except KeyError:
        pass  # It is OK to have new protobuf enum values not yet in Metric.


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_proto_enum_matches_enum_value(pb_name: str) -> None:
    """Test that all known protobuf enum values have a matching Metric enum member."""
    pb_value = metrics_pb2.Metric.Value(pb_name)
    try:
        metric = Metric(pb_value)
        assert metric.value == pb_value
    except ValueError:
        pass  # It is OK to have new protobuf enum values not yet in Metric.


@pytest.mark.parametrize("metric", list(Metric), ids=lambda m: m.name)
def test_enum_matches_proto_enum_name(metric: Metric) -> None:
    """Test that all Metric enum members have a matching protobuf enum name."""
    pb_value = metrics_pb2.Metric.ValueType(metric.value)
    pb_name = metrics_pb2.Metric.Name(pb_value)
    assert pb_name == f"METRIC_{metric.name}"


@pytest.mark.parametrize("metric", list(Metric), ids=lambda m: m.name)
def test_enum_matches_proto_enum_value(metric: Metric) -> None:
    """Test that all Metric enum members have a matching protobuf enum value."""
    pb_value = metrics_pb2.Metric.Value(f"METRIC_{metric.name}")
    assert metric.value == pb_value


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_from_proto(pb_name: str) -> None:
    """Test conversion from protobuf returns a matching member or the int for unknown values."""
    pb_value = metrics_pb2.Metric.Value(pb_name)
    metric = metric_from_proto(pb_value)
    if pb_value in [m.value for m in Metric]:
        assert metric is Metric(pb_value)
    else:
        assert metric == pb_value


def test_from_proto_unknown() -> None:
    """Test conversion from protobuf for yet unknown values return the int."""
    metric = metric_from_proto(UNKNOWN_PB_VALUE)
    assert isinstance(metric, int)
    assert metric == UNKNOWN_PB_VALUE


@pytest.mark.parametrize("metric", list(Metric), ids=lambda m: m.name)
def test_to_proto(metric: Metric) -> None:
    """Test conversion to protobuf return a matching protobuf value."""
    pb_value = metric_to_proto(metric)
    assert pb_value == metric.value
