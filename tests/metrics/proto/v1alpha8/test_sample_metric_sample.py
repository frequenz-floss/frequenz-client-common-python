# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for MetricSample protobuf conversion."""

import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Final

import pytest
from frequenz.api.common.v1alpha8.metrics import bounds_pb2, metrics_pb2
from google.protobuf.timestamp_pb2 import Timestamp

from frequenz.client.common.metrics import (
    AggregatedMetricValue,
    Bounds,
    Metric,
    MetricConnection,
    MetricConnectionCategory,
    MetricSample,
)
from frequenz.client.common.metrics.proto.v1alpha8 import (
    metric_connection_category_to_proto,
    metric_sample_from_proto_with_issues,
    metric_to_proto,
)

DATETIME: Final[datetime] = datetime(2023, 3, 15, 12, 0, 0, tzinfo=timezone.utc)
TIMESTAMP: Final[Timestamp] = Timestamp(seconds=int(DATETIME.timestamp()))


@dataclass(frozen=True, kw_only=True)
class _TestCase:
    """Test case for MetricSample protobuf conversion."""

    name: str
    """The description of the test case."""

    proto_message: metrics_pb2.MetricSample
    """The input protobuf message."""

    expected_sample: MetricSample
    """The expected MetricSample object."""

    expected_major_issues: list[str] = field(default_factory=list)
    """Expected major issues during conversion."""

    expected_minor_issues: list[str] = field(default_factory=list)
    """Expected minor issues during conversion."""


