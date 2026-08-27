# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Timestamps that have no Python equivalent."""

from dataclasses import dataclass

from ._exception import InvalidAttributeError


@dataclass(frozen=True, kw_only=True)
class InvalidDatetime:
    """A wire timestamp with no [`datetime`][datetime.datetime] equivalent.

    A protobuf `Timestamp` counts whole [`seconds`][.seconds] since the Unix
    epoch plus a fraction in [`nanos`][.nanos]. Both are plain integers on the
    wire, so a decoded message can carry a value with no meaningful
    [`datetime`][datetime.datetime]:

    - a [`seconds`][.seconds] count outside the years 1 to 9999, which is both
      the range the protobuf specification allows and the range
      [`datetime`][datetime.datetime] covers;
    - a [`nanos`][.nanos] fraction outside `[0, 999999999]`, which the
      protobuf specification does not allow and whose intended meaning is
      therefore unknown.

    This wrapper keeps both raw numbers unchanged so callers can inspect,
    report, or reinterpret what the server sent, instead of losing the message
    to an exception or to a silently repaired value. It is
    protobuf-independent, so it can appear in public wrapper fields.
    """

    seconds: int
    """The raw number of seconds since 1970-01-01T00:00:00Z."""

    nanos: int
    """The raw fraction of a second, in nanoseconds, to add to [`seconds`][..seconds]."""

    def __str__(self) -> str:
        """Return a compact representation flagging this as an invalid value."""
        return f"<invalid:{self.seconds}s{self.nanos:+d}ns>"


class InvalidDatetimeError(InvalidAttributeError):
    """Raised when a semantic accessor sees a timestamp with no `datetime` equivalent.

    The offending [`InvalidDatetime`][..InvalidDatetime] is available as the
    [`datetime`][.datetime] attribute so callers can inspect the raw wire
    data.

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self,
        instance: object,
        attr_name: str,
        datetime: InvalidDatetime,
        message: str | None = None,
    ) -> None:
        """Initialize this error.

        Args:
            instance: The instance that was being accessed when this error was raised.
            attr_name: The name of the attribute that was being accessed.
            datetime: The invalid timestamp instance.
            message: A custom error message. If `None`, a default message
                mentioning the invalid timestamp is used.
        """
        self.datetime: InvalidDatetime = datetime
        """The invalid timestamp that caused this error."""

        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"invalid timestamp {datetime} for attribute {attr_name!r} "
                f"in {instance}"
            ),
        )
