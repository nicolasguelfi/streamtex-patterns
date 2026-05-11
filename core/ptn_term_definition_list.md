---
name: ptn_term_definition_list
type: pattern
description: Vertical list of `term — definition` rows for glossaries, notations, abbreviation tables
tags: [list, glossary, reference, definitions]
extrapolable: true
since: 2026-05-11
---

# Term / Definition List

A vertical sequence of `(term, separator, definition)` rows used for
glossaries, notation tables, abbreviation references, and any place
where the page shape is "key terms on the left, explanations on the
right (within the same line)".

The rendering uses a single tuple-style `st_write` per entry so the
term and its definition flow as one line that wraps naturally.

## Visual

```
   ACI       —  Agent-Computer Interface — structured protocols for AI
                agents to interact with tools and environments
   AGENTS.md —  Linux Foundation standard for tool-agnostic project
                rules, enabling cross-tool portability
   CHOP      —  Chat-Oriented Programming — multi-turn conversational
                interaction with LLMs
   …
```

The **term** is bolded and uses the project's `primary` color.
A muted em-dash separator distinguishes the term from its prose.

## Structure

- Outer container: `st_block(<page_fill>)` + centered inner block.
- Optional `ptn_slide_heading` at the top (e.g. "Glossary", "Notation").
- A wrapping `st_zoom(120)` (slightly enlarged for readability of dense
  reference content).
- A simple Python loop over `_ENTRIES` — each entry produces one
  `st_write(bs.definition, (bs.term, term), (bs.separator, " — "),
  (bs.definition, definition))`.
- An `st_space("v", 0.5)` between entries (no separator line, just
  vertical air).

## Styling rules

| Element | Property | Value |
|---|---|---|
| Term | style | `s.project.colors.primary + s.bold + s.Large` (`bs.term`) |
| Separator | style | `s.project.colors.muted + s.Large` (`bs.separator`), content `" — "` |
| Definition | style | `s.Large` (`bs.definition`) — no color, no bold |
| Spacing between entries | size | `st_space("v", 0.5)` |
| Wrap zoom | level | `st_zoom(120)` |

## Code skeleton

```python
from streamtex import st_block, st_zoom, st_write, st_space, Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s

class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    term = Style.create(
        s.project.colors.primary + s.bold + s.Large, "td_term",
    )
    definition = Style.create(s.Large, "td_def")
    separator = Style.create(
        s.project.colors.muted + s.Large, "td_sep",
    )
bs = BlockStyles

_ENTRIES = [
    ("<TERM>", "<one-line definition>"),
    # … 5 to 50 rows; sort alphabetically for glossaries
]

def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            # Optional ptn_slide_heading here (e.g. "Glossary")
            st_space("v", 1)

        with st_zoom(120):
            for term, definition in _ENTRIES:
                st_write(
                    bs.definition,
                    (bs.term, term),
                    (bs.separator, " — "),
                    (bs.definition, definition),
                )
                st_space("v", 0.5)
```

## Extrapolation rules

### INVARIANTS (never change)

- One row = one `st_write` with three tuple fragments
  (term, separator, definition). Do not split into a grid.
- The term uses the project's `primary` color + bold — that signals
  "this is a vocabulary entry, not a regular bolded word".
- The separator is the em-dash (`—`) rendered in the `muted` color —
  the muting is what visually separates "key" from "value" without
  using a column.
- The definition is plain (no color, no bold) — emphasis inside the
  definition is allowed via further inline-emphasis tuples.
- Entries are stacked vertically, never in columns.

### PARAMS (adjustable)

- Number of entries: 5 to ~50 (a single slide). Beyond 50, paginate
  with `st_slide_break` into multiple sub-slides.
- Ordering: alphabetical (glossaries), categorical (sections inside
  the list), or sequential (notation introduced in lecture order).
- Wrap zoom: `st_zoom(120)` by default; reduce to `100` for very long
  lists, increase to `130` for short tables.
- Spacing between entries: `0.5` default; `0.3` for very dense
  reference, `0.8` for prose-heavy definitions.
- The definition body may itself contain inline-emphasis tuples
  (`ptn_inline_emphasis`) for sub-terms or examples.

### INTERDITS (forbidden)

- Do not render terms in a separate column (`st_grid` with `cols="..."`)
  — the wrapping behaviour depends on the inline tuple flow.
- Do not bold the definition or color it — only the term is
  emphasised. Otherwise the eye cannot scan terms quickly.
- Do not use a vertical bar / pipe separator (`|`) — the em-dash is
  the project convention.
- Do not mix `ptn_term_definition_list` with `ptn_comparison_table`
  rows in the same block — they look similar but signal very
  different things (definition vs comparison).

## When to use

- Module glossaries (every training module typically has one).
- API notation references (symbol → meaning).
- Abbreviation tables in a manual appendix.
- Configuration key references (`<key> — what it controls`).
- Any page where "key terms followed by short definitions" is the
  reading task.

## When NOT to use

- Comparing several attributes per term → `ptn_comparison_table`.
- Long-form definitions (paragraph or more per term) → one-term-per-page
  `ptn_api_reference_card`.
- Tagged / categorised glossary → `ptn_categorized_grid` (with each
  category as a sub-glossary).
- Sequence of steps or numbered insights → `ptn_takeaways`.

## Examples

Used in 4 ai4se6d glossaries (one per module + a shared cross-module
glossary). All four glossaries share an identical structure — this
pattern formalises that structure.

## Related patterns

- `ptn_inline_emphasis` — supplies the term + separator + definition
  tuple-style composition
- `ptn_slide_heading` — typically the title row above the list
- `ptn_categorized_grid` — when the glossary needs sections
- `ptn_api_reference_card` — when each term deserves its own page

## Changelog

- 2026-05-11: initial spec, generalised from 4 ai4se6d glossary blocks
  (audit 2026-05-10).
