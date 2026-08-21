# User Guide

`frequenz-client-common` wraps the raw protobuf messages of the Frequenz common
API in idiomatic, type-safe Python. Frequenz API client libraries build on it
and hand you these wrapper objects — typed IDs, metrics, bounds, locations, and
more — so you work with natural Python types instead of generated protobuf code.

This guide shows you how to use those objects safely: reading their values,
handling data that may be missing or invalid, and relying on the types to catch
mistakes early. You don't need to know anything about protobuf to follow it.
If you are building a client library instead, see the
[Client Developer Guide](../client-developer-guide/index.md).

## Sections

- [Typed IDs](typed-ids.md) — Shows how typed identifiers distinguish
  microgrids, components, sensors, and enterprises even when they have the
  same number. It also shows how to print, compare, and use them as keys.
- [Safe accessors & exceptions](safe-accessors.md) — Explains when `get_*()`
  accessors return a validated value and when they raise an exception. Use it
  when a field may be missing, invalid, or unrecognized.
- [Numeric types](numeric-types.md) — Explains why a numeric value may be a
  `float` or an `int` at runtime and how to handle either safely. It also
  covers the special case of boolean values.
- [Enum-or-int fields](enum-or-int-fields.md) — Shows why some fields can
  contain an enum member or a raw integer. Learn how to handle unspecified and
  unrecognized values with accessors or `match`, and why you should treat the
  underlying numbers as opaque values tied to a protocol version.
- [Validity in the type](validity-in-the-type.md) — Shows how wrappers retain
  invalid values instead of dropping them. Learn how to inspect those values
  or let a safe accessor raise an exception.
- [Membership & bounds](membership-and-bounds.md) — Shows how
  [`Bounds`][frequenz.client.common.metrics.Bounds] and
  [`BoundsSet`][frequenz.client.common.metrics.BoundsSet] support `in` range
  checks. It explains bounded and unbounded ranges and what to do with invalid
  bounds.
- [Reading string output](reading-string-output.md) — Explains markers such as
  `<invalid:…>` and unexpected raw values in logs. Learn which indicate invalid
  data and which indicate data that this client does not recognize yet.
- [Overview of available wrappers](overview.md) — Lists wrapper types by data
  group and links to their API reference. Use it to find the types for the
  common data you receive.
