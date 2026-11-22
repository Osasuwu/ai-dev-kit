---
kind: config
why: A permission prompt decides whether one command runs, not what it can reach once it runs, so a command that slips past a rule or is approved by habit can write anywhere and send data anywhere.
applies_when: an agent runs shell commands on a machine or runner that holds files, credentials or network access beyond what the task needs
last_reviewed: 2026-11-22
---

# Run the agent's shell inside a filesystem and network allowlist

## Check

For Claude Code, read the resolved sandbox settings with `/sandbox` (the Config tab), which
includes managed settings. The project and user files alone can be read with:

```
jq '.sandbox' .claude/settings.json .claude/settings.local.json ~/.claude/settings.json 2>/dev/null
```

The practice holds when `enabled` is `true`, `allowUnsandboxedCommands` is `false`,
`network.allowedDomains` names only the hosts the work needs, and `excludedCommands` is short.
On native Windows commands run unsandboxed whatever the settings say; there it holds only
inside WSL2 or a container. For other agents, check that they run in a container or VM whose
outbound traffic, DNS included, is default-deny.

## Fix

- In Claude Code, set `sandbox.enabled: true`, `failIfUnavailable: true` and
  `allowUnsandboxedCommands: false`, so a blocked command cannot be retried outside the
  sandbox. List the writable paths under `sandbox.filesystem.allowWrite` and the reachable hosts
  under `sandbox.network.allowedDomains`; keep broad code hosts off the list where you can.
- Deliver these keys through managed settings, and also set the locks the sandboxing docs list
  for them: list settings merge across scopes, so without a lock a project's settings can still
  append writable paths or allowed hosts to the managed ones.
- For unattended runs, use a container with an egress firewall, such as Claude Code's reference
  development container, and keep host secrets out of it.

## Learn

- [Rethinking Claude Code Best Practices (Anthropic), 7:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=440): what should move out of the prompt into permissions and an OS-level sandbox.
- [Security Firewall for Agents, 2:32](https://www.youtube.com/watch?v=MkRYPFIMCSA&t=152): why a control at the tool level is bypassed once the agent runs a client program as a subprocess, and why the check has to sit outside the agent.
- [Real AI Agent Attacks and What Would Have Stopped Them (Bloomberg), 9:20](https://www.youtube.com/watch?v=5O6jLtoeKrg&t=560): incidents matched to controls, including data sent out over DNS while web access was closed.
- [Claude Code sandboxing](https://code.claude.com/docs/en/sandboxing): the settings, what the sandbox covers, and the escape hatch.

## Evidence for

- 2026-11-22: Claude Code's docs say the allowed paths are enforced at the OS level for every command in the sandbox and its child processes, and that effective sandboxing needs both filesystem and network isolation ([pattern-matched boundaries](../docs/classes/pattern-matched-boundaries.md)).
- 2026-11-22: a survey of eleven open-source coding agents found that every guard reading a command's raw text was defeated by quote removal alone; a sandbox does not depend on reading the text ([irreversible effects](../docs/classes/irreversible-effects.md), from a security vendor's write-up).
- 2026-11-22: the talks above are case studies (Anthropic, Deno, Bloomberg) arguing that the model's alignment is not a security boundary and that the limit has to be enforced outside it; none gives a measured effect.

## Evidence against

- 2026-11-22: the sandbox covers shell commands only; file tools, MCP servers and hooks run outside it, and a command on the excluded list or retried with the sandbox off runs unsandboxed ([irreversible effects](../docs/classes/irreversible-effects.md)).
- 2026-11-22: an allowed host can itself be the way out: allowing a broad domain such as a code host opens a path for exfiltration ([untrusted content steers the agent](../docs/classes/untrusted-content-steers-the-agent.md)).
- 2026-11-22: the docs call it not a complete isolation boundary; a container used with an untrusted repository can still lose the agent's own credentials; and allowlists cost upkeep and fail legitimate commands. A network proxy outside the agent adds a component to run, and a single point of failure.

## Guards

- [irreversible-effects](../docs/classes/irreversible-effects.md)
- [pattern-matched-boundaries](../docs/classes/pattern-matched-boundaries.md)
- [untrusted-content-steers-the-agent](../docs/classes/untrusted-content-steers-the-agent.md)
