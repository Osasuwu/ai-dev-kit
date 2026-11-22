---
kind: habit
why: An agent given broad authority from the start, or promoted because fewer of its outputs get corrected, can do damage in exactly the places review has stopped looking.
applies_when: you decide what an AI agent may do without a person approving each step, such as merging, closing, deploying or changing data
last_reviewed: 2026-11-22
---

# Widen the agent's autonomy in stages, on its measured record per kind of action

## Check

List the kinds of action the agent takes and write the stage each one is at: shadow, draft a
person approves line by line, exceptions plus a random sample of the clean ones, or exceptions
only. Next to each, write what moved it there. If the answer is a feeling, or only a falling
rate of corrections, the stage was not earned. Then look for an independent sample of the work
the agent marked clean, and for a rule that sends an action back a stage when the model, the
prompt or a data source changes.

## Learn

- [The agent works. Does anyone trust it? (Leading at Scale), 10:13](https://www.youtube.com/watch?v=-a2oTS9J67U&t=613): four stages from shadow to exceptions only, and why a falling override rate can mean the review got shallower.
- [60% of our data PRs now merge with no human review (Robinhood), 3:58](https://www.youtube.com/watch?v=MQiojLnK-E0&t=238): scripts check the facts, an agent judges the remaining risk, and people keep the protected decisions.
- [Deploying AI inside a bank is not an engineering problem (Applied AI Engineers), 8:07](https://www.youtube.com/watch?v=3ZlQk4-knWM&t=487): starting from the least authority that is still useful, and promotion on observed errors.
- [Give your on-call its own AI teammate (Meta), 4:21](https://www.youtube.com/watch?v=_NBx2NNOuA4&t=261): an autonomy ladder per action rather than per agent.

## Evidence for

- 2026-11-22: Robinhood reports that 60% of its data pull requests merge without a person, behind deterministic checks against a source of truth that block on red, and an agent told what those checks already cover. It flags risky changes and never clears them, and counts false escalations alongside misses. Measured at one company, by that company.
- 2026-11-22: in the Meta talk an action moves up only when its errors are cheap, tests, CI or review catch them, and the agent has a record on that action. A case, no numbers on outcomes.
- 2026-11-22: the Leading at Scale talk treats any change of prompt, model or source as a trigger to revalidate, with a kill switch runbook. A framework from practice, not a measurement.

## Evidence against

- 2026-11-22: at the exceptions-only stage the weak spot is what the agent did not flag, and only an independent sample tells a better agent from a lazier review. That sample costs a person's time for as long as the stage lasts.
- 2026-11-22: approval is only a control when the approver can check the work and does not share the expectation the failure exploits; in the bank error behind [What a $900M bank error teaches us about AI agents (Two Sigma), 3:44](https://www.youtube.com/watch?v=iniryju23Sk&t=224), three approvers overrode a warning. A promotion that rests on such approvals rests on little.
- 2026-11-22: a record does not cover an action that cannot be undone; one mistake there outweighs any number of clean runs, which is why [irreversible effects](../docs/classes/irreversible-effects.md) keeps such actions behind a stop and a person.

## Guards

- [irreversible-effects](../docs/classes/irreversible-effects.md)
- [scope-overreach](../docs/classes/scope-overreach.md)
