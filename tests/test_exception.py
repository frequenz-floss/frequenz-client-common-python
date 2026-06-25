"""Tests for common exceptions."""

from frequenz.client.common import ClientCommonError, UnspecifiedValueError


def test_exceptions_exported_and_related() -> None:
    """Given exception exports, then their hierarchy and string form are correct."""
    assert issubclass(UnspecifiedValueError, ClientCommonError)
    assert issubclass(UnspecifiedValueError, ValueError)
    assert not issubclass(ClientCommonError, ValueError)
    assert str(UnspecifiedValueError("msg")) == "msg"
