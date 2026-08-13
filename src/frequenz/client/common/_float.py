# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Honest type alias for floating-point values."""

from typing import TypeAlias

FloatInt: TypeAlias = float | int
"""A `float` that may actually be an `int` at runtime.

[PEP 484's numeric tower](https://peps.python.org/pep-0484/#the-numeric-tower)
makes `int` assignable to any `float`-annotated parameter or field, so a plain
`float` annotation is a lie: type checkers (even `mypy --strict`) happily
accept `int` values, but `isinstance(1, float)` is `False` at runtime. That
breaks `match … case float():` arms (an `int` value falls through to
`assert_never()`), calls to `float`-only methods like `hex()`, and any other
code dispatching on the concrete runtime type.

This library instead annotates such values as `FloatInt`, making the
heterogeneity explicit: type checkers will push code reading these values to
handle both branches, typically by matching with `case float() | int():`. See
[issue #250](https://github.com/frequenz-floss/frequenz-client-common-python/issues/250)
for the full analysis and the alternatives that were rejected.

Danger:
    `bool` is a subclass of `int`, so `True` and `False` also satisfy this
    alias. This is inherent to Python's type system and not guarded against.

Example:
    ```python
    from typing import assert_never

    from frequenz.client.common import FloatInt


    def describe(value: FloatInt | None) -> str:
        match value:
            case float() | int():
                return f"number {value}"
            case None:
                return "nothing"
            case unexpected:
                assert_never(unexpected)


    assert describe(1) == "number 1"
    assert describe(1.5) == "number 1.5"
    assert describe(None) == "nothing"
    ```
"""
