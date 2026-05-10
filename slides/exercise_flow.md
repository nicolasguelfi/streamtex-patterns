---
name: exercise_flow
type: pattern
description: Slide template for a timed exercise — briefing, action, debrief
tags: [template, exercise, practice, slide]
extrapolable: true
since: 2026-05-10
---

# Exercise Flow

A multi-slide template for a timed workshop exercise. Each instance
produces three slides separated by `st_slide_break`:

1. **Briefing** — what the exercise is, why it matters, instructions.
2. **Action** — a minimal slide with timer / instruction during the
   exercise itself (often nearly blank).
3. **Debrief** — what to discuss after, key takeaways, callouts.

Used for the `practice_pN` series in the GenSEM module (8 exercises).

## Visual

```
   Slide 1 (Briefing)
   ────────────────────
   [slide_heading + tooltip]
   [logo / image]    [card_grid: 1. Install ... 2. Open ... 3. Run ...]
   [accent: "Time: 30 minutes"]

   Slide 2 (Action)
   ────────────────────
   [Huge instruction: "Follow the agent. Note what surprises you."]
   [Huge timer: "30 min"]

   Slide 3 (Debrief)
   ────────────────────
   [slide_heading: "Debrief — Practice 1"]
   [callout: "What did you notice?"]
   [card_grid: 3-5 typical observations]
```

## Structure

The pattern is a **composition spine**, not a monolithic template. It
calls three other patterns separated by `st_slide_break`:

```python
st_slide_break(marker_label="<Exercise N>: <name>")
# --- Briefing slide ---
#   slide_heading + (image | logo) + card_grid (1. ... 2. ... 3. ...)
#   + accent paragraph "Time: <N> minutes"

st_slide_break(marker_label="<Exercise N>: Action")
# --- Action slide (minimal) ---
#   instruction (Huge bold accent)
#   timer (Huge bold highlight)

st_slide_break(marker_label="<Exercise N>: Debrief")
# --- Debrief slide ---
#   slide_heading + callout (question) + card_grid (observations)
#   + (optional) takeaways / cite
```

## Styling rules

| Element | Property | Value |
|---|---|---|
| Briefing layout | grid cols | `"3fr 7fr"` (logo \| instructions) |
| Briefing instructions | container | cell `cell_primary_bg + cell_pad_md + center_txt` |
| Briefing time accent | style | `s.Large + s.bold + s.project.colors.accent + s.center_txt` |
| Action instruction | style | `s.huge + s.bold + s.project.colors.accent + s.center_txt` |
| Action timer | style | `s.Huge + s.bold + s.project.colors.highlight + s.center_txt` |
| Debrief callout | container | `s.project.containers.callout` |
| Slide breaks | call | `st_slide_break(marker_label="...")` between every slide |

## Code skeleton

