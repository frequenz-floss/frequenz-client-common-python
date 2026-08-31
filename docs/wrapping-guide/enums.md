# Enums

When you wrap a protobuf enum, first ask what its values mean to callers. Do
not copy it just because it is an enum. A status can become a boolean, a
component category can become a class, and a named vocabulary can remain an
enum.

## Translate a protobuf enum to a higher-level construct

Use this when callers need one simple answer, not the enum values themselves.
[`Microgrid`][frequenz.client.common.microgrid.Microgrid] is an example. Its
[`is_active()`][frequenz.client.common.microgrid.Microgrid.is_active] method
returns a `bool` for a known status.

```python
# `microgrid` was returned by microgrid_from_proto(...), with an ACTIVE status.
assert microgrid.is_active() is True
```

### Implementation mechanics

The private `_active` field stores `bool | int`. It is an implementation detail,
not public API. The conversion function turns the known protobuf status values
into `True` and `False`. It keeps `0` and unrecognized values as their raw
`int` so the public method can report the right problem.

```python
# Internal excerpt, simplified from microgrid/proto/v1alpha8/_microgrid.py.
_ACTIVE_BY_STATUS = {
    MICROGRID_STATUS_ACTIVE: True,
    MICROGRID_STATUS_INACTIVE: False,
}


def _microgrid_status_to_active(value: int) -> bool | int:
    return _ACTIVE_BY_STATUS.get(value, value)


# The converter passes this value to the wrapper.
Microgrid(_active=_microgrid_status_to_active(message.status), ...)
```

The accessor reads only that stored value. It does not derive the result later.

```python
# Internal excerpt, simplified from microgrid/_microgrid.py.
def is_active(self) -> bool:
    match self._active:
        case bool() as active:
            return active
        case 0:
            raise UnspecifiedEnumValueError(...)
        case int() as value:
            raise UnrecognizedEnumValueError(..., value, ...)
        case unknown:
            assert_never(unknown)
```

Use this when the enum only expresses a higher-level fact such as active or
inactive. Do not use it when callers must retain, compare, or write back each
distinct protobuf value.

## Make a class hierarchy the type identity

Use a class hierarchy when a category says what the object is. The electrical
component families are [`Battery`][frequenz.client.common.microgrid.electrical_components.Battery],
[`Inverter`][frequenz.client.common.microgrid.electrical_components.Inverter],
and [`EvCharger`][frequenz.client.common.microgrid.electrical_components.EvCharger].
Their concrete subclasses carry the subtype: for example,
[`LiIonBattery`][frequenz.client.common.microgrid.electrical_components.LiIonBattery],
[`PvInverter`][frequenz.client.common.microgrid.electrical_components.PvInverter],
or
[`AcEvCharger`][frequenz.client.common.microgrid.electrical_components.AcEvCharger].

### Implementation mechanics

The electrical-component protobuf has a `category` enum and category-specific
information. That nested message has a `oneof` named `kind`. Its options are
`battery`, `ev_charger`, `grid_connection_point`, `inverter`, and
`power_transformer`. Only one option can be set.

The converter calls [`WhichOneof("kind")`][google.protobuf.message.Message.WhichOneof]
to learn which nested message is set.
It checks that name against the declared `category`. A disagreement creates a
problematic wrapper instead of guessing. The `match` on `category` then chooses
the component family, and the nested `type` value chooses its concrete class.

```python
# Internal excerpt, simplified from electrical_components/proto/v1alpha8/
# _electrical_component.py.
kind = message.category_specific_info.WhichOneof("kind")
category = enum_from_proto(message.category, ElectricalComponentCategory)

if (
    kind
    and isinstance(category, ElectricalComponentCategory)
    and category.name.lower() != kind
):
    return MismatchedCategoryElectricalComponent(...)

match category:
    case ElectricalComponentCategory.BATTERY:
        raw_type = message.category_specific_info.battery.type
        cls = _BATTERY_CLASS_BY_PROTO_TYPE.get(raw_type)
        return cls(...) if cls else UnrecognizedBattery(..., type=raw_type)

    case ElectricalComponentCategory.EV_CHARGER:
        raw_type = message.category_specific_info.ev_charger.type
        cls = _EV_CHARGER_CLASS_BY_PROTO_TYPE.get(raw_type)
        return cls(...) if cls else UnrecognizedEvCharger(..., type=raw_type)

    case ElectricalComponentCategory.INVERTER:
        raw_type = message.category_specific_info.inverter.type
        cls = _INVERTER_CLASS_BY_PROTO_TYPE.get(raw_type)
        return cls(...) if cls else UnrecognizedInverter(..., type=raw_type)
```

