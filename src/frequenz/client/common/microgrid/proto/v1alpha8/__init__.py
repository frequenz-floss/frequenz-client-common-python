# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of microgrid objects from/to protobuf v1alpha8."""

from ._microgrid import microgrid_from_proto

__all__ = [
    "microgrid_from_proto",
]
