# Enum-or-int fields

Some fields are an enum member or an integer, such as
[`MetricSample.metric`][frequenz.client.common.metrics.MetricSample.metric].
The integer keeps newer server values available to an older client instead of
failing when the client does not recognize them.

Prefer a safe accessor when one is available. For example,
[`MetricSample.get_metric()`][frequenz.client.common.metrics.MetricSample.get_metric]
returns a known [`Metric`][frequenz.client.common.metrics.Metric] member. It
raises [`UnspecifiedEnumValueError`][frequenz.client.common.UnspecifiedEnumValueError] for the raw value `0` and
[`UnrecognizedEnumValueError`][frequenz.client.common.UnrecognizedEnumValueError] for another unrecognized integer. See [safe
accessors](safe-accessors.md) to handle those exceptions.

```python
from datetime import datetime, timezone

from frequenz.client.common import (
    UnrecognizedEnumValueError,
    UnspecifiedEnumValueError,
)
from frequenz.client.common.metrics import BoundsSet, Metric, MetricSample


def sample_with(metric: Metric | int) -> MetricSample:
    return MetricSample(
        sample_time=datetime(2026, 1, 1, tzinfo=timezone.utc),
        metric=metric,
        value=42.0,
        bounds_set=BoundsSet(),
    )


for sample in (
    sample_with(Metric.AC_POWER_ACTIVE),
    sample_with(0),
    sample_with(999),
):
    try:
        print(sample.get_metric().name)
    except UnspecifiedEnumValueError:
        print("unspecified")
    except UnrecognizedEnumValueError as error:
        print(f"unrecognized: {error.value}")
```

When you need the lower-level field, dispatch with `match`. A known member
matches the enum, raw `0` means unspecified, and any other integer is an
unrecognized value. Do not use `isinstance()` or look for an `UNSPECIFIED`
member.

You only read these values. Treat the raw integer `0` as unspecified rather
than setting an enum's `UNSPECIFIED` member.

```python
from datetime import datetime, timezone
from typing import assert_never

from frequenz.client.common.metrics import BoundsSet, Metric, MetricSample


def describe(sample: MetricSample) -> str:
    match sample.metric:
        case Metric() as metric:
            return f"known: {metric.name}"
        case 0:
            return "unspecified"
        case int() as value:
            return f"unrecognized: {value}"
        case unexpected:
            assert_never(unexpected)


samples = (
    MetricSample(
        sample_time=datetime(2026, 1, 1, tzinfo=timezone.utc),
        metric=Metric.AC_POWER_ACTIVE,
        value=42.0,
        bounds_set=BoundsSet(),
    ),
    MetricSample(
        sample_time=datetime(2026, 1, 1, tzinfo=timezone.utc),
        metric=0,
        value=42.0,
        bounds_set=BoundsSet(),
    ),
    MetricSample(
        sample_time=datetime(2026, 1, 1, tzinfo=timezone.utc),
        metric=999,
        value=42.0,
        bounds_set=BoundsSet(),
    ),
)

for sample in samples:
    print(describe(sample))
```

An unrecognized integer is not invalid data. It is a value the server knows
that this client version does not yet recognize. Invalid values are a separate
topic; see [Validity in the type](validity-in-the-type.md).

## Treat the numbers as opaque

Work with members, not numbers. Compare against the member itself, as in
`sample.metric is Metric.AC_POWER_ACTIVE`, and let the accessors and `match`
arms above do the rest. A number is how the protocol identifies a value. It is
not how your code should identify it.

Reach for `.value` only as a last resort, when you must hand a raw protocol
number to something that speaks the protocol itself. The mapping is direct: a
member name is the protocol name without its fixed prefix, and a member value is
the protocol number.

```python
from frequenz.client.common.metrics import Metric

# A last resort: Metric.AC_POWER_ACTIVE is METRIC_AC_POWER_ACTIVE in the protocol.
assert Metric.AC_POWER_ACTIVE.value == 26
```

Those numbers belong to a protocol version, and only that version gives them a
meaning. The same number can name different things in two versions. When a new
protocol version gives an existing name a different number, this library follows
the newest version it supports. A member's number therefore changes only in a
release that adds support for a new protocol version. That is a
[breaking change](https://github.com/frequenz-floss/docs/blob/v0.x.x/python/semver-0.x.x.md)
and the release notes call it out, but the member name stays the same.

A raw integer needs the same care, and more. Read it as "the server sent a value
this client does not know", not as a stable identifier. Do not persist it or
pass it to another system as if it were version-independent, and do not compare
it against a member number to guess which value it is. To learn what one means,
look it up in the [`frequenz-api-common`](https://github.com/frequenz-floss/frequenz-api-common)
definition for the version your client speaks, or upgrade this library and your
client so the value resolves to a member.
