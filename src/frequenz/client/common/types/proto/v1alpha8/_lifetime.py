# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Conversion of Lifetime objects from protobuf v1alpha8 messages."""

from frequenz.api.common.v1alpha8.microgrid import lifetime_pb2

from ....proto import datetime_from_proto
from ..._lifetime import Lifetime


def lifetime_from_proto(
    message: lifetime_pb2.Lifetime,
) -> Lifetime:
    """Create a [`Lifetime`][....Lifetime] from a protobuf message."""
    start = (
        datetime_from_proto(message.start_timestamp)
        if message.HasField("start_timestamp")
        else None
    )
    end = (
        datetime_from_proto(message.end_timestamp)
        if message.HasField("end_timestamp")
        else None
    )
    return Lifetime(start_time=start, end_time=end)
