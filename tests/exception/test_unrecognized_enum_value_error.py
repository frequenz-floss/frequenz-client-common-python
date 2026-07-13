# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `UnrecognizedEnumValueError`."""

from frequenz.client.common import (
    ClientCommonError,
    InvalidAttributeError,
    UnrecognizedEnumValueError,
)


def test_inherits_invalid_attribute_error() -> None:
    """`UnrecognizedEnumValueError` inherits `InvalidAttributeError` (and thus `ValueError`)."""
    assert issubclass(UnrecognizedEnumValueError, InvalidAttributeError)
    assert issubclass(UnrecognizedEnumValueError, ClientCommonError)
    assert issubclass(UnrecognizedEnumValueError, ValueError)


def test_stores_instance_attr_name_and_value() -> None:
    """`UnrecognizedEnumValueError` stores `instance`, `attr_name`, and `value` as attributes."""
    instance = object()
    error = UnrecognizedEnumValueError(instance, "attr_x", 999)
    assert error.instance is instance
    assert error.attr_name == "attr_x"
    assert error.value == 999


def test_default_message() -> None:
    """The default message follows the `unrecognized enum value ...` template."""
    assert (
        str(UnrecognizedEnumValueError("some-instance", "attr_x", 7))
        == "unrecognized enum value 7 for attribute 'attr_x' in some-instance"
    )


def test_custom_message_replaces_the_default() -> None:
    """A custom message replaces the default entirely."""
    assert (
        str(UnrecognizedEnumValueError("i", "a", 7, "explicit msg")) == "explicit msg"
    )
