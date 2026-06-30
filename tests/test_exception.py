"""Tests for common exceptions."""

import frequenz.client.common
from frequenz.client.common import (
    ClientCommonError,
    UnrecognizedValueError,
    UnspecifiedValueError,
)


def test_exceptions_exported_and_related() -> None:
    """Given exception exports, then their hierarchy and string form are correct."""
    assert issubclass(UnspecifiedValueError, ClientCommonError)
    assert issubclass(UnspecifiedValueError, ValueError)
    assert issubclass(UnrecognizedValueError, ClientCommonError)
    assert issubclass(UnrecognizedValueError, ValueError)
    assert not issubclass(ClientCommonError, ValueError)
    assert str(UnspecifiedValueError("msg")) == "msg"


def test_all_is_sorted_and_exports_unrecognized() -> None:
    """Given the package exports, then __all__ includes the new error and stays sorted."""
    assert "UnrecognizedValueError" in frequenz.client.common.__all__
    assert list(frequenz.client.common.__all__) == sorted(
        frequenz.client.common.__all__
    )


def test_unrecognized_value_error_carries_value() -> None:
    """Given an unrecognized value, then it is stored and catchable as both base types."""
    error = UnrecognizedValueError(999)
    assert error.value == 999
    assert isinstance(error, ValueError)
    assert isinstance(error, ClientCommonError)


def test_unrecognized_value_error_default_message() -> None:
    """Given no explicit message, then the default string contains the raw value."""
    assert "7" in str(UnrecognizedValueError(7))


def test_unrecognized_value_error_custom_message() -> None:
    """Given a custom message, then the string form is exactly that message."""
    assert str(UnrecognizedValueError(7, "msg")) == "msg"
