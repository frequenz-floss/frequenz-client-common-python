# Frequenz Client Common Library Release Notes

## Summary

<!-- Here goes a general summary of what this release is about -->

## Upgrading

* The `UNSPECIFIED` members in the following enums are now deprecated:

    * `frequenz.client.common.grid.EnergyMarketCodeType`
    * `frequenz.client.common.metrics.Metric`
    * `frequenz.client.common.metrics.MetricConnectionCategory`

    When loading these types from protobuf using dataclass-level converters (e.g., `delivery_area_from_proto`, `metric_sample_from_proto`), the low-level fields (`code_type`, `category`, `metric`) now store the raw integer `0` for unspecified values instead of the deprecated member. Unspecified values should be rare errors, so it is better to expose them only via the low-level interface.

    Lower-level enum-level converters still return the deprecated member.

    Users are encouraged to switch from direct field access to the new `get_*()` methods (see New Features), which provide a safer way to handle unspecified or unrecognized values.

## New Features

* Added new exceptions:

    * `frequenz.client.common.ClientCommonError` as a base exception for the package.
    * `frequenz.client.common.UnspecifiedValueError` for unspecified values (raw `0` or the deprecated member).
    * `frequenz.client.common.UnrecognizedValueError` for enum members not yet recognized by the library. Carries the raw integer value in its `value` attribute.

* Added safe convenience getters that raise the new exceptions for unspecified or unrecognized values:

    * `frequenz.client.common.grid.DeliveryArea.get_code_type()`
    * `frequenz.client.common.metrics.MetricConnection.get_category()`
    * `frequenz.client.common.metrics.MetricSample.get_metric()`

* Added a new `frequenz.client.common.types.Lifetime` type together with the `frequenz.client.common.types.proto.v1alpha8.lifetime_from_proto` conversion function.

* Added a new `frequenz.client.common.types.Location` type together with the `frequenz.client.common.types.proto.v1alpha8.location_from_proto` conversion function.

* Added a new `frequenz.client.common.microgrid.Microgrid` type, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

* Added a new `frequenz.client.common.microgrid.electrical_components` package, featuring a `ElectricalComponent` class hierarchy and its families (battery, inverter, EV charger, etc.), and `ElectricalComponentConnection`, including `v1alpha8` proto conversion functions.
* Added a new `frequenz.client.common.microgrid.Microgrid` type with a raising `is_active()` method, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->
