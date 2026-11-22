---
kind: belief
why: Counting pull requests, commits, lines or tokens rewards splitting and rushing work, so the count rises while what was checked and shipped does not.
applies_when: you measure agent-assisted development, or set targets for it, by output volume: pull requests, commits, lines changed, tokens spent
last_reviewed: 2026-11-22
---

# Volume metrics reward the wrong work

## Check

For each volume figure you report, find the metric that should move against it if quality
slips: review comments per change, reverts and change failure rate, time reviewers spend,
changes confirmed working in use. If volume rose and those fell, or nobody tracks them, the
volume figure measures production speed only. Look for the gaming signs: pull requests getting
smaller and more numerous for the same work, review time per change falling. Check whether any
dashboard ranks people by volume.

## Learn

- [ReviewDebt: a practical framework for scoring every pull request (eBay), 0:00](https://www.youtube.com/watch?v=TJPInBjhE4Q&t=0): industry data on review load as volume grows, and a deterministic score for the review burden of each pull request.
- [From Tokenmaxxing to Trusted Throughput (Ironclad), 5:47](https://www.youtube.com/watch?v=dSg0pu8d6qg&t=347): how one team's metric moved from lines, to open pull requests, to code verified in review and in customers' use.
- [How Building with AI Can Double the Throughput of Your Engineering Team, 3:25](https://www.youtube.com/watch?v=4_VQBbs2iQA&t=205): the other side, a volume target set on purpose by a team that knew it would distort.

## Evidence for

- 2026-11-22: industry figures cited in the eBay talk: commits up 25% and comments on them down 27% (GitHub), median review time up 441.5% and 31.3% of pull requests merged without review (Faros). Measured by others; seen second-hand.
- 2026-11-22: the talk's point is that pull requests per developer, their size and cycle time all mislead here. The mechanism is easy to see: the count rises when one change is split into several, and cycle time falls when reviewers stop pushing back. An argument, not a measurement.
- 2026-11-22: agent pull requests that passed their tests were, in one review, not mergeable as they stood, about 42 minutes of fixes each (METR, in [proxy optimisation](../docs/classes/proxy-optimisation.md)). A count of completed changes would have scored them all.
- 2026-11-22: DORA's guidance is to keep several metrics with tension between them, cited in the same class doc's measurement rung.

## Evidence against

- 2026-11-22: the team in the throughput talk set a target of twice the changes per engineer, said openly that any measure decays once it is a target, and reports that defects rose but were fixed faster. A volume target used knowingly, with a quality measure beside it, worked for them by their own account.
- 2026-11-22: the Ironclad talk still tracks lines and tokens, for learning rather than for targets or ranking people, so volume data is useful as context.
- 2026-11-22: no controlled comparison of teams with and without volume targets was found; the evidence is industry aggregates and company cases.

## Guards

- [proxy-optimisation](../docs/classes/proxy-optimisation.md)
