---
name: ptn_card_grid
type: pattern
description: Grid of equal-size cards with title and body, used for taxonomies and inventories
tags: [grid, cards, taxonomy]
extrapolable: true
since: 2026-05-10
---

# Card Grid

A responsive grid of equal-weight "cards", each containing a short
keyword/title and an optional body. Used for taxonomies, inventories of
risks/tasks/principles, and any list-like content where each item
deserves a small visual container.

## Visual

```
┌────────────┐ ┌────────────┐ ┌────────────┐
│ AgileGen   │ │ SE 3.0     │ │ MAISTRO    │
│ Gherkin +  │ │ intent-    │ │ 7-phase    │
│ memory     │ │ centric    │ │ agile      │
└────────────┘ └────────────┘ └────────────┘
```

## Structure

- Outer container: `st_block(<page_fill>)`.
- Optional `ptn_slide_heading` at the top.
- One `st_grid` with auto-fit columns:
  `cols="repeat(auto-fit, minmax(<W>, 1fr))"` where `<W>` is the minimum
  card width (typically `280px` to `360px`).
- Each cell uses a category-tinted style: `cell_primary_bg` (default),
  `cell_accent_bg` (highlighted), or `cell_active_bg` (current/featured).
- Inside each cell: `st_write(bs.body_c, (bs.keyword, "<title>"), (bs.body, " — <body>"))`.

## Styling rules

| Element | Property | Value |
|---|---|---|
| Cell (default) | container | `s.project.containers.cell_primary_bg + cell_pad_md + s.center_txt` |
| Cell (accent) | container | `s.project.containers.cell_accent_bg + cell_pad_md + s.center_txt` |
| Cell (active) | container | `s.project.containers.cell_active_bg + cell_pad_md + s.center_txt` |
| Card title | inline style | `bs.keyword` (uses `ptn_inline_emphasis`) |
| Card body | inline style | `bs.body` |
| Grid | cols | `"repeat(auto-fit, minmax(280px, 1fr))"` |
| Grid | gap | `"12px"` to `"24px"` |

## Code skeleton

```python
from streamtex import st_block, st_grid, st_write, st_space
from streamtex.enums import Tags as t
from custom.styles import Styles as s

class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    body = Style.create(s.Large + s.text.wrap.hyphens, "card_body")
    body_c = Style.create(s.Large + s.center_txt + s.text.wrap.hyphens, "card_body_c")
    keyword = s.bold + s.project.colors.primary
bs = BlockStyles

_cell = (
    s.project.containers.cell_primary_bg
    + s.project.containers.cell_pad_md
    + s.center_txt
)

CARDS = [
    ("AgileGen", "Gherkin + memory pool"),
    ("SE 3.0", "intent-centric"),
    ("MAISTRO", "7-phase agile"),
    # ... more cards
]

def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            st_write(bs.heading, "<Slide title>", tag=t.div, toc_lvl="1")
            st_space("v", 1)

            with st_grid(
                cols="repeat(auto-fit, minmax(280px, 1fr))",
                gap="12px",
                cell_styles=_cell,
            ) as g:
                for title, body in CARDS:
                    with g.cell():
                        st_write(
                            bs.body_c,
                            (bs.keyword, title),
                            (bs.body, f" — {body}"),
                        )
```

## Extrapolation rules

### INVARIANTS (never change)

- All cards share the same cell style within one grid (visual symmetry).
- Each card has a short keyword title (bolded with `ptn_inline_emphasis`)
  followed by an optional body fragment.
- Cards reflow responsively via `repeat(auto-fit, minmax(...))` — never
  hard-code the column count.
- The minimum card width (`<W>`) is between 280px and 360px so the cards
  remain legible at any viewport.

### PARAMS (adjustable)

- Number of cards: 2 to 12 (above 12, paginate or split into a
  `ptn_categorized_grid`).
- Cell tint: `primary` (neutral), `accent` (emphasized group), `active`
  (current/featured) — pick **one** per grid.
- Minimum card width (`280px`–`360px`) depending on body length.
- Cards may carry only a title (no body) or only a body (no title) when
  the message is uniform.
- Cards may include a tiny inline icon as part of the keyword.

### INTERDITS (forbidden)

- Do not mix two different cell tints within a single grid — to switch,
  use `ptn_categorized_grid` (multiple grids, each with its own tint).
- Do not embed images inside cards — illustrations belong outside the
  grid.
- Do not give cards drastically different heights by stuffing one with
  a long paragraph — keep card body to 1–2 lines.

## When to use

- Taxonomies of frameworks, principles, risks, tools.
- Inventory slides ("here are the 6 NFRs", "5 known dangers").
- Workshop instruction lists where each step is short.

## When NOT to use

- Comparable items across attributes → `ptn_comparison_table`.
- Cards with named categories → `ptn_categorized_grid`.
- Long-form descriptions → `ptn_callout` or body paragraphs.

## Examples

Live demo and gallery blocks (in the `stx_manual_patterns` documentation
manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_gallery_lists.py` — `card_grid` shown next to its
  cousins (`comparison_table`, `takeaways`).

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_categorized_grid` — when cards are organised in named groups
- `ptn_comparison_table` — when items differ across attributes rather than
  being independent
- `ptn_inline_emphasis` — used inside each card's title
