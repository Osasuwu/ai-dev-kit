---
kind: habit
why: An agent left to run for hours with no checkable end condition and no budget stops when it believes it is done, or runs on, and afterwards nobody can tell which.
applies_when: you hand an agent a task that runs for hours or unattended, rather than one you watch step by step
last_reviewed: 2026-11-22
---

# Give a long agent task a checkable goal, a budget and checkpoints against the goal

## Check

Open the brief of your last long or unattended agent run. It should state three things before
the work starts: done as a condition someone other than the agent can check (a named test turns
green, a scanner reports nothing), a budget in tokens, time or money, and the points where the
run's progress is compared with the goal it started from. Then look at how the run ended. It
should be one of: the condition was met and checked, the budget ran out, or the agent asked for
help, and you were told in each case, success included. A run that ended because the agent said
it was finished fails, and so does a brief whose done line describes steps instead of an
outcome.

## Learn

- [Cooking with Codex (OpenAI), 31:57](https://www.youtube.com/watch?v=FwiS44-xyYw&t=1917): a multi-hour task driven by a goals file and a progress page, with separate threads at milestones that review the code and audit whether the main thread has drifted from its goals.
- [Harness engineering: how to build software when humans steer, agents execute (OpenAI), 43:21](https://www.youtube.com/watch?v=am_oeAoUhew&t=2601): steering agents by a budget, priorities and success measures instead of step-by-step instructions, and what had to be built for that.
- [Lifestyles of the AI-native (WorkOS), 56:59](https://www.youtube.com/watch?v=AgBAOXVxt4A&t=3419): the difference between a goal that stops when done and a loop that repeats on a schedule, and when the agent should call a person.

## Evidence for

- 2026-11-22: the Codex workshop demonstrates a seven-hour task kept on course by a goals file and milestone audits run in separate threads ([Cooking with Codex](https://www.youtube.com/watch?v=FwiS44-xyYw&t=1917)). A vendor's workshop demo, not a measurement.
- 2026-11-22: the WorkOS talk advises scheduling only work whose done is already written down, notifying when a fix is ready or the agent needs help, and treating each question the agent asks a person as a defect in the loop ([Lifestyles of the AI-native](https://www.youtube.com/watch?v=AgBAOXVxt4A&t=3419)). Practitioner advice.
- 2026-11-22: [done is not the effect](../docs/classes/done-is-not-the-effect.md) records agents that reported done with every step real and the outcome missing; its first protection is writing the effect into the criterion and asking for evidence of it.
- 2026-11-22: [limits and cost unmeasured](../docs/classes/limits-and-cost-unmeasured.md) records agent runs stopped by a cap that nobody had measured, one of them after the work had already succeeded and another before it posted its result; it recommends that a run which hits its limit ends with a stop reason of its own.

## Evidence against

- 2026-11-22: all three talks are demos and the experience of vendor teams; none measures whether runs with a goal file finish more often or cost less.
- 2026-11-22: a budget set by guess is as unhelpful as none: [limits and cost unmeasured](../docs/classes/limits-and-cost-unmeasured.md) records caps set from a single run that cut off work that was going well, and recommends setting the value from runs that succeeded.
- 2026-11-22: a done condition the agent can check is one it can also bend until it passes, by editing the test or narrowing the criterion ([proxy optimisation](../docs/classes/proxy-optimisation.md)); the condition helps only if the agent cannot change it.
- 2026-11-22: asking for evidence is not checking it: in an incident in [done is not the effect](../docs/classes/done-is-not-the-effect.md), the agent said both modes were reachable while one had no caller.

## Guards

- [limits-and-cost-unmeasured](../docs/classes/limits-and-cost-unmeasured.md)
- [done-is-not-the-effect](../docs/classes/done-is-not-the-effect.md)
