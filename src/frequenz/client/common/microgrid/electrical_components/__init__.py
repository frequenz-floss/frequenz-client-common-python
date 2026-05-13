# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Defines the electrical components that can be used in a microgrid."""

from __future__ import annotations

import enum
from typing import final

# pylint: disable=no-name-in-module
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentCategory as PBElectricalComponentCategory,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentDiagnosticCode as PBElectricalComponentDiagnosticCode,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentStateCode as PBElectricalComponentStateCode,
)
from frequenz.core.id import BaseId
from typing_extensions import deprecated

# pylint: enable=no-name-in-module


@final
class ElectricalComponentId(BaseId, str_prefix="CID"):
    """A unique identifier for a microgrid electrical component."""


@enum.unique
class ElectricalComponentCategory(enum.Enum):
    """Possible types of microgrid electrical component."""

    UNSPECIFIED = 0
    """An unknown component category.

    Useful for error handling, and marking unknown components in
    a list of components with otherwise known categories.
    """

    GRID_CONNECTION_POINT = 1
    """The point where the local microgrid is connected to the grid."""

    METER = 2
    """A meter, for measuring electrical metrics, e.g., current, voltage, etc."""

    INVERTER = 3
    """An electricity generator, with batteries or solar energy."""

    CONVERTER = 4
    """An electricity converter, e.g., a DC-DC converter."""

    BATTERY = 5
    """A storage system for electrical energy, used by inverters."""

    EV_CHARGER = 6
    """A station for charging electrical vehicles."""

    CRYPTO_MINER = 14
    """A device for mining cryptocurrencies."""

    ELECTROLYZER = 10
    """A device for splitting water into hydrogen and oxygen using electricity."""

    CHP = 9
    """A heat and power combustion plant (CHP stands for combined heat and power)."""

    BREAKER = 7
    """A relay, used for switching electrical circuits on and off."""

    PRECHARGER = 8
    """A precharger, used for preparing electrical circuits for switching on."""

    POWER_TRANSFORMER = 11
    """A transformer, used for changing the voltage of electrical circuits."""

    HVAC = 12
    """A heating, ventilation, and air conditioning (HVAC) system."""

    @classmethod
    @deprecated(
        "frequenz.client.common.microgrid.electrical_components."
        "ElectricalComponentCategory.from_proto() is deprecated. "
        "Use frequenz.client.common.proto.enum_from_proto instead."
    )
    def from_proto(
        cls, component_category: PBElectricalComponentCategory.ValueType
    ) -> ElectricalComponentCategory:
        """Convert a protobuf ElectricalComponentCategory message to enum.

        Args:
            component_category: protobuf enum to convert

        Returns:
            Enum value corresponding to the protobuf message.
        """
        if not any(t.value == component_category for t in ElectricalComponentCategory):
            return ElectricalComponentCategory.UNSPECIFIED
        return cls(component_category)

    def to_proto(self) -> PBElectricalComponentCategory.ValueType:
        """Convert a ElectricalComponentCategory enum to protobuf message.

        Returns:
            Enum value corresponding to the protobuf message.
        """
        return self.value


@enum.unique
class ElectricalComponentStateCode(enum.Enum):
    """All possible states of a microgrid electrical component."""

    UNSPECIFIED = 0
    """Default value when the component state is not explicitly set."""

    UNKNOWN = 1
    """State when the component is in an unknown or undefined condition.

    This is used when the sender is unable to classify the component into any
    other state.
    """

    UNAVAILABLE = 2
    """State when the component is not available for use."""

    SWITCHING_OFF = 3
    """State when the component is in the process of switching off."""

    OFF = 4
    """State when the component has successfully switched off."""

    SWITCHING_ON = 5
    """State when the component is in the process of switching on from an off state."""

    STANDBY = 6
    """State when the component is in standby mode, and not immediately ready for operation."""

    READY = 7
    """State when the component is fully operational and ready for use."""

    CHARGING = 8
    """State when the component is actively consuming energy."""

    DISCHARGING = 9
    """State when the component is actively producing or releasing energy."""

    ERROR = 10
    """State when the component is in an error state and may need attention."""

    EV_CHARGING_CABLE_UNPLUGGED = 20
    """The Electric Vehicle (EV) charging cable is unplugged from the charging station."""

    EV_CHARGING_CABLE_PLUGGED_AT_STATION = 21
    """The EV charging cable is plugged into the charging station."""

    EV_CHARGING_CABLE_PLUGGED_AT_EV = 22
    """The EV charging cable is plugged into the vehicle."""

    EV_CHARGING_CABLE_LOCKED_AT_STATION = 23
    """The EV charging cable is locked at the charging station end, indicating
    readiness for charging."""

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
        "Use frequenz.client.common.proto.enum_from_proto instead."
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

    def to_proto(self) -> PBElectricalComponentStateCode.ValueType:
        """Convert a ElectricalComponentStateCode enum to protobuf message.

        Returns:
            Enum value corresponding to the protobuf message.
        """
        return self.value


