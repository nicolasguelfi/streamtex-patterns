---
name: ptn_takeaways
type: pattern
description: Numbered list of 3–5 key takeaways with bold lead and explanation
tags: [list, summary, conclusion]
extrapolable: true
since: 2026-05-10
---

# Takeaways

A numbered list of 3 to 5 key insights, each with a bolded lead-in
followed by a short explanation. Used to wrap up an evidence section, a
chapter, or a workshop's debrief. The numbering is part of the rhetoric
("here are the 3 things to remember").

## Visual

```
   1. Gains are real but variable
      — depends on experience, context, task complexity

   2. The methodology is the multiplier
      — 10% with tools → 25-30% with process

   3. Senior expertise + structured process
      — = where the real value is captured

      This is why we need GSE-One.
```

## Structure

- Outer container: `st_block(<page_fill>)` and centered inner block.
- Optional `ptn_slide_heading` at the top.
- A wrapping `st_zoom(110)` (slightly enlarged for readability).
- One `st_list(li_style=bs.body)` containing 3–5 `l.item()` entries.
- Each item: a single `st_write(bs.body, (bs.label, "<N>. <lead>"), (bs.body, " — <explanation>"))`.
- Optional closing `st_write(bs.highlight, "<conclusion sentence>")`
  after a final spacer.
- May be followed by a `ptn_cite` if the takeaways summarize evidence.

## Styling rules

| Element | Property | Value |
|---|---|---|
| List wrap | zoom | `st_zoom(110)` |
| Item body | style | `bs.body` (`s.Large + s.text.wrap.hyphens`) |
| Lead inline | style | `bs.label` (`s.bold + s.project.colors.primary`) |
| Closing punch line | style | `bs.highlight` (`s.Large + s.bold + s.project.colors.highlight + s.center_txt`) |

## Code skeleton

```python
from streamtex import st_block, st_zoom, st_list, st_write, st_space
from streamtex.enums import Tags as t
from custom.styles import Styles as s

class BlockStyles:
    body = Style.create(s.Large + s.text.wrap.hyphens, "tk_body")
    label = Style.create(s.Large + s.bold + s.project.colors.primary, "tk_lbl")
    highlight = Style.create(
        s.Large + s.bold + s.project.colors.highlight + s.center_txt, "tk_hl",
    )
bs = BlockStyles

TAKEAWAYS = [
    ("Gains are real but variable",
     "depends on experience, context, task complexity"),
    ("The methodology is the multiplier",
     "10% with tools → 25-30% with process"),
    ("Senior expertise + structured process",
     "= where the real value is captured"),
]
PUNCH = "This is why we need GSE-One."

def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            # Optional ptn_slide_heading here
            st_space("v", 2)

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
            st_write(bs.highlight, PUNCH)
```

## Extrapolation rules

### INVARIANTS (never change)

- Numbered list (`1.`, `2.`, `3.`, ...) — the ordering signals
  importance and aids recall.
- Each item has a bolded lead followed by a dash and explanation.
- Items use the project's `primary` color for the lead — that is the
  semantic "key term" color.
- The block ends optionally with one centered `highlight` punch line
  that ties the takeaways together.

### PARAMS (adjustable)

- Number of items: 3 to 5 (below 3, no need for a list; above 5, the
  audience won't remember).
- Closing punch line: present or absent.
- Lead-in length: short noun phrase (3–6 words). Avoid full sentences.
- Slide may follow a `ptn_cite` after the punch line if it summarizes
  evidence.

- The whole block is paginated via `st_slide_break(marker_label="…")`
  between each sub-recap.
- Each sub-slide is a regular `ptn_takeaways` (3 to 5 numbered
  insights), optionally preceded by a `ptn_slide_heading` naming the
  sub-section being recapped.
- The **final** sub-slide is a single-line "key message" slide using
  `s.Giant + s.bold + s.center_txt + s.project.colors.highlight`. It
  acts as the punch line of the whole multi-slide recap.
- Each sub-recap's lead-in uses an *inline emphasis variant*
  (`keyword`, `keyword_warn`, `keyword_accent`) keyed to the sub-section
  semantics — so the eye groups items per recap.

All INVARIANTS still apply per sub-slide. Do not collapse the
multi-slide recap into a single dense slide — the pagination is what
gives each sub-recap its own pedagogical beat.

Currently applied in ai4se6d as:
- `modules/ai4se6d_vibecoding/blocks/bck_recap.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_recap_v060.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_calcapp_recap.py`

### INTERDITS (forbidden)

- Do not use 6+ items — that defeats the "key takeaways" intent.
- Do not bold the explanation as well as the lead — the visual rhythm
  depends on the contrast between lead (bold) and explanation
  (regular).
- Do not nest takeaways (no sub-bullets) — promote sub-points to a
  separate slide if they matter.
- Do not change the numbering style (no bullets, no roman numerals) —
  Arabic numerals are the project convention.

## When to use

- Closing slide of an evidence section.
- Workshop debrief: "the 3 things to remember".
- Chapter summary at end of a session.
- "Key takeaways" recap before transitioning to the next concept.

## When NOT to use

- Independent items without an "important to remember" framing →
  `ptn_card_grid`.
- Hierarchical content (sections + subsections) → `ptn_categorized_grid` or
  separate slides.
- Sequence of steps in a procedure → use `st_list` with non-numbered
  styling.

## Variants

### Multi-slide recap variant

Used when a whole section needs to be recapped at the end (typically
3 to 8 sub-recaps spread across as many sub-slides):

- The whole block is paginated via `st_slide_break(marker_label="…")`
  between each sub-recap.
- Each sub-slide is a regular `ptn_takeaways` (3 to 5 numbered
  insights), optionally preceded by a `ptn_slide_heading` naming the
  sub-section being recapped.
- The **final** sub-slide is a single-line "key message" slide using
  `s.Giant + s.bold + s.center_txt + s.project.colors.highlight`. It
  acts as the punch line of the whole multi-slide recap.
- Each sub-recap's lead-in uses an *inline emphasis variant*
  (`keyword`, `keyword_warn`, `keyword_accent`) keyed to the sub-section
  semantics — so the eye groups items per recap.

All INVARIANTS still apply per sub-slide. Do not collapse the
multi-slide recap into a single dense slide — the pagination is what
gives each sub-recap its own pedagogical beat.

Currently applied in ai4se6d as:
- `modules/ai4se6d_vibecoding/blocks/bck_recap.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_recap_v060.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_calcapp_recap.py`

## Examples

Live demo and gallery blocks (in the `stx_manual_patterns` documentation
manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_gallery_lists.py` — `takeaways` with numbered items
  and `label` + `keyword` lead-ins.

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_slide_heading` — typically the title row above the list
- `ptn_inline_emphasis` — supplies the `label` (bold + primary) lead-in
- `ptn_evidence_insight` — composite template that includes a `ptn_takeaways`
  block
- `ptn_cite` — often follows the punch line for source attribution
