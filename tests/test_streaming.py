# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the frequenz.client.common.v1alpha8.streaming package."""

from frequenz.client.common.enum_proto import enum_from_proto
from frequenz.client.common.v1alpha8.streaming import Event


def test_event_enum() -> None:
    """Test the Event enum."""
    for event in Event:
        assert enum_from_proto(event.value, Event) == event
