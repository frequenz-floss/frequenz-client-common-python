# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for Event to/from protobuf v1alpha8 conversion.

These tests ensure that, for this version, all enum members are correctly matched by
name and value between the Python `Event` enum and the protobuf `Event` enum.
"""

import pytest
from frequenz.api.common.v1alpha8.streaming import event_pb2

from frequenz.client.common.streaming import Event
from frequenz.client.common.streaming.proto.v1alpha8 import (
    event_from_proto,
    event_to_proto,
)

PB_NAMES: list[str] = [m.name for m in event_pb2.Event.DESCRIPTOR.values]

UNKNOWN_PB_VALUE = event_pb2.Event.ValueType(max(m.value for m in Event) + 1)


def test_no_implicit_to_proto_conversion() -> None:
    """Test that protobuf enum values are not implicitly convertible."""
    # mypy should complain about this assignment, so we ignore the type check here.
    # If mypy doesn't find an issue with this conversion, it should complain about
    # the ignore comment having no effect.
    event = list(Event)[0]
    _: event_pb2.Event.ValueType = event.value  # type: ignore[assignment]
    event_pb2.Event.Name(event.value)  # type: ignore[arg-type]


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_proto_enum_matches_enum_name(pb_name: str) -> None:
    """Test that all known protobuf enum names have a matching Event enum member."""
    pb_value = event_pb2.Event.Value(pb_name)
    try:
        event = Event[pb_name.removeprefix("EVENT_")]
        assert event.value == pb_value
    except KeyError:
        pass  # It is OK to have new protobuf enum values not yet in Event.


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_proto_enum_matches_enum_value(pb_name: str) -> None:
    """Test that all known protobuf enum values have a matching Event enum member."""
    pb_value = event_pb2.Event.Value(pb_name)
    try:
        event = Event(pb_value)
        assert event.value == pb_value
    except ValueError:
        pass  # It is OK to have new protobuf enum values not yet in Event.


@pytest.mark.parametrize("event", list(Event), ids=lambda m: m.name)
def test_enum_matches_proto_enum_name(event: Event) -> None:
    """Test that all Event enum members have a matching protobuf enum name."""
    pb_value = event_pb2.Event.ValueType(event.value)
    pb_name = event_pb2.Event.Name(pb_value)
    assert pb_name == f"EVENT_{event.name}"


@pytest.mark.parametrize("event", list(Event), ids=lambda m: m.name)
def test_enum_matches_proto_enum_value(event: Event) -> None:
    """Test that all Event enum members have a matching protobuf enum value."""
    pb_value = event_pb2.Event.Value(f"EVENT_{event.name}")
    assert event.value == pb_value


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_from_proto(pb_name: str) -> None:
    """Test conversion from protobuf returns a matching member or the int."""
    pb_value = event_pb2.Event.Value(pb_name)
    event = event_from_proto(pb_value)
    if pb_value in [m.value for m in Event]:
        assert event is Event(pb_value)
    else:
        assert event == pb_value


def test_from_proto_unknown() -> None:
    """Test conversion from protobuf for yet unknown values return the int."""
    event = event_from_proto(UNKNOWN_PB_VALUE)
    assert isinstance(event, int)
    assert event == UNKNOWN_PB_VALUE


@pytest.mark.parametrize("event", list(Event), ids=lambda m: m.name)
def test_to_proto(event: Event) -> None:
    """Test conversion to protobuf return a matching protobuf value."""
    pb_value = event_to_proto(event)
    assert pb_value == event.value
