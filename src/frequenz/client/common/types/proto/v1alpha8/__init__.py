# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Common type protobuf v1alpha8 conversions."""

from ._lifetime import lifetime_from_proto
from ._location import location_from_proto

__all__ = [
    "lifetime_from_proto",
    "location_from_proto",
]
