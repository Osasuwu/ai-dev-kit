"""Behaviour checks for the interview prompt sync check (#344, #336 item 1).

The shipped-files test runs the check on `prompts/interview.en.md` and
`prompts/interview.ru.md`; the rest feed it small prompts written out here, each out of step
in one way, and assert the exact error.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from interview_sync import check, check_tree  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent


def _prompt(*items: str) -> str:
    body = "\n".join(items)
    return f"# Prompt\n\nIntro.\n\n<!-- questions:start -->\n{body}\n<!-- questions:end -->\n\nOutro.\n"


EN = _prompt(
    "1. <!-- q:agent --> What do you use?",
    "   A follow-up line under the question, not a question.",
    "2. <!-- q:done --> What did you check?",
    "3. <!-- q:merge --> How does a change get in?",
)
RU = _prompt(
    "1. <!-- q:agent --> Чем вы пользуетесь?",
    "2. <!-- q:done --> Что вы проверили?",
    "3. <!-- q:merge --> Как изменение попадает в код?",
)


def test_shipped_prompts_ask_the_same_questions_in_the_same_order():
    assert check_tree(REPO_ROOT) == []


def test_prompts_in_step_pass():
    assert check(EN, RU) == []


def test_swapped_order_fails():
    ru = _prompt(
        "1. <!-- q:agent --> Чем вы пользуетесь?",
        "2. <!-- q:merge --> Как изменение попадает в код?",
        "3. <!-- q:done --> Что вы проверили?",
    )
    assert check(EN, ru) == [
        "question order differs: en agent done merge; ru agent merge done",
    ]


def test_question_missing_from_one_language_fails():
    ru = _prompt(
        "1. <!-- q:agent --> Чем вы пользуетесь?",
        "2. <!-- q:done --> Что вы проверили?",
    )
    assert check(EN, ru) == [
        "question count differs: en has 3, ru has 2",
        "q:merge is in en, not in ru",
    ]


def test_question_renamed_in_one_language_fails():
    ru = RU.replace("q:done", "q:review")
    assert check(EN, ru) == [
        "q:done is in en, not in ru",
        "q:review is in ru, not in en",
    ]


def test_untagged_question_fails():
    en = EN.replace("3. <!-- q:merge --> How", "3. How")
    assert check(en, RU) == ["en:9: a question without a <!-- q:<id> --> tag"]


def test_english_question_left_in_the_russian_prompt_fails():
    ru = RU.replace("Как изменение попадает в код?", "How does a change get in?")
    assert check(EN, ru) == ["ru:8: q:merge has no Russian text on its line"]


def test_id_used_twice_fails():
    en = EN.replace("q:merge", "q:done")
    assert check(en, RU) == ["en:9: q:done is used twice"]


def test_empty_questions_section_fails():
    assert check(_prompt(), _prompt()) == [
        "en: no questions between <!-- questions:start --> and <!-- questions:end -->",
        "ru: no questions between <!-- questions:start --> and <!-- questions:end -->",
    ]


def test_missing_section_markers_fail():
    en = EN.replace("<!-- questions:end -->\n", "")
    assert check(en, RU) == [
        "en: needs exactly one <!-- questions:start --> line followed by one <!-- questions:end --> line",
    ]


def test_missing_prompt_file_fails(tmp_path):
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "interview.en.md").write_text(EN, encoding="utf-8")
    assert check_tree(tmp_path) == ["missing: prompts/interview.ru.md"]
