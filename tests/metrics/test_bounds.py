# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Bounds class."""

import re

import pytest

from frequenz.client.common import InvalidAttributeError
from frequenz.client.common.metrics import (
    BaseBounds,
    Bounds,
    InvalidBounds,
    InvalidBoundsError,
    MissingBounds,
)


def test_base_bounds_cannot_be_instantiated_directly() -> None:
    """`BaseBounds` refuses direct instantiation."""
    with pytest.raises(TypeError, match="Cannot instantiate BaseBounds directly"):
        BaseBounds()


def test_bounds_is_base_bounds_subclass() -> None:
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
def test_creation(lower: float, upper: float) -> None:
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


def test_invalid_bounds_is_base_bounds_subclass() -> None:
    """`InvalidBounds` is a subclass of `BaseBounds`."""
    assert issubclass(InvalidBounds, BaseBounds)


def test_invalid_bounds_is_not_bounds_subclass() -> None:
    """`InvalidBounds` is a sibling of `Bounds`, not a subclass."""
    assert not issubclass(InvalidBounds, Bounds)


def test_invalid_bounds_accepts_invalid_range() -> None:
    """`InvalidBounds` preserves an upper bound below its lower bound."""
    bounds = InvalidBounds(lower=10.0, upper=-10.0)
    assert bounds.lower == 10.0
    assert bounds.upper == -10.0


def test_invalid_bounds_accepts_valid_looking_values() -> None:
    """`InvalidBounds` enforces no invariants and accepts any values."""
    bounds = InvalidBounds(lower=-10.0, upper=10.0)
    assert bounds.lower == -10.0
    assert bounds.upper == 10.0


def test_invalid_bounds_str_representation() -> None:
    """`InvalidBounds.__str__` wraps the compact form in `<invalid:...>`."""
    assert str(InvalidBounds(lower=10.0, upper=-10.0)) == "<invalid:[10.0,-10.0]>"
    assert str(InvalidBounds()) == "<invalid:[None,None]>"


def test_invalid_bounds_equality() -> None:
    """Test equality comparison of `InvalidBounds` objects."""
    bounds1 = InvalidBounds(lower=10.0, upper=-10.0)
    bounds2 = InvalidBounds(lower=10.0, upper=-10.0)
    bounds3 = InvalidBounds(lower=5.0, upper=-5.0)

    assert bounds1 == bounds2
    assert bounds1 != bounds3


def test_invalid_bounds_hash() -> None:
    """Test that `InvalidBounds` objects can be used in sets and as dict keys."""
    bounds1 = InvalidBounds(lower=10.0, upper=-10.0)
    bounds2 = InvalidBounds(lower=10.0, upper=-10.0)
    bounds3 = InvalidBounds(lower=5.0, upper=-5.0)

    assert len({bounds1, bounds2, bounds3}) == 2


def test_missing_bounds_is_invalid_bounds_subclass() -> None:
    """`MissingBounds` is a subclass of `InvalidBounds` (and `BaseBounds`)."""
    assert issubclass(MissingBounds, InvalidBounds)
    assert issubclass(MissingBounds, BaseBounds)


def test_missing_bounds_defaults_to_none() -> None:
    """`MissingBounds` carries no bound values by default."""
    bounds = MissingBounds()
    assert bounds.lower is None
    assert bounds.upper is None


@pytest.mark.parametrize(
    "lower, upper",
    [
        (1.0, None),
        (None, 1.0),
        (1.0, 2.0),
        (0.0, 0.0),
    ],
)
def test_missing_bounds_rejects_values(
    lower: float | int | None, upper: float | int | None
) -> None:
    """`MissingBounds` refuses to carry any bound values."""
    with pytest.raises(
        ValueError, match=re.escape("MissingBounds cannot carry bound values")
    ):
        MissingBounds(lower=lower, upper=upper)


def test_missing_bounds_str_representation() -> None:
    """`MissingBounds.__str__` returns the `<invalid:missing>` marker."""
    assert str(MissingBounds()) == "<invalid:missing>"


def test_missing_bounds_not_equal_to_invalid_bounds() -> None:
    """Dataclass equality is class-scoped: `MissingBounds() != InvalidBounds()`."""
    assert MissingBounds() != InvalidBounds()


def test_missing_bounds_equality() -> None:
    """Two `MissingBounds` instances always compare equal."""
    assert MissingBounds() == MissingBounds()


def test_invalid_bounds_error_default_message() -> None:
    """`InvalidBoundsError` builds a default message from the invalid bounds."""
    invalid = InvalidBounds(lower=10.0, upper=-10.0)
    error = InvalidBoundsError("some-instance", "config_bounds", invalid)

    assert error.bounds is invalid
    assert (
        str(error)
        == f"invalid bounds {invalid!r} for attribute 'config_bounds' "
        "in some-instance"
    )


def test_invalid_bounds_error_custom_message() -> None:
    """`InvalidBoundsError` accepts a custom message."""
    invalid = InvalidBounds(lower=10.0, upper=-10.0)
    error = InvalidBoundsError(
        "some-instance",
        "config_bounds",
        invalid,
        message="bad bounds from server",
    )

    assert error.bounds is invalid
    assert str(error) == "bad bounds from server"


def test_invalid_bounds_error_is_invalid_attribute_error() -> None:
    """`InvalidBoundsError` is an `InvalidAttributeError`."""
    assert issubclass(InvalidBoundsError, InvalidAttributeError)


def test_invalid_bounds_error_is_value_error() -> None:
    """`InvalidBoundsError` is a `ValueError`."""
    assert issubclass(InvalidBoundsError, ValueError)
