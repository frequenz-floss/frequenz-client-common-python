# Numeric types

Numeric values can be an integer or a floating-point number. Handle them as
numbers without assuming a particular runtime type.

```python
from typing import assert_never

from frequenz.core.typing import FloatInt


def describe(value: FloatInt | None) -> str:
    match value:
        case float() | int():
            return f"next value: {value + 1}"
        case None:
            return "no value"
        case unexpected:
            assert_never(unexpected)


print(describe(1.5))  # next value: 2.5
print(describe(2))  # next value: 3
print(describe(None))  # no value
```

[`FloatInt`][frequenz.core.typing.FloatInt] is exactly `float | int`.
[PEP 484's numeric tower](https://peps.python.org/pep-0484/#the-numeric-tower)
allows an `int` where a `float` is annotated, so a [`FloatInt`][frequenz.core.typing.FloatInt] value may be a
real `float` or `int` at runtime. Arithmetic and comparisons work the same for
both. Do not use `isinstance(value, float)` alone: it is `False` for an `int`.

You can encounter [`FloatInt`][frequenz.core.typing.FloatInt] in
[`MetricSample.value`][frequenz.client.common.metrics.MetricSample.value] and
from
[`MetricSample.as_single_value()`][frequenz.client.common.metrics.MetricSample.as_single_value].
[`Bounds`][frequenz.client.common.metrics.Bounds] also uses it for `lower` and
`upper`. When you need to dispatch on the concrete type, use the `match` form
above so both number types are handled together.

`bool` is a subclass of `int`, so `True` and `False` also satisfy [`FloatInt`][frequenz.core.typing.FloatInt].
Handle them separately only when your application does not accept boolean
values.
