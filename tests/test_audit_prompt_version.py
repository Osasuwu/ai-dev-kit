"""The audit prompt's version line must change whenever the prompt changes (issue #380).

Step 2 of the prompt compares the version line of the copy the user pasted with the one in the
kit's latest `prompts/audit.md`, to catch a stale copy. That only works if every change to the
prompt block also raises its version. Two checks hold that:

- against the base branch: when the block differs from the block on `origin/main`, its version
  must be higher than the base's. Editing EXPECTED below cannot get around this one;
- a pin of the block's hash to its version, which also catches a change when no base is at hand.

When the pin fails after an intended change: raise the number on the block's first line by one
(once per pull request), then set EXPECTED below to the new number and the hash the failure
message prints.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "prompts" / "audit.md"
VERSION_LINE = re.compile(r"^Prompt version: (\d+)\.$")
# The ref the block is compared with. Overridable only so the check can be probed locally.
BASE_REF = os.environ.get("AUDIT_PROMPT_BASE", "origin/main")

EXPECTED = (6, "92494fcab0d81ca5fe0d8b65ca3eb8eee39c2850b8d5dcb8cef6b613b3e379d7")


def _block(text: str) -> list[str]:
    text = text.replace("\r\n", "\n")
    start = text.index("```text\n") + len("```text\n")
    end = text.index("\n```", start)
    return text[start:end].split("\n")


def _version(lines: list[str]) -> int | None:
    match = VERSION_LINE.match(lines[0])
    return int(match.group(1)) if match else None


def _digest(lines: list[str]) -> str:
    return hashlib.sha256("\n".join(lines[1:]).encode("utf-8")).hexdigest()


def _head() -> list[str]:
    return _block(PROMPT.read_text(encoding="utf-8"))


def test_block_opens_with_a_version_line() -> None:
    first = _head()[0]
    assert VERSION_LINE.match(first), (
        f"first line of the prompt block is not a version line: {first!r}"
    )


def test_version_rises_when_the_block_changes_from_base() -> None:
    result = subprocess.run(
        ["git", "show", f"{BASE_REF}:prompts/audit.md"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        pytest.skip(f"{BASE_REF} is not available: {result.stderr.strip()}")
    base = _block(result.stdout)
    base_version = _version(base)
    if base_version is None:
        pytest.skip(f"the prompt block on {BASE_REF} has no version line yet")
    head = _head()
    head_version = _version(head)
    assert head_version is not None, (
        "first line of the prompt block is not a version line"
    )
    if _digest(head) != _digest(base):
        assert head_version > base_version, (
            f"prompts/audit.md: the prompt block differs from {BASE_REF}, but its version "
            f"{head_version} is not higher than {BASE_REF}'s {base_version}. Raise it by one."
        )


def test_version_changes_with_the_block() -> None:
    lines = _head()
    version = _version(lines)
    assert version is not None, "first line of the prompt block is not a version line"
    digest = _digest(lines)
    assert (version, digest) == EXPECTED, (
        f"prompts/audit.md: the prompt block is version {version} with hash {digest}, "
        f"but EXPECTED is {EXPECTED}. If you changed the block, raise its version by one "
        f"and set EXPECTED to (<new version>, <the hash above>)."
    )
