"""Tests for the audit prompt's mask commands (issue #373).

The audit reads the user's agent config files only through a mask command that `prompts/audit.md`
gives for bash or zsh and for PowerShell. These tests take both commands from the prompt itself,
run them on the stand's seeded config files and on a file of harder cases, and check that no
secret value comes out while the lines the cards' Checks read come out unchanged.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "prompts" / "audit.md"
SEEDS = ROOT / "stand" / "seed"
CANARY = re.compile(r"CANARY-[A-Z0-9-]+")

HARD_JSON = """{
  "permissions": {
    "allow": ["Bash(git status)"]
  },
  "env": {
    "DATABASE_URL": "postgres://u:VALUE-DBURL@h/db",
    "PLAIN": "VALUE-PLAIN"
  },
  "theme": "dark",
  "headers": { "Authorization": "Bearer VALUE-BEARER" },
  "escaped_token": "VALUE-ESC\\"VALUE-AFTER-QUOTE"
}
"""

HARD_TOML = """model = "gpt-test"
approval_policy = "on-request"

[mcp_servers.gh]
command = "npx"
args = ["-y", "server", "--token", "VALUE-ARGS"]
http_headers = { "Authorization" = "Bearer VALUE-HEADER" }

[mcp_servers.gh.env]
GH_VALUE = "VALUE-TABLE"
OTHER = 'VALUE-LITERAL'

[profiles.work]
name = "work-profile"

[shell_environment_policy]
set = { "DEPLOY_TOKEN" = "VALUE-INLINE" }
"""

HARD_SECRETS = [
    "VALUE-DBURL",
    "VALUE-ESC",
    "VALUE-PLAIN",
    "VALUE-BEARER",
    "VALUE-AFTER-QUOTE",
    "VALUE-ARGS",
    "VALUE-HEADER",
    "VALUE-TABLE",
    "VALUE-LITERAL",
    "VALUE-INLINE",
]

HARD_KEPT = [
    '    "allow": ["Bash(git status)"]',
    '  "theme": "dark",',
    'model = "gpt-test"',
    'approval_policy = "on-request"',
    'command = "npx"',
    'name = "work-profile"',
]

# A masked line still names its key, so the agent can tell what is set without seeing the value.
HARD_MASKED = {
    "hard.json": ['    "DATABASE_URL": "<redacted>",', '    "PLAIN": "<redacted>"'],
    "hard.toml": ['GH_VALUE = "<redacted>"', "OTHER = '<redacted>'"],
}


def _command(label: str) -> str:
    text = PROMPT.read_text(encoding="utf-8")
    found = re.findall(
        rf"^\s*Mask, {re.escape(label)}: (.+)$", text, flags=re.MULTILINE
    )
    assert len(found) == 1, (
        f"prompts/audit.md must give exactly one 'Mask, {label}:' command"
    )
    assert '"FILE"' in found[0], 'the command must take the file as "FILE"'
    return found[0]


def _powershell() -> str | None:
    return shutil.which("pwsh") or shutil.which("powershell")


def _run_bash(path: Path) -> str:
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("no bash on this machine")
    cmd = _command("bash or zsh").replace('"FILE"', f'"{path.as_posix()}"')
    # The command goes in on stdin, as a pasted line would: passed as an argument, Windows
    # re-quotes it on the way to bash and collapses the backslashes the awk regexes need.
    out = subprocess.run(
        [bash, "-s"], input=cmd + "\n", capture_output=True, text=True, check=True
    )
    return out.stdout


def _run_powershell(path: Path) -> str:
    exe = _powershell()
    if exe is None:
        pytest.skip("no PowerShell on this machine")
    cmd = _command("PowerShell").replace('"FILE"', f'"{path}"')
    out = subprocess.run(
        [exe, "-NoProfile", "-NonInteractive", "-Command", "-"],
        input=cmd + "\n",
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.replace("\r\n", "\n")


RUNNERS = {"bash": _run_bash, "powershell": _run_powershell}


@pytest.fixture(params=sorted(RUNNERS))
def mask(request):
    return RUNNERS[request.param]


@pytest.mark.parametrize(
    "seed",
    ["claude-code/dot-claude/settings.json.seed", "codex/dot-codex/config.toml.seed"],
)
def test_mask_hides_the_stand_canary_and_keeps_check_lines(mask, seed, tmp_path):
    src = SEEDS / seed
    text = src.read_text(encoding="utf-8")
    assert CANARY.search(text), (
        "the seed must hold a canary for this test to mean anything"
    )
    path = tmp_path / src.name
    path.write_text(text, encoding="utf-8")

    out = mask(path)

    assert not CANARY.search(out), f"{seed}: a canary value came through the mask"
    kept = [
        line
        for line in text.splitlines()
        if re.search(r"allow|Bash\(|sandbox|enabled|approval_policy|trust_level", line)
        and not CANARY.search(line)
    ]
    assert kept, "the seed must hold lines a card's Check reads"
    out_lines = out.splitlines()
    for line in kept:
        assert line in out_lines, f"{seed}: changed a line the Checks read: {line!r}"


@pytest.mark.parametrize(
    "name,body", [("hard.json", HARD_JSON), ("hard.toml", HARD_TOML)]
)
def test_mask_hides_secrets_in_the_harder_shapes(mask, name, body, tmp_path):
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")

    out = mask(path)

    leaked = [s for s in HARD_SECRETS if s in out]
    assert not leaked, f"{name}: values came through the mask: {leaked}"
    out_lines = out.splitlines()
    for line in HARD_KEPT:
        if line in body.splitlines():
            assert line in out_lines, f"{name}: changed a line with no secret: {line!r}"
    for line in HARD_MASKED[name]:
        assert line in out_lines, (
            f"{name}: a masked line lost its key or its shape: {line!r}"
        )
    assert len(out_lines) == len(body.splitlines()), (
        f"{name}: the mask dropped or added lines"
    )
