# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of Event to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.streaming import event_pb2

from ....proto import enum_from_proto
from ... import Event


def event_from_proto(message: event_pb2.Event.ValueType) -> Event | int:
    """Convert a protobuf `Event` value to an enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`Event`][frequenz.client.common.streaming.Event] enum member,
            or the raw [`int`][] if the protobuf value is not recognized.
    """
    return enum_from_proto(message, Event)


def event_to_proto(event: Event) -> event_pb2.Event.ValueType:
    """Convert an enum member to a protobuf `Event` value.

    Args:
        event: The [`Event`][frequenz.client.common.streaming.Event] enum member to
            convert.

    Returns:
        The corresponding protobuf `Event` value.
    """
    return event_pb2.Event.ValueType(event.value)
