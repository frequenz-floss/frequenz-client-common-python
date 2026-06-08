# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for AggregatedMetricValue protobuf conversion."""

from dataclasses import dataclass, field

import pytest
from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from frequenz.client.common.metrics.proto.v1alpha8 import (
    aggregated_metric_sample_from_proto,
)


@dataclass(frozen=True, kw_only=True)
class _TestCase:
    """Test case for AggregatedMetricValue protobuf conversion."""

    name: str
    """The description of the test case."""

    avg_value: float
    """The average value to set."""

    has_min: bool = True
    """Whether to include min value."""

    has_max: bool = True
    """Whether to include max value."""

    min_value: float | None = None
    """The minimum value to set."""

    max_value: float | None = None
    """The maximum value to set."""

    raw: list[float] = field(default_factory=list)
    """The raw values to include."""


@pytest.mark.parametrize(
    "case",
    [
        _TestCase(
            name="full",
            avg_value=5.0,
            min_value=1.0,
            max_value=10.0,
            raw=[1.0, 5.0, 10.0],
        ),
        _TestCase(
            name="minimal",
            avg_value=5.0,
            has_min=False,
            has_max=False,
        ),
        _TestCase(
            name="only_min",
            avg_value=5.0,
            has_max=False,
            min_value=1.0,
        ),
        _TestCase(
            name="only_max",
            avg_value=5.0,
            has_min=False,
            max_value=10.0,
        ),
    ],
    ids=lambda case: case.name,
)
def test_from_proto(case: _TestCase) -> None:
    """Test conversion from protobuf message to AggregatedMetricValue."""
    proto = metrics_pb2.AggregatedMetricValue(
        avg_value=case.avg_value,
    )
    if case.has_min and case.min_value is not None:
        proto.min_value = case.min_value
    if case.has_max and case.max_value is not None:
        proto.max_value = case.max_value
    if case.raw:
        proto.raw_values.extend(case.raw)

    value = aggregated_metric_sample_from_proto(proto)

    assert value.avg == case.avg_value
    assert value.min == (case.min_value if case.has_min else None)
    assert value.max == (case.max_value if case.has_max else None)
    assert list(value.raw) == case.raw
