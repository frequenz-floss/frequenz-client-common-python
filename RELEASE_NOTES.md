# Frequenz Client Common Library Release Notes

## Summary

<!-- Here goes a general summary of what this release is about -->

## Upgrading

<!-- Here goes notes on how to upgrade from previous versions, including deprecations and what they should be replaced with -->

## New Features

* Added a new `frequenz.client.common.types.Lifetime` type together with the `frequenz.client.common.types.proto.v1alpha8.lifetime_from_proto` conversion function.
* Added a new `frequenz.client.common.types.Location` type together with the `frequenz.client.common.types.proto.v1alpha8.location_from_proto` conversion function.
* Added a new `frequenz.client.common.microgrid.Microgrid` type, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.
* Added a new `frequenz.client.common.ClientCommonError` base exception and `UnspecifiedValueError` at the package root.
* Added a new `frequenz.client.common.microgrid.electrical_components` package, featuring a `ElectricalComponent` class hierarchy and its families (battery, inverter, EV charger, etc.), and `ElectricalComponentConnection`, including `v1alpha8` proto conversion functions.
* Added a new `frequenz.client.common.microgrid.Microgrid` type with a raising `is_active()` method, together with the `frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto` conversion function.

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->
