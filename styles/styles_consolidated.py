"""StreamTeX — Consolidated style bundles.

Reference / template module that gathers the **reusable style bundles**
that would have covered every common need observed across the
551 blocks audited on 2026-05-11 (ai4se6d: 297 blocks; streamtex-docs:
254 blocks).

This file is NOT a project's `custom/styles.py`. It is the canonical
**bundle vocabulary** of streamtex-patterns. A consuming project can:

  1. Copy this file as a starting point for `custom/styles.py` and
     adjust the palette / sizes only.
  2. Import individual bundles and recompose into a project-local
     `Styles` class.
  3. Use the canonical attribute names (e.g. `s.project.callouts.info`,
     `s.project.keywords.warn`) so that patterns whose code skeletons
     reference these names work out of the box.

Each bundle is exposed both as a stand-alone class (for selective
import) and aggregated under `Project` / `Styles` at the bottom (for
a drop-in install).

────────────────────────────────────────────────────────────────────────
Bundle map (see bottom of this file for the canonical aggregation)

  Colors        — 6 semantic palette colors + 3 named hues
  Backgrounds   — 6 tinted backgrounds for callouts/cells
  Titles        — slide / section / subtitle / body / caption / page
  Headings      — centered title aliases (slide_heading, section_heading…)
  Keywords      — inline bold-color emphasis (primary, accent, warn,
                  critical, success, violet)
  StatHero      — 3 variants of the slide centerpiece statistic
  Table         — comparison-table text styles (header, cell, label…)
  Citation      — bibliographic source attribution (base + composed)
  Callouts      — 4 framed-container variants (info / warning /
                  critical / success)
  CellTints     — 3 cell background tints (primary / accent / active)
  Cells         — bordered + table cell containers, grid centering
  PageFill      — 4 viewport-filling page layouts
  Grid          — responsive column templates + gap presets
  DocPage       — manual-specific (mono_heading, description_muted,
                  file_label, step_label, cmd_title)
  Emphasis      — closing punch line + question highlight

  make_banner_header(...) — parametric gradient header builder

Naming conventions used in this file:

  - Semantic > visual. `Keywords.warn` not `Keywords.amber_bold`.
  - Explicit hierarchy in headings (`slide_heading`, `section_heading`,
    `page_heading`) — never a bare `heading`, which proved polysemous
    across the audited blocks.
  - Bundle classes are PascalCase, attributes snake_case.
  - Colors carry the palette default; override hex per project.

────────────────────────────────────────────────────────────────────────
"""

from streamtex.styles import Container, StxStyles, Style, Text


# ============================================================================
# 1. Colors — semantic palette (project-overridable hex values)
# ============================================================================


class Colors:
    """Semantic palette. Override the hex values in your project file.

    Six core slots cover every callout / emphasis variant observed in
    the audit; three named hues (violet / teal / amber) are kept as
    explicit aliases for projects whose visual language references the
    colour rather than its semantic role (docs manuals tend to do this).
    """

    # Core semantic slots
    primary = Style("color: #7AB8F5;", "primary")
    accent = Style("color: #2EC4B6;", "accent")
    highlight = Style("color: #F39C12;", "highlight")
    success = Style("color: #27AE60;", "success")
    critical = Style("color: #E74C3C;", "critical")
    muted = Style("color: #95A5A6;", "muted")

    # Named hues (visual aliases — used by some docs manuals)
    violet = Style("color: #a78bfa;", "violet")
    teal = Style("color: #2EC4B6;", "teal")
    amber = Style("color: #F39C12;", "amber")


# ============================================================================
# 2. Backgrounds — tinted overlays for callouts and cells
# ============================================================================


class Backgrounds:
    """Translucent background tints aligned with the Colors palette."""

    info_bg = Style(
        "background-color: rgba(122, 184, 245, 0.12);", "info_bg",
    )
    warning_bg = Style(
        "background-color: rgba(243, 156, 18, 0.12);", "warning_bg",
    )
    critical_bg = Style(
        "background-color: rgba(231, 76, 60, 0.15);", "critical_bg",
    )
    success_bg = Style(
        "background-color: rgba(39, 174, 96, 0.15);", "success_bg",
    )
    accent_bg = Style(
        "background-color: rgba(46, 196, 182, 0.12);", "accent_bg",
    )
    muted_bg = Style(
        "background-color: rgba(149, 165, 166, 0.08);", "muted_bg",
    )


