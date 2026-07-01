# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Conversion of Lifetime objects from protobuf v1alpha8 messages."""

from datetime import datetime

from frequenz.api.common.v1alpha8.microgrid import lifetime_pb2
from frequenz.core.math import Interval

from ....proto import datetime_from_proto


def lifetime_from_proto(
    message: lifetime_pb2.Lifetime,
) -> Interval[datetime | None]:
    """Create an [`Interval[datetime | None]`][frequenz.core.math.Interval] from a protobuf message.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`Interval[datetime | None]`][frequenz.core.math.Interval] object.
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
    return Interval[datetime | None](start, end)
