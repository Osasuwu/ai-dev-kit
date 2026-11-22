---
kind: belief
why: An agent is reliable on work whose result a program can check, and on work without such a check it turns out confident output that nobody can tell right from wrong.
applies_when: you decide which tasks to hand to an agent, or how far to trust its output on a kind of task
last_reviewed: 2026-11-22
---

# Agents are reliable where the result can be checked

## Check

List the kinds of task you give agents. For each, name the check that tells right from wrong
without anyone's opinion: a test, a compiler, a type checker, a comparison with known output,
the state of the target system. Where the honest answer is "a model judges it" or "nobody",
mark the kind. Then sort the agent mistakes you have recorded by kind; if the belief holds for
you, they gather in the marked kinds. For the kinds with a check, ask whether the check can
fail: a test that cannot go red is no check at all.

## Learn

- [State of Data, 6:22](https://www.youtube.com/watch?v=ZyIoTOAbRfs&t=382): three ways to rate how checkable a task is: how easily it splits into checkable steps, whether people agree on what correct means, and how often the world supplies fresh checked examples.
- [Perception Agents (Amazon AGI Lab), 5:29](https://www.youtube.com/watch?v=2JX6JYyQG4Y&t=329): why code was the first field where agents became dependable, and where checking runs into a wall.
- [Jev CEO: I made ChatGPT, now I'm building what's next, 7:19](https://www.youtube.com/watch?v=cJ0EOzey--o&t=439): why a reward built on human preference teaches a model to sound right rather than be right.
- [Reinforcement Learning without Verifiable Rewards (Prime Intellect), 5:50](https://www.youtube.com/watch?v=AQv3qRCG6Gw&t=350): what reward hacking looks like when the reward is a loose stand-in for the goal.

## Evidence for

- 2026-11-22: the State of Data and Perception Agents talks argue that code got ahead because its result can be run, tested and compiled, which gives the agent a signal while it works and training a reward that a confident tone cannot fool. Expert argument; the benchmarks one speaker leans on are private and the method is not given.
- 2026-11-22: the Jev talk explains the other side: a preference-based reward model punishes visible uncertainty more easily than a confident error. An argument, not a measurement.
- 2026-11-22: without an outside check, models judge poorly: on reasoning tasks they struggled to correct themselves without external feedback, and judges of agent success stayed near chance on one benchmark (in [LLM as the measuring instrument](../docs/classes/llm-as-measuring-instrument.md) and [claims from plausibility](../docs/classes/claims-from-plausibility.md)). Measured.

## Evidence against

- 2026-11-22: a check that exists is not a check that works. On SWE-bench Verified the benchmark's own validation counted 7.8% of patches correct while they failed the developers' tests, and 29.6% of plausible patches behaved differently from the reference fix ([tests that cannot fail](../docs/classes/tests-that-cannot-fail.md)). Reliability follows how strong the check is, not whether one exists.
- 2026-11-22: a checkable task is also one the agent can aim at the check instead of the goal: agents cheated on tests that contradicted the specification in up to 76% of runs on one benchmark variant ([proxy optimisation](../docs/classes/proxy-optimisation.md)).
- 2026-11-22: the Perception Agents talk says plainly that nobody has yet made open-ended knowledge work checkable this way, so the remedy of turning fuzzy tasks into checkable ones is untested there.

## Guards

- [llm-as-measuring-instrument](../docs/classes/llm-as-measuring-instrument.md)
- [tests-that-cannot-fail](../docs/classes/tests-that-cannot-fail.md)
