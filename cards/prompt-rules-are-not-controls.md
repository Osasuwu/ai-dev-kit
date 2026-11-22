---
kind: belief
why: A rule given to an agent only in its prompt or rules file is followed most of the time and broken when the task, a long session or an attacker pushes against it, and nothing stops the action.
applies_when: you rely on instructions in a prompt, a rules file or a skill to keep an agent from doing something costly
last_reviewed: 2026-11-22
---

# A rule in the prompt is not a control

## Check

List the rules in your rules files, prompts and skills whose breach would cost something hard
to undo: a push, a merge, a deploy, a delete, a secret leaving. For each, name what stops the
action if the agent ignores the sentence: a hook, a permission, a required check, a platform
setting, a sandbox. A rule for which the answer is "nothing" is a request. Then search your
session logs for a time the agent broke one of them, and note whether the session was long or
had been compacted when it did.

## Learn

- [We let an AI agent execute Bash and lived to talk about it (PostHog), 9:17](https://www.youtube.com/watch?v=4lXks428C9o&t=557): why detection and blocking stay deterministic and the model is only allowed to triage afterwards.
- [Build a Platform and Watch It Burn (Accenture, Datadog), 41:52](https://www.youtube.com/watch?v=1tpqdglI3T0&t=2512): a live attack on an agent in a platform workshop, and how far the presenters trust the model's own refusals.
- [Claude Code memory](https://code.claude.com/docs/en/memory): the vendor's own statement that rules files are context for the model, not enforced configuration.

## Evidence for

- 2026-11-22: on the IFScale benchmark the best frontier models reached 68% accuracy at 500 instructions, favouring earlier ones ([arXiv 2507.11538](https://arxiv.org/abs/2507.11538)). Measured, on general instruction following.
- 2026-11-22: rules that tell a coding agent to refuse or hand a step to a person were followed in 0% of runs across four models, and agents opened a policy file that was not loaded for them in 12 of 347 runs ([arXiv 2607.26819](https://arxiv.org/html/2607.26819v1)). Measured.
- 2026-11-22: in the Accenture and Datadog workshop the model's refusals were inconsistent, a framing story got an outside image deployed, and an admission policy in the cluster was what blocked it. A case, not a measurement.
- 2026-11-22: in one operator's audit cited in [knowledge not at the point of action](../docs/classes/knowledge-not-at-point-of-action.md), fixes that stayed in prose recurred in 3 of 3 cases and fixes put into something executed did not recur in 3 of 3. Private and small.

## Evidence against

- 2026-11-22: rules files are mostly followed: a study of repository context files found their instructions well followed, even though the files did not raise task success ([arXiv 2602.11988](https://arxiv.org/abs/2602.11988)). For a cheap, reversible action a prompt rule may be all that is worth paying for.
- 2026-11-22: deterministic controls fail too. [Pattern-matched boundaries](../docs/classes/pattern-matched-boundaries.md) records hooks and deny lists passed by spellings they did not anticipate, and harmless work blocked by false matches.
- 2026-11-22: the prompt still shapes what the agent tries, which the same class doc lists as its first rung; it lowers how often a control has to fire, even though it is not one.

## Guards

- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
- [pattern-matched-boundaries](../docs/classes/pattern-matched-boundaries.md)
