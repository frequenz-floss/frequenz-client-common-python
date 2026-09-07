# Validity in the type

Invalid protobuf data is still data the client received. Show whether it is
valid in the wrapper type. This lets a conversion function keep the received
data, ordinary construction enforce its rules, and later code ask for a valid
value when it needs one. For guidance on using these types, see the User Guide's
[validity-in-the-type section](../user-guide/validity-in-the-type.md) and
[safe-accessor section](../user-guide/safe-accessors.md).

## Model valid and invalid object states

For an object with rules that cover the whole object, define a guarded `Base*`
class and two concrete subclasses: the valid type and its `Invalid*`
counterpart. The base holds shared fields. Its `__new__` guard prevents callers
from constructing the base directly, so each instance has a meaningful state.
For example,
[`DeliveryArea`][frequenz.client.common.grid.DeliveryArea] and
[`InvalidDeliveryArea`][frequenz.client.common.grid.InvalidDeliveryArea] share
a base while making their validity visible in annotations.

Share a base only while both types hold the same field types. When the invalid
type has to accept a wider type in a field, because that field can itself
carry an `Invalid*` wrapper, write two independent classes instead.
[`BoundsSet`][frequenz.client.common.metrics.BoundsSet] and
[`InvalidBoundsSet`][frequenz.client.common.metrics.InvalidBoundsSet] do this,
as do [`Lifetime`][frequenz.client.common.microgrid.Lifetime] and
[`InvalidLifetime`][frequenz.client.common.microgrid.InvalidLifetime].

Normal constructors enforce the valid subclass's rules. A conversion function
that sees invalid protobuf data creates the matching invalid subclass and
returns `X | InvalidX`. The invalid subclass keeps the raw fields for
diagnosis, recovery, and later interpretation. It does not invent a valid
value.

Annotate results and fields with the union `X | InvalidX`, never with the
guarded base class. The union tells callers that invalid data is possible,
forces them to separate the two cases — or lets them require only the valid
type where nothing else makes sense — and keeps a `match` over the result
exhaustive. A `Base*` annotation would hide which states exist and accept any
future subclass, so a type checker could not check either decision. For
example, a delivery-area conversion function returns
[`DeliveryArea`][frequenz.client.common.grid.DeliveryArea]` | `[`InvalidDeliveryArea`][frequenz.client.common.grid.InvalidDeliveryArea],
and
[`MetricSample.bounds_set`][frequenz.client.common.metrics.MetricSample.bounds_set]
is annotated
[`BoundsSet`][frequenz.client.common.metrics.BoundsSet]` | `[`InvalidBoundsSet`][frequenz.client.common.metrics.InvalidBoundsSet],
while [`BaseDeliveryArea`][frequenz.client.common.grid.BaseDeliveryArea] and
[`BaseBounds`][frequenz.client.common.metrics.BaseBounds] appear in no public
signature.

## Wrap invalid fields precisely

An otherwise valid object can have one invalid field. In that case, put a
field-specific `Invalid*` wrapper in that field's union. Do not mark unrelated
data invalid. [`Location`][frequenz.client.common.types.Location] does this
with [`InvalidLatitude`][frequenz.client.common.types.InvalidLatitude],
[`InvalidLongitude`][frequenz.client.common.types.InvalidLongitude], and
[`InvalidCountryCode`][frequenz.client.common.types.InvalidCountryCode]. Each
wrapper keeps the raw value while leaving the other fields usable.

Reuse an existing field wrapper when several types have the same field. Every
wrapper timestamp is `datetime | InvalidDatetime` because a protobuf
`Timestamp` can break its own contract no matter which message it arrives in.
One wrapper and one
[`InvalidDatetimeError`][frequenz.client.common.InvalidDatetimeError] mean a
caller learns the pattern once. A field wrapper is protobuf-independent, so it
belongs in a public type module, not next to the conversion function that
produces it. When it wraps no `frequenz-api-common` message at all, like a
timestamp, put it directly in the top-level package or a utility-specific
module; do not mix it with a domain-specific module.

## Represent protobuf recovery as a subtype

When the class identifies a protobuf category or type, use dedicated subclasses
for recovery cases. An
[`UnspecifiedBattery`][frequenz.client.common.microgrid.electrical_components.UnspecifiedBattery]
represents a missing type, an
[`UnrecognizedBattery`][frequenz.client.common.microgrid.electrical_components.UnrecognizedBattery]
retains an unknown raw type, and
[`MismatchedCategoryElectricalComponent`][frequenz.client.common.microgrid.electrical_components.MismatchedCategoryElectricalComponent]
records conflicting category information. These subclasses make the recovery
case clear without pretending it is a known component.

Use the complete public type alias when working with guarded bases and recovery
subclasses. This handler deliberately does not construct an object. Type-check
it instead of running it:

```python
from typing import assert_never

from frequenz.client.common.microgrid.electrical_components import (
    BatteryTypes,
    LiIonBattery,
    NaIonBattery,
    UnrecognizedBattery,
    UnspecifiedBattery,
)


def describe_battery(battery: BatteryTypes) -> str:
    match battery:
        case LiIonBattery():
            return "li-ion"
        case NaIonBattery():
            return "na-ion"
        case UnspecifiedBattery():
            return "unspecified"
        case UnrecognizedBattery(type=raw_type):
            return f"unrecognized:{raw_type}"
        case unexpected:
            assert_never(unexpected)
```

## Design semantic accessors and errors together

Keep the low-level field unchanged, then add a `get_*()` accessor for callers
that need a valid value. Use an exhaustive `match` for valid, invalid, missing,
and unknown cases. End it with [`assert_never`][typing.assert_never]. For
example, [`Location.get_latitude()`][frequenz.client.common.types.Location.get_latitude]
returns a validated number and raises a typed error for an invalid latitude
wrapper.

Use this error hierarchy:
[`ClientCommonError`][frequenz.client.common.ClientCommonError] →
[`InvalidAttributeError`][frequenz.client.common.InvalidAttributeError]
(also a `ValueError`) →
[`UnspecifiedEnumValueError`][frequenz.client.common.UnspecifiedEnumValueError],
[`UnrecognizedEnumValueError`][frequenz.client.common.UnrecognizedEnumValueError],
[`MissingFieldError`][frequenz.client.common.MissingFieldError], and
domain-specific invalid-value errors such as
[`InvalidBoundsSetError`][frequenz.client.common.metrics.InvalidBoundsSetError].
Keep a specific error's raw value or invalid object on the error instance so
the caller can inspect it.

## Make invalid string output easy to search

Use the `<invalid:…>` marker only for a failed rule, such as a malformed
required field or the unspecified raw value `0`. It makes real failures clear
in logs and diagnostics. For data that is merely unknown to this version, show
the raw value as `:field=value`. Unknown data does not itself break a rule.
Use these compact forms consistently in each wrapper's `__str__` method.
