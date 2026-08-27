# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Loading of ElectricalComponentConnection objects from protobuf messages."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from ...._lifetime import InvalidLifetime, Lifetime
from ....proto.v1alpha8 import lifetime_from_proto
from ... import (
    ElectricalComponentConnection,
    ElectricalComponentConnectionTypes,
    ElectricalComponentId,
    SelfReferencingElectricalComponentConnection,
)


def electrical_component_connection_from_proto(
    message: electrical_components_pb2.ElectricalComponentConnection,
) -> ElectricalComponentConnectionTypes:
    """Create an electrical component connection from a protobuf message.

    A self-referencing connection (same source and destination component) is
    returned as a `SelfReferencingElectricalComponentConnection`, which surfaces
    that malformed state at the type level.

    Args:
        message: The protobuf message to convert.

    Returns:
        One of the concrete connection types.
    """
    source_component_id = ElectricalComponentId(message.source_electrical_component_id)
    destination_component_id = ElectricalComponentId(
        message.destination_electrical_component_id
    )
    lifetime = _get_operational_lifetime_from_proto(message)

    if source_component_id == destination_component_id:
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
) -> Lifetime | InvalidLifetime:
    """Get the operational lifetime from a protobuf message.

    Args:
        message: The protobuf message to extract the operational lifetime from.

    Returns:
        The extracted operational lifetime, an invalid lifetime preserving
            malformed timestamp ordering or a timestamp Python cannot
            represent, or an unbounded lifetime if the field is missing.
    """
    if message.HasField("operational_lifetime"):
        return lifetime_from_proto(message.operational_lifetime)
    return Lifetime()
