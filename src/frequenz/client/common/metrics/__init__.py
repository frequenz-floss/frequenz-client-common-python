# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Module to define the metrics used with the common client."""

from __future__ import annotations  # required for constructor type hinting

import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Self

# pylint: disable=no-name-in-module
from frequenz.api.common.v1.metrics.bounds_pb2 import Bounds
from frequenz.api.common.v1.metrics.metric_sample_pb2 import (
    AggregatedMetricSample as PBAggregatedMetricSample,
)
from frequenz.api.common.v1.metrics.metric_sample_pb2 import Metric as PBMetric
from frequenz.api.common.v1.metrics.metric_sample_pb2 import (
    MetricSample as PBMetricSample,
)
from frequenz.api.common.v1.metrics.metric_sample_pb2 import (
    MetricSampleVariant as PBMetricSampleVariant,
)
from frequenz.api.common.v1.metrics.metric_sample_pb2 import (
    SimpleMetricSample as PBSimpleMetricSample,
)
from google.protobuf.timestamp_pb2 import Timestamp

# pylint: enable=no-name-in-module


class Metric(enum.Enum):
    """List of supported metrics."""

    # Default value
    UNSPECIFIED = PBMetric.METRIC_UNSPECIFIED

    # DC electricity metrics
    DC_VOLTAGE = PBMetric.METRIC_DC_VOLTAGE
    DC_CURRENT = PBMetric.METRIC_DC_CURRENT
    DC_POWER = PBMetric.METRIC_DC_POWER

    # General AC electricity metrics
    AC_FREQUENCY = PBMetric.METRIC_AC_FREQUENCY
    AC_VOLTAGE = PBMetric.METRIC_AC_VOLTAGE
    AC_VOLTAGE_PHASE_1 = PBMetric.METRIC_AC_VOLTAGE_PHASE_1
    AC_VOLTAGE_PHASE_2 = PBMetric.METRIC_AC_VOLTAGE_PHASE_2
    AC_VOLTAGE_PHASE_3 = PBMetric.METRIC_AC_VOLTAGE_PHASE_3
    AC_APPARENT_CURRENT = PBMetric.METRIC_AC_APPARENT_CURRENT
    AC_APPARENT_CURRENT_PHASE_1 = PBMetric.METRIC_AC_APPARENT_CURRENT_PHASE_1
    AC_APPARENT_CURRENT_PHASE_2 = PBMetric.METRIC_AC_APPARENT_CURRENT_PHASE_2
    AC_APPARENT_CURRENT_PHASE_3 = PBMetric.METRIC_AC_APPARENT_CURRENT_PHASE_3

    # AC power metrics
    AC_APPARENT_POWER = PBMetric.METRIC_AC_APPARENT_POWER
    AC_APPARENT_POWER_PHASE_1 = PBMetric.METRIC_AC_APPARENT_POWER_PHASE_1
    AC_APPARENT_POWER_PHASE_2 = PBMetric.METRIC_AC_APPARENT_POWER_PHASE_2
    AC_APPARENT_POWER_PHASE_3 = PBMetric.METRIC_AC_APPARENT_POWER_PHASE_3
    AC_ACTIVE_POWER = PBMetric.METRIC_AC_ACTIVE_POWER
    AC_ACTIVE_POWER_PHASE_1 = PBMetric.METRIC_AC_ACTIVE_POWER_PHASE_1
    AC_ACTIVE_POWER_PHASE_2 = PBMetric.METRIC_AC_ACTIVE_POWER_PHASE_2
    AC_ACTIVE_POWER_PHASE_3 = PBMetric.METRIC_AC_ACTIVE_POWER_PHASE_3
    AC_REACTIVE_POWER = PBMetric.METRIC_AC_REACTIVE_POWER
    AC_REACTIVE_POWER_PHASE_1 = PBMetric.METRIC_AC_REACTIVE_POWER_PHASE_1
    AC_REACTIVE_POWER_PHASE_2 = PBMetric.METRIC_AC_REACTIVE_POWER_PHASE_2
    AC_REACTIVE_POWER_PHASE_3 = PBMetric.METRIC_AC_REACTIVE_POWER_PHASE_3

    # AC power factor
    AC_POWER_FACTOR = PBMetric.METRIC_AC_POWER_FACTOR
    AC_POWER_FACTOR_PHASE_1 = PBMetric.METRIC_AC_POWER_FACTOR_PHASE_1
    AC_POWER_FACTOR_PHASE_2 = PBMetric.METRIC_AC_POWER_FACTOR_PHASE_2
    AC_POWER_FACTOR_PHASE_3 = PBMetric.METRIC_AC_POWER_FACTOR_PHASE_3

    # AC energy metrics
    AC_APPARENT_ENERGY = PBMetric.METRIC_AC_APPARENT_ENERGY
    AC_APPARENT_ENERGY_PHASE_1 = PBMetric.METRIC_AC_APPARENT_ENERGY_PHASE_1
    AC_APPARENT_ENERGY_PHASE_2 = PBMetric.METRIC_AC_APPARENT_ENERGY_PHASE_2
    AC_APPARENT_ENERGY_PHASE_3 = PBMetric.METRIC_AC_APPARENT_ENERGY_PHASE_3
    AC_ACTIVE_ENERGY = PBMetric.METRIC_AC_ACTIVE_ENERGY
    AC_ACTIVE_ENERGY_PHASE_1 = PBMetric.METRIC_AC_ACTIVE_ENERGY_PHASE_1
    AC_ACTIVE_ENERGY_PHASE_2 = PBMetric.METRIC_AC_ACTIVE_ENERGY_PHASE_2
    AC_ACTIVE_ENERGY_PHASE_3 = PBMetric.METRIC_AC_ACTIVE_ENERGY_PHASE_3
    AC_ACTIVE_ENERGY_CONSUMED = PBMetric.METRIC_AC_ACTIVE_ENERGY_CONSUMED
    AC_ACTIVE_ENERGY_CONSUMED_PHASE_1 = (
        PBMetric.METRIC_AC_ACTIVE_ENERGY_CONSUMED_PHASE_1
    )
    AC_ACTIVE_ENERGY_CONSUMED_PHASE_2 = (
        PBMetric.METRIC_AC_ACTIVE_ENERGY_CONSUMED_PHASE_2
    )
    AC_ACTIVE_ENERGY_CONSUMED_PHASE_3 = (
        PBMetric.METRIC_AC_ACTIVE_ENERGY_CONSUMED_PHASE_3
    )
    AC_ACTIVE_ENERGY_DELIVERED = PBMetric.METRIC_AC_ACTIVE_ENERGY_DELIVERED
    AC_ACTIVE_ENERGY_DELIVERED_PHASE_1 = (
        PBMetric.METRIC_AC_ACTIVE_ENERGY_DELIVERED_PHASE_1
    )
    AC_ACTIVE_ENERGY_DELIVERED_PHASE_2 = (
        PBMetric.METRIC_AC_ACTIVE_ENERGY_DELIVERED_PHASE_2
    )
    AC_ACTIVE_ENERGY_DELIVERED_PHASE_3 = (
        PBMetric.METRIC_AC_ACTIVE_ENERGY_DELIVERED_PHASE_3
    )
    AC_REACTIVE_ENERGY = PBMetric.METRIC_AC_REACTIVE_ENERGY
    AC_REACTIVE_ENERGY_PHASE_1 = PBMetric.METRIC_AC_REACTIVE_ENERGY_PHASE_1
    AC_REACTIVE_ENERGY_PHASE_2 = PBMetric.METRIC_AC_REACTIVE_ENERGY_PHASE_2
    AC_REACTIVE_ENERGY_PHASE_3 = PBMetric.METRIC_AC_REACTIVE_ENERGY_PHASE_3

    # AC harmonics
    AC_THD_CURRENT = PBMetric.METRIC_AC_THD_CURRENT
    AC_THD_CURRENT_PHASE_1 = PBMetric.METRIC_AC_THD_CURRENT_PHASE_1
    AC_THD_CURRENT_PHASE_2 = PBMetric.METRIC_AC_THD_CURRENT_PHASE_2
    AC_THD_CURRENT_PHASE_3 = PBMetric.METRIC_AC_THD_CURRENT_PHASE_3

    # General BMS metrics
    BATTERY_CAPACITY = PBMetric.METRIC_BATTERY_CAPACITY
    BATTERY_SOC_PCT = PBMetric.METRIC_BATTERY_SOC_PCT
    BATTERY_TEMPERATURE = PBMetric.METRIC_BATTERY_TEMPERATURE

    # General inverter metrics
    INVERTER_TEMPERATURE = PBMetric.METRIC_INVERTER_TEMPERATURE
    INVERTER_TEMPERATURE_CABINET = PBMetric.METRIC_INVERTER_TEMPERATURE_CABINET
    INVERTER_TEMPERATURE_HEATSINK = PBMetric.METRIC_INVERTER_TEMPERATURE_HEATSINK
    INVERTER_TEMPERATURE_TRANSFORMER = PBMetric.METRIC_INVERTER_TEMPERATURE_TRANSFORMER

    # EV charging station metrics
    EV_CHARGER_TEMPERATURE = PBMetric.METRIC_EV_CHARGER_TEMPERATURE

    # General sensor metrics
    SENSOR_WIND_SPEED = PBMetric.METRIC_SENSOR_WIND_SPEED
    SENSOR_WIND_DIRECTION = PBMetric.METRIC_SENSOR_WIND_DIRECTION
    SENSOR_TEMPERATURE = PBMetric.METRIC_SENSOR_TEMPERATURE
    SENSOR_RELATIVE_HUMIDITY = PBMetric.METRIC_SENSOR_RELATIVE_HUMIDITY
    SENSOR_DEW_POINT = PBMetric.METRIC_SENSOR_DEW_POINT
    SENSOR_AIR_PRESSURE = PBMetric.METRIC_SENSOR_AIR_PRESSURE
    SENSOR_IRRADIANCE = PBMetric.METRIC_SENSOR_IRRADIANCE

    @classmethod
    def from_proto(cls, metric: PBMetric.ValueType) -> Metric:
        """Convert a protobuf Metric value to Metric enum.

        Args:
            metric: Metric to convert.
        Returns:
            Enum value corresponding to the protobuf message.
        """
        if not any(m.value == metric for m in cls):
            return Metric.UNSPECIFIED

        return cls(metric)

    def to_proto(self) -> PBMetric.ValueType:
        """Convert a Metric object to protobuf Metric.

        Returns:
            Protobuf message corresponding to the Metric object.
        """
        return self.value


