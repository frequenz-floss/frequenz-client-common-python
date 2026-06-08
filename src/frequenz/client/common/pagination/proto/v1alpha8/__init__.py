# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of pagination objects from/to protobuf v1alpha8."""

from ._pagination_info import (
    pagination_info_from_proto,
    pagination_info_to_proto,
)

__all__ = [
    "pagination_info_from_proto",
    "pagination_info_to_proto",
]
