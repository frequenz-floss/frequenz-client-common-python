# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Lifetime of an asset."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import assert_never

from .._datetime import InvalidDatetime
from .._exception import InvalidAttributeError


@dataclass(frozen=True, kw_only=True)
class Lifetime:
    """An active operational period of an asset.

    When both [`start_time`][.start_time] and [`end_time`][.end_time] are
    `None`, the lifetime is unbounded and the asset is considered operational
    at every timestamp.

    Both timestamps are well-formed [`datetime`][datetime.datetime] values.
    A lifetime built from a malformed wire timestamp is an
    [`InvalidLifetime`][..InvalidLifetime] instead, so code holding a
    `Lifetime` can compare and order its ends without checking them first.

    Warning:
        The [`end_time`][.end_time] timestamp indicates that the asset has been
        permanently removed from service.

    Note:
        Raises a `ValueError` if [`start_time`][.start_time] is later than the
        [`end_time`][.end_time] timestamp. Use
        [`InvalidLifetime`][..InvalidLifetime] to represent malformed lifetime
        data received from the wire.
    """

    start_time: datetime | None = None
    """The moment when the asset became operationally active.

    If `None`, the asset is considered to be active in any past moment previous to the
    [`end_time`][..end_time].
    """

    end_time: datetime | None = None
    """The moment when the asset's operational activity ceased.

    If `None`, the asset is considered to be active with no plans to be deactivated.
    """

    def __post_init__(self) -> None:
        """Validate this lifetime.

        Raises:
            ValueError: If [`start_time`][..start_time] is later than
                [`end_time`][..end_time].
        """
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.start_time > self.end_time
        ):
            raise ValueError(
                f"Start ({self.start_time}) must be before or equal to end "
                f"({self.end_time})"
            )

    def __str__(self) -> str:
        """Return a compact string representation of this lifetime."""
        start_str = (
            self.start_time.isoformat() if self.start_time is not None else "-inf"
        )
        end_str = self.end_time.isoformat() if self.end_time is not None else "+inf"
        return f"({start_str},{end_str}]"

    def is_operational_at(self, timestamp: datetime) -> bool:
        """Check whether this lifetime is active at a specific timestamp."""
        # Handle start time - it's not active if start_time is in the future
        if self.start_time is not None and self.start_time > timestamp:
            return False
        # Handle end time - active up to and including end_time
        if self.end_time is not None:
            return self.end_time >= timestamp
        # self.end_time is None, and either self.start_time is None or
        # self.start_time <= timestamp, so it is active at this timestamp
        return True

    def is_operational_now(self) -> bool:
        """Whether this lifetime is currently active."""
        return self.is_operational_at(datetime.now(timezone.utc))


@dataclass(frozen=True, kw_only=True)
class InvalidLifetime:
    """An operational lifetime with malformed data received from the wire.

    This class preserves lifetime data that fails the invariants required for
    a well-formed [`Lifetime`][..Lifetime], allowing callers to inspect the raw
    timestamps without accidentally using them for operational checks. Use a
    semantic accessor, such as `ElectricalComponent.get_operational_lifetime()`,
    to receive a clear [`InvalidLifetimeError`][..InvalidLifetimeError].

    Either end may also be an [`InvalidDatetime`][...InvalidDatetime], for a
    wire timestamp that is not a well-formed protobuf `Timestamp`. This class
    enforces no invariants, so it provides no operational checks and no
    accessors: code that reaches an `InvalidLifetime` is already handling
    malformed data and reads the two fields directly.
    """

    start_time: datetime | InvalidDatetime | None = None
    """The moment when the asset became operationally active.

    `None` when the wire did not set it. An
    [`InvalidDatetime`][....InvalidDatetime] when the wire set a malformed
    timestamp.
    """

    end_time: datetime | InvalidDatetime | None = None
    """The moment when the asset's operational activity ceased.

    `None` when the wire did not set it. An
    [`InvalidDatetime`][....InvalidDatetime] when the wire set a malformed
    timestamp.
    """

    def __str__(self) -> str:
        """Return a compact string representation of this invalid lifetime."""
        start_str = _format_time(self.start_time, unset="-inf")
        end_str = _format_time(self.end_time, unset="+inf")
        return f"<invalid:({start_str},{end_str}]>"


def _format_time(value: datetime | InvalidDatetime | None, *, unset: str) -> str:
    """Render one end of an invalid lifetime range.

    Args:
        value: The raw field value.
        unset: The text to use when the field is unset.

    Returns:
        The ISO 8601 representation of a well-formed timestamp, the invalid
            marker of a malformed one, or `unset`.
    """
    match value:
        case None:
            return unset
        case datetime() as valid:
            return valid.isoformat()
        case InvalidDatetime() as invalid:
            return str(invalid)
        case unknown:
            assert_never(unknown)


class InvalidLifetimeError(InvalidAttributeError):
    """Raised when a semantic accessor sees an invalid lifetime.

    The offending [`InvalidLifetime`][..InvalidLifetime] is available as the
    [`lifetime`][.lifetime] attribute so callers can inspect the raw wire data.

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self,
        instance: object,
        attr_name: str,
        lifetime: InvalidLifetime,
        message: str | None = None,
    ) -> None:
        """Initialize this error.

        Args:
            instance: The instance that was being accessed when this error was raised.
            attr_name: The name of the attribute that was being accessed.
            lifetime: The invalid lifetime instance.
            message: A custom error message. If `None`, a default message mentioning
                the invalid lifetime is used.
        """
        self.lifetime: InvalidLifetime = lifetime
        """The invalid lifetime that caused this error."""

        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"invalid lifetime {lifetime} for attribute {attr_name!r} in {instance}"
            ),
        )
