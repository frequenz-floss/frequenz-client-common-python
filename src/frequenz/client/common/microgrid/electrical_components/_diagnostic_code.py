# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component diagnostic codes."""

import enum


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

    EXCESS_LEAKAGE_CURRENT = 21
    """Excess leakage current was detected in the component."""

    LOW_SYSTEM_INSULATION_RESISTANCE = 22
    """Low system insulation resistance detected in the component."""

    GROUND_FAULT = 23
    """Ground fault detected in the component."""

    ARC_FAULT = 24
    """Arc fault detected in the component."""

    FAN_FAULT = 25
    """Fan fault detected in the component."""

    HARDWARE_FAULT = 26
    """Hardware fault detected in the component."""

    PROTECTIVE_SHUTDOWN = 27
    """The component performed a protective shutdown."""

    GRID_OVERVOLTAGE = 30
    """The grid voltage is over the maximum rated value."""

    GRID_UNDERVOLTAGE = 31
    """The grid voltage is under the minimum rated value."""

    GRID_OVERFREQUENCY = 32
    """The grid frequency is over the maximum rated value."""

    GRID_UNDERFREQUENCY = 33
    """The grid frequency is under the minimum rated value."""

    GRID_DISCONNECTED = 34
    """The grid is disconnected."""

    GRID_VOLTAGE_IMBALANCE = 35
    """Voltage imbalance between grid phases."""

    GRID_ABNORMAL = 36
    """The grid is in an abnormal condition not covered by other grid-specific diagnostic codes."""

    EV_UNEXPECTED_PILOT_FAILURE = 40
    """Unexpected pilot failure in an electric vehicle (EV) component."""

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

    PV_REVERSAL_POLARITY = 70
    """Reverse polarity condition detected on the photovoltaic (PV) side."""

    PV_UNDERPERFORMANCE = 71
    """The photovoltaic (PV) system is underperforming."""

    PV_FAULT = 72
    """Fault in the photovoltaic (PV) system."""

    PV_REVERSE_CURRENT = 73
    """Reverse current condition detected on the photovoltaic (PV) side."""

    PV_GROUND_FAULT = 74
    """Ground fault detected on the photovoltaic (PV) side."""

    INVERTER_DC_UNDERVOLTAGE = 80
    """The inverter DC bus voltage is under the minimum rated value."""

    INVERTER_DC_OVERVOLTAGE = 81
    """The inverter DC bus voltage is over the maximum rated value."""
