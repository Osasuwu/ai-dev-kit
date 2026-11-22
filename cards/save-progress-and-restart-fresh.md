---
kind: habit
why: Compaction decides what to keep, so a long session loses decisions and unchecked premises, and the agent carries on from the summary as if it were the record.
applies_when: an AI coding agent works on one task long enough to fill its context window or to span several sessions
last_reviewed: 2026-11-22
---

# Keep progress in a file, and start the next session fresh from it

## Check

Pick a task that ran across several sessions or compactions. Is there a progress file in the
workspace with the plan, the steps done, the next step and the premises not yet checked? Did
each new session start by reading it and running a quick smoke test before changing anything?
Then read the edits made right after a compaction and look for one built on a premise from the
summary that was wrong. Finally, ask whether you chose between fresh sessions and one long
session by trying both on your own tasks.

## Learn

- [How to build agents that run for hours (without losing the plot), 12:58](https://www.youtube.com/watch?v=mR-WAvEPRwE&t=778): a progress file, an init script and a feature list, with each iteration in a fresh window.
- [Context engineering in 2026: compaction, memory & cost, 40:57](https://www.youtube.com/watch?v=WP3hjUXd918&t=2457): a comparison against keeping the full history, and why dropped tool output gets fetched again.
- [How we solved context management in agents, 5:45](https://www.youtube.com/watch?v=esY99nYXxR4&t=345): why free-form summarisation was dropped and what replaced it.

## Evidence for

- 2026-11-22: Anthropic's write-up on harnesses for long-running agents keeps a progress file and a feature list across context windows ([Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), cited in [knowledge not at point of action](../docs/classes/knowledge-not-at-point-of-action.md)). Vendor engineering practice.
- 2026-11-22: Claude Code's hooks guide says compaction can lose important details, and the class doc records an agent acting on a premise from a summary without re-reading the source ([knowledge not at point of action](../docs/classes/knowledge-not-at-point-of-action.md)).
- 2026-11-22: the context management talk dropped free-form summarisation because it gave no control over what was kept. A case.

## Evidence against

- 2026-11-22: the team behind the first talk moved from fresh windows to one long session with compaction once newer models with a much larger window arrived, and says the choice should follow your own evals. The habit may be a workaround for current models.
- 2026-11-22: in the compaction comparison, the untouched history on sessions of 11 to 13 turns was cheaper, faster and better on recall, because output thrown away was fetched again. A small dataset.
- 2026-11-22: a progress file is a narrative too: when it is cheaper to read than the system of record, the agent reads it and trusts it, and summaries tend to keep conclusions while losing which files changed ([knowledge not at point of action](../docs/classes/knowledge-not-at-point-of-action.md); [claims from plausibility](../docs/classes/claims-from-plausibility.md)).

## Guards

- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
- [claims-from-plausibility](../docs/classes/claims-from-plausibility.md)
