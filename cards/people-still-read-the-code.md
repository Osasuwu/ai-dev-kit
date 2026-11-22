---
kind: belief
why: When every change goes through the same light approval, a person signs off on decisions they never saw, and plausible code with the wrong content merges.
applies_when: agents write most of your changes and a person approves them, or you are deciding which changes a person still has to read
last_reviewed: 2026-11-22
---

# Some changes still need a person to read the code

## Check

Take the changes a person approved in the last month. For each, ask the approver to name the
decision they made: a database migration, a permission change, a new dependency, a changed
limit. Count the approvals that named none, and the approvals that ever led to a change being
sent back. Then sort the problems found after merge by kind: a kind that keeps recurring belongs
in a lint rule, a doc or an automated reviewer; a kind that is new or costly is where a person
has to read. If people read everything equally, or nothing, the routing is missing.

## Learn

- [The friction is your judgment, 14:28](https://www.youtube.com/watch?v=_Zcw_sVF6hU&t=868): a review step that splits findings into mechanical ones the agent fixes and explicit calls a person must make.
- [The friction is your judgment, 17:32](https://www.youtube.com/watch?v=_Zcw_sVF6hU&t=1052): why removing all friction hands judgment to the agent along with the typing.
- [The Z/L continuum: should AI engineers still read code?, 11:53](https://www.youtube.com/watch?v=ZpK5PWX2YRM&t=713): the read-every-line and fix-the-system positions recast as a choice made per task, not per person.
- [I let agents refactor my codebase for 3 weeks. Then I read the code (Microsoft), 4:35](https://www.youtube.com/watch?v=6TjFjHPjVH0&t=275): what reading the code found after weeks of approving plans.

## Evidence for

- 2026-11-22: a practitioner approved an agent's refactoring plans for three weeks, then read the result and found constructs with the right names and the wrong content, such as a "skill" with none of the files a skill needs (the Microsoft talk above). One case, told by its author; not a measurement.
- 2026-11-22: the talk The friction is your judgment argues that review exists to make someone stop and decide, and gives a working split: bugs and rule breaches go back to the agent, while migrations, permission changes and new dependencies are put to a person. An argument with a mechanism, not a measurement.
- 2026-11-22: [gate checks a proxy](../docs/classes/gate-checks-a-proxy.md) records gates that counted an approval that existed without an independent person having read the change, and notes that GitHub now lets a model's approval count toward required approvals (off by default).

## Evidence against

- 2026-11-22: the opposite practice, in a team where agents write the code, sends attention to the system instead of the diff: each recurring class of mistake becomes a document, a test or an automated reviewer ([Harness engineering: how to build software when humans steer, agents execute (OpenAI), 36:13](https://www.youtube.com/watch?v=am_oeAoUhew&t=2173)). On recurring mistakes it is the better use of a person's time.
- 2026-11-22: no talk in the cluster measures how often a person's reading catches what the automated checks missed; every source is experience or a single case.
- 2026-11-22: reading costs the reader's time on every routed change, and an approval given by reflex costs it without the benefit; [LLM as the measuring instrument](../docs/classes/llm-as-measuring-instrument.md) argues for the model to advise while deterministic checks and a person decide, which assumes the person does decide.

## Guards

- [gate-checks-a-proxy](../docs/classes/gate-checks-a-proxy.md)
- [llm-as-measuring-instrument](../docs/classes/llm-as-measuring-instrument.md)
