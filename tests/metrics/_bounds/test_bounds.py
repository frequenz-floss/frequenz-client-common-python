# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for `Bounds`."""

import math
import re

import pytest
from frequenz.core.typing import FloatInt

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
        (-10, 10),  # the numeric tower lets plain `int` bounds in
        (0.0, 0.0),
    ],
)
def test_creation(lower: FloatInt | None, upper: FloatInt | None) -> None:
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


@pytest.mark.parametrize(
    "lower, upper",
    [
        (math.nan, 10.0),
        (-10.0, math.nan),
        (math.nan, math.nan),
        (math.nan, None),
        (None, math.nan),
    ],
    ids=["lower", "upper", "both", "lower-only", "upper-only"],
)
def test_nan_rejected(lower: FloatInt | None, upper: FloatInt | None) -> None:
    """`NaN` is not a valid bound in either endpoint."""
    with pytest.raises(ValueError, match="NaN"):
        Bounds(lower=lower, upper=upper)


def test_large_int_endpoint_constructs() -> None:
    """An integer endpoint too large to fit in a `float` is a valid finite bound."""
    huge = 10**1000
    bounds = Bounds(lower=-huge, upper=huge)
    assert bounds.lower == -huge
    assert bounds.upper == huge
    assert 0 in bounds
    assert 10**2000 not in bounds
    assert -(10**2000) not in bounds


@pytest.mark.parametrize(
    "lower, upper, expected_lower, expected_upper",
    [
        (-math.inf, math.inf, None, None),
        (-math.inf, None, None, None),
        (-math.inf, 10.0, None, 10.0),
        (None, math.inf, None, None),
        (-10.0, math.inf, -10.0, None),
    ],
    ids=["both", "lower-only", "lower-with-upper", "upper-only", "upper-with-lower"],
)
def test_infinite_open_endpoints_normalize_to_none(
    lower: FloatInt | None,
    upper: FloatInt | None,
    expected_lower: FloatInt | None,
    expected_upper: FloatInt | None,
) -> None:
    """A `-inf` lower and a `+inf` upper are the unbounded direction, so become `None`."""
    bounds = Bounds(lower=lower, upper=upper)
    assert bounds.lower == expected_lower
    assert bounds.upper == expected_upper


def test_infinite_full_equals_unbounded() -> None:
    """`Bounds(-inf, +inf)` canonicalizes to the unbounded `Bounds()`."""
    bounds = Bounds(lower=-math.inf, upper=math.inf)
    assert bounds == Bounds()
    assert bounds.lower is None
    assert bounds.upper is None
    assert not bounds.is_bounded()


@pytest.mark.parametrize(
    "lower, upper",
    [
        (math.inf, 5.0),
        (5.0, -math.inf),
    ],
    ids=["plus-inf-lower", "minus-inf-upper"],
)
def test_wrong_side_infinity_contradiction_is_invalid(
    lower: FloatInt, upper: FloatInt
) -> None:
    """A wrong-side infinity stays a real endpoint, so a contradictory pair still raises."""
    with pytest.raises(ValueError, match="must be less than or equal"):
        Bounds(lower=lower, upper=upper)


def test_wrong_side_infinity_alone_is_kept() -> None:
    """A lone wrong-side infinity is not the unbounded direction, so it is kept as-is."""
    assert Bounds(lower=math.inf).lower == math.inf
    assert Bounds(upper=-math.inf).upper == -math.inf


def test_str_representation() -> None:
    """Test string representation of Bounds."""
    bounds = Bounds(lower=-10.0, upper=10.0)
    assert str(bounds) == "[-10.0,10.0]"
    # `int` bounds keep their `int` repr; values are stored untouched.
    assert str(Bounds(lower=-10, upper=10)) == "[-10,10]"


def test_equality() -> None:
    """Test equality comparison of Bounds objects."""
    bounds1 = Bounds(lower=-10.0, upper=10.0)
    bounds2 = Bounds(lower=-10.0, upper=10.0)
    bounds3 = Bounds(lower=-5.0, upper=5.0)

    assert bounds1 == bounds2
    assert bounds1 != bounds3
    assert bounds2 != bounds3


