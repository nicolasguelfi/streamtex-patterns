---
name: cite
type: pattern
description: Inline source citation with author, year, and optional URL — placed under a quote, stat, or claim
tags: [citation, evidence, footer]
extrapolable: false
since: 2026-05-10
---

# Cite

A small, centered citation footer rendered through StreamTeX's
`bib.cite()` call. Used to attribute a source under a stat, claim, quote,
or any evidence-based content.

## Visual

```
              ─────────────────────────────────────
              METR (2025) — arXiv:2507.09089
              ─────────────────────────────────────
```

The text is rendered in a smaller, italicized "citation" style, centered,
typically at the bottom of a slide block.

## Structure

- One `st_write` call.
- Style: `s.project.citation + s.large + s.center_txt`.
- Content: a `cite("<bib_key>")` call from `streamtex.bib`.
- The actual reference data (author, year, URL) lives in the project's
  BibTeX file (`refs/refs.bib` or equivalent).

## Styling rules

| Element | Property | Value |
|---|---|---|
| Style | composition | `s.project.citation + s.large + s.center_txt` |
| Wrapping element | type | none — placed directly inside the slide flow |

## Code skeleton

```python
from streamtex import st_write, st_space
from streamtex.bib import cite
from custom.styles import Styles as s


class BlockStyles:
    source = s.project.citation + s.large + s.center_txt
bs = BlockStyles


def build():
    # ... slide content above ...
    st_space("v", 1)
    st_write(bs.source, cite("<bib_key>"))
```

## When to use

- After a statistic, factual claim, or quotation that needs attribution.
- At the bottom of a `stat_hero` or `evidence_insight` slide.
- After any block of body text that draws on external evidence.

## When NOT to use

- For inline references mid-sentence (use `cite()` directly inside an
  `st_write` tuple, not this footer pattern).
- When the source is a workshop facilitator note rather than a public
  reference (use a tooltip instead).
- On title slides — they should not carry citations.

## Examples

- `modules/ai4se6d_vibecoding/blocks/bck_vibecoding_danger_metr.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_evidence_paradox_ai.py`
- `modules/ai4se6d_gensem/blocks/bck_gensem_evidence_synthesis.py`

55 files in the `ai4se6d` corpus import `from streamtex.bib import cite`.

## Related patterns

- `stat_hero` — almost always pairs with a `cite` at the bottom
- `evidence_insight` — composes `stat_hero` + `cite` + `takeaways`
- `callout` — citation may appear under an emphasised claim
