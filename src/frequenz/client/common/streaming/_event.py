# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Streaming event type enum."""

from enum import Enum

from frequenz.api.common.v1alpha8.streaming import event_pb2


class Event(Enum):
    """Enum representing the type of streaming event."""

    UNSPECIFIED = event_pb2.EVENT_UNSPECIFIED
    """Unspecified event type."""

    CREATED = event_pb2.EVENT_CREATED
    """Event when a new resource is created."""

    UPDATED = event_pb2.EVENT_UPDATED
    """Event when an existing resource is updated."""

    DELETED = event_pb2.EVENT_DELETED
    """Event when a resource is deleted."""
