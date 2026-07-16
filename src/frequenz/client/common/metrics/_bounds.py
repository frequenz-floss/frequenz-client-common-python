# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH


"""Definitions for bounds."""

import dataclasses
from typing import Any, Self


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


@dataclasses.dataclass(frozen=True, kw_only=True)
class MissingBounds(InvalidBounds):
    """Metric bounds that were present on the wire but carried no data.

    Some wire messages name a metric without providing any bounds values
    (e.g. a `MetricConfigBounds` entry whose `config_bounds` field was not
    set). This class flags that situation explicitly so callers can decide
    how to handle it — treat the metric as unbounded, raise, or report —
    instead of the ambiguity of an unbounded [`Bounds`][..Bounds] that
    happens to have both fields as `None`.

    Being a subclass of [`InvalidBounds`][..InvalidBounds] keeps container
    typing simple: a `Bounds | InvalidBounds` union catches the missing
    case, and callers who want to distinguish it narrow with a
    ``case MissingBounds()`` arm before the generic
    ``case InvalidBounds()``.

    Instances always carry [`lower`][.lower] and [`upper`][.upper] as
    `None`.

    Note:
        Raises a `ValueError` if [`lower`][.lower] or [`upper`][.upper]
        is set to anything other than `None`.
    """

    def __post_init__(self) -> None:
        """Validate that no bound values are carried."""
        if self.lower is not None or self.upper is not None:
            raise ValueError("MissingBounds cannot carry bound values")

    def __str__(self) -> str:
        """Return a compact string representation of these missing bounds."""
        return "<invalid:missing>"
