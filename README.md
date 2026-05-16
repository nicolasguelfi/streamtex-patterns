# streamtex-patterns

Reusable graphic design patterns for StreamTeX projects.

A **pattern** is a markdown file with a name (e.g. `ptn_slide_heading`,
`ptn_callout`, `ptn_stat_hero`) and a structured description of a visual
primitive. Patterns are **read by Claude Code** when generating or
editing StreamTeX blocks, and the AI is then expected to reproduce or
extrapolate from them.

This repo is the **single source of truth** for the StreamTeX ecosystem.
Projects install patterns via the `stx patterns` CLI — interactively or
declaratively, never automatically. Pattern selection is *subjective*: an
empty project starts with zero patterns and the user picks what fits.

---

## Structure

```
streamtex-patterns/
├── manifest.toml             # repo metadata + presets registry
├── _pattern_library.md       # human-readable global index
│
├── core/                     # universal, cross-project
│   ├── ptn_slide_heading.md
│   ├── ptn_cite.md
│   ├── ptn_inline_emphasis.md
│   ├── ptn_callout.md
│   ├── ptn_card_grid.md
│   ├── ptn_comparison_table.md
│   └── ptn_takeaways.md
│
├── slides/                   # presentation / course-specific
│   ├── ptn_title_slide.md
│   ├── ptn_stat_hero.md
│   ├── ptn_evidence_insight.md
│   ├── ptn_exercise_flow.md
│   └── ptn_categorized_grid.md
│
├── docs/                     # StreamTeX-docs-style manuals
│   ├── ptn_manual_section.md
│   ├── ptn_feature_walkthrough.md
│   ├── ptn_api_reference_card.md
│   └── ptn_composite_block.md
│
├── projects/                 # ultra-specific to one project
│   ├── ai4se6d/
│   └── streamtex-docs/
│
└── presets/                  # named recipes for installation
    ├── core.toml             # core/* only
    ├── slides.toml           # core/* + slides/*
    ├── docs.toml             # core/* + docs/*
    ├── minimal.toml          # 3 atoms only
    └── ai4se6d.toml          # full ai4se6d set
```

## Pattern format (spec A2)

Every pattern file has YAML frontmatter + structured markdown sections:

- `## Visual` — short description / ASCII mockup
- `## Structure` — logical grammar
- `## Styling rules` — exact reproducibility (table)
- `## Code skeleton` — concrete StreamTeX starting point
- `## Extrapolation rules` — INVARIANTS / PARAMS / INTERDITS
- `## When to use` / `## When NOT to use`
- `## Examples` / `## Related patterns` (optional)

See [`core/ptn_slide_heading.md`](core/ptn_slide_heading.md) for a complete
example.

---

## Installation in a project

Two paths get patterns into a project — pick one.

### A) Interactive picker (recommended on a TTY)

```bash
# Open a checkbox-style multi-select grouped by scope.
# Already-installed patterns are pre-checked; re-run any time to revisit.
stx patterns install

# Narrow the picker with a frontmatter tag (case-insensitive).
stx patterns install --tag slide
```

Non-TTY contexts (CI, scripts) refuse this form with a clear error — use
the explicit flags below.

### B) Declarative flags (composable)

`--preset`, `--pattern`, and `--exclude` can be combined in any way.
`--all` is exclusive with `--preset` and `--pattern` (but still accepts
`--exclude`).

```bash
# A single preset
stx patterns install --preset slides

# Multiple presets at once (their patterns union together)
stx patterns install --preset slides --preset docs

# A preset PLUS extra individuals
stx patterns install --preset slides --pattern ptn_inline_emphasis

# A preset MINUS some patterns
stx patterns install --preset slides --exclude ptn_takeaways

# Everything except a few
stx patterns install --all --exclude ptn_takeaways,ptn_categorized_grid

# Hand-picked list (no preset)
stx patterns install --pattern ptn_slide_heading,ptn_callout,ptn_stat_hero

# Positional names also work (equivalent to --pattern)
stx patterns install ptn_slide_heading ptn_callout
```

### Lifecycle

