# scripts/

Repository tooling for `streamtex-patterns`. All scripts here are
**self-contained**: they run with Python 3.11+ and PyYAML only — they
do not require the `streamtex` library to be installed.

## `validate.py`

Validates pattern files (`<scope>/<name>.md`) against the A2 spec.
Implements the rules described in
`streamtex/documentation/maintenance/streamtex-patterns/SPEC.md`
(rules `PV001`-`PV020`), plus repo-level coherence checks for the
`presets/*.toml` files and the `_pattern_library.md` AUTO block.

### Requirements

```bash
python --version    # 3.11 or newer (uses tomllib stdlib)
pip install pyyaml
```

### Usage

Validate the entire repository (used by CI):

```bash
python scripts/validate.py --all
```

Validate one or more specific files:

```bash
python scripts/validate.py core/cite.md slides/title_slide.md
```

CI-strict mode — treat warnings as errors:

```bash
python scripts/validate.py --all --warnings-as-errors
```

Quiet mode — only print errors (warnings and info suppressed):

```bash
python scripts/validate.py --all --quiet
```

### Exit codes

| Code | Meaning |
|---|---|
| 0 | No errors (warnings may still be present) |
| 1 | One or more errors found |
| 2 | Usage error or repo not found |

### What it checks

- **Per pattern file** (`core/`, `slides/`, `docs/`, `projects/<X>/`):
  - frontmatter delimiters, YAML parse, required fields, no unknown keys
  - `name` matches filename, snake_case, ISO date for `since`
  - all six required H2 sections present, no duplicates, canonical order
  - `## Code skeleton` has exactly one ` ```python ` fence that parses
    with `ast.parse(...)`
  - `extrapolable: true` ⇒ `## Extrapolation rules` with `INVARIANTS`,
    `PARAMS`, `INTERDITS` (each with ≥ 2 items)
  - `## When to use` / `## When NOT to use` are 2-6 bullet lists
  - `## Visual` ≤ 500 chars; trailing newline; `When NOT to use` casing
- **Per preset** (`presets/*.toml`):
  - parses as TOML
  - every path under `[patterns].include` exists on disk
- **`_pattern_library.md`**:
  - `<!-- BEGIN AUTO --> … <!-- END AUTO -->` block exists
  - every entry resolves to a real file under a scope directory
  - every pattern file on disk is listed in the AUTO block

### Severity

- **error** — CI rejects the PR (exit code 1).
- **warning** — CI accepts but prints the diagnostic (`-W` upgrades to error).
- **info** — purely advisory.

## CI integration

`.github/workflows/validate.yml` runs `python scripts/validate.py --all`
on every PR targeting `main` or `develop`, and on every push to `main`.

## Pre-commit hook

`.pre-commit-config.yaml` declares a `local` hook that runs the same
command before each commit. Install once:

```bash
pip install pre-commit
pre-commit install
```

Bypass with `git commit --no-verify` if absolutely needed (not
recommended — the CI will reject the PR anyway).
