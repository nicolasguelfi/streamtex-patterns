#!/usr/bin/env python3
"""
streamtex-patterns validator (A2 spec).

Standalone validator — depends only on the Python 3.11+ stdlib plus PyYAML.
It does NOT require the `streamtex` library to be installed.

Implements (a pragmatic subset of) the rules defined in
`documentation/maintenance/streamtex-patterns/SPEC.md` of the streamtex repo.

Usage:
    python scripts/validate.py --all
    python scripts/validate.py path/to/pattern.md [path/to/other.md ...]
    python scripts/validate.py --all --warnings-as-errors

Exit codes:
    0 — no errors (warnings may be present)
    1 — one or more errors found
    2 — usage / IO error
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "ERROR: PyYAML is required. Install with `pip install pyyaml`.\n"
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Constants — A2 spec
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

SCOPE_DIRS = ("core", "slides", "docs")  # plus "projects/<X>" handled separately

REQUIRED_FRONTMATTER_FIELDS = ("name", "type", "description", "extrapolable", "since")
ALLOWED_FRONTMATTER_FIELDS = REQUIRED_FRONTMATTER_FIELDS + ("tags",)

REQUIRED_SECTIONS = (
    "Visual",
    "Structure",
    "Styling rules",
    "Code skeleton",
    "When to use",
    "When NOT to use",
)
CANONICAL_ORDER = (
    "Visual",
    "Structure",
    "Styling rules",
    "Code skeleton",
    "Extrapolation rules",
    "When to use",
    "When NOT to use",
    "Examples",
    "Related patterns",
    "Changelog",
)

NAME_RE = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
FILENAME_RE = re.compile(r"^[a-z][a-z0-9_]*\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TAG_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*$")
PYTHON_FENCE_OPEN_RE = re.compile(r"^```python\s*$")
ANY_FENCE_RE = re.compile(r"^```")


# ---------------------------------------------------------------------------
# Diagnostic model
# ---------------------------------------------------------------------------

@dataclass
class Diag:
    severity: str  # "error" | "warning" | "info"
    rule: str  # e.g. "PV001"
    message: str
    file: Path | None = None
    line: int | None = None

    def format(self) -> str:
        loc = ""
        if self.file is not None:
            loc = str(self.file.relative_to(REPO_ROOT)) if self.file.is_absolute() and REPO_ROOT in self.file.parents else str(self.file)
            if self.line is not None:
                loc += f":{self.line}"
            loc += ": "
        return f"{loc}[{self.severity.upper()}/{self.rule}] {self.message}"


@dataclass
class Report:
    diags: list[Diag] = field(default_factory=list)

    def add(self, d: Diag) -> None:
        self.diags.append(d)

    def err(self, rule: str, msg: str, file: Path | None = None, line: int | None = None) -> None:
        self.add(Diag("error", rule, msg, file, line))

    def warn(self, rule: str, msg: str, file: Path | None = None, line: int | None = None) -> None:
        self.add(Diag("warning", rule, msg, file, line))

    def info(self, rule: str, msg: str, file: Path | None = None, line: int | None = None) -> None:
        self.add(Diag("info", rule, msg, file, line))

    @property
    def errors(self) -> list[Diag]:
        return [d for d in self.diags if d.severity == "error"]

    @property
    def warnings(self) -> list[Diag]:
        return [d for d in self.diags if d.severity == "warning"]

    @property
    def infos(self) -> list[Diag]:
        return [d for d in self.diags if d.severity == "info"]


# ---------------------------------------------------------------------------
# Frontmatter / body splitting
# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[str | None, str, int]:
    """
    Returns (frontmatter_text, body_text, body_start_line).

    body_start_line is 1-based and points to the first line of the body.
    frontmatter_text is None if delimiters are missing.
    """
    lines = text.splitlines(keepends=False)
    if not lines or lines[0].strip() != "---":
        return None, text, 1
    # find closing '---'
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1:])
            return fm, body, i + 2  # body lines are 1-based, after the '---'
    return None, text, 1


# ---------------------------------------------------------------------------
# Body section parsing
# ---------------------------------------------------------------------------

@dataclass
class Section:
    name: str  # H2 title (e.g. "Visual")
    start_line: int  # 1-based, line of the '## …' header (relative to file start)
    body_lines: list[str] = field(default_factory=list)
    body_start_line: int = 0


def parse_sections(body: str, body_start_line: int) -> list[Section]:
    """
    Parse H2 sections from the body. body_start_line is the 1-based file line
    of the first body line.

    Lines inside fenced code blocks are NOT scanned for headers.
    """
    sections: list[Section] = []
    current: Section | None = None
    in_fence = False
    fence_marker = ""

    body_lines = body.splitlines(keepends=False)
    for idx, raw in enumerate(body_lines):
        file_line = body_start_line + idx
        stripped = raw.lstrip()

        # toggle fence state on lines that start with ``` or ~~~ (3+)
        if not in_fence:
            m = re.match(r"^(```+|~~~+)", stripped)
            if m:
                in_fence = True
                fence_marker = m.group(1)[0] * 3  # only need first char triple
                if current is not None:
                    current.body_lines.append(raw)
                continue
        else:
            if stripped.startswith(fence_marker):
                in_fence = False
                if current is not None:
                    current.body_lines.append(raw)
                continue
            if current is not None:
                current.body_lines.append(raw)
            continue

        # outside fence
        h2 = H2_RE.match(raw)
        if h2:
            current = Section(
                name=h2.group(1).strip(),
                start_line=file_line,
                body_start_line=file_line + 1,
            )
            sections.append(current)
            continue

        if current is not None:
            current.body_lines.append(raw)

    return sections


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def validate_filename(path: Path, report: Report) -> str | None:
    """Return the stem if filename is valid, else None (and record the error)."""
    name = path.name
    if not FILENAME_RE.match(name):
        report.err("PV005", f"filename {name!r} violates naming rule ^[a-z][a-z0-9_]*\\.md$", file=path)
        return None
    stem = path.stem
    if not (2 <= len(stem) <= 64):
        report.err("PV005", f"filename stem {stem!r} length must be 2-64", file=path)
        return None
    return stem


def validate_frontmatter(
    fm_text: str | None,
    file_stem: str,
    path: Path,
    report: Report,
) -> dict | None:
    if fm_text is None:
        report.err("PV001", "frontmatter: missing leading or trailing '---'", file=path, line=1)
        return None

    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        line = getattr(getattr(exc, "problem_mark", None), "line", None)
        line_num = (line + 2) if isinstance(line, int) else None  # +2: skip leading '---'
        report.err("PV002", f"frontmatter: YAML parse error — {exc}", file=path, line=line_num)
        return None

    if not isinstance(data, dict):
        report.err("PV002", "frontmatter: expected a YAML mapping", file=path, line=1)
        return None

    # Required fields
    for f in REQUIRED_FRONTMATTER_FIELDS:
        if f not in data:
            report.err("PV003", f"frontmatter: missing required field {f!r}", file=path, line=1)

    # Unknown fields
    for k in data:
        if k not in ALLOWED_FRONTMATTER_FIELDS:
            report.err("PV003", f"frontmatter: unknown field {k!r} (allowed: {sorted(ALLOWED_FRONTMATTER_FIELDS)})", file=path, line=1)

    # name
    name = data.get("name")
    if isinstance(name, str):
        if not NAME_RE.match(name):
            report.err("PV003", f"frontmatter.name {name!r} must match ^[a-z][a-z0-9_]{{1,63}}$", file=path, line=1)
        if name != file_stem:
            report.err("PV004", f"frontmatter.name {name!r} does not match filename {file_stem!r}", file=path, line=1)
    elif "name" in data:
        report.err("PV003", "frontmatter.name must be a string", file=path, line=1)

    # type
    typ = data.get("type")
    if "type" in data and typ != "pattern":
        report.err("PV003", f"frontmatter.type must be the literal 'pattern' (got {typ!r})", file=path, line=1)

    # description
    desc = data.get("description")
    if isinstance(desc, str):
        if "\n" in desc or "\r" in desc:
            report.err("PV003", "frontmatter.description must be a single line", file=path, line=1)
        if not (10 <= len(desc) <= 100):
            report.err("PV003", f"frontmatter.description length {len(desc)} must be 10-100 chars", file=path, line=1)
    elif "description" in data:
        report.err("PV003", "frontmatter.description must be a string", file=path, line=1)

    # extrapolable
    extra = data.get("extrapolable")
    if "extrapolable" in data and not isinstance(extra, bool):
        report.err("PV003", f"frontmatter.extrapolable must be a boolean (got {type(extra).__name__})", file=path, line=1)

    # since
    since = data.get("since")
    if isinstance(since, str):
        if not DATE_RE.match(since):
            report.err("PV017", f"frontmatter.since {since!r} is not YYYY-MM-DD", file=path, line=1)
    elif "since" in data:
        # YAML may parse 2026-05-10 as a date object; accept that.
        try:
            from datetime import date as _date
            if not isinstance(since, _date):
                report.err("PV017", f"frontmatter.since must be a YYYY-MM-DD string (got {type(since).__name__})", file=path, line=1)
        except Exception:
            pass

    # tags
    tags = data.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            report.err("PV003", "frontmatter.tags must be a list of strings", file=path, line=1)
        else:
            seen: set[str] = set()
            for t in tags:
                if not isinstance(t, str):
                    report.err("PV003", f"frontmatter.tags: items must be strings (got {type(t).__name__})", file=path, line=1)
                    continue
                if not TAG_RE.match(t):
                    report.warn("PV018", f"tag {t!r} should match ^[a-z][a-z0-9_-]*$", file=path, line=1)
                if t in seen:
                    report.warn("PV018", f"duplicate tag {t!r}", file=path, line=1)
                seen.add(t)

    return data


def validate_sections(
    sections: list[Section],
    fm: dict,
    path: Path,
    report: Report,
) -> None:
    names = [s.name for s in sections]

    # PV007 — no duplicates
    seen: dict[str, int] = {}
    for s in sections:
        if s.name in seen:
            report.err("PV007", f"duplicate section '## {s.name}'", file=path, line=s.start_line)
        seen[s.name] = s.start_line

    # PV020 — exact 'When NOT to use'
    for s in sections:
        if s.name.lower() == "when not to use" and s.name != "When NOT to use":
            report.err("PV020", f"expected '## When NOT to use', got '## {s.name}'", file=path, line=s.start_line)

    # PV006 — required sections present
    missing = [r for r in REQUIRED_SECTIONS if r not in names]
    for m in missing:
        report.err("PV006", f"missing required section '## {m}'", file=path)

    # PV011 — extrapolable rule
    extrapolable = bool(fm.get("extrapolable"))
    has_extrap = "Extrapolation rules" in names
    if extrapolable and not has_extrap:
        report.err(
            "PV011",
            "extrapolable=true requires section '## Extrapolation rules' with INVARIANTS, PARAMS, INTERDITS",
            file=path,
        )
    if not extrapolable and has_extrap:
        report.err(
            "PV011",
            "extrapolable=false: section '## Extrapolation rules' must NOT be present",
            file=path,
        )

    # PV008 — canonical ordering of known sections (unknown ones are simply ignored)
    known = [n for n in names if n in CANONICAL_ORDER]
    canonical_indices = {n: i for i, n in enumerate(CANONICAL_ORDER)}
    last_idx = -1
    last_name = ""
    for n in known:
        idx = canonical_indices[n]
        if idx < last_idx:
            report.err(
                "PV008",
                f"section '## {n}' must precede '## {last_name}' (out of canonical order)",
                file=path,
            )
        else:
            last_idx = idx
            last_name = n


def _section(sections: list[Section], name: str) -> Section | None:
    for s in sections:
        if s.name == name:
            return s
    return None


def validate_visual(sections: list[Section], path: Path, report: Report) -> None:
    s = _section(sections, "Visual")
    if s is None:
        return
    # Strip fence delimiters and header for length count
    content_chars = 0
    in_fence = False
    fence = ""
    for line in s.body_lines:
        m = re.match(r"^(```+|~~~+)", line.lstrip())
        if m and not in_fence:
            in_fence = True
            fence = m.group(1)[0] * 3
            continue
        if in_fence and line.lstrip().startswith(fence):
            in_fence = False
            continue
        content_chars += len(line)
    if content_chars > 500:
        report.warn(
            "PV013",
            f"Visual section is {content_chars} chars, recommended <= 500",
            file=path,
            line=s.start_line,
        )


def validate_when_lists(sections: list[Section], path: Path, report: Report) -> None:
    for label in ("When to use", "When NOT to use"):
        s = _section(sections, label)
        if s is None:
            continue
        items = _count_top_bullets(s.body_lines)
        if not (2 <= items <= 6):
            report.warn(
                "PV014",
                f"'## {label}' has {items} item(s), expected 2-6",
                file=path,
                line=s.start_line,
            )


def _count_top_bullets(lines: list[str]) -> int:
    """Count top-level '- ' bullets, skipping fenced code."""
    count = 0
    in_fence = False
    fence = ""
    for line in lines:
        m = re.match(r"^(```+|~~~+)", line.lstrip())
        if m and not in_fence:
            in_fence = True
            fence = m.group(1)[0] * 3
            continue
        if in_fence and line.lstrip().startswith(fence):
            in_fence = False
            continue
        if in_fence:
            continue
        if re.match(r"^- \S", line):
            count += 1
    return count


def validate_styling_rules(sections: list[Section], path: Path, report: Report) -> None:
    s = _section(sections, "Styling rules")
    if s is None:
        return
    has_table = False
    has_kv_list = False
    for line in s.body_lines:
        if line.strip().startswith("|"):
            # crude — count pipes; need >= 3 columns (i.e. 4 pipes minimum on a row)
            cols = [c for c in line.split("|") if c.strip() != ""]
            if len(cols) >= 3:
                has_table = True
                break
    if not has_table:
        for line in s.body_lines:
            if re.match(r"^- \S+.*:\s*\S", line):
                has_kv_list = True
                break
    if not (has_table or has_kv_list):
        report.warn(
            "PV015",
            "Styling rules: expected table with >= 3 columns or '- key: value' list",
            file=path,
            line=s.start_line,
        )


def validate_code_skeleton(sections: list[Section], path: Path, report: Report) -> None:
    s = _section(sections, "Code skeleton")
    if s is None:
        return

    # Locate fenced python blocks. Per spec, the section MUST contain
    # exactly one ```python fence and no nested fences.
    py_blocks: list[tuple[int, int, list[str]]] = []  # (open_line, close_line, lines)
    other_fences = 0
    in_fence = False
    fence_lang = ""
    block_start = 0
    block_lines: list[str] = []

    for idx, line in enumerate(s.body_lines):
        file_line = s.body_start_line + idx
        stripped = line.lstrip()
        if not in_fence:
            m = re.match(r"^```([A-Za-z0-9_+-]*)\s*$", stripped)
            if m:
                in_fence = True
                fence_lang = m.group(1).strip().lower()
                block_start = file_line
                block_lines = []
                if fence_lang != "python":
                    other_fences += 1
                continue
        else:
            if stripped.startswith("```"):
                in_fence = False
                if fence_lang == "python":
                    py_blocks.append((block_start, file_line, block_lines))
                continue
            block_lines.append(line)

    if len(py_blocks) != 1:
        report.err(
            "PV009",
            f"code skeleton: expected exactly 1 python fence, found {len(py_blocks)}",
            file=path,
            line=s.start_line,
        )

    if other_fences > 0 and len(py_blocks) >= 1:
        # spec forbids non-python sibling fences in this section
        report.err(
            "PV009",
            f"code skeleton: forbidden non-python fenced block(s) in section ({other_fences} found)",
            file=path,
            line=s.start_line,
        )

    if py_blocks:
        open_line, _, code_lines = py_blocks[0]
        source = "\n".join(code_lines)
        try:
            ast.parse(source, mode="exec")
        except SyntaxError as exc:
            err_line = open_line + (exc.lineno or 0)
            report.err(
                "PV010",
                f"code skeleton: SyntaxError — {exc.msg}",
                file=path,
                line=err_line,
            )


def validate_extrapolation_rules(sections: list[Section], fm: dict, path: Path, report: Report) -> None:
    if not bool(fm.get("extrapolable")):
        return
    s = _section(sections, "Extrapolation rules")
    if s is None:
        return  # already reported by PV011

    # Find H3 headers among the body lines (outside fences).
    h3_tokens: list[tuple[str, int, int]] = []  # (first_word, file_line, body_index)
    in_fence = False
    fence = ""
    for idx, line in enumerate(s.body_lines):
        stripped = line.lstrip()
        if not in_fence:
            m = re.match(r"^(```+|~~~+)", stripped)
            if m:
                in_fence = True
                fence = m.group(1)[0] * 3
                continue
        else:
            if stripped.startswith(fence):
                in_fence = False
            continue
        h3 = H3_RE.match(line)
        if h3:
            title = h3.group(1).strip()
            first_word = title.split(None, 1)[0] if title else ""
            h3_tokens.append((first_word, s.body_start_line + idx, idx))

    expected = ["INVARIANTS", "PARAMS", "INTERDITS"]
    actual_words = [w for (w, _, _) in h3_tokens]
    if actual_words != expected:
        report.err(
            "PV011",
            f"## Extrapolation rules: H3 sub-sections must be exactly INVARIANTS, PARAMS, INTERDITS in that order (got {actual_words})",
            file=path,
            line=s.start_line,
        )

    # PV016 — each H3 must have >= 2 bullet items
    for k, (word, file_line, body_idx) in enumerate(h3_tokens):
        next_idx = h3_tokens[k + 1][2] if k + 1 < len(h3_tokens) else len(s.body_lines)
        sub_lines = s.body_lines[body_idx + 1:next_idx]
        items = _count_top_bullets(sub_lines)
        if items < 2:
            report.warn(
                "PV016",
                f"### {word} has {items} item(s), expected >= 2",
                file=path,
                line=file_line,
            )


def validate_trailing_newline(text: str, path: Path, report: Report) -> None:
    if not text.endswith("\n"):
        report.info("PV019", "file does not end with a newline", file=path)
    elif text.endswith("\n\n\n"):
        report.info("PV019", "file ends with multiple trailing newlines (single newline preferred)", file=path)


# ---------------------------------------------------------------------------
# Pattern file driver
# ---------------------------------------------------------------------------

def validate_pattern_file(path: Path, report: Report) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.err("PV000", f"cannot read file: {exc}", file=path)
        return

    stem = validate_filename(path, report)
    if stem is None:
        # still try to parse the rest for additional diagnostics
        stem = path.stem

    fm_text, body, body_start_line = split_frontmatter(text)
    fm = validate_frontmatter(fm_text, stem, path, report) or {}

    sections = parse_sections(body, body_start_line)
    validate_sections(sections, fm, path, report)
    validate_visual(sections, path, report)
    validate_when_lists(sections, path, report)
    validate_styling_rules(sections, path, report)
    validate_code_skeleton(sections, path, report)
    validate_extrapolation_rules(sections, fm, path, report)
    validate_trailing_newline(text, path, report)


# ---------------------------------------------------------------------------
# Presets and pattern_library coherence
# ---------------------------------------------------------------------------

def _is_pattern_candidate(path: Path) -> bool:
    """A pattern file is a snake_case .md file not starting with '_'.

    Files like README.md, NOTES.md, etc. are project documentation, not
    pattern files — they are skipped during auto-discovery (`--all`).
    Explicitly passing them on the command line will still flag PV005.
    """
    name = path.name
    if name.startswith("_"):
        return False
    return bool(FILENAME_RE.match(name))


def discover_pattern_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for scope in SCOPE_DIRS:
        d = repo_root / scope
        if d.is_dir():
            for p in sorted(d.glob("*.md")):
                if _is_pattern_candidate(p):
                    files.append(p)
    projects = repo_root / "projects"
    if projects.is_dir():
        for sub in sorted(projects.iterdir()):
            if sub.is_dir():
                for p in sorted(sub.glob("*.md")):
                    if _is_pattern_candidate(p):
                        files.append(p)
    return files


def validate_presets(repo_root: Path, report: Report) -> None:
    presets_dir = repo_root / "presets"
    if not presets_dir.is_dir():
        return
    for toml_path in sorted(presets_dir.glob("*.toml")):
        try:
            data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError, UnicodeDecodeError) as exc:
            report.err("PR001", f"preset: TOML parse error — {exc}", file=toml_path)
            continue

        patterns = data.get("patterns") or {}
        include = patterns.get("include") or []
        if not isinstance(include, list):
            report.err("PR002", "preset: [patterns].include must be a list", file=toml_path)
            continue
        for entry in include:
            if not isinstance(entry, str):
                report.err("PR002", f"preset: [patterns].include item must be a string (got {type(entry).__name__})", file=toml_path)
                continue
            target = repo_root / entry
            if not target.is_file():
                report.err(
                    "PR003",
                    f"preset: include path {entry!r} does not exist",
                    file=toml_path,
                )


def validate_pattern_library(repo_root: Path, report: Report) -> None:
    lib = repo_root / "_pattern_library.md"
    if not lib.is_file():
        report.warn("PL001", "_pattern_library.md not found at repo root", file=lib)
        return
    try:
        text = lib.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.err("PL002", f"cannot read _pattern_library.md: {exc}", file=lib)
        return

    auto_match = re.search(
        r"<!--\s*BEGIN AUTO\s*-->(.*?)<!--\s*END AUTO\s*-->",
        text,
        re.DOTALL,
    )
    if not auto_match:
        report.warn(
            "PL003",
            "_pattern_library.md: missing '<!-- BEGIN AUTO -->' / '<!-- END AUTO -->' block",
            file=lib,
        )
        return

    block = auto_match.group(1)
    listed: set[str] = set()
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Name"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0] and cells[0] not in ("Name",):
            listed.add(cells[0])

    actual = {p.stem for p in discover_pattern_files(repo_root)}

    only_listed = listed - actual
    only_actual = actual - listed
    for n in sorted(only_listed):
        report.err(
            "PL004",
            f"_pattern_library.md AUTO block lists {n!r} but no matching <scope>/{n}.md exists",
            file=lib,
        )
    for n in sorted(only_actual):
        report.err(
            "PL005",
            f"pattern {n!r} exists on disk but is not listed in _pattern_library.md AUTO block",
            file=lib,
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="validate.py",
        description="Validate streamtex-patterns files against the A2 spec.",
    )
    p.add_argument(
        "files",
        nargs="*",
        help="Pattern files to validate (relative to repo root). Ignored when --all is used.",
    )
    p.add_argument(
        "--all",
        action="store_true",
        help="Discover and validate every pattern under core/, slides/, docs/, projects/<X>/",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: parent of this script's directory)",
    )
    p.add_argument(
        "--warnings-as-errors",
        "-W",
        action="store_true",
        help="Treat warnings as errors (CI-strict mode).",
    )
    p.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Print only errors (suppress warnings and info).",
    )
    return p.parse_args(argv)


def gather_targets(args: argparse.Namespace) -> list[Path]:
    if args.all:
        return discover_pattern_files(args.repo_root)
    targets: list[Path] = []
    for f in args.files:
        p = Path(f)
        if not p.is_absolute():
            p = (args.repo_root / p).resolve()
        targets.append(p)
    return targets


def print_report(report: Report, quiet: bool) -> None:
    # group by file for readability
    by_file: dict[str, list[Diag]] = {}
    for d in report.diags:
        key = str(d.file) if d.file else "<global>"
        by_file.setdefault(key, []).append(d)
    for key in sorted(by_file):
        diags = by_file[key]
        if quiet:
            diags = [d for d in diags if d.severity == "error"]
        if not diags:
            continue
        for d in diags:
            print(d.format())


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.all and not args.files:
        sys.stderr.write("ERROR: pass --all or one or more file paths.\n")
        return 2

    repo_root: Path = args.repo_root.resolve()
    if not (repo_root / "manifest.toml").is_file():
        sys.stderr.write(
            f"ERROR: {repo_root} does not look like the streamtex-patterns repo "
            f"(no manifest.toml at root).\n"
        )
        return 2

    report = Report()

    # File-level validation
    for path in gather_targets(args):
        if not path.is_file():
            report.err("PV000", f"file not found: {path}", file=path)
            continue
        validate_pattern_file(path, report)

    # Repo-level validation when running --all
    if args.all:
        validate_presets(repo_root, report)
        validate_pattern_library(repo_root, report)

    print_report(report, quiet=args.quiet)

    n_err = len(report.errors)
    n_warn = len(report.warnings)
    n_info = len(report.infos)
    print()
    print(f"streamtex-patterns validation: {n_err} error(s), {n_warn} warning(s), {n_info} info")

    if n_err > 0:
        return 1
    if args.warnings_as_errors and n_warn > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
