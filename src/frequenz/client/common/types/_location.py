# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Geographical co-ordinates of a place."""

from dataclasses import dataclass


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
