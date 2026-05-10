---
name: ptn_manual_section
type: pattern
description: Documentation section — heading + sub + explanation + code snippet + live demo
tags: [docs, manual, demo, code]
extrapolable: true
since: 2026-05-10
---

# Manual Section

The canonical "feature explanation" pattern in StreamTeX manuals: a
section heading, a sub-heading naming the specific topic, a short
written explanation, a code snippet (verbatim), and a live demonstration
that renders that exact code. Used pervasively across documentation manuals
manuals (intro, advanced, ai, ce, deploy, developer).

## Visual

```
   Section Title                                ← bs.heading (toc_lvl="1")

   Sub-topic A                                  ← bs.sub (toc_lvl="+1")

     [show_explanation]
     "Pass an integer to cols for equal-width columns."

     [show_code]
     with st_grid(cols=3, cell_styles=bs.cell) as g:
         with g.cell(): st_write(s.large, "Cell A1")
         ...

     [live demo — actually rendered]
     ┌──────┬──────┬──────┐
     │ A1   │ B1   │ C1   │
     └──────┴──────┴──────┘

   Sub-topic B                                  ← repeat
   ...
```

## Structure

- One block file (`bck_<topic>.py`) per coherent section.
- Outer container: `with st_block(s.center_txt):` (or absent — manuals
  are read in continuous mode).
- Section heading: `st_write(bs.heading, "<Topic>", tag=t.div, toc_lvl="1")`.
- For each sub-topic:
  1. `st_write(bs.sub, "<sub-topic>", toc_lvl="+1")`
  2. `show_explanation("""...""")` — short prose
  3. `show_code("""...""")` — code shown verbatim (the **same string**
     that would render the demo)
  4. The actual code, executed inline, producing the demo
- `st_space("v", 1)` between explanation/code/demo, `st_space("v", 2)`
  between sub-topics.
- Helpers `show_code`, `show_explanation`, `show_details` come from
  `blocks.helpers` (the manual's helper module).

## Styling rules

| Element | Property | Value |
|---|---|---|
| Heading | composition | `s.project.titles.section_title + s.center_txt` |
| Sub-heading | composition | `s.project.titles.section_subtitle` |
| Demo cell (when used) | composition | `s.container.borders.solid_border + small_padding + s.center_txt + vertical_center_layout` |
| Spacing — within sub-topic | size | `st_space("v", 1)` |
| Spacing — between sub-topics | size | `st_space("v", 2)` |
| `show_code` | source | `from blocks.helpers import show_code` |
| `show_explanation` | source | `from blocks.helpers import show_explanation` |

## Code skeleton

```python
"""<Topic> — manual section."""
from streamtex import *
from streamtex.styles import Style as ns
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.container.layouts.vertical_center_layout
    )
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "<Topic>", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # ---- Sub-topic A ----
        st_write(bs.sub, "<Sub-topic A>", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            <Short prose explaining what the snippet below demonstrates.>
        """)
        st_space("v", 1)

        show_code("""\
with st_grid(cols=3, cell_styles=bs.cell) as g:
    with g.cell(): st_write(s.large, "Cell A1")
    with g.cell(): st_write(s.large, "Cell B1")
    with g.cell(): st_write(s.large, "Cell C1")""")
        st_space("v", 1)

        # Live demo — same code as above, executed
        with st_grid(cols=3, cell_styles=bs.cell) as g:
            with g.cell(): st_write(s.large, "Cell A1")
            with g.cell(): st_write(s.large, "Cell B1")
            with g.cell(): st_write(s.large, "Cell C1")
        st_space("v", 2)

        # ---- Sub-topic B ----
        # ... repeat the same explanation / code / demo triad ...
```

## Extrapolation rules

### INVARIANTS (never change)

- The triad is **explanation → code → demo**, in that order. The reader
  reads "what + how + result".
- `show_code` displays **the exact same code** that the live demo
  executes. They are not allowed to drift.
- The section has one heading at `toc_lvl="1"` and sub-topics at
  `toc_lvl="+1"`. The TOC structure must follow.
- Helpers (`show_code`, `show_explanation`, `show_details`) are imported
  from the manual's helper module, never inlined.
- The block stays focused on **one feature topic** — split into multiple
  block files if the topic grows beyond ~5 sub-topics.

### PARAMS (adjustable)

- Number of sub-topics: 1 to ~5 per section.
- `show_details` may be added between explanation and code for an
  expandable deeper-dive (rare).
- The cell style for demos may vary (`solid_border` vs `dashed_border`,
  padding size).
- A sub-topic may **omit the live demo** when the code only illustrates
  syntax that doesn't render (e.g. configuration in `book.py`).
- Multiple code snippets per sub-topic are allowed (variant A / variant
  B), each followed by its own demo.

### INTERDITS (forbidden)

- Do not put the live demo before the code — the reader needs to know
  what they are about to see.
- Do not skip the explanation — even a one-line explanation anchors
  the reader.
- Do not duplicate `show_code` snippets for the same demo (DRY at the
  reader level — one snippet, one demo).
- Do not use slide-presentation patterns (`ptn_stat_hero`, `ptn_evidence_insight`)
  in a manual section — they are visually too dramatic for a docs context.

## When to use

- Any section of a StreamTeX manual that explains a feature with code.
- Tutorial-style content where the reader expects "show me the code +
  show me what it does".
- Reference sections that describe configuration options.

## When NOT to use

- Pure prose / narrative documentation → no helpers needed, regular
  `st_write` is enough.
- Conceptual sections without code → use a `ptn_callout` or plain text.
- One-shot API references with no demo → use `ptn_api_reference_card`.

## Examples

Live demo blocks (in the `stx_manual_patterns` documentation manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_gallery_docs.py` — `manual_section` showcased next to
  its peers (`feature_walkthrough`, `api_reference_card`,
  `composite_block`). The pattern is also applied by every
  `bck_gallery_*.py` and `bck_demo_*.py` block in the manual itself —
  the manual is the canonical, self-referential reference.

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_feature_walkthrough` — when a topic spans many small steps (more
  narrative / numbered)
- `ptn_api_reference_card` — when documenting a single function in detail
- `ptn_composite_block` — when a block aggregates several atomic blocks via
  `st_include`
- `ptn_callout` — for "Note" / "Warning" boxes within a section
