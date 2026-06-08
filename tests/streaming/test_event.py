# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the `Event` enum domain model."""

from frequenz.client.common.streaming import Event


def test_event_members() -> None:
    """Test that Event has the expected members with correct values."""
    assert [m.name for m in Event] == ["UNSPECIFIED", "CREATED", "UPDATED", "DELETED"]
    assert Event.UNSPECIFIED.value == 0
    assert Event.CREATED.value == 1
    assert Event.UPDATED.value == 2
    assert Event.DELETED.value == 3
