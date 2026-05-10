---
name: composite_block
type: pattern
description: Composite block aggregating several atomic sub-blocks via st_include
tags: [docs, manual, composition, atomic]
extrapolable: true
since: 2026-05-10
---

# Composite Block

A block whose only role is to **compose** several atomic sub-blocks into
a single coherent section. Used in StreamTeX manuals to keep individual
files small and focused while still presenting a unified topic in the
TOC. Atomic sub-blocks live in a sibling `_atomic/` folder.

## Visual

```
   blocks/
   ├── bck_grids_and_lists.py        ← composite (this pattern)
   └── _atomic/
       ├── bck_grid_basics.py        ← rendered first
       ├── bck_grid_cell_styles.py   ← rendered second
       └── bck_lists.py              ← rendered third

   When the composite is registered in book.py, the rendered output is
   the concatenation of the three atomic blocks.
```

## Structure

- One Python file (the composite) at the regular block location.
- A `_atomic/` sibling folder containing the actual content blocks
  (`bck_*.py`).
- The composite imports each atomic block via `stx.load_atomic_block`
  and includes them with `st_include` inside its `build()`.
- The composite has an **empty** `BlockStyles` (no styles of its own —
  it only delegates).

## Styling rules

| Element | Property | Value |
|---|---|---|
| `BlockStyles` | content | empty (only a `pass` body, kept for convention) |
| Loading | call | `stx.load_atomic_block("<name>", __file__)` |
| Composition | call | `st_include(<atomic_block>)` |

## Code skeleton

```python
"""<Topic> — composite block grouping multiple atomic sub-blocks."""
import streamtex as stx
from streamtex import st_include


bck_part_a = stx.load_atomic_block("bck_part_a", __file__)
bck_part_b = stx.load_atomic_block("bck_part_b", __file__)
bck_part_c = stx.load_atomic_block("bck_part_c", __file__)


class BlockStyles:
    """Composite block — no styles of its own."""
    pass

bs = BlockStyles


def build():
    """Include atomic blocks for this section."""
    st_include(bck_part_a)
    st_include(bck_part_b)
    st_include(bck_part_c)
```

The atomic blocks (`_atomic/bck_part_a.py`, etc.) follow the
`manual_section` pattern individually.

## Extrapolation rules

### INVARIANTS (never change)

- The composite block lives at the regular block location;
  atomic blocks live in a `_atomic/` sibling folder.
- The composite **only includes** — no styles, no content, no
  conditional logic in `build()`.
- Atomic blocks loaded via `stx.load_atomic_block` (not regular import
  — the loader handles relative paths and registry).
- `st_include` is the inclusion mechanism — never copy-paste the build
  body of an atomic block.
- Each atomic block is **independently renderable** (declares its own
  `toc_lvl`, has its own `BlockStyles` etc.).

### PARAMS (adjustable)

- Number of atomic sub-blocks: 2 to ~6.
- Order of `st_include` calls determines render order in the TOC and
  in the final document.
- Atomic blocks may use any pattern (`manual_section`,
  `feature_walkthrough`, `api_reference_card`).
- The composite's filename signals the topic (`bck_grids_and_lists.py`
  → atomic blocks are about grids and lists).

### INTERDITS (forbidden)

- Do not put inline content in the composite's `build()` other than
  `st_include` calls (and possibly an opening `st_space` if needed).
- Do not load atomic blocks from outside the `_atomic/` sibling folder
  — keep co-location for clarity.
- Do not nest composites inside composites — flatten if a sub-topic
  needs its own composite, register both at top level.
- Do not duplicate `toc_lvl` between composite and atomic — only the
  atomic blocks declare TOC entries.

## When to use

- A topic that naturally splits into 3-6 sub-blocks of comparable size
  (each with its own `manual_section`).
- When a single block file would exceed ~200 lines and become unwieldy.
- When sub-blocks need to be reused across multiple composites.

## When NOT to use

- Topic fits in one block under ~200 lines → use `manual_section`
  directly.
- Composite of 1 atomic block → meaningless wrapper, just inline.
- Procedural walkthroughs that depend on each other → use
  `feature_walkthrough` in a single block.

## Examples

- `streamtex-docs/manuals/stx_manual_intro/blocks/bck_grids_and_lists.py`
  composes `_atomic/bck_grid_basics.py`,
  `_atomic/bck_grid_cell_styles.py`, `_atomic/bck_lists.py`.
- `streamtex-docs/manuals/stx_manual_intro/blocks/bck_containers_and_layout.py`

## Related patterns

- `manual_section` — used inside each atomic block
- `feature_walkthrough` — alternative when the topic is sequential
  rather than parallel sub-topics
