# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for AggregatedMetricValue class."""

import pytest

from frequenz.client.common import FloatInt
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
        pytest.param(
            5,
            1,
            10,
            [1, 5.0, 10],
            "avg:5<min:1 max:10 num_raw:3>",
            id="int_data",
        ),
    ],
)
def test_creation_and_str(
    avg: FloatInt,
    min_val: FloatInt | None,
    max_val: FloatInt | None,
    raw: list[FloatInt],
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
