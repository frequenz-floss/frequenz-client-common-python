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

    def __str__(self) -> str:
        """Return the short string representation of this instance."""
        country = self.country_code or "<NO COUNTRY CODE>"
        lat = f"{self.latitude:.2f}" if self.latitude is not None else "?"
        lon = f"{self.longitude:.2f}" if self.longitude is not None else "?"
        coordinates = ""
        if self.latitude is not None or self.longitude is not None:
            coordinates = f":({lat}, {lon})"
        return f"{country}{coordinates}"
