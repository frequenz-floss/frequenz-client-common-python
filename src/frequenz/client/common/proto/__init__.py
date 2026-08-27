# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""General utilities for converting common types to/from protobuf types."""

from ._enum import enum_from_proto
from ._datetime import datetime_from_proto, datetime_to_proto

__all__ = [
    "datetime_from_proto",
    "datetime_to_proto",
    "enum_from_proto",
]
