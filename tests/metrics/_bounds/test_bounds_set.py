# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `BoundsSet`."""

import math

import pytest

from frequenz.client.common import FloatInt
from frequenz.client.common.metrics import Bounds, BoundsSet


def test_empty() -> None:
    """The empty set is the unbounded set: falsy and contains everything."""
    empty = BoundsSet()
    assert not empty.bounds
    assert not empty
    assert not empty.is_bounded()
    assert 0.0 in empty
    assert 1e9 in empty
    assert -1e9 in empty
    assert None not in empty
    assert str(empty) == "[None,None]"


def test_default_is_empty() -> None:
    """`BoundsSet()` and `BoundsSet(bounds=())` are equal empty sets."""
    assert BoundsSet() == BoundsSet(bounds=())


def test_positional_collection_construction() -> None:
    """`BoundsSet` accepts any positional collection of bounds."""
    from_list = BoundsSet([Bounds(lower=1.0, upper=5.0)])
    assert from_list.bounds == (Bounds(lower=1.0, upper=5.0),)
    assert 3.0 in from_list
    assert from_list == BoundsSet((Bounds(lower=1.0, upper=5.0),))
    assert from_list == BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0),))


def test_iter_construction() -> None:
    """An iterator is accepted and normalized."""
    from_set = BoundsSet(
        b for b in (Bounds(lower=1.0, upper=5.0), Bounds(lower=3.0, upper=10.0))
    )
    assert from_set.bounds == (Bounds(lower=1.0, upper=10.0),)


def test_positional_empty_collection_is_unbounded() -> None:
    """A positional empty collection is the empty (unbounded) set."""
    assert BoundsSet([]) == BoundsSet()
    assert not BoundsSet([]).bounds


def test_single() -> None:
    """A single bound is kept as-is and is bounded."""
    single = BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0),))
    assert single.bounds == (Bounds(lower=1.0, upper=5.0),)
    assert single
    assert single.is_bounded()


def test_disjoint_kept_sorted() -> None:
    """Non-overlapping bounds are kept as separate, sorted members."""
    result = BoundsSet(
        bounds=(Bounds(lower=15.0, upper=20.0), Bounds(lower=1.0, upper=5.0))
    )
    assert result.bounds == (
        Bounds(lower=1.0, upper=5.0),
        Bounds(lower=15.0, upper=20.0),
    )


def test_overlapping_merged() -> None:
    """Overlapping bounds are merged into one."""
    result = BoundsSet(
        bounds=(Bounds(lower=1.0, upper=5.0), Bounds(lower=3.0, upper=10.0))
    )
    assert result.bounds == (Bounds(lower=1.0, upper=10.0),)


def test_touching_merged() -> None:
    """Bounds sharing an endpoint touch (inclusive) and merge."""
    result = BoundsSet(
        bounds=(Bounds(lower=1.0, upper=5.0), Bounds(lower=5.0, upper=10.0))
    )
    assert result.bounds == (Bounds(lower=1.0, upper=10.0),)


def test_gap_not_merged() -> None:
    """Bounds separated by a gap are not merged."""
    result = BoundsSet(
        bounds=(Bounds(lower=1.0, upper=4.0), Bounds(lower=5.0, upper=10.0))
    )
    assert result.bounds == (
        Bounds(lower=1.0, upper=4.0),
        Bounds(lower=5.0, upper=10.0),
    )


def test_containment_merged() -> None:
    """A bound contained in another is absorbed."""
    result = BoundsSet(
        bounds=(Bounds(lower=1.0, upper=10.0), Bounds(lower=3.0, upper=5.0))
    )
    assert result.bounds == (Bounds(lower=1.0, upper=10.0),)


def test_duplicate_merged() -> None:
    """Duplicate bounds collapse to a single member."""
    result = BoundsSet(
        bounds=(Bounds(lower=1.0, upper=5.0), Bounds(lower=1.0, upper=5.0))
    )
    assert result.bounds == (Bounds(lower=1.0, upper=5.0),)


def test_unbounded_below_merge() -> None:
    """A `None` lower bound is treated as -inf when merging."""
    result = BoundsSet(
        bounds=(Bounds(lower=None, upper=5.0), Bounds(lower=3.0, upper=8.0))
    )
    assert result.bounds == (Bounds(lower=None, upper=8.0),)


