# Validity in the type

When data violates an invariant, the library keeps the raw value instead of
silently dropping it or failing immediately. The type makes the invalid value
visible, so you can decide how to handle it.

Some fields return a whole object or its invalid counterpart. For example, a
delivery area can be a [`DeliveryArea`][frequenz.client.common.grid.DeliveryArea]
or an [`InvalidDeliveryArea`][frequenz.client.common.grid.InvalidDeliveryArea].
Match both cases when you read such a value:

```python
from typing import assert_never

from frequenz.client.common.grid import DeliveryArea, InvalidDeliveryArea


def describe(area: DeliveryArea | InvalidDeliveryArea) -> str:
    match area:
        case DeliveryArea():
            return "valid"
        case InvalidDeliveryArea():
            return "invalid"
        case unexpected:
            assert_never(unexpected)
```

An invalid object keeps its raw fields. Prefer a safe accessor when the object
offers one: it returns the valid value or raises a typed
[`InvalidAttributeError`][frequenz.client.common.InvalidAttributeError] subclass.
For example, an [`InvalidDeliveryAreaError`][frequenz.client.common.grid.InvalidDeliveryAreaError] exposes the invalid value on
[`InvalidDeliveryAreaError.delivery_area`][frequenz.client.common.grid.InvalidDeliveryAreaError.delivery_area]. See [safe accessors](safe-accessors.md).

An otherwise valid object can also carry an invalid value in one field.
[`Location`][frequenz.client.common.types.Location] uses
[`InvalidLatitude`][frequenz.client.common.types.InvalidLatitude],
[`InvalidLongitude`][frequenz.client.common.types.InvalidLongitude], and
[`InvalidCountryCode`][frequenz.client.common.types.InvalidCountryCode] wrappers.
Each has the raw value on [`InvalidLatitude.value`][frequenz.client.common.types.InvalidLatitude.value],
[`InvalidLongitude.value`][frequenz.client.common.types.InvalidLongitude.value], or
[`InvalidCountryCode.value`][frequenz.client.common.types.InvalidCountryCode.value].

```python
from frequenz.client.common.types import (
    InvalidCountryCode,
    InvalidLatitude,
    InvalidLongitude,
    Location,
)

location = Location(
    latitude=InvalidLatitude(value=999.0),
    longitude=InvalidLongitude(value=-999.0),
    country_code=InvalidCountryCode(value="Germany"),
)

match location.latitude:
    case InvalidLatitude(value=raw_latitude):
        print(raw_latitude)  # 999.0
    case latitude:
        print(latitude)
```

Use [`Location.get_latitude()`][frequenz.client.common.types.Location.get_latitude] when you need a valid number. It returns the
latitude or raises
[`InvalidLatitudeError`][frequenz.client.common.types.InvalidLatitudeError],
whose [`InvalidLatitudeError.value`][frequenz.client.common.types.InvalidLatitudeError.value] is the raw value.

Timestamps work the same way. A protobuf `Timestamp` counts seconds and
nanoseconds as plain integers, so a message can carry values the `Timestamp`
contract does not allow: an instant outside the years 1 to 9999, or a
nanosecond fraction outside `[0, 999999999]`. Every wrapper timestamp field is
therefore `datetime | `[`InvalidDatetime`][frequenz.client.common.InvalidDatetime],
with [`InvalidDatetime.seconds`][frequenz.client.common.InvalidDatetime.seconds]
and [`InvalidDatetime.nanos`][frequenz.client.common.InvalidDatetime.nanos]
holding exactly what the server sent:

```python
from datetime import datetime

from frequenz.client.common.metrics import BoundsSet, Metric, MetricSample
from frequenz.client.common import InvalidDatetime, InvalidDatetimeError

sample = MetricSample(
    sample_time2=InvalidDatetime(seconds=253402300800, nanos=0),
    metric=Metric.AC_POWER_ACTIVE,
    value=42.0,
    bounds_set=BoundsSet(),
)

match sample.sample_time2:
    case InvalidDatetime(seconds=raw_seconds):
        print(raw_seconds)  # 253402300800
    case datetime() as sample_time:
        print(sample_time.isoformat())

try:
    sample.get_sample_time()
except InvalidDatetimeError as error:
    print(error.attr_name)  # sample_time2
    print(error.datetime)  # <invalid:253402300800s+0ns>
```

A [`Lifetime`][frequenz.client.common.microgrid.Lifetime] is the exception: its
two ends are plain `datetime | None`, because a period whose ends cannot be
ordered is not a usable period. Only
[`InvalidLifetime`][frequenz.client.common.microgrid.InvalidLifetime] can hold
an [`InvalidDatetime`][frequenz.client.common.InvalidDatetime], and a malformed
wire timestamp gives you one of those instead.

Some wrapper types use a dedicated subclass for a value that is invalid,
unspecified, or unrecognized. For a battery, that can be
[`UnspecifiedBattery`][frequenz.client.common.microgrid.electrical_components.UnspecifiedBattery]
or
[`UnrecognizedBattery`][frequenz.client.common.microgrid.electrical_components.UnrecognizedBattery],
alongside a known subtype such as
[`LiIonBattery`][frequenz.client.common.microgrid.electrical_components.LiIonBattery].
They are all [`Battery`][frequenz.client.common.microgrid.electrical_components.Battery]
values. [`UnrecognizedBattery.type`][frequenz.client.common.microgrid.electrical_components.UnrecognizedBattery.type] keeps the raw type. Likewise,
[`MismatchedCategoryElectricalComponent`][frequenz.client.common.microgrid.electrical_components.MismatchedCategoryElectricalComponent]
is an [`ElectricalComponent`][frequenz.client.common.microgrid.electrical_components.ElectricalComponent]
whose [`MismatchedCategoryElectricalComponent.category`][frequenz.client.common.microgrid.electrical_components.MismatchedCategoryElectricalComponent.category] records the mismatched value.

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
            return "Li-ion"
        case NaIonBattery():
            return "Na-ion"
        case UnspecifiedBattery():
            return "unspecified"
        case UnrecognizedBattery(type=raw_type):
            return f"unrecognized: {raw_type}"
        case unexpected:
            assert_never(unexpected)
```

Use `match` with [`assert_never`][typing.assert_never] rather than `isinstance()` chains so a type
checker can keep the cases exhaustive. Invalid data is different from an
unrecognized enum integer: `Invalid*` signals an invariant violation, while an
unrecognized integer is unknown but well-formed. See [enum-or-int
fields](enum-or-int-fields.md) for that forward-compatible case.
