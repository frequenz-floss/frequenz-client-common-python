# Deprecation and compatibility

Use these steps when you change a public wrapper type or conversion function.
They keep the old name visible and usable for a limited time. The upstream
[semantic-versioning rules](https://github.com/frequenz-floss/docs/blob/v0.x.x/python/semver-0.x.x.md)
define the wider 0.x versioning process.

## Name the replacement precisely

Mark the old public symbol with
[`typing_extensions.deprecated`][typing_extensions.deprecated]. Use this exact
message form: `"<old FQCN> is deprecated. Use <new FQCN> instead."`. Write both
fully qualified names exactly. In the old API documentation, explain any change
to the return type or behavior. A caller should know what to use from the
warning alone.

This example gives the replacement conversion function a numeric-suffixed name
and checks its warning:

```python
from pytest import deprecated_call
from typing_extensions import deprecated


def thing_from_proto2(value: int) -> str:
    return str(value)


@deprecated(
    "example.thing_from_proto is deprecated. Use example.thing_from_proto2 instead."
)
def thing_from_proto(value: int) -> str:
    return thing_from_proto2(value)


with deprecated_call(
    match="example.thing_from_proto is deprecated. "
    "Use example.thing_from_proto2 instead."
):
    assert thing_from_proto(3) == "3"
```

## Add a new converter when its contract changes

When a conversion function's arguments or return type change in an incompatible
way, add a new name with a numeric suffix such as `thing_from_proto2`. Keep the
previous name as a deprecated function. The new function has its own stable
signature and can return the current `X | InvalidX` result described in
[Conversion functions](conversion-functions.md).

The numeric suffix supports the compatibility transition; it is not necessarily
permanent. At the next minor release, follow the upstream
[semantic-versioning rules](https://github.com/frequenz-floss/docs/blob/v0.x.x/python/semver-0.x.x.md)
for removing deprecated versions and, when applicable, restoring the
unsuffixed name while retaining a deprecated alias for the suffixed name.

For an enum-member change, use
[`deprecated_member`][frequenz.core.enum.deprecated_member]. It keeps the old
member temporarily and warns when code uses it. Document the representation new
code should use.

## Tighten invariants in stages

When you tighten a rule, do not always reject old input immediately. First,
accept it and emit a [`DeprecationWarning`][] with
[`warnings.warn()`][warnings.warn]. Where feasible, provide a documented opt-in
flag for the stricter behavior. In a later minor release, make invalid normal
construction raise every time. A conversion function must still keep invalid
protobuf data in the typed invalid result from
[Validity in the type](validity-in-the-type.md).

This lets callers find affected construction code when warnings are errors. They
can test the stricter behavior before it becomes required and migrate on purpose.

## Test and document each transition

Test every public deprecation with
[`pytest.deprecated_call()`][pytest.deprecated_call]. Check the exact message
and the replacement behavior. If deprecated code correctly calls another
deprecated symbol, suppress only that expected inner
[`DeprecationWarning`][]
in a small [`warnings.catch_warnings()`][warnings.catch_warnings] block. The
outer API must still emit its one public warning.

Add `RELEASE_NOTES.md` migration bullets that state the old behavior, the
replacement, what changes, and the planned removal version. Remove the
deprecated name at the right minor-version bump. Follow the upstream
[semantic-versioning rules](https://github.com/frequenz-floss/docs/blob/v0.x.x/python/semver-0.x.x.md).
