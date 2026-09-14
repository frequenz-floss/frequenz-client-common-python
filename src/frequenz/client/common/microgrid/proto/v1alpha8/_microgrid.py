# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Loading of Microgrid objects from protobuf messages."""

from frequenz.api.common.v1alpha8.microgrid import microgrid_pb2

from ....grid import DeliveryArea, InvalidDeliveryArea
from ....grid.proto.v1alpha8 import delivery_area_from_proto2
from ....proto import datetime_from_proto2
from ....types import Location
from ....types.proto.v1alpha8 import location_from_proto
from ..._ids import EnterpriseId, MicrogridId
from ..._microgrid import Microgrid

_ACTIVE_BY_STATUS: dict[int, bool] = {
    microgrid_pb2.MICROGRID_STATUS_ACTIVE: True,
    microgrid_pb2.MICROGRID_STATUS_INACTIVE: False,
}


def _microgrid_status_to_active(value: int) -> bool | int:
    """Map a protobuf microgrid status to an active boolean.

    Args:
        value: A protobuf microgrid-status enum value (a `MICROGRID_STATUS_*`
            constant).

    Returns:
        `True` if active, `False` if inactive, or the raw `int` `value`
            unchanged when the status is unspecified (`0`) or unrecognized.
            This forward-compatible representation lets the higher-level
            accessor distinguish unspecified from unrecognized values.
    """
    return _ACTIVE_BY_STATUS.get(value, value)


def microgrid_from_proto(message: microgrid_pb2.Microgrid) -> Microgrid:
    """Convert a protobuf message to a [`Microgrid`][....Microgrid] object.

    Malformed input is surfaced through the returned object rather than a side
    channel: a malformed delivery area becomes an `InvalidDeliveryArea` and a
    creation time Python cannot represent an `InvalidDatetime`.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`Microgrid`][....Microgrid] object.
    """
    delivery_area: DeliveryArea | InvalidDeliveryArea | None = None
    if message.HasField("delivery_area"):
        delivery_area = delivery_area_from_proto2(message.delivery_area)

    location: Location | None = None
    if message.HasField("location"):
        location = location_from_proto(message.location)

    # The wrapper uses create_time, but the protobuf field remains create_timestamp.
    return Microgrid(
        id=MicrogridId(message.id),
        enterprise_id=EnterpriseId(message.enterprise_id),
        name=message.name,
        delivery_area=delivery_area,
        location=location,
        create_time=datetime_from_proto2(message.create_timestamp),
        _active=_microgrid_status_to_active(message.status),
        _allow_construction=True,
    )
