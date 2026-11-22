---
kind: habit
why: An error that is caught and logged in production can go unread for weeks, and a fix written without first reproducing it can merge without changing anything where the failure happens.
applies_when: your software emits errors, logs, replays or user reports in production, and an agent can read them and open pull requests
last_reviewed: 2026-11-22
---

# Let production signals start an agent that reproduces the failure and opens a fix for a person to approve

## Check

Take the last few production failures that got fixed and measure the time from the first signal
to someone acting on it; a signal source that nobody and nothing reads fails the check. For the
fix pull requests an agent opened, check that each carries a test, replay or dataset case that
fails on the base commit and passes on the head, and that a person approved it before merge. Then
look at the input side: signals that outsiders can write into, such as error messages from a
public site or support tickets, should pass a filter for injected instructions before the agent
reads them.

## Learn

- [Self driving products: product signals to pull requests, 3:26](https://www.youtube.com/watch?v=zMiSRliEzv4&t=206): a full pipeline from errors, replays, logs and support messages through filtering, grouping and research to a pull request built in a sandbox.
- [Self driving products: product signals to pull requests, 5:04](https://www.youtube.com/watch?v=zMiSRliEzv4&t=304): the engineering failures on the way: public signals as an injection route, and grouping that clustered by format instead of by problem.
- [The missing layer after launch, 6:43](https://www.youtube.com/watch?v=kZsf_Sfm7RU&t=403): a separate review agent with a fresh context that judges the fix agent's pull requests before a person sees them.
- [The self-improving OSS agent stack (Langfuse), 12:11](https://www.youtube.com/watch?v=TeErpYBUIeM&t=731): reproducing the problem on the current version and backtesting the new one on an updated dataset before the agent opens a pull request.

## Evidence for

- 2026-11-22: PostHog describes running signals through a safety filter, grouping them into reports, and sending a report to a research agent only once its combined weight crosses a threshold ([Self driving products](https://www.youtube.com/watch?v=zMiSRliEzv4&t=206)). A practitioner's case.
- 2026-11-22: Langfuse runs such an agent on a schedule; it reproduces the problem on the current version, backtests the change, and opens a pull request instead of publishing ([The self-improving OSS agent stack](https://www.youtube.com/watch?v=TeErpYBUIeM&t=731)). A practitioner's case.
- 2026-11-22: [silent fallback](../docs/classes/silent-fallback.md) records failures that were caught and dropped while the service looked healthy; sending errors where something acts on them is one of its protections, and [done is not the effect](../docs/classes/done-is-not-the-effect.md) records fixes that passed their tests and changed nothing where the effect lands, which a failing reproduction guards against.

## Evidence against

- 2026-11-22: signals from public sources carry text an attacker can write; the pipeline needs a filter in front, and a filter is a classifier that can miss ([untrusted content steers the agent](../docs/classes/untrusted-content-steers-the-agent.md)).
- 2026-11-22: the person stays the bottleneck: in one case the agents opened about ten times as many pull requests as three people had, and the fix agents were too eager to change code, which is why a review agent was put in front ([The missing layer after launch](https://www.youtube.com/watch?v=kZsf_Sfm7RU&t=621)).
- 2026-11-22: the evidence is case studies with no measured effect on time to fix or on regressions, and the talks disagree on scope, from narrow diagnosis to ticket-to-deploy, and on how much independent review comes before a person.

## Guards

- [silent-fallback](../docs/classes/silent-fallback.md)
- [done-is-not-the-effect](../docs/classes/done-is-not-the-effect.md)
