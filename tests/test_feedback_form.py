"""The feedback form and the README sentence about it ask what the prompts report (#355).

The audit prompt reports a verdict per card (holds / does not hold / cannot tell); the interview
prompt reports in place / gap / later. The form must ask for those, and for the practice the
reader missed, and must not ask about failure classes. The README sentence must name the same
fields. A reader who follows the prompts has no class list to give.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
FORM = REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "base-not-enough.yml"
README = REPO_ROOT / "README.md"

REPORTED = "which cards the agent reported"
MISSED = "which practice you missed"
VERDICTS = ("holds", "does not hold", "cannot tell", "in place", "gap", "later")


def _labels() -> list[str]:
    return re.findall(r"^\s+label:\s*(.+?)\s*$", FORM.read_text(encoding="utf-8"), re.M)


def _form_sentence() -> str:
    """The README sentence that says what the form asks."""
    text = README.read_text(encoding="utf-8")
    para = next(p for p in text.split("\n\n") if "template=base-not-enough.yml" in p)
    return next(
        s for s in re.split(r"(?<=\.)\s+", para) if s.startswith("The form asks")
    )


def test_form_labels_are_the_two_fields_the_prompts_can_answer() -> None:
    assert [label.lower() for label in _labels()] == [REPORTED, MISSED]


def test_form_asks_for_every_verdict_the_prompts_report() -> None:
    text = FORM.read_text(encoding="utf-8").lower()
    for verdict in VERDICTS:
        assert verdict in text, verdict


def test_form_does_not_ask_about_classes() -> None:
    assert "class" not in FORM.read_text(encoding="utf-8").lower()


def test_readme_sentence_names_the_same_fields_and_verdicts() -> None:
    sentence = _form_sentence().lower()
    assert REPORTED in sentence
    assert MISSED in sentence
    for verdict in VERDICTS:
        assert verdict in sentence, verdict
    assert "class" not in sentence
