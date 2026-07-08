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
class Location:
    """A pair of geographical co-ordinates, representing the location of a place."""

    latitude: float | None
    """The latitude, ranging from -90 (South) to 90 (North)."""

    longitude: float | None
    """The longitude, ranging from -180 (West) to 180 (East)."""

    country_code: str | None
    """The country code in ISO 3166-1 Alpha 2 format."""

    def __post_init__(self) -> None:
        """Validate latitude and longitude are within their respective ranges."""
        if self.latitude is not None and not -90.0 <= self.latitude <= 90.0:
            raise ValueError(
                f"latitude must be in the range [-90, 90], got {self.latitude!r}"
            )
        if self.longitude is not None and not -180.0 <= self.longitude <= 180.0:
            raise ValueError(
                f"longitude must be in the range [-180, 180], got {self.longitude!r}"
            )

    def __str__(self) -> str:
        """Return the short string representation of this instance."""
        country = self.country_code or "<NO COUNTRY CODE>"
        lat = f"{self.latitude:.2f}" if self.latitude is not None else "?"
        lon = f"{self.longitude:.2f}" if self.longitude is not None else "?"
        coordinates = ""
        if self.latitude is not None or self.longitude is not None:
            coordinates = f":({lat}, {lon})"
        return f"{country}{coordinates}"
