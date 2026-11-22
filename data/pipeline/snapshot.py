"""Fingerprint of the files that run code in the credentialed session of a rerun (#341).

Usage: python -I -B data/pipeline/snapshot.py [--repo <repo root>] [--home <home folder>]

The rerun's agents can write files anywhere, and some files run code in, or give
instructions to, the session that holds the maintainer's credentials:

- git: the repo's hooks, its config and worktree config, the global config
  (`~/.gitconfig`, `$XDG_CONFIG_HOME/git/config`, `$GIT_CONFIG_GLOBAL`) and every file these
  include. A credential helper, `core.sshCommand`, a `pushInsteadOf`, a signing program or a
  `filter.*.clean` driver there runs at `git add`, commit or push, and the commit step's
  `-c core.hooksPath=<empty>` stops none of them. The effective config is read with
  `git config --list --show-origin` under `--home`, so an include is followed;
- Claude Code: the project's and the user's settings (hooks), `.mcp.json`, the project's and
  the user's agents, rules and rules files (`CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md`).
  A project agent takes precedence over an installed one of the same name.

This script hashes them and prints one line, `snapshot <sha256>`. The session prints it
before step 1 and keeps the line in its own context, then prints it again before every later
script step and before the commit: a different line stops the run. The data a rerun writes
is not part of it. The maintainer's own credential helper is read, not changed, so the push
authenticates as before.

It hashes what it names only: a file elsewhere that none of these names is not caught. The
session compares the line itself; the script never reads a stored value, which an agent
could rewrite.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

PROJECT_PATHS = (
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".claude/agents",
    ".claude/rules",
    ".mcp.json",
    "CLAUDE.md",
    "CLAUDE.local.md",
    "AGENTS.md",
)
USER_PATHS = (
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".claude/agents",
    ".claude/rules",
    ".claude/CLAUDE.md",
)


def git_env(home: Path, environ: Mapping[str, str]) -> dict[str, str]:
    return {**environ, "HOME": str(home)}


def git(repo: Path, home: Path, environ: Mapping[str, str], *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "core.fsmonitor=false", *args],
        cwd=repo,
        env=git_env(home, environ),
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def git_path(repo: Path, home: Path, environ: Mapping[str, str], *args: str) -> Path:
    path = Path(git(repo, home, environ, "rev-parse", *args).strip())
    return path if path.is_absolute() else repo / path


def watched(repo: Path, home: Path, environ: Mapping[str, str]) -> list[Path]:
    # Git config files are not listed here: `config_listing` covers every one git reads.
    common = git_path(repo, home, environ, "--git-common-dir")
    paths = [repo / p for p in PROJECT_PATHS] + [home / p for p in USER_PATHS]
    paths.append(common / "hooks")
    paths.append(git_path(repo, home, environ, "--git-path", "hooks"))
    return paths


def config_listing(repo: Path, home: Path, environ: Mapping[str, str]) -> str:
    """Every config value git uses in this repo, with the file it came from: the system,
    global (`~/.gitconfig`, `$XDG_CONFIG_HOME/git/config`, `$GIT_CONFIG_GLOBAL`), repo and
    worktree config, and every file they include."""
    return git(repo, home, environ, "config", "--list", "--show-origin")


def fingerprint(
    repo: Path, home: Path, environ: Mapping[str, str] | None = None
) -> str:
    environ = os.environ if environ is None else environ
    lines = []
    for path in sorted(set(watched(repo, home, environ))):
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
    lines.append(config_listing(repo, home, environ))
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
