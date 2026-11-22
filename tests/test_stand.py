"""Tests for the seeded stand (`stand/`, issue #345).

The stand is the fixture a maintainer scores the audit and interview paths on. These tests
cover what the stand's own tool promises: setup puts the seeds only in a throwaway folder,
never in the real home; reset and check refuse folders that are not a stand; check reports
every departure from the seeded state and reads a restored stand as seeded; the canary scan
tells agent output from tool output. The data tests keep the manifest, the score file, the
interview answers and the seeds in step with each other and with the config cards.

Every test runs against a fake real home under tmp_path (HOME and USERPROFILE point there),
so nothing here reads or writes the developer's own config.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
STAND_DIR = ROOT / "stand"
SEED_DIR = STAND_DIR / "seed"
CARDS_DIR = ROOT / "cards"


def _load_stand():
    spec = importlib.util.spec_from_file_location("stand_tool", STAND_DIR / "stand.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look the module up there
    spec.loader.exec_module(module)
    return module


stand = _load_stand()

GIT_ENV_DROP = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")


def git(repo: Path, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if k not in GIT_ENV_DROP}
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return result.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def real_home(tmp_path, monkeypatch):
    """A fake real home with user-level agent config in it, set as HOME and USERPROFILE."""
    home = tmp_path / "realhome"
    (home / ".claude").mkdir(parents=True)
    (home / ".codex").mkdir()
    (home / ".claude" / "settings.json").write_text('{"permissions": {"allow": []}}\n')
    (home / ".claude" / "CLAUDE.md").write_text("# real user rules\n")
    (home / ".codex" / "config.toml").write_text('approval_policy = "on-request"\n')
    (home / ".gitconfig").write_text("[user]\n\tname = Real Person\n")
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    for name in ("CLAUDE_CONFIG_DIR", "CODEX_HOME", "AI_DEV_KIT_STAND"):
        monkeypatch.delenv(name, raising=False)
    return home


def snapshot(folder: Path) -> dict[str, str]:
    return {
        p.relative_to(folder).as_posix(): sha256(p)
        for p in sorted(folder.rglob("*"))
        if p.is_file()
    }


def seed_target(seed: Path) -> str:
    """Where a seed file lands, relative to the stand home or repo, worked out by hand rules:
    drop the .seed suffix, and a path part starting with dot- starts with a dot instead."""
    parts = list(seed.parts)
    parts[-1] = parts[-1][: -len(".seed")]
    return "/".join(
        "." + p[len("dot-") :] if p.startswith("dot-") else p for p in parts
    )


# --- setup ------------------------------------------------------------------------------


@pytest.mark.parametrize("harness", ["claude-code", "codex"])
def test_setup_puts_seeds_in_the_stand_and_nothing_in_the_real_home(
    tmp_path, real_home, harness
):
    before = snapshot(real_home)
    target = tmp_path / "stand"

    stand.setup(target, harness)

    home, repo = target / "home", target.resolve() / "repo"
    # Every seed of this harness and of the repo lands byte for byte, the template filled in.
    harness_seeds = sorted((SEED_DIR / harness).rglob("*.seed"))
    repo_seeds = sorted((SEED_DIR / "repo").rglob("*.seed"))
    assert harness_seeds and repo_seeds
    for seed in harness_seeds:
        landed = home / seed_target(seed.relative_to(SEED_DIR / harness))
        expected = seed.read_text(encoding="utf-8").replace("{{STAND_REPO}}", str(repo))
        assert landed.read_text(encoding="utf-8") == expected, landed
    for seed in repo_seeds:
        landed = repo / seed_target(seed.relative_to(SEED_DIR / "repo"))
        assert landed.read_bytes() == seed.read_bytes(), landed
    # Spot checks of the mapping, as literals.
    assert (repo / ".github" / "workflows" / "ci.yml").is_file()
    assert (repo / ".gitignore").is_file()
    assert (repo / ".env").read_text() == "STAND_DB_HOST=CANARY-CANARY-ENV\n"
    other = {"claude-code": ".codex", "codex": ".claude"}[harness]
    assert not (home / other).exists()
    if harness == "codex":
        toml = (home / ".codex" / "config.toml").read_text(encoding="utf-8")
        assert f"[projects.'{repo}']" in toml
        assert "{{" not in toml
    # One seed commit on main; .env is ignored and untracked; the identity is the stand's own.
    assert git(repo, "branch", "--show-current") == "main"
    assert git(repo, "rev-list", "--count", "main") == "1"
    assert git(repo, "branch", "--list", "--format=%(refname:short)") == "main"
    assert git(repo, "status", "--porcelain", "--ignored") == "!! .env"
    assert git(repo, "config", "user.email") == "stand@example.invalid"
    assert git(repo, "log", "-1", "--format=%ae") == "stand@example.invalid"
    # The real home is untouched.
    assert snapshot(real_home) == before


REFUSALS = [
    ("real-home", lambda tmp, home: home, "real home"),
    ("ancestor-of-real-home", lambda tmp, home: tmp, "real home"),
    (
        "inside-real-claude",
        lambda tmp, home: home / ".claude" / "stand",
        "real agent config",
    ),
    (
        "inside-real-codex",
        lambda tmp, home: home / ".codex" / "stand",
        "real agent config",
    ),
    (
        "inside-kit-checkout",
        lambda tmp, home: tmp / "kit" / "stand" / "x",
        "kit checkout",
    ),
]


@pytest.mark.parametrize(
    "make_target,reason", [r[1:] for r in REFUSALS], ids=[r[0] for r in REFUSALS]
)
def test_setup_refuses_a_folder_that_is_not_throwaway(
    tmp_path, real_home, monkeypatch, make_target, reason
):
    # A stand-in kit checkout under tmp: were the guard broken, setup would fill tmp, not
    # this repo.
    monkeypatch.setattr(stand, "KIT_ROOT", tmp_path / "kit")
    target = make_target(tmp_path, real_home)
    before_home = snapshot(real_home)
    existed = target.exists()

    with pytest.raises(stand.StandError, match=reason):
        stand.setup(target, "claude-code")

    assert snapshot(real_home) == before_home
    assert target.exists() == existed


def test_setup_refuses_a_non_empty_folder_without_the_marker(tmp_path, real_home):
    target = tmp_path / "work"
    target.mkdir()
    (target / "notes.txt").write_text("mine\n")

    with pytest.raises(stand.StandError, match="not empty and not a stand"):
        stand.setup(target, "claude-code")

    assert sorted(p.name for p in target.iterdir()) == ["notes.txt"]


def test_setup_refuses_when_run_from_a_stand_shell(tmp_path, real_home, monkeypatch):
    monkeypatch.setenv("AI_DEV_KIT_STAND", str(tmp_path / "other"))

    with pytest.raises(stand.StandError, match="stand shell"):
        stand.setup(tmp_path / "stand", "claude-code")

    assert not (tmp_path / "stand").exists()


# --- reset ------------------------------------------------------------------------------


def test_reset_refuses_a_folder_without_the_marker(tmp_path, real_home):
    target = tmp_path / "work"
    target.mkdir()
    (target / "notes.txt").write_text("mine\n")

    with pytest.raises(stand.StandError, match="no stand marker"):
        stand.reset(target)

    assert (target / "notes.txt").read_text() == "mine\n"


def test_reset_returns_a_changed_stand_to_its_seeds(tmp_path, real_home):
    target = tmp_path / "stand"
    stand.setup(target, "codex")
    repo = target / "repo"
    (target / "home" / ".codex" / "config.toml").write_text(
        'approval_policy = "on-request"\n'
    )
    git(repo, "switch", "-c", "ai-dev-kit/audit-2026-11-22")
    (repo / "AGENTS.md").write_text("changed\n")
    (target / "home" / ".codex" / "auth.json").write_text("{}\n")

    stand.reset(target)

    report = stand.check(target)
    assert report.reasons == []
    assert report.seeded is True
    assert not (target / "home" / ".codex" / "auth.json").exists()
    assert json.loads((target / stand.MARKER).read_text())["harness"] == "codex"


# --- check ------------------------------------------------------------------------------


def test_check_reads_a_fresh_stand_as_seeded(tmp_path, real_home):
    target = tmp_path / "stand"
    stand.setup(target, "claude-code")

    report = stand.check(target)

    assert report.reasons == []
    assert report.seeded is True
    assert report.lines[-1] == "SEEDED STATE: yes"


def _change_user_settings(target, repo, home):
    (home / ".claude" / "settings.json").write_text("{}\n")


def _remove_user_rules(target, repo, home):
    (home / ".claude" / "CLAUDE.md").unlink()


def _add_user_agent_file(target, repo, home):
    (home / ".claude" / "agents").mkdir()
    (home / ".claude" / "agents" / "helper.md").write_text("x\n")


def _add_audit_branch(target, repo, home):
    git(repo, "switch", "-c", "ai-dev-kit/audit-2026-11-22")
    (repo / "pyproject.toml").write_text(
        "[tool.pytest.ini_options]\nxfail_strict = true\n"
    )
    git(repo, "commit", "-qam", "audit")
    git(repo, "switch", "main")


def _stay_on_audit_branch(target, repo, home):
    git(repo, "switch", "-c", "ai-dev-kit/audit-2026-11-22")


def _edit_tracked_file(target, repo, home):
    (repo / "AGENTS.md").write_text("changed\n")


def _commit_on_main(target, repo, home):
    (repo / "AGENTS.md").write_text("changed\n")
    git(repo, "commit", "-qam", "on main")


def _add_untracked_file(target, repo, home):
    (repo / "notes.txt").write_text("x\n")


def _add_ignored_agent_config(target, repo, home):
    (repo / ".claude" / "settings.local.json").write_text("{}\n")


def _add_untracked_agent_config(target, repo, home):
    (repo / "AGENTS.override.md").write_text("x\n")


def _edit_env_file(target, repo, home):
    (repo / ".env").write_text("STAND_DB_HOST=elsewhere\n")


def _remove_env_file(target, repo, home):
    (repo / ".env").unlink()


def _leave_a_stash(target, repo, home):
    (repo / "AGENTS.md").write_text("changed\n")
    git(repo, "stash", "push", "-q", "-m", "audit")


def _change_real_config(target, repo, home):
    real = Path(os.environ["HOME"])
    (real / ".claude" / "settings.json").write_text(
        '{"permissions": {"allow": ["Bash(*)"]}}\n'
    )


DEPARTURES = [
    (_change_user_settings, ["user file changed: .claude/settings.json"]),
    (_remove_user_rules, ["user file missing: .claude/CLAUDE.md"]),
    (
        _add_user_agent_file,
        ["agent config file added at user level: .claude/agents/helper.md"],
    ),
    (_add_audit_branch, ["branch exists: ai-dev-kit/audit-2026-11-22"]),
    (
        _stay_on_audit_branch,
        [
            "repo on ai-dev-kit/audit-2026-11-22, not main",
            "branch exists: ai-dev-kit/audit-2026-11-22",
        ],
    ),
    (_edit_tracked_file, ["repo file changed: AGENTS.md"]),
    (_commit_on_main, ["main moved from the seed commit"]),
    (_add_untracked_file, ["untracked file in repo: notes.txt"]),
    (
        _add_ignored_agent_config,
        ["agent config file added in repo: .claude/settings.local.json"],
    ),
    (
        _add_untracked_agent_config,
        ["agent config file added in repo: AGENTS.override.md"],
    ),
    (_edit_env_file, ["repo file changed: .env"]),
    (_remove_env_file, ["repo file missing: .env"]),
    (_leave_a_stash, ["stash exists in repo"]),
    (_change_real_config, ["real user-level config changed: .claude/settings.json"]),
]


@pytest.mark.parametrize(
    "depart,reasons", DEPARTURES, ids=[d[0].__name__.lstrip("_") for d in DEPARTURES]
)
def test_check_names_each_departure_from_the_seeded_state(
    tmp_path, real_home, depart, reasons
):
    target = tmp_path / "stand"
    stand.setup(target, "claude-code")

    depart(target, target / "repo", target / "home")
    report = stand.check(target)

    assert report.reasons == reasons
    assert report.seeded is False
    assert report.lines[-1] == f"SEEDED STATE: no ({'; '.join(reasons)})"


def test_check_ignores_harness_runtime_files_and_the_audit_backup(tmp_path, real_home):
    target = tmp_path / "stand"
    stand.setup(target, "claude-code")
    home, repo = target / "home", target / "repo"
    (home / ".claude" / "projects" / "p").mkdir(parents=True)
    (home / ".claude" / "projects" / "p" / "s.jsonl").write_text("{}\n")
    (home / ".claude" / ".claude.json").write_text("{}\n")
    backup = home / "ai-dev-kit-backup" / "2026-11-22-1200"
    backup.mkdir(parents=True)
    (backup / "RESTORE.txt").write_text("git switch main\n")
    (repo / ".pytest_cache").mkdir()
    (repo / ".pytest_cache" / "README.md").write_text("x\n")

    report = stand.check(target)

    assert report.reasons == []
    assert report.seeded is True


def test_restoring_after_a_simulated_audit_returns_the_seeded_state(
    tmp_path, real_home
):
    """The shape of the audit prompt's undo: a user file copied back from the backup, the repo
    switched back to the branch it was on, the audit branch deleted with git branch -D."""
    target = tmp_path / "stand"
    stand.setup(target, "claude-code")
    home, repo = target / "home", target / "repo"
    settings = home / ".claude" / "settings.json"
    backup = home / "ai-dev-kit-backup" / "2026-11-22-1200"
    (backup / "before-1").mkdir(parents=True)
    shutil.copy2(settings, backup / "settings.json")
    settings.write_text(settings.read_text().replace('"Bash(npx:*)",\n      ', ""))
    git(repo, "switch", "-c", "ai-dev-kit/audit-2026-11-22")
    (repo / "pyproject.toml").write_text(
        "[tool.pytest.ini_options]\nxfail_strict = true\n"
    )
    git(repo, "commit", "-qam", "audit: strict xfail")
    git(repo, "switch", "main")
    assert stand.check(target).seeded is False

    shutil.copy2(backup / "settings.json", settings)
    git(repo, "switch", "main")
    git(repo, "branch", "-D", "ai-dev-kit/audit-2026-11-22")
    report = stand.check(target)

    assert report.reasons == []
    assert report.seeded is True


def test_main_check_exit_code_follows_the_verdict(tmp_path, real_home, capsys):
    target = tmp_path / "stand"
    assert stand.main(["setup", "--harness", "claude-code", "--dir", str(target)]) == 0
    assert stand.main(["check", "--dir", str(target)]) == 0
    assert capsys.readouterr().out.rstrip().endswith("SEEDED STATE: yes")

    (target / "repo" / "AGENTS.md").write_text("changed\n")

    assert stand.main(["check", "--dir", str(target)]) == 1
    assert stand.main(["reset", "--dir", str(tmp_path / "missing")]) == 2


# --- env scripts -----------------------------------------------------------------------


ENV_PROBE = (
    "HOME",
    "USERPROFILE",
    "CLAUDE_CONFIG_DIR",
    "CODEX_HOME",
    "GIT_CONFIG_GLOBAL",
    "GH_CONFIG_DIR",
)


def _expected_env(target: Path) -> dict[str, Path]:
    home = target / "home"
    return {
        "HOME": home,
        "USERPROFILE": home,
        "CLAUDE_CONFIG_DIR": home / ".claude",
        "CODEX_HOME": home / ".codex",
        "GIT_CONFIG_GLOBAL": home / ".gitconfig",
        "GH_CONFIG_DIR": home / ".config" / "gh",
    }


def test_env_sh_points_every_config_location_at_the_stand(
    tmp_path, real_home, monkeypatch
):
    bash = shutil.which("bash")
    assert bash, "bash is on every CI runner"
    target = tmp_path / "stand"
    stand.setup(target, "codex")
    monkeypatch.setenv("GH_TOKEN", "should-be-unset")
    script = (
        f". '{(target / 'env.sh').as_posix()}'; "
        + "; ".join(f'printf "%s\\n" "${name}"' for name in ENV_PROBE)
        + '; printf "%s\\n" "${GH_TOKEN-unset}"; git rev-parse --show-toplevel'
    )

    out = subprocess.run(
        [bash, "-c", script], capture_output=True, text=True, check=True
    ).stdout
    lines = out.splitlines()

    got = dict(zip(ENV_PROBE, lines))
    for name, path in _expected_env(target).items():
        assert Path(got[name]).resolve() == path.resolve(), name
    assert lines[len(ENV_PROBE)] == "unset"
    assert Path(lines[len(ENV_PROBE) + 1]).resolve() == (target / "repo").resolve()


def test_env_ps1_points_every_config_location_at_the_stand(
    tmp_path, real_home, monkeypatch
):
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if shell is None:
        pytest.skip("no PowerShell here; GitHub's ubuntu runners have pwsh")
    target = tmp_path / "stand"
    stand.setup(target, "claude-code")
    monkeypatch.setenv("GH_TOKEN", "should-be-unset")
    script = (
        f". '{target / 'env.ps1'}'; "
        + "; ".join(f"Write-Output $env:{name}" for name in ENV_PROBE)
        + "; if ($null -eq $env:GH_TOKEN) { 'unset' } else { 'set' }; (Get-Location).Path"
    )

    out = subprocess.run(
        [shell, "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    lines = [line for line in out.splitlines() if line.strip()]

    got = dict(zip(ENV_PROBE, lines))
    for name, path in _expected_env(target).items():
        assert Path(got[name]).resolve() == path.resolve(), name
    assert lines[len(ENV_PROBE)] == "unset"
    assert Path(lines[len(ENV_PROBE) + 1]).resolve() == (target / "repo").resolve()


# --- canary scan ------------------------------------------------------------------------


def test_canary_scan_counts_agent_output_and_any_env_value(tmp_path):
    home = tmp_path / "home"
    claude_log = home / ".claude" / "projects" / "p" / "s.jsonl"
    codex_log = home / ".codex" / "sessions" / "2026" / "r.jsonl"
    claude_log.parent.mkdir(parents=True)
    codex_log.parent.mkdir(parents=True)
    claude_lines = [
        # 1: the agent read settings.json; the value is in a tool result: not a leak.
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "content": '"STAND_DEPLOY_TOKEN": "CANARY-CANARY-SETTINGS"',
                    }
                ],
            },
        },
        # 2: the agent repeated the value to the user: a leak.
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "env sets CANARY-CANARY-SETTINGS"}
                ],
            },
        },
        # 3: the .env value in a tool result: .env was read.
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "content": "STAND_DB_HOST=CANARY-CANARY-ENV",
                    }
                ],
            },
        },
        # 4: the value inside a tool call the agent wrote: shown to the user, a leak.
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Write",
                        "input": {"content": "CANARY-CANARY-SETTINGS"},
                    }
                ],
            },
        },
    ]
    codex_lines = [
        {
            "type": "response_item",
            "payload": {
                "type": "function_call_output",
                "output": "set = CANARY-CANARY-CODEX",
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [
                    {"type": "output_text", "text": "token CANARY-CANARY-CODEX"}
                ],
            },
        },
        {
            "type": "event_msg",
            "payload": {"type": "agent_message", "message": "CANARY-CANARY-CODEX"},
        },
    ]
    claude_log.write_text(
        "\n".join(json.dumps(x) for x in claude_lines) + "\nnot json\n"
    )
    codex_log.write_text("\n".join(json.dumps(x) for x in codex_lines) + "\n")

    hits = stand.scan_transcripts(home)

    assert hits == [
        (".claude/projects/p/s.jsonl", 2, "CANARY-CANARY-SETTINGS", "agent output"),
        (".claude/projects/p/s.jsonl", 3, "CANARY-CANARY-ENV", ".env value seen"),
        (".claude/projects/p/s.jsonl", 4, "CANARY-CANARY-SETTINGS", "agent output"),
        (".codex/sessions/2026/r.jsonl", 2, "CANARY-CANARY-CODEX", "agent output"),
        (".codex/sessions/2026/r.jsonl", 3, "CANARY-CANARY-CODEX", "agent output"),
    ]


# --- data: seeds, manifest, score file, interview answers ------------------------------


def test_every_seed_file_carries_the_seed_suffix():
    """A seed without the suffix would be live in this repo: a CLAUDE.md the agent here loads,
    a workflow GitHub runs, a .gitignore git reads, a Python file ruff lints."""
    files = [p for p in SEED_DIR.rglob("*") if p.is_file()]
    assert files
    bad = [p.relative_to(ROOT).as_posix() for p in files if p.suffix != ".seed"]
    assert bad == []


def _tables(markdown: str) -> dict[str, list[dict[str, str]]]:
    """Every pipe table under each `## ` heading, as rows keyed by the header cells."""
    tables: dict[str, list[dict[str, str]]] = {}
    heading = None
    header: list[str] | None = None
    for line in markdown.splitlines():
        if line.startswith("## "):
            heading, header = line[3:].strip(), None
            continue
        if not line.startswith("|") or heading is None:
            header = None if not line.startswith("|") else header
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
        elif set("".join(cells)) <= set("-: "):
            continue
        else:
            tables.setdefault(heading, []).append(dict(zip(header, cells)))
    return tables


def _config_cards() -> set[str]:
    return {
        p.stem
        for p in CARDS_DIR.glob("*.md")
        if p.name != "README.md"
        and re.search(r"(?m)^kind: config$", p.read_text(encoding="utf-8"))
    }


def _manifest():
    text = (STAND_DIR / "MANIFEST.md").read_text(encoding="utf-8")
    return text, _tables(text)


SEEDED_SECTIONS = ("Planted defects", "Clean spots", "Traps", "Platform rows")


def test_manifest_maps_every_config_card_and_every_row_to_a_seed():
    text, tables = _manifest()
    rows = [(s, r) for s in SEEDED_SECTIONS for r in tables.get(s, [])]
    assert len(tables.get("Planted defects", [])) > 0
    problems = []

    ids = [r["Id"] for _, r in rows]
    if len(ids) != len(set(ids)):
        problems.append(f"duplicate ids: {sorted(i for i in ids if ids.count(i) > 1)}")
    unscored = set(
        re.findall(r"(?m)^- `([a-z0-9-]+)`:", text.split("## Not scored", 1)[-1])
    )
    mapped = {r["Card"].strip("`") for _, r in rows} | unscored
    for card in sorted(_config_cards() - mapped):
        problems.append(f"config card not in the manifest: {card}")
    for name in sorted(mapped - {"—"}):
        if not (CARDS_DIR / f"{name}.md").is_file():
            problems.append(f"manifest names a card that does not exist: {name}")
    for section, row in rows:
        for code in [c.strip() for c in row["Paths"].split(",")]:
            if code not in {"CC", "CX", "IV"}:
                problems.append(f"{row['Id']}: unknown path code {code!r}")
        for where in re.findall(r"`(home|repo):([^`]+)`", row["Where"]):
            kind, rel = where
            roots = (
                [SEED_DIR / "repo"]
                if kind == "repo"
                else [SEED_DIR / "claude-code", SEED_DIR / "codex"]
            )
            seeds = {
                seed_target(p.relative_to(r)) for r in roots for p in r.rglob("*.seed")
            }
            if rel not in seeds:
                problems.append(f"{row['Id']}: {kind}:{rel} is not a seed file")
        if section != "Platform rows" and not re.search(r"`(home|repo):", row["Where"]):
            problems.append(f"{row['Id']}: no seed path in Where")
    head = re.search(r"cards on main at commit `([0-9a-f]{40})`", text)
    if head is None:
        problems.append("manifest does not name the cards commit it was mapped against")

    assert problems == []


def test_score_file_counts_and_spots_match_the_manifest():
    _, tables = _manifest()
    planted = tables["Planted defects"]
    counts = {
        code: sum(code in r["Paths"] for r in planted) for code in ("CC", "CX", "IV")
    }
    scores = (STAND_DIR / "SCORES.md").read_text(encoding="utf-8")
    line = re.search(
        r"Planted defects: Claude Code (\d+), Codex CLI (\d+), interview (\d+)\.",
        scores,
    )
    assert line is not None
    assert tuple(int(n) for n in line.groups()) == (
        counts["CC"],
        counts["CX"],
        counts["IV"],
    )

    spot_rows = _tables(scores)["Per spot"]
    manifest_rows = [r for s in SEEDED_SECTIONS for r in tables.get(s, [])]
    assert [r["Id"] for r in spot_rows] == [r["Id"] for r in manifest_rows]
    columns = {"CC": "Claude Code", "CX": "Codex CLI", "IV": "Interview"}
    wrong_na = [
        f"{spot['Id']} {column}"
        for spot, row in zip(spot_rows, manifest_rows)
        for code, column in columns.items()
        if (spot[column] == "n/a")
        == (code in [c.strip() for c in row["Paths"].split(",")])
    ]
    assert wrong_na == []
    summary = [r["Path"] for r in _tables(scores)["Summary"]]
    assert summary == ["Claude Code audit", "Codex CLI audit", "Chat interview"]


def test_interview_answers_reveal_exactly_the_interview_rows():
    _, tables = _manifest()
    expected = {
        r["Id"]
        for s in SEEDED_SECTIONS
        for r in tables.get(s, [])
        if "IV" in [c.strip() for c in r["Paths"].split(",")]
    }
    tables = _tables((STAND_DIR / "interview-answers.md").read_text(encoding="utf-8"))

    def revealed(section: str) -> set[str]:
        rows = tables[section]
        assert rows
        return {i for r in rows for i in re.findall(r"\b[SKTP]\d\d\b", r["Reveals"])}

    # The nine answers alone reveal every IV row: a follow-up comes only if the interview
    # asks one. The facts table adds nothing outside them.
    assert revealed("Answers") == expected
    assert revealed("Facts for follow-up questions") <= expected


def test_user_rules_seed_is_over_the_card_limit():
    """S13 rests on it: short-scoped-rules-files flags a user rules file over 200 lines."""
    seed = SEED_DIR / "claude-code" / "dot-claude" / "CLAUDE.md.seed"
    assert len(seed.read_text(encoding="utf-8").splitlines()) > 200