# ============================================================================
# 3. Titles — projection-safe title hierarchy
# ============================================================================


class Titles:
    """Title hierarchy tuned for live projection (10–20 m audience).

    Size scale (StreamTeX names → approx. pt):
      Huge  ≈ 96 pt  → slide_title (one per slide)
      huge  ≈ 80 pt  → section_title
      LARGE ≈ 64 pt  → page_title (manuals)
      Large ≈ 48 pt  → subtitle, body
      large ≈ 32 pt  → caption
    """

    slide_title = Style.create(
        Colors.primary
        + Text.weights.bold_weight
        + Text.sizes.Huge_size,
        "slide_title",
    )
    section_title = Style.create(
        Colors.accent
        + Text.weights.bold_weight
        + Text.sizes.huge_size,
        "section_title",
    )
    page_title = Style.create(
        Colors.primary
        + Text.weights.bold_weight
        + Text.sizes.LARGE_size,
        "page_title",
    )
    subtitle = Style.create(
        Colors.highlight
        + Text.weights.bold_weight
        + Text.sizes.Large_size,
        "subtitle",
    )
    body = Style.create(Text.sizes.Large_size, "body")
    caption = Style.create(
        Colors.muted + Text.sizes.large_size,
        "caption",
    )


# ============================================================================
# 4. Headings — centered title aliases
#    (Resolves the polysemous local `heading = X + center_txt` pattern
#    observed 480× across the audited blocks, with X varying silently.)
# ============================================================================


class Headings:
    """Centered heading aliases. Explicit names per hierarchy level.

    Replaces the bare `heading` attribute — which carried 11 distinct
    expressions in the audit — with discriminating names so the
    intended hierarchy is always obvious in the call site.
    """

    slide_heading = Titles.slide_title + StxStyles.center_txt
    section_heading = Titles.section_title + StxStyles.center_txt
    page_heading = Titles.page_title + StxStyles.center_txt
    subtitle_centered = Titles.subtitle + StxStyles.center_txt


# ============================================================================
# 5. Keywords — inline bold-colored emphasis
# ============================================================================


class Keywords:
    """Inline emphasis palette for tuple-style mixed text.

    Used inside `st_write(<base>, (Keywords.primary, "term"), …)`.
    Each variant encodes a semantic role through its color so a future
    reader can guess intent without re-reading the surrounding prose.
    """

    primary = Text.weights.bold_weight + Colors.primary
    accent = Text.weights.bold_weight + Colors.accent
    highlight = Text.weights.bold_weight + Colors.highlight
    success = Text.weights.bold_weight + Colors.success
    critical = Text.weights.bold_weight + Colors.critical
    violet = Text.weights.bold_weight + Colors.violet

    # Semantic alias — "warning emphasis" reads better than "highlight" in code
    warn = Text.weights.bold_weight + Colors.highlight


# ============================================================================
# 6. StatHero — slide centerpiece statistic (3 variants)
# ============================================================================


class StatHero:
    """Hero-statistic styles for `ptn_stat_hero`.

    Three variants encoded by color:
      default  — highlight (the "wow" stat)
      primary  — primary color (neutral hero)
      critical — critical red (alarming stat)
    """

    default = Style.create(
        Text.sizes.GIANT_size
        + Text.weights.bold_weight
        + Colors.highlight
        + StxStyles.center_txt,
        "stat_hero",
    )
    primary = Style.create(
        Text.sizes.GIANT_size
        + Text.weights.bold_weight
        + Colors.primary
        + StxStyles.center_txt,
        "stat_hero_primary",
    )
    critical = Style.create(
        Text.sizes.GIANT_size
        + Text.weights.bold_weight
        + Colors.critical
        + StxStyles.center_txt,
        "stat_hero_critical",
    )


# ============================================================================
# 7. Table — comparison-table text styles
#    (Used by `ptn_comparison_table` and its sequence/timeline variant.)
# ============================================================================


class Table:
    """Text styles for comparison-table cells.

    Composes with `Cells.table_*_cell` for the container side. Keeps
    columns aligned at a consistent ~36 pt body height with hyphenation
    enabled to avoid overflow in narrow columns.
    """

    header_text = Style.create(
        Text.sizes.pt36
        + Text.weights.bold_weight
        + Colors.accent
        + Text.wrap.hyphens,
        "table_header_text",
    )
    cell_text = Style.create(
        Text.sizes.pt36 + Text.wrap.hyphens,
        "table_cell_text",
    )
    label_text = Style.create(
        Text.sizes.pt36
        + Text.weights.bold_weight
        + Colors.primary
        + Text.wrap.hyphens,
        "table_label_text",
    )
    label_active = Style.create(
        Text.sizes.pt36
        + Text.weights.bold_weight
        + Colors.highlight
        + Text.wrap.hyphens,
        "table_label_active",
    )


