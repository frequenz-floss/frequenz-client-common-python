# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidBoundsSet`."""

from frequenz.client.common.metrics import (
    Bounds,
    BoundsSet,
    InvalidBounds,
    InvalidBoundsSet,
)


def test_preserves_raw_bounds_unmerged() -> None:
    """All bounds are preserved in order, without sorting or merging."""
    raw = (
        Bounds(lower=5.0, upper=10.0),
        InvalidBounds(lower=10.0, upper=-10.0),
        Bounds(lower=1.0, upper=3.0),
    )
    invalid = InvalidBoundsSet(bounds=raw)
    assert invalid.bounds == raw


def test_is_not_bounds_set_subclass() -> None:
    """`InvalidBoundsSet` is a sibling of `BoundsSet`, not a subclass."""
    assert not issubclass(InvalidBoundsSet, BoundsSet)


def test_no_membership_test() -> None:
    """`InvalidBoundsSet` provides no membership test for malformed data."""
    invalid = InvalidBoundsSet(bounds=(InvalidBounds(lower=10.0, upper=-10.0),))
    assert not hasattr(invalid, "__contains__")


def test_truthy() -> None:
    """An invalid set is truthy: it is malformed, not "unbounded"."""
    invalid = InvalidBoundsSet(bounds=(InvalidBounds(lower=10.0, upper=-10.0),))
    assert invalid


def test_str() -> None:
    """`__str__` wraps the members in the `<invalid:...>` marker."""
    invalid = InvalidBoundsSet(
        bounds=(Bounds(lower=1.0, upper=5.0), InvalidBounds(lower=10.0, upper=-10.0))
    )
    assert str(invalid) == "<invalid:[1.0,5.0]∪<invalid:[10.0,-10.0]>>"


def test_equality() -> None:
    """Two invalid sets with the same raw bounds are equal and hash equal."""
    a = InvalidBoundsSet(bounds=(InvalidBounds(lower=10.0, upper=-10.0),))
    b = InvalidBoundsSet(bounds=(InvalidBounds(lower=10.0, upper=-10.0),))
    assert a == b
    assert hash(a) == hash(b)
