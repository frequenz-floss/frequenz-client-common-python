# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidLatitudeError`."""

from frequenz.client.common import ClientCommonError, InvalidAttributeError
from frequenz.client.common.types import InvalidLatitudeError


def test_inherits_invalid_attribute_error() -> None:
    """`InvalidLatitudeError` inherits `InvalidAttributeError` (and thus `ValueError`)."""
    assert issubclass(InvalidLatitudeError, InvalidAttributeError)
    assert issubclass(InvalidLatitudeError, ClientCommonError)
    assert issubclass(InvalidLatitudeError, ValueError)


def test_stores_instance_attr_name_and_value() -> None:
    """`InvalidLatitudeError` stores `instance`, `attr_name`, and `value` as attributes."""
    instance = object()
    error = InvalidLatitudeError(instance, "latitude", 91.0)
    assert error.instance is instance
    assert error.attr_name == "latitude"
    assert error.value == 91.0


def test_default_message() -> None:
    """The default message follows the `invalid latitude ...` template."""
    assert (
        str(InvalidLatitudeError("some-instance", "latitude", 91.0))
        == "invalid latitude 91.0 for attribute 'latitude' in some-instance; "
        "must be in [-90, 90]"
    )


def test_custom_message_replaces_the_default() -> None:
    """A custom message replaces the default entirely."""
    assert str(InvalidLatitudeError("i", "a", 91.0, "explicit msg")) == "explicit msg"
