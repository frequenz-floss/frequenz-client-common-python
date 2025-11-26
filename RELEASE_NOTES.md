# Frequenz Client Common Library Release Notes

## Summary

This release main change is the introduction of a new `metrics` package compatible with the common API v0.8 (`v1alpha8`) (the old `metric` package, in singular, still works with the old v0.5/`v1` version).

## Deprecations

- The old `frequenz.client.common.enum_proto` module is now deprecated, please use `frequenz.client.common.proto.enum_from_proto` instead.

## New Features

- New `frequenz.client.common.common.proto` module with conversion utilities for protobuf types:
  - `enum_from_proto()` (moved from `enum_proto).
  - `datetime_to_proto()` and `datetime_from_proto()` functions to convert between Python `datetime` and protobuf `Timestamp` (imported from `frequenz-client-base`.
- New `metrics` package compatible with API v0.8, which includes:
  - `Metric` enum with all supported metrics.
  - `MetricSample` dataclass to represent metric samples.
  - `AggregatedMetricValue` dataclass to represent derived statistical summaries.
  - `Bounds` dataclass to represent bounds for metrics.
  - `MetricConnection` and `MetricConnectionCategory` to represent connections from which metrics are obtained.
  - `proto` submodule with conversion functions to/from protobuf types.