# ============================================================================
# 8. Citation — bibliographic source attribution
# ============================================================================


class Citation:
    """Citation styling — base + composed footer variant."""

    base = Style(
        "color: #81C784; font-style: italic;", "citation_base",
    )
    source = base + Text.sizes.large_size + StxStyles.center_txt


# ============================================================================
# 9. Callouts — 4 framed container variants
# ============================================================================


class Callouts:
    """Container styles for `ptn_callout`.

    Each variant = background tint + 4 px coloured left border +
    medium padding. Semantic encoding is reinforced by `Keywords.*`
    on the inline label inside the container.
    """

    info = Style.create(
        Backgrounds.info_bg
        + Container.borders.solid_border
        + Style(
            "border-color: #7AB8F5; border-width: 0 0 0 4px;",
            "callout_info_border",
        )
        + Container.paddings.medium_padding,
        "callout_info",
    )
    warning = Style.create(
        Backgrounds.warning_bg
        + Container.borders.solid_border
        + Style(
            "border-color: #F39C12; border-width: 0 0 0 4px;",
            "callout_warning_border",
        )
        + Container.paddings.medium_padding,
        "callout_warning",
    )
    critical = Style.create(
        Backgrounds.critical_bg
        + Container.borders.solid_border
        + Style(
            "border-color: #E74C3C; border-width: 0 0 0 4px;",
            "callout_critical_border",
        )
        + Container.paddings.medium_padding,
        "callout_critical",
    )
    success = Style.create(
        Backgrounds.success_bg
        + Container.borders.solid_border
        + Style(
            "border-color: #27AE60; border-width: 0 0 0 4px;",
            "callout_success_border",
        )
        + Container.paddings.medium_padding,
        "callout_success",
    )


# ============================================================================
# 10. CellTints — coloured cell backgrounds for grids
# ============================================================================


class CellTints:
    """Cell backgrounds for `ptn_categorized_grid` and its timeline variant.

    Three tints, semantic encoding:
      primary — neutral / "the existing"
      accent  — novelty / "AI-native"
      active  — current focus / "you are here"
    """

    primary = Style(
        "background-color: rgba(122, 184, 245, 0.08); "
        "border: 1px solid rgba(122, 184, 245, 0.3); "
        "border-radius: 10px;",
        "cell_primary_bg",
    )
    accent = Style(
        "background-color: rgba(46, 196, 182, 0.2); "
        "border: 1px solid rgba(46, 196, 182, 0.5); "
        "border-radius: 10px;",
        "cell_accent_bg",
    )
    active = Style(
        "background-color: rgba(243, 156, 18, 0.15); "
        "border: 2px solid #F39C12; "
        "border-radius: 10px;",
        "cell_active_bg",
    )


# ============================================================================
# 11. Cells — bordered cell containers and table cells
# ============================================================================


# Two padding presets reused across cell containers (avoid repetition below).
_CELL_PAD_SM = Style("padding: 8px 12px;", "cell_pad_sm")
_CELL_PAD_MD = Style("padding: 12px 16px;", "cell_pad_md")


