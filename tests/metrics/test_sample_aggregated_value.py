# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for AggregatedMetricValue class."""

import pytest

from frequenz.client.common.metrics import AggregatedMetricValue


@pytest.mark.parametrize(
    "avg, min_val, max_val, raw, expected_str",
    [
        pytest.param(
            5.0,
            1.0,
            10.0,
            [1.0, 5.0, 10.0],
            "avg:5.0<min:1.0 max:10.0 num_raw:3>",
            id="full_data",
        ),
        pytest.param(
            5.0,
            None,
            None,
            [],
            "avg:5.0",
            id="minimal_data",
        ),
    ],
)
def test_creation_and_str(
    avg: float,
    min_val: float | None,
    max_val: float | None,
    raw: list[float],
    expected_str: str,
) -> None:
    """Test AggregatedMetricValue creation and string representation."""
    value = AggregatedMetricValue(
        avg=avg,
        min=min_val,
        max=max_val,
        raw=raw,
    )
    assert value.avg == avg
    assert value.min == min_val
    assert value.max == max_val
    assert list(value.raw) == raw
    assert str(value) == expected_str
