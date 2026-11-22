---
kind: habit
why: Agents that share one checkout overwrite each other's edits and commit each other's half-finished files, and neither session shows it.
applies_when: you run more than one AI coding agent or session on the same repository at the same time
last_reviewed: 2026-11-22
---

# Give each agent its own workspace

## Check

List the agent sessions that ran in parallel yesterday and where each one worked. Did any two
share a working directory, or did one work in the main checkout while another worked beside it?
`git worktree list` shows the worktrees in use. Look at recent pull requests for changes that
belong to another task, a sign two agents shared a tree. Look for a worktree placed inside the
repository, which a later `git add -A` stages as a submodule entry with no URL.

## Learn

- [Your team's agents are all shipping to the same code at once (Tessl), 5:20](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=320): the ways to isolate agents (worktree, own machine, mocked APIs, database snapshots) and to settle the collisions that remain. Product-leaning.
- [Claude Code worktrees](https://code.claude.com/docs/en/worktrees): a separate copy of the files per session, and what the isolation does not track.
- [Codex worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees): why one branch can be checked out in only one place at a time.
- [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams): splitting work so that each agent owns a different set of files.

## Evidence for

- 2026-11-22: Claude Code's agent teams page warns that two teammates editing the same file overwrite each other ([agent teams](https://code.claude.com/docs/en/agent-teams)). Vendor docs.
- 2026-11-22: Claude Code, Cursor and Codex all ship per-session worktrees as the way to run agents in parallel (sources in [shared state without ownership](../docs/classes/shared-state-without-ownership.md), rung "One workspace per writer").
- 2026-11-22: the class doc's symptoms include a pull request that carried another task's changes because two agents shared a working tree, and a main checkout left on a detached head by an agent working in it.

## Evidence against

- 2026-11-22: a worktree isolates files, not commands: a shell command can write outside it, and the tool does not track which files a command wrote ([Claude Code worktrees](https://code.claude.com/docs/en/worktrees)).
- 2026-11-22: the isolation itself fails in recorded cases: worktrees share one `.git`, so creating them in parallel races; a subagent resumed after its worktree was removed ran in the main checkout; a worktree inside the repository was committed and broke every CI checkout of the branch ([shared state without ownership](../docs/classes/shared-state-without-ownership.md)).
- 2026-11-22: it costs disk and setup per agent, and Cursor caps worktrees per machine. Separate trees also defer conflicts to the merge, and state outside the repository (issues, databases, CI checks) stays shared; other practices have to cover both.
- 2026-11-22: no source measures how often separate workspaces prevent the failure; the evidence is vendor docs and incident reports.

## Guards

- [shared-state-without-ownership](../docs/classes/shared-state-without-ownership.md)
