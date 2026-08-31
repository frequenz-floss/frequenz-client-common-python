# Safe accessors & exceptions

Some fields can contain a value the library cannot use safely. Prefer a
`get_*()` accessor when you need that value: it returns a validated value or
raises a specific exception.

```python
from datetime import datetime, timezone

from frequenz.client.common.metrics import BoundsSet, Metric, MetricSample

sample = MetricSample(
    sample_time=datetime(2026, 1, 1, tzinfo=timezone.utc),
    metric=Metric.AC_POWER_ACTIVE,
    value=42.0,
    bounds_set=BoundsSet(),
)

metric: Metric = sample.get_metric()
print(metric.name)  # AC_POWER_ACTIVE
```

[`MetricSample.get_metric()`][frequenz.client.common.metrics.MetricSample.get_metric]
returns a known [`Metric`][frequenz.client.common.metrics.Metric]. Reading
[`MetricSample.metric`][frequenz.client.common.metrics.MetricSample.metric]
directly can instead give you a lower-level integer that needs checking.

```python
from datetime import datetime, timezone

from frequenz.client.common import UnrecognizedEnumValueError
from frequenz.client.common.metrics import BoundsSet, MetricSample

sample = MetricSample(
    sample_time=datetime(2026, 1, 1, tzinfo=timezone.utc),
    metric=999,
    value=42.0,
    bounds_set=BoundsSet(),
)

try:
    sample.get_metric()
except UnrecognizedEnumValueError as error:
    print(error.attr_name)  # metric
    print(error.value)  # 999
```

Catch [`UnrecognizedEnumValueError`][frequenz.client.common.UnrecognizedEnumValueError]
when you need to handle an unrecognized value and inspect its raw integer.
[`UnspecifiedEnumValueError`][frequenz.client.common.UnspecifiedEnumValueError]
handles the unspecified value. Other accessors follow the same pattern; for
example,
[`MetricSample.get_bounds_set()`][frequenz.client.common.metrics.MetricSample.get_bounds_set]
returns a valid [`BoundsSet`][frequenz.client.common.metrics.BoundsSet] or
raises [`InvalidBoundsSetError`][frequenz.client.common.metrics.InvalidBoundsSetError].

For a shared fallback, catch
[`InvalidAttributeError`][frequenz.client.common.InvalidAttributeError] for any
invalid field value, including a
[`MissingFieldError`][frequenz.client.common.MissingFieldError]. It is also a
[`ValueError`][]. Catch
[`ClientCommonError`][frequenz.client.common.ClientCommonError] when you need
to handle any library-defined semantic accessor error. Constructors,
conversion functions, and normal Python operations can also raise built-in
exceptions such as `ValueError` or `TypeError`.
