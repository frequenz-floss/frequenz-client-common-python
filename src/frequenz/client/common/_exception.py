# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Common exception types for Frequenz API clients."""


class ClientCommonError(Exception):
    """Base class for all errors raised by frequenz-client-common."""


class UnrecognizedValueError(ClientCommonError, ValueError):
    """Raised when a semantic accessor sees an unrecognized protobuf value.

    This happens when the server sets an enum value that this version of the
    client does not recognize, as opposed to an unspecified value (see
    [`UnspecifiedValueError`][..UnspecifiedValueError]). The raw
    unrecognized value is available as `value`.

    This is also a ``ValueError`` for convenience.
    """

    def __init__(self, value: int, message: str | None = None) -> None:
        """Initialize this error.

        Args:
            value: The raw protobuf value that was not recognized.
            message: A custom error message. If `None`, a default message
                mentioning the unrecognized value is used.
        """
        self.value: int = value
        super().__init__(
            message if message is not None else f"unrecognized enum value: {value!r}"
        )


class UnspecifiedValueError(ClientCommonError, ValueError):
    """Raised when a semantic accessor sees an unspecified protobuf value.

    For a value that is set but not recognized by this client, see
    [`UnrecognizedValueError`][..UnrecognizedValueError].

    This is also a [`ValueError`][] for convenience.
    """
