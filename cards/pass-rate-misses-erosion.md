---
kind: belief
why: An agent trained and judged on passing tests can deliver code that passes and is harder to change, and a pass rate cannot see the difference.
applies_when: you judge an agent's work, or compare agents or models, by tests passed or tasks completed
last_reviewed: 2026-11-22
---

# Pass rate does not see maintainability erosion

## Check

Take a sample of the agent's changes that passed their checks. For each, have a maintainer say
whether they would merge it as it stands, and if not, why. Compare that share with the pass
rate on the same changes; a wide gap means the pass rate is measuring something else. Over
months, compare how long changes to agent-written code take against changes to code people
wrote.

## Learn

- [Why software factories fail, 12:03](https://www.youtube.com/watch?v=Ib5GBkD555M&t=723): why a reward for passing tests cannot account for how easy the code is to change.
- [AI writes the code, so what's left for engineers? (Arize AI), 6:01](https://www.youtube.com/watch?v=kspZP5BgkEU&t=361): a measurement where asking whether a maintainer would merge cut the success rate well below the test pass rate.
- [AI-generated code is already competing with human code (Greptile), 5:58](https://www.youtube.com/watch?v=474j-n1Ltxc&t=358): review data comparing agent and human pull requests, which finds no clear gap.

## Evidence for

- 2026-11-22: the reward a coding model is trained on is mostly whether the tests pass, with nothing that charges for design, so nothing in training pushes against code that passes and erodes (argued in the Why software factories fail talk; an argument, not a measurement).
- 2026-11-22: a measurement attributed to Cognition, cited in the Arize AI talk, found task success fell from 87% to 54% when the bar changed from tests passing to a maintainer being willing to merge. Seen second-hand; the method was not checked here.
- 2026-11-22: [proxy optimisation](../docs/classes/proxy-optimisation.md) records agents that met the check while missing the goal it stood for.

## Evidence against

- 2026-11-22: Greptile's observational review data found no clear difference between agent and human pull requests in reverts, size, or severe review findings. It is vendor data, and it measures what shows within days; erosion would show over months.
- 2026-11-22: the measurement above comes from one benchmark, cited in a talk; no independent replication was found.

## Guards

- [proxy-optimisation](../docs/classes/proxy-optimisation.md)
