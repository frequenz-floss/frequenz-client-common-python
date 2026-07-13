# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Loading of ElectricalComponentConnection objects from protobuf messages."""

import logging
from typing import assert_never

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....types import InvalidLifetime, Lifetime
from .....types.proto.v1alpha8 import lifetime_from_proto
from ... import (
    ElectricalComponentConnection,
    ElectricalComponentConnectionTypes,
    ElectricalComponentId,
    SelfReferencingElectricalComponentConnection,
)

_logger = logging.getLogger(__name__)


def electrical_component_connection_from_proto(
    message: electrical_components_pb2.ElectricalComponentConnection,
) -> ElectricalComponentConnectionTypes:
    """Create an electrical component connection from a protobuf message.

    Args:
        message: The protobuf message to convert.

    Returns:
        One of the concrete connection types.
    """
    major_issues: list[str] = []
    minor_issues: list[str] = []

    connection = electrical_component_connection_from_proto_with_issues(
        message, major_issues=major_issues, minor_issues=minor_issues
    )

    if major_issues:
        _logger.warning(
            "Found issues in electrical component connection: %s | Protobuf message:\n%s",
            ", ".join(major_issues),
            message,
        )
    if minor_issues:
        _logger.debug(
            "Found minor issues in electrical component connection: %s | Protobuf message:\n%s",
            ", ".join(minor_issues),
            message,
        )

    return connection


def electrical_component_connection_from_proto_with_issues(
    message: electrical_components_pb2.ElectricalComponentConnection,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> ElectricalComponentConnectionTypes:
    """Create an electrical component connection from a protobuf message, collecting issues.

    This function is useful when you want to collect issues during the parsing
    of multiple connections, rather than logging them immediately.

    Args:
        message: The protobuf message to parse.
        major_issues: A list to collect major issues found during parsing.
        minor_issues: A list to collect minor issues found during parsing.

    Returns:
        One of the concrete connection types.
    """
    source_component_id = ElectricalComponentId(message.source_electrical_component_id)
    destination_component_id = ElectricalComponentId(
        message.destination_electrical_component_id
    )
    lifetime = _get_operational_lifetime_from_proto(
        message, major_issues=major_issues, minor_issues=minor_issues
    )

    if source_component_id == destination_component_id:
        major_issues.append(
            "self-referencing connection: source and destination are the same "
            f"({source_component_id})",
        )
        return SelfReferencingElectricalComponentConnection(
            source_id=source_component_id,
            destination_id=destination_component_id,
            operational_lifetime=lifetime,
        )

    return ElectricalComponentConnection(
        source_id=source_component_id,
        destination_id=destination_component_id,
        operational_lifetime=lifetime,
    )


def _get_operational_lifetime_from_proto(
    message: electrical_components_pb2.ElectricalComponentConnection,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> Lifetime:
    """Get the operational lifetime from a protobuf message.

    Args:
        message: The protobuf message to extract the operational lifetime from.
        major_issues: A list to collect major issues found during parsing.
        minor_issues: A list to collect minor issues found during parsing.

    Returns:
        The extracted operational lifetime, or an empty lifetime if the protobuf
            field is missing or invalid.
    """
    if message.HasField("operational_lifetime"):
        try:
            lifetime = lifetime_from_proto(message.operational_lifetime)
        except ValueError as exc:
            major_issues.append(
                f"invalid operational lifetime ({exc}), considering it as missing "
                "(i.e. always operational)",
            )
        else:
            match lifetime:
                case Lifetime() as valid:
                    return valid
                case InvalidLifetime(start_time=start, end_time=end):
                    major_issues.append(
                        f"invalid operational lifetime (Start ({start}) must be before "
                        f"or equal to end ({end})), considering it as missing "
                        "(i.e. always operational)",
                    )
                case unknown:
                    assert_never(unknown)
    else:
        minor_issues.append(
            "missing operational lifetime, considering it always operational",
        )
    return Lifetime()
