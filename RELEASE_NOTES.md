# Frequenz Client Common Library Release Notes

## Summary

This breaking release removes deprecated compatibility modules and symbols, and implicit enum conversions.

## Upgrading

* Passing enum values directly to build protobuf messages is not longer supported, you need to call the conversion functions `xxx_(from|to)_proto_v1alpha8()` explicitly.
* Replace `frequenz.client.common.metric.Metric` with `frequenz.client.common.metrics.Metric`.
* Replace `frequenz.client.common.microgrid.components` imports with `frequenz.client.common.microgrid.electrical_components` imports.
* Replace `frequenz.client.common.enum_proto.enum_from_proto` with `frequenz.client.common.proto.enum_from_proto`.
* Replace `frequenz.client.common.metrics.proto` conversion imports with `frequenz.client.common.metrics.proto.v1alpha8` imports.
* Replace `PaginationInfo.from_proto()`, `PaginationInfo.to_proto()`, and `PaginationInfo.to_proto_v1alpha8()` with `frequenz.client.common.pagination.proto.v1alpha8` conversion functions.
* Replace `frequenz.client.common.pagination.Info` with `frequenz.client.common.pagination.PaginationInfo`.
* Use API-provided `v1alpha8` pagination protobuf messages directly instead of `frequenz.client.common.pagination.Params`.

## New Features

<!-- Here goes the main new features and examples or instructions on how to use them -->

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->
