---
kind: belief
why: Past some point, loading more into an agent's context lowers how well it uses any of it, so a longer rules file, more skills or a bigger window can make the work worse.
applies_when: you decide what goes into an agent's context: rules files, skills, docs, search results, tool output, long sessions, or a model with a larger window
last_reviewed: 2026-11-22
---

# More context is not better context

## Check

Measure what loads into every session before the task starts: rules files, skills, memory,
tool descriptions. Then look at your session logs for where the agent stopped following a
written rule or lost a constraint, and note how far into the session it happened and how
large the context was by then. Run one task you know well twice, once with the usual load and
once with only what the task needs, and compare the result. If the lean run is as good or
better, the extra context was costing you.

## Learn

- [The unreasonable effectiveness of BM25 for agentic search (Hornet.dev), 5:54](https://www.youtube.com/watch?v=fZH97QHHYjY&t=354): context as a small, fixed space, where what you put in decides the result.
- [How I deleted 95% of my agent skills and got better results (WorkOS), 8:26](https://www.youtube.com/watch?v=vy7o1g2iHY8&t=506): a measured case where loaded skill text lowered accuracy, and what replaced it.
- [Context Engineering in 2026: Compaction, Memory & Cost, 40:57](https://www.youtube.com/watch?v=WP3hjUXd918&t=2457): the counter-case, where keeping the full history beat cutting it.
- [How to Build Agents That Run for Hours (Without Losing the Plot), 41:55](https://www.youtube.com/watch?v=mR-WAvEPRwE&t=2515): fresh windows against one long session, and why the authors' answer changed with newer models.

## Evidence for

- 2026-11-22: on the IFScale benchmark, compliance falls as instructions are added, to 68% for the best models at 500; across 1,650 Claude Code sessions, compliance fell as the agent generated more code; repository context files did not generally raise task success and added over 20% to cost (all in [knowledge not at the point of action](../docs/classes/knowledge-not-at-point-of-action.md)). Measured.
- 2026-11-22: the WorkOS talk reports a case where a loaded skill cut accuracy by about 20 percentage points. One team's measurement.
- 2026-11-22: a voice-companion team stopped carrying the whole transcript because long sessions degraded and the model lost track of the middle, and now rebuilds context each turn ([Tolan: Voice-First AI Companion (Tolan), 6:53](https://www.youtube.com/watch?v=xLUQOqjudtA&t=413)). A case.

## Evidence against

- 2026-11-22: the team behind the long-running-agents talk moved from fresh windows to one long session with compaction once models had a 1M-token window, treats context rot as a model defect that is going away, and says to choose by your own evals.
- 2026-11-22: in the Context Engineering talk, on sessions of 11 to 13 turns, the untouched full history was cheaper, faster and better on recall than the compaction strategies, because the agent fetched dropped tool output again. A small dataset.
- 2026-11-22: cutting context loses things too: in one evaluation, compression methods kept track of files worst of all the dimensions scored (Factory, in [knowledge not at the point of action](../docs/classes/knowledge-not-at-point-of-action.md)).
- 2026-11-22: a model vendor's talk, Why AI Agents Need Million-Token Context (MiniMax), argues that long-horizon agents need very large windows to avoid lossy summaries. An argument without a measurement; no timestamped citation for it was found, so it is not linked.

## Guards

- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
