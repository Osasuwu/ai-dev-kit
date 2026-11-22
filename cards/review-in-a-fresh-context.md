---
kind: habit
why: An agent that checks its own work in the context where it did the work sees its own reasoning and tends to confirm it, so the check finds little.
applies_when: an AI coding agent's work is checked by a model, the same agent or another one, before you accept it
last_reviewed: 2026-11-22
---

# Review the agent's work in a fresh context, against criteria written before the code

## Check

For your last few accepted changes, look at who reviewed them. Was it the session that wrote
the code, asked to look over its work, or a separate session that got only the task, the
criteria and the diff? Did the reviewer see the author's conversation? Was its rubric written
before the code or made up while reviewing? Did it run anything, or only read? Over a month,
count how often the separate reviewer found something the author's own check had passed.

## Learn

- [The multi-agent architecture that actually ships (Factory), 4:27](https://www.youtube.com/watch?v=ow1we5PzK-o&t=267): a validation contract written before the code, and validators that never saw the implementation.
- [Claude for long-horizon tasks, 5:08](https://www.youtube.com/watch?v=9QebvrrY3KY&t=308): a build-then-verify loop with the grader kept apart from the generator, and why grading in the same context drifts.
- [How to build an AI code review agent (Greptile), 7:34](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=454): a set of pull requests that caused incidents, used to measure what a reviewer from another model family catches.
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices): the built-in review that runs in a subagent which never saw the conversation.

## Evidence for

- 2026-11-22: Anthropic's prompting guide says separate, fresh-context verifier subagents tend to do better than self-critique ([Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5), cited in [claims from plausibility](../docs/classes/claims-from-plausibility.md)). Vendor guidance.
- 2026-11-22: in the Factory talk's case study, validation never passed on the first try, and about half of the final lines were tests. One case, no comparison group.
- 2026-11-22: Greptile reports about 10% more defects caught when the reviewer comes from another model family, measured on its own set of incident pull requests. Vendor data; the protocol is not published.
- 2026-11-22: a model judging its own output prefers it, more so the better it recognises its own text ([Panickssery et al.](https://arxiv.org/abs/2404.13076), cited in [LLM as measuring instrument](../docs/classes/llm-as-measuring-instrument.md)).

## Evidence against

- 2026-11-22: each review round is another run, in latency and tokens.
- 2026-11-22: a fresh reviewer that only reads judges on plausibility again, and one asked to find problems will report something whether or not it is there ([claims from plausibility](../docs/classes/claims-from-plausibility.md), rung "Review: verify in a fresh context, with tools").
- 2026-11-22: without a rubric fixed in advance, an independent reviewer reproduces the author's preferences. A fresh context removes the conversation, not the blind spots of the same model family; the debiasing studies measured chat judges, not code review ([LLM as measuring instrument](../docs/classes/llm-as-measuring-instrument.md)).

## Guards

- [claims-from-plausibility](../docs/classes/claims-from-plausibility.md)
- [llm-as-measuring-instrument](../docs/classes/llm-as-measuring-instrument.md)
