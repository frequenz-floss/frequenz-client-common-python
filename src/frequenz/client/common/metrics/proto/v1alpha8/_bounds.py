# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Loading of Bounds objects from protobuf messages."""

import warnings

from frequenz.api.common.v1alpha8.metrics import bounds_pb2
from frequenz.core.math import Interval
from typing_extensions import deprecated

from ..._bounds import Bounds


@deprecated(
    "`bounds_from_proto` is deprecated; use `bounds_from_proto2` "
    "(returns `Interval[float | None]`) instead."
)
def bounds_from_proto(message: bounds_pb2.Bounds) -> Bounds:  # noqa: DOC502
    """Create a [`Bounds`][....Bounds] object from a protobuf message.

    Deprecated:
        Use [`bounds_from_proto2`][..bounds_from_proto2] instead.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`Bounds`][....Bounds] object.

    Raises:
        ValueError: If the message is not valid.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return Bounds(
            lower=message.lower if message.HasField("lower") else None,
            upper=message.upper if message.HasField("upper") else None,
        )


def bounds_from_proto2(  # noqa: DOC502
    message: bounds_pb2.Bounds,
) -> Interval[float | None]:
    """Create an [`Interval`][frequenz.core.math.Interval] object from a protobuf message.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`Interval`][frequenz.core.math.Interval] object.

    Raises:
        ValueError: If the message is not valid.
    """
    return Interval(
        message.lower if message.HasField("lower") else None,
        message.upper if message.HasField("upper") else None,
    )


@deprecated(
    "`bounds_from_proto_with_issues` is deprecated; use "
    "`bounds_from_proto_with_issues2` (returns `Interval[float | None] | None`) "
    "instead."
)
def bounds_from_proto_with_issues(
    message: bounds_pb2.Bounds,
    *,
    major_issues: list[str],
    minor_issues: list[str],  # pylint: disable=unused-argument
) -> Bounds | None:  # noqa: DOC502
    """Create a [`Bounds`][....Bounds] object from a protobuf message, collecting issues.

    Deprecated:
        Use [`bounds_from_proto_with_issues2`][..bounds_from_proto_with_issues2]
        instead.

    Args:
        message: The protobuf message to convert.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The corresponding [`Bounds`][....Bounds] object.
    """
    try:
        # `bounds_from_proto` is itself `@deprecated`; suppress its warning so
        # callers see only the outer `bounds_from_proto_with_issues` notice.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            return bounds_from_proto(message)
    except ValueError as exc:
        major_issues.append(str(exc))
        return None


def bounds_from_proto_with_issues2(
    message: bounds_pb2.Bounds,
    *,
    major_issues: list[str],
    minor_issues: list[str],  # pylint: disable=unused-argument
) -> Interval[float | None] | None:  # noqa: DOC502
    """Create an [`Interval`][frequenz.core.math.Interval] object from a protobuf message.

    Collect issues.

    Args:
        message: The protobuf message to convert.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The corresponding [`Interval`][frequenz.core.math.Interval] object.
    """
    try:
        return bounds_from_proto2(message)
    except ValueError as exc:
        major_issues.append(str(exc))
        return None
