# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for MetricSample class."""

from datetime import datetime, timezone

import pytest

from frequenz.client.common import UnrecognizedValueError, UnspecifiedValueError
from frequenz.client.common.metrics import (
    AggregatedMetricValue,
    AggregationMethod,
    Bounds,
    Metric,
    MetricConnection,
    MetricSample,
)


@pytest.fixture
def now() -> datetime:
    """Get the current time."""
    return datetime.now(timezone.utc)


@pytest.mark.parametrize(
    "value,connection",
    [
        pytest.param(
            5.0,
            None,
            id="simple_value",
        ),
        pytest.param(
            AggregatedMetricValue(
                avg=5.0,
                min=1.0,
                max=10.0,
                raw=[1.0, 5.0, 10.0],
            ),
            "dc_battery_0",
            id="aggregated_value",
        ),
        pytest.param(
            None,
            None,
            id="none_value",
        ),
    ],
)
def test_creation(
    now: datetime,
    value: float | AggregatedMetricValue | None,
    connection: MetricConnection | None,
) -> None:
    """Test MetricSample creation with different value types."""
    bounds = [Bounds(lower=-10.0, upper=10.0)]
    sample = MetricSample(
        sample_time=now,
        metric=Metric.AC_POWER_ACTIVE,
        value=value,
        bounds=bounds,
        connection=connection,
    )
    assert sample.sample_time == now
    assert sample.metric == Metric.AC_POWER_ACTIVE
    assert sample.value == value
    assert sample.bounds == bounds
    assert sample.connection == connection


@pytest.mark.parametrize(
    "value, method_results",
    [
        pytest.param(
            5.0,
            {
                AggregationMethod.AVG: 5.0,
                AggregationMethod.MIN: 5.0,
                AggregationMethod.MAX: 5.0,
            },
            id="simple_value",
        ),
        pytest.param(
            AggregatedMetricValue(
                avg=5.0,
                min=1.0,
                max=10.0,
                raw=[1.0, 5.0, 10.0],
            ),
            {
                AggregationMethod.AVG: 5.0,
                AggregationMethod.MIN: 1.0,
                AggregationMethod.MAX: 10.0,
            },
            id="aggregated_value",
        ),
        pytest.param(
            None,
            {
                AggregationMethod.AVG: None,
                AggregationMethod.MIN: None,
                AggregationMethod.MAX: None,
            },
            id="none_value",
        ),
    ],
)
def test_as_single_value(
    now: datetime,
    value: float | AggregatedMetricValue | None,
    method_results: dict[AggregationMethod, float | None],
) -> None:
    """Test MetricSample.as_single_value with different value types and methods."""
    bounds = [Bounds(lower=-10.0, upper=10.0)]

    sample = MetricSample(
        sample_time=now,
        metric=Metric.AC_POWER_ACTIVE,
        value=value,
        bounds=bounds,
    )

    for method, expected in method_results.items():
        assert sample.as_single_value(aggregation_method=method) == expected


def test_multiple_bounds(now: datetime) -> None:
    """Test MetricSample creation with multiple bounds."""
    bounds = [
        Bounds(lower=-10.0, upper=-5.0),
        Bounds(lower=5.0, upper=10.0),
    ]
    sample = MetricSample(
        sample_time=now,
        metric=Metric.AC_POWER_ACTIVE,
        value=7.0,
        bounds=bounds,
    )
    assert sample.bounds == bounds


def test_get_metric_returns_known_member(now: datetime) -> None:
    """get_metric returns the metric when it is a known member."""
    sample = MetricSample(
        sample_time=now, metric=Metric.AC_POWER_ACTIVE, value=None, bounds=[]
    )
    assert sample.get_metric() is Metric.AC_POWER_ACTIVE


def test_get_metric_unspecified_int_raises(now: datetime) -> None:
    """get_metric raises UnspecifiedValueError for the raw int 0."""
    sample = MetricSample(sample_time=now, metric=0, value=None, bounds=[])
    with pytest.raises(UnspecifiedValueError):
        sample.get_metric()


def test_get_metric_unspecified_member_raises(now: datetime) -> None:
    """get_metric raises UnspecifiedValueError for the value-0 member."""
    with pytest.deprecated_call():
        sample = MetricSample(
            sample_time=now, metric=Metric.UNSPECIFIED, value=None, bounds=[]
        )
    with pytest.raises(UnspecifiedValueError):
        sample.get_metric()


def test_get_metric_unrecognized_int_raises(now: datetime) -> None:
    """get_metric raises UnrecognizedValueError carrying the raw int value."""
    sample = MetricSample(sample_time=now, metric=99999, value=None, bounds=[])
    with pytest.raises(UnrecognizedValueError) as exc_info:
        sample.get_metric()
    assert exc_info.value.value == 99999
