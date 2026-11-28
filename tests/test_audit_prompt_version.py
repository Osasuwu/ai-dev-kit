"""The audit prompt's version line must change whenever the prompt changes (issue #380).

Step 2 of the prompt compares the version line of the copy the user pasted with the one in the
kit's latest `prompts/audit.md`, to catch a stale copy. That only works if every change to the
prompt block also changes its version. This test pins the block's hash to its version: change the
block without bumping the version and it fails.

When it fails after an intended change: raise the number on the block's first line by one, then
set EXPECTED below to the new number and the hash the failure message prints.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "prompts" / "audit.md"
VERSION_LINE = re.compile(r"^Prompt version: (\d+)\.$")

EXPECTED = (6, "a7bb946655dea2476a539fa8fe98cc1a169c8a1bba0fb6ade5e89b3219b32ace")


def _block() -> list[str]:
    text = PROMPT.read_text(encoding="utf-8").replace("\r\n", "\n")
    start = text.index("```text\n") + len("```text\n")
    end = text.index("\n```", start)
    return text[start:end].split("\n")


def test_block_opens_with_a_version_line() -> None:
    first = _block()[0]
    assert VERSION_LINE.match(first), (
        f"first line of the prompt block is not a version line: {first!r}"
    )


def test_version_changes_with_the_block() -> None:
    lines = _block()
    match = VERSION_LINE.match(lines[0])
    assert match, "first line of the prompt block is not a version line"
    version = int(match.group(1))
    digest = hashlib.sha256("\n".join(lines[1:]).encode("utf-8")).hexdigest()
    assert (version, digest) == EXPECTED, (
        f"prompts/audit.md: the prompt block is version {version} with hash {digest}, "
        f"but EXPECTED is {EXPECTED}. If you changed the block, raise its version by one "
        f"and set EXPECTED to (<new version>, <the hash above>)."
    )
