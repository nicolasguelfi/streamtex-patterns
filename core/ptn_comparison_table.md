---
name: ptn_comparison_table
type: pattern
description: Multi-column comparison table with header row and aligned rows
tags: [grid, table, comparison]
extrapolable: true
since: 2026-05-10
---

# Comparison Table

A grid laid out as a table with a styled header row and aligned data
rows. Used to compare items across attributes (Day vs morning vs
afternoon, Tool vs Autonomy vs Best for, etc.). Each row may be marked
"active" with a different cell style to draw the eye.

## Visual

```
┌────────────┬─────────────────────┬────────────────────────┐
│ Day 1      │ Morning content     │ Afternoon content      │  ← header
├────────────┼─────────────────────┼────────────────────────┤
│ Day 2      │ ...                 │ ...                    │
├────────────┼─────────────────────┼────────────────────────┤
│ Day 3 ★    │ ...                 │ ...                    │  ← active row
└────────────┴─────────────────────┴────────────────────────┘
```

## Structure

- Outer container: `st_block(<page_fill>)`.
- Optional `ptn_slide_heading` at the top.
- One `st_grid` per row of the table (no nested header — each row is its
  own grid, but they share `cols=` so columns line up visually).
- Header row: cells styled with `s.project.containers.table_header_cell`
  (or `cell_active_bg`) and `bs.table_hdr` text style.
- Data rows: cells styled with `s.project.containers.table_normal_cell`
  (or `cell_primary_bg`).
- Active rows (current day, recommended option): cells styled with
  `s.project.containers.table_active_cell` (or `cell_active_bg`).
- All grids share `gap="12px"` for vertical alignment.

## Styling rules

| Element | Property | Value |
|---|---|---|
| Header cell | container | `s.project.containers.table_header_cell` |
| Normal cell | container | `s.project.containers.table_normal_cell` (≈ `cell_primary_bg + cell_pad_sm + center_txt`) |
| Active cell | container | `s.project.containers.table_active_cell` (≈ `cell_active_bg + cell_pad_sm + center_txt`) |
| Header text | style | `s.project.titles.table_header` |
| Cell text | style | `s.project.titles.table_cell` (or `bs.body_c` for centered body) |
| Cell label (lead) | style | `s.project.titles.table_label` (or `+ active`) |
| Grid | gap | `"12px"` |

## Code skeleton

```python
from streamtex import st_block, st_grid, st_write, st_space
from streamtex.enums import Tags as t
from custom.styles import Styles as s

class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    table_hdr = s.project.titles.table_header
    table_txt = s.project.titles.table_cell
    table_lbl = s.project.titles.table_label
    table_lbl_active = s.project.titles.table_label_active
bs = BlockStyles

_hdr_cell = s.project.containers.table_header_cell
_normal_cell = s.project.containers.table_normal_cell
_active_cell = s.project.containers.table_active_cell

def _row(cells, cell_style=_normal_cell, label_style=None):
    """Render one row. cells = list of strings. label_style applied to first cell if set."""
    n = len(cells)
    cols = " ".join(["1fr"] * n)  # adjust ratios per row spec
    with st_grid(cols=cols, gap="12px", cell_styles=cell_style) as g:
        for i, txt in enumerate(cells):
            with g.cell():
                st_write((label_style or bs.table_txt) if i == 0 else bs.table_txt, txt)

def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            st_write(bs.heading, "<Comparison title>", tag=t.div, toc_lvl="1")
            st_space("v", 1)

            # Header
            _row(
                ["<Col 1 header>", "<Col 2 header>", "<Col 3 header>"],
                cell_style=_hdr_cell,
                label_style=bs.table_hdr,
            )

            # Data rows
            for label, c2, c3, is_active in DATA_ROWS:
                _row(
                    [label, c2, c3],
                    cell_style=_active_cell if is_active else _normal_cell,
                    label_style=bs.table_lbl_active if is_active else bs.table_lbl,
                )
```

## Extrapolation rules

### INVARIANTS (never change)

- All rows share the same `cols=` template so columns align vertically.
- The header row is always visually distinct (different cell style and
  text style).
- Active rows are marked with the `cell_active_bg` palette — never with
  inline color overrides.
- Each cell is single-line / short — long prose belongs in a `ptn_card_grid`
  or `ptn_callout`, not a comparison table.
- The first column is the row label (uses `table_label` style or the
  active variant).

### PARAMS (adjustable)

- Number of columns: 2 to 5 (above 5, vertical density becomes harmful;
  prefer two stacked tables).
- Number of rows: 2 to 8.
- Column ratios: equal (`1fr 1fr 1fr`) or weighted (`0.7fr 1.3fr 1fr`)
  depending on label length.
- Active row: 0 or 1 highlighted at a time. For more than one, the
  emphasis loses its function.
- The "row" abstraction may collapse two consecutive grids when one row
  spans the full width (e.g. Day label spans full width, then 2-column
  AM/PM row underneath — see `bck_intro_roadmap.py`).

### INTERDITS (forbidden)

- Do not embed images or AI illustrations in cells — they break vertical
  rhythm.
- Do not vary cell padding row-by-row — keep `cell_pad_sm` consistent.
- Do not use this pattern for nested taxonomies — use `ptn_categorized_grid`
  instead.

## When to use

- Course / day / session schedule overviews.
- Tool comparisons (Cursor vs Copilot vs Claude Code).
- Spectrum / paradigm tables (e.g. waterfall vs agile vs ad-hoc).
- Any "X across N attributes" comparison where each cell is short.

## When NOT to use

- Single-stat emphasis → `ptn_stat_hero`.
- Card-style enumerations of independent items → `ptn_card_grid`.
- Nested categories → `ptn_categorized_grid`.

## Examples

Live demo and gallery blocks (in the `stx_manual_patterns` documentation
manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_gallery_lists.py` — `comparison_table` with header
  row + 3 data rows.

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_slide_heading` — typically used as the title row above the table
- `ptn_card_grid` — alternative when items are independent rather than
  comparable across columns
- `ptn_categorized_grid` — alternative when rows belong to named categories
