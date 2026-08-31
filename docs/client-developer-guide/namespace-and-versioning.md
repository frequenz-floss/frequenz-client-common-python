# Namespace and versioning

The conversion functions this library provides are grouped by the version of
the [`frequenz-api-common`](https://github.com/frequenz-floss/frequenz-api-common)
protobuf API they understand. Right now, this library provides `v1alpha8`.
Import the group that matches the messages your client receives.

## Import the matching version

When your client receives messages from the `v1alpha8` protobuf API, import
conversion functions from `frequenz.client.common.<domain>.proto.v1alpha8`.

For example,
[`location_from_proto`][frequenz.client.common.types.proto.v1alpha8.location_from_proto]
translates a protobuf
[`location_pb2.Location`][frequenz.api.common.v1alpha8.types.location_pb2.Location]
message into a high-level
[`Location`][frequenz.client.common.types.Location] wrapper:

```python
from frequenz.client.common.types.proto.v1alpha8 import location_from_proto

location = location_from_proto(response.location)
```

Your client works with the returned
[`Location`][frequenz.client.common.types.Location] wrapper.

## Keep your import and messages on the same version

The version of the protobuf messages determines which package you import. The
release version of this library does not.

- Import `frequenz.client.common.<domain>.proto.v1alpha8` for messages from the
  `v1alpha8` protobuf API.
- Use `v1alphaN` only after your client uses that protobuf API version.

## When a new protobuf API version is available

When this library adds another protobuf API version, it adds a sibling package:

```text
types/
└── proto/
    ├── v1alpha8/
    │   └── __init__.py
    └── v1alphaN/
        └── __init__.py
```

Clients that use `v1alpha8` keep importing `v1alpha8`. When your client moves
to a newer protobuf API version, update its imports to the matching package.
