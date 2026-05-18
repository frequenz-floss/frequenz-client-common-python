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
        "Use frequenz.client.common.microgrid.electrical_components.proto."
        "v1alpha8.electrical_component_category_from_proto instead."
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
        return PBElectricalComponentCategory.ValueType(self.value)


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

    def to_proto(self) -> PBElectricalComponentStateCode.ValueType:
        """Convert a ElectricalComponentStateCode enum to protobuf message.

        Returns:
            Enum value corresponding to the protobuf message.
        """
        return PBElectricalComponentStateCode.ValueType(self.value)


@enum.unique
class ElectricalComponentDiagnosticCode(enum.Enum):
    """All diagnostics that can occur across electrical component categories."""

    UNSPECIFIED = 0
    """Default value. No specific error is specified."""

    UNKNOWN = 1
    """The component is reporting an unknown or an undefined error.

    The sender cannot parse the component error to any of the variants below.
    """

    SWITCH_ON_FAULT = 2
    """The component could not be switched on."""

    UNDERVOLTAGE = 3
    """The component is operating under the minimum rated voltage."""

    OVERVOLTAGE = 4
    """The component is operating over the maximum rated voltage."""

    OVERCURRENT = 5
    """The component is drawing more current than the maximum rated value."""

    OVERCURRENT_CHARGING = 6
    """The component's consumption current is over the maximum rated value during charging."""

    OVERCURRENT_DISCHARGING = 7
    """The component's production current is over the maximum rated value during discharging."""

    OVERTEMPERATURE = 8
    """The component is operating over the maximum rated temperature."""

    UNDERTEMPERATURE = 9
    """The component is operating under the minimum rated temperature."""

    HIGH_HUMIDITY = 10
    """The component is exposed to high humidity levels over the maximum rated value."""

    FUSE_ERROR = 11
    """The component's fuse has blown."""

    PRECHARGE_ERROR = 12
    """The component's precharge unit has failed."""

    PLAUSIBILITY_ERROR = 13
    """Plausibility issues within the system involving this component."""

    EV_UNEXPECTED_PILOT_FAILURE = 40
    """Unexpected pilot failure in an electric vehicle (EV) component."""

    FAULT_CURRENT = 14
    """Fault current detected in the component."""

    SHORT_CIRCUIT = 15
    """Short circuit detected in the component."""

    CONFIG_ERROR = 16
    """Configuration error related to the component."""

    ILLEGAL_COMPONENT_STATE_CODE_REQUESTED = 17
    """An illegal state was requested for the component."""

    HARDWARE_INACCESSIBLE = 18
    """The hardware of the component is inaccessible."""

    INTERNAL = 19
    """An internal error within the component."""

    UNAUTHORIZED = 20
    """The component is unauthorized to perform the last requested action."""

    EV_CHARGING_CABLE_UNPLUGGED_FROM_STATION = 41
    """Electric vehicle (EV) cable was abruptly unplugged from the charging station."""

    EV_CHARGING_CABLE_UNPLUGGED_FROM_EV = 42
    """Electric vehicle (EV) cable was abruptly unplugged from the vehicle."""

    EV_CHARGING_CABLE_LOCK_FAILED = 43
    """Electric vehicle (EV) cable lock failure."""

    EV_CHARGING_CABLE_INVALID = 44
    """Invalid electric vehicle (EV) cable."""

    EV_CONSUMER_INCOMPATIBLE = 45
    """Incompatible electric vehicle (EV) plug."""

    BATTERY_IMBALANCE = 50
    """Battery system imbalance detected."""

    BATTERY_LOW_SOH = 51
    """Low state of health (SOH) detected in the battery."""

    BATTERY_BLOCK_ERROR = 52
    """Battery block error detected."""

    BATTERY_CONTROLLER_ERROR = 53
    """Battery controller error detected."""

    BATTERY_RELAY_ERROR = 54
    """Battery relay error detected."""

    BATTERY_CALIBRATION_NEEDED = 56
    """Battery calibration is needed."""

    RELAY_CYCLE_LIMIT_REACHED = 60
    """The relays have been cycled for the maximum number of times."""

    @classmethod
    @deprecated(
        "frequenz.client.common.microgrid.electrical_components."
        "ElectricalComponentDiagnosticCode.from_proto() is deprecated. "
        "Use frequenz.client.common.microgrid.electrical_components.proto."
        "v1alpha8.electrical_component_diagnostic_code_from_proto instead."
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
        return PBElectricalComponentDiagnosticCode.ValueType(self.value)
