---
name: ptn_title_slide
type: pattern
description: Title slide with hero image, course/section title, subtitle, and author
tags: [template, title, slide]
extrapolable: true
since: 2026-05-10
---

# Title Slide

The opening slide of a session, course module, or major section. A
center-aligned, image-dominant layout: huge primary-color title, an AI-
generated hero image, two-line subtitle, and a small caption with
session/author info.

## Visual

```
                AI for Software Engineering            ← Huge primary title

              ┌─────────────────────────────┐
              │                             │
              │     [hero illustration]     │
              │                             │
              └─────────────────────────────┘

         VibeEngineering: The Future of Software       ← subtitle (zoom 150)
         Development with Generative AI

              ─── Session 1 — DLH Luxembourg ───       ← caption (muted)
```

## Structure

- Outer container: `st_block(s.project.containers.page_fill_center)`.
- Inner container: `st_block(s.center_txt)`.
- Title: `st_write(bs.title, "<Title>", tag=t.div, toc_lvl="1")` —
  always carries the top-level `toc_lvl="1"`.
- Hero image: `st_image(...)` with an AI prompt (declared at module
  level as `HERO_PROMPT`).
- Wrapped in `st_zoom(150)`: a 1- to 3-line subtitle (each line in its
  own `st_write(bs.subtitle, ..., tag=t.div)`), then an optional small
  caption with `s.project.colors.muted`.

## Styling rules

| Element | Property | Value |
|---|---|---|
| Outer container | composition | `s.project.containers.page_fill_center` |
| Title | composition | `s.Huge + s.bold + s.center_txt + s.project.colors.primary + line-height 1.1` |
| Subtitle | composition | `s.project.titles.subtitle + s.center_txt` |
| Caption | composition | `s.project.titles.caption + s.center_txt` |
| Image | width | `"80%"` |
| Image | aspect | landscape (`"1536x1024"`) for wide title slides |
| Subtitle wrap | zoom | `st_zoom(150)` |

## Code skeleton

```python
from streamtex import st_block, st_image, st_write, st_space, st_zoom
from streamtex.styles import Style
from streamtex.styles import Style as ns
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from custom.config import IS_EDITABLE
from custom.prompts import AI_PREFIX as _PREFIX, AI_SUFFIX_LANDSCAPE as _SUFFIX

_page_fill = s.project.containers.page_fill_center

class BlockStyles:
    title = Style.create(
        s.Huge + s.bold + s.center_txt + s.project.colors.primary
        + ns("line-height:1.1;", "title_lh"),
        "title",
    )
    subtitle = Style.create(
        s.project.titles.subtitle + s.center_txt, "subtitle",
    )
    info = Style.create(
        s.project.titles.caption + s.center_txt, "info",
    )
bs = BlockStyles

HERO_PROMPT = (
    f"{_PREFIX} <Visual concept describing the hero image, in evocative terms>. "
    f"{_SUFFIX}"
)

def build():
    with st_block(_page_fill):
        with st_block(s.center_txt):
            st_write(bs.title, "<Title>", tag=t.div, toc_lvl="1")

            st_image(
                s.none, width="80%",
                editable=IS_EDITABLE,
                name="<image_name>",
                prompt=HERO_PROMPT,
                provider="openai",
                ai_size="1536x1024",
            )

            with st_zoom(150):
                st_write(bs.subtitle, "<Subtitle line 1>", tag=t.div)
                st_write(bs.subtitle, "<Subtitle line 2>", tag=t.div)
                st_space("v", 0.5)
                st_write(
                    bs.info,
                    (s.project.colors.muted, "<Session info — Location>"),
                )
```

## Extrapolation rules

### INVARIANTS (never change)

- Center-aligned layout — title, image and subtitle all on the central
  axis.
- The title uses `s.project.colors.primary` (the dominant project color)
  and the largest available size (`s.Huge`).
- An AI-generated hero image is present and declared via a module-level
  `HERO_PROMPT` constant — never inlined inside `build()`.
- The image uses the project's AI editability flag (`IS_EDITABLE`) so
  the user can regenerate it from the UI.
- `toc_lvl="1"` on the title (this is a top-level entry in navigation).
- The subtitle is wrapped in `st_zoom(150)` to occupy the lower half of
  the slide proportionally.

### PARAMS (adjustable)

- Title text length: 1 line ideally, 2 lines maximum.
- Subtitle: 1 to 3 lines.
- Caption: present or absent.
- Image aspect: landscape (`1536x1024`) for wide title, portrait
  (`1024x1536`) for figure-dominated topics.
- Image size: `"80%"` typical; reduce to `"60%"` for very long titles.
- AI provider: `openai`, `google`, or `fal` per project policy.

### INTERDITS (forbidden)

- Do not omit the AI image — the title slide is image-dominant by
  design.
- Do not use this pattern for content slides (sub-section titles inside
  a chapter use a `ptn_slide_heading` instead).
- Do not place a citation (`ptn_cite`) on a title slide.
- Do not skip `toc_lvl="1"` — the title slide must anchor the
  navigation.
- Do not hardcode the title color — always go through
  `s.project.colors.primary`.

## When to use

- The very first slide of a presentation.
- Major section / chapter dividers ("Session 3 — Generative SE Methods").
- The cover slide of a workshop or training module.

## When NOT to use

- Sub-section dividers inside a chapter (use a smaller `ptn_slide_heading`
  with optional image).
- Pure data slides (use `ptn_stat_hero` or `ptn_evidence_insight`).
- Conclusion slides (use `ptn_takeaways` followed by a final
  acknowledgements slide).

## Examples

Live demo blocks (in the `stx_manual_patterns` documentation manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_demo_title_slide.py` — full live demo with title,
  subtitle and authors row, ready to be copy-adapted to a new project.

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_slide_heading` — for sub-section titles inside a chapter
- `ptn_stat_hero` (variant b) — for image + content content slides (not
  title slides)
