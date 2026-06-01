# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for Event to/from protobuf v1alpha8 conversion."""

from frequenz.api.common.v1alpha8.streaming import event_pb2

from frequenz.client.common.streaming import Event
from frequenz.client.common.streaming.proto.v1alpha8 import (
    event_from_proto,
    event_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestEventParity(EnumParityTest):
    """Parity tests for the `Event` enum."""

    python_enum = Event
    proto_enum = event_pb2.Event
    name_prefix = "EVENT_"
    from_proto = staticmethod(event_from_proto)
    to_proto = staticmethod(event_to_proto)
