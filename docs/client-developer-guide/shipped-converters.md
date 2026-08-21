# Conversion functions provided by this library

The conversion functions this library provides translate the low-level protobuf
messages from
[`frequenz-api-common`](https://github.com/frequenz-floss/frequenz-api-common)
into high-level Python wrappers. This page lists the packages that contain them
and links to their API reference pages.

## v1alpha8 conversion packages

Right now, this library provides packages for the `v1alpha8` protobuf API.
Import the package that matches the messages your code receives.

| Package | What it translates |
| --- | --- |
| [`grid`][frequenz.client.common.grid.proto.v1alpha8] | Delivery areas ([`delivery_area_pb2.DeliveryArea`][frequenz.api.common.v1alpha8.grid.delivery_area_pb2.DeliveryArea]) through [`delivery_area_from_proto2`][frequenz.client.common.grid.proto.v1alpha8.delivery_area_from_proto2], plus energy-market code-type enum conversion. |
| [`metrics`][frequenz.client.common.metrics.proto.v1alpha8] | Metric samples ([`metrics_pb2.MetricSample`][frequenz.api.common.v1alpha8.metrics.metrics_pb2.MetricSample]), connections, aggregate values, bounds and bounds sets, plus metric and connection-category enum conversion. |
| [`microgrid`][frequenz.client.common.microgrid.proto.v1alpha8] | Microgrids ([`microgrid_pb2.Microgrid`][frequenz.api.common.v1alpha8.microgrid.microgrid_pb2.Microgrid]) and lifetimes through [`microgrid_from_proto`][frequenz.client.common.microgrid.proto.v1alpha8.microgrid_from_proto] and [`lifetime_from_proto`][frequenz.client.common.microgrid.proto.v1alpha8.lifetime_from_proto]. |
| [`microgrid.electrical_components`][frequenz.client.common.microgrid.electrical_components.proto.v1alpha8] | Electrical-component classes ([`electrical_components_pb2.ElectricalComponent`][frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2.ElectricalComponent]), component instances and connections, plus category, diagnostic-code, and state-code enums. |
| [`pagination`][frequenz.client.common.pagination.proto.v1alpha8] | Pagination information ([`pagination_info_pb2.PaginationInfo`][frequenz.api.common.v1alpha8.pagination.pagination_info_pb2.PaginationInfo]) in both directions through [`pagination_info_from_proto`][frequenz.client.common.pagination.proto.v1alpha8.pagination_info_from_proto] and [`pagination_info_to_proto`][frequenz.client.common.pagination.proto.v1alpha8.pagination_info_to_proto]. |
| [`streaming`][frequenz.client.common.streaming.proto.v1alpha8] | Streaming events ([`event_pb2.Event`][frequenz.api.common.v1alpha8.streaming.event_pb2.Event]) in both directions through [`event_from_proto`][frequenz.client.common.streaming.proto.v1alpha8.event_from_proto] and [`event_to_proto`][frequenz.client.common.streaming.proto.v1alpha8.event_to_proto]. |
| [`types`][frequenz.client.common.types.proto.v1alpha8] | Locations ([`location_pb2.Location`][frequenz.api.common.v1alpha8.types.location_pb2.Location]) through [`location_from_proto`][frequenz.client.common.types.proto.v1alpha8.location_from_proto]. |

## Choose a conversion direction

Call a `*_from_proto` function after your code receives a low-level protobuf
message over gRPC. It returns a high-level Python wrapper. Call a `*_to_proto`
function when your code builds a low-level protobuf message to send over gRPC.
Some packages only provide one direction because their protobuf API only needs
one direction.

Import from the public package in the table, such as
`frequenz.client.common.types.proto.v1alpha8`. Do not import from an internal
module whose name starts with an underscore.

Use the API reference links in the table for parameters, return types, and the
full function lists. For the usual client-method pattern, see
[Using conversion functions](using-conversion-functions.md).
