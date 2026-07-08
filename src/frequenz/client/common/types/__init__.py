# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Common types."""

from ._lifetime import Lifetime
from ._location import (
    InvalidCountryCodeError,
    InvalidLatitudeError,
    InvalidLongitudeError,
    Location,
)

__all__ = [
    "InvalidCountryCodeError",
    "InvalidLatitudeError",
    "InvalidLongitudeError",
    "Lifetime",
    "Location",
]
