# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidBoundsError`."""

from frequenz.client.common import InvalidAttributeError
from frequenz.client.common.metrics import InvalidBounds, InvalidBoundsError


def test_default_message() -> None:
    """`InvalidBoundsError` builds a default message from the invalid bounds."""
    invalid = InvalidBounds(lower=10.0, upper=-10.0)
    error = InvalidBoundsError("some-instance", "config_bounds", invalid)

    assert error.bounds is invalid
    assert (
        str(error) == f"invalid bounds {invalid} for attribute 'config_bounds' "
        "in some-instance"
    )


def test_custom_message() -> None:
    """`InvalidBoundsError` accepts a custom message."""
    invalid = InvalidBounds(lower=10.0, upper=-10.0)
    error = InvalidBoundsError(
        "some-instance",
        "config_bounds",
        invalid,
        message="bad bounds from server",
    )

    assert error.bounds is invalid
    assert str(error) == "bad bounds from server"


def test_is_invalid_attribute_error() -> None:
    """`InvalidBoundsError` is an `InvalidAttributeError`."""
    assert issubclass(InvalidBoundsError, InvalidAttributeError)


def test_is_value_error() -> None:
    """`InvalidBoundsError` is a `ValueError`."""
    assert issubclass(InvalidBoundsError, ValueError)
