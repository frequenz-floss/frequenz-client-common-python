# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidLifetime`."""

from datetime import datetime

from frequenz.client.common.types import BaseLifetime, InvalidLifetime


def test_is_base_lifetime_subclass() -> None:
    """`InvalidLifetime` is a subclass of `BaseLifetime`."""
    assert issubclass(InvalidLifetime, BaseLifetime)


def test_accepts_invalid_range(present: datetime, future: datetime) -> None:
    """`InvalidLifetime` preserves an end time before its start time."""
    lifetime = InvalidLifetime(start_time=future, end_time=present)

    assert lifetime.start_time is future
    assert lifetime.end_time is present
