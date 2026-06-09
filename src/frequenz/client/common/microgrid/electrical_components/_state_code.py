# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component state codes."""

from __future__ import annotations

import enum

# pylint: disable=no-name-in-module
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentStateCode as PBElectricalComponentStateCode,
)
from typing_extensions import deprecated

# pylint: enable=no-name-in-module


@enum.unique
class ElectricalComponentStateCode(enum.Enum):
    """All possible states of a microgrid electrical component."""

    UNSPECIFIED = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_UNSPECIFIED
    """Default value when the component state is not explicitly set."""

    UNKNOWN = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_UNKNOWN
    """The component is in an unknown or undefined condition.

    This is used when the sender is unable to classify the component into any
    other state.
    """

    UNAVAILABLE = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_UNAVAILABLE
    """The component is not available for use."""

    SWITCHING_OFF = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_SWITCHING_OFF
    )
    """The component is in the process of switching off."""

    OFF = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_OFF
    """The component has successfully switched off."""

    SWITCHING_ON = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_SWITCHING_ON
    )
    """The component is in the process of switching on from an off state."""

    STANDBY = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_STANDBY
    """The component is in standby mode, and not immediately ready for operation."""

    READY = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_READY
    """The component is fully operational and ready for use."""

    CHARGING = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_CHARGING
    """The component is actively consuming energy."""

    DISCHARGING = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_DISCHARGING
    """The component is actively producing or releasing energy."""

    ERROR = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_ERROR
    """The component is in an error state and may need attention."""

    EV_CHARGING_CABLE_UNPLUGGED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_EV_CHARGING_CABLE_UNPLUGGED
    )
    """The Electric Vehicle (EV) charging cable is unplugged from the charging station."""

    EV_CHARGING_CABLE_PLUGGED_AT_STATION = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_EV_CHARGING_CABLE_PLUGGED_AT_STATION  # noqa: E501
    )
    """The EV charging cable is plugged into the charging station."""

    EV_CHARGING_CABLE_PLUGGED_AT_EV = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_EV_CHARGING_CABLE_PLUGGED_AT_EV
    )
    """The EV charging cable is plugged into the vehicle."""

    EV_CHARGING_CABLE_LOCKED_AT_STATION = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_EV_CHARGING_CABLE_LOCKED_AT_STATION  # noqa: E501
    )
    """The EV charging cable is locked at the charging station end, ready for charging."""

    EV_CHARGING_CABLE_LOCKED_AT_EV = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_EV_CHARGING_CABLE_LOCKED_AT_EV
    )
    """The EV charging cable is locked at the vehicle end, indicating that charging is active."""

    RELAY_OPEN = electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_RELAY_OPEN
    """The relay is in an open state, meaning no current can flow through."""

    RELAY_CLOSED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_RELAY_CLOSED
    )
    """The relay is in a closed state, allowing current to flow."""

    PRECHARGER_OPEN = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_PRECHARGER_OPEN
    )
    """The precharger circuit is open, meaning it's not currently active."""

    PRECHARGER_PRECHARGING = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_PRECHARGER_PRECHARGING
    )
    """The precharger is in a precharging state, preparing the main circuit for activation."""

    PRECHARGER_CLOSED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_STATE_CODE_PRECHARGER_CLOSED
    )
    """The precharger circuit is closed, allowing full current to flow to the main circuit."""

    @classmethod
    @deprecated(
        "frequenz.client.common.microgrid.electrical_components."
        "ElectricalComponentStateCode.from_proto() is deprecated. "
        "Use frequenz.client.common.microgrid.electrical_components.proto."
        "v1alpha8.electrical_component_state_code_from_proto instead."
    )
    def from_proto(
        cls, component_state: PBElectricalComponentStateCode.ValueType
    ) -> ElectricalComponentStateCode:
        """Convert a protobuf ElectricalComponentStateCode message to enum.

        Args:
            component_state: protobuf enum to convert

        Returns:
            Enum value corresponding to the protobuf message.
        """
        if not any(c.value == component_state for c in ElectricalComponentStateCode):
            return ElectricalComponentStateCode.UNSPECIFIED
        return cls(component_state)

    @deprecated(
        "frequenz.client.common.microgrid.electrical_components."
        "ElectricalComponentStateCode.to_proto() is deprecated. "
        "Use frequenz.client.common.microgrid.electrical_components.proto."
        "v1alpha8.electrical_component_state_code_to_proto instead."
    )
    def to_proto(self) -> PBElectricalComponentStateCode.ValueType:
        """Convert a ElectricalComponentStateCode enum to protobuf message.

        Returns:
            Enum value corresponding to the protobuf message.
        """
        return PBElectricalComponentStateCode.ValueType(self.value)
