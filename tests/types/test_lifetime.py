# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Lifetime class."""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum, auto

import pytest

from frequenz.client.common.types import Lifetime


class _Time(Enum):
    """Types of time points used in tests."""

    PAST = auto()
    """A time point in the past."""

    PRESENT = auto()
    """The current time point."""

    FUTURE = auto()
    """A time point in the future."""


@dataclass(frozen=True, kw_only=True)
class _LifetimeTestCase:
    """Test case for Lifetime creation and validation."""

    name: str
    """The description of the test case."""

    include_start: bool
    """Whether to include start time."""

    include_end: bool
    """Whether to include end time."""

    expected_start: bool
    """Whether start should be set."""

    expected_end: bool
    """Whether end should be set."""

    expected_operational: bool
    """The expected operational state."""


@dataclass(frozen=True, kw_only=True)
class _ActivityTestCase:
    """Test case for Lifetime activity state."""

    name: str
    """The description of the test case."""

    start_type: _Time | None
    """The type of start time."""

    end_type: _Time | None
    """The type of end time."""

    expected_operational: bool
    """The expected operational state."""


@dataclass(frozen=True, kw_only=True)
class _FixedLifetimeTestCase:
    """Test case for fixed lifetime activity testing."""

    name: str
    """The description of the test case."""

    test_time: _Time
    """The type of time point to test."""

    expected_operational: bool
    """The expected operational state."""


@pytest.fixture
def present() -> datetime:
    """Fixture to provide current UTC time."""
    return datetime.now(timezone.utc)


@pytest.fixture
def past(present: datetime) -> datetime:
    """Fixture to provide a past time."""
    return present.replace(year=present.year - 1)


@pytest.fixture
def future(present: datetime) -> datetime:
    """Fixture to provide a future time."""
    return present.replace(year=present.year + 1)


@pytest.mark.parametrize(
    "case",
    [
        _LifetimeTestCase(
            name="full",
            include_start=True,
            include_end=True,
            expected_start=True,
            expected_end=True,
            expected_operational=True,
        ),
        _LifetimeTestCase(
            name="only_start",
            include_start=True,
            include_end=False,
            expected_start=True,
            expected_end=False,
            expected_operational=True,
        ),
        _LifetimeTestCase(
            name="only_end",
            include_start=False,
            include_end=True,
            expected_start=False,
            expected_end=True,
            expected_operational=True,
        ),
        _LifetimeTestCase(
            name="no_dates",
            include_start=False,
            include_end=False,
            expected_start=False,
            expected_end=False,
            expected_operational=True,
        ),
    ],
    ids=lambda case: case.name,
)
def test_creation(present: datetime, future: datetime, case: _LifetimeTestCase) -> None:
    """Test creating Lifetime instances with various parameters."""
    lifetime = Lifetime(
        start_time=present if case.include_start else None,
        end_time=future if case.include_end else None,
    )
    assert (lifetime.start_time is not None) == case.expected_start
    if case.expected_start:
        assert lifetime.start_time == present
    assert (lifetime.end_time is not None) == case.expected_end
    if case.expected_end:
        assert lifetime.end_time == future
    assert lifetime.is_operational_now() == case.expected_operational


@pytest.mark.parametrize("start", [None, *_Time], ids=lambda x: f"start_{x}")
@pytest.mark.parametrize("end", [None, *_Time], ids=lambda x: f"end_{x}")
def test_validation(
    past: datetime,
    present: datetime,
    future: datetime,
    start: _Time | None,
    end: _Time | None,
) -> None:
    """Test validation of Lifetime parameters."""
    time_map = {
        _Time.PAST: past,
        _Time.PRESENT: present,
        _Time.FUTURE: future,
        None: None,
    }

    start_time = time_map[start]
    end_time = time_map[end]

    # Invalid combinations are when end is before start
    should_fail = (
        start is not None
        and end is not None
        and (
            (start == _Time.PRESENT and end == _Time.PAST)
            or (start == _Time.FUTURE and end == _Time.PAST)
            or (start == _Time.FUTURE and end == _Time.PRESENT)
        )
    )

    if should_fail:
        with pytest.raises(
            ValueError, match=r"Start \(.*\) must be before or equal to end \(.*\)"
        ):
            Lifetime(start_time=start_time, end_time=end_time)
    else:
        lifetime = Lifetime(start_time=start_time, end_time=end_time)
        # Verify the timestamps are set correctly
        assert lifetime.start_time == start_time
        assert lifetime.end_time == end_time


