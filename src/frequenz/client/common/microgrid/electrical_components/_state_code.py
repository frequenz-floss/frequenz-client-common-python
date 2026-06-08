# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component state codes."""

from __future__ import annotations

import enum

# pylint: disable=no-name-in-module
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentStateCode as PBElectricalComponentStateCode,
)
from typing_extensions import deprecated

# pylint: enable=no-name-in-module


@enum.unique
class ElectricalComponentStateCode(enum.Enum):
    """All possible states of a microgrid electrical component."""

    UNSPECIFIED = 0
    """Default value when the component state is not explicitly set."""

    UNKNOWN = 1
    """The component is in an unknown or undefined condition.

    This is used when the sender is unable to classify the component into any
    other state.
    """

    UNAVAILABLE = 2
    """The component is not available for use."""

    SWITCHING_OFF = 3
    """The component is in the process of switching off."""

    OFF = 4
    """The component has successfully switched off."""

    SWITCHING_ON = 5
    """The component is in the process of switching on from an off state."""

    STANDBY = 6
    """The component is in standby mode, and not immediately ready for operation."""

    READY = 7
    """The component is fully operational and ready for use."""

    CHARGING = 8
    """The component is actively consuming energy."""

    DISCHARGING = 9
    """The component is actively producing or releasing energy."""

    ERROR = 10
    """The component is in an error state and may need attention."""

    EV_CHARGING_CABLE_UNPLUGGED = 20
    """The Electric Vehicle (EV) charging cable is unplugged from the charging station."""

    EV_CHARGING_CABLE_PLUGGED_AT_STATION = 21
    """The EV charging cable is plugged into the charging station."""

    EV_CHARGING_CABLE_PLUGGED_AT_EV = 22
    """The EV charging cable is plugged into the vehicle."""

    EV_CHARGING_CABLE_LOCKED_AT_STATION = 23
    """The EV charging cable is locked at the charging station end, ready for charging."""

    EV_CHARGING_CABLE_LOCKED_AT_EV = 24
    """The EV charging cable is locked at the vehicle end, indicating that charging is active."""

    RELAY_OPEN = 30
    """The relay is in an open state, meaning no current can flow through."""

    RELAY_CLOSED = 31
    """The relay is in a closed state, allowing current to flow."""

    PRECHARGER_OPEN = 40
    """The precharger circuit is open, meaning it's not currently active."""

    PRECHARGER_PRECHARGING = 41
    """The precharger is in a precharging state, preparing the main circuit for activation."""

    PRECHARGER_CLOSED = 42
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
