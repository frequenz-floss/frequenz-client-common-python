# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidLifetime`."""

from dataclasses import dataclass
from datetime import datetime, timezone

import pytest

from frequenz.client.common import InvalidDatetime
from frequenz.client.common.microgrid import InvalidLifetime


@dataclass(frozen=True, kw_only=True)
class _StrTestCase:
    """Test case for `InvalidLifetime.__str__`."""

    name: str
    """The description of the test case."""

    start_time: datetime | InvalidDatetime | None
    """The start time to use for the invalid lifetime."""

    end_time: datetime | InvalidDatetime | None
    """The end time to use for the invalid lifetime."""

    expected_str: str
    """The expected string representation."""


def test_accepts_invalid_range(present: datetime, future: datetime) -> None:
    """`InvalidLifetime` preserves an end time before its start time."""
    lifetime = InvalidLifetime(start_time=future, end_time=present)

    assert lifetime.start_time is future
    assert lifetime.end_time is present


def test_accepts_invalid_datetime(present: datetime) -> None:
    """`InvalidLifetime` preserves a timestamp with no `datetime` equivalent."""
    invalid = InvalidDatetime(seconds=253402300800, nanos=0)
    lifetime = InvalidLifetime(start_time=present, end_time=invalid)

    assert lifetime.start_time is present
    assert lifetime.end_time is invalid


@pytest.mark.parametrize(
    "case",
    [
        _StrTestCase(
            name="invalid_range",
            start_time=datetime(2025, 6, 1, 15, 30, 45, tzinfo=timezone.utc),
            end_time=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            expected_str=(
                "<invalid:(2025-06-01T15:30:45+00:00,2025-01-01T12:00:00+00:00]>"
            ),
        ),
        _StrTestCase(
            name="only_start",
            start_time=datetime(2025, 6, 1, 15, 30, 45, tzinfo=timezone.utc),
            end_time=None,
            expected_str="<invalid:(2025-06-01T15:30:45+00:00,+inf]>",
        ),
        _StrTestCase(
            name="only_end",
            start_time=None,
            end_time=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            expected_str="<invalid:(-inf,2025-01-01T12:00:00+00:00]>",
        ),
        _StrTestCase(
            name="unbounded",
            start_time=None,
            end_time=None,
            expected_str="<invalid:(-inf,+inf]>",
        ),
        _StrTestCase(
            name="unrepresentable_start",
            start_time=InvalidDatetime(seconds=253402300800, nanos=0),
            end_time=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            expected_str=(
                "<invalid:(<invalid:253402300800s+0ns>,2025-01-01T12:00:00+00:00]>"
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_str(case: _StrTestCase) -> None:
    """`InvalidLifetime.__str__` wraps timestamps in the `<invalid:...>` marker."""
    lifetime = InvalidLifetime(start_time=case.start_time, end_time=case.end_time)
    assert str(lifetime) == case.expected_str
