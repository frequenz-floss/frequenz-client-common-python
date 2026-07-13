# Frequenz Client Common Library Release Notes

## Summary

<!-- Here goes a general summary of what this release is about -->

## Upgrading

* The `frequenz.client.common.microgrid.electrical_components.ElectricalComponentCategory` enum is now deprecated and will be removed in a future release.

    Accessing any member of this enum will emit a `DeprecationWarning`. Users are encouraged to switch to the `ElectricalComponent` class hierarchy (using `match` expressions or `isinstance()`) to identify components.

    Client implementers: To convert a component class to the protobuf enum values the server expects, use the new `electrical_component_class_to_proto()` / `electrical_component_class_from_proto()` converters (see New Features).

    For example, instead of:

    ```text
    def filter_by(category: ElectricalComponentCategory) -> ...:
        ...
    ```

    Use:

    ```text
    def filter_by(component: ElectricalComponentTypes | type[ConvertibleElectricalComponentTypes]) -> ...:
        category_value, sub_type_value = electrical_component_class_to_proto(component)
        ...
    ```

    The related proto-layer converters (`electrical_component_category_to_proto`, `electrical_component_category_from_proto`) are also deprecated.

* The `UNSPECIFIED` members in the following enums are now deprecated:

    * `frequenz.client.common.grid.EnergyMarketCodeType`
    * `frequenz.client.common.metrics.Metric`
    * `frequenz.client.common.metrics.MetricConnectionCategory`
    * `frequenz.client.common.microgrid.electrical_components.ElectricalComponentDiagnosticCode`
    * `frequenz.client.common.microgrid.electrical_components.ElectricalComponentStateCode`
    * `frequenz.client.common.streaming.Event`

    When loading these types from protobuf using dataclass-level converters (e.g., `delivery_area_from_proto`, `metric_sample_from_proto`), the low-level fields (`code_type`, `category`, `metric`) now store the raw integer `0` for unspecified values instead of the deprecated member. Unspecified values should be rare errors, so it is better to expose them only via the low-level interface.

    Lower-level enum-level converters still return the deprecated member.

    Users are encouraged to switch from direct field access to the new `get_*()` methods (see New Features), which provide a safer way to handle unspecified or unrecognized values.

## New Features

* Added 4 new electrical component classes for categories that previously collapsed into `UnrecognizedElectricalComponent`:

    * `frequenz.client.common.microgrid.electrical_components.Plc` (PLC, category 13)
    * `frequenz.client.common.microgrid.electrical_components.StaticTransferSwitch` (category 15)
    * `frequenz.client.common.microgrid.electrical_components.UninterruptiblePowerSupply` (UPS, category 16)
    * `frequenz.client.common.microgrid.electrical_components.CapacitorBank` (category 17)

* Added two new proto-layer converters in `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8`:

    * `electrical_component_class_to_proto(component_class)` — converts a `ValidElectricalComponentTypes` class to the `(category, sub_type)` protobuf enum value tuple the server expects. Implemented with raw proto constants only (no deprecated wrapper enums), so it will continue to work after the wrapper enums are removed.
    * `electrical_component_class_from_proto(category, sub_type=None)` — converts a raw `(category, sub_type)` protobuf enum value pair back to the corresponding `ConcreteElectricalComponentTypes` class.

    Added a few new type aliases to support them. In particular `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8.ConvertibleElectricalComponentTypes` is the most useful (see Upgrading section above).

* Added new exceptions:

    * `frequenz.client.common.ClientCommonError` as a base exception for the package.
    * `frequenz.client.common.InvalidAttributeError` as a base for all exceptions raised when an invalid attribute is encountered. Inherits also from `ValueError` for convenience.
    * `frequenz.client.common.MissingFieldError` for accessors that resolve a `T | ... | None` wrapper field to a concrete value and see `None` because the underlying field was not set on the wire.
    * `frequenz.client.common.UnspecifiedEnumValueError` for unspecified enum values (raw `0` or the deprecated member).
    * `frequenz.client.common.UnrecognizedEnumValueError` for enum members not yet recognized by the library. Carries the raw integer value in its `value` attribute.

* Added safe convenience getters that raise the new exceptions for unspecified or unrecognized values:

    * `frequenz.client.common.grid.DeliveryArea.get_code_type()`
    * `frequenz.client.common.metrics.MetricConnection.get_category()`
    * `frequenz.client.common.metrics.MetricSample.get_metric()`

* Added a new `frequenz.client.common.types.Lifetime` type together with the `frequenz.client.common.types.proto.v1alpha8.lifetime_from_proto` conversion function.

* Added a new `frequenz.client.common.types.Location` type together with the `frequenz.client.common.types.proto.v1alpha8.location_from_proto` conversion function.

* Added a new `frequenz.client.common.microgrid.Microgrid` type, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

* Added a new `frequenz.client.common.microgrid.electrical_components` package, featuring a `ElectricalComponent` class hierarchy and its families (battery, inverter, EV charger, etc.), and `ElectricalComponentConnection` class hierarchy, including `v1alpha8` proto conversion functions.

    The class of a component is its identity; components don't carry category or type attributes. The only exceptions are the error-recovery classes `UnrecognizedElectricalComponent` and `MismatchedCategoryElectricalComponent` (with a raw protobuf `category` value) and `UnrecognizedBattery`, `UnrecognizedInverter` and `UnrecognizedEvCharger` (with a raw protobuf `type` value), which preserve the raw protobuf values received from the protocol version used to load them.

* Added a new `frequenz.client.common.microgrid.Microgrid` type with a raising `is_active()` method, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

## Bug Fixes

* Fixed `EnumParityTest` so protobuf values whose Python member name exists with a different number fail parity checks instead of being treated as unmirrored protobuf values.
