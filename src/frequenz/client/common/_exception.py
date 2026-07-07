# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Common exception types for Frequenz API clients."""


class ClientCommonError(Exception):
    """Base class for all errors raised by frequenz-client-common."""


class InvalidAttributeError(ClientCommonError, ValueError):
    """Raised when a semantic accessor sees an invalid value for a field.

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self, instance: object, attr_name: str, message: str | None = None
    ) -> None:
        """Initialize this error.

        Args:
            instance: The object instance that had an invalid value.
            attr_name: The name of the attribute that had an invalid value.
            message: A custom error message. If `None`, a default message
                mentioning the instance and attribute is used.
        """
        self.instance: object = instance
        """The object instance that had an invalid value."""

        self.attr_name: str = attr_name
        """The name of the attribute that had an invalid value."""

        super().__init__(
            message
            if message is not None
            else f"invalid value for attribute {attr_name!r} in {instance}"
        )


class UnrecognizedEnumValueError(InvalidAttributeError):
    """Raised when a semantic accessor sees an unrecognized protobuf enum value.

    This happens when the server sets an enum value that this version of the
    client does not recognize, as opposed to an unspecified value (see
    [`UnspecifiedEnumValueError`][..UnspecifiedEnumValueError]). The raw
    unrecognized value is available as `value`.

    This is also a ``ValueError`` for convenience.
    """

    def __init__(
        self, instance: object, attr_name: str, value: int, message: str | None = None
    ) -> None:
        """Initialize this error.

        Args:
            instance: The object instance that had the unrecognized value.
            attr_name: The name of the attribute that had the unrecognized value.
            value: The raw protobuf value that was not recognized.
            message: A custom error message. If `None`, a default message
                mentioning the unrecognized value is used.
        """
        self.value: int = value
        """The raw protobuf value that was not recognized."""

        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"unrecognized enum value {value!r} for attribute {attr_name!r} in {instance}"
            ),
        )


class UnspecifiedEnumValueError(InvalidAttributeError):
    """Raised when a semantic accessor sees an unspecified protobuf enum value.

    For a value that is set but not recognized by this client, see
    [`UnrecognizedEnumValueError`][..UnrecognizedEnumValueError].

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self, instance: object, attr_name: str, message: str | None = None
    ) -> None:
        """Initialize this error.

        Args:
            instance: The object instance that had the unspecified value.
            attr_name: The name of the attribute that had the unspecified value.
            message: A custom error message. If `None`, a default message
                mentioning the unspecified value is used.
        """
        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"unspecified enum value for attribute {attr_name!r} in {instance}"
            ),
        )
