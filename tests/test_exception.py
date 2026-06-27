"""Tests for common exceptions."""

import frequenz.client.common
from frequenz.client.common import (
    ClientCommonError,
    UnrecognizedEnumValueError,
    UnspecifiedEnumValueError,
)


def test_exceptions_exported_and_related() -> None:
    """Given exception exports, then their hierarchy and string form are correct."""
    assert issubclass(UnspecifiedEnumValueError, ClientCommonError)
    assert issubclass(UnspecifiedEnumValueError, ValueError)
    assert issubclass(UnrecognizedEnumValueError, ClientCommonError)
    assert issubclass(UnrecognizedEnumValueError, ValueError)
    assert not issubclass(ClientCommonError, ValueError)
    assert str(UnspecifiedEnumValueError("msg")) == "msg"


def test_all_is_sorted_and_exports_unrecognized() -> None:
    """Given the package exports, then __all__ includes the new error and stays sorted."""
    assert "UnrecognizedEnumValueError" in frequenz.client.common.__all__
    assert list(frequenz.client.common.__all__) == sorted(
        frequenz.client.common.__all__
    )


def test_unrecognized_enum_value_error_carries_value() -> None:
    """Given an unrecognized value, then it is stored and catchable as both base types."""
    error = UnrecognizedEnumValueError(999)
    assert error.value == 999
    assert isinstance(error, ValueError)
    assert isinstance(error, ClientCommonError)


def test_unrecognized_enum_value_error_default_message() -> None:
    """Given no explicit message, then the default string contains the raw value."""
    assert "7" in str(UnrecognizedEnumValueError(7))


def test_unrecognized_enum_value_error_custom_message() -> None:
    """Given a custom message, then the string form is exactly that message."""
    assert str(UnrecognizedEnumValueError(7, "msg")) == "msg"
