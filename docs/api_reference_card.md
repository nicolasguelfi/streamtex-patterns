---
name: api_reference_card
type: pattern
description: Reference card for one StreamTeX API function — signature, params, return, example
tags: [docs, api, reference]
extrapolable: true
since: 2026-05-10
---

# API Reference Card

A focused documentation block describing **one** StreamTeX API function
(or class). Provides signature, parameter details, return semantics, a
minimal usage example, and pointers to related functions. Used in
reference manuals to give a single canonical entry per API symbol.

## Visual

```
   st_grid(cols, gap=None, cell_styles=None)               ← bs.heading

   Lay out content in a CSS grid container.                ← bs.lead

   Parameters:                                             ← bs.sub
     cols          int | str        Column spec
                                    (3 = 3 equal cols; "1fr 2fr" = ratio)
     gap           str | None       CSS gap (e.g. "12px")
     cell_styles   Style | None     Style applied to every cell

   Returns:                                                ← bs.sub
     A context manager exposing .cell() for each child cell.

   Example:                                                ← bs.sub
     [show_code]
     with st_grid(cols=3, gap="12px") as g:
         with g.cell(): st_write(s.large, "A")
         with g.cell(): st_write(s.large, "B")
         with g.cell(): st_write(s.large, "C")

   See also: st_block, st_span, st_list                    ← bs.related
```

## Structure

- One block per API symbol (or one block per cohesive group of related
  symbols).
- Heading: the function signature in monospace style.
- Lead: one-line summary of what the function does.
- Three sub-sections: `Parameters`, `Returns`, `Example`.
- Optional `See also` line listing related symbols.
- The Example sub-section uses `show_code` (and optionally a live demo
  rendering the example).

## Styling rules

| Element | Property | Value |
|---|---|---|
| Heading | style | `s.project.titles.section_title + s.text.fonts.font_monospace + s.center_txt` (or project's `code_title`) |
| Lead summary | style | `s.project.titles.body` (or `body_c` for centered) |
| Sub-heading | style | `s.project.titles.section_subtitle` |
| Param table | layout | small `st_grid(cols="1fr 1fr 3fr")` rows or definition list |
| Param name | inline style | `bs.keyword` (bold + primary) |
| Param type | inline style | `bs.accent` (bold + accent, often italic) |

## Code skeleton

```python
"""API reference: <function_name>."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    heading = s.project.titles.section_title + s.text.fonts.font_monospace + s.center_txt
    lead = s.project.titles.body + s.center_txt
    sub = s.project.titles.section_subtitle
    keyword = s.bold + s.project.colors.primary
    accent = s.bold + s.project.colors.accent
    body = s.project.titles.body
bs = BlockStyles


PARAMS = [
    ("cols", "int | str", "Column spec (3 = 3 equal cols; \"1fr 2fr\" = ratio)"),
    ("gap", "str | None", "CSS gap (e.g. \"12px\")"),
    ("cell_styles", "Style | None", "Style applied to every cell"),
]
RELATED = ["st_block", "st_span", "st_list"]


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "st_grid(cols, gap=None, cell_styles=None)",
                 tag=t.div, toc_lvl="1")
        st_space("v", 1)
        st_write(bs.lead, "Lay out content in a CSS grid container.")
        st_space("v", 2)

        # ---- Parameters ----
        st_write(bs.sub, "Parameters", toc_lvl="+1")
        st_space("v", 0.5)
        with st_grid(cols="1fr 1fr 3fr", gap="8px") as g:
            for name, type_, doc in PARAMS:
                with g.cell():
                    st_write(bs.body, (bs.keyword, name))
                with g.cell():
                    st_write(bs.body, (bs.accent, type_))
                with g.cell():
                    st_write(bs.body, doc)
        st_space("v", 2)

        # ---- Returns ----
        st_write(bs.sub, "Returns", toc_lvl="+1")
        st_space("v", 0.5)
        st_write(bs.body, "A context manager exposing .cell() for each child cell.")
        st_space("v", 2)

        # ---- Example ----
        st_write(bs.sub, "Example", toc_lvl="+1")
        st_space("v", 0.5)
        show_code("""\
with st_grid(cols=3, gap="12px") as g:
    with g.cell(): st_write(s.large, "A")
    with g.cell(): st_write(s.large, "B")
    with g.cell(): st_write(s.large, "C")""")
        st_space("v", 2)

        # ---- See also ----
        st_write(bs.body, (bs.keyword, "See also: "),
                 ", ".join(RELATED))
```

## Extrapolation rules

### INVARIANTS (never change)

- The card has the **function signature as heading** in monospace.
- Always three core sections in this order: `Parameters`, `Returns`,
  `Example`.
- The Example uses `show_code` and shows **realistic, runnable code**
  (not pseudo-code).
- The lead summary is **one sentence**, factual, no marketing voice.

### PARAMS (adjustable)

- Number of parameters in the table: 0 (no params) to ~10. Above ~10,
  consider grouping related params or splitting the function doc.
- Parameter table format: 3-column grid (default) or definition list
  (alternative).
- Optional sections: `Notes`, `Raises`, `Deprecated`, `Changed in <vX>`.
- Live demo after the Example is allowed when the function output is
  visual.

### INTERDITS (forbidden)

- Do not use this pattern for tutorials or walkthroughs — that's
  `feature_walkthrough`'s role.
- Do not omit the function signature — it's the heading.
- Do not mix multiple unrelated functions in the same card — split.
- Do not use slide patterns (`stat_hero`, etc.) here — wrong context.

## When to use

- Reference manuals (developer docs).
- One-symbol-per-page documentation in autogenerated or hand-written
  references.
- Cheatsheet entries that need more depth than a one-liner.

## When NOT to use

- Tutorial-style content → `feature_walkthrough`.
- Conceptual sections → `manual_section`.
- Quick lists of all functions → use a `card_grid` or
  `comparison_table`.

## Related patterns

- `manual_section` — when the doc is broader than one function
- `feature_walkthrough` — for goal-oriented tutorials using the function
- `card_grid` — for cataloging many functions in a list view
- `inline_emphasis` — used for parameter names and types
