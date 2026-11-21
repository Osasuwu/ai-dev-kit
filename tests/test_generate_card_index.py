"""Behaviour checks for scripts/generate_card_index.py, the card index and watch-list (#340).

The expected files are written out by hand from the cards in the committed
`structure_gate/valid` tree, so they do not come from the generator's own steps.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from generate_card_index import main, render_index, render_watch_list  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent
VALID = Path(__file__).parent / "fixtures" / "structure_gate" / "valid"

FORMAT = "cards/README.md"
CONFIG_CARD = "cards/require-checks.md"
HOLD_PATHS = ".github/hold-paths.json"

INDEX = """\
# Card index

Generated from `cards/` by `python scripts/generate_card_index.py`; do not edit. One line per card: kind, card, why it matters, when it applies, the failure classes it guards against. Format and line limit: [cards/README.md](cards/README.md).

- config · [Require the checks you merge on](cards/require-checks.md) · A check that is not required can fail and the merge still goes through. · when changes merge through a branch rule · guards [alpha](docs/classes/alpha.md) (class evidence is one operator's practice)
- habit · [Run the app before calling it done](cards/run-the-app.md) · A green build does not show that the feature works. · when an agent changes code that a person uses · guards [alpha](docs/classes/alpha.md), [irreversible-effects](docs/classes/cross.md) (class evidence is one operator's practice)
- belief · [Pass rate does not see erosion](cards/tests-miss-erosion.md) · Passing tests say nothing about whether the code stays easy to change. · when you judge agent work by its pass rate
"""

WATCH_LIST = """\
# Watch list

Generated from the `Learn` sections in `cards/` by `python scripts/generate_card_index.py`; do not edit. The talks and pages each card learns from, with what to look for in each.

## [Require the checks you merge on](cards/require-checks.md)

- [Protected branches](https://example.com/protected-branches): what a required check blocks.

## [Run the app before calling it done](cards/run-the-app.md)

- [A talk on feedback, 2:12](https://example.com/talk?t=132): why the agent needs to see the result.
- [A second talk, 20:51](https://example.com/other?t=1251): proof that goes stale.

## [Pass rate does not see erosion](cards/tests-miss-erosion.md)

- [A talk on reward](https://example.com/reward?t=723): why the reward cannot see design.
"""


def _tree(tmp_path: Path) -> Path:
    root = tmp_path / "tree"
    shutil.copytree(VALID, root)
    return root


def _edit(root: Path, rel: str, old: str, new: str) -> None:
    path = root / rel
    text = path.read_bytes().decode("utf-8")
    assert old in text, f"fixture text not found in {rel}: {old!r}"
    path.write_bytes(text.replace(old, new).encode("utf-8"))


def test_the_index_has_one_line_per_card_in_the_format_s_kind_order(tmp_path):
    assert render_index(_tree(tmp_path)) == INDEX


def test_the_watch_list_has_every_card_s_learn_links_grouped_by_card(tmp_path):
    assert render_watch_list(_tree(tmp_path)) == WATCH_LIST


def test_every_index_line_that_names_classes_carries_the_caveat(tmp_path):
    lines = [
        x for x in render_index(_tree(tmp_path)).splitlines() if x.startswith("- ")
    ]
    with_guards = [x for x in lines if " · guards " in x]
    assert len(with_guards) == 2
    assert all(
        x.endswith("(class evidence is one operator's practice)") for x in with_guards
    )
    assert "one operator" not in lines[2]


def test_cards_of_one_kind_are_ordered_by_path(tmp_path):
    root = _tree(tmp_path)
    text = (root / CONFIG_CARD).read_bytes().decode("utf-8")
    first = text.replace("# Require the checks you merge on", "# An earlier card")
    (root / "cards/a-first.md").write_bytes(first.encode("utf-8"))
    titles = [
        x.split("](")[0].split("[", 1)[1]
        for x in render_index(root).splitlines()
        if x.startswith("- ")
    ]
    assert titles == [
        "An earlier card",
        "Require the checks you merge on",
        "Run the app before calling it done",
        "Pass rate does not see erosion",
    ]


def test_a_card_relative_learn_link_is_rewritten_from_the_root(tmp_path):
    root = _tree(tmp_path)
    _edit(
        root,
        CONFIG_CARD,
        "(https://example.com/protected-branches)",
        "(../docs/classes/alpha.md#protections)",
    )
    assert (
        "- [Protected branches](docs/classes/alpha.md#protections): what a required check blocks.\n"
        in render_watch_list(root)
    )


def test_an_index_over_the_line_limit_is_refused(tmp_path):
    root = _tree(tmp_path)
    _edit(root, FORMAT, "- **Index line limit:** 12", "- **Index line limit:** 6")
    with pytest.raises(
        ValueError, match=r"INDEX\.md would have 7 lines; the limit is 6"
    ):
        render_index(root)


def test_an_index_at_the_line_limit_is_written(tmp_path):
    root = _tree(tmp_path)
    _edit(root, FORMAT, "- **Index line limit:** 12", "- **Index line limit:** 7")
    assert render_index(root) == INDEX


def test_cards_are_selected_through_the_hold_path_definition(tmp_path):
    root = _tree(tmp_path)
    _edit(root, HOLD_PATHS, '"cards/"', '"elsewhere/"')
    assert [x for x in render_index(root).splitlines() if x.startswith("- ")] == []


def test_a_format_file_the_generator_cannot_read_is_refused(tmp_path):
    root = _tree(tmp_path)
    (root / FORMAT).unlink()
    with pytest.raises(ValueError, match=r"cards/README\.md"):
        render_index(root)


def test_main_writes_both_files_and_check_then_passes(tmp_path):
    root = _tree(tmp_path)
    assert main(["--root", str(root)]) == 0
    assert (root / "INDEX.md").read_bytes().decode("utf-8") == INDEX
    assert (root / "WATCH-LIST.md").read_bytes().decode("utf-8") == WATCH_LIST
    assert main(["--check", "--root", str(root)]) == 0


@pytest.mark.parametrize("stale", ["INDEX.md", "WATCH-LIST.md"])
def test_check_fails_on_a_stale_file_and_leaves_it(tmp_path, capsys, stale):
    root = _tree(tmp_path)
    assert main(["--root", str(root)]) == 0
    (root / stale).write_bytes(b"old\n")
    capsys.readouterr()
    assert main(["--check", "--root", str(root)]) == 1
    assert capsys.readouterr().out == (
        f"{stale} is out of date; run: python scripts/generate_card_index.py\n"
    )
    assert (root / stale).read_bytes() == b"old\n"


def test_check_fails_when_a_file_is_missing(tmp_path, capsys):
    root = _tree(tmp_path)
    assert main(["--check", "--root", str(root)]) == 1
    assert capsys.readouterr().out == (
        "INDEX.md is out of date; run: python scripts/generate_card_index.py\n"
        "WATCH-LIST.md is out of date; run: python scripts/generate_card_index.py\n"
    )


def test_the_command_line_reports_a_refusal_and_writes_nothing(tmp_path, capsys):
    root = _tree(tmp_path)
    _edit(root, FORMAT, "- **Index line limit:** 12", "- **Index line limit:** 6")
    assert main(["--root", str(root)]) == 2
    assert capsys.readouterr().out == (
        "generate_card_index: INDEX.md would have 7 lines; the limit is 6 "
        "(cards/README.md). Merge or retire cards first.\n"
    )
    assert not (root / "INDEX.md").exists()
    assert not (root / "WATCH-LIST.md").exists()


def test_the_repository_index_and_watch_list_are_up_to_date():
    assert main(["--check", "--root", str(REPO_ROOT)]) == 0
