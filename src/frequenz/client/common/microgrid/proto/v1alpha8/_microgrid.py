# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Loading of Microgrid objects from protobuf messages."""

import logging

from frequenz.api.common.v1alpha8.microgrid import microgrid_pb2

from ....grid import DeliveryArea
from ....grid.proto.v1alpha8 import delivery_area_from_proto
from ....proto import datetime_from_proto, enum_from_proto
from ....types import Location
from ....types.proto.v1alpha8 import location_from_proto
from ..._ids import EnterpriseId, MicrogridId
from ..._microgrid import Microgrid, MicrogridStatus

_logger = logging.getLogger(__name__)


def microgrid_status_from_proto(
    message: microgrid_pb2.MicrogridStatus.ValueType,
) -> MicrogridStatus | int:
    """Convert a protobuf MicrogridStatus enum value to a MicrogridStatus enum member.

    Args:
        message: A protobuf MicrogridStatus enum value.

    Returns:
        The corresponding MicrogridStatus enum member, or the raw `int` if the protobuf
            value is not recognized.
    """
    return enum_from_proto(message, MicrogridStatus)


def microgrid_status_to_proto(
    status: MicrogridStatus,
) -> microgrid_pb2.MicrogridStatus.ValueType:
    """Convert a MicrogridStatus enum member to a protobuf MicrogridStatus enum value.

    Args:
        status: A MicrogridStatus enum member.

    Returns:
        The corresponding protobuf MicrogridStatus enum value.
    """
    return microgrid_pb2.MicrogridStatus.ValueType(status.value)


def microgrid_from_proto(message: microgrid_pb2.Microgrid) -> Microgrid:
    """Convert a protobuf microgrid message to a microgrid object.

    Args:
        message: The protobuf message to convert.

    Returns:
        The resulting microgrid object.
    """
    major_issues: list[str] = []
    minor_issues: list[str] = []

    delivery_area: DeliveryArea | None = None
    if message.HasField("delivery_area"):
        delivery_area = delivery_area_from_proto(message.delivery_area)
    else:
        major_issues.append("delivery_area is missing")

    location: Location | None = None
    if message.HasField("location"):
        location = location_from_proto(message.location)
    else:
        major_issues.append("location is missing")

    name = message.name or None
    if name is None:
        minor_issues.append("name is empty")

    status = microgrid_status_from_proto(message.status)
    if status is MicrogridStatus.UNSPECIFIED:
        major_issues.append("status is unspecified")
    elif isinstance(status, int):
        major_issues.append("status is unrecognized")

    if major_issues:
        _logger.warning(
            "Found issues in microgrid: %s | Protobuf message:\n%s",
            ", ".join(major_issues),
            message,
        )

    if minor_issues:
        _logger.debug(
            "Found minor issues in microgrid: %s | Protobuf message:\n%s",
            ", ".join(minor_issues),
            message,
        )

    # The wrapper uses create_time, but the protobuf field remains create_timestamp.
    return Microgrid(
        id=MicrogridId(message.id),
        enterprise_id=EnterpriseId(message.enterprise_id),
        name=message.name or None,
        delivery_area=delivery_area,
        location=location,
        status=status,
        create_time=datetime_from_proto(message.create_timestamp),
    )
