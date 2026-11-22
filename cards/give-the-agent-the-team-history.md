---
kind: habit
why: Code shows what the system does, not why; an agent that sees only the code undoes deliberate choices and brings back changes that were already tried and reverted.
applies_when: an agent changes or reviews code in an area whose past decisions, reverts or incidents are recorded outside the code
last_reviewed: 2026-11-22
---

# Give the agent the history of the code it changes: decisions, reverts and incidents

## Check

Take the agent's last few changes and look up the history of the files they touched: reverts,
fix commits, linked decisions, incidents, open pull requests on the same lines. Then read the
agent's plan or the review of each change. Did either cite any of that history, or name the
person who owns the trade-off? Count review findings of the kind "this was tried and reverted"
or "this was decided the other way"; each one is history that existed and did not reach the agent
before it wrote the code.

## Learn

- [What your coding agent can't see in the code (Linear), 7:02](https://www.youtube.com/watch?v=Xw9utONfhIY&t=422): a review agent that starts from the issue and its intent, then searches the same area's past decisions, reverts, regressions and incidents.
- [What your coding agent can't see in the code (Linear), 14:15](https://www.youtube.com/watch?v=Xw9utONfhIY&t=855): what else such a reviewer pulls in: overlapping changes, the authoring agent's session and the owner of the product trade-off.
- [Mergeable by default: building the context engine to save time and tokens, 9:36](https://www.youtube.com/watch?v=5ID22ACI7IM&t=576): satisfaction of search, where an agent stops at the first plausible explanation while the right one sits in an old incident or discussion, and a demo of one task with and without that context; a vendor talk, the first quarter hour is enough.
- [How to build an AI code review agent (Greptile), 13:34](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=814): how knowledge about the codebase narrows which files a review agent has to read.

## Evidence for

- 2026-11-22: Linear describes a review agent built around this habit: intent first, then the area's history and the people who own its trade-offs ([What your coding agent can't see in the code](https://www.youtube.com/watch?v=Xw9utONfhIY&t=422)). A practitioner's case without measurements.
- 2026-11-22: in Unblocked's demo, an agent without the history deleted legacy code that existed for a reason, and with it kept backward compatibility ([Mergeable by default](https://www.youtube.com/watch?v=5ID22ACI7IM&t=576)). A vendor's demo of the product it sells.
- 2026-11-22: [knowledge not at the point of action](../docs/classes/knowledge-not-at-point-of-action.md) records agents that acted as if they did not know something written down elsewhere, and [spec not grounded in current state](../docs/classes/spec-not-grounded-in-current-state.md) records tasks whose premises had changed since they were written.

## Evidence against

- 2026-11-22: every source in this cluster is a case or a demo from a vendor that sells such context; none measures how much it changes the share of changes that merge.
- 2026-11-22: naive retrieval over docs runs into sources that disagree, can keep an agent searching until its session has to be compacted, and serves cached answers that go stale (as described in the Mergeable by default talk above).
- 2026-11-22: when an old document and the current code disagree, the talks differ on what should win: freshness checked by a person, or a ranking by who wrote what; a history packet that is out of date misleads as confidently as code alone.
- 2026-11-22: it costs tokens on every change and a place where decisions and reverts are actually recorded; a team that keeps no such record has nothing to give the agent.

## Guards

- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
- [spec-not-grounded-in-current-state](../docs/classes/spec-not-grounded-in-current-state.md)