class Cells:
    """Cell container styles for `st_grid(cell_styles=...)`.

    The four most common cell shapes observed in the audit:
      bordered         — solid border + small padding + vertical center
      bordered_centered— bordered + text centered (most common in docs)
      centered         — no border, just vertical centering + text-center
      table_*_cell     — table-row cells with one of the three CellTints
    """

    bordered = Style.create(
        Container.borders.solid_border
        + Container.paddings.small_padding
        + Container.layouts.vertical_center_layout,
        "cell_bordered",
    )
    bordered_centered = Style.create(
        Container.borders.solid_border
        + Container.paddings.small_padding
        + Container.layouts.vertical_center_layout
        + StxStyles.center_txt,
        "cell_bordered_centered",
    )
    centered = Style.create(
        Container.layouts.vertical_center_layout + StxStyles.center_txt,
        "cell_centered",
    )

    table_header_cell = Style.create(
        CellTints.accent
        + _CELL_PAD_SM
        + Container.layouts.vertical_center_layout
        + StxStyles.center_txt,
        "table_header_cell",
    )
    table_normal_cell = Style.create(
        CellTints.primary
        + _CELL_PAD_SM
        + Container.layouts.vertical_center_layout
        + StxStyles.center_txt,
        "table_normal_cell",
    )
    table_active_cell = Style.create(
        CellTints.active
        + _CELL_PAD_SM
        + Container.layouts.vertical_center_layout
        + StxStyles.center_txt,
        "table_active_cell",
    )

    # Padded card cells (used by `ptn_card_grid` and the categorized variant)
    card_primary = Style.create(
        CellTints.primary + _CELL_PAD_MD + StxStyles.center_txt,
        "card_primary",
    )
    card_accent = Style.create(
        CellTints.accent + _CELL_PAD_MD + StxStyles.center_txt,
        "card_accent",
    )
    card_active = Style.create(
        CellTints.active + _CELL_PAD_MD + StxStyles.center_txt,
        "card_active",
    )


# ============================================================================
# 12. PageFill — viewport-filling page layouts
# ============================================================================


class PageFill:
    """Page-level layout containers (min-height ≈ 85 vh)."""

    top = Style(
        "display:flex;flex-direction:column;justify-content:flex-start;"
        "min-height:85vh;gap:1.5rem;",
        "page_fill_top",
    )
    center = Style(
        "display:flex;flex-direction:column;justify-content:center;"
        "align-items:center;min-height:85vh;gap:1.5rem;",
        "page_fill_center",
    )
    center_wide = Style(
        "display:flex;flex-direction:column;justify-content:center;"
        "align-items:center;min-height:85vh;gap:2rem;",
        "page_fill_center_wide",
    )
    center_noalign = Style(
        "display:flex;flex-direction:column;justify-content:center;"
        "min-height:85vh;gap:2rem;",
        "page_fill_center_noalign",
    )


# ============================================================================
# 13. Grid — responsive column templates and gaps
# ============================================================================


class Grid:
    """Grid presets — `cols` strings and gap helpers.

    The `cols` attributes are plain strings (suitable for direct use in
    `st_grid(cols=Grid.responsive_3col)`). The `gap_*` attributes are
    Style instances composable into `cell_styles=...`.
    """

    # `cols` presets (use directly in st_grid)
    responsive_2col = "repeat(auto-fit, minmax(350px, 1fr))"
    responsive_3col = "repeat(auto-fit, minmax(280px, 1fr))"
    responsive_4col = "repeat(auto-fit, minmax(220px, 1fr))"

    # Fixed-ratio presets (recurrent layouts)
    title_with_tooltip = "95% 5%"
    image_text_split = "1fr 2fr"
    image_text_wide = "2fr 3fr"
    morning_afternoon = "1fr 1fr"
    three_equal = "1fr 1fr 1fr"

    # Gap Style helpers (composable into a grid's cell_styles)
    gap_8 = Style("gap: 8px;", "gap_8")
    gap_12 = Style("gap: 12px;", "gap_12")
    gap_16 = Style("gap: 16px;", "gap_16")
    gap_24 = Style("gap: 24px;", "gap_24")
    gap_32 = Style("gap: 32px;", "gap_32")


# ============================================================================
# 14. DocPage — manual-specific styles (mono headings, file labels, …)
# ============================================================================


class DocPage:
    """Documentation-manual specific styles.

    Used by patterns scoped to `docs/` (`ptn_manual_section`,
    `ptn_api_reference_card`, `ptn_feature_walkthrough`,
    `ptn_composite_block`) and by the manual-internal blocks
    (intro, scan_rule, cli_overview, extrapolation…).
    """

    # Monospace heading for API-reference card titles
    mono_heading = Style.create(
        Text.sizes.Large_size
        + Text.weights.bold_weight
        + Text.fonts.font_monospace
        + StxStyles.center_txt
        + Colors.violet,
        "doc_mono_heading",
    )

    # Muted italic description (under API signatures, beneath images)
    description_muted = Style.create(
        Text.sizes.large_size
        + Style("font-style: italic;", "doc_italic_inline")
        + Colors.muted,
        "doc_description_muted",
    )

    # File label (e.g. "bck_intro.py" beneath a code example)
    file_label = Style.create(
        Text.sizes.medium_size
        + Style("font-style: italic;", "doc_italic_inline2")
        + Colors.muted,
        "doc_file_label",
    )

    # Step label inside walkthroughs (e.g. "Step 1.", "Step 2.")
    step_label = Style.create(
        Colors.violet
        + Text.weights.bold_weight
        + Text.sizes.large_size,
        "doc_step_label",
    )

    # CLI command title (e.g. "$ stx patterns install")
    cmd_title = Style.create(
        Colors.violet
        + Text.weights.bold_weight
        + Text.sizes.Large_size,
        "doc_cmd_title",
    )


