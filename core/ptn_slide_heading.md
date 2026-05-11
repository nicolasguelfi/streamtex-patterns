---
name: ptn_slide_heading
type: pattern
description: Two-cell heading row (title + tooltip icon) at the top of a slide
tags: [atom, heading, layout]
extrapolable: true
since: 2026-05-10
---

# Slide Heading

The standard heading row used at the top of nearly every content slide in
StreamTeX presentation projects. A 2-column grid with the slide title on
the left (95%) and a small tooltip-icon hover area on the right (5%).

## Visual

```
┌──────────────────────────────────────────────────────────┬─┐
│   Slide title (centered, slide_title style)             │?│
└──────────────────────────────────────────────────────────┴─┘
```

The tooltip icon (`st_hover_tooltip`) reveals additional notes for the
presenter when hovered. It does not show by default.

## Structure

- One `st_grid` with `cols="95% 5%"` and `gap="0px"`.
- Left cell: the heading text (`bs.heading`), wrapped in `st_zoom(90)` to
  shrink slightly relative to the rest of the slide.
- Right cell: an `st_hover_tooltip(...)` with title + entries, positioned
  on the left so the popover doesn't overflow the screen.
- The title carries the navigation marker via `tag=t.div, toc_lvl="+1"`
  (or `toc_lvl="1"` for the first slide of a section).

## Styling rules

| Element | Property | Value |
|---|---|---|
| Heading style | composition | `s.project.titles.slide_title + s.center_txt` |
| Grid | cols | `"95% 5%"` |
| Grid | gap | `"0px"` |
| Grid | cell_styles | `s.project.containers.grid_cell_centered` |
| Heading wrap | zoom | `st_zoom(90)` |
| Tooltip | scale | `"2vw"` |
| Tooltip | width | `"70vw"` (or `"80vw"` for image-heavy slides) |
| Tooltip | position | `"left"` |

## Code skeleton

```python
from streamtex import st_grid, st_write, st_zoom
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from shared_widgets import st_hover_tooltip

class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
bs = BlockStyles

def build():
    with st_grid(
        cols="95% 5%",
        gap="0px",
        cell_styles=s.project.containers.grid_cell_centered,
    ) as g:
        with g.cell():
            with st_zoom(90):
                st_write(
                    bs.heading,
                    "<Slide title>",
                    tag=t.div,
                    toc_lvl="+1",
                )
        with g.cell():
            st_hover_tooltip(
                title="<Tooltip title>",
                entries=[
                    ("<Entry label>", "<Entry body>"),
                    # ... 2 to 5 entries usually
                ],
                scale="2vw",
                width="70vw",
                position="left",
            )
```

## Extrapolation rules

### INVARIANTS (never change)

- 2-column grid with split `95% / 5%` (the title dominates, the tooltip
  is a discreet aside).
- Title uses `s.project.titles.slide_title + s.center_txt` so it remains
  consistent across the deck.
- Tooltip is positioned on the left to avoid right-edge overflow on
  projectors.
- Heading carries a `toc_lvl` so the slide is reachable from the navigation.

### PARAMS (adjustable)

- `st_zoom(90)` may be reduced to 80 or 70 for very long titles, or
  increased to 100 for the first slide of a section.
- Tooltip `width` can grow to `"80vw"` for richer notes.
- Tooltip `entries` count: 2 to 6 entries.
- `toc_lvl` follows the document structure (`"1"`, `"+1"`, `"+2"`, etc.).
- The right cell can be left empty (no tooltip) for slides that don't
  need presenter notes — keep the 95/5 grid for layout consistency.
- **Tooltip-rich variant** (≈ 56% of slides in ai4se6d's GenSEM
  module): the tooltip carries a structured recap of the slide's key
  points (3 to 5 entries, each `("<Label>", "<one-line body>")`). The
  variant is the same pattern — only the density and number of tooltip
  entries grow. No new structural change.

### INTERDITS (forbidden)

- Do not change the 95/5 ratio (the visual rhythm relies on it).
- Do not omit the `toc_lvl` — slides without it are invisible in
  navigation.
- Do not use a different heading style — to preserve the deck's identity,
  the title must remain `s.project.titles.slide_title`.
- Do not place the tooltip on the right (`position="right"`) — popovers
  overflow the projector edge.

## When to use

- Every content slide that has a title and may need presenter notes.
- Slides where the speaker wants to keep extra context "one hover away"
  without polluting the visible layout.

## When NOT to use

- True title slides (use `ptn_title_slide` instead).
- Slide breaks / dividers (no title, no tooltip).
- Slides where the title needs to span over an image and a tooltip would
  be redundant — use a plain `st_write(bs.heading, ...)` instead.

## Examples

Live demo and gallery blocks (in the `stx_manual_patterns` documentation
manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_demo_slide_heading.py` — full live demo with three
  variants (default, with subtitle, narrow accent column).
- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_gallery_atoms.py` — `slide_heading` showcased side by
  side with the other core atoms (`cite`, `inline_emphasis`).

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_title_slide` — for true cover/title slides
- `ptn_cite` — often paired at the bottom of the same slide to attribute
  sources for the content shown
