# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component diagnostic codes."""

from __future__ import annotations

import enum

# pylint: disable=no-name-in-module
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentDiagnosticCode as PBElectricalComponentDiagnosticCode,
)
from typing_extensions import deprecated

# pylint: enable=no-name-in-module


@enum.unique
class ElectricalComponentDiagnosticCode(enum.Enum):
    """All diagnostics that can occur across electrical component categories."""

    UNSPECIFIED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_UNSPECIFIED
    )
    """Default value. No specific error is specified."""

    UNKNOWN = electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_UNKNOWN
    """The component is reporting an unknown or an undefined error.

    The sender cannot parse the component error to any of the variants below.
    """

    SWITCH_ON_FAULT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_SWITCH_ON_FAULT
    )
    """The component could not be switched on."""

    UNDERVOLTAGE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_UNDERVOLTAGE
    )
    """The component is operating under the minimum rated voltage."""

    OVERVOLTAGE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_OVERVOLTAGE
    )
    """The component is operating over the maximum rated voltage."""

    OVERCURRENT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_OVERCURRENT
    )
    """The component is drawing more current than the maximum rated value."""

    OVERCURRENT_CHARGING = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_OVERCURRENT_CHARGING
    )
    """The component's consumption current is over the maximum rated value during charging."""

    OVERCURRENT_DISCHARGING = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_OVERCURRENT_DISCHARGING
    )
    """The component's production current is over the maximum rated value during discharging."""

    OVERTEMPERATURE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_OVERTEMPERATURE
    )
    """The component is operating over the maximum rated temperature."""

    UNDERTEMPERATURE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_UNDERTEMPERATURE
    )
    """The component is operating under the minimum rated temperature."""

    HIGH_HUMIDITY = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_HIGH_HUMIDITY
    )
    """The component is exposed to high humidity levels over the maximum rated value."""

    FUSE_ERROR = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_FUSE_ERROR
    )
    """The component's fuse has blown."""

    PRECHARGE_ERROR = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_PRECHARGE_ERROR
    )
    """The component's precharge unit has failed."""

    PLAUSIBILITY_ERROR = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_PLAUSIBILITY_ERROR
    )
    """Plausibility issues within the system involving this component."""

    EV_UNEXPECTED_PILOT_FAILURE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_EV_UNEXPECTED_PILOT_FAILURE
    )
    """Unexpected pilot failure in an electric vehicle (EV) component."""

    FAULT_CURRENT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_FAULT_CURRENT
    )
    """Fault current detected in the component."""

    SHORT_CIRCUIT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_SHORT_CIRCUIT
    )
    """Short circuit detected in the component."""

    CONFIG_ERROR = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_CONFIG_ERROR
    )
    """Configuration error related to the component."""

    ILLEGAL_COMPONENT_STATE_CODE_REQUESTED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_ILLEGAL_COMPONENT_STATE_CODE_REQUESTED  # noqa: E501
    )
    """An illegal state was requested for the component."""

    HARDWARE_INACCESSIBLE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_HARDWARE_INACCESSIBLE
    )
    """The hardware of the component is inaccessible."""

    INTERNAL = electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_INTERNAL
    """An internal error within the component."""

    UNAUTHORIZED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_UNAUTHORIZED
    )
    """The component is unauthorized to perform the last requested action."""

    EXCESS_LEAKAGE_CURRENT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_EXCESS_LEAKAGE_CURRENT
    )
    """Excess leakage current was detected in the component."""

    LOW_SYSTEM_INSULATION_RESISTANCE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_LOW_SYSTEM_INSULATION_RESISTANCE  # noqa: E501
    )
    """Low system insulation resistance detected in the component."""

    GROUND_FAULT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_GROUND_FAULT
    )
    """Ground fault detected in the component."""

    ARC_FAULT = electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_ARC_FAULT
    """Arc fault detected in the component."""

    FAN_FAULT = electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_FAN_FAULT
    """Fan fault detected in the component."""

    HARDWARE_FAULT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_HARDWARE_FAULT
    )
    """Hardware fault detected in the component."""

    PROTECTIVE_SHUTDOWN = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_PROTECTIVE_SHUTDOWN
    )
    """The component performed a protective shutdown."""

    GRID_OVERVOLTAGE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_GRID_OVERVOLTAGE
    )
    """The grid voltage is over the maximum rated value."""

    GRID_UNDERVOLTAGE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_GRID_UNDERVOLTAGE
    )
    """The grid voltage is under the minimum rated value."""

    GRID_OVERFREQUENCY = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_GRID_OVERFREQUENCY
    )
    """The grid frequency is over the maximum rated value."""

    GRID_UNDERFREQUENCY = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_GRID_UNDERFREQUENCY
    )
    """The grid frequency is under the minimum rated value."""

    GRID_DISCONNECTED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_GRID_DISCONNECTED
    )
    """The grid is disconnected."""

    GRID_VOLTAGE_IMBALANCE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_GRID_VOLTAGE_IMBALANCE
    )
    """Voltage imbalance between grid phases."""

    GRID_ABNORMAL = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_GRID_ABNORMAL
    )
    """The grid is in an abnormal condition not covered by other grid-specific diagnostic codes."""

    EV_CHARGING_CABLE_UNPLUGGED_FROM_STATION = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_EV_CHARGING_CABLE_UNPLUGGED_FROM_STATION  # noqa: E501
    )
    """Electric vehicle (EV) cable was abruptly unplugged from the charging station."""

    EV_CHARGING_CABLE_UNPLUGGED_FROM_EV = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_EV_CHARGING_CABLE_UNPLUGGED_FROM_EV  # noqa: E501
    )
    """Electric vehicle (EV) cable was abruptly unplugged from the vehicle."""

    EV_CHARGING_CABLE_LOCK_FAILED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_EV_CHARGING_CABLE_LOCK_FAILED
    )
    """Electric vehicle (EV) cable lock failure."""

    EV_CHARGING_CABLE_INVALID = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_EV_CHARGING_CABLE_INVALID
    )
    """Invalid electric vehicle (EV) cable."""

    EV_CONSUMER_INCOMPATIBLE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_EV_CONSUMER_INCOMPATIBLE
    )
    """Incompatible electric vehicle (EV) plug."""

    BATTERY_IMBALANCE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_BATTERY_IMBALANCE
    )
    """Battery system imbalance detected."""

    BATTERY_LOW_SOH = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_BATTERY_LOW_SOH
    )
    """Low state of health (SOH) detected in the battery."""

    BATTERY_BLOCK_ERROR = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_BATTERY_BLOCK_ERROR
    )
    """Battery block error detected."""

    BATTERY_CONTROLLER_ERROR = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_BATTERY_CONTROLLER_ERROR
    )
    """Battery controller error detected."""

    BATTERY_RELAY_ERROR = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_BATTERY_RELAY_ERROR
    )
    """Battery relay error detected."""

    BATTERY_CALIBRATION_NEEDED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_BATTERY_CALIBRATION_NEEDED
    )
    """Battery calibration is needed."""

    RELAY_CYCLE_LIMIT_REACHED = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_RELAY_CYCLE_LIMIT_REACHED
    )
    """The relays have been cycled for the maximum number of times."""

    PV_REVERSAL_POLARITY = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_PV_REVERSAL_POLARITY
    )
    """Reverse polarity condition detected on the photovoltaic (PV) side."""

    PV_UNDERPERFORMANCE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_PV_UNDERPERFORMANCE
    )
    """The photovoltaic (PV) system is underperforming."""

    PV_FAULT = electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_PV_FAULT
    """Fault in the photovoltaic (PV) system."""

    PV_REVERSE_CURRENT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_PV_REVERSE_CURRENT
    )
    """Reverse current condition detected on the photovoltaic (PV) side."""

    PV_GROUND_FAULT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_PV_GROUND_FAULT
    )
    """Ground fault detected on the photovoltaic (PV) side."""

    INVERTER_DC_UNDERVOLTAGE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_INVERTER_DC_UNDERVOLTAGE
    )
    """The inverter DC bus voltage is under the minimum rated value."""

    INVERTER_DC_OVERVOLTAGE = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_INVERTER_DC_OVERVOLTAGE
    )
    """The inverter DC bus voltage is over the maximum rated value."""

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

    @deprecated(
        "frequenz.client.common.microgrid.electrical_components."
        "ElectricalComponentDiagnosticCode.to_proto() is deprecated. "
        "Use frequenz.client.common.microgrid.electrical_components.proto."
        "v1alpha8.electrical_component_diagnostic_code_to_proto instead."
    )
    def to_proto(self) -> PBElectricalComponentDiagnosticCode.ValueType:
        """Convert a ElectricalComponentDiagnosticCode enum to protobuf message.

        Returns:
            Enum value corresponding to the protobuf message.
        """
        return PBElectricalComponentDiagnosticCode.ValueType(self.value)
