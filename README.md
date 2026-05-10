# streamtex-patterns

Reusable graphic design patterns for StreamTeX projects.

A **pattern** is a markdown file with a name (e.g. `slide_heading`,
`callout`, `stat_hero`) and a structured description of a visual
primitive. Patterns are **read by Claude Code** when generating or
editing StreamTeX blocks, and the AI is then expected to reproduce or
extrapolate from them.

This repo is the **single source of truth** for the StreamTeX ecosystem.
Projects install patterns via the `stx patterns` CLI (or, in phase 1,
manually following the same conventions).

---

## Structure

```
streamtex-patterns/
├── manifest.toml             # repo metadata + presets registry
├── _pattern_library.md       # human-readable global index
│
├── core/                     # universal, cross-project
│   ├── slide_heading.md
│   ├── cite.md
│   ├── inline_emphasis.md
│   ├── callout.md
│   ├── card_grid.md
│   ├── comparison_table.md
│   └── takeaways.md
│
├── slides/                   # presentation / course-specific
│   ├── title_slide.md
│   ├── stat_hero.md
│   ├── evidence_insight.md
│   ├── exercise_flow.md
│   └── categorized_grid.md
│
├── docs/                     # StreamTeX-docs-style manuals
│   ├── manual_section.md
│   ├── feature_walkthrough.md
│   ├── api_reference_card.md
│   └── composite_block.md
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

See [`core/slide_heading.md`](core/slide_heading.md) for a complete
example.

---

## Installation in a project

Once `stx patterns` is implemented in the StreamTeX CLI:

```bash
# Install a preset (recommended)
stx patterns install --preset slides
stx patterns install --preset docs

# Or pick individual patterns
stx patterns install --pattern slide_heading,callout,stat_hero

# Update (with drift detection)
stx patterns update

# Status
stx patterns status

# Promote a local edit back to this repo
stx patterns promote callout
```

The CLI copies patterns into `<project>/.claude/custom/streamtex-patterns/`
and tracks origin/SHA in `.patterns-meta.json`.

### Source resolution (no env var)

The CLI resolves the source of patterns through TOML config (no
environment variable, by design — keeps state in files for portability):

1. `--source <path>` (CLI flag, override)
2. `[patterns].source` in `<project>/stx.toml` or `pyproject.toml`
3. `[patterns].source` in `<workspace>/stx.toml`
4. Auto-discover: `<workspace>/streamtex-patterns/`
5. Otherwise: error with the list of paths tried.

Example workspace config (`streamtex-dev/stx.toml`):

```toml
[patterns]
source = "./streamtex-patterns"
default_preset = "slides"
```

Example project config (`projects/ai4se6d/stx.toml`):

```toml
[patterns]
source = "../../streamtex-patterns"
preset = "ai4se6d"
```

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
