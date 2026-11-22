---
kind: habit
why: A review comment that keeps coming back is knowledge the agent never keeps, and a model reviewer told to remember it catches it only some of the time.
applies_when: an agent writes code that people or a model reviewer comment on, and the same comment turns up on more than one pull request
last_reviewed: 2026-11-22
---

# Turn each repeated review comment into a rule a tool enforces

## Check

Collect the review comments on your last twenty or so merged pull requests, from people and from
any review bot, and group them by what they ask for. For every group that appears three times or
more, look for the lint rule, test or script that would now catch it; a repeated comment with
nothing behind it fails. Then read your model reviewer's instructions. Each item there should be
a judgement a rule cannot express, such as whether error handling is needlessly defensive; an item a
linter could check is in the wrong place. If the reviewer reports which rule produced each
finding, look at how often each rule's findings get fixed: a rule whose findings are always
dismissed is noise.

## Learn

- [Stop prompting (Sentry), 4:26](https://www.youtube.com/watch?v=E3KbFLAGD6A&t=266): why agents made custom lint rules cheap enough to write for one repeated comment, and where the candidates come from.
- [Stop prompting (Sentry), 12:03](https://www.youtube.com/watch?v=E3KbFLAGD6A&t=723): the line between a rule and a policy left to a model reviewer, with one reviewer subagent per policy.
- [Harness engineering: how to build software when humans steer, agents execute (OpenAI), 36:13](https://www.youtube.com/watch?v=am_oeAoUhew&t=2173): a weekly cleanup that removes noticed slop as a category and feeds it back into docs, a failing test or a reviewer agent.
- [How to kill the code review, 7:02](https://www.youtube.com/watch?v=YgEv7IQzGdM&t=422): the principle in short form, and a register of repeated review findings.
- [Building uReview, Uber's multi-agent code review engine (Uber), 3:37](https://www.youtube.com/watch?v=EL123UNokkI&t=217): team standards run as reviewer policies at scale, with each policy judged by whether developers act on its comments.

## Evidence for

- 2026-11-22: Sentry describes running this loop: scheduled passes over session transcripts and review threads to find rule candidates, lint rules for what can be checked, and per-policy reviewer subagents for the rest ([Stop prompting](https://www.youtube.com/watch?v=E3KbFLAGD6A&t=266)). A practitioner's case; the effect is not measured.
- 2026-11-22: an OpenAI team where agents write the code reports the same flow run by people each week ([Harness engineering](https://www.youtube.com/watch?v=am_oeAoUhew&t=2173)). A practitioner's case, no measurement.
- 2026-11-22: Uber's review engine routes comments by team policy and reports that about two thirds of its comments get fixed, and tracks that per rule ([uReview](https://www.youtube.com/watch?v=EL123UNokkI&t=217)). Measured on the company's own system.
- 2026-11-22: [knowledge not at the point of action](../docs/classes/knowledge-not-at-point-of-action.md) cites a study that turned a user's corrections into rules plus runtime checks and saw fewer violations than storing them as memory, and an incident where one lesson was written down five times without ever reaching a check.

## Evidence against

- 2026-11-22: every rule is one more check with its own false positives and upkeep; the talks above do not count that cost or measure how much the rules help.
- 2026-11-22: many review comments are judgements no rule can express; those stay with a model reviewer or a person, and a model reviewer is an uncertain instrument ([LLM as measuring instrument](../docs/classes/llm-as-measuring-instrument.md)).
- 2026-11-22: someone has to do the routing from comment to rule; when nobody does, the lesson is recorded again instead ([knowledge not at the point of action](../docs/classes/knowledge-not-at-point-of-action.md)).

## Guards

- [llm-as-measuring-instrument](../docs/classes/llm-as-measuring-instrument.md)
- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