# ============================================================================
# 15. Emphasis — closing punch line and question highlight
# ============================================================================


class Emphasis:
    """Closing / punch-line styles for `ptn_takeaways` and recap slides.

    Two named slots:
      closing — bolded body + highlight color (closes a takeaway list)
      question — bolded body + primary, centered (opens a debrief slide)
    """

    closing = (
        Titles.body
        + Colors.highlight
        + Text.weights.bold_weight
    )
    question = (
        Titles.body
        + Colors.primary
        + Text.weights.bold_weight
        + StxStyles.center_txt
    )


# ============================================================================
# Helper — parametric banner header
# ============================================================================


def make_banner_header(
    color_from: str,
    color_to: str,
    *,
    padding: str = "40px 20px",
    radius: str = "8px",
) -> Style:
    """Build a banner-header style from a 2-stop linear gradient.

    Replaces the ~9 occurrences of ad-hoc gradient bandeaux observed in
    the audit (each manual rolled its own with slightly different
    colours). Use as the outer container of a section-opening slide.

    Args:
        color_from: starting CSS color, e.g. "#7AB8F5".
        color_to:   ending CSS color, e.g. "#a78bfa".
        padding:    CSS padding shorthand (default "40px 20px").
        radius:     border-radius (default "8px").
    """
    # Build a stable style_id from the two hex values (strip the '#').
    sid = f"banner_{color_from.lstrip('#')}_{color_to.lstrip('#')}"
    return Style(
        f"background: linear-gradient(135deg, {color_from} 0%, "
        f"{color_to} 100%); "
        f"padding: {padding}; border-radius: {radius};",
        sid,
    )


# ============================================================================
# Project aggregation
# ============================================================================


class Project:
    """Canonical aggregation — exposes every bundle under one root.

    A consumer project would typically:
      1. Subclass `Colors` to override the palette.
      2. Re-instantiate every bundle that depends on the colors (most
         bundles already reference `Colors.*` symbolically, so a class
         attribute swap is enough).
      3. Add project-specific bundles next to the canonical ones (e.g.
         GSE letter colors, custom slide-title fonts).
    """

    colors = Colors
    backgrounds = Backgrounds

    titles = Titles
    headings = Headings
    keywords = Keywords
    emphasis = Emphasis

    stat_hero = StatHero
    table = Table
    callouts = Callouts

    cell_tints = CellTints
    cells = Cells

    page_fill = PageFill
    grid = Grid

    doc = DocPage

    # Citation kept at two levels for compatibility with current
    # shared_styles.py which exposes `project.citation` as the base style.
    citation = Citation.base
    citation_source = Citation.source

    # Helper exposed on the project root for symmetry with the bundles.
    banner_header = staticmethod(make_banner_header)


class Styles(StxStyles):
    """Drop-in `Styles` class — inherits StreamTeX defaults + bundles.

    Usage in a project's `custom/styles.py`:

        from streamtex_patterns.styles.styles_consolidated import (
            Styles as ConsolidatedStyles,
        )

        class Styles(ConsolidatedStyles):
            # Override what differs in this project, e.g.:
            class colors(ConsolidatedStyles.project.colors):
                primary = Style("color: #FF6B6B;", "primary")

    Or copy this whole file into `custom/styles.py` and edit in place.
    """

    project = Project


# ============================================================================
# Public re-exports — for `from styles_consolidated import *`
# ============================================================================


__all__ = [
    # Bundles
    "Colors",
    "Backgrounds",
    "Titles",
    "Headings",
    "Keywords",
    "Emphasis",
    "StatHero",
    "Table",
    "Citation",
    "Callouts",
    "CellTints",
    "Cells",
    "PageFill",
    "Grid",
    "DocPage",
    # Helper
    "make_banner_header",
    # Aggregations
    "Project",
    "Styles",
]
