# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Test conversion helper functions."""

from datetime import datetime, timezone

# pylint: disable=no-name-in-module
from google.protobuf.timestamp_pb2 import Timestamp

# pylint: enable=no-name-in-module
from hypothesis import given
from hypothesis import strategies as st

from frequenz.client.common.proto import datetime_from_proto, datetime_to_proto

# Strategy for generating datetime objects
# It requires naive datetime objects because it creates the timezone via a strategy
datetime_strategy = st.datetimes(
    min_value=datetime(1970, 1, 1),  # noqa: DTZ001
    max_value=datetime(9999, 12, 31),  # noqa: DTZ001
    timezones=st.just(timezone.utc),
)

# Strategy for generating Timestamp objects
timestamp_strategy = st.builds(
    Timestamp,
    seconds=st.integers(
        min_value=0,
        max_value=int(datetime(9999, 12, 31, tzinfo=timezone.utc).timestamp()),
    ),
)


@given(datetime_strategy)
def test_to_timestamp_with_datetime(dt: datetime) -> None:
    """Test conversion from datetime to Timestamp."""
    ts = datetime_to_proto(dt)
    assert ts is not None
    converted_back_dt = datetime_from_proto(ts)
    assert dt.tzinfo == converted_back_dt.tzinfo
    assert dt.timestamp() == converted_back_dt.timestamp()


def test_to_timestamp_with_none() -> None:
    """Test that passing None returns None."""
    assert datetime_to_proto(None) is None


@given(timestamp_strategy)
def test_to_datetime(ts: Timestamp) -> None:
    """Test conversion from Timestamp to datetime."""
    dt = datetime_from_proto(ts)
    assert dt is not None
    # Convert back to Timestamp and compare
    converted_back_ts = datetime_to_proto(dt)
    assert ts.seconds == converted_back_ts.seconds


@given(datetime_strategy)
def test_no_none_datetime(dt: datetime) -> None:
    """Test behavior of type hinting."""
    ts: Timestamp = datetime_to_proto(dt)
    dt_none: datetime | None = None

    # The test would fail without the ignore comment as it should.
    ts2: Timestamp = datetime_to_proto(dt_none)  # type: ignore

    assert ts is not None
    assert ts2 is None
