---
name: ptn_narrative_transition
type: pattern
description: Narrative bridge slide pivoting from a problem state to the proposed solution / methodology
tags: [template, narrative, transition, slide]
extrapolable: true
since: 2026-05-11
---

# Narrative Transition

A bridge slide whose job is to pivot the audience from "here is the
problem we just established" to "here is the solution we are about to
unfold". The slide reads as a single rhetorical step: *previous section
exposed a gap → next section answers it*.

Use this whenever a session changes register — at the end of an
evidence section, between a state-of-the-art review and a method
proposal, or before introducing a named methodology.

## Visual

```
   <ptn_slide_heading: "The Methodological Gap">             ← 95/5 + tooltip
        (tooltip exposes a 3-bullet recap of the section we leave)

   ┌──────────────┐ ┌──────────────────────────────────────┐
   │              │ │  Today: beyond <state> →            │
   │   <logo /    │ │  <named methodology> as the answer  │
   │   illustration│ │                                      │
   │   of the     │ │  (highlight color, 1-2 lines max)   │
   │   solution>  │ │                                      │
   └──────────────┘ └──────────────────────────────────────┘
```

## Structure

The slide composes four elements in a fixed order:

1. `ptn_slide_heading` — the title announces the gap or the pivot
   (e.g. "The Methodological Gap", "What's Missing", "Beyond
   VibeEngineering"). The tooltip carries a short recap of the
   section being left.
2. A 2-column `st_grid` with an asymmetric ratio (commonly `1fr 2fr`
   or `2fr 3fr`).
3. Left cell: an `st_image` of the solution's logo or an AI-generated
   illustration, sized at `width="50%"` to `"80%"`.
4. Right cell: a single `st_write(bs.highlight, "<one-line pivot>")`
   in the project's `highlight` color. The text typically uses an
   arrow (`→`) to make the transition explicit.

## Styling rules

| Element | Property | Value |
|---|---|---|
| Heading style | composition | `s.project.titles.slide_title + s.center_txt` |
| Grid | cols | `"1fr 2fr"` (or `"2fr 3fr"` for richer illustrations) |
| Grid | gap | `"24px"` |
| Grid | cell_styles | a vertical-centered cell container (`grid_cell_centered`) |
| Image | width | `"50%"` to `"80%"` (depends on aspect ratio) |
| Pivot line style | composition | `s.Large + s.bold + s.project.colors.highlight + s.center_txt` |
| Pivot line | tone | one sentence, contains a `→` between the leaving and arriving concepts |

## Code skeleton

```python
from streamtex import st_block, st_grid, st_image, st_write, st_space, st_zoom
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from shared_widgets import st_hover_tooltip

class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    highlight = Style.create(
        s.Large + s.bold + s.project.colors.highlight + s.center_txt, "tr_hl",
    )
bs = BlockStyles

_cell_center = (
    s.project.containers.grid_cell_centered + s.center_txt
)

def build():
    with st_block(s.project.containers.page_fill_top):
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
                            "<Title of the pivot>",
                            tag=t.div, toc_lvl="+1",
                        )
                with g.cell():
                    st_hover_tooltip(
                        title="<Section we are leaving>",
                        entries=[
                            ("<Recap point>", "<one-line summary>"),
                            # 2 to 4 entries that summarize the section just covered
                        ],
                        scale="2vw", width="70vw", position="left",
                    )

            st_space("v", 2)

            # 2. asymmetric 2-column image + pivot line
            with st_grid(cols="1fr 2fr", gap="24px",
                         cell_styles=_cell_center) as g:
                with g.cell():
                    st_image(
                        s.center_txt, width="50%",
                        uri="<path to logo / AI illustration of the solution>",
                    )
                with g.cell():
                    st_write(
                        bs.highlight,
                        "Today: beyond <state we leave> "
                        "→ <named methodology / next concept>",
                    )
```

## Extrapolation rules

### INVARIANTS (never change)

- The slide is **a transition**, not a content slide — it carries
  exactly one rhetorical pivot and nothing else.
- The pivot line uses the project's `highlight` color (not `primary`
  nor `accent`) — that color signals "important transition" in the
  project palette.
- The pivot line contains a `→` (or "leads to" / "becomes") between
  the leaving and arriving concepts.
- The left cell carries a visual anchor (logo, illustration) that
  represents the destination, not the origin.
- The heading carries `toc_lvl` so the transition is reachable in
  navigation.

### PARAMS (adjustable)

- Column ratio: `"1fr 2fr"` (default), `"2fr 3fr"`, or `"45% 55%"` —
  the text side is always wider than the image side.
- Image type: project logo, AI-generated illustration
  (`provider="openai"`), or a stylised icon. Avoid photographs.
- Tooltip on the heading: present (with section recap) or absent.
- Pivot phrasing: "Today: A → B", "From A, toward B", "Beyond A:
  B emerges". Stick to one sentence.
- May be followed by a `ptn_slide_heading` of the next section on the
  next slide (no need to repeat the pivot).

### INTERDITS (forbidden)

- Do not put the image on the right — the eye reads left-to-right, and
  the visual anchor must come before the verbal claim.
- Do not list more than one pivot per slide — multiple transitions
  fragment the rhetoric. Split into separate transition slides.
- Do not include data, citations, or stats on a transition slide —
  those belong in the section being left (use `ptn_evidence_insight`
  for that purpose).
- Do not use the `primary` color for the pivot line — that color is
  reserved for ongoing key terms, not transitions.

## When to use

- End of an evidence section, just before introducing a methodology.
- Between a state-of-the-art review and a method proposal.
- Before a workshop chapter that asks "now how do we fix it?".
- Closing of a critique section, opening of a constructive section.

## When NOT to use

- Section starts that don't pivot — use `ptn_slide_heading` alone.
- Slides carrying both content and a pivot — break into two slides.
- Conclusion / wrap-up slides → use `ptn_takeaways`.
- Cover / title slides → use `ptn_title_slide`.

## Examples

Used in `ai4se6d` to bridge GenSEM evidence into the GSE-One method;
the project-specific variant is documented in
`projects/ai4se6d/ptn_transition_gse.md` and applied in four blocks of
the GenSEM module.

## Related patterns

- `ptn_slide_heading` — composed at the top of the slide
- `ptn_evidence_insight` — typically the slide *before* a transition
- `ptn_title_slide` — the slide *after* a transition often opens with
  the cover of the new section

## Changelog

- 2026-05-11: initial spec, generalised from the `ptn_transition_gse`
  project-specific variant (see audit on 2026-05-10).