@dataclass(frozen=True, kw_only=True)
class SimpleMetricSample:
    """
    Represents a single sample of a specific metric.

    The value of which is either measured or derived at a particular time.
    """

    value: float
    """The value of the metric, which could be either measured or derived."""

    @classmethod
    def from_proto(cls, simple_metric_sample: PBSimpleMetricSample) -> Self:
        """Convert a protobuf SimpleMetricSample to SimpleMetricSample object.

        Args:
            simple_metric_sample: SimpleMetricSample to convert.
        Returns:
            SimpleMetricSample object corresponding to the protobuf message.
        """
        return cls(
            value=simple_metric_sample.value,
        )

    def to_proto(self) -> PBSimpleMetricSample:
        """Convert a SimpleMetricSample object to protobuf SimpleMetricSample.

        Returns:
            Protobuf message corresponding to the SimpleMetricSample object.
        """
        return PBSimpleMetricSample(
            value=self.value,
        )


@dataclass(frozen=True, kw_only=True)
class AggregatedMetricSample:
    """
    Encapsulates derived statistical summaries of a single metric.

    The message allows for the reporting of statistical summaries —
    minimum, maximum, and average values - as well as the complete
    list of individual samples if available.

    This message represents derived metrics and contains fields for
    statistical summaries—minimum, maximum, and average values.
    Individual measurements are optional, accommodating scenarios
    where only subsets of this information are available.
    """

    avg_value: float
    """The derived average value of the metric."""

    min_value: float
    """The minimum measured value of the metric."""

    max_value: float
    """The maximum measured value of the metric."""

    raw_values: list[float]
    """Optional array of all the raw individual values."""

    @classmethod
    def from_proto(cls, aggregated_metric_sample: PBAggregatedMetricSample) -> Self:
        """Convert proto AggregatedMetricSample to AggregatedMetricSample obj.

        Args:
            aggregated_metric_sample: AggregatedMetricSample to convert.
        Returns:
            AggregatedMetricSample object corresponding to the protobuf
            message.
        """
        return cls(
            avg_value=aggregated_metric_sample.avg_value,
            min_value=aggregated_metric_sample.min_value,
            max_value=aggregated_metric_sample.max_value,
            raw_values=list(aggregated_metric_sample.raw_values),
        )

    def to_proto(self) -> PBAggregatedMetricSample:
        """Convert AggregatedMetricSample obj to proto AggregatedMetricSample.

        Returns:
            Protobuf message corresponding to the AggregatedMetricSample
            object.
        """
        return PBAggregatedMetricSample(
            avg_value=self.avg_value,
            min_value=self.min_value,
            max_value=self.max_value,
            raw_values=list(self.raw_values),
        )


