# Pattern Library — streamtex-patterns

This is the **global index** of the streamtex-patterns repository. It
lists every pattern with its scope and a short description.

> **Note**: this index lists what's **available in the repo**.
> Each consumer project also has its own `_pattern_library.md` that
> lists what's actually **installed** in that project (auto-regenerated
> by `stx patterns install/update`).

<!-- BEGIN AUTO -->
| Name | Scope | Description | Tags | Extrapolable |
|---|---|---|---|---|
| ptn_slide_heading | core | Two-cell heading row (title + tooltip icon) at the top of a slide | atom, heading, layout | ✓ |
| ptn_cite | core | Inline source citation with author, year, and optional URL | citation, evidence, footer | ✗ |
| ptn_inline_emphasis | core | Inline keyword/label/accent variants for mixed-style text | inline, text, emphasis | ✓ |
| ptn_callout | core | Highlighted box for emphasized content (info/warning/critical/success) | callout, container, emphasis | ✓ |
| ptn_card_grid | core | Grid of equal-size cards with title and body | grid, cards, taxonomy | ✓ |
| ptn_comparison_table | core | Multi-column comparison table with header row and aligned rows | grid, table, comparison | ✓ |
| ptn_takeaways | core | Numbered list of 3–5 key takeaways with bold lead and explanation | list, summary, conclusion | ✓ |
| ptn_term_definition_list | core | Vertical list of `term — definition` rows for glossaries, notations, abbreviation tables | list, glossary, reference, definitions | ✓ |
| ptn_title_slide | slides | Title slide with hero image, title, subtitle, and author | template, title, slide | ✓ |
| ptn_stat_hero | slides | Slide centerpiece — a single oversized statistic with body and source | stat, evidence, hero | ✓ |
| ptn_evidence_insight | slides | Slide template combining stat hero, body, takeaways, and source | template, evidence, slide | ✓ |
| ptn_exercise_flow | slides | Slide template for timed exercises — briefing, action, debrief | template, exercise, practice, slide | ✓ |
| ptn_categorized_grid | slides | Grid of cards organised in named categories with category headers | grid, cards, categories, taxonomy | ✓ |
| ptn_narrative_transition | slides | Bridge slide pivoting from a problem state to the proposed solution / methodology | template, narrative, transition, slide | ✓ |
| ptn_manual_section | docs | Documentation section — heading + sub + explanation + code snippet + live demo | docs, manual, demo, code | ✓ |
| ptn_feature_walkthrough | docs | Multi-step feature presentation with numbered steps | docs, manual, walkthrough, tutorial | ✓ |
| ptn_api_reference_card | docs | Reference card for one StreamTeX API function | docs, api, reference | ✓ |
| ptn_composite_block | docs | Composite block aggregating several atomic sub-blocks via st_include | docs, manual, composition, atomic | ✓ |
| ptn_transition_gse | projects/ai4se6d | ai4se6d-specific transition slide pivoting a section into the GSE-One methodology | template, narrative, transition, slide, ai4se6d, gse-one | ✗ |
<!-- END AUTO -->

## Presets

| Preset | Includes | Use case |
|---|---|---|
| `core` | 7 universal patterns | Any StreamTeX project |
| `slides` | core + 5 slide patterns | Presentations, courses |
| `docs` | core + 4 docs patterns | Manuals, references |
| `minimal` | 3 atoms only | Lightweight projects |
| `ai4se6d` | extends slides + ai4se6d-specific | The AI4SE6D collection |

## Scopes

- **core/** — universal, cross-project (atoms + molecules)
- **slides/** — slide-based courses and presentations
- **docs/** — StreamTeX-docs-style manuals (code + explanation + demo)
- **projects/<X>/** — patterns ultra-specific to a single project

## Application rules (manual)

### When generating a block

1. Read this index first to know what patterns are available.
2. If the user names a pattern, read its `<scope>/<name>.md` in full
   before generating code.
3. Respect each pattern's INVARIANTS strictly.
4. Adapt the code skeleton to the project's `custom/styles.py` and
   palette — the skeleton is a **starting point**.
5. If a referenced pattern doesn't exist, generate inline and propose
   `/stx-pattern:new`.

### Slides vs Docs — frontier

| Project type | Use scope | Why |
|---|---|---|
| Course / training / talk | `core` + `slides` | High visual impact, narrative arc |
| StreamTeX manual / reference | `core` + `docs` | Code-centric, demo-driven |
| Hybrid (workshop with demos) | `core` + `slides` + `docs` | Both modes coexist |

Patterns in `slides/` (e.g. `ptn_stat_hero`, `ptn_evidence_insight`) are
visually dramatic — using them in a manual is wrong. Patterns in
`docs/` (e.g. `ptn_manual_section`, `ptn_api_reference_card`) assume the
`show_code` / `show_explanation` helpers — using them in slides is
wrong.

### Cross-references

A pattern may reference another by name (e.g. `ptn_evidence_insight`
references `ptn_stat_hero`, `ptn_takeaways`, `ptn_cite`). Resolution is automatic:
Claude reads the referenced pattern when needed. If broken, fall back
to inline generation and propose `/stx-pattern:new`.
