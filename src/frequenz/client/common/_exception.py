# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Common exception types for Frequenz API clients."""


class ClientCommonError(Exception):
    """Base class for all errors raised by frequenz-client-common."""


class UnspecifiedValueError(ClientCommonError, ValueError):
    """Raised when a semantic accessor sees an unspecified or unknown protobuf value.

    This is also a [`ValueError`][] for convenience.
    """
