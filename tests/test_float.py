# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the `FloatInt` type alias."""

from frequenz.core.typing import FloatInt


def test_alias_covers_float_and_int() -> None:
    """The alias is exactly the `float | int` union."""
    assert FloatInt == float | int


def test_alias_admits_the_numeric_tower() -> None:
    """`float`, `int` and (inherently) `bool` values all satisfy the alias."""
    assert isinstance(1.5, FloatInt)
    assert isinstance(1, FloatInt)
    # `bool` is a subclass of `int`, this is documented as not guarded against.
    assert isinstance(True, FloatInt)
    assert not isinstance("1.5", FloatInt)
    assert not isinstance(None, FloatInt)
