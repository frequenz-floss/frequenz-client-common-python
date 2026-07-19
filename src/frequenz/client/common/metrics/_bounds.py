# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH


"""Definitions for bounds."""

import dataclasses
from typing import Any, Self

from .._exception import InvalidAttributeError


@dataclasses.dataclass(frozen=True, kw_only=True)
class BaseBounds:
    """A base class for well-formed and malformed metric bounds.

    This class cannot be instantiated directly. Use [`Bounds`][..Bounds] for a
    valid pair of bounds or [`InvalidBounds`][..InvalidBounds] to preserve
    malformed wire data.
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
        [`upper`][.upper]. Use [`InvalidBounds`][..InvalidBounds] to
        represent malformed bounds data received from the wire.
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

    def __contains__(self, item: float | None) -> bool:
        """Check whether a value is within these bounds.

        The bounds are inclusive on both ends, and a `None` bound means these
        bounds are unbounded in that direction. `None` is a bound marker only
        and is never itself a value, so `None` is never contained.

        Args:
            item: The value to check.

        Returns:
            Whether `item` is within these bounds.
        """
        if item is None:
            return False
        if self.lower is not None and item < self.lower:
            return False
        if self.upper is not None and item > self.upper:
            return False
        return True

    def __bool__(self) -> bool:
        """Return whether these bounds restrict the range in any direction.

        Fully unbounded bounds (`Bounds()`, where both `lower` and `upper`
        are `None`) accept every value and are therefore falsy; any set bound
        makes them truthy.

        Returns:
            Whether at least one of `lower` or `upper` is set.
        """
        return self.lower is not None or self.upper is not None

    def is_bounded(self) -> bool:
        """Return whether these bounds restrict the range in any direction.

        This is the explicit spelling of these bounds' truthiness: fully
        unbounded bounds (`Bounds()`) are not bounded, while any set `lower`
        or `upper` makes them bounded.

        Returns:
            Whether at least one of `lower` or `upper` is set.
        """
        return bool(self)


@dataclasses.dataclass(frozen=True, kw_only=True)
class InvalidBounds(BaseBounds):
    """Metric bounds with malformed data received from the wire.

    This class preserves bounds data that fails the invariants required for
    a well-formed [`Bounds`][..Bounds], allowing callers to inspect the raw
    values without accidentally using them for range checks. Use a semantic
    accessor, such as `ElectricalComponent.get_metric_config_bounds()`, to
    receive a clear error on invalid data.
    """

    def __str__(self) -> str:
        """Return a compact string representation of these invalid bounds."""
        return f"<invalid:[{self.lower},{self.upper}]>"


class InvalidBoundsError(InvalidAttributeError):
    """Raised when a semantic accessor sees invalid metric bounds.

    The offending [`InvalidBounds`][..InvalidBounds] is available as the
    [`bounds`][.bounds] attribute so callers can inspect the raw wire data.

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self,
        instance: object,
        attr_name: str,
        bounds: InvalidBounds,
        message: str | None = None,
    ) -> None:
        """Initialize this error.

        Args:
            instance: The instance that was being accessed when this error was raised.
            attr_name: The name of the attribute that was being accessed.
            bounds: The invalid bounds instance.
            message: A custom error message. If `None`, a default message mentioning
                the invalid bounds is used.
        """
        self.bounds: InvalidBounds = bounds
        """The invalid bounds that caused this error."""

        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"invalid bounds {bounds!r} for attribute {attr_name!r} in {instance}"
            ),
        )
