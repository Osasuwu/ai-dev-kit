"""Commit guard for the credentialed step of a rerun (#341).

Usage: python data/pipeline/commit_guard.py   (from the repo root, after `git add`)

Reads the staged changes (`git diff --cached --name-status --no-renames`, so a rename shows
as the deletion of its old path and the addition of its new one) and exits 1 when any path is
outside what a rerun produces: `cards/`, `data/` except `data/pipeline/`, and `CHANGELOG.md`.
The sources list is `data/sources.md`, inside `data/`. `.github/`, the pipeline's own code and
instructions, tests, scripts and every other path are refused, as is a path with a segment
that starts with a dot (`..`, `data/.gitattributes`) or a leading `/`. Paths are compared
case-folded, because on a case-insensitive checkout `data/Pipeline/` is `data/pipeline/`. A
staged deletion is refused anywhere: a rerun only adds and changes files, and claims are
never deleted (`data/sources.md`). Nothing staged also exits 1.

This is a check the step runs before it commits, not a permission: an agent that skips it
is stopped only by the human who reviews the pull request.
"""

from __future__ import annotations

import subprocess
import sys

ALLOWED_PREFIXES = ("cards/", "data/")
REFUSED_PREFIXES = ("data/pipeline/",)
ALLOWED_FILES = ("CHANGELOG.md",)
ALLOWED_FILES_FOLDED = tuple(f.casefold() for f in ALLOWED_FILES)


def allowed(path: str) -> bool:
    folded = path.casefold()
    # A segment starting with a dot covers `..` and dot files such as `data/.gitattributes`,
    # which can name a filter that runs a command on the next `git add`.
    if folded.startswith("/") or any(s.startswith(".") for s in folded.split("/")):
        return False
    if folded.startswith(REFUSED_PREFIXES):
        return False
    return folded in ALLOWED_FILES_FOLDED or folded.startswith(ALLOWED_PREFIXES)


def refused(paths: list[str]) -> list[str]:
    return [p for p in paths if not allowed(p)]


def staged() -> list[tuple[str, str]]:
    """Return (status letter, path) for each staged change."""
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-status", "--no-renames", "-z"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    fields = out.split("\0")
    return [(fields[i][:1], fields[i + 1]) for i in range(0, len(fields) - 1, 2)]


def main() -> int:
    changes = staged()
    paths = [p for _, p in changes]
    if not paths:
        print("commit guard: nothing staged", file=sys.stderr)
        return 1
    bad = [(p, "deleted") for s, p in changes if s == "D"]
    bad += [(p, "outside") for p in refused(paths) if (p, "deleted") not in bad]
    for p, why in bad:
        print(f"commit guard: refused: {p} ({why})", file=sys.stderr)
    if bad:
        print(
            f"commit guard: {len(bad)} of {len(paths)} staged path(s) refused: a rerun"
            " only adds or changes files under cards/, data/ (not data/pipeline/) and"
            " CHANGELOG.md; unstage them",
            file=sys.stderr,
        )
        return 1
    print(f"commit guard: ok, {len(paths)} staged path(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
