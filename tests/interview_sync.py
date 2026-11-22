"""Sync check for the interview prompt's two languages (#344, #336 item 1).

`prompts/interview.en.md` and `prompts/interview.ru.md` are kept by hand, one per language.
This check keeps their questions in step:

- Each file has one questions section, between the lines `<!-- questions:start -->` and
  `<!-- questions:end -->`.
- Every top-level numbered item in that section is a question and opens with a tag,
  `1. <!-- q:<id> --> <question text>`. The id is lowercase letters, digits and hyphens.
  A question runs from its tag line to the next item or the end of the section.
- A `<!-- q:` tag anywhere else in the file (after the section, on a bullet, mid-line) fails,
  so a question cannot be added where the check does not count it.
- Both files list the same ids in the same order. A question added, dropped or moved in one
  file and not the other fails, and so does an untagged question or an id used twice.
- Each question has as many question marks in one file as in the other, so a sub-question
  added in one language only fails.
- Each question in the Russian file has Russian text on its tag line, so an English question
  pasted into the Russian file unchanged fails too.

The check reads the question structure only. It cannot tell whether a translation says the
same thing; a reviewer reading both files does that.

`tests/test_interview_sync.py` runs it on the shipped files, inside the required `tests` check.
"""

from __future__ import annotations

import re
from pathlib import Path

START = "<!-- questions:start -->"
END = "<!-- questions:end -->"
TAG = "<!-- q:"

PROMPTS = Path("prompts")
EN_PROMPT = PROMPTS / "interview.en.md"
RU_PROMPT = PROMPTS / "interview.ru.md"

_ITEM = re.compile(r"^\d+\.\s")
_TAGGED = re.compile(r"^\d+\.\s+<!-- q:([a-z0-9-]+) -->\s*(.*)$")
_CYRILLIC = re.compile(r"[А-Яа-яЁё]")


def questions(
    text: str, label: str, *, russian: bool = False
) -> tuple[list[tuple[str, int]], list[str]]:
    """One prompt's questions in order as (id, question marks), and the errors reading them."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == START]
    ends = [i for i, line in enumerate(lines) if line.strip() == END]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        return [], [
            f"{label}: needs exactly one {START} line followed by one {END} line"
        ]
    first, last = starts[0] + 1, ends[0]

    found: list[tuple[str, int]] = []
    errors: list[str] = []
    current = False
    for index, line in enumerate(lines):
        lineno = index + 1
        inside = first <= index < last
        tagged = _TAGGED.match(line) if inside else None
        if TAG in line and not tagged:
            errors.append(
                f"{label}:{lineno}: a q: tag outside a question line of the section"
            )
        if not inside:
            continue
        if not _ITEM.match(line):
            if current:
                qid, marks = found[-1]
                found[-1] = (qid, marks + line.count("?"))
            continue
        current = False
        if not tagged:
            if TAG not in line:
                errors.append(
                    f"{label}:{lineno}: a question without a {TAG}<id> --> tag"
                )
            continue
        qid, rest = tagged.group(1), tagged.group(2)
        if qid in (seen for seen, _ in found):
            errors.append(f"{label}:{lineno}: q:{qid} is used twice")
            continue
        if russian and not _CYRILLIC.search(rest):
            errors.append(f"{label}:{lineno}: q:{qid} has no Russian text on its line")
        found.append((qid, rest.count("?")))
        current = True
    if not found and not errors:
        errors.append(f"{label}: no questions between {START} and {END}")
    return found, errors


def check(en_text: str, ru_text: str) -> list[str]:
    """Every way the two prompts' questions are out of step; empty when they match."""
    en, errors = questions(en_text, "en")
    ru, ru_errors = questions(ru_text, "ru", russian=True)
    errors += ru_errors
    if errors:
        return errors
    en_ids = [qid for qid, _ in en]
    ru_ids = [qid for qid, _ in ru]
    if en_ids == ru_ids:
        return [
            f"q:{qid} has {en_marks} question marks in en, {ru_marks} in ru"
            for (qid, en_marks), (_, ru_marks) in zip(en, ru)
            if en_marks != ru_marks
        ]
    if len(en_ids) != len(ru_ids):
        errors.append(
            f"question count differs: en has {len(en_ids)}, ru has {len(ru_ids)}"
        )
    for qid in en_ids:
        if qid not in ru_ids:
            errors.append(f"q:{qid} is in en, not in ru")
    for qid in ru_ids:
        if qid not in en_ids:
            errors.append(f"q:{qid} is in ru, not in en")
    if sorted(en_ids) == sorted(ru_ids):
        errors.append(
            f"question order differs: en {' '.join(en_ids)}; ru {' '.join(ru_ids)}"
        )
    return errors


def check_tree(root: Path) -> list[str]:
    """Run the check on the two prompt files under `root`."""
    paths = (root / EN_PROMPT, root / RU_PROMPT)
    missing = [p.relative_to(root).as_posix() for p in paths if not p.is_file()]
    if missing:
        return [f"missing: {name}" for name in missing]
    return check(*(p.read_text(encoding="utf-8") for p in paths))
