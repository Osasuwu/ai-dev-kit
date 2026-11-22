---
kind: belief
why: A static allow or deny list sees how a command is spelled, not whether the action still serves the session's task, so drift and slow injection pass it.
applies_when: you guard an agent's tool calls with permission lists or pattern rules and are weighing a model that judges each call in context
last_reviewed: 2026-11-22
---

# Judging each action against the task catches what a static list cannot, but does not replace a deny

## Check

Take your guard's log for a recent week. For each action it stopped, note whether it was
stopped for how the command was spelled or for what it did against the task. Then replay two
kinds of case in a throwaway session: known bypass spellings of a denied command, and an action
that is harmless in form but off-task (an agent sent to investigate an incident that starts
reading mail). See which layer stops each. Last, list the actions you could not undo and check
that a deterministic deny sits under any judging model for them.

## Learn

- [300 agents, 60 people: how we secured our own AI agents (Runlayer), 7:42](https://www.youtube.com/watch?v=BgLdvF7Qkh8&t=462): why drift shows only across a whole session, and a classifier that reads the session before each tool call.
- [Unlock agent autonomy: the runtime for AI-native systems, 8:13](https://www.youtube.com/watch?v=zaGyGgLW3SM&t=493): access granted by the task's intent, with a worked example, and the admission that it is not solved yet.
- [Stop making your customers click approve (Wise), 4:05](https://www.youtube.com/watch?v=V2UqEUA8NjM&t=245): the counterpoint, where "looks safe" is the wrong question for an action that needs authorisation.

## Evidence for

- 2026-11-22: a company running about 300 agents for 60 people logged every session and tool call and found that attacks and mistakes unfold over a whole session: an agent approves a pull request after losing track of a constraint, or an injection lands on a later attempt. Their answer was a classifier that judges each call against what the agent is for (the Runlayer talk). A case study; no precision or recall published.
- 2026-11-22: static lists keep being bypassed by spelling: one agent vendor published 13 advisories in seven months on bypassed command, path or domain rules, and a survey found ten of eleven open-source agents' command guards exploitable ([pattern-matched boundaries](../docs/classes/pattern-matched-boundaries.md)).
- 2026-11-22: a talk on intent-based access argues that reading the incident channel fits a task "investigate an incident" and a sudden request for mail does not, a distinction no command list can draw (the runtime talk above). A prototype, not a deployed result.

## Evidence against

- 2026-11-22: the claim is contested: the sources agree that spelling-based lists miss drift, and disagree on whether a judging model is the answer and where it must not be used.
- 2026-11-22: a judging model answers whether an action looks safe; for a payment the question is whether the customer authorised this exact payment on these terms, so Wise uses a fixed agreement for the task instead of a classifier (the Wise talk). For actions that need authorisation, the classifier is the wrong instrument.
- 2026-11-22: a vendor's own measurement of its per-action classifier let through 17% of overeager actions in a test set of 52, and the vendor says it does not replace careful human review on high-stakes infrastructure ([irreversible effects](../docs/classes/irreversible-effects.md)).
- 2026-11-22: it costs a model call per action, blocks some harmless ones, and none of the talks publishes how often it is right; the class doc treats it as one rung added to deterministic ones, not a replacement ([pattern-matched boundaries](../docs/classes/pattern-matched-boundaries.md)).

## Guards

- [pattern-matched-boundaries](../docs/classes/pattern-matched-boundaries.md)
