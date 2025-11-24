# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Helper functions to convert protobuf Timestamp <-> Python datetime."""

from datetime import datetime, timezone
from typing import overload

from google.protobuf import timestamp_pb2


@overload
def datetime_to_proto(dt: datetime) -> timestamp_pb2.Timestamp:
    """Convert a datetime to a protobuf Timestamp.

    Args:
        dt: datetime object to convert

    Returns:
        datetime converted to Timestamp
    """


@overload
def datetime_to_proto(dt: None) -> None:
    """Overload to handle None values.

    Args:
        dt: None

    Returns:
        None
    """


def datetime_to_proto(dt: datetime | None) -> timestamp_pb2.Timestamp | None:
    """Convert a datetime to a protobuf Timestamp.

    Returns None if dt is None.

    Args:
        dt: datetime object to convert

    Returns:
        datetime converted to Timestamp
    """
    if dt is None:
        return None

    ts = timestamp_pb2.Timestamp()
    ts.FromDatetime(dt)
    return ts


def datetime_from_proto(
    ts: timestamp_pb2.Timestamp, tz: timezone = timezone.utc
) -> datetime:
    """Convert a protobuf Timestamp to a datetime.

    Args:
        ts: Timestamp object to convert
        tz: Timezone to use for the datetime

    Returns:
        Timestamp converted to datetime
    """
    # Add microseconds and add nanoseconds converted to microseconds
    microseconds = int(ts.nanos / 1000)
    return datetime.fromtimestamp(ts.seconds + microseconds * 1e-6, tz=tz)
