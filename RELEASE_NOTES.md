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

* `frequenz.client.common.grid.proto.v1alpha8.delivery_area_from_proto` is now deprecated; use `delivery_area_from_proto2` instead.

    The new converter returns `DeliveryArea | InvalidDeliveryArea` and surfaces malformed wire data at the type level rather than silently constructing a `DeliveryArea` with invalid content. The old converter continues to work but emits a `DeprecationWarning`.

* `frequenz.client.common.grid.DeliveryArea` construction with invalid data is deprecated. Please construct only valid `DeliveryArea` objects.

    A well-formed `DeliveryArea` has a non-empty `code` and a specified (non-`UNSPECIFIED`) `code_type`. Constructing one with invalid data currently emits a `DeprecationWarning`; a future release will replace the warning with a hard `ValueError`. To opt into the upcoming behavior right now, pass `_raise_on_invalid=True` to the constructor. Prefer `delivery_area_from_proto2` to load delivery areas from the wire — malformed messages become `InvalidDeliveryArea` instances instead.

* `frequenz.client.common.metrics.proto.v1alpha8.bounds_from_proto` is now deprecated; use `bounds_from_proto2` instead.

    The new converter returns `Bounds | InvalidBounds` and surfaces malformed wire data at the type level rather than raising a `ValueError` when `lower > upper`. The old converter continues to work but emits a `DeprecationWarning`.

* `frequenz.client.common.metrics.proto.v1alpha8.bounds_from_proto_with_issues` is now deprecated with no direct replacement.

    Validity is now encoded in the return type of `bounds_from_proto2` (`Bounds | InvalidBounds`), so callers should inspect the returned type instead of collecting issue strings via a side channel. The old converter continues to work but emits a `DeprecationWarning`.

* `frequenz.client.common.metrics.Bounds.__str__` now renders as `[lower,upper]` (no space after the comma) to match the compact format used by `Lifetime` and to compose cleanly with the `<invalid:...>` marker on `InvalidBounds`.

* `frequenz.client.common.metrics.MetricSample.bounds` is now deprecated; use `bounds_set` instead.

    The field type changed from `list[Bounds]` to `BoundsSet | InvalidBoundsSet` (see New Features). Reads and construction remain backward compatible: passing the `bounds=` keyword argument still works (it builds a `BoundsSet` and emits a `DeprecationWarning`), and reading `MetricSample.bounds` still returns the valid `Bounds` as a `list` (also emitting a `DeprecationWarning`). The compatibility property returns only the valid, normalized bounds, so it may differ from the raw wire list when bounds overlapped or touched.

* `frequenz.client.common.metrics.proto.v1alpha8.metric_sample_from_proto_with_issues` no longer drops invalid bounds or reports them as a major issue.

    Malformed bounds are now preserved in the returned `MetricSample.bounds_set` as an `InvalidBoundsSet` (validity is encoded in the type), so the previous "bounds for ... is invalid, ignoring these bounds" major issue is no longer produced.

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

* Added safe convenience getters that raise the new exceptions for unspecified, unrecognized, missing or invalid values:

    * `frequenz.client.common.grid.DeliveryArea.get_code_type()`
    * `frequenz.client.common.metrics.MetricConnection.get_category()`
    * `frequenz.client.common.metrics.MetricSample.get_metric()`
    * `frequenz.client.common.metrics.MetricSample.get_bounds_set()`
    * `frequenz.client.common.microgrid.electrical_components.ElectricalComponent.get_metric_config_bounds()`

* Added new delivery-area class hierarchy:

    * `frequenz.client.common.grid.BaseDeliveryArea` — abstract common supertype of the two concrete leaves; not directly instantiable.
    * `frequenz.client.common.grid.DeliveryArea` — well-formed delivery area (retroactively made a subclass of `BaseDeliveryArea`).
    * `frequenz.client.common.grid.InvalidDeliveryArea` — malformed wire data; same fields as `DeliveryArea` with no invariants enforced, so callers can inspect whatever the server actually sent.

* Added `frequenz.client.common.grid.proto.v1alpha8.delivery_area_from_proto2` returning `DeliveryArea | InvalidDeliveryArea`. This is the replacement for the now-deprecated `delivery_area_from_proto`.

* Added a new `frequenz.client.common.microgrid.Lifetime` type together with the `frequenz.client.common.microgrid.proto.v1alpha8.lifetime_from_proto` conversion function.

* Added `frequenz.client.common.metrics.proto.v1alpha8.bounds_from_proto2` returning `Bounds | InvalidBounds`. This is the replacement for the now-deprecated `bounds_from_proto`.

* `frequenz.client.common.metrics.Bounds` gained containment check capabilities:

    * `value in bounds` (`__contains__`) tests membership, inclusive on both ends, with a `None` bound meaning unbounded in that direction.
    * `bool(bounds)` and `bounds.is_bounded()` report whether the bounds restrict anything; a fully unbounded `Bounds()` is falsy.

* Added a new bounds-set class hierarchy:

    * `frequenz.client.common.metrics.BoundsSet` — a normalized union of `Bounds` with an efficient `value in bounds_set` membership test. Overlapping and touching bounds are merged on construction, and the empty set is the unbounded set (it contains every value and is falsy).
    * `frequenz.client.common.metrics.InvalidBoundsSet` — a set built from bounds that included at least one `InvalidBounds`; it preserves all the raw bounds unmerged and provides no membership test.

* Added a new `frequenz.client.common.metrics.MetricSample.bounds_set` field, typed `BoundsSet | InvalidBoundsSet`, replacing the deprecated `bounds` list (see Upgrading). Malformed wire bounds are preserved as an `InvalidBoundsSet` instead of being dropped. Use `get_bounds_set()` to resolve it to a valid `BoundsSet` or a clear `InvalidBoundsSetError`.

* Added a new `frequenz.client.common.types.Location` type together with the `frequenz.client.common.types.proto.v1alpha8.location_from_proto` conversion function.

* Added a new `frequenz.client.common.microgrid.Microgrid` type, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

* Added a new `frequenz.client.common.microgrid.electrical_components` package, featuring a `ElectricalComponent` class hierarchy and its families (battery, inverter, EV charger, etc.), and `ElectricalComponentConnection` class hierarchy, including `v1alpha8` proto conversion functions.

    The class of a component is its identity; components don't carry category or type attributes. The only exceptions are the error-recovery classes `UnrecognizedElectricalComponent` and `MismatchedCategoryElectricalComponent` (with a raw protobuf `category` value) and `UnrecognizedBattery`, `UnrecognizedInverter` and `UnrecognizedEvCharger` (with a raw protobuf `type` value), which preserve the raw protobuf values received from the protocol version used to load them.

    `ElectricalComponent.metric_config_bounds` is typed `Mapping[Metric | int, Bounds | InvalidBounds]`: malformed wire entries are preserved as `InvalidBounds` instead of being silently dropped, and entries that named a metric but carried no (or an empty) `config_bounds` submessage load as an unbounded `Bounds()` (a `Bounds` with neither bound set imposes no limit in either direction). Use `get_metric_config_bounds()` to resolve an entry to a valid `Bounds` or a clear `InvalidBoundsError`; it mimics `dict.get()`, returning an unbounded `Bounds()` (or a caller-supplied `default`) for absent metrics.

* Added a new `frequenz.client.common.microgrid.Microgrid` type with a raising `is_active()` method, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

## Bug Fixes

* Fixed `EnumParityTest` so protobuf values whose Python member name exists with a different number fail parity checks instead of being treated as unmirrored protobuf values.
