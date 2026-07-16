# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidLongitudeError`."""

from frequenz.client.common import ClientCommonError, InvalidAttributeError
from frequenz.client.common.types import InvalidLongitudeError


def test_inherits_invalid_attribute_error() -> None:
    """`InvalidLongitudeError` inherits `InvalidAttributeError` (and thus `ValueError`)."""
    assert issubclass(InvalidLongitudeError, InvalidAttributeError)
    assert issubclass(InvalidLongitudeError, ClientCommonError)
    assert issubclass(InvalidLongitudeError, ValueError)


def test_stores_instance_attr_name_and_value() -> None:
    """`InvalidLongitudeError` stores `instance`, `attr_name`, and `value` as attributes."""
    instance = object()
    error = InvalidLongitudeError(instance, "longitude", 181.0)
    assert error.instance is instance
    assert error.attr_name == "longitude"
    assert error.value == 181.0


def test_default_message() -> None:
    """The default message follows the `invalid longitude ...` template."""
    assert (
        str(InvalidLongitudeError("some-instance", "longitude", 181.0))
        == "invalid longitude 181.0 for attribute 'longitude' in some-instance; "
        "must be in [-180, 180]"
    )


def test_custom_message_replaces_the_default() -> None:
    """A custom message replaces the default entirely."""
    assert str(InvalidLongitudeError("i", "a", 181.0, "explicit msg")) == "explicit msg"
