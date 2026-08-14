# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidBoundsSetError`."""

from frequenz.client.common import InvalidAttributeError
from frequenz.client.common.metrics import (
    Bounds,
    InvalidBounds,
    InvalidBoundsSet,
    InvalidBoundsSetError,
)


def test_default_message() -> None:
    """`InvalidBoundsSetError` builds a default message from the invalid set."""
    invalid = InvalidBoundsSet(
        bounds=(Bounds(lower=1.0, upper=5.0), InvalidBounds(lower=10.0, upper=-10.0))
    )
    error = InvalidBoundsSetError("some-instance", "bounds_set", invalid)

    assert error.bounds_set is invalid
    assert (
        str(error) == f"invalid bounds set {invalid} for attribute 'bounds_set' "
        "in some-instance"
    )


def test_custom_message() -> None:
    """`InvalidBoundsSetError` accepts a custom message."""
    invalid = InvalidBoundsSet(bounds=(InvalidBounds(lower=10.0, upper=-10.0),))
    error = InvalidBoundsSetError(
        "some-instance",
        "bounds_set",
        invalid,
        message="bad bounds set from server",
    )

    assert error.bounds_set is invalid
    assert str(error) == "bad bounds set from server"


def test_is_invalid_attribute_error() -> None:
    """`InvalidBoundsSetError` is an `InvalidAttributeError`."""
    assert issubclass(InvalidBoundsSetError, InvalidAttributeError)


def test_is_value_error() -> None:
    """`InvalidBoundsSetError` is a `ValueError`."""
    assert issubclass(InvalidBoundsSetError, ValueError)
