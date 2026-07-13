# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `MissingFieldError`."""

from frequenz.client.common import (
    ClientCommonError,
    InvalidAttributeError,
    MissingFieldError,
)


def test_inherits_invalid_attribute_error() -> None:
    """`MissingFieldError` inherits `InvalidAttributeError` (and thus `ValueError`)."""
    assert issubclass(MissingFieldError, InvalidAttributeError)
    assert issubclass(MissingFieldError, ClientCommonError)
    assert issubclass(MissingFieldError, ValueError)


def test_stores_instance_and_attr_name() -> None:
    """`MissingFieldError` stores its `instance` and `attr_name` args."""
    instance = object()
    error = MissingFieldError(instance, "field_x")
    assert error.instance is instance
    assert error.attr_name == "field_x"


def test_default_message() -> None:
    """The default message follows the `missing protobuf field ...` template."""
    assert (
        str(MissingFieldError("some-instance", "field_x"))
        == "missing protobuf field 'field_x' in some-instance"
    )


def test_custom_message_replaces_the_default() -> None:
    """A custom message replaces the default entirely."""
    assert str(MissingFieldError("i", "a", "explicit msg")) == "explicit msg"