def test_equality_int_float() -> None:
    """`int` and `float` bounds with the same value compare equal (`1 == 1.0`)."""
    assert Bounds(lower=-10, upper=10) == Bounds(lower=-10.0, upper=10.0)


def test_hash() -> None:
    """Test that Bounds objects can be used in sets and as dictionary keys."""
    bounds1 = Bounds(lower=-10.0, upper=10.0)
    bounds2 = Bounds(lower=-10.0, upper=10.0)
    bounds3 = Bounds(lower=-5.0, upper=5.0)

    bounds_set = {bounds1, bounds2, bounds3}
    assert len(bounds_set) == 2  # bounds1 and bounds2 are equal

    bounds_dict = {bounds1: "test1", bounds3: "test2"}
    assert len(bounds_dict) == 2


@pytest.mark.parametrize(
    "lower, upper, item, expected",
    [
        (None, None, 0.0, True),
        (None, None, 1e9, True),
        (-10.0, 10.0, 0.0, True),
        (-10.0, 10.0, -10.0, True),  # lower bound is inclusive
        (-10.0, 10.0, 10.0, True),  # upper bound is inclusive
        (-10.0, 10.0, -10.1, False),
        (-10.0, 10.0, 10.1, False),
        (None, 10.0, -1e9, True),  # unbounded below
        (None, 10.0, 10.0, True),
        (None, 10.0, 10.1, False),
        (-10.0, None, 1e9, True),  # unbounded above
        (-10.0, None, -10.0, True),
        (-10.0, None, -10.1, False),
        (-10, 10, 5, True),  # `int` bounds and `int` items work the same
        (-10, 10, 10, True),
        (-10, 10, 11, False),
        (-10.0, 10.0, 10, True),  # `int` item against `float` bounds
        (-10, 10, 10.1, False),  # `float` item against `int` bounds
    ],
)
def test_contains(
    lower: FloatInt | None, upper: FloatInt | None, item: FloatInt, expected: bool
) -> None:
    """Test membership with `in`, inclusive on both ends."""
    assert (item in Bounds(lower=lower, upper=upper)) is expected


def test_contains_none() -> None:
    """`None` is never contained, even by unbounded bounds."""
    assert None not in Bounds()
    assert None not in Bounds(lower=-10.0, upper=10.0)


def test_contains_nan() -> None:
    """`NaN` is never contained, even by unbounded bounds."""
    assert math.nan not in Bounds()
    assert math.nan not in Bounds(lower=-10.0, upper=10.0)


@pytest.mark.parametrize(
    "lower, upper, item, expected",
    [
        (None, None, 10**1000, True),  # huge positive int in the unbounded set
        (None, None, -(10**1000), True),  # huge negative int in the unbounded set
        (0.0, None, 10**1000, True),  # huge int above a finite lower
        (0.0, None, -(10**1000), False),  # huge negative int below the lower
        (None, 0.0, 10**1000, False),  # huge int above a finite upper
        (None, 0.0, -(10**1000), True),  # huge negative int below the upper
        (-1.0, 1.0, 10**1000, False),  # huge int outside a finite range
        (-1.0, 1.0, -(10**1000), False),
    ],
)
def test_contains_large_int(
    lower: FloatInt | None, upper: FloatInt | None, item: FloatInt, expected: bool
) -> None:
    """Integers too large to convert to `float` are tested without overflowing."""
    assert (item in Bounds(lower=lower, upper=upper)) is expected


@pytest.mark.parametrize(
    "lower, upper, expected",
    [
        (None, None, False),  # fully unbounded accepts everything -> falsy
        (-10.0, None, True),
        (None, 10.0, True),
        (-10.0, 10.0, True),
        (0.0, 0.0, True),  # a zero bound still counts as bounded
    ],
)
def test_bool_and_is_bounded(
    lower: float | None, upper: float | None, expected: bool
) -> None:
    """Unbounded bounds are falsy; any set bound makes them bounded/truthy."""
    bounds = Bounds(lower=lower, upper=upper)
    assert bool(bounds) is expected
    assert bounds.is_bounded() is expected
