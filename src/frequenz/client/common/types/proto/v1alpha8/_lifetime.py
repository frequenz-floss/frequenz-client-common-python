# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Conversion of Lifetime objects from protobuf v1alpha8 messages."""

from frequenz.api.common.v1alpha8.microgrid import lifetime_pb2

from ....proto import datetime_from_proto
from ..._lifetime import InvalidLifetime, Lifetime


def lifetime_from_proto(message: lifetime_pb2.Lifetime) -> Lifetime | InvalidLifetime:
    """Create a lifetime from a protobuf message, preserving malformed data.

    Args:
        message: The protobuf message to convert.

    Returns:
        A [`Lifetime`][....Lifetime] when the timestamps form a valid range, or
            an [`InvalidLifetime`][....InvalidLifetime] preserving malformed
            timestamp ordering. A present but empty protobuf message becomes an
            unbounded `Lifetime()`.
    """
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
    try:
        return Lifetime(start_time=start, end_time=end)
    except ValueError:
        pass
    return InvalidLifetime(start_time=start, end_time=end)
