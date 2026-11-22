"""Fingerprint of the files that run code in the credentialed session of a rerun (#341).

Usage: python data/pipeline/snapshot.py [--repo <repo root>] [--home <home folder>]

The rerun's agents can write files anywhere, and some files run code in the session that
holds the maintainer's credentials: git hooks and git config (a hook, a filter, an fsmonitor
command), the project's and the user's Claude Code settings (hooks), and the installed
agent definitions (their tool lists). This script hashes those files and prints one line,
`snapshot <sha256>`. The session prints it before step 1 and keeps the line in its own
context, then prints it again before every later script step and before the commit: a
different line stops the run. The data a rerun writes is not part of it.

It hashes files only: a change it does not cover (a file elsewhere that a hashed file does
not name) is not caught. The session compares the line itself; the script never reads a
stored value, which an agent could rewrite.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

PROJECT_FILES = (".claude/settings.json", ".claude/settings.local.json")
USER_FILES = (
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".claude/agents/aie-fetcher.md",
    ".claude/agents/aie-worker.md",
)


def git_path(repo: Path, *args: str) -> Path:
    out = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "rev-parse", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    path = Path(out)
    return path if path.is_absolute() else repo / path


def watched(repo: Path, home: Path) -> list[Path]:
    common = git_path(repo, "--git-common-dir")
    git_dir = git_path(repo, "--git-dir")
    paths = [repo / p for p in PROJECT_FILES] + [home / p for p in USER_FILES]
    paths += [common / "config", git_dir / "config.worktree", common / "hooks"]
    paths.append(git_path(repo, "--git-path", "hooks"))
    return paths


def fingerprint(repo: Path, home: Path) -> str:
    lines = []
    for path in sorted(set(watched(repo, home))):
        files = (
            sorted(p for p in path.rglob("*") if p.is_file())
            if path.is_dir()
            else [path]
        )
        if not files:
            lines.append(f"{path.as_posix()}\tempty")
        for f in files:
            digest = (
                hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else "missing"
            )
            lines.append(f"{f.as_posix()}\t{digest}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--home", type=Path, default=Path.home())
    args = ap.parse_args(argv)
    print(f"snapshot {fingerprint(args.repo, args.home)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
