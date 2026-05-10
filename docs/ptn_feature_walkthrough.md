---
name: ptn_feature_walkthrough
type: pattern
description: Multi-step feature presentation — numbered steps, each with explanation, code, and demo
tags: [docs, manual, walkthrough, tutorial]
extrapolable: true
since: 2026-05-10
---

# Feature Walkthrough

A narrative, numbered tutorial that walks a reader through using a
StreamTeX feature end-to-end. Differs from `ptn_manual_section` by being
**sequential and goal-oriented**: each step builds on the previous one,
and at the end the reader has accomplished a concrete task.

## Visual

```
   Quick Start — First Block & Run                          ← bs.heading

   Step 1: Create a block file                              ← bs.sub "+1"
     [explanation]
     [code: blocks/bck_hello.py source]

   Step 2: Register in book.py                              ← bs.sub "+1"
     [explanation]
     [code: book.py change]

   Step 3: Run it                                           ← bs.sub "+1"
     [explanation]
     [code: terminal command]
     [optional live demo or screenshot]
```

## Structure

- One block file per walkthrough.
- Section heading carries the **goal** ("Quick Start — First Block & Run"),
  not just a topic name.
- Sub-headings are **numbered steps** with an action verb
  ("Step 1: Create a block file", "Step 2: Register...").
- Each step contains:
  1. `show_explanation` — what the step accomplishes and why.
  2. `show_code` — the file/snippet the reader must produce.
  3. (optional) live demo if the step itself produces visible output.
- Closing recap (optional): a single `show_explanation` summarising what
  the reader achieved.

## Styling rules

| Element | Property | Value |
|---|---|---|
| Heading | composition | `s.project.titles.section_title + s.center_txt` |
| Step heading | composition | `s.project.titles.section_subtitle` (with `toc_lvl="+1"`) |
| Step number | content | always present in the sub-heading text ("Step N: ...") |
| Spacing — within step | size | `st_space("v", 1)` |
| Spacing — between steps | size | `st_space("v", 2)` |

## Code skeleton

```python
"""<Goal> — feature walkthrough."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation

class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    st_space("v", 1)
    st_write(bs.heading, "<Goal>", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ---- Step 1 ----
    st_write(bs.sub, "Step 1: <Action verb + object>", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        <What this step accomplishes and why it matters.>
    """)
    st_space("v", 1)

    show_code("""\
        # <file path or shell command>
        <code or command>
    """)
    st_space("v", 2)

    # ---- Step 2 ----
    st_write(bs.sub, "Step 2: <Action verb + object>", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        <Explanation>
    """)
    st_space("v", 1)

    show_code("""\
        <code>
    """)
    st_space("v", 2)

    # ---- Step N: Run / Verify ----
    st_write(bs.sub, "Step N: Run it", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Run the project to see your block live.
    """)
    st_space("v", 1)

    show_code("""\
        stx run
    """)
    st_space("v", 2)
```

## Extrapolation rules

### INVARIANTS (never change)

- Steps are **numbered**: "Step 1", "Step 2", ..., visible in the
  sub-heading. The reader must always know where they are in the
  sequence.
- Each step is **goal-oriented**: an action verb in imperative form.
- The walkthrough has a clear **terminal goal** stated in the section
  heading — by the last step, the reader has achieved it.
- `show_explanation` precedes `show_code` in every step (same as
  `ptn_manual_section`).
- Each step is **self-contained enough** that the reader can verify
  progress (file saved, command run, output seen).

### PARAMS (adjustable)

- Number of steps: 2 to ~8.
- Final step may include a live demo of the achieved result.
- A step may have multiple `show_code` blocks (one for each file
  modified), but always preceded by a single `show_explanation`.
- A short closing `show_explanation` may recap what was accomplished.

### INTERDITS (forbidden)

- Do not skip step numbering ("Step 1", "Step 2"...) — narrative tutorials
  rely on the linear progression.
- Do not mix walkthroughs and reference content in the same block —
  separate them.
- Do not use this pattern for purely descriptive content — use
  `ptn_manual_section` instead.
- Do not have a step that only contains code without explanation — the
  reader will skim and miss the point.

## When to use

- Quick Start tutorials.
- "How do I X?" recipes that need 3+ steps.
- Onboarding sequences in a manual.

## When NOT to use

- Pure feature documentation → `ptn_manual_section`.
- Single-action snippet ("how to use this one function") →
  `ptn_api_reference_card`.
- Conceptual / narrative documentation → plain text + `ptn_callout`.

## Examples

Live demo blocks (in the `stx_manual_patterns` documentation manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_gallery_docs.py` — `feature_walkthrough` with a
  numbered 7-step demo.

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_manual_section` — for feature descriptions without explicit step
  numbering
- `ptn_composite_block` — when a tutorial is too long for one block file
  and is decomposed into atomic blocks
- `ptn_callout` — for "Note: ..." / "Tip: ..." asides within a step
