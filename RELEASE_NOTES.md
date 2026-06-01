# Frequenz Client Common Library Release Notes

## Summary

This release adds a new `grid` package for delivery area definitions and
continues the move to explicit v1alpha8 protobuf conversion helpers for public
enums.

## Upgrading

- Converting v1alpha8-backed enums from/to protobuf directly is not supported anymore, you need to use explicit conversion functions in `frequenz.client.common.metrics.proto.v1alpha8`, `frequenz.client.common.streaming.proto.v1alpha8`, or `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8`.

## New Features

- Added a new `frequenz.client.common.grid` package with `DeliveryArea` and
  `EnergyMarketCodeType` definitions for representing energy delivery areas.
- Added v1alpha8 conversion functions for `DeliveryArea` and
  `EnergyMarketCodeType` in `frequenz.client.common.grid.proto.v1alpha8`,
  preserving unrecognized code types as raw `int` values.
- Added v1alpha8 conversion functions for `MetricConnectionCategory`, `Event`, and electrical component enums.
- Added a new `frequenz.client.common.test` package with a `enum_parity` module providing a convenient class to test for protobuf-Python enum parity.

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->
