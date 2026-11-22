---
kind: config
why: A guard whose settings, hooks or rules the agent or a cloned repository can write is one edit away from allowing anything, and the edit looks like ordinary configuration.
applies_when: an agent works under permission rules, hooks or sandbox settings kept in files, including repositories you clone and run it in
last_reviewed: 2026-11-22
---

# Keep the guard's own configuration out of reach of the agent and the project

## Check

Ask the agent, in a scratch session, to add an allow rule to its own settings file and to edit
one of its hook scripts. Both should be refused or put to you, by name, and so should the same
edit made through a shell command rather than the edit tool. Then answer three questions:

- Which settings does a freshly cloned repository apply before you have trusted it? Its hooks,
  environment block and allow rules should wait for your yes.
- Do your headless runs (a `-p` run, an SDK session, CI) trust every folder by default? They show
  no trust dialog.
- Are the rules you never want widened set at a level neither the agent nor a project can
  override, such as managed settings?

## Fix

Keep the agent's settings, hook scripts and rule files on protected paths: Claude Code's sandbox
denies writes to its own configuration inside writable directories, and Codex keeps `.git`,
`.agents` and `.codex` read-only inside a writable root. Create the protected files and folders
up front, since a protection that covers only existing files lets the agent create them. Accept
a repository's workspace settings only after reading them. Put the rules that must hold
everywhere in managed settings, and turn off the mode that skips prompts there.

## Learn

- [Claude Code sandboxing, protected paths](https://code.claude.com/docs/en/sandboxing.md#protected-paths): which files are protected and why a command that could edit them could grant itself permissions.
- [Claude Code permissions, managed settings](https://code.claude.com/docs/en/permissions.md#managed-settings): rules no other level can override, and when a project's allow rules apply.
- [Gemini CLI trusted folders](https://geminicli.com/docs/cli/trusted-folders/): what an untrusted folder's settings and `.env` files may not do.
- [Check Point on project-file RCE](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/): how repository settings read before trust became code execution.

## Evidence for

- 2026-11-22: security advisories describe a sandbox that protected the settings file only when it existed, so code could create it, and a piped command that got past file-write restrictions into the settings folder ([pattern-matched boundaries](../docs/classes/pattern-matched-boundaries.md), [GHSA-mhg7-666j-cqg4](https://github.com/advisories/GHSA-mhg7-666j-cqg4)).
- 2026-11-22: researchers showed project files applied before the trust dialog leading to code execution and token theft ([Check Point](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)); a headless agent that trusted every folder was patched in 2026-04 ([GHSA-wpqr-6v78-jr5g](https://github.com/advisories/GHSA-wpqr-6v78-jr5g)).
- 2026-11-22: two vendors ship this as a default: protected configuration paths in Claude Code and read-only agent folders in Codex ([Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)).

## Evidence against

- 2026-11-22: in a mode that skips permission prompts, writes to protected paths are approved automatically ([permission modes](https://code.claude.com/docs/en/permission-modes.md)).
- 2026-11-22: a trust dialog protects only when it is shown and read; headless runs never show it, and a person who trusts by habit trusts the attack too.
- 2026-11-22: managed policy has to arrive: an advisory describes sessions that started without the organisation's server-managed policy ([GHSA-gfvf-j8jh-jxxw](https://github.com/anthropics/claude-code/security/advisories/GHSA-gfvf-j8jh-jxxw)); and the locked rules are still patterns that leak in the usual ways.
- 2026-11-22: every change to the guard's files goes through a person, and managed settings need an administrator.

## Guards

- [pattern-matched-boundaries](../docs/classes/pattern-matched-boundaries.md)
- [untrusted-content-steers-the-agent](../docs/classes/untrusted-content-steers-the-agent.md)
