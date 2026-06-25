# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Common code and utilities for Frequenz API clients."""

from ._exception import ClientCommonError, UnspecifiedValueError

__all__ = [
    "ClientCommonError",
    "UnspecifiedValueError",
]