@dataclass(frozen=True, kw_only=True)
class MetricSampleVariant:
    """
    MetricSampleVariant serves as a union type.

    It can encapsulate either a `SimpleMetricSample` or an
    `AggregatedMetricSample`.

    This is designed to offer flexibility in capturing different
    granularities of metric samples—either a simple single-point
    measurement or an aggregated set of measurements for a metric.

    A `MetricSampleVariant` can hold either a `SimpleMetricSample`
    or an `AggregatedMetricSample`, but not both simultaneously.
    Setting one will nullify the other.
    """

    simple_metric: SimpleMetricSample | None = None
    """Single sample of a specific metric, which is measured or derived."""

    aggregated_metric: AggregatedMetricSample | None = None
    """Encapsulates derived statistical summaries of a single metric."""

    @classmethod
    def from_proto(cls, metric_sample_variant: PBMetricSampleVariant) -> Self:
        """Convert proto MetricSampleVariant to MetricSampleVariant object.

        Args:
            metric_sample_variant: MetricSampleVariant to convert.

        Returns:
            MetricSampleVariant object corresponding to the protobuf message.
        """
        return cls(
            simple_metric=SimpleMetricSample.from_proto(
                metric_sample_variant.simple_metric
            ),
            aggregated_metric=AggregatedMetricSample.from_proto(
                metric_sample_variant.aggregated_metric
            ),
        )

    def to_proto(self) -> PBMetricSampleVariant:
        """Convert MetricSampleVariant object to proto MetricSampleVariant.

        Returns:
            Protobuf message corresponding to the MetricSampleVariant object.
        """
        metric_sample_variant = PBMetricSampleVariant()

        if self.simple_metric is not None:
            metric_sample_variant.simple_metric.CopyFrom(self.simple_metric.to_proto())
        if self.aggregated_metric is not None:
            metric_sample_variant.aggregated_metric.CopyFrom(
                self.aggregated_metric.to_proto()
            )
        return metric_sample_variant


