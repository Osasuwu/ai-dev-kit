---
kind: habit
why: A green build and passing unit tests do not show that the feature works for whoever uses it, and an agent that never runs the app reports done on that evidence alone.
applies_when: an agent changes an app or service that people or other programs use, and you accept its report that the work is done
last_reviewed: 2026-11-22
---

# Have the agent use the running app before it calls the work done

## Check

Open the agent's log or report for its last finished change. It should name a run of the app:
how it started it, what it did there as a user would, and what it saw. A report that cites only
the build, the unit tests and the type checker fails this check. Then ask whether the whole stack
starts with one command in the agent's sandbox; if it does not, the agent cannot do this step
even when told to.

## Learn

- [Your agent is blindfolded, 2:12](https://www.youtube.com/watch?v=iRcX54EO5g8&t=132): why an agent that cannot see the running app cannot tell a working feature from a broken one.
- [Teach your agent to prove it's done (WorkOS), 20:51](https://www.youtube.com/watch?v=q4WC4TowkBo&t=1251): proof of done in two layers, a deterministic check and a model judge on top.
- [Teach your agent to prove it's done (WorkOS), 46:10](https://www.youtube.com/watch?v=q4WC4TowkBo&t=2770): why a proof goes stale once later changes land, and has to be redone.
- [How to build an AI code review agent (Greptile), 13:34](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=814): what an agent needs to test a change by using it: a sandbox, written scenarios, a one-command start.

## Evidence for

- 2026-11-22: several talks at AI Engineer events describe agents that reported features done on unit tests while the app was broken, and the fix of giving the agent the app or a browser to drive. These are cases and practitioners' experience; none gives a controlled measurement.
- 2026-11-22: the incidents behind [done is not the effect](../docs/classes/done-is-not-the-effect.md) include changes that passed their tests and did nothing where the effect should land.
- 2026-11-22: Anthropic's write-up on harnesses for long-running agents reports that its agent tended to mark features complete without testing them end to end, and built the harness around stopping that ([Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).

## Evidence against

- 2026-11-22: it costs a sandbox with every dependency, a one-command start of the whole stack, and user scenarios written down (the Greptile review-agent talk above); an app that needs a database, secrets or a graphical session to start is where the agent's run gets unreliable ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- 2026-11-22: the run can differ from what ships: an agent testing its own change switched off a feature flag to reach the page and turned it back on before pushing ([Cursor](https://cursor.com/blog/agent-computer-use)).
- 2026-11-22: when the effect lands where the agent cannot run anything, such as a phone after the app is closed or a robot, this habit cannot be kept and a live probe has to replace it.

## Guards

- [done-is-not-the-effect](../docs/classes/done-is-not-the-effect.md)
- [tests-that-cannot-fail](../docs/classes/tests-that-cannot-fail.md)
