---
kind: habit
why: Decisions agreed in a conversation with the agent or in the ticket never become written criteria, so review catches broken code but not code that does the wrong thing.
applies_when: you agree with an agent or a teammate what a change should do, and an agent then writes the pull request you review
last_reviewed: 2026-11-22
---

# Write the agreed intent as criteria, and check the pull request against each one

## Check

Open a recently merged agent pull request and its issue. Are the acceptance criteria written
down, and do they include the decisions made while talking the task through, not only the
ticket's first draft? For each criterion, point to the evidence in the pull request that it
holds: a test, a command and its output, a screenshot. Count the criteria with no evidence and
the decisions that never became criteria. A review that discussed only the diff fails this
check, however careful it was.

## Learn

- [How to kill the code review, 7:02](https://www.youtube.com/watch?v=YgEv7IQzGdM&t=422): a loop that turns the decisions made in an agent session into acceptance criteria and a test plan run against a preview.
- [BDD, ADR, PRD, WTF: capturing decisions for humans and AI alike (Safe Intelligence), 4:21](https://www.youtube.com/watch?v=504PvfXou5Y&t=261): executable scenarios that a person can read and a machine can run, as the link between the requirement and the check.
- [Why a one-line change can break your whole stack (Qodo), 11:04](https://www.youtube.com/watch?v=YqxpPI7YUjE&t=664): a demo of comparing a change with its ticket's criteria before the pull request opens. A vendor demo; watch this part only.

## Evidence for

- 2026-11-22: the How to kill the code review talk argues that the most valuable decisions are made in the conversation, and that review should move from reading lines to evidence that the intent was met. A practitioner's case, no measurement.
- 2026-11-22: GitHub's guidance for its coding agent asks for complete acceptance criteria in the issue, and Anthropic's guide asks the agent for evidence such as the command it ran and its output (both cited in [spec not grounded in current state](../docs/classes/spec-not-grounded-in-current-state.md) and [done is not the effect](../docs/classes/done-is-not-the-effect.md)).
- 2026-11-22: the incidents behind [done is not the effect](../docs/classes/done-is-not-the-effect.md) include work reported done, each step real, while the effect the task was for never happened.

## Evidence against

- 2026-11-22: asking is not checking. In the done-is-not-the-effect class doc an agent asked whether both modes were reachable said they were while one had no caller, and other runs were judged on their own exit code. The evidence for each criterion has to be read, not just listed.
- 2026-11-22: a criterion that is clear and false passes this habit, and one about the deployed system cannot be shown inside the pull request at all ([spec not grounded in current state](../docs/classes/spec-not-grounded-in-current-state.md)).
- 2026-11-22: the talks disagree on who accepts the change, a person or an automated contract check, and their evidence is cases and demos, one of them a vendor's.

## Guards

- [spec-not-grounded-in-current-state](../docs/classes/spec-not-grounded-in-current-state.md)
- [done-is-not-the-effect](../docs/classes/done-is-not-the-effect.md)
