# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `InvalidCountryCodeError`."""

from frequenz.client.common import ClientCommonError, InvalidAttributeError
from frequenz.client.common.types import InvalidCountryCodeError


def test_inherits_invalid_attribute_error() -> None:
    """`InvalidCountryCodeError` inherits `InvalidAttributeError` (and thus `ValueError`)."""
    assert issubclass(InvalidCountryCodeError, InvalidAttributeError)
    assert issubclass(InvalidCountryCodeError, ClientCommonError)
    assert issubclass(InvalidCountryCodeError, ValueError)


def test_stores_instance_attr_name_and_value() -> None:
    """`InvalidCountryCodeError` stores `instance`, `attr_name`, and `value` as attributes."""
    instance = object()
    error = InvalidCountryCodeError(instance, "country_code", "DEU")
    assert error.instance is instance
    assert error.attr_name == "country_code"
    assert error.value == "DEU"


def test_default_message() -> None:
    """The default message follows the `invalid country code ...` template."""
    assert (
        str(InvalidCountryCodeError("some-instance", "country_code", "DEU"))
        == "invalid country code 'DEU' for attribute 'country_code' in some-instance; "
        "must be exactly 2 characters"
    )


def test_custom_message_replaces_the_default() -> None:
    """A custom message replaces the default entirely."""
    assert (
        str(InvalidCountryCodeError("i", "a", "DEU", "explicit msg")) == "explicit msg"
    )
