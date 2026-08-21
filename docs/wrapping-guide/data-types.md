# Data types

Wrapper objects should make their values, identity, and behavior clear. Do not
expose generated protobuf details. Use immutable data classes, typed
identifiers, and numeric annotations that match runtime values.

## Use immutable, keyword-only value objects

Declare record-like wrapper types as dataclasses with `frozen=True` and
`kw_only=True`. Freezing prevents fields from being reassigned; use immutable
field values too when the wrapper must be fully immutable. Equality depends on
the field values, and instances are hashable when those values are hashable.
Keyword-only construction keeps calls readable when fields change. Give each
public wrapper a short, useful `__str__` representation. For example,
[`Bounds`][frequenz.client.common.metrics.Bounds] renders its interval without
the extra detail of a dataclass representation.

```python
# Simplified from metrics/_bounds.py, without its validation.
import dataclasses

from frequenz.core.typing import FloatInt


@dataclasses.dataclass(frozen=True, kw_only=True)
class Bounds:
    """A set of lower and upper bounds for any metric."""

    lower: FloatInt | None = None
    """The lower bound, or `None` when unbounded."""

    upper: FloatInt | None = None
    """The upper bound, or `None` when unbounded."""

    def __str__(self) -> str:
        """Return a string representation of these bounds."""
        return f"[{self.lower},{self.upper}]"


assert str(Bounds(lower=0, upper=1)) == "[0,1]"
```

Keep the string form short enough for log messages and errors. Show the value's
useful identity or state. Do not repeat every internal detail or protobuf field.

## Use typed identifiers

Use a small type derived from [`BaseId`][frequenz.core.id.BaseId] for an
identifier. Pass its `str_prefix` as a class argument, and decorate the class
with [`final`][typing.final] because an ID type names one kind of entity and
nothing should subclass it further.

A typed ID stays integer-like for storage and comparison, and stops unrelated
IDs from comparing equal. For example,
[`MicrogridId`][frequenz.client.common.microgrid.MicrogridId] and another ID
type with the same numeric value are still different values and dictionary keys.

```python
from typing import final

from frequenz.core.id import BaseId


@final
class MicrogridId(BaseId, str_prefix="MID"):
    """A unique identifier for a microgrid."""


assert str(MicrogridId(42)) == "MID42"
```

Do not expose a bare `int` when you know what the identifier identifies. A
dedicated ID type tells callers which ID a function needs and gives compact
strings a recognizable prefix.

## Tell the truth about numbers

Use [`FloatInt`][frequenz.core.typing.FloatInt], which is exactly
`float | int`, for a value that may be an `int` at runtime even when a type
checker accepts it as `float`. [PEP 484's numeric tower](https://peps.python.org/pep-0484/#the-numeric-tower)
allows an `int` where `float` is annotated. A plain `float` annotation can hide
a runtime case that matters when code checks the concrete number type.

The alias lives in `frequenz-core`, so every Frequenz library annotates these
values the same way. Import it from there instead of defining a local copy.

Keep a numeric API generic when it only does arithmetic. When code must check
the concrete number type, handle both possibilities together:

```python
from typing import assert_never

from frequenz.core.typing import FloatInt


def describe(value: FloatInt) -> str:
    match value:
        case float() | int():
            return f"number:{value}"
        case unexpected:
            assert_never(unexpected)


assert describe(1) == "number:1"
assert describe(1.5) == "number:1.5"
```

Do not match only `float()`. An `int` accepted by the annotation would not
match. `bool` is also an `int` subclass. Reject it explicitly only when the
value you model needs that distinction.
