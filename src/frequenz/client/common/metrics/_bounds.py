# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH


"""Definitions for bounds."""

from typing import cast

from frequenz.core.math import Interval
from typing_extensions import deprecated


@deprecated(
    "`Bounds` is deprecated; use `frequenz.core.math.Interval[float | None]` "
    "directly. `Bounds` is kept as a subclass of `Interval[float | None]` so "
    "existing instances remain assignment-compatible with the new "
    "`Interval`-typed fields."
)
class Bounds(Interval[float | None]):
    """A set of lower and upper bounds for any metric.

    The lower bound must be less than or equal to the upper bound.

    The units of the bounds are always the same as the related metric.

    `Bounds` is a thin, deprecated subclass of
    [`Interval[float | None]`][frequenz.core.math.Interval]. It inherits all
    validation, containment, equality, and string-conversion behaviour from
    `Interval` and exposes the historical `lower` / `upper` attribute names
    as deprecated aliases for `start` / `end`.

    Deprecated:
        Use [`Interval[float | None]`][frequenz.core.math.Interval] from
        the `frequenz-core` package instead.
    """

    def __init__(
        self, *, lower: float | None = None, upper: float | None = None
    ) -> None:
        """Create a `Bounds` instance using the deprecated `lower`/`upper` kwargs.

        Args:
            lower: Deprecated alias for
                [`Interval.start`][frequenz.core.math.Interval.start].
            upper: Deprecated alias for
                [`Interval.end`][frequenz.core.math.Interval.end].
        """
        super().__init__(lower, upper)

    @property
    @deprecated("`Bounds.lower` is deprecated; use `Interval.start` instead.")
    def lower(self) -> float | None:
        """Return the lower bound (deprecated alias for `start`).

        Deprecated:
            Use [`start`][frequenz.core.math.Interval.start] instead.

        Returns:
            The value stored in [`start`][frequenz.core.math.Interval.start].
        """
        return self.start

    @property
    @deprecated("`Bounds.upper` is deprecated; use `Interval.end` instead.")
    def upper(self) -> float | None:
        """Return the upper bound (deprecated alias for `end`).

        Deprecated:
            Use [`end`][frequenz.core.math.Interval.end] instead.

        Returns:
            The value stored in [`end`][frequenz.core.math.Interval.end].
        """
        return self.end

    def __eq__(self, other: object) -> bool:
        """Return whether this bound matches another interval-like object."""
        if isinstance(other, Interval):
            other_interval = cast(Interval[float | None], other)
            return self.start == other_interval.start and self.end == other_interval.end
        return False

    def __hash__(self) -> int:
        """Return the hash for this interval-compatible bound."""
        return hash((self.start, self.end))
