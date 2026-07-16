# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for `Bounds`."""

import re

import pytest

from frequenz.client.common.metrics import BaseBounds, Bounds


def test_is_base_bounds_subclass() -> None:
    """`Bounds` is a subclass of `BaseBounds`."""
    assert issubclass(Bounds, BaseBounds)


@pytest.mark.parametrize(
    "lower, upper",
    [
        (None, None),
        (10.0, None),
        (None, -10.0),
        (-10.0, 10.0),
        (10.0, 10.0),
        (-10.0, -10.0),
        (0.0, 10.0),
        (-10, 0.0),
        (0.0, 0.0),
    ],
)
def test_creation(lower: float | int | None, upper: float | int | None) -> None:
    """Test creation of Bounds with valid values."""
    bounds = Bounds(lower=lower, upper=upper)
    assert bounds.lower == lower
    assert bounds.upper == upper


def test_invalid_values() -> None:
    """Test that Bounds creation fails with invalid values."""
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Lower bound (10.0) must be less than or equal to upper bound (-10.0)"
        ),
    ):
        Bounds(lower=10.0, upper=-10.0)


def test_str_representation() -> None:
    """Test string representation of Bounds."""
    bounds = Bounds(lower=-10.0, upper=10.0)
    assert str(bounds) == "[-10.0,10.0]"


def test_equality() -> None:
    """Test equality comparison of Bounds objects."""
    bounds1 = Bounds(lower=-10.0, upper=10.0)
    bounds2 = Bounds(lower=-10.0, upper=10.0)
    bounds3 = Bounds(lower=-5.0, upper=5.0)

    assert bounds1 == bounds2
    assert bounds1 != bounds3
    assert bounds2 != bounds3


def test_hash() -> None:
    """Test that Bounds objects can be used in sets and as dictionary keys."""
    bounds1 = Bounds(lower=-10.0, upper=10.0)
    bounds2 = Bounds(lower=-10.0, upper=10.0)
    bounds3 = Bounds(lower=-5.0, upper=5.0)

    bounds_set = {bounds1, bounds2, bounds3}
    assert len(bounds_set) == 2  # bounds1 and bounds2 are equal

    bounds_dict = {bounds1: "test1", bounds3: "test2"}
    assert len(bounds_dict) == 2
