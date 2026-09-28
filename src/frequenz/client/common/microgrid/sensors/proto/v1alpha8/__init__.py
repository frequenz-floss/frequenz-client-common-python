# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of microgrid sensor objects from/to protobuf v1alpha8."""

from ._sensor import sensor_from_proto

__all__ = [
    "sensor_from_proto",
]
