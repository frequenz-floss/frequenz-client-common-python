# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `ClientCommonError` and cross-cutting exception-module checks."""

import frequenz.client.common
from frequenz.client.common import ClientCommonError


def test_is_a_plain_exception() -> None:
    """`ClientCommonError` is an `Exception` but deliberately not a `ValueError`."""
    assert issubclass(ClientCommonError, Exception)
    assert not issubclass(ClientCommonError, ValueError)


def test_all_exports_every_exception_class() -> None:
    """Every public exception class is re-exported through the package `__all__`."""
    for name in (
        "ClientCommonError",
        "InvalidAttributeError",
        "MissingFieldError",
        "UnrecognizedEnumValueError",
        "UnspecifiedEnumValueError",
    ):
        assert name in frequenz.client.common.__all__
