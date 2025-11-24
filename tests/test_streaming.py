# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the frequenz.client.common.streaming package."""

from frequenz.client.common.proto import enum_from_proto
from frequenz.client.common.streaming import Event


def test_event_enum() -> None:
    """Test the Event enum."""
    for event in Event:
        assert enum_from_proto(event.value, Event) == event
