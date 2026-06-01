# Frequenz Client Common Library Release Notes

## Summary

<!-- Here goes a general summary of what this release is about -->

## Upgrading

- Converting v1alpha8-backed enums from/to protobuf directly is not supported anymore, you need to use explicit conversion functions in `frequenz.client.common.metrics.proto.v1alpha8`, `frequenz.client.common.streaming.proto.v1alpha8`, or `frequenz.client.common.microgrid.electrical_components.proto.v1alpha8`.

## New Features

- Added v1alpha8 conversion functions for `MetricConnectionCategory`, `Event`, and electrical component enums.
- Added a new `frequenz.client.common.test` package with a `enum_parity` module providing a convenient class to test for protobuf-Python enum parity.

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->
