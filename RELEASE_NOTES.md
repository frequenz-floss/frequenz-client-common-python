# Frequenz Client Common Library Release Notes

## Summary

This release adds a new `grid` package for delivery area definitions, introduces explicit v1alpha8 protobuf conversion helpers across public modules (`metrics`, `streaming`, `electrical_components`, `pagination`, `grid`), and reorganises a number of subpackages to mirror the established `proto/v1alpha8/` layout. Several legacy conversion entry points have been deprecated in favour of new free functions.

## New Features

- Added a new `frequenz.client.common.grid` package with `DeliveryArea` and `EnergyMarketCodeType` definitions for representing energy delivery areas.
- Added v1alpha8 conversion functions for `DeliveryArea` and `EnergyMarketCodeType` in `frequenz.client.common.grid.proto.v1alpha8`, preserving unrecognized code types as raw `int` values.
- Added v1alpha8 conversion functions for `MetricConnectionCategory`, `Event`, and the electrical component enums.
- Added v1alpha8 conversion functions for `PaginationInfo` in `frequenz.client.common.pagination.proto.v1alpha8` (`pagination_info_from_proto`, `pagination_info_to_proto`).
- Added new enum values up to `frequenz-api-common` 0.8.4.
- Added a new `frequenz.client.common.test` package with an `enum_parity` module providing a convenient class to test for protobuf-Python enum parity.

## Deprecations

> [!IMPORTANT]
> Passing enum values directly to build protobuf messages is now deprecated, but it **does NOT emit a deprecation warning**, so migration needs to be done manually. Use the new conversion functions to convert enum values to their protobuf equivalents before passing them to message builders.
>
> **Implicit conversions will fail type checking in v0.4.0.**

- `frequenz.client.common.metrics.proto` is deprecated; use `frequenz.client.common.metrics.proto.v1alpha8` instead.
- `frequenz.client.common.pagination.PaginationInfo.from_proto` is deprecated; use `frequenz.client.common.pagination.proto.v1alpha8.pagination_info_from_proto` instead.
- `frequenz.client.common.pagination.PaginationInfo.to_proto` is deprecated; use `frequenz.client.common.pagination.proto.v1alpha8.pagination_info_to_proto` instead.
- `frequenz.client.common.pagination.PaginationInfo.to_proto_v1alpha8` is deprecated; use `frequenz.client.common.pagination.proto.v1alpha8.pagination_info_to_proto` instead.
- `frequenz.client.common.microgrid.electrical_components.ElectricalComponentCategory.from_proto()` is deprecated; use `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8.electrical_component_category_from_proto` instead.
- `frequenz.client.common.microgrid.electrical_components.ElectricalComponentCategory.to_proto()` is deprecated; use `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8.electrical_component_category_to_proto` instead.
- `frequenz.client.common.microgrid.electrical_components.ElectricalComponentStateCode.from_proto()` is deprecated; use `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8.electrical_component_state_code_from_proto` instead.
- `frequenz.client.common.microgrid.electrical_components.ElectricalComponentStateCode.to_proto()` is deprecated; use `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8.electrical_component_state_code_to_proto` instead.
- `frequenz.client.common.microgrid.electrical_components.ElectricalComponentDiagnosticCode.from_proto()` is deprecated; use `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8.electrical_component_diagnostic_code_from_proto` instead.
- `frequenz.client.common.microgrid.electrical_components.ElectricalComponentDiagnosticCode.to_proto()` is deprecated; use `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8.electrical_component_diagnostic_code_to_proto` instead.
- `frequenz.client.common.enum_proto.enum_from_proto` is deprecated; use `frequenz.client.common.proto.enum_from_proto` instead.
