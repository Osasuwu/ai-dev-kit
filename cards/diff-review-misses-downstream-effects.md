---
kind: belief
why: A review that reads only the diff cannot see who consumes what changed, so a change correct on its own breaks a caller while every check stays green.
applies_when: a person or a model approves changes by reading the diff, in a codebase where other code, services or data pipelines consume what changes
last_reviewed: 2026-11-22
---

# Reviewing the diff misses what breaks downstream

## Check

Take your recent reverts and incidents. For each, ask whether the part that broke was in the
diff or in a consumer outside it: a caller, a service on the other end of an API, a job that
reads a changed column. Then look at what your reviewer, person or model, is given: the diff
alone, or also the callers, the consumers and the data lineage of what changed. If most breaks
sit outside the diff and the reviewer sees only the diff, the belief holds for you.

## Learn

- [How to Build an AI Code Review Agent (Greptile), 3:11](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=191): why a naive reviewer, a model given the diff by a webhook, misses bugs and does not understand how the codebase fits together.
- [60% of Our Data PRs Now Merge With No Human Review (Robinhood), 8:08](https://www.youtube.com/watch?v=MQiojLnK-E0&t=488): deterministic checks that walk the data lineage and ask each registered consumer of a changed column whether it breaks.
- [We Mapped 115 Microservices for Our Coding Agents (Postman), 12:53](https://www.youtube.com/watch?v=k2ClBT4aqAg&t=773): a dependency graph given to the agent, and what happened when the graph fell behind the code.

## Evidence for

- 2026-11-22: the Robinhood talk shows a schema change with CI green and the linter satisfied, and a consumer several steps away that broke. A case.
- 2026-11-22: in the Postman talk, about 75% of pull requests in the ten busiest repositories touched an API, and with the graph the agent found the shapes of consumers' requests and judged impact better. Internal measurements, no control group.
- 2026-11-22: [done is not the effect](../docs/classes/done-is-not-the-effect.md) records a review that asked who calls the new code and found a module with no production caller, and notes that a review breaks when the missing effect lies outside the diff.

## Evidence against

- 2026-11-22: the remedy depends on a map that stays current. Postman's graph fell behind as new consumers appeared, its results diverged from reality and developers stopped trusting it; Robinhood's check sees only what the lineage records. Both limits are stated by the teams themselves.
- 2026-11-22: tests and CI that run the real consumers catch part of this without the reviewer seeing past the diff ([done is not the effect](../docs/classes/done-is-not-the-effect.md), integration-test rung), so the gap is widest where consumers have no such tests.
- 2026-11-22: the evidence is company cases with internal numbers; no study was found that measures what share of agent-caused breaks lie outside the diff.

## Guards

- [llm-as-measuring-instrument](../docs/classes/llm-as-measuring-instrument.md)
- [done-is-not-the-effect](../docs/classes/done-is-not-the-effect.md)
