---
name: ptn_categorized_grid
type: pattern
description: Grid of cards organised in named categories with category headers
tags: [grid, cards, categories, taxonomy]
extrapolable: true
since: 2026-05-10
---

# Categorized Grid

A vertical sequence of `ptn_card_grid` instances, each preceded by a
**category header**, where each category uses a different cell tint
(`primary` / `accent` / `active`). Used for taxonomies that have named
groups: "Adaptations / AI-Native / Process Plugins", "NEW / ELEVATED /
TRANSFORMED", etc.

## Visual

```
   Adaptations — Existing methods extended      ← category header (highlight)
   ┌──────────────┐ ┌──────────────┐
   │ AgileGen     │ │ Agentic DevOps│           ← cells: cell_primary_bg
   └──────────────┘ └──────────────┘

   AI-Native — Built for GenAI from scratch     ← category header
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │ SE 3.0       │ │ V-Bounce     │ │ Promptware   │ │ MAISTRO      │  ← cell_accent_bg
   └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

   Process Plugins — Portable methodology       ← category header
   ┌────────────────────────────────────┐
   │ Compound Engineering → GSE-One     │       ← cell_active_bg
   └────────────────────────────────────┘
```

## Structure

The pattern is a sequence of category sections. Each section is:

1. A category header — `st_write(bs.cat_label, "<Category — subtitle>")`
2. A small spacer — `st_space("v", 0.5)`.
3. A `ptn_card_grid` instance with the category's tint applied to all
   cells.
4. A vertical spacer between categories — `st_space("v", 1)`.

The **category tint mapping** follows project palette conventions:

| Tint | Container | Semantic role |
|---|---|---|
| primary | `cell_primary_bg` | "neutral" / "the existing" |
| accent | `cell_accent_bg` | "novelty" / "AI-native" |
| active | `cell_active_bg` | "current focus" / "this is where we land" |

## Styling rules

| Element | Property | Value |
|---|---|---|
| Category header | style | `s.Large + s.bold + s.project.colors.highlight + s.center_txt` (`bs.cat_label`) |
| Cell (primary) | container | `s.project.containers.cell_primary_bg + cell_pad_md + center_txt` |
| Cell (accent) | container | `s.project.containers.cell_accent_bg + cell_pad_md + center_txt` |
| Cell (active) | container | `s.project.containers.cell_active_bg + cell_pad_md + center_txt` |
| Each grid | cols | `"repeat(auto-fit, minmax(280px, 1fr))"` |
| Each grid | gap | `"12px"` |
| Vertical spacer between categories | size | `st_space("v", 1)` |

## Code skeleton

```python
from streamtex import st_block, st_grid, st_write, st_space
from streamtex.enums import Tags as t
from custom.styles import Styles as s

class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    body = Style.create(s.Large + s.text.wrap.hyphens, "ct_body")
    body_c = Style.create(s.Large + s.center_txt + s.text.wrap.hyphens, "ct_body_c")
    keyword = Style.create(s.Large + s.bold + s.project.colors.primary, "ct_kw")
    highlight = Style.create(
        s.Large + s.bold + s.project.colors.highlight + s.center_txt, "ct_hl",
    )
    cat_label = Style.create(
        s.Large + s.bold + s.project.colors.highlight + s.center_txt, "ct_cat",
    )
bs = BlockStyles

_cat_primary = (
    s.project.containers.cell_primary_bg
    + s.project.containers.cell_pad_md + s.center_txt
)
_cat_accent = (
    s.project.containers.cell_accent_bg
    + s.project.containers.cell_pad_md + s.center_txt
)
_cat_active = (
    s.project.containers.cell_active_bg
    + s.project.containers.cell_pad_md + s.center_txt
)

CATEGORIES = [
    ("Adaptations — Existing methods extended", _cat_primary, [
        ("AgileGen", "Gherkin + memory pool"),
        ("Agentic DevOps", "Microsoft vision"),
    ]),
    ("AI-Native — Built for GenAI from scratch", _cat_accent, [
        ("SE 3.0", "intent-centric"),
        ("V-Bounce", "V-model adapted"),
        ("Promptware", "SE for prompts"),
        ("MAISTRO", "7-phase agile"),
    ]),
    ("Process Plugins — Portable methodology", _cat_active, [
        ("Compound Engineering → GSE-One", ""),
    ]),
]

def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            st_write(bs.heading, "<Slide title>", tag=t.div, toc_lvl="1")
            st_space("v", 2)

            for label, cell_style, items in CATEGORIES:
                st_write(bs.cat_label, label)
                st_space("v", 0.5)

                with st_grid(
                    cols="repeat(auto-fit, minmax(280px, 1fr))",
                    gap="12px",
                    cell_styles=cell_style,
                ) as g:
                    for title, body in items:
                        with g.cell():
                            if body:
                                st_write(
                                    bs.body_c,
                                    (bs.keyword, title),
                                    (bs.body, f" — {body}"),
                                )
                            else:
                                st_write(bs.body_c, (bs.highlight, title))

                st_space("v", 1)
```

