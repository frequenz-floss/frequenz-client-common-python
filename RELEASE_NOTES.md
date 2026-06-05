# Frequenz Client Common Library Release Notes

## Summary

This release adds a new `grid` package for delivery area definitions, introduces explicit v1alpha8 protobuf conversion helpers across public modules (`metrics`, `streaming`, `electrical_components`, `pagination`, `grid`), and reorganises a number of subpackages to mirror the established `proto/v1alpha8/` layout. Several legacy conversion entry points have been deprecated in favour of the new free functions.

## Upgrading

- v1alpha8-backed enums (`Metric`, `MetricConnectionCategory`, `Event`, electrical component enums, `EnergyMarketCodeType`) are now plain `int`s. Converting them from/to protobuf directly is no longer supported; use the explicit conversion functions in:
    - `frequenz.client.common.metrics.proto.v1alpha8`
    - `frequenz.client.common.streaming.proto.v1alpha8`
    - `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8`
    - `frequenz.client.common.grid.proto.v1alpha8`

- The metrics proto helpers have moved from `frequenz.client.common.metrics.proto` to `frequenz.client.common.metrics.proto.v1alpha8`. The old import path is kept as a deprecated shim (importing from it now emits a deprecation warning) and will be removed in a future release. Update your imports as follows:
    - `from frequenz.client.common.metrics.proto import bounds_from_proto` → `from frequenz.client.common.metrics.proto.v1alpha8 import bounds_from_proto`
    - `from frequenz.client.common.metrics.proto import bounds_from_proto_with_issues` → `from frequenz.client.common.metrics.proto.v1alpha8 import bounds_from_proto_with_issues`
    - `from frequenz.client.common.metrics.proto import aggregated_metric_sample_from_proto` → `from frequenz.client.common.metrics.proto.v1alpha8 import aggregated_metric_sample_from_proto`
    - `from frequenz.client.common.metrics.proto import metric_connection_from_proto_with_issues` → `from frequenz.client.common.metrics.proto.v1alpha8 import metric_connection_from_proto_with_issues`
    - `from frequenz.client.common.metrics.proto import metric_sample_from_proto_with_issues` → `from frequenz.client.common.metrics.proto.v1alpha8 import metric_sample_from_proto_with_issues`

- The `PaginationInfo` conversion methods are deprecated in favour of new free functions in `frequenz.client.common.pagination.proto.v1alpha8` (calling the methods now emits a deprecation warning). Migrate as follows:
    - `PaginationInfo.from_proto(msg)` → `pagination_info_from_proto(msg)` (from `frequenz.client.common.pagination.proto.v1alpha8`)
    - `PaginationInfo.to_proto()` → `pagination_info_to_proto(info)` (from `frequenz.client.common.pagination.proto.v1alpha8`)
    - `PaginationInfo.to_proto_v1alpha8()` → `pagination_info_to_proto(info)` (from `frequenz.client.common.pagination.proto.v1alpha8`)

## New Features

- Added a new `frequenz.client.common.grid` package with `DeliveryArea` and `EnergyMarketCodeType` definitions for representing energy delivery areas.
- Added v1alpha8 conversion functions for `DeliveryArea` and `EnergyMarketCodeType` in `frequenz.client.common.grid.proto.v1alpha8`, preserving unrecognized code types as raw `int` values.
- Added v1alpha8 conversion functions for `MetricConnectionCategory`, `Event`, and the electrical component enums.
- Added v1alpha8 conversion functions for `PaginationInfo` in `frequenz.client.common.pagination.proto.v1alpha8` (`pagination_info_from_proto`, `pagination_info_to_proto`).
- Added new enum values up to `frequenz-api-common` 0.8.4.
- Added a new `frequenz.client.common.test` package with an `enum_parity` module providing a convenient class to test for protobuf-Python enum parity.

## Deprecations

- `frequenz.client.common.metrics.proto` is deprecated; use `frequenz.client.common.metrics.proto.v1alpha8` instead.
- `frequenz.client.common.pagination.PaginationInfo.from_proto` is deprecated; use `frequenz.client.common.pagination.proto.v1alpha8.pagination_info_from_proto` instead.
- `frequenz.client.common.pagination.PaginationInfo.to_proto` is deprecated; use `frequenz.client.common.pagination.proto.v1alpha8.pagination_info_to_proto` instead.
- `frequenz.client.common.pagination.PaginationInfo.to_proto_v1alpha8` is deprecated; use `frequenz.client.common.pagination.proto.v1alpha8.pagination_info_to_proto` instead.

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->
