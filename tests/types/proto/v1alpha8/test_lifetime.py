# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Lifetime protobuf conversion."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import pytest
from frequenz.api.common.v1alpha8.microgrid import lifetime_pb2
from google.protobuf import timestamp_pb2

from frequenz.client.common.types.proto.v1alpha8 import lifetime_from_proto


@dataclass(frozen=True, kw_only=True)
class _ProtoConversionTestCase:
    """Test case for protobuf conversion."""

    name: str
    """The description of the test case."""

    include_start: bool
    """Whether to include start timestamp."""

    include_end: bool
    """Whether to include end timestamp."""


@pytest.fixture
def now() -> datetime:
    """Fixture to provide current UTC time."""
    return datetime.now(timezone.utc)


@pytest.fixture
def future(now: datetime) -> datetime:
    """Fixture to provide a future time."""
    return now.replace(year=now.year + 1)


@pytest.mark.parametrize(
    "case",
    [
        _ProtoConversionTestCase(
            name="both timestamps", include_start=True, include_end=True
        ),
        _ProtoConversionTestCase(
            name="only start timestamp", include_start=True, include_end=False
        ),
        _ProtoConversionTestCase(
            name="only end timestamp", include_start=False, include_end=True
        ),
        _ProtoConversionTestCase(
            name="no timestamps", include_start=False, include_end=False
        ),
    ],
    ids=lambda case: case.name,
)
def test_from_proto(
    now: datetime, future: datetime, case: _ProtoConversionTestCase
) -> None:
    """Test conversion from protobuf message to Lifetime."""
    now_ts = timestamp_pb2.Timestamp()
    now_ts.FromDatetime(now)

    future_ts = timestamp_pb2.Timestamp()
    future_ts.FromDatetime(future)

    proto_kwargs: dict[str, Any] = {}
    if case.include_start:
        proto_kwargs["start_timestamp"] = now_ts
    if case.include_end:
        proto_kwargs["end_timestamp"] = future_ts

    proto = lifetime_pb2.Lifetime(**proto_kwargs)
    lifetime = lifetime_from_proto(proto)

    if case.include_start:
        assert lifetime.start_time == now
    else:
        assert lifetime.start_time is None

    if case.include_end:
        assert lifetime.end_time == future
    else:
        assert lifetime.end_time is None


def test_from_proto_rejects_start_after_end(now: datetime, future: datetime) -> None:
    """Test conversion rejects protobuf messages with start after end."""
    start_ts = timestamp_pb2.Timestamp()
    start_ts.FromDatetime(future)

    end_ts = timestamp_pb2.Timestamp()
    end_ts.FromDatetime(now)

    proto = lifetime_pb2.Lifetime(
        start_timestamp=start_ts,
        end_timestamp=end_ts,
    )

    with pytest.raises(
        ValueError, match=r"Start \(.*\) must be before or equal to end \(.*\)"
    ):
        lifetime_from_proto(proto)
