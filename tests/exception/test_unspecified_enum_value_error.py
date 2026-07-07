# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `UnspecifiedEnumValueError`."""

from frequenz.client.common import (
    ClientCommonError,
    InvalidAttributeError,
    UnspecifiedEnumValueError,
)


def test_inherits_invalid_attribute_error() -> None:
    """`UnspecifiedEnumValueError` inherits `InvalidAttributeError` (and thus `ValueError`)."""
    assert issubclass(UnspecifiedEnumValueError, InvalidAttributeError)
    assert issubclass(UnspecifiedEnumValueError, ClientCommonError)
    assert issubclass(UnspecifiedEnumValueError, ValueError)


def test_stores_instance_and_attr_name() -> None:
    """`UnspecifiedEnumValueError` stores its `instance` and `attr_name` args."""
    instance = object()
    error = UnspecifiedEnumValueError(instance, "attr_x")
    assert error.instance is instance
    assert error.attr_name == "attr_x"


def test_default_message() -> None:
    """The default message follows the `unspecified enum value ...` template."""
    assert (
        str(UnspecifiedEnumValueError("some-instance", "attr_x"))
        == "unspecified enum value for attribute 'attr_x' in some-instance"
    )


def test_custom_message_replaces_the_default() -> None:
    """A custom message replaces the default entirely."""
    assert str(UnspecifiedEnumValueError("i", "a", "explicit msg")) == "explicit msg"
