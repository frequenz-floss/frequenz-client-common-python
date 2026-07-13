# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidLifetimeError`."""

from datetime import datetime

from frequenz.client.common import InvalidAttributeError
from frequenz.client.common.types import InvalidLifetime, InvalidLifetimeError


def test_default_message(present: datetime, future: datetime) -> None:
    """`InvalidLifetimeError` builds a default message from the invalid lifetime."""
    invalid = InvalidLifetime(start_time=future, end_time=present)
    error = InvalidLifetimeError("some-instance", "operational_lifetime", invalid)

    assert error.lifetime is invalid
    assert (
        str(error)
        == f"invalid lifetime {invalid!r} for attribute 'operational_lifetime' "
        "in some-instance"
    )


def test_custom_message(present: datetime, future: datetime) -> None:
    """`InvalidLifetimeError` accepts a custom message."""
    invalid = InvalidLifetime(start_time=future, end_time=present)
    error = InvalidLifetimeError(
        "some-instance",
        "operational_lifetime",
        invalid,
        message="bad lifetime from server",
    )

    assert error.lifetime is invalid
    assert str(error) == "bad lifetime from server"


def test_is_invalid_attribute_error() -> None:
    """`InvalidLifetimeError` is an `InvalidAttributeError`."""
    assert issubclass(InvalidLifetimeError, InvalidAttributeError)


def test_is_value_error() -> None:
    """`InvalidLifetimeError` is a `ValueError`."""
    assert issubclass(InvalidLifetimeError, ValueError)
