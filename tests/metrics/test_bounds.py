# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Bounds class."""

import re
import warnings

import pytest
from frequenz.core.math import Interval

from frequenz.client.common.metrics import Bounds


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
def test_creation(lower: float | None, upper: float | None) -> None:
    """Test creation of Bounds with valid values."""
    with pytest.deprecated_call():
        bounds = Bounds(lower=lower, upper=upper)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        assert bounds.lower == lower
        assert bounds.upper == upper


def test_invalid_values() -> None:
    """Test that Bounds creation fails with invalid values."""
    with pytest.raises(
        ValueError,
        match=re.escape("The start (10.0) can't be bigger than end (-10.0)"),
    ):
        with pytest.deprecated_call():
            Bounds(lower=10.0, upper=-10.0)


def test_str_representation() -> None:
    """Test string representation of Bounds."""
    with pytest.deprecated_call():
        bounds = Bounds(lower=-10.0, upper=10.0)
    assert str(bounds) == "[-10.0, 10.0]"


def test_str_representation_for_none_endpoints() -> None:
    """Test string representation of open Bounds."""
    with pytest.deprecated_call():
        bounds = Bounds(lower=None, upper=None)
    assert str(bounds) == "[∞, ∞]"


def test_equality() -> None:
    """Test equality comparison of Bounds objects."""
    with pytest.deprecated_call():
        bounds1 = Bounds(lower=-10.0, upper=10.0)
    with pytest.deprecated_call():
        bounds2 = Bounds(lower=-10.0, upper=10.0)
    with pytest.deprecated_call():
        bounds3 = Bounds(lower=-5.0, upper=5.0)

    assert bounds1 == bounds2
    assert bounds1 != bounds3
    assert bounds2 != bounds3


def test_hash() -> None:
    """Test that Bounds objects can be used in sets and as dictionary keys."""
    with pytest.deprecated_call():
        bounds1 = Bounds(lower=-10.0, upper=10.0)
    with pytest.deprecated_call():
        bounds2 = Bounds(lower=-10.0, upper=10.0)
    with pytest.deprecated_call():
        bounds3 = Bounds(lower=-5.0, upper=5.0)

    bounds_set = {bounds1, bounds2, bounds3}
    assert len(bounds_set) == 2

    bounds_dict = {bounds1: "test1", bounds3: "test2"}
    assert len(bounds_dict) == 2


def test_bounds_is_interval_subclass() -> None:
    """`Bounds` is a subclass of `Interval[float | None]`."""
    assert issubclass(Bounds, Interval)


def test_bounds_instance_is_interval() -> None:
    """A `Bounds` instance is an `Interval` instance (LSP)."""
    with pytest.deprecated_call():
        b = Bounds(lower=1.0, upper=2.0)
    assert isinstance(b, Interval)


def test_bounds_equals_interval_with_same_endpoints() -> None:
    """`Bounds(lower=1, upper=2) == Interval(1, 2)`."""
    with pytest.deprecated_call():
        b = Bounds(lower=1.0, upper=2.0)
    assert b == Interval[float | None](1.0, 2.0)


def test_bounds_lower_is_deprecated() -> None:
    """Reading `Bounds.lower` emits `DeprecationWarning` and returns `.start`."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        b = Bounds(lower=1.0, upper=2.0)
    with pytest.deprecated_call(match=r"lower.*deprecated.*start"):
        value = b.lower
    assert value == b.start == 1.0


def test_bounds_upper_is_deprecated() -> None:
    """Reading `Bounds.upper` emits `DeprecationWarning` and returns `.end`."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        b = Bounds(lower=1.0, upper=2.0)
    with pytest.deprecated_call(match=r"upper.*deprecated.*end"):
        value = b.upper
    assert value == b.end == 2.0
