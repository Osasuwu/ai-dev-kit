"""Commit guard for the credentialed step of a rerun (#341).

Usage: python data/pipeline/commit_guard.py   (from the repo root, after `git add`)

Reads the staged paths (`git diff --cached --name-only --no-renames`, so a rename shows both
its old and its new path) and exits 1 when any of them is outside what a rerun produces:
`cards/`, `data/` except `data/pipeline/`, and `CHANGELOG.md`. The sources list is
`data/sources.md`, inside `data/`. `.github/`, the pipeline's own code and instructions,
tests, scripts and every other path are refused, as is a path with a `..` segment or a
leading `/`. Nothing staged also exits 1.

This is a check the step runs before it commits, not a permission: an agent that skips it
is stopped only by the human who reviews the pull request.
"""

from __future__ import annotations

import subprocess
import sys

ALLOWED_PREFIXES = ("cards/", "data/")
REFUSED_PREFIXES = ("data/pipeline/",)
ALLOWED_FILES = ("CHANGELOG.md",)


def allowed(path: str) -> bool:
    if path.startswith("/") or ".." in path.split("/"):
        return False
    if path.startswith(REFUSED_PREFIXES):
        return False
    return path in ALLOWED_FILES or path.startswith(ALLOWED_PREFIXES)


def refused(paths: list[str]) -> list[str]:
    return [p for p in paths if not allowed(p)]


def staged() -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--no-renames", "-z"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    return [p for p in out.split("\0") if p]


def main() -> int:
    paths = staged()
    if not paths:
        print("commit guard: nothing staged", file=sys.stderr)
        return 1
    bad = refused(paths)
    for p in bad:
        print(f"commit guard: refused: {p}", file=sys.stderr)
    if bad:
        print(
            f"commit guard: {len(bad)} of {len(paths)} staged path(s) are outside"
            " cards/, data/ (not data/pipeline/) and CHANGELOG.md; unstage them",
            file=sys.stderr,
        )
        return 1
    print(f"commit guard: ok, {len(paths)} staged path(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