```python
from streamtex import (
    st_block, st_grid, st_image, st_write, st_space, st_zoom,
    st_list, st_slide_break,
)
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from shared_widgets import st_hover_tooltip


class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    body = Style.create(s.Large + s.center_txt + s.text.wrap.hyphens, "ex_body")
    accent = Style.create(
        s.Large + s.bold + s.project.colors.accent + s.center_txt, "ex_acc",
    )
    keyword = Style.create(
        s.Large + s.bold + s.project.colors.primary, "ex_kw",
    )
    instruction = Style.create(
        s.huge + s.bold + s.project.colors.accent + s.center_txt, "ex_instr",
    )
    timer = Style.create(
        s.Huge + s.bold + s.project.colors.highlight + s.center_txt, "ex_timer",
    )
bs = BlockStyles

_cell = (
    s.project.containers.cell_primary_bg
    + s.project.containers.cell_pad_md + s.center_txt
)


def build():
    # === Slide 1: Briefing ===========================================
    st_slide_break(marker_label="Practice N: <name>")
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            # slide_heading (with tooltip)
            with st_grid(
                cols="95% 5%", gap="0px",
                cell_styles=s.project.containers.grid_cell_centered,
            ) as g:
                with g.cell():
                    with st_zoom(90):
                        st_write(bs.heading, "Practice: <name>", tag=t.div, toc_lvl="+1")
                with g.cell():
                    st_hover_tooltip(
                        title="Why this exercise?",
                        entries=[("Pedagogy", "..."), ("What to expect", "...")],
                        scale="2vw", width="70vw", position="left",
                    )

            st_space("v", 1)

            with st_grid(cols="3fr 7fr", gap="24px") as g:
                with g.cell():
                    st_image(s.center_txt, width="90%", uri="<logo or image path>")
                with g.cell():
                    with st_block(_cell):
                        with st_list(list_type=lt.unordered) as l:
                            with l.item():
                                st_write(bs.body, (bs.keyword, "1. "),
                                         (bs.keyword, "<step 1>"), " <continuation>")
                            with l.item():
                                st_write(bs.body, (bs.keyword, "2. "),
                                         (bs.keyword, "<step 2>"), " <continuation>")
                            # ...

            st_space("v", 1)
            st_write(bs.accent, "Time: <N> minutes")

    # === Slide 2: Action =============================================
    st_slide_break(marker_label="Practice N: Action")
    with st_block(s.project.containers.page_fill_center):
        with st_block(s.center_txt):
            st_write(bs.instruction, "<Action instruction>")
            st_space("v", 4)
            st_write(bs.timer, "<N> min")

    # === Slide 3: Debrief ============================================
    st_slide_break(marker_label="Practice N: Debrief")
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            st_write(bs.heading, "Debrief — Practice N", tag=t.div, toc_lvl="+1")
            st_space("v", 1)
            with st_block(s.project.containers.callout):
                st_write(bs.accent, "What did you notice?")
            st_space("v", 1)
            # card_grid of typical observations ...
```

## Extrapolation rules

### INVARIANTS (never change)

- Three slides separated by `st_slide_break`. The "briefing → action →
  debrief" tempo is mandatory; it mirrors how the trainer guides the
  workshop.
- The action slide is **minimal** (1 instruction line + 1 timer line).
  Never add detail there — the audience must focus on doing, not
  reading.
- Each slide carries a `toc_lvl="+1"` (or `+2`) for navigation.
- The briefing always names the time budget.
- The debrief always opens with a question (callout) before showing
  expected observations.

### PARAMS (adjustable)

- Number of briefing instructions: 2 to 6 (use `card_grid` or a
  `st_list` for them).
- Image / logo on briefing: present or absent.
- Tooltip on each slide heading: present or absent.
- Number of debrief observations: 2 to 6.
- Timer phrasing: `"30 min"`, `"1 hour"`, `"15-20 min"` etc.

### INTERDITS (forbidden)

- Do not collapse the three slides into one — the workshop tempo
  depends on dedicated slides.
- Do not put bullet lists on the action slide — it must remain visually
  empty.
- Do not skip the debrief — even short exercises need closure.
- Do not use this pattern for non-timed activities (e.g. quizzes /
  surveys) — those have their own patterns.

## When to use

- Workshop practice exercises (P1...PN of a session).
- Hands-on coding moments where the trainer steps back.
- Any timed group activity that needs setup + execution + closure.

## When NOT to use

- Pure quiz / poll → use the `survey-convert` tooling.
- Reading exercises → a single content slide is enough.
- Demo-only segments where the trainer drives → no exercise pattern
  needed.

## Examples

- `modules/ai4se6d_gensem/blocks/bck_gensem_practice_p1.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_practice_p2.py`
- ... through `bck_gensem_practice_p8.py`

8 blocks annotated `# @pattern: exercise-flow` in the corpus.

## Related patterns

- `slide_heading` (composed in briefing and debrief)
- `card_grid` (composed for instructions / observations)
- `callout` (composed for the debrief question)
- `inline_emphasis` (used in the briefing list)
- `takeaways` (optional final slide if the debrief leads to a synthesis)
