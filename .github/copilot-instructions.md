# GitHub Copilot Instructions - shortfx

## Project
Python library: 3000+ reusable functions organized like Excel formulas. Also a **deterministic AI agent toolset** via `llms.txt` + built-in MCP server (meta-tools: search → inspect → execute).

## Tech Stack
Python ≥3.10 · uv/pip · Hatchling · pytest · Optional: `mcp[cli]` (MCP server), `fastembed`+`truststore` (semantic search)

## Conventions
Style: [`python-development.instructions.md`](.github/instructions/python-development.instructions.md) · Tests: [`unit-tests.instructions.md`](.github/instructions/testing/unit-tests.instructions.md) · Docs: [`docs-changelog-sync.instructions.md`](.github/instructions/docs-changelog-sync.instructions.md)
English everywhere · `snake_case.py` → `<category>_functions.py` · ❌ No external runtime deps (stdlib only)

## Architecture
Flat hierarchy: 6 `fx*` packages → submodule files → public functions. `auto_export()` dynamically re-exports all public callables. `registry.py` walks `fx*` at runtime for JSON Schema + MCP exposure.

## Key Patterns
- **Dynamic Re-export** (`_loader.auto_export`): Each `fx*/__init__.py` calls `auto_export()` — no manual imports
- **⚠️ Shadowing risk**: `auto_export()` iterates `_SUBMODULES` in order — same-name functions silently shadow. Always verify uniqueness before adding
- **Automatic Discovery** (`registry.py`): Runtime introspection → OpenAI-compatible JSON Schemas
- **Dynamic MCP Meta-tools** (`mcp/server.py`): 6 meta-tools instead of 3000+ individual tools

## Base Classes
- `_loader.auto_export()` (`shortfx/_loader.py`): Central import machinery for all `fx*` packages
- `_validators` (`shortfx/_validators.py`): Shared validation (`ensure_type`, `ensure_numeric`, `ensure_positive`)
- `registry` (`shortfx/registry.py`): Tool discovery, schema generation, invocation dispatch
- `SemanticToolSearch` (`shortfx/semantic_search.py`): Vector-based function discovery via fastembed

---

## Key Abstractions

| Module | Purpose |
| ------ | ------- |
| `fxDate` | Date operations, evaluations, conversions, system dates |
| `fxNumeric` | Finance, statistics, geometry, transforms, series, number theory (30+ submodules) |
| `fxString` | Text manipulation, regex, hashing, validation, encoding, similarity, Spanish NLP |
| `fxPython` | Iterable utilities, type conversions, logic helpers |
| `fxExcel` | Excel-compatible formulas (VLOOKUP, PMT, CONCATENATE, etc.) |

And 1 more: `fxVBA` (VBA/Access-compatible functions) — see source.

| Function | Location | Purpose |
| -------- | -------- | ------- |
| `auto_export()` | `shortfx/_loader.py` | Dynamic re-export of submodule callables |
| `get_tool_schemas()` | `shortfx/registry.py` | Build JSON Schemas for all functions |
| `invoke_tool()` | `shortfx/registry.py` | Execute any function by qualified name |
| `search_tools()` | `shortfx/registry.py` | Keyword/semantic search across catalogue |
| `call_shortfx()` | `shortfx/mcp/server.py` | MCP tool: execute function with JSON args |

And 1 more: `search_shortfx_tools()` (MCP natural-language discovery) — see source.

## Configuration
- `pyproject.toml`: metadata, deps, build, entry points · `shortfx/mcp/mcp.json`: MCP client template
- Priority: function args → module defaults · No config files or env vars (pure library)

## Security
- ❌ No `eval()`/`exec()` — `scientific_calculate` uses AST-based parsing
- ❌ No external network calls (core fully offline; `fastembed` optional model download)
- ❌ Never hardcode secrets/API keys

## Best Practices
1. New function → correct `fx*/<category>_functions.py` · use `_validators` · Google docstring (`Args`, `Returns`, `Raises`, `Example`, `Complexity`) · **check name uniqueness**: `grep -rn "^def func_name(" shortfx/fxPackage/`
2. New file in existing module → add filename to `__init__.py` `_SUBMODULES` list
3. New module → `fx<Name>/` + `__init__.py` with `auto_export()` + update `README.md`
4. Doc changes → update `CHANGELOG.md` + module `README.md` + `llms.txt` together
5. Tests → one file per source module, `pytest.approx` for floats, `pytest.mark.parametrize` for data-driven
6. Error handling: use `_validators.py` helpers (not ad-hoc `isinstance`) · `TypeError`/`ValueError` with descriptive messages · MCP server catches all exceptions → structured error JSON

## Common Patterns
See [`patterns/common_patterns.md`](patterns/common_patterns.md) — load with `read_file` when implementing new code.

## Git
Conventional Commits · `feature/*`, `bugfix/*`, `hotfix/*` · Version: `pyproject.toml [project].version`
