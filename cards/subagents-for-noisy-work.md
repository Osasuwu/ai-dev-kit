---
kind: habit
why: Search hits, long logs and large tool outputs pile up in the main agent's context, crowd out the task and bring compaction early.
applies_when: an AI coding agent does work that produces far more output than its conclusion needs, such as searching a codebase, reading logs, running a test suite or reading docs
last_reviewed: 2026-11-22
---

# Send noisy work to a subagent that returns a short summary

## Check

Open the log of a long session and look at what filled its context: how much came from tool
output the agent read once, such as search results, full test output or a log dump? Did the
session compact before the task was done? Where subagents were used, were their returns short,
and did they say where the full output was kept? Pick one subagent verdict the main agent acted
on and check it against the subagent's own tool calls: did it do the work its summary claims?

## Learn

- [If we want them to do knowledge work, design them as knowledge agents (Mixedbread), 12:09](https://www.youtube.com/watch?v=O84lhGc1OOI&t=729): searcher subagents that return short memos to a lead agent, measured on a public benchmark.
- [How we solved context management in agents, 10:00](https://www.youtube.com/watch?v=esY99nYXxR4&t=600): the path from truncation to summarisation to an external store plus subagents, and why each earlier step failed.
- [Building agent interfaces: lessons from Chrome DevTools (MCP) for agents, 3:44](https://www.youtube.com/watch?v=_B4Pv9ttFgY&t=224): a tool that handed the agent a raw trace of several megabytes, and the digest that replaced it.
- [Your sub-agents are a distributed system. Treat them like one. (Microsoft), 4:25](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=265): why a subagent's confident verdict looks the same whether it investigated or made the answer up.

## Evidence for

- 2026-11-22: in the Mixedbread talk, a lead agent that split the question and took short memos from searcher subagents gained about 3.5 points and closed roughly 40% of the gap to having the right documents up front. A public benchmark, measured by a search vendor.
- 2026-11-22: the context management talk reports that free summarisation of long tool output was unstable, and that keeping heavy data in subagents and an external store worked instead. A case.
- 2026-11-22: the Chrome DevTools team found that the raw trace did not work for agents and replaced it with a summary of the key metrics, keeping the raw data reachable. A case.

## Evidence against

- 2026-11-22: a subagent's summary is a claim. In the Microsoft talk three subagents returned the same verdict with the same confidence; one had investigated, one had matched a header, one had invented the answer. The main agent sees the output, not the work behind it ([claims from plausibility](../docs/classes/claims-from-plausibility.md)).
- 2026-11-22: a summary that drops what the agent later needs makes it fetch that again and pay twice; in a comparison on short sessions, keeping the full history came out cheaper and better on recall ([Context engineering in 2026: compaction, memory & cost, 40:57](https://www.youtube.com/watch?v=WP3hjUXd918&t=2457)). A small dataset.
- 2026-11-22: each subagent spends its own tokens, and the savings reported in the talks come from vendors and rarely compare answer quality, so the cost side stays unmeasured unless you record it ([limits and cost unmeasured](../docs/classes/limits-and-cost-unmeasured.md)).

## Guards

- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
- [limits-and-cost-unmeasured](../docs/classes/limits-and-cost-unmeasured.md)
