# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the InvalidDeliveryAreaError class."""

import pytest

from frequenz.client.common import InvalidAttributeError
from frequenz.client.common.grid import InvalidDeliveryArea, InvalidDeliveryAreaError


def test_default_message() -> None:
    """`InvalidDeliveryAreaError` builds a default message from the invalid area."""
    invalid = InvalidDeliveryArea(code="", code_type=0)
    error = InvalidDeliveryAreaError("some-instance", "delivery_area", invalid)
    assert error.delivery_area is invalid
    assert (
        "invalid delivery area InvalidDeliveryArea(code='', code_type=0) for "
        "attribute 'delivery_area' in some-instance" == str(error)
    )


def test_custom_message() -> None:
    """`InvalidDeliveryAreaError` accepts a custom message."""
    invalid = InvalidDeliveryArea(code="X", code_type=0)
    error = InvalidDeliveryAreaError(
        "some-instance", "attr", invalid, message="bad delivery area from server"
    )
    assert error.delivery_area is invalid
    assert str(error) == "bad delivery area from server"


def test_is_invalid_attribute_error() -> None:
    """`InvalidDeliveryAreaError` is also a `InvalidAttributeError` for convenience."""
    invalid = InvalidDeliveryArea(code="", code_type=0)
    with pytest.raises(InvalidAttributeError):
        raise InvalidDeliveryAreaError("other-instance", "delivery_area", invalid)


def test_is_value_error() -> None:
    """`InvalidDeliveryAreaError` is also a `ValueError` for convenience."""
    invalid = InvalidDeliveryArea(code="", code_type=0)
    with pytest.raises(ValueError):
        raise InvalidDeliveryAreaError("some-instance", "delivery_area", invalid)
