---
name: evidence_insight
type: pattern
description: Slide template combining a hero stat, a body explanation, key takeaways, and a source citation
tags: [template, evidence, slide]
extrapolable: true
since: 2026-05-10
---

# Evidence Insight

A composite slide template used to drive home a single piece of evidence.
It composes four other patterns in a fixed order: `slide_heading` →
`stat_hero` (or short body) → `takeaways` → `cite`. Use it when you want
the slide to read as "headline + finding + what to remember + source".

## Visual

```
   <slide_heading: "Evidence Synthesis">                 ← 95/5 + tooltip

                          7h
   Lost per team member weekly to AI inefficiencies.

      1. Gains are real but variable
      2. The methodology is the multiplier
      3. Senior expertise + structured process

           This is why we need GSE-One.

              ─── GitLab DevSecOps 2025 ───              ← cite
```

## Structure

This pattern composes four other patterns in this order:

1. `slide_heading` — title row with optional tooltip.
2. (Optional) hero stat — uses the `stat_hero` core (just the big number,
   not the full hero variant).
3. (Optional) one-paragraph body explanation in `bs.body`.
4. `takeaways` — 3 numbered key insights with optional punch line.
5. `cite` — source citation at the very bottom.

## Styling rules

Each composed pattern follows its own `Styling rules` section. The
template adds:

- Vertical spacing of `st_space("v", 1)` to `st_space("v", 2)` between
  each section.
- A wrapping `st_zoom(110)` on the takeaways list (inherited from
  `takeaways`).

## Code skeleton

```python
from streamtex import st_block, st_grid, st_zoom, st_list, st_write, st_space
from streamtex.bib import cite
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from shared_widgets import st_hover_tooltip


class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    stat = s.project.titles.stat_hero
    body = Style.create(s.Large + s.text.wrap.hyphens, "ev_body")
    label = Style.create(s.Large + s.bold + s.project.colors.primary, "ev_lbl")
    highlight = Style.create(
        s.Large + s.bold + s.project.colors.highlight + s.center_txt, "ev_hl",
    )
    source = s.project.citation + s.large + s.center_txt
bs = BlockStyles


def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            # 1. slide_heading (with tooltip)
            with st_grid(
                cols="95% 5%", gap="0px",
                cell_styles=s.project.containers.grid_cell_centered,
            ) as g:
                with g.cell():
                    with st_zoom(90):
                        st_write(bs.heading, "<Slide title>", tag=t.div, toc_lvl="+1")
                with g.cell():
                    st_hover_tooltip(
                        title="<Tooltip title>",
                        entries=[("<Label>", "<Body>"), ...],
                        scale="2vw", width="70vw", position="left",
                    )

            st_space("v", 2)

            # 2. (Optional) hero stat
            st_write(bs.stat, "<HERO STAT>")
            st_space("v", 1)

            # 3. (Optional) one-paragraph body
            st_write(bs.body, "<Body explanation>")
            st_space("v", 2)

            # 4. takeaways
            with st_zoom(110):
                with st_list(li_style=bs.body) as l:
                    for i, (lead, body) in enumerate(TAKEAWAYS, start=1):
                        with l.item():
                            st_write(
                                bs.body,
                                (bs.label, f"{i}. {lead} "),
                                (bs.body, f"— {body}"),
                            )

            st_space("v", 2)
            st_write(bs.highlight, "<Punch line>")

        # 5. cite
        st_space("v", 1)
        st_write(bs.source, cite("<bib_key>"))
```

## Extrapolation rules

### INVARIANTS (never change)

- The composition order is fixed: heading → (stat / body) → takeaways →
  cite. The reader's eye must travel top-to-bottom in that order.
- The slide presents **one piece of evidence**, not several.
- The citation is mandatory — no evidence_insight without source
  attribution.
- The slide ends with the `highlight` punch line (1 line) tying the
  takeaways together — it sets up the transition to the next concept.

### PARAMS (adjustable)

- Hero stat: present (centered, single number/short phrase) or absent
  (in which case the body paragraph carries the headline).
- Body paragraph: present or absent.
- Number of takeaways: 3 to 5 (inherits from `takeaways` pattern).
- Tooltip on the heading: present or absent.
- The composition may swap the order of `stat_hero` and the body
  paragraph (stat-first vs paragraph-first), but never break out of
  this five-section spine.

### INTERDITS (forbidden)

- Do not split the evidence across two columns — `evidence_insight` is
  a single-column slide.
- Do not include images (other than the hero stat as text).
- Do not omit the source — for "no source available" content, use a
  different pattern.
- Do not use this template when the goal is comparing several pieces
  of evidence — use a `comparison_table` or break into separate
  `evidence_insight` slides instead.

## When to use

- Synthesis slide at the end of an evidence-heavy section.
- "Here's the data and what it means" slides in technical talks.
- Workshop debrief that ties a study finding to a methodological
  recommendation.

## When NOT to use

- Single-stat slides without takeaways → `stat_hero` (just the
  centerpiece).
- Multi-source comparisons → `comparison_table`.
- Pure-takeaways slides without supporting evidence → `takeaways`
  alone.

## Examples

- `modules/ai4se6d_gensem/blocks/bck_gensem_evidence_synthesis.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_evidence_rcts.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_evidence_reality.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_evidence_enterprise.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_sdlc_paradigms.py`

5 blocks annotated `# @pattern: evidence-insight` in the corpus.

## Related patterns

- `slide_heading` (composed)
- `stat_hero` (composed, optional)
- `takeaways` (composed)
- `cite` (composed)
- `inline_emphasis` (used inside the body and takeaways)
