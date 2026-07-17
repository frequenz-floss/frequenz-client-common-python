# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of microgrid objects from/to protobuf v1alpha8."""

from ._lifetime import lifetime_from_proto
from ._microgrid import microgrid_from_proto

__all__ = [
    "lifetime_from_proto",
    "microgrid_from_proto",
]
