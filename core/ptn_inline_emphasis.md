---
name: ptn_inline_emphasis
type: pattern
description: Inline keyword/label/accent variants for mixed-style text inside a single st_write
tags: [inline, text, emphasis]
extrapolable: true
since: 2026-05-10
---

# Inline Emphasis

A set of three reusable inline styles — `keyword`, `label`, `accent` — used
inside a single `st_write` to mix emphasized fragments into a sentence
without breaking the line. The variants encode meaning, not just visual
weight: `keyword` for the dominant primary color, `accent` for the
accent/secondary, `highlight` for the warning/critical secondary tone.

## Visual

```
   "Predicted AI would make them <KEYWORD>24% faster</KEYWORD>."
   "<HIGHLIGHT>still believed</HIGHLIGHT> they were 20% faster."
   "Open Cursor with <ACCENT>.cursor</ACCENT> profile."
```

## Structure

- A single `st_write(bs.body, ...)` call.
- Each emphasized fragment is a tuple `(<inline_style>, "text")`.
- Multiple tuples can be combined in one call to compose mixed-style text.

## Styling rules

| Variant | Composition | Semantic role |
|---|---|---|
| `keyword` | `s.bold + s.project.colors.primary` | the dominant emphasized term in a sentence |
| `accent` | `s.bold + s.project.colors.accent` | a secondary highlight (often a tool name, identifier) |
| `highlight` | `s.bold + s.project.colors.highlight` | a warning, paradox or surprising fact |
| `label` | `s.bold + s.project.colors.primary + s.center_txt` | a short caption used as a list-item lead-in |

When the block already has its own `BlockStyles`, define the variants
locally on top of `bs.body` (so the size matches the surrounding text):

```python
keyword = s.bold + s.project.colors.primary
accent  = s.bold + s.project.colors.accent
highlight = s.bold + s.project.colors.highlight
```

## Code skeleton

```python
from streamtex import st_write
from custom.styles import Styles as s

class BlockStyles:
    body = s.project.titles.body
    keyword = s.bold + s.project.colors.primary
    accent = s.bold + s.project.colors.accent
    highlight = s.bold + s.project.colors.highlight
    label = s.bold + s.project.colors.primary + s.center_txt
bs = BlockStyles

def build():
    # Single st_write with mixed-style fragments
    st_write(
        bs.body,
        "Predicted AI would make them ",
        (bs.keyword, "24% faster"),
        ".",
    )
    st_write(
        bs.body,
        (bs.highlight, "still believed"),
        " they were 20% faster.",
    )
    st_write(
        bs.body,
        (bs.label, "1. "),
        (bs.keyword, "Install GSE-One"),
        " from GitHub.",
    )
```

## Extrapolation rules

### INVARIANTS (never change)

- Each variant maps to a **specific semantic role**, not merely a color
  — a "warning fact" is `highlight`, a "primary term" is `keyword`.
- Always one `st_write` call per visual line; mixed styles are composed
  via tuples, never via multiple stacked `st_write` calls.
- Inline styles inherit size from the surrounding `body` style — do not
  hardcode font sizes on the inline variant itself.

### PARAMS (adjustable)

- A block may add a fourth variant for its specific need (e.g.
  `keyword_warn` combining `bold + highlight`).
- Variants may be wrapped at the top of the block in `BlockStyles` for
  local reuse.
- Combine with project text utilities (e.g. `s.text.wrap.hyphens`) when
  needed.

### INTERDITS (forbidden)

- Do not split a mixed-style sentence across multiple `st_write` calls
  to "emphasize" — they stack vertically as separate paragraphs.
- Do not invent new semantic colors outside the project palette
  (`primary`, `accent`, `highlight`, `success`, `critical`, `muted`).
- Do not embed inline HTML or `<span>` tags — the StreamTeX styling
  system handles all inline formatting via tuples.

## When to use

- Any sentence where 1–3 fragments need stronger emphasis than the
  surrounding text (statistics, identifiers, paradoxical phrases).
- List item leads (`1. <keyword>Install</keyword> ...`).
- Body explanation under a `ptn_stat_hero`.

## When NOT to use

- For long blocks of bold text — promote them to a separate
  `st_write(bs.bold_style, ...)` instead.
- For decorative emphasis with no semantic role — keep usage meaningful.
- For headings — use `ptn_slide_heading` styles, not inline emphasis.

## Examples

Live demo and gallery blocks (in the `stx_manual_patterns` documentation
manual):

- `streamtex-docs/manuals/stx_manual_patterns/blocks/bck_gallery_atoms.py` — `inline_emphasis` showcased with
  every variant (`label`, `keyword`, `accent`, `highlight`, `critical`,
  `success`).

Run the manual locally with `./run-manuals.sh --patterns` (port 8508).

## Related patterns

- `ptn_takeaways` — heavy user of `label` + `keyword` lead-ins
- `ptn_callout` — accent / highlight variants pair with critical / warning
  callouts
