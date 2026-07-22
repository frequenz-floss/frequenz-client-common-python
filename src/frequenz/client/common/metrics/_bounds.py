# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH


"""Definitions for bounds."""

import bisect
import dataclasses
import math
from collections.abc import Iterable
from typing import Any, Self

from .._exception import InvalidAttributeError
from .._float import FloatInt


@dataclasses.dataclass(frozen=True, kw_only=True)
class BaseBounds:
    """A base class for well-formed and malformed metric bounds.

    This class cannot be instantiated directly. Use [`Bounds`][..Bounds] for a
    valid pair of bounds or [`InvalidBounds`][..InvalidBounds] to preserve
    malformed wire data.
    """

    lower: FloatInt | None = None
    """The lower bound.

    If `None`, there is no lower bound.
    """

    upper: FloatInt | None = None
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
        [`upper`][.upper], or if either bound is `NaN` (which is never a
        valid endpoint). Use [`InvalidBounds`][..InvalidBounds] to
        represent malformed bounds data received from the wire.
    """

    def __post_init__(self) -> None:
        """Validate these bounds."""
        # Only `float` can be `NaN`; guarding with `isinstance` also avoids
        # `math.isnan()` raising `OverflowError` on an `int` too large for a
        # `float` (a valid `FloatInt` endpoint).
        if isinstance(self.lower, float) and math.isnan(self.lower):
            raise ValueError("Lower bound cannot be NaN")
        if isinstance(self.upper, float) and math.isnan(self.upper):
            raise ValueError("Upper bound cannot be NaN")
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

    def __contains__(self, item: FloatInt | None) -> bool:
        """Check whether a value is within these bounds.

        The bounds are inclusive on both ends, and a `None` bound means these
        bounds are unbounded in that direction. `None` is a bound marker only
        and is never itself a value, so `None` is never contained.

        Args:
            item: The value to check.

        Returns:
            Whether `item` is within these bounds.
        """
        if item is None or (isinstance(item, float) and math.isnan(item)):
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
                else f"invalid bounds {bounds} for attribute {attr_name!r} in {instance}"
            ),
        )


def _end_covers_start(upper: FloatInt | None, lower: FloatInt | None) -> bool:
    """Return whether an upper bound reaches a lower bound, treating `None` as ±∞.

    Args:
        upper: An upper bound, where `None` means +∞.
        lower: A lower bound, where `None` means -∞.

    Returns:
        Whether `upper >= lower` under the ±∞ convention.
    """
    if upper is None:
        return True
    if lower is None:
        return True
    return not upper < lower


def _max_upper(first: FloatInt | None, second: FloatInt | None) -> FloatInt | None:
    """Return the larger of two upper bounds, where `None` means +∞.

    Args:
        first: An upper bound.
        second: Another upper bound.

    Returns:
        The larger of `first` and `second` under the +∞ convention.
    """
    if first is None or second is None:
        return None
    return second if first < second else first


def _sort_and_merge_bounds(bounds: Iterable[Bounds]) -> tuple[Bounds, ...]:
    """Sort bounds by lower value and merge overlapping or touching ones.

    A `None` lower bound is treated as -∞ and a `None` upper bound as +∞.
    Bounds are inclusive on both ends, so `[1, 5]` and `[5, 10]` touch and
    merge into `[1, 10]`. If the merged result covers the whole space (a single
    unbounded `[None, None]`), the empty tuple is returned instead, so the
    unbounded set has a single canonical (empty) representation.

    Args:
        bounds: The bounds to normalize.

    Returns:
        A tuple of sorted, pairwise non-overlapping bounds covering the same
            values as the input, or the empty tuple when the union is unbounded.
    """
    all_bounds = list(bounds)
    if not all_bounds:
        return ()

    with_none_lower: list[Bounds] = []
    with_real_lower: list[tuple[FloatInt, Bounds]] = []
    for bound in all_bounds:
        if bound.lower is None:
            with_none_lower.append(bound)
        else:
            with_real_lower.append((bound.lower, bound))
    with_real_lower.sort(key=lambda pair: pair[0])
    ordered = [pair[1] for pair in with_real_lower]

    if with_none_lower:
        if any(bound.upper is None for bound in with_none_lower):
            ordered.insert(0, Bounds(lower=None, upper=None))
        else:
            uppers = [b.upper for b in with_none_lower if b.upper is not None]
            ordered.insert(0, Bounds(lower=None, upper=max(uppers)))

    result: list[Bounds] = [ordered[0]]
    for current in ordered[1:]:
        last = result[-1]
        if _end_covers_start(last.upper, current.lower):
            result[-1] = Bounds(
                lower=last.lower, upper=_max_upper(last.upper, current.upper)
            )
        else:
            result.append(current)

    if len(result) == 1 and result[0].lower is None and result[0].upper is None:
        return ()
    return tuple(result)


@dataclasses.dataclass(frozen=True, kw_only=True)
class BoundsSet:
    """A normalized set of metric bounds for efficient membership testing.

    A `BoundsSet` represents the union of a collection of
    [`Bounds`][..Bounds]: a value is contained when it falls within *any* of
    them. This matches the way multiple metric-sample bounds work — the value
    must be within at least one of the bounds. On construction the bounds are
    sorted by their lower bound and any overlapping or touching bounds are
    merged, so the stored `bounds` are canonical: sorted and pairwise
    non-overlapping.

    Note:
        This is a domain-specialized set, not a mathematical one: **the empty
        set is the unbounded set**. It contains every value and is falsy, so
        `not bounds_set` reliably means "unbounded" (bounds that together cover
        the whole space also normalize to the empty set). Because of this,
        membership must be tested with `value in bounds_set`, which is
        authoritative — do not reconstruct it by iterating `bounds`, since the
        two disagree for the unbounded set.

    Example:
        ```python
        from frequenz.client.common.metrics import Bounds, BoundsSet

        allowed = BoundsSet(
            bounds=(
                Bounds(lower=1.0, upper=5.0),
                Bounds(lower=3.0, upper=10.0),
                Bounds(lower=15.0, upper=20.0),
            )
        )
        # Overlapping bounds are merged on construction.
        assert allowed.bounds == (
            Bounds(lower=1.0, upper=10.0),
            Bounds(lower=15.0, upper=20.0),
        )
        assert 7.0 in allowed
        assert 12.0 not in allowed
        ```
    """

    bounds: tuple[Bounds, ...] = ()
    """The normalized bounds: sorted by lower bound and pairwise non-overlapping."""

    def __post_init__(self) -> None:
        """Normalize the bounds by sorting and merging overlapping ones."""
        object.__setattr__(self, "bounds", _sort_and_merge_bounds(self.bounds))

    def __contains__(self, item: FloatInt | None) -> bool:
        """Check whether a value is within any bounds of this set.

        Args:
            item: The value to check.

        Returns:
            Whether `item` is within any bounds of this set. `None` is never
                contained, and the empty (unbounded) set contains every value.
        """
        if item is None or (isinstance(item, float) and math.isnan(item)):
            return False
        if not self.bounds:
            return True
        position = bisect.bisect_right(
            self.bounds,
            item,
            key=lambda bound: -math.inf if bound.lower is None else bound.lower,
        )
        index = position - 1
        return index >= 0 and item in self.bounds[index]

    def __bool__(self) -> bool:
        """Return whether this set restricts the accepted values.

        The empty set is the unbounded set: it accepts every value and is
        therefore falsy. A set with any bounds is truthy.

        Returns:
            Whether this set contains any bounds.
        """
        return bool(self.bounds)

    def is_bounded(self) -> bool:
        """Return whether this set restricts the accepted values.

        This is the explicit spelling of this set's truthiness: the empty
        (unbounded) set is not bounded, while a set with any bounds is.

        Returns:
            Whether this set contains any bounds.
        """
        return bool(self)

    def __str__(self) -> str:
        """Return a string representation of this set."""
        if not self.bounds:
            return "[None,None]"
        return "∪".join(str(bound) for bound in self.bounds)


@dataclasses.dataclass(frozen=True, kw_only=True)
class InvalidBoundsSet:
    """A set of metric bounds built from at least one malformed bound.

    When a collection of bounds contains any [`InvalidBounds`][..InvalidBounds]
    it cannot be normalized into a well-formed [`BoundsSet`][..BoundsSet]:
    malformed ranges cannot be meaningfully sorted or merged. This type
    preserves all of the raw bounds — valid and invalid alike — in their
    original order, so callers can inspect exactly what was received without
    accidentally range-checking against broken data.

    Unlike [`BoundsSet`][..BoundsSet], this type intentionally provides no
    membership test: malformed bounds must not be used for range checks. Use a
    semantic accessor, such as `MetricSample.get_bounds_set()`, to receive a
    clear error on invalid data.
    """

    bounds: tuple[Bounds | InvalidBounds, ...] = ()
    """The raw bounds, preserved in their original order without merging."""

    def __str__(self) -> str:
        """Return a compact string representation of this invalid set."""
        inner = "∪".join(str(bound) for bound in self.bounds)
        return f"<invalid:{inner}>"


class InvalidBoundsSetError(InvalidAttributeError):
    """Raised when a semantic accessor sees an invalid bounds set.

    The offending [`InvalidBoundsSet`][..InvalidBoundsSet] is available as the
    [`bounds_set`][.bounds_set] attribute so callers can inspect the raw wire
    data.

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self,
        instance: object,
        attr_name: str,
        bounds_set: InvalidBoundsSet,
        message: str | None = None,
    ) -> None:
        """Initialize this error.

        Args:
            instance: The instance that was being accessed when this error was raised.
            attr_name: The name of the attribute that was being accessed.
            bounds_set: The invalid bounds set instance.
            message: A custom error message. If `None`, a default message mentioning
                the invalid bounds set is used.
        """
        self.bounds_set: InvalidBoundsSet = bounds_set
        """The invalid bounds set that caused this error."""

        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"invalid bounds set {bounds_set} for attribute {attr_name!r} in {instance}"
            ),
        )
