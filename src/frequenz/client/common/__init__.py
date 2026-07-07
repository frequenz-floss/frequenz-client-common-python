# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Common code and utilities for Frequenz API clients."""

from ._exception import (
    ClientCommonError,
    InvalidAttributeError,
    MissingFieldError,
    UnrecognizedEnumValueError,
    UnspecifiedEnumValueError,
)

__all__ = [
    "ClientCommonError",
    "InvalidAttributeError",
    "MissingFieldError",
    "UnrecognizedEnumValueError",
    "UnspecifiedEnumValueError",
]
