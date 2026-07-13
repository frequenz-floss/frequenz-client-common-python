# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Common types."""

from ._lifetime import BaseLifetime, InvalidLifetime, Lifetime
from ._location import (
    InvalidCountryCode,
    InvalidCountryCodeError,
    InvalidLatitude,
    InvalidLatitudeError,
    InvalidLongitude,
    InvalidLongitudeError,
    Location,
)

__all__ = [
    "BaseLifetime",
    "InvalidCountryCode",
    "InvalidCountryCodeError",
    "InvalidLatitude",
    "InvalidLatitudeError",
    "InvalidLifetime",
    "InvalidLongitude",
    "InvalidLongitudeError",
    "Lifetime",
    "Location",
]
