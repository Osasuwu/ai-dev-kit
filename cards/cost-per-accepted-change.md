---
kind: belief
why: Token price and benchmark accuracy leave out retries, review, escalations and rework, so a setup that looks cheap per call can cost more per change you keep.
applies_when: you choose a model, an agent setup or a workflow for coding work by what it costs, or justify agent spend
last_reviewed: 2026-11-22
---

# The cost of agent work is the cost of an accepted change, people included

## Check

For one month, add up what the agent work cost: tokens, CI runner minutes, the time people spent
reviewing, answering escalations and fixing what came back. Divide by the changes that were
merged and not reverted in that month, not by the pull requests opened or the runs started. Put
that figure next to the token spend per pull request you track now. If you can only fill in the
token line, you are measuring the part that is usually cheapest, and a cheaper model or a
tighter budget may be raising the total.

## Learn

- [Tokens are the cheap part (Jellyfish), 4:02](https://www.youtube.com/watch?v=U7ZYBCcdJPg&t=242): cost per merged pull request across many companies, salaries included.
- [Tokens are the cheap part (Jellyfish), 16:29](https://www.youtube.com/watch?v=U7ZYBCcdJPg&t=989): the limits of the figure, which is observational, not causal.
- [Tokens should have jobs (Anthropic), 7:37](https://www.youtube.com/watch?v=PXj0p_mW9nI&t=457): computing the cost of a fully correct answer when only those count, across strategies.
- [What technical due diligence finds when the deck says "70% automated", 3:49](https://www.youtube.com/watch?v=gDRCpTMCqEU&t=229): a full formula for the cost of an accepted autonomous task, with failure, escalation and rework priced in.

## Evidence for

- 2026-11-22: across many companies, the dollar cost of a merged pull request fell 26% in a year while AI spend rose about 60 times, with the fall at 83% of companies; AI came to between about 0.3% and 8.5% of a pull request's cost, because salaries spread over more pull requests faster than tokens grew (the Jellyfish talk above). Observational data from a vendor; the metric counts merged pull requests and includes review time.
- 2026-11-22: when only a fully correct answer is worth anything, one strategy gave a perfect answer in about 40% of runs, so it took about three runs of 600,000 tokens, 1.8 million in all, to get one; other strategies came out cheaper per correct answer (the Anthropic talk). A measurement on financial tasks, not coding.
- 2026-11-22: agent pull requests that passed their tests in 38% of tasks were none of them mergeable as they stood, and each needed about 42 minutes of fixes (METR, in [proxy optimisation](../docs/classes/proxy-optimisation.md)). That rework is cost a per-call price never shows.

## Evidence against

- 2026-11-22: merged is not the same as good: a change can be accepted and still make the code harder to change later, which no cost per merged change sees ([pass rate does not see maintainability erosion](pass-rate-misses-erosion.md), [proxy optimisation](../docs/classes/proxy-optimisation.md)).
- 2026-11-22: people's time is hard to attribute to one change, and the cross-company figures are observational; the due diligence talk states its formula with references rather than measuring it.
- 2026-11-22: watching cost can change behaviour for the worse: at Revolut, engineers under strict token budgets economised, and after a move to self-hosted models with effectively no limit, the gains in coding time and lead time grew, as people also automated work around the code ([How Revolut cut AI coding costs 90% with self-hosted open models (Revolut), 2:38](https://www.youtube.com/watch?v=Ok6QdZHCcI8&t=158)). The model change coincided with better models, so it is not clean evidence either way.

## Guards

- [limits-and-cost-unmeasured](../docs/classes/limits-and-cost-unmeasured.md)
- [proxy-optimisation](../docs/classes/proxy-optimisation.md)
