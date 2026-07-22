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

* Several `__str__` representations were standardized around the `<invalid:VALUE>` marker, so a `grep '<invalid:'` over logs finds every invariant violation regardless of which type produced it:

    * `frequenz.client.common.metrics.MetricConnection.__str__` renders as `{name}:{category}` (with `name` possibly empty); known categories render as their member name, the unspecified category renders as `cat=<invalid:0>`, and unknown non-zero categories render as `cat=<int>`.
    * `frequenz.client.common.metrics.MetricSample` gained a compact `__str__` (`metric=value`, plus `@connection` when a connection is set) instead of falling back to the dataclass `repr`.
    * `UnrecognizedElectricalComponent`, `MismatchedCategoryElectricalComponent`, `UnrecognizedBattery`, `UnrecognizedEvCharger` and `UnrecognizedInverter` now expose their raw wire `category` / `type` in `__str__` (e.g. `CID1:comp1:Inverter:type=99`), instead of hiding it behind the class name alone. These values are merely unrecognized (forward-compatible), not invariant violations, so they use a plain `:field=value` detail rather than the `<invalid:...>` marker.

* `frequenz.client.common.metrics.MetricSample.bounds` is now deprecated; use `bounds_set` instead.

    The field type changed from `list[Bounds]` to `BoundsSet | InvalidBoundsSet` (see New Features), and `bounds` is now a deprecated read-only property backed by `bounds_set`, not a real dataclass field. Basic reads and construction still work: passing the `bounds=` keyword argument builds a `BoundsSet` (emitting a `DeprecationWarning`), and reading `MetricSample.bounds` returns the valid `Bounds` as a normalized, merged `list` (also emitting a `DeprecationWarning`), so it may differ from the raw wire list when bounds overlapped or touched.

    Because `bounds` is no longer a real field, this is an intentional hard break of the released dataclass API (following the project's [0.x compatibility guidance](https://github.com/frequenz-floss/docs/blob/v0.x.x/python/semver-0.x.x.md)), not a transparent shim. Several behaviors that worked with the previous `list[Bounds]` field no longer do:

    * `dataclasses.fields(sample)`, `dataclasses.asdict(sample)` and `dataclasses.astuple(sample)` no longer include `bounds` (only `bounds_set`), so e.g. `dataclasses.asdict(sample)["bounds"]` now raises `KeyError`.
    * `dataclasses.replace(sample, bounds=...)` raises `TypeError`, because the copied-over `bounds_set` field and the deprecated `bounds` argument cannot both be supplied.
    * In-place mutation such as `sample.bounds.append(...)` no longer affects the sample: the property returns a fresh list on every read.
    * Equality, hashing, list length and ordering may differ from the old raw list, because overlapping or touching bounds are merged and sorted on construction, and malformed bounds are dropped from the property.
    * Old pickles carrying a `bounds` field will not round-trip.

    Migrate to `bounds_set` (or `get_bounds_set()`) for all of these.

* `frequenz.client.common.metrics.proto.v1alpha8.metric_sample_from_proto_with_issues` no longer drops invalid bounds or reports them as a major issue.

    Malformed bounds are now preserved in the returned `MetricSample.bounds_set` as an `InvalidBoundsSet` (validity is encoded in the type), so the previous "bounds for ... is invalid, ignoring these bounds" major issue is no longer produced.

    This changes the converter's diagnostic contract: callers that used a non-empty `major_issues` list as their sample-acceptance gate will no longer see malformed bounds rejected there, and must instead inspect `bounds_set` (or call `get_bounds_set()`, which raises `InvalidBoundsSetError`) to detect them. This is an intentional trade-off — bounds validity now lives in the return type rather than the issue side-channel.

* `float`-typed fields and accessors are now annotated with the new `FloatInt` (`float | int`) type alias (see New Features), to be honest about what PEP 484's numeric tower actually admits. These symbols are affected:

    * `frequenz.client.common.metrics.AggregatedMetricValue`: the `avg`, `min`, `max` and `raw` fields.
    * `frequenz.client.common.metrics.MetricSample`: the `value` field and the `as_single_value()` return type.
    * `frequenz.client.common.metrics.Bounds`: the `lower` and `upper` fields (shared with the new `BaseBounds` / `InvalidBounds` hierarchy).

    Runtime behavior is completely unchanged: these fields could always end up storing `int` values (`x: float = 1` is legal even under `mypy --strict`), the annotations just didn't admit it. Reads that assign to `float`-typed destinations or do plain arithmetic keep type-checking as before. However, code that pattern-matches these values with a bare `case float():` arm — a latent runtime crash, since `isinstance(1, float)` is `False` — will now be flagged as non-exhaustive by strict type checkers and should be widened to `case float() | int():`, and calling `float`-only methods (e.g. `hex()`) on them now requires an explicit `float(...)` conversion.

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

    * `value in bounds` (`__contains__`) tests membership, inclusive on both ends, with a `None` bound meaning unbounded in that direction. Any `FloatInt` value is accepted, including integers too large to fit in a `float`.
    * `bool(bounds)` and `bounds.is_bounded()` report whether the bounds restrict anything; a fully unbounded `Bounds()` is falsy. A `-inf` lower or `+inf` upper endpoint is canonicalized to `None` (unbounded) on construction, so `Bounds(lower=-math.inf, upper=math.inf)` equals `Bounds()`; a wrong-side infinity (`+inf` lower or `-inf` upper) is kept as a real endpoint.

* Added a new bounds-set class hierarchy:

    * `frequenz.client.common.metrics.BoundsSet` — a normalized union of `Bounds` with an efficient `value in bounds_set` membership test (accepting any `FloatInt`, including very large integers). Overlapping and touching bounds are merged on construction, and the empty set is the unbounded set (it contains every value and is falsy).
    * `frequenz.client.common.metrics.InvalidBoundsSet` — a set built from bounds that included at least one `InvalidBounds`; it preserves all the raw bounds unmerged and provides no membership test.
    * `frequenz.client.common.metrics.proto.v1alpha8.bounds_set_from_proto` conversion function returning `BoundsSet | InvalidBoundsSet`. It converts a `repeated Bounds` field into a single bounds set.

* Added a new `frequenz.client.common.metrics.MetricSample.bounds_set` field, typed `BoundsSet | InvalidBoundsSet`, replacing the deprecated `bounds` list (see Upgrading). Malformed wire bounds are preserved as an `InvalidBoundsSet` instead of being dropped. Use `get_bounds_set()` to resolve it to a valid `BoundsSet` or a clear `InvalidBoundsSetError`.

* Added a new `frequenz.client.common.types.Location` type together with the `frequenz.client.common.types.proto.v1alpha8.location_from_proto` conversion function.

* Added a new `frequenz.client.common.microgrid.Microgrid` type, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

* Added a new `frequenz.client.common.microgrid.electrical_components` package, featuring a `ElectricalComponent` class hierarchy and its families (battery, inverter, EV charger, etc.), and `ElectricalComponentConnection` class hierarchy, including `v1alpha8` proto conversion functions.

    The class of a component is its identity; components don't carry category or type attributes. The only exceptions are the error-recovery classes `UnrecognizedElectricalComponent` and `MismatchedCategoryElectricalComponent` (with a raw protobuf `category` value) and `UnrecognizedBattery`, `UnrecognizedInverter` and `UnrecognizedEvCharger` (with a raw protobuf `type` value), which preserve the raw protobuf values received from the protocol version used to load them.

* Added a new `frequenz.client.common.microgrid.Microgrid` type with a raising `is_active()` method, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

* Added `frequenz.client.common.FloatInt`, a type alias for `float | int`.

    PEP 484's numeric tower makes `int` assignable wherever `float` is annotated, even under `mypy --strict`, while at runtime `isinstance(1, float)` is `False` — so a plain `float` annotation silently admits values that crash `match … case float():` arms and `float`-only methods like `hex()`. The library now spells such annotations `FloatInt` instead of lying (see Upgrading); the alias docstring documents the trap in detail, including the inherent `bool ⊂ int` leak. New numeric fields (`Location` latitudes/longitudes, `PowerTransformer` voltages, bounds and bounds sets) use it as well. Values loaded from protobuf are unaffected in practice, as the wire always delivers real `float`s.

## Bug Fixes

* Fixed `EnumParityTest` so protobuf values whose Python member name exists with a different number fail parity checks instead of being treated as unmirrored protobuf values.
* Fixed potential unexpected exceptions due to type-checking accepting `int` for code annotated to only accept `float`. Fixes #250.
