# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the frequenz.client.common.streaming package."""

from frequenz.client.common.streaming import Event
from frequenz.client.common.streaming.proto.v1alpha8 import (
    event_from_proto,
    event_to_proto,
)


def test_event_enum() -> None:
    """Test the Event enum."""
    for event in Event:
        assert event_from_proto(event_to_proto(event)) == event
