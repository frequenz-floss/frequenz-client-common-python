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

Never re-scaffold enum/proto checks. Subclass the shared base and pin attributes:

```python
from frequenz.api.common.v1alpha8.metrics import metrics_pb2
from frequenz.client.common.metrics import Metric
from frequenz.client.common.metrics.proto.v1alpha8 import metric_from_proto, metric_to_proto
from frequenz.client.common.test.enum_parity import EnumParityTest

class TestMetricParity(EnumParityTest):
    python_enum = Metric
    proto_enum = metrics_pb2.Metric
    name_prefix = "METRIC_"
    from_proto = staticmethod(metric_from_proto)   # MUST wrap in staticmethod(...)
    to_proto = staticmethod(metric_to_proto)
```

`EnumParityTest` (`src/.../test/enum_parity.py`) auto-parametrizes and checks name/value
parity both ways, `from_proto` known + unknown-int handling, and `to_proto`. Class name MUST
start with `Test` for collection.

## CONVENTIONS

- `pytest` with `asyncio_mode = "auto"` — `async def test_*` needs no decorator.
- Property-based tests use `hypothesis`; mocking via `pytest-mock`.
- Warnings are errors (`pyproject.toml`); a test emitting an unexpected warning fails.
- `testpaths = ["tests", "src"]` — docstring examples under `src/` also run (via Sybil); a
  broken ```python``` block in a docstring breaks the suite.

## DON'T

- Don't copy-paste enum-parity assertions instead of subclassing `EnumParityTest`.
- Don't break the mirror layout — keep the proto-version subdir nesting.
