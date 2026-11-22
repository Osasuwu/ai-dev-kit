---
kind: habit
why: The same agent mistakes recur because what one session learned stays in its transcript and never reaches what the next session reads.
applies_when: you run an AI coding agent over many sessions, keep its transcripts or traces, and give it rules files, skills or memory it loads
last_reviewed: 2026-11-22
---

# Mine the agent's sessions for lessons, write them back, and measure whether each helped

## Check

Pick a mistake you corrected more than once in the last month. Is there a rule, skill, memory
entry or check that came from it, and did the mistake stop after that date? Then look at how
lessons are found: is there a regular pass over transcripts for the places the agent got stuck,
was asked the same thing twice, or had its edit reverted, or do lessons enter only when someone
remembers one? For each change written back, name the measure that should move and whether it
did.

## Learn

- [Giving AI agents memory that learns (LangChain), 7:45](https://www.youtube.com/watch?v=KGFyOtl5ktI&t=465): why a trace becomes memory only after a filter picks the signal and writes it back.
- [Your AI agent is hiding its mistakes from you (Warp), 1:42](https://www.youtube.com/watch?v=pz74r-4dGfQ&t=102): a nightly pass that grades conversations against a rubric, proposes skill edits, and matches score changes to the dates the edits merged.
- [How Lovable self-improves every hour, 5:17](https://www.youtube.com/watch?v=KA5kPbdkK2E&t=317): implicit signals that a session got stuck, and ranking fixes by project success instead of complaint count.
- [Claude for long-horizon tasks, 10:27](https://www.youtube.com/watch?v=9QebvrrY3KY&t=627): an offline pass over transcripts that corrects what the agent wrote into memory during the work.

## Evidence for

- 2026-11-22: the Warp talk ties breaks in the conversation score to the merge dates of skill edits, so a change has a visible effect. A case presented as a product pitch.
- 2026-11-22: in the Claude for long-horizon tasks talk, a wrong memory made the agent fail in 5 of 5 repeats until an offline pass over its sessions corrected it. Small and controlled, one task.
- 2026-11-22: turning a user's corrections into rules plus runtime checks, instead of storing them as memory, gave fewer violations than a memory baseline ([TRACE](https://arxiv.org/abs/2606.13174v1), cited in [knowledge not at point of action](../docs/classes/knowledge-not-at-point-of-action.md)). A research measurement.
- 2026-11-22: in [Hill-climbing skills: improve agents without changing the model (Browserbase), 8:15](https://www.youtube.com/watch?v=p7gaxmCUiIU&t=495), a teacher agent reading traces found a shortcut that cut a task's cost from about $12 to about $3; the next iteration then failed. A pitch, and an honest example of uneven gains.

## Evidence against

- 2026-11-22: without a before-and-after measure the loop collects rules, not quality. Each learned edit is one more rule, and contradictory rules cost accuracy (see the measurements in [Your old prompts are making Claude worse (Anthropic), 1:58](https://www.youtube.com/watch?v=ys6YQ2yfBpM&t=118)).
- 2026-11-22: the background pass can write its own errors, which is why the talks have a person read its report or review each skill edit before it takes effect.
- 2026-11-22: lessons go stale with each new model and feature; the Lovable talk throws collected context away on a schedule.
- 2026-11-22: a lesson that cannot be checked mechanically stays a prose rule, and when nobody routes it, it gets recorded again instead: five times for one lesson in [knowledge not at point of action](../docs/classes/knowledge-not-at-point-of-action.md).

## Guards

- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
