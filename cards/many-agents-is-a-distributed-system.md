---
kind: belief
why: Once several agents share state or hand work to each other, their failures are races, stale reads and lost replies, which a prompt cannot fix and a confident summary hides.
applies_when: you run several agents, subagents or automated jobs that hand work to each other or share a repository, tracker, cache or record
last_reviewed: 2026-11-22
---

# Several agents working together are a distributed system

## Check

Pick a recent run with more than one agent. At each handoff, ask: did it end in a named state
(done, failed, unknown) or in free text? When a subagent timed out, did the orchestrator record
"unknown" or carry on as if it had answered? Does code, not the prompt, check each subagent's
output for its shape, its evidence and how fresh it is? Is any shared record, cache or branch
written by more than one agent with no rule for who owns it? Would a retry open a second pull
request?

## Learn

- [Your Sub-Agents Are a Distributed System. Treat Them Like One. (Microsoft), 4:25](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=265): why a confident verdict and a lost answer look alike without explicit states and checks in code.
- [From Chaos to Choreography: Multi-Agent Orchestration Patterns That Actually Work, 3:40](https://www.youtube.com/watch?v=2czYyrTzILg&t=220): an incident with a shared cache, and why coordination grows harder faster than the number of agents.
- [What Does Done Even Mean? Agents and Paperclip's Liveness Model (Paperclip), 1:34](https://www.youtube.com/watch?v=7P0elyLIxXo&t=94): keeping work moving against checking all of it, and where checking everything stops being real.

## Evidence for

- 2026-11-22: in the Chaos to Choreography talk, agents read a stale score from a shared cache whose invalidation was broken; the race was in the architecture, not the model, and immutable versioned state with explicit handoffs fixed it. A case.
- 2026-11-22: in the Microsoft talk, three subagents returned the same verdict with the same confidence: one had investigated, one had matched a header, one had made the answer up. After a timeout, still working, crashed and reply lost cannot be told apart, so a timeout is recorded as unknown. A case and an argument from distributed-systems theory.
- 2026-11-22: [shared state without ownership](../docs/classes/shared-state-without-ownership.md) records duplicate dispatch, a shared working tree, claims that outlived their run and merges racing a review, with defect reports that count them; in one operator's audit, every fix that only told the agents to coordinate was followed by a recurrence.

## Evidence against

- 2026-11-22: none of the talks measures anything; they are cases and incident write-ups.
- 2026-11-22: a taxonomy built from over 1,600 multi-agent traces grouped failures mostly as problems in the conversation between agents and named no race on a repository, tracker or CI ([shared state without ownership](../docs/classes/shared-state-without-ownership.md), Evidence). The distributed-systems framing was not where most failures fell in that study.
- 2026-11-22: the framing pays only where work really runs in parallel. A single-threaded agent or a synchronous lead avoids most of it, and one vendor notes that coding tasks offer fewer parallel parts than research (same class doc).

## Guards

- [shared-state-without-ownership](../docs/classes/shared-state-without-ownership.md)
