# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Loading of Bounds objects from protobuf messages."""

from frequenz.api.common.v1alpha8.metrics import bounds_pb2

from ..._bounds import Bounds, InvalidBounds


def bounds_from_proto(message: bounds_pb2.Bounds) -> Bounds:  # noqa: DOC502
    """Create a [`Bounds`][....Bounds] object from a protobuf message.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`Bounds`][....Bounds] object.

    Raises:
        ValueError: If the message is not valid.
    """
    return Bounds(
        lower=message.lower if message.HasField("lower") else None,
        upper=message.upper if message.HasField("upper") else None,
    )


def bounds_from_proto2(
    message: bounds_pb2.Bounds,
) -> Bounds | InvalidBounds:
    """Create bounds from a protobuf message, preserving malformed data.

    Args:
        message: The protobuf message to convert.

    Returns:
        A [`Bounds`][....Bounds] when the values form a valid range, or an
            [`InvalidBounds`][....InvalidBounds] preserving values that
            violate `lower <= upper`. A present but empty protobuf message
            becomes an unbounded `Bounds()`.
    """
    lower = message.lower if message.HasField("lower") else None
    upper = message.upper if message.HasField("upper") else None
    try:
        return Bounds(lower=lower, upper=upper)
    except ValueError:
        pass
    return InvalidBounds(lower=lower, upper=upper)


def bounds_from_proto_with_issues(
    message: bounds_pb2.Bounds,
    *,
    major_issues: list[str],
    minor_issues: list[str],  # pylint: disable=unused-argument
) -> Bounds | None:  # noqa: DOC502
    """Create a [`Bounds`][....Bounds] object from a protobuf message, collecting issues.

    Args:
        message: The protobuf message to convert.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The corresponding [`Bounds`][....Bounds] object.
    """
    try:
        return bounds_from_proto(message)
    except ValueError as exc:
        major_issues.append(str(exc))
        return None