@pytest.mark.parametrize(
    "case",
    [
        _TestCase(
            name="simple_value",
            proto_message=metrics_pb2.MetricSample(
                sample_time=TIMESTAMP,
                metric=metric_to_proto(Metric.AC_POWER_ACTIVE),
                value=metrics_pb2.MetricValueVariant(
                    simple_metric=metrics_pb2.SimpleMetricValue(value=5.0)
                ),
            ),
            expected_sample=MetricSample(
                sample_time=DATETIME,
                metric=Metric.AC_POWER_ACTIVE,
                value=5.0,
                bounds=[],
                connection=None,
            ),
        ),
        _TestCase(
            name="aggregated_value",
            proto_message=metrics_pb2.MetricSample(
                sample_time=TIMESTAMP,
                metric=metric_to_proto(Metric.AC_POWER_ACTIVE),
                value=metrics_pb2.MetricValueVariant(
                    aggregated_metric=metrics_pb2.AggregatedMetricValue(
                        avg_value=5.0, min_value=1.0, max_value=10.0
                    )
                ),
            ),
            expected_sample=MetricSample(
                sample_time=DATETIME,
                metric=Metric.AC_POWER_ACTIVE,
                value=AggregatedMetricValue(avg=5.0, min=1.0, max=10.0, raw=[]),
                bounds=[],
                connection=None,
            ),
        ),
        _TestCase(
            name="no_value",
            proto_message=metrics_pb2.MetricSample(
                sample_time=TIMESTAMP,
                metric=metric_to_proto(Metric.AC_POWER_ACTIVE),
            ),
            expected_sample=MetricSample(
                sample_time=DATETIME,
                metric=Metric.AC_POWER_ACTIVE,
                value=None,
                bounds=[],
                connection=None,
            ),
        ),
        _TestCase(
            name="unrecognized_metric",
            proto_message=metrics_pb2.MetricSample(
                sample_time=TIMESTAMP,
                metric=999,  # type: ignore[arg-type]
                value=metrics_pb2.MetricValueVariant(
                    simple_metric=metrics_pb2.SimpleMetricValue(value=5.0)
                ),
            ),
            expected_sample=MetricSample(
                sample_time=DATETIME, metric=999, value=5.0, bounds=[], connection=None
            ),
        ),
        _TestCase(
            name="with_valid_bounds",
            proto_message=metrics_pb2.MetricSample(
                sample_time=TIMESTAMP,
                metric=metric_to_proto(Metric.AC_POWER_ACTIVE),
                value=metrics_pb2.MetricValueVariant(
                    simple_metric=metrics_pb2.SimpleMetricValue(value=5.0)
                ),
                bounds=[bounds_pb2.Bounds(lower=-10.0, upper=10.0)],
            ),
            expected_sample=MetricSample(
                sample_time=DATETIME,
                metric=Metric.AC_POWER_ACTIVE,
                value=5.0,
                bounds=[Bounds(lower=-10.0, upper=10.0)],
                connection=None,
            ),
        ),
        _TestCase(
            name="with_invalid_bounds",
            proto_message=metrics_pb2.MetricSample(
                sample_time=TIMESTAMP,
                metric=metric_to_proto(Metric.AC_POWER_ACTIVE),
                value=metrics_pb2.MetricValueVariant(
                    simple_metric=metrics_pb2.SimpleMetricValue(value=5.0)
                ),
                bounds=[
                    bounds_pb2.Bounds(lower=-10.0, upper=10.0),
                    bounds_pb2.Bounds(lower=10.0, upper=-10.0),  # Invalid
                ],
            ),
            expected_sample=MetricSample(
                sample_time=DATETIME,
                metric=Metric.AC_POWER_ACTIVE,
                value=5.0,
                bounds=[Bounds(lower=-10.0, upper=10.0)],  # Invalid bounds are ignored
                connection=None,
            ),
            expected_major_issues=[
                (
                    "bounds for AC_POWER_ACTIVE is invalid (Lower bound (10.0) must be "
                    "less than or equal to upper bound (-10.0)), ignoring these bounds"
                )
            ],
        ),
        _TestCase(
            name="with_connection",
            proto_message=metrics_pb2.MetricSample(
                sample_time=TIMESTAMP,
                metric=metric_to_proto(Metric.AC_POWER_ACTIVE),
                value=metrics_pb2.MetricValueVariant(
                    simple_metric=metrics_pb2.SimpleMetricValue(value=5.0)
                ),
                connection=metrics_pb2.MetricConnection(
                    category=metric_connection_category_to_proto(
                        MetricConnectionCategory.BATTERY
                    ),
                    name="dc_battery_0",
                ),
            ),
            expected_sample=MetricSample(
                sample_time=DATETIME,
                metric=Metric.AC_POWER_ACTIVE,
                value=5.0,
                bounds=[],
                connection=MetricConnection(
                    category=MetricConnectionCategory.BATTERY, name="dc_battery_0"
                ),
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_from_proto_with_issues(case: _TestCase) -> None:
    """Test conversion from protobuf message to MetricSample."""
    major_issues: list[str] = []
    minor_issues: list[str] = []

    # The timestamp in the expected sample needs to match the one from proto conversion
    # We use a fixed timestamp in test cases, so this is fine.
    # If dynamic timestamps were used, we'd need to adjust here or in the fixture.

    sample = metric_sample_from_proto_with_issues(
        case.proto_message,
        major_issues=major_issues,
        minor_issues=minor_issues,
    )

    assert sample == case.expected_sample
    assert major_issues == case.expected_major_issues
    assert minor_issues == case.expected_minor_issues


def test_with_unspecified_metric() -> None:
    """Test an unspecified metric is stored as int 0 without warning.

    The dataclass-level converter stores the raw int ``0`` for an unspecified
    metric (never the deprecated member) and emits no ``DeprecationWarning``.
    """
    proto = metrics_pb2.MetricSample(
        sample_time=TIMESTAMP,
        metric=metrics_pb2.Metric.METRIC_UNSPECIFIED,
        value=metrics_pb2.MetricValueVariant(
            simple_metric=metrics_pb2.SimpleMetricValue(value=5.0)
        ),
    )

    major_issues: list[str] = []
    minor_issues: list[str] = []

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        sample = metric_sample_from_proto_with_issues(
            proto, major_issues=major_issues, minor_issues=minor_issues
        )

    assert sample.metric == 0
    assert not isinstance(sample.metric, Metric)
    assert not major_issues
    assert not minor_issues
