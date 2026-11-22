---
kind: habit
why: A skill or prompt rule that hurts does not fail, it quietly makes output worse, and rules written around an older model keep costing after the model stops needing them.
applies_when: your AI coding agent loads skills, rules files or prompt instructions that you wrote or generated, and you change models from time to time
last_reviewed: 2026-11-22
---

# Test each skill with and without it, and prune what the model no longer needs

## Check

For each skill or long rules file, look for a run of the same tasks with it and without it,
repeated a few times. When you last changed models, did you rerun those and remove anything?
Read the rules for pairs that contradict each other. Take your longest skill and mark which
lines restate general knowledge or the docs, and which carry exact facts (names, values, steps)
the model could not know; the first kind is the candidate for cutting, and a restated doc is a
second copy that drifts from the first.

## Learn

- [How I deleted 95% of my agent skills and got better results (WorkOS), 8:26](https://www.youtube.com/watch?v=vy7o1g2iHY8&t=506): a measured case where a skill lowered accuracy, and the short list of gotchas that replaced it.
- [Don't ship skills without evals, 11:51](https://www.youtube.com/watch?v=0vphxNt4wyk&t=711): ablation with and without a skill over repeated runs, trigger tests, and when to retire a skill.
- [Your SKILL.md is 70% stuff the model already knows (Intel), 6:54](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=414): quizzing the model on each claim in a skill, without the skill, to find what it already knows.
- [Your old prompts are making Claude worse (Anthropic), 1:58](https://www.youtube.com/watch?v=ys6YQ2yfBpM&t=118): the measured cost of stale and contradictory instructions on a newer model, and an audit procedure.

## Evidence for

- 2026-11-22: in the WorkOS talk a task was solved correctly 77% of the time with a skill and 97% without it; replacing over 10,000 generated lines with a few hundred lines of gotchas cut the eval run from 68 to 6 minutes. The speaker's own measurement.
- 2026-11-22: the Intel talk found about 70% of a first skill was already known to the model; models knew about 70% of general ideas but only about 22% of exact details, so the general parts are the ones to cut. Own sets, no outside replication.
- 2026-11-22: in the Anthropic talk, telling the model to verify twice added 48% to cost per ticket with no accuracy gain, telling it to be as thorough as possible multiplied needless tool calls, and two contradictory rules cost 9 points of accuracy. One ticket benchmark.
- 2026-11-22: a harness workaround for one model's weakness turned out unnecessary on the next ([Decoupling the brain from the hands: Claude Managed Agents (Anthropic), 1:58](https://www.youtube.com/watch?v=Uv0nAf_7tyU&t=118)). A case.
- 2026-11-22: [Is the agent harness dead? (SpaceXAI), 4:43](https://www.youtube.com/watch?v=7Y4sbZgBdnc&t=283) argues that harness workarounds get absorbed into newer models, and logs each workaround when it fires so that one which stops firing can be removed. An argument citing outside benchmarks, retold.

## Evidence against

- 2026-11-22: ablation needs a task set and repeated runs per skill; every number above is from the speakers' own sets.
- 2026-11-22: rules that encode your own conventions, permissions or guardrails are not something a model grows into; the talks keep those and protect them with evals, so pruning applies to skills that teach a missing capability.
- 2026-11-22: what a frontier model no longer needs can still help a smaller one: the same model scored from 52.4% to 76.2% on one benchmark by harness alone, with larger gains for weaker models ([What if the harness mattered more than the model? (Etsy), 0:01](https://www.youtube.com/watch?v=2e9ANoOEn28&t=1)). A rule removed for one model may have to come back for another.

## Guards

- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
- [copies-of-one-truth-drift](../docs/classes/copies-of-one-truth-drift.md)
