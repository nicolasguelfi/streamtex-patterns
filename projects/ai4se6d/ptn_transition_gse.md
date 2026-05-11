---
name: ptn_transition_gse
type: pattern
description: ai4se6d-specific transition slide pivoting a section into the GSE-One methodology
tags: [template, narrative, transition, slide, ai4se6d, gse-one]
extrapolable: false
since: 2026-05-11
---

# Transition → GSE-One (ai4se6d)

A project-specific specialisation of `ptn_narrative_transition` used in
the GenSEM module of the `ai4se6d` training collection. The pattern
fixes the *destination* of the pivot to the GSE-One methodology and
fixes the visual anchor to the GSE-One logo.

This pattern exists so that the four GenSEM slides that bridge into
GSE-One stay typographically and rhetorically consistent.

## Visual

```
   <ptn_slide_heading: "The Methodological Gap" or similar>
        (tooltip recaps the section we leave: SDLC paradigms,
         frameworks landscape, risks, evidence synthesis…)

   ┌──────────────┐ ┌──────────────────────────────────────┐
   │              │ │  Today: beyond VibeEngineering →    │
   │  GSE-One     │ │  Generative SE practiced through    │
   │  logo        │ │  GSE-One                            │
   │              │ │                                      │
   └──────────────┘ └──────────────────────────────────────┘
```

## Structure

Identical to `ptn_narrative_transition`, with these fixed choices:

1. `ptn_slide_heading` — title varies per slide but always names a gap
   or a "beyond X" framing.
2. 2-column `st_grid` with `cols="1fr 2fr"` and `gap="24px"`.
3. Left cell: GSE-One logo
   (`uri="images/managed/GSE/images/logo-gse-geni-with-shield.webp"`)
   sized at `width="50%"`.
4. Right cell: a single `st_write(bs.highlight, "Today: ... → ... GSE-One")`.

## Styling rules

Inherits every styling rule from `ptn_narrative_transition`. Fixed
project-specific values:

| Element | Value |
|---|---|
| Logo URI | `images/managed/GSE/images/logo-gse-geni-with-shield.webp` |
| Logo width | `"50%"` |
| Pivot line color | `s.project.colors.highlight` (amber in the ai4se6d palette) |
| Destination concept | always "GSE-One" |

## Code skeleton

```python
from streamtex import st_block, st_grid, st_image, st_write, st_space, st_zoom
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from shared_widgets import st_hover_tooltip

class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    highlight = Style.create(
        s.Large + s.bold + s.project.colors.highlight + s.center_txt, "tg_hl",
    )
bs = BlockStyles

_cell_center = (
    s.project.containers.grid_cell_centered + s.center_txt
)

def build_transition_to_gse():
    """Call at the end of any GenSEM section to bridge into GSE-One."""
    with st_block(s.center_txt):
        # 1. ptn_slide_heading with recap tooltip
        with st_grid(
            cols="95% 5%", gap="0px",
            cell_styles=s.project.containers.grid_cell_centered,
        ) as g:
            with g.cell():
                with st_zoom(90):
                    st_write(
                        bs.heading,
                        "The Methodological Gap",
                        tag=t.div, toc_lvl="+1",
                    )
            with g.cell():
                st_hover_tooltip(
                    title="<Section recap>",
                    entries=[
                        ("<Recap point>", "<one-line summary>"),
                    ],
                    scale="2vw", width="70vw", position="left",
                )

    st_space("v", 2)

    with st_grid(cols="1fr 2fr", gap="24px",
                 cell_styles=_cell_center) as g:
        with g.cell():
            st_image(
                s.center_txt, width="50%",
                uri="images/managed/GSE/images/logo-gse-geni-with-shield.webp",
            )
        with g.cell():
            st_write(
                bs.highlight,
                "Today: beyond VibeEngineering "
                "→ Generative SE as a discipline, practiced through "
                "GSE-One",
            )
```

## Specialisation note

This pattern is **not extrapolable** (`extrapolable: false`). It is a
fixed instantiation of `ptn_narrative_transition` for the ai4se6d
collection. If you need a different destination (another methodology,
another visual anchor), use the generic `ptn_narrative_transition`
directly instead — do not adapt this one.

The invariants inherited from `ptn_narrative_transition` still apply.

## When to use

- Closing slide of a GenSEM section (SDLC paradigms, framework
  landscape, risks, evidence synthesis) that introduces or
  re-introduces GSE-One.
- Anywhere in the `ai4se6d` collection that needs to pivot from a
  problem state to GSE-One as the answer.

## When NOT to use

- Transitions to other methodologies (AgileGen, V-Bounce, SE 3.0…) —
  use the generic `ptn_narrative_transition`.
- Transitions *out of* GSE-One (e.g. towards limitations / open
  questions) — those are not pivots-to-solution; use a different
  pattern.
- Outside the `ai4se6d` collection — the logo URI is project-local.

## Examples

Annotated and applied in 4 blocks of `ai4se6d`:

- `modules/ai4se6d_gensem/blocks/bck_gensem_frameworks.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_sdlc_paradigms.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_risks.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_evidence_synthesis.py`

## Related patterns

- `ptn_narrative_transition` — the generic pattern this specialises
- `ptn_slide_heading` — composed at the top of the slide
- `ptn_evidence_insight` — typically the slide *before* this transition

## Changelog

- 2026-05-11: initial spec, captured from 4 existing block annotations
  (audit 2026-05-10).
