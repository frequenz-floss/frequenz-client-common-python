# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Geographical co-ordinates of a place."""

from dataclasses import dataclass

from .._exception import InvalidAttributeError


class InvalidLatitudeError(InvalidAttributeError):
    """Raised when a semantic accessor sees a latitude outside `[-90, 90]`.

    A well-formed latitude lies in the closed interval `[-90, 90]`. The raw
    out-of-range float is available as `value`.

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self,
        instance: object,
        attr_name: str,
        value: float,
        message: str | None = None,
    ) -> None:
        """Initialize this error.

        Args:
            instance: The object instance that had the invalid latitude.
            attr_name: The name of the attribute that had the invalid latitude.
            value: The out-of-range latitude value.
            message: A custom error message. If `None`, a default message
                mentioning the invalid value is used.
        """
        self.value: float = value
        """The out-of-range latitude value."""

        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"invalid latitude {value!r} for attribute {attr_name!r} in "
                f"{instance}; must be in [-90, 90]"
            ),
        )


class InvalidLongitudeError(InvalidAttributeError):
    """Raised when a semantic accessor sees a longitude outside `[-180, 180]`.

    A well-formed longitude lies in the closed interval `[-180, 180]`. The raw
    out-of-range float is available as `value`.

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self,
        instance: object,
        attr_name: str,
        value: float,
        message: str | None = None,
    ) -> None:
        """Initialize this error.

        Args:
            instance: The object instance that had the invalid longitude.
            attr_name: The name of the attribute that had the invalid longitude.
            value: The out-of-range longitude value.
            message: A custom error message. If `None`, a default message
                mentioning the invalid value is used.
        """
        self.value: float = value
        """The out-of-range longitude value."""

        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"invalid longitude {value!r} for attribute {attr_name!r} in "
                f"{instance}; must be in [-180, 180]"
            ),
        )


class InvalidCountryCodeError(InvalidAttributeError):
    """Raised when a semantic accessor sees a country code of length other than 2.

    A well-formed country code is an ISO 3166-1 Alpha-2 string, so it must be
    exactly 2 characters long. The raw string is available as `value`.

    This is also a [`ValueError`][] for convenience.
    """

    def __init__(
        self,
        instance: object,
        attr_name: str,
        value: str,
        message: str | None = None,
    ) -> None:
        """Initialize this error.

        Args:
            instance: The object instance that had the invalid country code.
            attr_name: The name of the attribute that had the invalid country code.
            value: The invalid country code string.
            message: A custom error message. If `None`, a default message
                mentioning the invalid value is used.
        """
        self.value: str = value
        """The invalid country code string."""

        super().__init__(
            instance,
            attr_name,
            (
                message
                if message is not None
                else f"invalid country code {value!r} for attribute {attr_name!r} in "
                f"{instance}; must be exactly 2 characters"
            ),
        )


@dataclass(frozen=True, kw_only=True)
class InvalidLatitude:
    """A latitude value that fails the invariant of `[-90, 90]`.

    Wraps a raw wire latitude that fell outside the well-formed range.
    """

    value: float
    """The raw out-of-range latitude value."""

    def __str__(self) -> str:
        """Return a compact representation flagging this as an invalid value."""
        return f"<invalid:{self.value:.2f}>"


@dataclass(frozen=True, kw_only=True)
class InvalidLongitude:
    """A longitude value that fails the invariant of `[-180, 180]`.

    Wraps a raw wire longitude that fell outside the well-formed range.
    """

    value: float
    """The raw out-of-range longitude value."""

    def __str__(self) -> str:
        """Return a compact representation flagging this as an invalid value."""
        return f"<invalid:{self.value:.2f}>"


@dataclass(frozen=True, kw_only=True)
class InvalidCountryCode:
    """A country code that fails the invariant of exactly 2 characters.

    Wraps a raw wire country code that is set but not exactly 2 characters
    long.
    """

    value: str
    """The raw invalid country code."""

    def __str__(self) -> str:
        """Return a compact representation flagging this as an invalid value."""
        return f"<invalid:{self.value!r}>"


@dataclass(frozen=True, kw_only=True)
class Location:
    """A location's information.

    Instances carry the raw wire values of a protobuf `Location` message.
    Invalid or absent field values are expressed in the type system:
    [`latitude`][.latitude] and [`longitude`][.longitude] may be
    [`InvalidLatitude`][..InvalidLatitude] or
    [`InvalidLongitude`][..InvalidLongitude];
    [`country_code`][.country_code] may be
    [`InvalidCountryCode`][..InvalidCountryCode] or `None` when the field
    was unset on the wire. Users can pattern-match on the fields directly.

    Constructing a `Location` with a plain `float` or `str` that violates
    its invariant raises `ValueError`; use the corresponding `Invalid*`
    type to represent an out-of-invariant wire value.
    """

    latitude: float | InvalidLatitude
    """The latitude.

    A plain `float` when well-formed (in `[-90, 90]`); an
    [`InvalidLatitude`][...InvalidLatitude] wrapper when the wire delivered
    an out-of-range value.
    """

    longitude: float | InvalidLongitude
    """The longitude.

    A plain `float` when well-formed (in `[-180, 180]`); an
    [`InvalidLongitude`][...InvalidLongitude] wrapper when the wire
    delivered an out-of-range value.
    """

    country_code: str | InvalidCountryCode | None
    """The country code.

    A plain `str` (exactly 2 characters, ISO 3166-1 Alpha-2) when
    well-formed; an [`InvalidCountryCode`][...InvalidCountryCode] wrapper
    when the wire delivered a non-empty string of a different length;
    `None` when the field was unset on the wire (an empty string on the
    wire is normalized to `None` by the converter).
    """

    def __post_init__(self) -> None:
        """Enforce that plain (unwrapped) fields respect their invariants.

        Raises:
            ValueError: If `latitude` is a plain `float` outside `[-90, 90]`;
                if `longitude` is a plain `float` outside `[-180, 180]`; or
                if `country_code` is a plain `str` not exactly 2 characters
                long. To represent an invalid wire value, wrap it in the
                corresponding `Invalid*` type.
        """
        if not isinstance(self.latitude, InvalidLatitude) and not (
            -90.0 <= self.latitude <= 90.0
        ):
            raise ValueError(
                f"latitude {self.latitude!r} is outside [-90, 90]; wrap in "
                "InvalidLatitude to represent an invalid wire value"
            )
        if not isinstance(self.longitude, InvalidLongitude) and not (
            -180.0 <= self.longitude <= 180.0
        ):
            raise ValueError(
                f"longitude {self.longitude!r} is outside [-180, 180]; wrap "
                "in InvalidLongitude to represent an invalid wire value"
            )
        if (
            self.country_code is not None
            and not isinstance(self.country_code, InvalidCountryCode)
            and len(self.country_code) != 2
        ):
            raise ValueError(
                f"country_code {self.country_code!r} is not exactly 2 "
                "characters; wrap in InvalidCountryCode to represent an "
                "invalid wire value"
            )

    def __str__(self) -> str:
        """Return the short string representation of this instance."""
        country = self.country_code or ""
        lat = (
            str(self.latitude)
            if isinstance(self.latitude, InvalidLatitude)
            else f"{self.latitude:.2f}"
        )
        lon = (
            str(self.longitude)
            if isinstance(self.longitude, InvalidLongitude)
            else f"{self.longitude:.2f}"
        )
        return f"{country}({lat},{lon})"
