---
kind: habit
why: An agent on a schedule with a loose task and its own write access makes changes nobody asked for, and a run that failed or did nothing reads the same as one that worked.
applies_when: you run an agent on a schedule for recurring chores such as dependency and CVE bumps, code cleanup, flag removal or issue triage
last_reviewed: 2026-11-22
---

# Schedule agents only for narrow chores with an outside check, and let code do the writes

## Check

List every agent job that runs on a schedule. For each, answer four questions. Is the chore
narrow, with done stated as something a tool outside the agent reports (the scanner no longer
sees the CVE, the build is green)? Can the agent's own credentials commit, push or open a pull
request, or does a deterministic step do that after checking the change? Is the change the
smallest that meets the condition, for example a version raised only to the release that fixes
the issue? Does every run report its result, success included? A job with a vague chore, an
agent that writes to the repository itself, or a run you would only hear about when it fails,
fails the check.

## Learn

- [We gave an agent production code access and then tried to sleep at night, 3:41](https://www.youtube.com/watch?v=LqLoYksJ6do&t=221): a CVE-fixing setup where a deterministic orchestrator does the work around the agent and the agent only reasons.
- [We gave an agent production code access and then tried to sleep at night, 5:21](https://www.youtube.com/watch?v=LqLoYksJ6do&t=321): why the agent cannot commit, push or open a pull request, and how the controller checks and writes its edits.
- [Realtime multiplayer, automation, and you!, 11:12](https://www.youtube.com/watch?v=iQ5xldZ9StU&t=672): guardrails for scheduled agent workflows: no secrets for the agent, a checking stage before every write, a log of everything.
- [Agents, codebases, and teams: what it actually takes to ship together, 9:14](https://www.youtube.com/watch?v=aeTb5BdmTTc&t=554): a nightly code-tidying agent and a long-running shipping workflow inside a team's routine.

## Evidence for

- 2026-11-22: Form3 describes scheduled CVE fixes where the agent makes the smallest working change, checks the container build, rescans, and hands its edits to a controller that verifies and writes them; the security team's objection shaped that boundary ([We gave an agent production code access](https://www.youtube.com/watch?v=LqLoYksJ6do&t=221)). A practitioner's case without measurements.
- 2026-11-22: GitHub Next shows scheduled agent workflows (a CI doctor, a daily repository summary, issue triage in a large open-source project) run with layered defences and all writes through a checking stage ([Realtime multiplayer, automation, and you!](https://www.youtube.com/watch?v=iQ5xldZ9StU&t=672)). Examples, not a measurement.
- 2026-11-22: [scope overreach](../docs/classes/scope-overreach.md) records agents whose diffs changed things nobody asked for; a chore with a narrow outside condition and a controller that checks the edit leaves less room for that.

## Evidence against

- 2026-11-22: the evidence is three practitioners' cases with no numbers; none reports how often the scheduled changes were rejected or reverted.
- 2026-11-22: it costs a deterministic controller around the agent, and many chores have no outside check to stop on; those are not candidates, and forcing one into the schedule moves the judgement back to the agent.
- 2026-11-22: reporting every run does not catch a job that stops running at all; [silent fallback](../docs/classes/silent-fallback.md) needs an external heartbeat per job for that, and a heartbeat that pings whether or not the job succeeded misses a run that did nothing.

## Guards

- [scope-overreach](../docs/classes/scope-overreach.md)
- [silent-fallback](../docs/classes/silent-fallback.md)
