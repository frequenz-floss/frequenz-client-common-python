# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH


"""Definitions for bounds."""

import dataclasses
from typing import Any, Self


@dataclasses.dataclass(frozen=True, kw_only=True)
class BaseBounds:
    """A base class for well-formed and malformed metric bounds.

    This class cannot be instantiated directly. Use [`Bounds`][..Bounds] for a
    valid pair of bounds.
    """

    lower: float | int | None = None
    """The lower bound.

    If `None`, there is no lower bound.
    """

    upper: float | int | None = None
    """The upper bound.

    If `None`, there is no upper bound.
    """

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is BaseBounds:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Bounds(BaseBounds):
    """A set of lower and upper bounds for any metric.

    The lower bound must be less than or equal to the upper bound.

    The units of the bounds are always the same as the related metric.

    Note:
        Raises a `ValueError` if [`lower`][.lower] is greater than
        [`upper`][.upper].
    """

    def __post_init__(self) -> None:
        """Validate these bounds."""
        if self.lower is None:
            return
        if self.upper is None:
            return
        if self.lower > self.upper:
            raise ValueError(
                f"Lower bound ({self.lower}) must be less than or equal to upper "
                f"bound ({self.upper})"
            )

    def __str__(self) -> str:
        """Return a string representation of these bounds."""
        return f"[{self.lower},{self.upper}]"
