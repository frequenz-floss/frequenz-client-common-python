# src/frequenz/client/common — CODE PATTERNS

**Purpose:** wrap the rough `frequenz.api.common.*_pb2` gRPC-generated bindings in idiomatic
modern Python. Each domain exposes a clean Pythonic type (enum / frozen dataclass) plus a
converter layer that translates to/from the generated protobuf messages. The wrapper is the
product — generated `*_pb2` types must stay out of every public signature.

The library is a thin set of domain types + protobuf converters. Every domain follows the
same shape; learn it once and apply everywhere.

## DOMAIN LAYOUT (the pattern)

```
<domain>/
├── __init__.py          # re-exports public types; defines __all__ (sorted)
├── _<thing>.py          # the public type/enum (underscore-prefixed module, public symbol)
└── proto/
    └── v1alpha8/
        ├── __init__.py  # re-exports *_from_proto / *_to_proto; __all__ (sorted)
        └── _<thing>.py  # the converter functions for that proto schema version
```

Domains: `grid`, `metrics`, `microgrid` (+ `electrical_components`, `sensors`),
`pagination`, `streaming`, `types`.

Exception: `test`. This module is not a *domain*, it defines testing utilities
for downstream users, they don't wrap protobuf messages.

## CORE RULES

- **Wrapper field names and docstrings follow the rules in
  [`organizing-a-wrapper-package.md`](../../../../docs/wrapping-guide/organizing-a-wrapper-package.md).**
- **Public symbols live in `_name.py`, exported via the package `__init__.py`.** External
  importers never use the underscore module path.
- **Internal cross-module imports are ALWAYS relative and use the real symbol
  location**, using the public export can lead to circular imports or
  import-order issues.
- **`__all__` is always present and alphabetically sorted** in every `__init__.py`.
- **Conversion functions are ALWAYS keyed by the `frequenz.api.common` API namespace** and live
  at `frequenz.client.common.<domain>.proto.<namespace>` — currently **only `v1alpha8` exists**.
- **Proto code is isolated under `proto/<namespace>/`.** Pure types (`_metric.py`, `_location.py`)
  must NOT import `protobuf` / `frequenz.api.common`; only the `proto/` modules may.
- **New API namespace = new sibling dir** `proto/v1alphaN/`. Never edit `v1alpha8` in place;
  there is no shared/unversioned converter module.
- Converter naming: `<thing>_from_proto(message)` and `<thing>_to_proto(value)`. A converter that
  preserves malformed message data returns a typed `X | InvalidX`; enum converters follow the
  enum-or-int rule from the guides below. Do not add issue side channels.

## DESIGN PATTERNS → USE THE GUIDES (don't duplicate here)

The *how and why* of wrapper/converter design lives in `docs/wrapping-guide/`
(authored, example-backed). When adding or changing a wrapper or converter, follow the
relevant page instead of re-deriving it — and keep the code consistent with it:

| Task | Guide page |
|------|-----------|
| Package/module layout, proto isolation | [`organizing-a-wrapper-package.md`](../../../../docs/wrapping-guide/organizing-a-wrapper-package.md) |
| Enum representation (bool / class hierarchy / export-as-is); member naming & docstrings; no `UNSPECIFIED`; `TheEnum \| int` | [`enums.md`](../../../../docs/wrapping-guide/enums.md) |
| Frozen kw-only dataclasses + `__str__`, typed IDs (`BaseId`, `str_prefix`, `@final`), `FloatInt` | [`data-types.md`](../../../../docs/wrapping-guide/data-types.md) |
| Validity in the type (`X \| InvalidX`, never `Base*`; per-field `Invalid*`; recovery subtypes) | [`validity-in-the-type.md`](../../../../docs/wrapping-guide/validity-in-the-type.md) |
| Writing `*_from_proto` / `*_to_proto`; delegating to `enum_from_proto`; `HasField`/`WhichOneof`; preserving raw wire data | [`conversion-functions.md`](../../../../docs/wrapping-guide/conversion-functions.md) |
| Deprecation & compatibility | [`deprecation-and-compatibility.md`](../../../../docs/wrapping-guide/deprecation-and-compatibility.md) |
| Testing (`EnumParityTest`, Sybil) | [`testing.md`](../../../../docs/wrapping-guide/testing.md) |

## DON'T

- No `as any`-style escapes / `# type: ignore` to silence mypy strict.
- Don't import protobuf-generated modules from pure-type modules (only `proto/` may).
- Don't add a public symbol without adding it to the domain `__init__.py` `__all__`.