def test_all_covering_single_collapses_to_empty() -> None:
    """An explicit fully-unbounded bound collapses to the empty set."""
    result = BoundsSet(bounds=(Bounds(lower=None, upper=None),))
    assert not result.bounds
    assert not result


def test_all_covering_halves_collapse_to_empty() -> None:
    """Two half-bounds that together cover the space collapse to the empty set."""
    result = BoundsSet(
        bounds=(Bounds(lower=None, upper=5.0), Bounds(lower=3.0, upper=None))
    )
    assert not result.bounds
    assert not result
    assert 42.0 in result  # unbounded -> contains everything


@pytest.mark.parametrize(
    "item, expected",
    [
        (0.0, False),
        (1.0, True),  # lower bound is inclusive
        (5.0, True),  # upper bound is inclusive
        (3.0, True),
        (6.0, False),  # in the gap between the two bounds
        (15.0, True),
        (20.0, True),
        (21.0, False),
        (3, True),  # `int` items work the same
        (6, False),
    ],
)
def test_contains(item: FloatInt, expected: bool) -> None:
    """Membership tests the union of all bounds, inclusive on both ends."""
    bounds_set = BoundsSet(
        bounds=(Bounds(lower=1.0, upper=5.0), Bounds(lower=15.0, upper=20.0))
    )
    assert (item in bounds_set) is expected


def test_contains_none() -> None:
    """`None` is never contained, not even by the unbounded set."""
    assert None not in BoundsSet()
    assert None not in BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0),))


def test_contains_nan() -> None:
    """`NaN` is never contained, not even by the unbounded set."""
    assert math.nan not in BoundsSet()
    assert math.nan not in BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0),))


def test_contains_large_int() -> None:
    """Integers too large to convert to `float` are tested without overflowing."""
    huge = 10**1000
    assert huge in BoundsSet()  # unbounded set contains everything
    assert -huge in BoundsSet()
    bounded = BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0),))
    assert huge not in bounded
    assert -huge not in bounded


def test_infinite_bounds_collapse_to_empty() -> None:
    """An explicit `[-inf, +inf]` bound collapses to the empty (unbounded) set."""
    result = BoundsSet(bounds=(Bounds(lower=-math.inf, upper=math.inf),))
    assert not result.bounds
    assert not result
    assert result == BoundsSet()
    assert 42.0 in result


def test_contains_infinity_value() -> None:
    """`inf`/`-inf` as a *value* stay testable; only endpoints normalize to `None`."""
    assert math.inf in BoundsSet()
    assert -math.inf in BoundsSet()
    bounded = BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0),))
    assert math.inf not in bounded
    assert -math.inf not in bounded


def test_int_bounds_normalize_with_float_bounds() -> None:
    """`int` bounds sort, merge and membership-test seamlessly with `float` ones."""
    result = BoundsSet(bounds=(Bounds(lower=1, upper=5), Bounds(lower=5.0, upper=10.0)))
    assert result.bounds == (Bounds(lower=1, upper=10.0),)
    assert 7 in result
    assert 0 not in result


def test_str() -> None:
    """The string form joins members with a union symbol."""
    bounds_set = BoundsSet(
        bounds=(Bounds(lower=1.0, upper=5.0), Bounds(lower=15.0, upper=20.0))
    )
    assert str(bounds_set) == "[1.0,5.0]∪[15.0,20.0]"


def test_equality_on_normalized_form() -> None:
    """Sets built from different inputs that normalize equal are equal and hash equal."""
    a = BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0), Bounds(lower=3.0, upper=10.0)))
    b = BoundsSet(bounds=(Bounds(lower=1.0, upper=10.0),))
    assert a == b
    assert hash(a) == hash(b)


def test_hashable() -> None:
    """`BoundsSet` can be used in sets and as dict keys."""
    a = BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0),))
    b = BoundsSet(bounds=(Bounds(lower=1.0, upper=5.0),))
    c = BoundsSet(bounds=(Bounds(lower=6.0, upper=8.0),))
    assert len({a, b, c}) == 2
