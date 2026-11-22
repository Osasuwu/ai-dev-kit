---
kind: belief
why: An agent's or a model judge's result varies from run to run, so a choice made on one run, or on best-of-k, can rest on noise.
applies_when: you compare models, prompts or agent setups, or gate a change, on the result of an agent run or an LLM check
last_reviewed: 2026-11-22
---

# One run of an agent is a sample, not a measurement

## Check

Take the last decision you made from an agent or eval result: a model switch, a prompt change,
a regression call. How many runs per task was it based on, and was a spread or an interval
reported with the figure? Would the decision flip if one run on one task had gone the other way?
If the figure came from pass@k or from retrying until a run passed, ask whether it counts
ability or attempts. For a model check that gates merges, look for the same change judged twice
with different verdicts in your own history.

## Learn

- [Computer use at the edge of the statistical precipice, 2:03](https://www.youtube.com/watch?v=CTLa_p6iOiY&t=123): why pass@k can measure the number of attempts rather than ability.
- [Computer use at the edge of the statistical precipice, 11:27](https://www.youtube.com/watch?v=CTLa_p6iOiY&t=687): intervals that account for variation between tasks as well as between runs.
- [From zero to leaderboard: agent evaluation (Weights & Biases), 39:22](https://www.youtube.com/watch?v=YIxzNZDDy1A&t=2362): a five-run report with mean, best, worst, ceiling and the share solved in every run.
- [Why frontier models fail as buy-side analysts (Google DeepMind, LinqAlpha), 5:54](https://www.youtube.com/watch?v=aVbRSIQO2dE&t=354): reproduced benchmarks whose scores moved widely on the same infrastructure.

## Evidence for

- 2026-11-22: a talk shows that in deterministic environments pass@k equals the success of an agent that just replays its lucky attempt, and that intervals built from repeated runs alone, ignoring variation between tasks, covered the true value in only about 17% to 20% of cases; intervals over tasks and runs together brought it back to about 95% (the statistical precipice talk). A measurement.
- 2026-11-22: a five-run report found two models whose means were close, 73 against 74, six points apart on the share of tasks solved in every run (the Weights & Biases talk). One worked example.
- 2026-11-22: the same benchmark on the same infrastructure gave results that varied by about 20% either way when reproduced (the Google DeepMind talk).
- 2026-11-22: at temperature 0, 1,000 completions of one prompt gave 80 different outputs, and one review tool run twice on the same diff gave 10 findings, then 7, catching a planted bug only once ([LLM as the measuring instrument](../docs/classes/llm-as-measuring-instrument.md)).

## Evidence against

- 2026-11-22: repeats cost N times the tokens, and on a small task set even many runs cannot tell close configurations apart (the evaluation talks above); runs of one task can already differ up to 30 times in tokens ([limits and cost unmeasured](../docs/classes/limits-and-cost-unmeasured.md)).
- 2026-11-22: inference noise can be removed: with batch-invariant kernels all 1,000 completions came out identical, at about 60% more time in one benchmark ([LLM as the measuring instrument](../docs/classes/llm-as-measuring-instrument.md)). Then one run is reproducible, but it is still one draw from the task set, and the spread between tasks remains.
- 2026-11-22: more runs of one model share its blind spots, so their agreement is not recall: in one calibration three runs of the same reviewer all missed the same kinds of defect ([LLM as the measuring instrument](../docs/classes/llm-as-measuring-instrument.md)).

## Guards

- [llm-as-measuring-instrument](../docs/classes/llm-as-measuring-instrument.md)
