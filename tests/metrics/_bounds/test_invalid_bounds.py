# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidBounds`."""

from frequenz.client.common.metrics import BaseBounds, Bounds, InvalidBounds


def test_is_base_bounds_subclass() -> None:
    """`InvalidBounds` is a subclass of `BaseBounds`."""
    assert issubclass(InvalidBounds, BaseBounds)


def test_is_not_bounds_subclass() -> None:
    """`InvalidBounds` is a sibling of `Bounds`, not a subclass."""
    assert not issubclass(InvalidBounds, Bounds)


def test_accepts_invalid_range() -> None:
    """`InvalidBounds` preserves an upper bound below its lower bound."""
    bounds = InvalidBounds(lower=10.0, upper=-10.0)
    assert bounds.lower == 10.0
    assert bounds.upper == -10.0


def test_accepts_valid_looking_values() -> None:
    """`InvalidBounds` enforces no invariants and accepts any values."""
    bounds = InvalidBounds(lower=-10.0, upper=10.0)
    assert bounds.lower == -10.0
    assert bounds.upper == 10.0


def test_str_representation() -> None:
    """`InvalidBounds.__str__` wraps the compact form in `<invalid:...>`."""
    assert str(InvalidBounds(lower=10.0, upper=-10.0)) == "<invalid:[10.0,-10.0]>"
    assert str(InvalidBounds()) == "<invalid:[None,None]>"


def test_equality() -> None:
    """Test equality comparison of `InvalidBounds` objects."""
    bounds1 = InvalidBounds(lower=10.0, upper=-10.0)
    bounds2 = InvalidBounds(lower=10.0, upper=-10.0)
    bounds3 = InvalidBounds(lower=5.0, upper=-5.0)

    assert bounds1 == bounds2
    assert bounds1 != bounds3


def test_hash() -> None:
    """Test that `InvalidBounds` objects can be used in sets and as dict keys."""
    bounds1 = InvalidBounds(lower=10.0, upper=-10.0)
    bounds2 = InvalidBounds(lower=10.0, upper=-10.0)
    bounds3 = InvalidBounds(lower=5.0, upper=-5.0)

    assert len({bounds1, bounds2, bounds3}) == 2
