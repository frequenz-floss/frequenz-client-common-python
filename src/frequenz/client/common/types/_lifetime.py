# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Lifetime of an asset."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Self


@dataclass(frozen=True, kw_only=True)
class BaseLifetime:
    """A base class for all lifetimes."""

    start_time: datetime | None = None
    """The moment when the asset became operationally active.

    If `None`, the asset is considered to be active in any past moment previous to the
    [`end_time`][..end_time].
    """

    end_time: datetime | None = None
    """The moment when the asset's operational activity ceased.

    If `None`, the asset is considered to be active with no plans to be deactivated.
    """

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is BaseLifetime:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)


@dataclass(frozen=True, kw_only=True)
class Lifetime(BaseLifetime):
    """An active operational period of an asset.

    When both [`start_time`][.start_time] and [`end_time`][.end_time] are
    `None`, the lifetime is unbounded and the asset is considered operational
    at every timestamp.

    Warning:
        The [`end_time`][.end_time] timestamp indicates that the asset has been
        permanently removed from service.
    """

    def __post_init__(self) -> None:
        """Validate this lifetime."""
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.start_time > self.end_time
        ):
            raise ValueError(
                f"Start ({self.start_time}) must be before or equal to end "
                f"({self.end_time})"
            )

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
