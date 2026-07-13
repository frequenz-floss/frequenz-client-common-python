# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidAttributeError`."""

from frequenz.client.common import ClientCommonError, InvalidAttributeError


def test_is_client_common_and_value_error() -> None:
    """`InvalidAttributeError` is both a `ClientCommonError` and a `ValueError`."""
    assert issubclass(InvalidAttributeError, ClientCommonError)
    assert issubclass(InvalidAttributeError, ValueError)


def test_stores_instance_and_attr_name() -> None:
    """`InvalidAttributeError` stores its `instance` and `attr_name` args as attributes."""
    instance = object()
    error = InvalidAttributeError(instance, "attr_x")
    assert error.instance is instance
    assert error.attr_name == "attr_x"


def test_default_message() -> None:
    """The default message follows the `invalid value for attribute ...` template."""
    assert (
        str(InvalidAttributeError("some-instance", "attr_x"))
        == "invalid value for attribute 'attr_x' in some-instance"
    )


def test_custom_message_replaces_the_default() -> None:
    """A custom message replaces the default entirely."""
    assert str(InvalidAttributeError("i", "a", "explicit msg")) == "explicit msg"