def test_equal_start_and_end_is_valid(present: datetime) -> None:
    """Test that a Lifetime with the same start and end time is valid."""
    lifetime = Lifetime(start_time=present, end_time=present)

    assert lifetime.start_time == present
    assert lifetime.end_time == present
    assert lifetime.is_operational_at(present)


def test_equality_and_hashing(present: datetime, future: datetime) -> None:
    """Test that Lifetime objects support equality and hashing."""
    lifetime1 = Lifetime(start_time=present, end_time=future)
    lifetime2 = Lifetime(start_time=present, end_time=future)
    lifetime3 = Lifetime(start_time=present, end_time=None)

    assert lifetime1 == lifetime2
    assert lifetime1 != lifetime3
    assert {lifetime1, lifetime2, lifetime3} == {lifetime1, lifetime3}


@pytest.mark.parametrize(
    "case",
    [
        _ActivityTestCase(
            name="past_start-no_end",
            start_type=_Time.PAST,
            end_type=None,
            expected_operational=True,
        ),
        _ActivityTestCase(
            name="past_start-future_end",
            start_type=_Time.PAST,
            end_type=_Time.FUTURE,
            expected_operational=True,
        ),
        _ActivityTestCase(
            name="future_start-no_end",
            start_type=_Time.FUTURE,
            end_type=None,
            expected_operational=False,
        ),
        _ActivityTestCase(
            name="past_start-past_end",
            start_type=_Time.PAST,
            end_type=_Time.PAST,
            expected_operational=False,
        ),
        _ActivityTestCase(
            name="now_start-no_end",
            start_type=_Time.PRESENT,
            end_type=None,
            expected_operational=True,
        ),
        _ActivityTestCase(
            name="no_start-now_end",
            start_type=None,
            end_type=_Time.PRESENT,
            expected_operational=True,
        ),
        _ActivityTestCase(
            name="now_start-now_end",
            start_type=_Time.PRESENT,
            end_type=_Time.PRESENT,
            expected_operational=True,
        ),
        _ActivityTestCase(
            name="no_start-past_end",
            start_type=None,
            end_type=_Time.PAST,
            expected_operational=False,
        ),
    ],
    ids=lambda case: case.name,
)
def test_active_property(
    past: datetime, future: datetime, present: datetime, case: _ActivityTestCase
) -> None:
    """Test the active property of Lifetime."""
    start_time = {
        _Time.PAST: past,
        _Time.FUTURE: future,
        _Time.PRESENT: present,
        None: None,
    }[case.start_type]

    end_time = {
        _Time.PAST: past,
        _Time.FUTURE: future,
        _Time.PRESENT: present,
        None: None,
    }[case.end_type]

    lifetime = Lifetime(start_time=start_time, end_time=end_time)
    assert lifetime.is_operational_at(present) == case.expected_operational


@pytest.mark.parametrize(
    "case",
    [
        _FixedLifetimeTestCase(
            name="past", test_time=_Time.PAST, expected_operational=True
        ),
        _FixedLifetimeTestCase(
            name="present", test_time=_Time.PRESENT, expected_operational=True
        ),
        _FixedLifetimeTestCase(
            name="future", test_time=_Time.FUTURE, expected_operational=True
        ),
    ],
    ids=lambda case: case.name,
)
def test_active_at_with_fixed_lifetime(
    past: datetime,
    future: datetime,
    present: datetime,
    case: _FixedLifetimeTestCase,
) -> None:
    """Test active_at with different timestamps for a fixed lifetime period."""
    lifetime = Lifetime(start_time=past, end_time=future)
    test_time = {
        _Time.PAST: past,
        _Time.PRESENT: present,
        _Time.FUTURE: future,
    }[case.test_time]

    assert lifetime.is_operational_at(test_time) == case.expected_operational
