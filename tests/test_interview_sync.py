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


def test_second_questions_section_fails():
    ru = (
        RU
        + "\n<!-- questions:start -->\n1. <!-- q:extra --> Ещё вопрос?\n<!-- questions:end -->\n"
    )
    assert check(EN, ru) == [
        "ru: needs exactly one <!-- questions:start --> line followed by one <!-- questions:end --> line",
    ]


def test_question_tag_after_the_section_fails():
    ru = RU + "\n10. <!-- q:extra --> Ещё вопрос?\n"
    assert check(EN, ru) == ["ru:13: a q: tag outside a question line of the section"]


def test_question_tag_on_a_bullet_inside_the_section_fails():
    en = EN.replace(
        "   A follow-up line under the question, not a question.",
        "- <!-- q:extra --> A bulleted question?",
    )
    assert check(en, RU) == ["en:7: a q: tag outside a question line of the section"]


def test_sub_question_added_in_one_language_fails():
    en = EN.replace(
        "   A follow-up line under the question, not a question.",
        "   And which version of it?",
    )
    assert check(en, RU) == ["q:agent has 2 question marks in en, 1 in ru"]


def test_extra_question_on_the_tag_line_in_one_language_fails():
    ru = RU.replace("Что вы проверили?", "Что вы проверили? И как?")
    assert check(EN, ru) == ["q:done has 1 question marks in en, 2 in ru"]


def test_untagged_question_after_the_section_fails():
    ru = RU + "\n10. Сколько человек в команде?\n"
    assert check(EN, ru) == ["ru:13: a question mark outside a question of the section"]


def test_untagged_question_in_another_form_inside_the_section_fails():
    ru = RU.replace(
        "<!-- questions:end -->", "10) Расскажите о команде?\n<!-- questions:end -->"
    )
    assert check(EN, ru) == ["q:merge has 1 question marks in en, 2 in ru"]
    ru = RU.replace(
        "1. <!-- q:agent -->",
        "Сначала вопрос без номера?\n1. <!-- q:agent -->",
    )
    assert check(EN, ru) == ["ru:6: a question mark outside a question of the section"]


def test_tag_without_spaces_after_the_section_fails():
    ru = RU + "\n10. <!--q:team--> Кто в команде\n"
    assert check(EN, ru) == ["ru:13: a q: tag outside a question line of the section"]


def test_malformed_tag_on_a_question_line_fails():
    en = EN.replace("<!-- q:agent -->", "<!-- q:Agent -->")
    assert check(en, RU) == ["en:6: a malformed q: tag on a question line"]


def test_question_mark_in_a_link_is_not_a_question():
    en = EN.replace("Intro.", "See [a talk](https://example.com/watch?v=1&t=2).")
    assert check(en, RU) == []


def test_missing_prompt_file_fails(tmp_path):
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "interview.en.md").write_text(EN, encoding="utf-8")
    assert check_tree(tmp_path) == ["missing: prompts/interview.ru.md"]


def test_missing_english_prompt_file_fails(tmp_path):
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "interview.ru.md").write_text(RU, encoding="utf-8")
    assert check_tree(tmp_path) == ["missing: prompts/interview.en.md"]
