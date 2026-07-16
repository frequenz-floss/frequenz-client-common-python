# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `MissingBounds`."""

import re

import pytest

from frequenz.client.common.metrics import BaseBounds, InvalidBounds, MissingBounds


def test_is_invalid_bounds_subclass() -> None:
    """`MissingBounds` is a subclass of `InvalidBounds` (and `BaseBounds`)."""
    assert issubclass(MissingBounds, InvalidBounds)
    assert issubclass(MissingBounds, BaseBounds)


def test_defaults_to_none() -> None:
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
def test_rejects_values(lower: float | int | None, upper: float | int | None) -> None:
    """`MissingBounds` refuses to carry any bound values."""
    with pytest.raises(
        ValueError, match=re.escape("MissingBounds cannot carry bound values")
    ):
        MissingBounds(lower=lower, upper=upper)


def test_str_representation() -> None:
    """`MissingBounds.__str__` returns the `<invalid:missing>` marker."""
    assert str(MissingBounds()) == "<invalid:missing>"


def test_not_equal_to_invalid_bounds() -> None:
    """Dataclass equality is class-scoped: `MissingBounds() != InvalidBounds()`."""
    assert MissingBounds() != InvalidBounds()


def test_equality() -> None:
    """Two `MissingBounds` instances always compare equal."""
    assert MissingBounds() == MissingBounds()