```bash
stx patterns status                # drift between installed copy and source
stx patterns sync                  # apply recorded intent on a fresh clone
stx patterns update                # pull source-side updates (drift-aware)
stx patterns diff ptn_callout      # local-vs-source for one pattern
stx patterns remove ptn_callout    # uninstall one pattern
stx patterns promote ptn_callout   # push a local edit back to this repo
```

The CLI copies patterns into `<project>/.claude/custom/streamtex-patterns/`
and records two things:

* `.patterns-meta.json` — execution cache (SHA per pattern, drift baseline).
* `<project>/stx.toml [patterns.selection]` — your *intent* (preset name,
  hand-picked list, or `all`). Versioned with the project, so a fresh
  `git clone` followed by `stx patterns sync` rebuilds the same set.

### Bootstrap from a fresh project

When you scaffold a project with `stx install --project <name>` and no
patterns source is yet reachable, an **opt-in prompt** offers to clone
the official patterns repo into the workspace, then to open the picker.
Both questions default to NO; pass `--no-patterns` to skip them entirely
(also skipped silently in CI / non-TTY).

```bash
stx install --project hello --no-patterns   # don't ask about patterns
```

### Source resolution (no env var)

The CLI resolves the source of patterns through TOML config (no
environment variable, by design — keeps state in files for portability):

1. `--source <path>` (CLI flag, override)
2. `[patterns].source` in `<project>/stx.toml` or `pyproject.toml`
3. `[patterns].source` in `<workspace>/stx.toml`
4. Auto-discover: `<workspace>/streamtex-patterns/`
5. Otherwise: error with the per-level trace + a hint.

Use the `source` subgroup to inspect or change the resolution:

```bash
# Show what each R4 level probed (great for debugging "source not found")
stx patterns source show

# Clone the official repo into the workspace (R4 level 4)
stx patterns source clone

# Symlink to an existing clone (share one checkout across workspaces)
stx patterns source link /path/to/my/streamtex-patterns

# Record a custom path in stx.toml without cloning
stx patterns source set ../shared/patterns
```

Example workspace config (`streamtex-dev/stx.toml`):

```toml
[patterns]
source = "./streamtex-patterns"

[patterns.selection]
mode = "preset"
items = ["slides"]
```

Example project config (`projects/ai4se6d/stx.toml`) — composite selection:

```toml
[patterns]
source = "../../streamtex-patterns"

[patterns.selection]
presets = ["slides", "docs"]            # multiple presets are unioned
individuals = ["ptn_inline_emphasis"]   # extra patterns on top
excludes = ["ptn_takeaways"]            # subtracted from the union
all = false                             # true = "every pattern, subject to excludes"
```

Hand-edited shortcuts are accepted on read (the canonical sub-table form
is restored on the next `stx patterns install`):

```toml
[patterns]
preset = "slides"         # → presets=["slides"]
selected = ["ptn_x"]      # → individuals=["ptn_x"]
all = true                # → all=true
```

The old v2 shape (`mode = "..."` + `items = [...]`) is also accepted on
read and silently migrated to the v3 composite form on the next write.

---

## Modes — `copy` (default) vs `symlink`

| Mode | Use when |
|---|---|
| `copy` (default) | Consumer project — robust, portable, snapshot in git |
| `symlink` | Pattern author iterating — edits are live |

```bash
stx patterns install --preset slides --mode symlink   # for pattern authors
```

---

## Update strategy — drift detection

`.patterns-meta.json` (in the consumer project) stores the SHA of each
pattern at install time. `stx patterns update` compares:

| Local SHA | Source SHA | Action |
|---|---|---|
| unchanged | unchanged | skip |
| unchanged | changed | update silently |
| changed | unchanged | skip + info |
| changed | changed | refuse + suggest `diff` / `promote` / `--force` |

This guarantees no silent loss of local edits.

---

## Contributing a pattern

1. Decide the scope: `core/`, `slides/`, `docs/`, or `projects/<X>/`.
2. Create `<scope>/<name>.md` following the format A2 spec.
3. Update `_pattern_library.md` (or run `stx pattern reindex` after install).
4. If the pattern fits an existing preset, update the preset's
   `presets/<preset>.toml` if needed.
5. Open a PR. CI validates the format A2.

---

## License

(TBD — same as the StreamTeX ecosystem.)
