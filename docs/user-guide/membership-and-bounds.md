# Membership & bounds

Use `in` to check whether a value is within a
[`Bounds`][frequenz.client.common.metrics.Bounds] range. Endpoints are
inclusive, so the values at either end are members too.

Create [`Bounds`][frequenz.client.common.metrics.Bounds] with optional lower and
upper endpoints. `-inf` for a lower endpoint and `+inf` for an upper endpoint
become `None`; reversed endpoints and `NaN` raise [`ValueError`][].

```python
from frequenz.client.common.metrics import Bounds, BoundsSet

bounds = Bounds(lower=0, upper=100)
bounds_set = BoundsSet([bounds])
unbounded = Bounds()

print(50 in bounds)  # True
print(150 in bounds)  # False
print(0 in bounds)  # True
print(100 in bounds)  # True
print(50 in bounds_set)  # True
print(bool(unbounded))  # False
```

A `None` endpoint leaves that direction unbounded. A lower endpoint of `0`
accepts any value at least `0`, while bounds without endpoints accept every
numeric value. `None` and `NaN` are never members. You can use
[`Bounds.is_bounded()`][frequenz.client.common.metrics.Bounds.is_bounded] or
truthiness when you need to distinguish a restricted range from a fully
unbounded one.

Test a [`BoundsSet`][frequenz.client.common.metrics.BoundsSet] in the same way.
It stores a normalized union: overlapping or touching ranges are merged, and a
union that covers the full numeric range is stored as an empty
[`BoundsSet.bounds`][frequenz.client.common.metrics.BoundsSet.bounds] tuple. That
empty tuple represents the unbounded set and still contains every numeric value
except `NaN`. Direct membership with `value in bounds_set` is authoritative; do
not reconstruct it by iterating over `bounds_set.bounds`.

```python
from frequenz.client.common.metrics import Bounds, BoundsSet

unbounded_set = BoundsSet([Bounds()])

assert unbounded_set.bounds == ()
assert 42 in unbounded_set
```

[`BoundsSet`][frequenz.client.common.metrics.BoundsSet] accepts any iterable of
[`Bounds`][frequenz.client.common.metrics.Bounds], such as a list, passed
positionally—not only a tuple.

When you read a metric sample, prefer
[`MetricSample.get_bounds_set()`][frequenz.client.common.metrics.MetricSample.get_bounds_set].
It returns a valid [`BoundsSet`][frequenz.client.common.metrics.BoundsSet] or
raises
[`InvalidBoundsSetError`][frequenz.client.common.metrics.InvalidBoundsSetError].
See [safe accessors](safe-accessors.md) for handling the exception.

If you need the lower-level
[`MetricSample.bounds_set`][frequenz.client.common.metrics.MetricSample.bounds_set]
field, handle both cases explicitly:

```python
from typing import assert_never

from frequenz.client.common.metrics import BoundsSet, InvalidBoundsSet


def describe(bounds_set: BoundsSet | InvalidBoundsSet) -> str:
    match bounds_set:
        case BoundsSet():
            return "valid"
        case InvalidBoundsSet():
            return "malformed"
        case unexpected:
            assert_never(unexpected)


print(describe(BoundsSet()))  # valid
```

[`InvalidBounds`][frequenz.client.common.metrics.InvalidBounds] and
[`InvalidBoundsSet`][frequenz.client.common.metrics.InvalidBoundsSet] retain
malformed data for inspection. Do not use either for range checks; use the
safe accessor or handle the union as above. See [validity in the
type](validity-in-the-type.md) for this pattern.