[`WhichOneof()`][google.protobuf.message.Message.WhichOneof] does not choose a
class by itself. It identifies the protobuf field and verifies it matches
`category`. The category and subtype lookup then select one concrete subclass
for the returned object.

Use this when each category has different fields, behavior, or likely future
extensions. Do not use it for a small, stable vocabulary whose values need no
object-specific data or behavior.

## Export a semantic enum as-is

Use an enum when its named members are the public concept. For example,
[`Metric`][frequenz.client.common.metrics.Metric] gives callers a stable list of
metric names and numbers. Copy the known names and numeric values, but do not
copy an `UNSPECIFIED` member.

Derive each member name from the protobuf value name by removing the fixed
prefix that repeats the enum name, so `METRIC_DC_VOLTAGE` becomes `DC_VOLTAGE`.
Keep the protobuf number as the member value, so conversion stays a plain
lookup. Subclass [`Enum`][frequenz.core.enum.Enum] from `frequenz-core` instead
of the standard library enum, because it supports the member deprecation
described in [Deprecation and compatibility](deprecation-and-compatibility.md).
Decorate the class with [`unique`][frequenz.core.enum.unique], which rejects two
non-deprecated members sharing a number. Give each member a one-line docstring.

```python
# A simplified wrapper enum. Known numeric values match the protobuf values.
from frequenz.core.enum import Enum, unique


@unique
class Metric(Enum):
    """List of supported metrics."""

    DC_VOLTAGE = 1
    """The DC voltage."""

    DC_CURRENT = 2
    """The DC current."""

    AC_POWER_ACTIVE = 26
    """The AC active power."""
```

The parity test described in [Testing](testing.md) checks every wrapper member
against its generated name and number, so a member that drifts from its protobuf
value fails the test suite. It intentionally accepts generated values that the
wrapper does not expose yet, preserving compatibility when the protobuf API adds
a value before the wrapper does.

!!! warning "Renumbered protobuf values"

    When a new protobuf API version keeps a value name but changes its number,
    give the member the number from the newest version you support. No single
    wrapper enum can match both versions, and taking the newest number keeps
    conversion for that version a plain lookup, with no mapping to maintain on
    the path most callers use.

    The `proto/<namespace>/` package for the older version must then translate
    its numbers explicitly instead of delegating to
    [`enum_from_proto`][frequenz.client.common.proto.enum_from_proto]. It also
    needs its own tests in place of the parity test, which no longer holds for
    those numbers.

    Renumbering a member is a breaking change for callers that read `.value`,
    so release it with the support for the new protobuf API version and record
    it as described in
    [Deprecation and compatibility](deprecation-and-compatibility.md).

The shared enum helper first tries to create the wrapper enum. If the number is
not a member, it returns the raw `int` instead. That preserves values added by a
newer protobuf API.

```python
# Internal excerpt, simplified from proto/_enum.py.
def enum_from_proto(value: int, enum_type: type[EnumT]) -> EnumT | int:
    try:
        return enum_type(value)
    except ValueError:
        return value
```

An exported wrapper enum has no `UNSPECIFIED` member. The protobuf value `0` is
the plain `int` `0`. Type every enum-valued field as `TheEnum | int`. The `int`
case covers both `0` and an unrecognized nonzero value.

When consuming such a field directly, match all three cases. Put `case 0`
before `case int()`, then finish with [`assert_never`][typing.assert_never].

```python
from typing import assert_never

from frequenz.client.common.metrics import Metric


def describe(metric: Metric | int) -> str:
    match metric:
        case 0:
            return "unspecified"
        case Metric() as known:
            return known.name
        case int() as value:
            return f"unrecognized:{value}"
        case unexpected:
            assert_never(unexpected)


assert describe(Metric.AC_POWER_ACTIVE) == "AC_POWER_ACTIVE"
assert describe(0) == "unspecified"
assert describe(999) == "unrecognized:999"
```

Use this when callers naturally compare, select, or display named values. Do
not use it merely because the protobuf uses an enum. Use a boolean or class
hierarchy when either describes the Python type more clearly.