## Extrapolation rules

### INVARIANTS (never change)

- Each category has a header rendered with `bs.cat_label`
  (`highlight + bold + center_txt`).
- All cards within a single category share the same cell tint.
- Different categories use different tints — that's how the eye
  identifies the grouping.
- The `ptn_card_grid` cell semantics from the underlying pattern are
  preserved (responsive `auto-fit`, `minmax(280px, 1fr)`).
- Categories are stacked vertically, never side-by-side.

### PARAMS (adjustable)

- Number of categories: 2 to 4. Above 4, the eye loses the grouping —
  split into two slides.
- Number of cards per category: 1 to 8 (each `ptn_card_grid` instance
  follows its own params).
- Tint assignment: `primary → accent → active` (default progression),
  or `primary → accent` for binary groupings, or other mappings as
  long as each category has a distinct tint.
- Category header may include a dash-separated subtitle
  (`"<name> — <one-line description>"`).
- Final category may be highlighted with a single full-width "winner"
  card (see Process Plugins example).

- Category headers are phase labels (`"Day 1 — <theme>"`, `"Phase 2 —
  <theme>"`). The dash-separated subtitle becomes mandatory because it
  carries the phase's content.
- Inside each phase, the inner grid is **two columns** (typically
  `cols="1fr 1fr"` for Morning / Afternoon, or `cols="repeat(N, 1fr)"`
  for finer sub-divisions) — never `auto-fit`, because the temporal
  alignment depends on a fixed number of columns.
- The "current" phase uses the `active` tint to indicate "you are
  here"; past phases use `primary`; future phases use `accent` or a
  muted variant.
- All other INVARIANTS still apply: each phase has its header, all
  cards in a phase share the same tint, phases are stacked vertically.

Currently applied in ai4se6d as:
- `modules/ai4se6d_genai_intro/blocks/bck_intro_roadmap.py` (3-day
  schedule with the "current" day highlighted)
- `modules/ai4se6d_gensem/blocks/bck_gensem_roadmap.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_fw_agilegen_roadmap.py`

Do not use this variant for non-temporal groupings — the temporal
alignment guarantee only matters when phases follow each other in time.

### INTERDITS (forbidden)

- Do not reuse the same tint across two categories — the visual
  distinction must remain.
- Do not put a category with no header — naming the category is the
  whole point of the pattern.
- Do not nest sub-categories inside a category — promote them to a
  separate slide.
- Do not mix `ptn_card_grid` and `ptn_comparison_table` rows in the same
  pattern instance.

## When to use

- Multi-tier taxonomies of frameworks, principles, tools.
- Decision spectrums where each "zone" of the spectrum has its own
  group of items.
- Workshop content presenting "old way / new way / our way".

## When NOT to use

- Flat enumerations without categories → `ptn_card_grid`.
- Comparison across attributes → `ptn_comparison_table`.
- Single-stat focal slide → `ptn_stat_hero`.

## Variants

### Sequence / timeline variant

When the categories represent **temporal phases** rather than
qualitative groupings (Day 1 / Day 2 / Day 3, Phase 1 / Phase 2 / …,
Step 1 / Step 2 / …), the pattern adapts as follows:

- Category headers are phase labels (`"Day 1 — <theme>"`, `"Phase 2 —
  <theme>"`). The dash-separated subtitle becomes mandatory because it
  carries the phase's content.
- Inside each phase, the inner grid is **two columns** (typically
  `cols="1fr 1fr"` for Morning / Afternoon, or `cols="repeat(N, 1fr)"`
  for finer sub-divisions) — never `auto-fit`, because the temporal
  alignment depends on a fixed number of columns.
- The "current" phase uses the `active` tint to indicate "you are
  here"; past phases use `primary`; future phases use `accent` or a
  muted variant.
- All other INVARIANTS still apply: each phase has its header, all
  cards in a phase share the same tint, phases are stacked vertically.

Currently applied in ai4se6d as:
- `modules/ai4se6d_genai_intro/blocks/bck_intro_roadmap.py` (3-day
  schedule with the "current" day highlighted)
- `modules/ai4se6d_gensem/blocks/bck_gensem_roadmap.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_fw_agilegen_roadmap.py`

Do not use this variant for non-temporal groupings — the temporal
alignment guarantee only matters when phases follow each other in time.

## Examples

Live demo blocks (in the `stx_manual_patterns` documentation manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_demo_categorized_grid.py`
  — three named categories, each with its own tint and an inner grid
  of cards, plus the **sequence / timeline variant** rendered as a
  3-phase course schedule (Day 1 / Day 2 / Day 3) with the current
  day highlighted.

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_card_grid` — used as the building block within each category
- `ptn_slide_heading` — typically used as the title row above the grid
- `ptn_inline_emphasis` — used inside each card title
- `ptn_comparison_table` — alternative when items are comparable across
  attributes rather than grouped
