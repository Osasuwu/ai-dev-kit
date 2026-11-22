---
kind: habit
why: An agent handed a short or ambiguous request fills the gaps with its own guesses and builds on them, and the mismatch shows only when the work comes back.
applies_when: you hand an AI coding agent a feature or change described in a few sentences, before any spec or acceptance criteria exist
last_reviewed: 2026-11-22
---

# Have the agent interview you before it writes code

## Check

Take your last few tasks that started from a short request. Did the agent ask you questions
before it planned or edited, and did your answers end up in a written spec or issue that the
work was then held to? Count the review rounds in which you corrected what was built rather than
how it was built: each one is a question nobody asked up front. If the agent's first reply to a
request is usually a plan or a diff, the habit is not in place.

## Learn

- [Your spec has bugs. Catch them before your agent codes. (AWS), 4:17](https://www.youtube.com/watch?v=0EnLxIbAvYk&t=257): a mechanical hunt for ambiguous and contradictory requirements, run before the agent writes code.
- [How forward deployed engineering is done at Ramp, 7:33](https://www.youtube.com/watch?v=ITMXwI6QL6A&t=453): an agent that asks scoping questions about each incoming request before any work starts.
- [One developer, two dozen agents, zero alignment: why we need collaborative AI engineering, 3:28](https://www.youtube.com/watch?v=ClWD8OEYgp8&t=208): why agreement on what to build slid from before the code to the pull request.
- [Spec Kit clarify step](https://github.com/github/spec-kit/blob/main/templates/commands/clarify.md): a ready-made prompt that asks the author about gaps before planning, with a cap on the number of questions.

## Evidence for

- 2026-11-22: on underspecified tasks, models tend to carry on without asking unless they are told to ask ([Vijayvargiya et al.](https://arxiv.org/html/2502.13069v3), cited in [spec not grounded in current state](../docs/classes/spec-not-grounded-in-current-state.md)). A research measurement, not a field report.
- 2026-11-22: the AWS talk above reports a 20–40% drop in first-attempt success when prompts are unclear. The figure is the speaker's; the method was not checked here.
- 2026-11-22: tools now build the step in: Spec Kit's clarify step, and plan modes in Codex and VS Code that ask clarifying questions before proposing a plan (sources in the [class doc](../docs/classes/spec-not-grounded-in-current-state.md), rungs "Spec pass" and "Plan mode").
- 2026-11-22: the Ramp talk describes scoping every request with an agent's questions before work as standard practice. A practitioner's case, no measurement.

## Evidence against

- 2026-11-22: the interview reads your answers, not the repository. A premise that is stated clearly and is false against the current code passes it; the class doc's spec pass breaks the same way, and only a pass that reads the repository catches it ([spec not grounded in current state](../docs/classes/spec-not-grounded-in-current-state.md)).
- 2026-11-22: it costs your time on every task, and on a small change a long interview costs more than the rework it saves. Spec Kit caps its clarify step at five questions per session, a sign the cost is known.
- 2026-11-22: in an unattended run nobody answers. The class doc records a run that stopped on a question, got its answer as a comment, and stopped again on the next run.
- 2026-11-22: the talks offer cases and demos; no controlled comparison of interviewed and not interviewed tasks was found.

## Guards

- [spec-not-grounded-in-current-state](../docs/classes/spec-not-grounded-in-current-state.md)
