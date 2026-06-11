# PROJECT KNOWLEDGE BASE

## OVERVIEW

`frequenz-client-common` — **idiomatic modern-Python wrappers** over the rough gRPC-generated
bindings of [`frequenz-api-common`](https://github.com/frequenz-floss/frequenz-api-common/)
(`frequenz.api.common.*_pb2`). It hides the generated protobuf surface behind clean enums,
frozen dataclasses, and typed `*_from_proto`/`*_to_proto` converters, shared by all Frequenz
API clients. Pure Python 3.11+ library, src-layout, namespace package `frequenz.client.common`.
No runtime app; it is imported by other client libraries.

**Prime directive:** the public API must feel hand-written and Pythonic. Generated protobuf
types never leak into a public signature — they are confined to the `proto/` converter layer.

## STRUCTURE

```
.
├── src/frequenz/client/common/   # the library (PEP 420 namespace pkg)
├── tests/                         # mirrors src/ layout by domain + proto version
├── docs/_scripts/                 # mkdocstrings autoapi generation (not prose)
├── noxfile.py                     # 8 lines; delegates everything to frequenz-repo-config
└── site/                          # generated docs output — do NOT hand-edit or commit
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add/change a public type or enum | `src/.../<domain>/` | See `src/.../AGENTS.md` for the pattern |
| Add/change protobuf conversion | `src/.../<domain>/proto/<namespace>/` | Per API namespace; only `v1alpha8` exists |
| Shared enum proto helper | `src/.../proto/_enum.py` | `enum_from_proto` used by every enum wrapper |
| Reusable enum test scaffold | `src/.../test/enum_parity.py` | `EnumParityTest` base class |
| Add tests | `tests/<domain>/...` | Mirrors src tree; see `tests/AGENTS.md` |
| Docs API pages | `docs/_scripts/mkdocstrings_autoapi.py` | Pages are auto-generated from docstrings |

## CONVENTIONS

- All config is in `pyproject.toml`.
- Formatting: `black` line 88 + `isort` (black profile). `flake8` allows up to 100.
- `mypy --strict`, `explicit_package_bases`, package root `frequenz.client.common`.
- `pytest`: warnings are errors (`filterwarnings = ["error", ...]`), `asyncio_mode = "auto"`,
  `-vv`, `testpaths = ["tests", "src"]` (docstring examples in `src/` run via Sybil/conftest).
- pydoclint: Google-style docstrings, types in signature only (not in docstring).
- This library is strict about breaking changes and follows this guide:
  https://github.com/frequenz-floss/docs/blob/v0.x.x/python/semver-0.x.x.md
  Before making breaking changes that file should be read and followed.

## ANTI-PATTERNS (THIS PROJECT)

- Do NOT add type-in-docstring args (pydoclint: `arg-type-hints-in-docstring = false`).
- Do NOT introduce new runtime deps casually; this is a low-level shared lib.
- Do NOT make breaking changes without asking first.

## COMMANDS

```bash
python -m pip install -e .[dev]          # full dev install
nox                                       # all checks (creates own venvs)
nox -R -s pytest -- tests/test_*.py       # tests, reuse env
nox -R -s pylint -- ...                   # lint;  nox -R -s mypy -- ...  for types
pytest                                    # direct run (needs .[dev-pytest])
mkdocs serve                              # live docs preview
python -m build                           # sdist + wheel
```

## NOTES

- Releasing: tag a signed `vX.Y.Z` from `RELEASE_NOTES.md`; PRs touching `src/**` must update
  `RELEASE_NOTES.md` unless labeled `cmd:skip-release-notes`. See `CONTRIBUTING.md`.
- Conversion functions are always tied to a `frequenz.api.common` namespace (`v1alpha8` only for
  now) and live in `<domain>/proto/<namespace>/`; new namespaces get sibling `proto/v1alphaN/`
  dirs rather than edits in place. Tests mirror src with the package prefix stripped:
  `src/frequenz/client/common/<path>/_yyy.py` → `tests/<path>/test_yyy.py`.
