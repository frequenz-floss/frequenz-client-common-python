# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Loading of Sensor objects from protobuf messages."""

from frequenz.api.common.v1alpha8.microgrid.sensors import sensors_pb2

from ...._ids import MicrogridId
from ...._lifetime import InvalidLifetime, Lifetime
from ....proto.v1alpha8._lifetime import lifetime_from_proto
from ..._id import SensorId
from ..._sensor import Sensor


def sensor_from_proto(message: sensors_pb2.Sensor) -> Sensor:
    """Convert a protobuf message to a [`Sensor`][....Sensor] object.

    Malformed input is surfaced through the returned object rather than a side
    channel: a malformed operational lifetime becomes an
    [`InvalidLifetime`][.....InvalidLifetime]. A missing operational lifetime
    becomes an unbounded [`Lifetime`][.....Lifetime].

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`Sensor`][....Sensor] object.
    """
    operational_lifetime: Lifetime | InvalidLifetime = Lifetime()
    if message.HasField("operational_lifetime"):
        operational_lifetime = lifetime_from_proto(message.operational_lifetime)

    return Sensor(
        id=SensorId(message.id),
        microgrid_id=MicrogridId(message.microgrid_id),
        name=message.name,
        model=message.model,
        operational_lifetime=operational_lifetime,
        _allow_construction=True,
    )