@dataclass(frozen=True, kw_only=True)
class MetricSample:
    """
    Representation of a sampled metric along with its value.

    This represents a single sample of a specific metric, the value of which
    is either measured or derived at a particular time. The real-time
    system-defined bounds are optional and may not always be present or set.

    # Relationship Between Bounds and Metric Samples
    Suppose a metric sample for active power has a lower-bound of -10,000 W,
    and an upper-bound of 10,000 W. For the system to accept a charge
    command, clients need to request current values within the bounds.
    """

    sampled_at: datetime
    """The UCT timestamp at which metric was sampled."""

    metric: PBMetric
    """Metric that was sampled."""

    sample: PBMetricSampleVariant
    """Value of the sampled metric."""

    bounds: list[Bounds]
    """List of bounds that apply to the metric sample.

       These bounds adapt in real-time to reflect the operating conditions
       at the time of aggregation or derivation.

       # Multiple Bounds
       In the case of certain components like batteries, multiple bounds
       might exist. These multiple bounds collectively extend the range of
       allowable values, effectively forming a union of all given bounds.
       In such cases, the value of the metric must be within at least one
       of the bounds. In accordance with the passive sign convention, bounds
       that limit discharge would have negative numbers, while those limiting
       charge, such as for the State of Power (SoP) metric, would be positive.
       Hence bounds can have positive and negative values depending on the
       metric they represent.
    """

    source: str | None = None
    """An optional string that can be used to identify the source
       of the metric.

       This is expected to be populated when the same `Metric` variant
       can be obtained from multiple sensors in the component.
       Knowing the source of the metric can help in certain control
       and monitoring applications.

       E.g., a hybrid inverter can have a DC string for a battery and
       another DC string for a PV array. The source names could resemble,
       say, `dc_battery_0` and ``dc_pv_0`. A metric like DC voltage can be
       obtained from both sources. For an application to determine the SoC
       of the battery using the battery voltage, the source of the voltage
       metric is important.

       In cases where the component has just one source for a metric,
       then this field is not expected to be present, because the source
       is implicit.
    """

    @classmethod
    def from_proto(cls, metric_sample: PBMetricSample) -> Self:
        """Convert a protobuf MetricSample to MetricSample object.

        Args:
            metric_sample: MetricSample to convert.

        Returns:
            MetricSample object corresponding to the protobuf message.
        """
        return cls(
            sampled_at=metric_sample.sampled_at.ToDatetime(),
            metric=metric_sample.metric,
            sample=metric_sample.sample,
            bounds=list(metric_sample.bounds),
            source=metric_sample.source,
        )

    def to_proto(self) -> PBMetricSample:
        """Convert a MetricSample object to protobuf MetricSample.

        Returns:
           Protobuf message corresponding to the MetricSample object.
        """
        return PBMetricSample(
            sampled_at=Timestamp().FromDatetime(self.sampled_at),
            metric=self.metric,
            sample=self.sample,
            bounds=list(self.bounds),
            source=self.source,
        )
