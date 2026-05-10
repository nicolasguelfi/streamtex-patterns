---
name: ptn_stat_hero
type: pattern
description: Slide centerpiece — a single oversized statistic with body and source
tags: [stat, evidence, hero]
extrapolable: true
since: 2026-05-10
---

# Stat Hero

A slide whose visual centerpiece is a single oversized number or short
phrase (the "hero stat"), supported by a brief body explanation and an
attribution. Used to anchor evidence-driven slides where one data point
must dominate.

## Visual

```
                    The METR Paradox
                    ────────────────
                          +19%

   Experienced developers on well known projects.
   The perception gap: predicted 24% faster, still believed 20%.

                  ─── METR (2025) ───
```

Three layout variants are supported:

- **(a) stat-only** — title, big number, body lines, source. Single column.
- **(b) image + stat** — 2-column grid (image left, stat + body + source
  on the right). Used when an AI illustration accompanies the data.
- **(c) stat + tooltip** — like (a) but the title is rendered through
  the `ptn_slide_heading` 95/5 grid so a tooltip exposes the study details.

## Structure

- Outer container: `st_block(s.project.containers.page_fill_top)` and
  inner `st_block(s.center_txt)`.
- Title — either via `ptn_slide_heading` (variant c) or a plain
  `st_write(bs.heading, ..., toc_lvl="1")` (variants a, b).
- Hero stat — `st_write(bs.stat, "<value>")` using
  `s.project.titles.stat_hero`. Wrapped in `st_zoom(60)` only for
  variant (c) where the stat is in a 95/5 sub-grid.
- Body — one or more `st_write(bs.body, ...)` lines. Inline emphasis
  uses the `ptn_inline_emphasis` pattern.
- Source — final line, `st_write(bs.source, cite("<key>"))` (the
  `ptn_cite` pattern).

## Styling rules

| Element | Property | Value |
|---|---|---|
| Outer wrap | container | `s.project.containers.page_fill_top` |
| Heading | style | `s.project.titles.slide_title + s.center_txt` |
| Stat | style | `s.project.titles.stat_hero` |
| Body | style | `s.project.titles.body` (often `+ s.center_txt`) |
| Source | style | `s.project.citation + s.large + s.center_txt` |
| Vertical spacing | between blocks | `st_space("v", 1)` |
| Variant (b) grid | cols | `"1.5fr 3.5fr"` or `"2fr 3fr"` |
| Variant (b) grid | gap | `"24px"` |

## Code skeleton

Variant (a) — stat only:

```python
from streamtex import st_block, st_write, st_space
from streamtex.bib import cite
from streamtex.enums import Tags as t
from custom.styles import Styles as s

class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    stat = s.project.titles.stat_hero
    body = s.project.titles.body
    keyword = s.bold + s.project.colors.primary
    source = s.project.citation + s.large + s.center_txt
bs = BlockStyles

def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            st_write(bs.heading, "<Slide title>", tag=t.div, toc_lvl="1")
            st_space("v", 1)
            st_write(bs.stat, "<HERO STAT>")
            st_space("v", 1)
            st_write(
                bs.body,
                "<Body explanation, usually 1–3 lines.>",
            )
            st_space("v", 1)
            st_write(
                bs.body,
                (bs.keyword, "<inline emphasis>"),
                " <continuation>",
            )
        st_space("v", 1)
        st_write(bs.source, cite("<bib_key>"))
```

Variant (b) — image + stat:

```python
def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            st_write(bs.heading, "<Slide title>", tag=t.div, toc_lvl="1")

            with st_grid(
                cols="1.5fr 3.5fr",
                gap="24px",
                cell_styles=s.project.containers.grid_cell_centered,
            ) as g:
                with g.cell():
                    st_image(
                        s.none, width="80%",
                        editable=IS_EDITABLE,
                        name="<image_name>",
                        prompt=_PROMPT,
                        provider="openai",
                        ai_size="1024x1536",
                    )
                with g.cell():
                    st_write(bs.stat, "<HERO STAT>")
                    st_space("v", 0.5)
                    st_write(bs.body, "<Body line 1>")
                    st_write(bs.body, "<Body line 2>")
                    st_space("v", 0.5)
                    st_write(bs.source, cite("<bib_key>"))
```

Variant (c) is variant (a) with the title replaced by a `ptn_slide_heading`
pattern instance.

## Extrapolation rules

### INVARIANTS (never change)

- Exactly **one hero stat** per slide. The stat is the visual focal point.
- The hero stat uses `s.project.titles.stat_hero` (the project's
  largest text style).
- The slide ends with a `ptn_cite` pattern for source attribution.
- Body text stays brief — the eye should land on the stat first.

### PARAMS (adjustable)

- Number of body lines (1 to 4).
- Inline emphasis on body lines (uses the `ptn_inline_emphasis` pattern).
- Layout variant: (a) stat-only, (b) image + stat, (c) stat + tooltip.
- Variant (b) grid ratio: `1.5fr 3.5fr` (image-light) to `2fr 3fr`
  (image-balanced).
- Title may carry a tooltip via the `ptn_slide_heading` pattern (variant c).

### INTERDITS (forbidden)

- Do not display two hero stats side-by-side — that breaks the focal
  point. Use a `ptn_comparison_table` or two separate slides instead.
- Do not omit the source — a hero stat without attribution undermines
  credibility.
- Do not put the hero stat at the top of the slide above the title — the
  title comes first.
- Do not use this pattern for non-quantitative emphasis (a quote should
  use a `ptn_callout`, not `ptn_stat_hero`).

## When to use

- Slides whose purpose is to drive home a single quantitative insight.
- Evidence-based discussion of a study's headline finding.
- Paradox / "wow" data points that the audience must remember.

## When NOT to use

- Multi-stat comparisons → `ptn_comparison_table`.
- Synthesis of several findings → `ptn_evidence_insight` (which composes
  `ptn_stat_hero` + `ptn_takeaways`).
- Qualitative claim or quote → `ptn_callout` instead.

## Examples

Live demo blocks (in the `stx_manual_patterns` documentation manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_demo_stat_hero.py` — three variant layouts:
  centered hero, side-by-side stat + body, multi-stat 2-column grid.

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_slide_heading` — used as the title row in variant (c)
- `ptn_cite` — used at the bottom for source attribution
- `ptn_inline_emphasis` — used in body lines
- `ptn_evidence_insight` — composite template that wraps `ptn_stat_hero`
- `ptn_callout` — alternative when the centerpiece is qualitative, not numeric
