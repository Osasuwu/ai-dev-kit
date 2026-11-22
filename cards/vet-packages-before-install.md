---
kind: config
why: An agent adds a package whose name it made up or a version published an hour ago, the install succeeds, the build and tests pass, and what runs is whatever the name's registrant published.
applies_when: an agent can add or update dependencies (a lockfile, `package.json`, `pyproject.toml`) in a project that installs from a public registry
last_reviewed: 2026-11-22
---

# Vet a package before the agent installs it, and refuse versions that are too new

## Check

Look for a release-age floor in the package manager's config:

```
grep -rnE 'minimumReleaseAge|min-release-age|exclude-newer' .npmrc pnpm-workspace.yaml pyproject.toml uv.toml 2>/dev/null
```

No hit means the newest version of anything is installed the moment it is published. Then
check whether installs go through a malware filter, and whether a new dependency in a pull
request gets a lookup (age of the package, who publishes it, whether the name is one letter off
a popular one) before it merges, by a tool or by a reviewer's checklist.

## Fix

- Set a minimum release age: `minimumReleaseAge` in pnpm (set it yourself, which also makes it
  strict), `min-release-age` in npm, `exclude-newer` in uv. A few days covers the window in
  which most malicious releases are found and pulled.
- Give dependency update bots the same delay, so they do not propose a release on its first day.
- Route installs through a tool that blocks known malware, such as Socket Firewall Free.
- Give the agent a package lookup it can call before adding a name, such as Socket's MCP
  server, and require a person's yes for any new dependency.
- Keep a path for urgent security updates that bypasses the delay on purpose.

## Learn

- [Agentic Security: Permissions, Provenance, and the Agent Supply Chain, 2:10](https://www.youtube.com/watch?v=yWS0udrIOc8&t=130): why a squatted package that does what was expected passes the build and the tests unnoticed.
- [AI Security Engineer Foundations + Certificate (Snyk), 1:43:08](https://www.youtube.com/watch?v=ZyC56eV8sVw&t=6188): how a hallucinated name gets registered, and a real case that was downloaded about two hundred times before removal.
- [Real AI Agent Attacks and What Would Have Stopped Them (Bloomberg), 11:50](https://www.youtube.com/watch?v=5O6jLtoeKrg&t=710): a malicious package that shipped many clean releases before one bad one, and why delaying intake works against it.
- [Exploits Now Beat Patches: Open Source Security in the AI Era (Chainguard), 12:43](https://www.youtube.com/watch?v=xZX3pmaB8Hk&t=763): CI, developer machines and agent tooling as the soft targets, and package cooldowns among the defences.
- [pnpm dependency resolution settings](https://pnpm.io/settings/dependency-resolution): `minimumReleaseAge`, its default and when it is strict.

## Evidence for

- 2026-11-22: across 16 models and 576,000 code samples, at least 5.2% of packages named by commercial models and 21.7% by open-source models did not exist ([arXiv 2406.10279](https://arxiv.org/abs/2406.10279), via [claims from plausibility](../docs/classes/claims-from-plausibility.md)).
- 2026-11-22: a researcher registered an empty package under a name models kept inventing, and it was downloaded more than 30,000 times in three months ([Lasso Security](https://www.lasso.security/blog/ai-package-hallucinations), via the class doc).
- 2026-11-22: pnpm's docs give the reason for an age floor: most malicious releases are found and removed from the registry within about an hour.
- 2026-11-22: the Bloomberg talk above is an incident case study of a package that turned malicious after many clean releases; the Chainguard talk's case for cooldowns is made inside a product pitch.

## Evidence against

- 2026-11-22: an age floor stops a squatted name only while it is new; a name registered months ago passes, as the package in the Lasso case did ([claims from plausibility](../docs/classes/claims-from-plausibility.md)).
- 2026-11-22: the delay holds back security fixes too; npm keeps the vulnerable version and errors when the floor blocks an audit fix. pnpm's built-in default is not strict and falls back to a newer version.
- 2026-11-22: a malware filter blocks only confirmed malware; an unknown or empty package is not blocked ([Socket Firewall Free](https://docs.socket.dev/docs/socket-firewall-free)). An agent-side lookup works only when the agent chooses to call it.
- 2026-11-22: neither talk on hallucinated names gives a frequency measurement; both speak from products in the space.

## Guards

- [claims-from-plausibility](../docs/classes/claims-from-plausibility.md)
- [untrusted-content-steers-the-agent](../docs/classes/untrusted-content-steers-the-agent.md)
