# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for Bounds/Interval protobuf conversion."""

from dataclasses import dataclass

import pytest
from frequenz.api.common.v1alpha8.metrics import bounds_pb2

from frequenz.client.common.metrics.proto.v1alpha8 import (
    bounds_from_proto,
    bounds_from_proto2,
    bounds_from_proto_with_issues,
    bounds_from_proto_with_issues2,
)


@dataclass(frozen=True, kw_only=True)
class ProtoConversionTestCase:
    """Test case for protobuf conversion."""

    name: str
    """Description of the test case."""

    has_lower: bool
    """Whether to include lower bound in the protobuf message."""

    has_upper: bool
    """Whether to include upper bound in the protobuf message."""

    lower: float | None
    """The lower bound value to set."""

    upper: float | None
    """The upper bound value to set."""


@pytest.mark.parametrize(
    "case",
    [
        ProtoConversionTestCase(
            name="full",
            has_lower=True,
            has_upper=True,
            lower=-10.0,
            upper=10.0,
        ),
        ProtoConversionTestCase(
            name="no_upper_bound",
            has_lower=True,
            has_upper=False,
            lower=-10.0,
            upper=None,
        ),
        ProtoConversionTestCase(
            name="no_lower_bound",
            has_lower=False,
            has_upper=True,
            lower=None,
            upper=10.0,
        ),
        ProtoConversionTestCase(
            name="no_both_bounds",
            has_lower=False,
            has_upper=False,
            lower=None,
            upper=None,
        ),
    ],
    ids=lambda case: case.name,
)
def test_from_proto(case: ProtoConversionTestCase) -> None:
    """Test conversion from protobuf message to Bounds."""
    proto = bounds_pb2.Bounds()
    if case.has_lower and case.lower is not None:
        proto.lower = case.lower
    if case.has_upper and case.upper is not None:
        proto.upper = case.upper

    bounds = bounds_from_proto(proto)

    assert bounds.lower == case.lower
    assert bounds.upper == case.upper


@pytest.mark.parametrize(
    "case",
    [
        ProtoConversionTestCase(
            name="full",
            has_lower=True,
            has_upper=True,
            lower=-10.0,
            upper=10.0,
        ),
        ProtoConversionTestCase(
            name="no_upper_bound",
            has_lower=True,
            has_upper=False,
            lower=-10.0,
            upper=None,
        ),
        ProtoConversionTestCase(
            name="no_lower_bound",
            has_lower=False,
            has_upper=True,
            lower=None,
            upper=10.0,
        ),
        ProtoConversionTestCase(
            name="no_both_bounds",
            has_lower=False,
            has_upper=False,
            lower=None,
            upper=None,
        ),
    ],
    ids=lambda case: case.name,
)
def test_from_proto2(case: ProtoConversionTestCase) -> None:
    """Test conversion from protobuf message to Interval."""
    proto = bounds_pb2.Bounds()
    if case.has_lower and case.lower is not None:
        proto.lower = case.lower
    if case.has_upper and case.upper is not None:
        proto.upper = case.upper

    bounds = bounds_from_proto2(proto)

    assert bounds.start == case.lower
    assert bounds.end == case.upper


def test_from_proto_with_issues_valid() -> None:
    """Test bounds_from_proto_with_issues with valid bounds."""
    proto = bounds_pb2.Bounds()
    proto.lower = -10.0
    proto.upper = 10.0

    major_issues: list[str] = []
    minor_issues: list[str] = []

    bounds = bounds_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert bounds is not None
    assert bounds.lower == -10.0
    assert bounds.upper == 10.0
    assert not major_issues
    assert not minor_issues


def test_from_proto2_with_issues_valid() -> None:
    """Test bounds_from_proto_with_issues2 with valid bounds."""
    proto = bounds_pb2.Bounds()
    proto.lower = -10.0
    proto.upper = 10.0

    major_issues: list[str] = []
    minor_issues: list[str] = []

    bounds = bounds_from_proto_with_issues2(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert bounds is not None
    assert bounds.start == -10.0
    assert bounds.end == 10.0
    assert not major_issues
    assert not minor_issues


def test_from_proto_with_issues_invalid() -> None:
    """Test bounds_from_proto_with_issues with invalid bounds (lower > upper)."""
    proto = bounds_pb2.Bounds()
    proto.lower = 10.0
    proto.upper = -10.0

    major_issues: list[str] = []
    minor_issues: list[str] = []

    bounds = bounds_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert bounds is None
    assert len(major_issues) == 1
    assert (
        "Lower bound (10.0) must be less than or equal to upper bound (-10.0)"
        in major_issues[0]
    )
    assert not minor_issues


def test_from_proto2_with_issues_invalid() -> None:
    """Test bounds_from_proto_with_issues2 with invalid bounds (start > end)."""
    proto = bounds_pb2.Bounds()
    proto.lower = 10.0
    proto.upper = -10.0

    major_issues: list[str] = []
    minor_issues: list[str] = []

    bounds = bounds_from_proto_with_issues2(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert bounds is None
    assert len(major_issues) == 1
    assert "The start (10.0) can't be bigger than end (-10.0)" in major_issues[0]
    assert not minor_issues
