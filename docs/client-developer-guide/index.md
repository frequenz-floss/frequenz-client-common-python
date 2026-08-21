# Client Developer Guide

This guide is for developers building `frequenz-client-*` libraries with this
library. Your client gets low-level protobuf messages from a gRPC service. The
conversion functions this library provides turn them into high-level Python
wrappers that you return to your users.

If this library does not provide a wrapper you need, see the
[Wrapping Guide](../wrapping-guide/index.md). The [User Guide](../user-guide/index.md)
explains how users can work with the wrappers your client returns.

## Sections

- [Namespace and versioning](namespace-and-versioning.md) — Shows how the
  conversion functions are grouped by protobuf API version. Import the group
  that matches the messages your service sends.

- [Using conversion functions](using-conversion-functions.md) — Shows the two
  usual client-method shapes: one protobuf message and a list of them. Your
  methods convert the messages and return the wrappers.

- [Conversion functions provided by this library](shipped-converters.md) — Lists
  the `v1alpha8` packages and the messages they translate. The table links each
  package to its API reference.

- [Building your own wrappers](building-your-own.md) — Explains when your client
  library needs its own wrapper types and conversion functions. It points to the
  Wrapping Guide for the patterns to use.
