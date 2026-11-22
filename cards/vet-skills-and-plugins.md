---
kind: habit
why: Skills, plugins, hooks and MCP servers run with the agent's rights, so one that leaks a secret or fetches its instructions from the web changes what the agent does without any code review.
applies_when: you or your team install skills, plugins, hooks, rules files or MCP servers written by someone else, or ones that update themselves
last_reviewed: 2026-11-22
---

# Review skills and plugins like code before they load, and again after they change

## Check

List everything your agent loads besides its own prompt: skills, plugins, hooks, MCP servers,
rules files, each with its source and version. For each one from outside your team, name who
reviewed it, which version they read, and when it was last checked after an update. Then search
their files for the patterns that matter: printing environment variables or auth headers,
destructive shell commands, permissions wider than the task, and instructions or rules fetched
from a URL at run time. An item nobody reviewed, an item that updates itself with no re-check,
or one that pulls its behaviour from a remote file fails.

## Learn

- [We vetted 2,000 AI skills before they reached developers, 7:20](https://www.youtube.com/watch?v=iKQ78wyJEXU&t=440): a vetting pipeline from local scan to pull request, a deterministic scanner, model review for context, and a policy decision.
- [We vetted 2,000 AI skills before they reached developers, 9:40](https://www.youtube.com/watch?v=iKQ78wyJEXU&t=580): why the deterministic scan comes first, and why skills are scanned again after upload.
- [Skills are new features: building skill-centric harness (FactSet), 14:01](https://www.youtube.com/watch?v=7jjudsEhBtM&t=841): running skills like features: admission gates, owners, versions, deprecation, audits, a tool allowlist per skill.
- [Through the AI fog: the architectural decision the next 24 months of agentic security depends on, 18:55](https://www.youtube.com/watch?v=1EZdpEhwmNc&t=1135): a shared skill that echoes an authorization header and loads its rules from a file on the internet.

## Evidence for

- 2026-11-22: Nubank scanned more than 2,000 skills and found more than 1,500 risks, fixed about a thousand at once, blocked some before they reached its internal marketplace, and found new risks when it rescanned old skills ([We vetted 2,000 AI skills](https://www.youtube.com/watch?v=iKQ78wyJEXU&t=440)). A case study with counts from the company's own pipeline.
- 2026-11-22: the Snyk demo shows why a re-check is needed even when the file does not change: a skill that reads its rules from a remote file behaves differently when that file changes ([Through the AI fog](https://www.youtube.com/watch?v=1EZdpEhwmNc&t=1135)). A demo.
- 2026-11-22: [pattern-matched boundaries](../docs/classes/pattern-matched-boundaries.md) records repository files that were once passive data and now control what runs, including settings that took effect before a person trusted the repository; a plugin or hook is such a file.
- 2026-11-22: [untrusted content steers the agent](../docs/classes/untrusted-content-steers-the-agent.md) records text from outside reaching an agent that holds tokens and a shell; a skill's instructions are text the agent follows by design.

## Evidence against

- 2026-11-22: the scans are noisy: Nubank had to calibrate severity, and its model review saw a risk on some runs and missed it on others, which is why it put a deterministic scanner in front ([We vetted 2,000 AI skills](https://www.youtube.com/watch?v=iKQ78wyJEXU&t=580)).
- 2026-11-22: a review covers the version read; a skill that fetches content at run time, or a plugin that updates itself, is unreviewed again the next day unless the version is pinned or the fetch removed.
- 2026-11-22: it costs reviewer time per skill and per update, and the case for it at a small team rests on one company's counts and vendor demos, not on a measured rate of harm.

## Guards

- [untrusted-content-steers-the-agent](../docs/classes/untrusted-content-steers-the-agent.md)
- [pattern-matched-boundaries](../docs/classes/pattern-matched-boundaries.md)