@enum.unique
class ElectricalComponentDiagnosticCode(enum.Enum):
    """All diagnostics that can occur across electrical component categories."""

    UNSPECIFIED = 0
    """Default value. No specific error is specified."""

    UNKNOWN = 1
    """The component is reporting an unknown or an undefined error, and the sender
    cannot parse the component error to any of the variants below."""

    SWITCH_ON_FAULT = 2
    """Error indicating that the component could not be switched on."""

    UNDERVOLTAGE = 3
    """Error indicating that the component is operating under the minimum rated
    voltage."""

    OVERVOLTAGE = 4
    """Error indicating that the component is operating over the maximum rated
    voltage."""

    OVERCURRENT = 5
    """Error indicating that the component is drawing more current than the
    maximum rated value."""

    OVERCURRENT_CHARGING = 6
    """Error indicating that the component's consumption current is over the
    maximum rated value during charging."""

    OVERCURRENT_DISCHARGING = 7
    """Error indicating that the component's production current is over the
    maximum rated value during discharging."""

    OVERTEMPERATURE = 8
    """Error indicating that the component is operating over the maximum rated
    temperature."""

    UNDERTEMPERATURE = 9
    """Error indicating that the component is operating under the minimum rated
    temperature."""

    HIGH_HUMIDITY = 10
    """Error indicating that the component is exposed to high humidity levels over
    the maximum rated value."""

    FUSE_ERROR = 11
    """Error indicating that the component's fuse has blown."""

    PRECHARGE_ERROR = 12
    """Error indicating that the component's precharge unit has failed."""

    PLAUSIBILITY_ERROR = 13
    """Error indicating plausibility issues within the system involving this
    component."""

    EV_UNEXPECTED_PILOT_FAILURE = 40
    """Error indicating unexpected pilot failure in an electric vehicle (EV)
    component."""

    FAULT_CURRENT = 14
    """Error indicating fault current detected in the component."""

    SHORT_CIRCUIT = 15
    """Error indicating a short circuit detected in the component."""

    CONFIG_ERROR = 16
    """Error indicating a configuration error related to the component."""

    ILLEGAL_COMPONENT_STATE_CODE_REQUESTED = 17
    """Error indicating an illegal state requested for the component."""

    HARDWARE_INACCESSIBLE = 18
    """Error indicating that the hardware of the component is inaccessible."""

    INTERNAL = 19
    """Error indicating an internal error within the component."""

    UNAUTHORIZED = 20
    """Error indicating that the component is unauthorized to perform the
    last requested action."""

    EV_CHARGING_CABLE_UNPLUGGED_FROM_STATION = 41
    """Error indicating electric vehicle (EV) cable was abruptly unplugged from
    the charging station."""

    EV_CHARGING_CABLE_UNPLUGGED_FROM_EV = 42
    """Error indicating electric vehicle (EV) cable was abruptly unplugged from
    the vehicle."""

    EV_CHARGING_CABLE_LOCK_FAILED = 43
    """Error indicating electric vehicle (EV) cable lock failure."""

    EV_CHARGING_CABLE_INVALID = 44
    """Error indicating an invalid electric vehicle (EV) cable."""

    EV_CONSUMER_INCOMPATIBLE = 45
    """Error indicating an incompatible electric vehicle (EV) plug."""

    BATTERY_IMBALANCE = 50
    """Error indicating a battery system imbalance."""

    BATTERY_LOW_SOH = 51
    """Error indicating a low state of health (SOH) detected in the battery."""

    BATTERY_BLOCK_ERROR = 52
    """Error indicating a battery block error."""

    BATTERY_CONTROLLER_ERROR = 53
    """Error indicating a battery controller error."""

    BATTERY_RELAY_ERROR = 54
    """Error indicating a battery relay error."""

    BATTERY_CALIBRATION_NEEDED = 56
    """Error indicating that battery calibration is needed."""

    RELAY_CYCLE_LIMIT_REACHED = 60
    """Error indicating that the relays have been cycled for the maximum number of
    times."""

    @classmethod
    @deprecated(
        "frequenz.client.common.microgrid.electrical_components."
        "ElectricalComponentDiagnosticCode.from_proto() is deprecated. "
        "Use frequenz.client.common.proto.enum_from_proto instead."
    )
    def from_proto(
        cls, component_error_code: PBElectricalComponentDiagnosticCode.ValueType
    ) -> ElectricalComponentDiagnosticCode:
        """Convert a protobuf ElectricalComponentDiagnosticCode message to enum.

        Args:
            component_error_code: protobuf enum to convert

        Returns:
            Enum value corresponding to the protobuf message.
        """
        if not any(
            c.value == component_error_code for c in ElectricalComponentDiagnosticCode
        ):
            return ElectricalComponentDiagnosticCode.UNSPECIFIED
        return cls(component_error_code)

    def to_proto(self) -> PBElectricalComponentDiagnosticCode.ValueType:
        """Convert a ElectricalComponentDiagnosticCode enum to protobuf message.

        Returns:
            Enum value corresponding to the protobuf message.
        """
        return self.value
