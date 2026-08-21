# Building your own wrappers

This library provides high-level Python wrappers and conversion functions for
messages from
[`frequenz-api-common`](https://github.com/frequenz-floss/frequenz-api-common).
If your client receives protobuf messages from a service-specific API, write
the wrapper and its conversion functions in your own client library.

## Choose where to write the wrapper

Use the conversion functions this library provides for messages from
`frequenz-api-common`. They let every client return the same high-level Python
wrapper types.

Write a custom wrapper in your own client library for messages from a
service-specific API. Keep low-level protobuf types inside your conversion
functions. Your public methods should only expose high-level Python wrappers.

## Follow the Wrapping Guide

When you write custom wrappers and conversion functions, use the patterns in the
[Wrapping Guide](../wrapping-guide/index.md):

- [Organizing a wrapper package](../wrapping-guide/organizing-a-wrapper-package.md)
  shows how to keep low-level protobuf imports out of wrapper modules.
- [Enums](../wrapping-guide/enums.md) and
  [Data types](../wrapping-guide/data-types.md) show Python types for protobuf
  fields and enums.
- [Validity in the type](../wrapping-guide/validity-in-the-type.md) and
  [Conversion functions](../wrapping-guide/conversion-functions.md) show how to
  represent invalid values, unknown enum numbers, and optional or `oneof` fields.
- [Deprecation and compatibility](../wrapping-guide/deprecation-and-compatibility.md)
  and [Testing](../wrapping-guide/testing.md) show how to change wrapper APIs
  safely and test conversion functions.

## Use shared wrappers in your custom conversion functions

When a service-specific protobuf message has a nested `frequenz-api-common`
message, call one of this library's conversion functions for that field. It
returns the shared high-level Python wrapper without making you write the same
translation again.
