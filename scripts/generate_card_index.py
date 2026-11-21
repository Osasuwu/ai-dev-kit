"""Card index and watch-list generator (#340).

Writes two files at the repository root from the cards in `cards/`:

- `INDEX.md`: one line per card, for an agent to read first. A line has the card's kind, its
  title linked to the file, its `why`, its `applies_when` and, when the card has a `Guards`
  section, the failure classes it guards against followed by the caveat that the class evidence
  is one operator's practice. Lines run in the order the format lists the kinds, then by path.
  The generator refuses to write an index longer than the format's line limit.
- `WATCH-LIST.md`: every card's `Learn` bullets under the card's title, in the same order.

    python scripts/generate_card_index.py            # rewrite both files
    python scripts/generate_card_index.py --check    # exit 1 if either file would change

Inputs: the card format in `cards/README.md` (kinds, index line limit), the path definition in
`.github/hold-paths.json` (which files under `cards/` are cards), and the cards. The field names
it reads (`kind`, `why`, `applies_when`, `Learn`, `Guards`) are the structure gate's constants,
and the gate's format reader refuses a `cards/README.md` that drops any of them, so a rename in
the format alone fails here instead of emptying a column. It imports the structure gate's
readers from `tests/structure_gate.py`, so the gate and the generator read a card the same way. Card-relative links are rewritten to be relative to
the root, where both files live.

Install: nothing to install; Python 3.12+ and the standard library.
Check: `python scripts/generate_card_index.py --check` prints nothing and exits 0 when both
files are up to date. `tests/test_generate_card_index.py` runs the same comparison in the Tests
workflow, so a PR that changes a card without regenerating fails.
"""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tests"))

from structure_gate import (  # noqa: E402
    CARD_APPLIES,
    CARD_FORMAT_FILE,
    CARD_GUARDS,
    CARD_KIND_FIELD,
    CARD_LEARN,
    CARD_WHY,
    _load_hold_paths,
    _read_text,
    _rel,
    card_paths,
    load_card_format,
    read_card,
)

INDEX = "INDEX.md"
WATCH_LIST = "WATCH-LIST.md"
SCRIPT = "python scripts/generate_card_index.py"
CAVEAT = "class evidence is one operator's practice"

INDEX_HEAD = (
    "# Card index\n"
    "\n"
    f"Generated from `cards/` by `{SCRIPT}`; do not edit. One line per card: kind, card, why "
    "it matters, when it applies, the failure classes it guards against. Format and line "
    f"limit: [{CARD_FORMAT_FILE}]({CARD_FORMAT_FILE}).\n"
    "\n"
)
WATCH_LIST_HEAD = (
    "# Watch list\n"
    "\n"
    f"Generated from the `{CARD_LEARN}` sections in `cards/` by `{SCRIPT}`; do not edit. The "
    "talks and pages each card learns from, with what to look for in each.\n"
)

_LINK_RE = re.compile(r"(\[([^\]]*)\]\()([^)\s]+)(\))")


def _from_root(card_rel: str, target: str) -> str:
    """A link target written in a card, made relative to the repository root."""
    if "://" in target or target.startswith(("#", "mailto:")):
        return target
    return posixpath.normpath(posixpath.join(posixpath.dirname(card_rel), target))


def _rewrite_links(card_rel: str, text: str) -> str:
    return _LINK_RE.sub(
        lambda m: m.group(1) + _from_root(card_rel, m.group(3)) + m.group(4), text
    )


def _cards(root: Path) -> tuple[int, list[tuple[str, dict, str, dict[str, str]]]]:
    """(index line limit, [(path, fields, title, sections)] in index order)."""
    root = Path(root)
    problems: list = []
    fmt = load_card_format(root, problems)
    definition = _load_hold_paths(root, problems)
    if fmt is None or definition is None:
        raise ValueError("; ".join(p.message for p in problems))
    cards = []
    for path in card_paths(root, definition):
        rel = _rel(path, root)
        fields, title, sections = read_card(_read_text(path))
        if title is None or fields.get(CARD_KIND_FIELD) not in fmt.kinds:
            raise ValueError(
                f"{rel} is not a card the gate accepts; run tests/structure_gate.py"
            )
        cards.append((rel, fields, title, sections))
    cards.sort(key=lambda c: (fmt.kinds.index(c[1][CARD_KIND_FIELD]), c[0]))
    return fmt.index_line_limit, cards


def _index_line(rel: str, fields: dict, title: str, sections: dict[str, str]) -> str:
    parts = [
        f"- {fields[CARD_KIND_FIELD]}",
        f"[{title}]({rel})",
        str(fields.get(CARD_WHY, "")),
        f"when {fields.get(CARD_APPLIES, '')}",
    ]
    guards = [
        f"[{text}]({_from_root(rel, target)})"
        for _, text, target, _ in _LINK_RE.findall(
            sections.get(CARD_GUARDS.lower(), "")
        )
    ]
    if guards:
        parts.append(f"guards {', '.join(guards)} ({CAVEAT})")
    return " · ".join(parts)


def render_index(root: Path) -> str:
    limit, cards = _cards(root)
    text = INDEX_HEAD + "".join(_index_line(*card) + "\n" for card in cards)
    lines = text.count("\n")
    if lines > limit:
        raise ValueError(
            f"{INDEX} would have {lines} lines; the limit is {limit} ({CARD_FORMAT_FILE}). "
            "Merge or retire cards first."
        )
    return text


def render_watch_list(root: Path) -> str:
    _, cards = _cards(root)
    blocks = [
        f"\n## [{title}]({rel})\n\n"
        + _rewrite_links(rel, sections.get(CARD_LEARN.lower(), "").strip())
        + "\n"
        for rel, _, title, sections in cards
    ]
    return WATCH_LIST_HEAD + "".join(blocks)


def _current(root: Path, rel: str) -> str | None:
    path = root / rel
    return _read_text(path) if path.is_file() else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the card index and watch-list."
    )
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if either file would change"
    )
    parser.add_argument(
        "--root", default=str(Path(__file__).parent.parent), help="repository root"
    )
    args = parser.parse_args(argv)
    root = Path(args.root)
    try:
        expected = {INDEX: render_index(root), WATCH_LIST: render_watch_list(root)}
    except ValueError as error:
        print(f"generate_card_index: {error}")
        return 2
    stale = [rel for rel, text in expected.items() if _current(root, rel) != text]
    if args.check:
        for rel in stale:
            print(f"{rel} is out of date; run: {SCRIPT}")
        return 1 if stale else 0
    for rel in stale:
        (root / rel).write_bytes(expected[rel].encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
