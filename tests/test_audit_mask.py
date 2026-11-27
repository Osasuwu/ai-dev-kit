"""Tests for the audit prompt's mask commands (issue #373).

The audit reads the user's agent config files only through a mask command that `prompts/audit.md`
gives for bash or zsh and for PowerShell. These tests take both commands from the prompt itself,
run them on the stand's seeded config files and on files of harder cases, and check that no
secret value comes out while the values the cards' Checks read come out unchanged.

Each command runs twice: fed on stdin, as a pasted line reaches a shell, and passed as one
argument, as an agent's shell tool passes it. On Windows the second path re-quotes the command
on its way to bash, which is where a mask that needs backslashes breaks.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "prompts" / "audit.md"
SEEDS = ROOT / "stand" / "seed"
CANARY = re.compile(r"CANARY-[A-Z0-9-]+")

# Claude Code settings.json and .mcp.json shapes: pretty-printed the way the tools write them,
# plus hand-written layouts (a value on the line after its key, an object on one line).
HARD_JSON = """{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(gh auth status)",
      "mcp__github__create_pull_request",
      "Bash(./run_all_integration_tests)",
      ["VALUE-INALLOW"],
      "Bash(deploy --token VALUELONGTOKEN0123456789abcdef)"
    ],
    "deny": ["Read(./.env)", "Read(./secrets/**)"],
    "ask": ["Bash(git push:*)",
      "Bash(rm:*)"],
    "defaultMode": "acceptEdits"
  },
  "mcpServers": {
    "allman": {
      "args":
      [
        "--token",
        "VALUE-ALLMAN"
      ]
    },
    "nextline": {
      "command": "npx",
      "args":
      ["-y", "srv", "--api-key", "VALUE-NEXTLINE"]
    },
    "inline": { "type": "stdio", "command": "npx", "args": ["--db", "VALUE-INLARG"], "env": {"DB_PASS": "VALUE-INLENV"} },
    "pairs": {
      "type": "stdio", "command": "npx", "args": ["--db", "VALUE-PAIRS"]
    },
    "db": {
      "options": {
        "MODEL": "VALUE-OPTMODEL"
      },
      "command": "npx",
      "args": [
        "-y",
        "--key",
        "VALUE-ARGLINE"
      ],
      "headers": { "Authorization": "Bearer VALUE-HEADER" },
      "url": "https://mcp.example.com/sse?k=VALUE-URLQUERY"
    }
  },
  "env": {
    "BASE_URL": "${BASE_URL:-https://api.example.com}",
    "GITHUB_PAT": "VALUE-PAT",
    "MODEL": "VALUE-ENVMODEL",
    "command": "VALUE-ENVCMD",
    "DATABASE_URL": "postgres://u:VALUE-DBURL@h/db"
  },
  "sandbox": {
    "enabled": true,
    "network": {
      "allowedDomains": ["github.com"]
    }
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npm test"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "wget --header='Authorization: Bearer VALUE-BEARER' https://hooks.example.com"
          },
          {
            "type": "command",
            "command": "wget --header='Authorization: Basic VALUEBASIC=' https://hooks.example.com"
          },
          {
            "type": "command",
            "command": "wget --header='PRIVATE-TOKEN: glpat-VALUEGLPAT' https://gitlab.example.com"
          },
          {
            "type": "command",
            "command": "deploy --key 123e4567-e89b-12d3-a456-426614174000"
          },
          {
            "type": "command",
            "command": "gh api --token ghp_VALUEGHP"
          }
        ]
      }
    ]
  },
  "escaped": "VALUE-ESC\\"VALUE-AFTER-QUOTE"
}
"""

# Codex CLI config.toml shapes.
HARD_TOML = """# комментарий без секретов
model = "gpt-test"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
# old key VALUECOMMENT0123456789abcdefgh
developer_instructions = \"\"\"
VALUE-MULTILINE
\"\"\"
notes = \"\"\"
quoting '''
VALUE-MIXEDML
\"\"\"

[mcp_servers.gh]
command = "npx"
args = [
  "--api-key",
  "VALUE-TOMLARG",
]
http_headers = { "Authorization" = "Bearer VALUE-HEADER2" }

[mcp_servers.nested]
args = [
  ["--token", "VALUE-NESTED"],
]

[mcp_servers.pg]
command = "psql postgresql://u:VALUE-USERINFO@db.example.com/app"

[mcp_servers.gh.env]
GH_VALUE = "VALUE-TABLE"
OTHER = 'VALUE-LITERAL'
command = "VALUE-TABLECMD"

[projects.'/home/u/src/keycloak-app']
trust_level = "trusted"

[projects.'/home/u/src/tabbed']
\ttrust_level = "untrusted"

[mcp_servers.mysql]
command = "mysql --password=VALUE-PASSWORD"

[shell_environment_policy]
inherit = "all"
set = { "DEPLOY_TOKEN" = "VALUE-INLINE" }
"""

HARD_SECRETS = [
    "VALUELONGTOKEN",
    "VALUE-ALLMAN",
    "VALUE-NEXTLINE",
    "VALUE-INLARG",
    "VALUE-INLENV",
    "VALUE-PAIRS",
    "VALUE-INALLOW",
    "VALUE-OPTMODEL",
    "VALUE-ARGLINE",
    "VALUE-HEADER",
    "VALUE-URLQUERY",
    "VALUE-PAT",
    "VALUE-ENVMODEL",
    "VALUE-ENVCMD",
    "VALUE-DBURL",
    "VALUE-BEARER",
    "VALUEBASIC",
    "VALUEGLPAT",
    "426614174000",
    "VALUEGHP",
    "VALUE-ESC",
    "VALUE-AFTER-QUOTE",
    "VALUECOMMENT",
    "VALUE-MULTILINE",
    "VALUE-MIXEDML",
    "VALUE-TOMLARG",
    "VALUE-HEADER2",
    "VALUE-NESTED",
    "VALUE-USERINFO",
    "VALUE-TABLE",
    "VALUE-LITERAL",
    "VALUE-TABLECMD",
    "VALUE-PASSWORD",
    "VALUE-INLINE",
]

# Lines a card's Check reads: they must come out exactly as they went in.
HARD_KEPT = {
    "hard.json": [
        '      "Bash(npm test)",',
        '      "Bash(gh auth status)",',
        '      "mcp__github__create_pull_request",',
        '      "Bash(./run_all_integration_tests)",',
        '    "deny": ["Read(./.env)", "Read(./secrets/**)"],',
        '    "ask": ["Bash(git push:*)",',
        '      "Bash(rm:*)"],',
        '    "defaultMode": "acceptEdits"',
        '    "enabled": true,',
        '      "allowedDomains": ["github.com"]',
        '        "matcher": "Bash",',
        '            "type": "command",',
        '            "command": "npm test"',
        '      "command": "npx",',
    ],
    "hard.toml": [
        "# комментарий без секретов",
        'model = "gpt-test"',
        'approval_policy = "on-request"',
        'sandbox_mode = "workspace-write"',
        "[mcp_servers.gh]",
        'command = "npx"',
        "[projects.'/home/u/src/keycloak-app']",
        'trust_level = "trusted"',
        '\ttrust_level = "untrusted"',
        "[shell_environment_policy]",
        'inherit = "all"',
    ],
}

# Masked lines keep their key and their shape, so the agent can tell what is set.
HARD_MASKED = {
    "hard.json": [
        '    "BASE_URL": "<redacted>",',
        '    "GITHUB_PAT": "<redacted>",',
        '    "MODEL": "<redacted>",',
        '    "command": "<redacted>",',
        '    "DATABASE_URL": "<redacted>"',
        '        "<redacted>"',
        '      "headers": { "<redacted>": "<redacted>" },',
    ],
    "hard.toml": [
        '  "<redacted>",',
        'command = "<redacted>"',
        'GH_VALUE = "<redacted>"',
        "OTHER = '<redacted>'",
        'set = { "<redacted>" = "<redacted>" }',
    ],
}

# A file saved on Windows: a byte order mark and CRLF line ends. The first line is a Check line,
# so a mask that misreads the mark would change it.
BOM_FILES = {
    "settings.json": (
        '{\n  "permissions": {\n    "defaultMode": "acceptEdits"\n  },\n'
        '  "env": {\n    "K": "VALUE-BOM"\n  }\n}\n',
        ["{", '    "defaultMode": "acceptEdits"'],
    ),
    "config.toml": (
        'approval_policy = "never"\n[projects.\'/x\']\ntrust_level = "trusted"\n'
        '[mcp_servers.a.env]\nK = "VALUE-BOM"\n',
        ['approval_policy = "never"', "[projects.'/x']", 'trust_level = "trusted"'],
    ),
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


def _exe(*names: str) -> str:
    for name in names:
        found = shutil.which(name)
        if name == "bash" and os.name == "nt" and found and "system32" in found.lower():
            # On Windows, PATH may find the WSL launcher first; the agents' shell tools run
            # Git Bash, so test that one.
            git = shutil.which("git")
            found = None
            for parent in Path(git).resolve().parents if git else ():
                if (parent / "bin" / "bash.exe").exists():
                    found = str(parent / "bin" / "bash.exe")
                    break
        if found:
            return found
    if os.environ.get("CI"):
        pytest.fail(f"CI must have {' or '.join(names)} to test the mask")
    pytest.skip(f"no {' or '.join(names)} on this machine")


def _run(args: list[str], stdin: str | None) -> str:
    out = subprocess.run(
        args, input=stdin, capture_output=True, text=True, encoding="utf-8", check=True
    )
    return out.stdout.replace("\r\n", "\n")


def _bash(path: Path, via: str) -> str:
    bash = _exe("bash")
    cmd = _command("bash or zsh").replace('"FILE"', f'"{path.as_posix()}"')
    if via == "stdin":
        return _run([bash, "-s"], cmd + "\n")
    return _run([bash, "-c", cmd], None)


def _powershell(path: Path, via: str) -> str:
    exe = _exe("pwsh", "powershell")
    cmd = _command("PowerShell").replace('"FILE"', f'"{path}"')
    utf8 = "[Console]::OutputEncoding = [Text.Encoding]::UTF8; "
    base = [exe, "-NoProfile", "-NonInteractive", "-Command"]
    if via == "stdin":
        return _run([*base, "-"], utf8 + cmd + "\n")
    return _run([*base, utf8 + cmd], None)


RUNNERS = {
    "bash-stdin": lambda p: _bash(p, "stdin"),
    "bash-arg": lambda p: _bash(p, "arg"),
    "powershell-stdin": lambda p: _powershell(p, "stdin"),
    "powershell-arg": lambda p: _powershell(p, "arg"),
}


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
    # The mask reads TOML by the file's extension, so the file keeps its real name.
    path = tmp_path / src.name.removesuffix(".seed")
    path.write_bytes(text.encode("utf-8"))

    out = mask(path)

    assert not CANARY.search(out), f"{seed}: a canary value came through the mask"
    kept = [
        line
        for line in text.splitlines()
        if re.search(
            r"allow|Bash\(|sandbox|enabled|approval_policy|trust_level|^\[", line
        )
        and not CANARY.search(line)
    ]
    assert kept, "the seed must hold lines a card's Check reads"
    out_lines = out.splitlines()
    for line in kept:
        assert line in out_lines, f"{seed}: changed a line the Checks read: {line!r}"
    assert len(out_lines) == len(text.splitlines()), (
        f"{seed}: the mask dropped or added lines"
    )


@pytest.mark.parametrize(
    "name,body", [("hard.json", HARD_JSON), ("hard.toml", HARD_TOML)]
)
def test_mask_hides_secrets_in_the_harder_shapes(mask, name, body, tmp_path):
    path = tmp_path / name
    path.write_bytes(body.encode("utf-8"))

    out = mask(path)

    leaked = [s for s in HARD_SECRETS if s in out]
    assert not leaked, f"{name}: values came through the mask: {leaked}"
    out_lines = out.splitlines()
    for line in HARD_KEPT[name]:
        assert line in body.splitlines(), f"fixture error: {line!r} is not in {name}"
        assert line in out_lines, f"{name}: changed a line a Check reads: {line!r}"
    for line in HARD_MASKED[name]:
        assert line in out_lines, (
            f"{name}: a masked line lost its key or its shape: {line!r}"
        )
    assert len(out_lines) == len(body.splitlines()), (
        f"{name}: the mask dropped or added lines"
    )


@pytest.mark.parametrize("name", sorted(BOM_FILES))
def test_mask_reads_a_file_saved_with_a_bom_and_crlf(mask, name, tmp_path):
    body, kept = BOM_FILES[name]
    path = tmp_path / name
    path.write_bytes(("﻿" + body.replace("\n", "\r\n")).encode("utf-8"))

    out = mask(path)

    assert "VALUE-BOM" not in out, f"{name}: a value came through the mask"
    out_lines = out.splitlines()
    for line in kept:
        assert line in out_lines, f"{name}: changed a line a Check reads: {line!r}"
    assert len(out_lines) == len(body.splitlines()), (
        f"{name}: the mask dropped or added lines"
    )
