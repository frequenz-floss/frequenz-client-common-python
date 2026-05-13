# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of Event from/to protobuf v1alpha8."""

from ._event import event_from_proto, event_to_proto

__all__ = [
    "event_from_proto",
    "event_to_proto",
]
