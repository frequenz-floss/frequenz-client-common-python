# Conversion functions

Conversion functions translate low-level protobuf messages into high-level
Python wrappers. They keep generated types out of public wrapper modules. They
also retain values that a newer server sends or that an invalid message
contains. This page explains how to write one; the conversion functions this
library provides follow the same rules.

## Keep generated code in conversion packages

Put a conversion function named `*_from_proto` or `*_to_proto` in
`proto/<namespace>/`, where `<namespace>` identifies a protobuf API version such
as `v1alpha8`. Add a sibling directory when you support a new protobuf API
version. Public type modules must not import generated protobuf code. They
define the wrapper types that conversion functions use. See
[Organizing a wrapper package](organizing-a-wrapper-package.md) for the package
layout.

Keep the protobuf type in the conversion function signature and export the
function from its versioned `proto` package. Public wrapper types and their
ordinary constructors must not depend on generated message classes.

## Delegate enum conversion

An enum conversion function calls
[`enum_from_proto`][frequenz.client.common.proto.enum_from_proto]. The helper
returns a known wrapper enum member. It returns an unrecognized number as
`int`. Use `allow_invalid=False` only when your code cannot accept an
unrecognized value. This is how [Enums](enums.md) keeps an enum usable with
newer protobuf APIs.

```python
from frequenz.client.common.metrics import Metric
from frequenz.client.common.proto import enum_from_proto


assert enum_from_proto(Metric.AC_POWER_ACTIVE.value, Metric) is Metric.AC_POWER_ACTIVE
assert enum_from_proto(999, Metric) == 999
```

Do not copy this logic into each enum conversion function. Using the helper
keeps unrecognized values consistent across wrapper packages. The one exception
is a protobuf API version that numbers a value differently from the wrapper
enum, which [Enums](enums.md) covers: those conversion functions translate the
numbers themselves.

The matching `*_to_proto` function needs no helper. The wrapper member value is
the protobuf number, as [Enums](enums.md) requires, so the function wraps that
number in the generated `ValueType`:

```python
# Excerpt from metrics/proto/v1alpha8/_metric.py, without its docstring.
def metric_to_proto(metric: Metric) -> metrics_pb2.Metric.ValueType:
    return metrics_pb2.Metric.ValueType(metric.value)
```

Type the parameter as the wrapper enum, not `Metric | int`. A caller that
received an unrecognized number decides what to send back; the conversion
function does not choose for it.

## Return validity in the type

When a protobuf message breaks a rule for the wrapper type, return
`X | InvalidX`. The valid subclass gives callers the normal behavior. The
invalid subclass keeps the received fields for diagnosis, recovery, or later
interpretation. For example,
[`Bounds`][frequenz.client.common.metrics.Bounds] and
[`InvalidBounds`][frequenz.client.common.metrics.InvalidBounds] represent valid
and invalid ranges, while
[`DeliveryArea`][frequenz.client.common.grid.DeliveryArea] and
[`InvalidDeliveryArea`][frequenz.client.common.grid.InvalidDeliveryArea] do the
same for delivery-area data. See [Validity in the type](validity-in-the-type.md)
for how to model these types.

Normal construction must enforce the valid type's rules and reject invalid
values. A conversion function, however, must keep invalid protobuf data by
creating the matching invalid subclass. This gives callers a reliable valid type
without discarding a message the client received. Annotate the return type as
the explicit union, not as the shared `Base*` class, so callers must separate
the two cases; see [Validity in the type](validity-in-the-type.md).

When working with this result, use a safe `get_*()` accessor if the wrapper has
one. Otherwise, handle every member of the union with `match` and
[`assert_never`][typing.assert_never]:

```python
from typing import assert_never

from frequenz.client.common.metrics import Bounds, InvalidBounds


def describe(bounds: Bounds | InvalidBounds) -> str:
    match bounds:
        case Bounds():
            return "valid"
        case InvalidBounds():
            return "invalid"
        case unexpected:
            assert_never(unexpected)


assert describe(Bounds(lower=0, upper=1)) == "valid"
assert describe(InvalidBounds(lower=1, upper=0)) == "invalid"
```

## Check unset fields and alternatives

Generated scalar defaults do not tell you whether a field was sent. Use
[`HasField()`][google.protobuf.message.Message.HasField] for an optional or
message field. Use [`WhichOneof()`][google.protobuf.message.Message.WhichOneof]
to check the active option in a `oneof` before you read it. Base the conversion
on those results, not on a default value that could mean the field is absent or
set.

When a message contains descriptor-known content that the current wrapper type
does not model, retain it in a JSON-compatible mapping for inspection. When
creating that mapping with
[`MessageToDict()`][google.protobuf.json_format.MessageToDict], pass
`preserving_proto_field_name=True` so its keys use the original protobuf field
names.

This mapping is not a lossless protobuf representation. It does not preserve
unknown wire fields, all field-presence information, or the exact protobuf
representation of each value. Do not use it when the wrapper must write the
original content back unchanged; preserve a lossless representation for that
use case instead.
