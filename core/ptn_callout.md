---
name: ptn_callout
type: pattern
description: Highlighted box for emphasized content (info / warning / critical / success variants)
tags: [callout, container, emphasis]
extrapolable: true
since: 2026-05-10
---

# Callout

A small framed container that visually lifts a piece of content out of
the surrounding flow. Used for definitions, warnings, key insights,
quotes, and "what's missing" callouts. Variants are differentiated by
background tint and inline accent style.

## Visual

```
   ┌─────────────────────────────────────────┐
   │  Knowledge Capitalization                │   ← accent label
   │                                          │
   │  No compound phase                       │   ← body
   └─────────────────────────────────────────┘
```

## Structure

- A `with st_block(s.project.containers.callout)` block.
- First line: an accent / label heading using one of the inline emphasis
  variants (`accent`, `highlight`, `keyword`, `critical`, `success`).
- Optional spacer (`st_space("v", 0.5)`).
- Body: one or two `st_write(bs.body_c, ...)` lines.
- The variant (info / warning / critical / success) is encoded by the
  **inline label color**, not by a different container — the callout backgrounds stays uniform per project.

## Styling rules

| Variant | Label inline style | Use case |
|---|---|---|
| info | `bs.accent` (= `s.bold + s.project.colors.accent`) | neutral emphasis, definition |
| warning | `bs.highlight` (= `s.bold + s.project.colors.highlight`) | risk, caveat, paradox |
| critical | `bs.critical` if defined, else `bs.highlight` | hard warning |
| success | `bs.success` (= `s.bold + s.project.colors.success`) | confirmation, win |
| key | `bs.keyword` (= `s.bold + s.project.colors.primary`) | dominant insight |

| Element | Property | Value |
|---|---|---|
| Container | composition | `s.project.containers.callout` |
| Body | style | `bs.body_c` (= `s.Large + s.center_txt + s.text.wrap.hyphens`) |
| Inner spacer | size | `st_space("v", 0.5)` |

## Code skeleton

```python
from streamtex import st_block, st_write, st_space
from custom.styles import Styles as s

class BlockStyles:
    body_c = Style.create(s.Large + s.center_txt + s.text.wrap.hyphens, "co_body_c")
    accent = Style.create(
        s.Large + s.bold + s.project.colors.accent + s.center_txt, "co_acc",
    )
    highlight = Style.create(
        s.Large + s.bold + s.project.colors.highlight + s.center_txt, "co_hl",
    )
bs = BlockStyles

def build():
    # Single ptn_callout
    with st_block(s.project.containers.callout):
        st_write(bs.accent, "<Label>")
        st_space("v", 0.5)
        st_write(bs.body_c, "<Body line>")

    # Multiple callouts in a card grid
    with st_grid(
        cols="repeat(auto-fit, minmax(280px, 1fr))",
        gap="24px",
    ) as g:
        for label, body in ITEMS:
            with g.cell():
                with st_block(s.project.containers.callout):
                    st_write(bs.accent, label)
                    st_space("v", 0.5)
                    st_write(bs.body_c, body)
```

## Extrapolation rules

### INVARIANTS (never change)

- Background container is always `s.project.containers.callout` — never
  inline a custom box style. The variant is encoded **only** by the
  label color.
- Each callout has at most one label and one short body block
  (1–3 lines). Long content does not belong in a callout.
- The label sits on the first line, the body underneath, with a small
  vertical spacer between.
- Callouts are centered (`s.center_txt`) — they are visually
  self-contained units, not inline text.

### PARAMS (adjustable)

- Variant: info / warning / critical / success / key (chosen by label
  inline color).
- Body length: 1 to 3 lines. Above 3, prefer a `ptn_card_grid` cell or
  paragraph.
- Multiple callouts can be laid out in a `ptn_card_grid` (each cell holds
  one callout) — useful for "what's missing" / "key takeaways" slides.
- The label may be omitted for purely visual emphasis (rare).

### INTERDITS (forbidden)

- Do not stack 4+ lines of body in a callout — it stops being a callout
  and becomes a paragraph.
- Do not nest callouts inside callouts.
- Do not customize the container background per callout — variant is
  signaled via inline label color, never via the container.
- Do not use callouts for navigation aids (titles, headings) — they are
  for emphasised body content only.

## When to use

- Definitions and key insights inside an explanatory slide.
- "Watch out" / "Note" / "Did you know" callouts.
- Quoted statements that need a visual frame.
- Grids of "what's missing" / "key risks" — one callout per cell.

## When NOT to use

- Slide titles → `ptn_slide_heading`.
- Long quotes (4+ lines) → use a styled body paragraph.
- Hero statistics → `ptn_stat_hero` (callouts are not for big numbers).
- Lists of takeaways → `ptn_takeaways`.

## Examples

Live demo and gallery blocks (in the `stx_manual_patterns` documentation
manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_gallery_callouts.py` — every variant on one page
  (info, warning, critical, success).

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_card_grid` — N callouts laid out in a responsive grid
- `ptn_inline_emphasis` — supplies the variant accent colors
- `ptn_takeaways` — alternative when you need a numbered list rather than
  framed boxes
