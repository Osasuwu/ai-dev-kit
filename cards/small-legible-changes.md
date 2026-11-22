---
kind: habit
why: Cheap generation makes pull requests bigger and more varied in style, and a reviewer who has to rebuild both the code and its intent approves what they did not understand.
applies_when: agents write changes that people review before they merge
last_reviewed: 2026-11-22
---

# Keep agent changes small and owned, with the why written by a person

## Check

Look at the agent pull requests merged over the last month. Track changed lines per pull request
and whether the figure is rising. Check that each has one named owner who can explain it, and that
it does one thing: a refactor and a feature in one pull request fail. Read the top of each
description: it should open with a few lines its author wrote by hand saying what changed and
why, with any generated summary below and marked as such. Then ask a reviewer to explain, from
memory, a pull request they approved last week; if they cannot, the changes are bigger than
review can carry.

## Learn

- [The state of AI in software development: data from 400+ orgs (DX), 4:42](https://www.youtube.com/watch?v=Se8jHLliLXE&t=282): how pull request size and engineers' confidence in their changes moved over a year.
- [The state of AI in software development: data from 400+ orgs (DX), 6:12](https://www.youtube.com/watch?v=Se8jHLliLXE&t=372): the widening spread of change failure rate between companies.
- [Generation is cheap, review is expensive: how to stop shipping AI slop (G2i), 11:02](https://www.youtube.com/watch?v=6qkzlT962es&t=662): why conventions, small review surfaces and clear ownership lower the cost of understanding a change.
- [How to get your org to adopt coding agents (without shipping garbage) (Figma), 12:30](https://www.youtube.com/watch?v=5Bn0xro2ol8&t=750): opening each pull request description with lines the author wrote, and reading the generated part with suspicion.
- [Small CLs (Google engineering practices)](https://google.github.io/eng-practices/review/developer/small-cls.html): why small changes review better, and keeping refactors apart from feature changes.

## Evidence for

- 2026-11-22: DX reports, from data on about 200,000 engineers, that the average pull request grew from about 44 to about 72 lines in a year, confidence in changes fell 6%, and change failure rate spread much more widely between companies ([DX, 4:42](https://www.youtube.com/watch?v=Se8jHLliLXE&t=282)). A large measurement by a vendor that sells such measurement; it shows a correlation, not that size caused the failures.
- 2026-11-22: the G2i talk argues that generation does not remove the cost of understanding: an agent can produce several plausible patterns in several styles, and the reviewer has to recover the intent as well as the code ([Generation is cheap, review is expensive](https://www.youtube.com/watch?v=6qkzlT962es&t=662)). An argument from practice.
- 2026-11-22: [scope overreach](../docs/classes/scope-overreach.md) cites a study in which about 40% of agent pull requests had several objectives, against about 12% of human ones.

## Evidence against

- 2026-11-22: the pattern of growing, harder-to-review changes existed before agents; the DX data says agents made it larger, so this habit treats an old problem, not a new one.
- 2026-11-22: a size limit misses the small change with a large effect, such as one changed default or one deleted step ([scope overreach](../docs/classes/scope-overreach.md)).
- 2026-11-22: more, smaller pull requests mean more to open and review, and agents do not keep to the norm unless told or gated ([scope overreach](../docs/classes/scope-overreach.md)).

## Guards

- [scope-overreach](../docs/classes/scope-overreach.md)
