# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Streaming event type enum."""

from enum import Enum


class Event(Enum):
    """Enum representing the type of streaming event."""

    UNSPECIFIED = 0
    """Unspecified event type."""

    CREATED = 1
    """Event when a new resource is created."""

    UPDATED = 2
    """Event when an existing resource is updated."""

    DELETED = 3
    """Event when a resource is deleted."""
