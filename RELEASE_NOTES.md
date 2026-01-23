# Frequenz Client Common Library Release Notes

## Summary

<!-- Here goes a general summary of what this release is about -->

## Deprecation

- Converting `Metric` enums from/to protobuf directly is deprecated and will be dropped in the next breaking release.

    You should switch to use the new conversion functions in `frequenz.client.common.metrics.proto.v1alpha8` to convert from/to protobuf.

    Since we can't emit deprecation messages for this (as they will trigger every time a metric value is used), please consider using the new conversion functions as soon as possible so the migration to the next breaking release is smooth.

## New Features

- A new module `frequenz.client.common.metrics.proto.v1alpha8` has been added to provide conversion functions for `Metric`s from/to protobuf version `v1alpha8`.

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->
