# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Supported metrics for microgrid components."""

import enum

from frequenz.api.common.v1alpha8.metrics import metrics_pb2


@enum.unique
class Metric(enum.Enum):
    """List of supported metrics.

    Metric units are as follows:

    * `VOLTAGE`: V (Volts)
    * `CURRENT`: A (Amperes)
    * `POWER_ACTIVE`: W (Watts)
    * `POWER_APPARENT`: VA (Volt-Amperes)
    * `POWER_REACTIVE`: VAr (Volt-Amperes reactive)
    * `ENERGY_ACTIVE`: Wh (Watt-hours)
    * `ENERGY_APPARENT`: VAh (Volt-Ampere hours)
    * `ENERGY_REACTIVE`: VArh (Volt-Ampere reactive hours)
    * `FREQUENCY`: Hz (Hertz)
    * `TEMPERATURE`: °C (Degree Celsius)
    * `BATTERY_SOC_PCT`: % (percentage)
    * `BATTERY_CAPACITY`: Wh (Watt-hours)
    * `FACTOR`: no unit

    Note: AC energy metrics information
        - This energy metric is reported directly from the component, and not a
          result of aggregations in our systems. If a component does not have this
          metric, this field cannot be populated.

        - Components that provide energy metrics reset this metric from time to
          time. This behaviour is specific to each component model. E.g., some
          components reset it on UTC 00:00:00.

        - This energy metric does not specify the start time of the accumulation
          period, and therefore can be inconsistent.
    """

    UNSPECIFIED = metrics_pb2.METRIC_UNSPECIFIED
    """The metric is unspecified (this should not be used)."""

    DC_VOLTAGE = metrics_pb2.METRIC_DC_VOLTAGE
    """The DC voltage."""

    DC_CURRENT = metrics_pb2.METRIC_DC_CURRENT
    """The DC current."""

    DC_POWER = metrics_pb2.METRIC_DC_POWER
    """The DC power."""

    AC_FREQUENCY = metrics_pb2.METRIC_AC_FREQUENCY
    """The AC frequency."""

    AC_VOLTAGE = metrics_pb2.METRIC_AC_VOLTAGE
    """The AC electric potential difference."""

    AC_VOLTAGE_PHASE_1_N = metrics_pb2.METRIC_AC_VOLTAGE_PHASE_1_N
    """The AC electric potential difference between phase 1 and neutral."""

    AC_VOLTAGE_PHASE_2_N = metrics_pb2.METRIC_AC_VOLTAGE_PHASE_2_N
    """The AC electric potential difference between phase 2 and neutral."""

    AC_VOLTAGE_PHASE_3_N = metrics_pb2.METRIC_AC_VOLTAGE_PHASE_3_N
    """The AC electric potential difference between phase 3 and neutral."""

    AC_VOLTAGE_PHASE_1_PHASE_2 = metrics_pb2.METRIC_AC_VOLTAGE_PHASE_1_PHASE_2
    """The AC electric potential difference between phase 1 and phase 2."""

    AC_VOLTAGE_PHASE_2_PHASE_3 = metrics_pb2.METRIC_AC_VOLTAGE_PHASE_2_PHASE_3
    """The AC electric potential difference between phase 2 and phase 3."""

    AC_VOLTAGE_PHASE_3_PHASE_1 = metrics_pb2.METRIC_AC_VOLTAGE_PHASE_3_PHASE_1
    """The AC electric potential difference between phase 3 and phase 1."""

    AC_CURRENT = metrics_pb2.METRIC_AC_CURRENT
    """The AC current."""

    AC_CURRENT_PHASE_1 = metrics_pb2.METRIC_AC_CURRENT_PHASE_1
    """The AC current in phase 1."""

    AC_CURRENT_PHASE_2 = metrics_pb2.METRIC_AC_CURRENT_PHASE_2
    """The AC current in phase 2."""

    AC_CURRENT_PHASE_3 = metrics_pb2.METRIC_AC_CURRENT_PHASE_3
    """The AC current in phase 3."""

    AC_POWER_APPARENT = metrics_pb2.METRIC_AC_POWER_APPARENT
    """The AC apparent power."""

    AC_POWER_APPARENT_PHASE_1 = metrics_pb2.METRIC_AC_POWER_APPARENT_PHASE_1
    """The AC apparent power in phase 1."""

    AC_POWER_APPARENT_PHASE_2 = metrics_pb2.METRIC_AC_POWER_APPARENT_PHASE_2
    """The AC apparent power in phase 2."""

    AC_POWER_APPARENT_PHASE_3 = metrics_pb2.METRIC_AC_POWER_APPARENT_PHASE_3
    """The AC apparent power in phase 3."""

    AC_POWER_ACTIVE = metrics_pb2.METRIC_AC_POWER_ACTIVE
    """The AC active power."""

    AC_POWER_ACTIVE_PHASE_1 = metrics_pb2.METRIC_AC_POWER_ACTIVE_PHASE_1
    """The AC active power in phase 1."""

    AC_POWER_ACTIVE_PHASE_2 = metrics_pb2.METRIC_AC_POWER_ACTIVE_PHASE_2
    """The AC active power in phase 2."""

    AC_POWER_ACTIVE_PHASE_3 = metrics_pb2.METRIC_AC_POWER_ACTIVE_PHASE_3
    """The AC active power in phase 3."""

    AC_POWER_REACTIVE = metrics_pb2.METRIC_AC_POWER_REACTIVE
    """The AC reactive power."""

    AC_POWER_REACTIVE_PHASE_1 = metrics_pb2.METRIC_AC_POWER_REACTIVE_PHASE_1
    """The AC reactive power in phase 1."""

    AC_POWER_REACTIVE_PHASE_2 = metrics_pb2.METRIC_AC_POWER_REACTIVE_PHASE_2
    """The AC reactive power in phase 2."""

    AC_POWER_REACTIVE_PHASE_3 = metrics_pb2.METRIC_AC_POWER_REACTIVE_PHASE_3
    """The AC reactive power in phase 3."""

    AC_POWER_FACTOR = metrics_pb2.METRIC_AC_POWER_FACTOR
    """The AC power factor."""

    AC_POWER_FACTOR_PHASE_1 = metrics_pb2.METRIC_AC_POWER_FACTOR_PHASE_1
    """The AC power factor in phase 1."""

    AC_POWER_FACTOR_PHASE_2 = metrics_pb2.METRIC_AC_POWER_FACTOR_PHASE_2
    """The AC power factor in phase 2."""

    AC_POWER_FACTOR_PHASE_3 = metrics_pb2.METRIC_AC_POWER_FACTOR_PHASE_3
    """The AC power factor in phase 3."""

    AC_ENERGY_APPARENT = metrics_pb2.METRIC_AC_ENERGY_APPARENT
    """The AC apparent energy."""

    AC_ENERGY_APPARENT_PHASE_1 = metrics_pb2.METRIC_AC_ENERGY_APPARENT_PHASE_1
    """The AC apparent energy in phase 1."""

    AC_ENERGY_APPARENT_PHASE_2 = metrics_pb2.METRIC_AC_ENERGY_APPARENT_PHASE_2
    """The AC apparent energy in phase 2."""

    AC_ENERGY_APPARENT_PHASE_3 = metrics_pb2.METRIC_AC_ENERGY_APPARENT_PHASE_3
    """The AC apparent energy in phase 3."""

    AC_ENERGY_ACTIVE = metrics_pb2.METRIC_AC_ENERGY_ACTIVE
    """The AC active energy."""

    AC_ENERGY_ACTIVE_PHASE_1 = metrics_pb2.METRIC_AC_ENERGY_ACTIVE_PHASE_1
    """The AC active energy in phase 1."""

    AC_ENERGY_ACTIVE_PHASE_2 = metrics_pb2.METRIC_AC_ENERGY_ACTIVE_PHASE_2
    """The AC active energy in phase 2."""

    AC_ENERGY_ACTIVE_PHASE_3 = metrics_pb2.METRIC_AC_ENERGY_ACTIVE_PHASE_3
    """The AC active energy in phase 3."""

    AC_ENERGY_ACTIVE_CONSUMED = metrics_pb2.METRIC_AC_ENERGY_ACTIVE_CONSUMED
    """The AC active energy consumed."""

    AC_ENERGY_ACTIVE_CONSUMED_PHASE_1 = (
        metrics_pb2.METRIC_AC_ENERGY_ACTIVE_CONSUMED_PHASE_1
    )
    """The AC active energy consumed in phase 1."""

    AC_ENERGY_ACTIVE_CONSUMED_PHASE_2 = (
        metrics_pb2.METRIC_AC_ENERGY_ACTIVE_CONSUMED_PHASE_2
    )
    """The AC active energy consumed in phase 2."""

    AC_ENERGY_ACTIVE_CONSUMED_PHASE_3 = (
        metrics_pb2.METRIC_AC_ENERGY_ACTIVE_CONSUMED_PHASE_3
    )
    """The AC active energy consumed in phase 3."""

    AC_ENERGY_ACTIVE_DELIVERED = metrics_pb2.METRIC_AC_ENERGY_ACTIVE_DELIVERED
    """The AC active energy delivered."""

    AC_ENERGY_ACTIVE_DELIVERED_PHASE_1 = (
        metrics_pb2.METRIC_AC_ENERGY_ACTIVE_DELIVERED_PHASE_1
    )
    """The AC active energy delivered in phase 1."""

    AC_ENERGY_ACTIVE_DELIVERED_PHASE_2 = (
        metrics_pb2.METRIC_AC_ENERGY_ACTIVE_DELIVERED_PHASE_2
    )
    """The AC active energy delivered in phase 2."""

    AC_ENERGY_ACTIVE_DELIVERED_PHASE_3 = (
        metrics_pb2.METRIC_AC_ENERGY_ACTIVE_DELIVERED_PHASE_3
    )
    """The AC active energy delivered in phase 3."""

    AC_ENERGY_REACTIVE = metrics_pb2.METRIC_AC_ENERGY_REACTIVE
    """The AC reactive energy."""

    AC_ENERGY_REACTIVE_PHASE_1 = metrics_pb2.METRIC_AC_ENERGY_REACTIVE_PHASE_1
    """The AC reactive energy in phase 1."""

    AC_ENERGY_REACTIVE_PHASE_2 = metrics_pb2.METRIC_AC_ENERGY_REACTIVE_PHASE_2
    """The AC reactive energy in phase 2."""

    AC_ENERGY_REACTIVE_PHASE_3 = metrics_pb2.METRIC_AC_ENERGY_REACTIVE_PHASE_3
    """The AC reactive energy in phase 3."""

    AC_TOTAL_HARMONIC_DISTORTION_CURRENT = (
        metrics_pb2.METRIC_AC_TOTAL_HARMONIC_DISTORTION_CURRENT
    )
    """The AC total harmonic distortion current."""

    AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_1 = (
        metrics_pb2.METRIC_AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_1
    )
    """The AC total harmonic distortion current in phase 1."""

    AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_2 = (
        metrics_pb2.METRIC_AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_2
    )
    """The AC total harmonic distortion current in phase 2."""

    AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_3 = (
        metrics_pb2.METRIC_AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_3
    )
    """The AC total harmonic distortion current in phase 3."""

    BATTERY_CAPACITY = metrics_pb2.METRIC_BATTERY_CAPACITY
    """The capacity of the battery."""

    BATTERY_SOC_PCT = metrics_pb2.METRIC_BATTERY_SOC_PCT
    """The state of charge of the battery as a percentage."""

    BATTERY_TEMPERATURE = metrics_pb2.METRIC_BATTERY_TEMPERATURE
    """The temperature of the battery."""

    INVERTER_TEMPERATURE = metrics_pb2.METRIC_INVERTER_TEMPERATURE
    """The temperature of the inverter."""

    INVERTER_TEMPERATURE_CABINET = metrics_pb2.METRIC_INVERTER_TEMPERATURE_CABINET
    """The temperature of the inverter cabinet."""

    INVERTER_TEMPERATURE_HEATSINK = metrics_pb2.METRIC_INVERTER_TEMPERATURE_HEATSINK
    """The temperature of the inverter heatsink."""

    INVERTER_TEMPERATURE_TRANSFORMER = (
        metrics_pb2.METRIC_INVERTER_TEMPERATURE_TRANSFORMER
    )
    """The temperature of the inverter transformer."""

    EV_CHARGER_TEMPERATURE = metrics_pb2.METRIC_EV_CHARGER_TEMPERATURE
    """The temperature of the EV charger."""

    SENSOR_WIND_SPEED = metrics_pb2.METRIC_SENSOR_WIND_SPEED
    """The speed of the wind measured."""

    SENSOR_WIND_DIRECTION = metrics_pb2.METRIC_SENSOR_WIND_DIRECTION
    """The direction of the wind measured."""

    SENSOR_TEMPERATURE = metrics_pb2.METRIC_SENSOR_TEMPERATURE
    """The temperature measured."""

    SENSOR_RELATIVE_HUMIDITY = metrics_pb2.METRIC_SENSOR_RELATIVE_HUMIDITY
    """The relative humidity measured."""

    SENSOR_DEW_POINT = metrics_pb2.METRIC_SENSOR_DEW_POINT
    """The dew point measured."""

    SENSOR_AIR_PRESSURE = metrics_pb2.METRIC_SENSOR_AIR_PRESSURE
    """The air pressure measured."""

    SENSOR_IRRADIANCE = metrics_pb2.METRIC_SENSOR_IRRADIANCE
    """The irradiance measured."""
