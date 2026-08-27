# Overview of available wrappers

The library groups its wrappers by the kind of common API data you receive.
Use this map to find the relevant domain, then follow its links for the public
API details.

## Grid

Start with [`DeliveryArea`][frequenz.client.common.grid.DeliveryArea] and
[`EnergyMarketCodeType`][frequenz.client.common.grid.EnergyMarketCodeType].
[`InvalidDeliveryArea`][frequenz.client.common.grid.InvalidDeliveryArea],
[`BaseDeliveryArea`][frequenz.client.common.grid.BaseDeliveryArea], and
[`InvalidDeliveryAreaError`][frequenz.client.common.grid.InvalidDeliveryAreaError]
cover invalid delivery-area data.

## Metrics

The main types are
[`Metric`][frequenz.client.common.metrics.Metric],
[`MetricSample`][frequenz.client.common.metrics.MetricSample],
[`MetricConnection`][frequenz.client.common.metrics.MetricConnection],
[`MetricConnectionCategory`][frequenz.client.common.metrics.MetricConnectionCategory],
[`Bounds`][frequenz.client.common.metrics.Bounds],
[`BoundsSet`][frequenz.client.common.metrics.BoundsSet],
[`AggregatedMetricValue`][frequenz.client.common.metrics.AggregatedMetricValue], and
[`AggregationMethod`][frequenz.client.common.metrics.AggregationMethod]. The
[`BaseBounds`][frequenz.client.common.metrics.BaseBounds],
[`InvalidBounds`][frequenz.client.common.metrics.InvalidBounds],
[`InvalidBoundsError`][frequenz.client.common.metrics.InvalidBoundsError],
[`InvalidBoundsSet`][frequenz.client.common.metrics.InvalidBoundsSet], and
[`InvalidBoundsSetError`][frequenz.client.common.metrics.InvalidBoundsSetError]
cover the base and invalid range variants.

## Microgrid

Use [`Microgrid`][frequenz.client.common.microgrid.Microgrid],
[`MicrogridId`][frequenz.client.common.microgrid.MicrogridId],
[`EnterpriseId`][frequenz.client.common.microgrid.EnterpriseId], and
[`Lifetime`][frequenz.client.common.microgrid.Lifetime].
[`InvalidLifetime`][frequenz.client.common.microgrid.InvalidLifetime] carries
malformed wire data, while
[`InvalidLifetimeError`][frequenz.client.common.microgrid.InvalidLifetimeError]
is raised by safe accessors.

## Electrical components

The common base is
[`ElectricalComponent`][frequenz.client.common.microgrid.electrical_components.ElectricalComponent],
with [`ElectricalComponentId`][frequenz.client.common.microgrid.electrical_components.ElectricalComponentId]
for component identities. Concrete categories include
[`Battery`][frequenz.client.common.microgrid.electrical_components.Battery] and
[`LiIonBattery`][frequenz.client.common.microgrid.electrical_components.LiIonBattery]/[`NaIonBattery`][frequenz.client.common.microgrid.electrical_components.NaIonBattery],
the [`Inverter`][frequenz.client.common.microgrid.electrical_components.Inverter]
family, the [`EvCharger`][frequenz.client.common.microgrid.electrical_components.EvCharger]
family, [`Meter`][frequenz.client.common.microgrid.electrical_components.Meter],
and [`GridConnectionPoint`][frequenz.client.common.microgrid.electrical_components.GridConnectionPoint].

Recovery types preserve data this version cannot classify, including
[`UnspecifiedElectricalComponent`][frequenz.client.common.microgrid.electrical_components.UnspecifiedElectricalComponent],
[`UnrecognizedElectricalComponent`][frequenz.client.common.microgrid.electrical_components.UnrecognizedElectricalComponent],
[`UnspecifiedBattery`][frequenz.client.common.microgrid.electrical_components.UnspecifiedBattery],
[`UnrecognizedBattery`][frequenz.client.common.microgrid.electrical_components.UnrecognizedBattery],
and [`MismatchedCategoryElectricalComponent`][frequenz.client.common.microgrid.electrical_components.MismatchedCategoryElectricalComponent].
See the [API Reference](../reference/frequenz/client/common/index.md) for the complete component list.

## Sensors

This namespace provides [`SensorId`][frequenz.client.common.microgrid.sensors.SensorId]
for sensor identities.

## Common types

Use [`Location`][frequenz.client.common.types.Location] for location data;
[`InvalidLatitude`][frequenz.client.common.types.InvalidLatitude],
[`InvalidLongitude`][frequenz.client.common.types.InvalidLongitude], and
[`InvalidCountryCode`][frequenz.client.common.types.InvalidCountryCode] preserve
invalid fields.

## Streaming

[`Event`][frequenz.client.common.streaming.Event] is the event wrapper.

## Pagination

[`PaginationInfo`][frequenz.client.common.pagination.PaginationInfo] carries
pagination details.

For every field, method, and remaining wrapper type, see the [API
Reference](../reference/frequenz/client/common/index.md). The
[Client Developer Guide](../client-developer-guide/index.md) explains how
client libraries return these wrappers.
