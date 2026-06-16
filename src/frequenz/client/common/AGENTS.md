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

- **Wrapper field names and docstrings follow the rules in [CONTRIBUTING.md](../../../../CONTRIBUTING.md).**
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
- Converter naming: `<thing>_from_proto(message) -> T | int` and `<thing>_to_proto(T) -> ...ValueType`.
  Richer parsers use the `_from_proto_with_issues` suffix (returns value + collected issues).

## ENUMS (most common case)

- Python enum mirrors a protobuf enum: member name = proto name minus a fixed prefix
  (e.g. `METRIC_` → `Metric`), member value = proto numeric value. Start with `UNSPECIFIED = 0`.
- Decorate with `@enum.unique`; one-line `"""docstring"""` under each member.
- Conversion delegates to the shared helper — do NOT reimplement:
  ```python
  from ....proto import enum_from_proto
  def metric_from_proto(message): return enum_from_proto(message, Metric)
  def metric_to_proto(metric): return metrics_pb2.Metric.ValueType(metric.value)
  ```
- `enum_from_proto` (`proto/_enum.py`) returns the member for known values, raw `int` for
  unknown ones (forward-compat). `allow_invalid=False` raises instead.

## NON-ENUM TYPES

- Use `@dataclass(frozen=True, kw_only=True)`; give a custom `__str__` for compact display.
- Fields that may carry an unknown proto enum are typed `T | int` (see `MetricSample.metric`).
- IDs subclass `frequenz.core.id.BaseId` with a `str_prefix=` and are `@final`.

## DEVIATIONS (do not "fix" blindly)

- Two issue-reporting styles coexist: `*_with_issues` returns issues; `location_from_proto`
  logs a `warning` and silently clamps out-of-range values. Match the neighbor you edit.

## DON'T

- No `as any`-style escapes / `# type: ignore` to silence mypy strict.
- Don't import protobuf-generated modules from pure-type modules.
- Don't add a public symbol without adding it to the domain `__init__.py` `__all__`.
