# tests — TEST CONVENTIONS

Tests verify that the idiomatic wrappers stay in lock-step with the generated
`frequenz.api.common.*_pb2` bindings they wrap (parity + round-trip conversion).

## LAYOUT

Tests mirror the package tree with the `src/frequenz/client/common/` prefix stripped, the
leading underscore dropped, and `test_` prepended:

```
src/frequenz/client/common/<path>/_yyy.py  ->  tests/<path>/test_yyy.py
```

Examples:
- `src/.../types/_location.py`                       -> `tests/types/test_location.py`
- `src/.../metrics/proto/v1alpha8/_metric.py`        -> `tests/metrics/proto/v1alpha8/test_metric.py`

Keep the `proto/<namespace>/` nesting intact (currently only `v1alpha8`).

## ENUM TESTS = ONE-LINE SUBCLASS

Never re-scaffold enum/proto checks. Subclass
`frequenz.client.common.test.enum_parity.EnumParityTest`. Class name MUST start
with `Test` for collection.

## CONVENTIONS

- Imports for the tested code are always absolute — this verifies the real
  public import path works. Target the **public** package path whenever the
  symbol is publicly exported. Import from an internal `_`-module only when
  testing an internal symbol not exposed publicly.
- Imports from test utilities in `tests/` are always relative.
- `pytest` with `asyncio_mode = "auto"` — `async def test_*` needs no decorator.
- Property-based tests use `hypothesis`; mocking via `pytest-mock`.
- Warnings are errors (`pyproject.toml`); a test emitting an unexpected warning fails.
- `testpaths = ["tests", "src"]` — docstring examples under `src/` also run (via Sybil); a
  broken ```python``` block in a docstring breaks the suite.

## DON'T

- Don't copy-paste enum-parity assertions instead of subclassing `EnumParityTest`.
- Don't break the mirror layout — keep the proto-version subdir nesting.
