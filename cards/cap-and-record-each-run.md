---
kind: config
why: Without a recorded stop reason and cost per run, a run cut off at its turn cap reads like a finished one, a loop that burns the budget goes unseen, and every limit's value stays a guess.
applies_when: agents run headless or on a schedule (CI jobs, bots, the Agent SDK, `claude -p` and the like), with turn caps, timeouts or budgets around them
last_reviewed: 2026-11-22
---

# Cap each agent run, and record its turns, cost, duration and stop reason

## Check

Open the record of the last ten agent runs. For each you should find the number of turns, the
cost (or tokens), the duration, and why the run stopped: success, turn cap, budget, timeout,
error or cancel. With Claude Code in print mode, the result carries these fields:

```
claude -p "<task>" --output-format json | jq '{subtype, num_turns, total_cost_usd, duration_ms}'
```

The practice fails if a run that hit a cap is reported the same way as one that finished, if
the record is missing for the runs that hit a limit, or if any run has no cap on turns, time or
spend.

## Fix

- Give every run a turn cap (`--max-turns`, `max_turns`), a wall-clock limit (the job's
  `timeout-minutes`, or `timeout` around the command), and, in the Agent SDK, a cost cap with
  `max_budget_usd`.
- Write one record per run, also when it fails or hits a cap: turns, cost, duration, the result
  subtype. Store it where someone reads it.
- Treat a cap as its own outcome: `error_max_turns` and `error_max_budget_usd` should fail the
  job or open a follow-up, never pass as success or vanish as silence.
- Once you have a few weeks of records, set each cap from the runs that succeeded rather than
  from a round number.

## Learn

- [Your Agent Didn’t Fail. Your Harness Did., 10:45](https://www.youtube.com/watch?v=BInpv7lGp1o&t=645): every external boundary needs an end (success, failure, timeout, cancel, max attempts), and a record of which one happened.
- [Agents in Orbit: Workflows, Not Autopilot (Flywire), 8:05](https://www.youtube.com/watch?v=rAUyRDOFyHU&t=485): per-agent timeouts, rate limits and duplicate locks on thousands of review runs.
- [An AI Agent Got Its User Banned From Resy (Keycard, JPMorgan Chase & AAuth), 24:52](https://www.youtube.com/watch?v=IavxrdVnwXM&t=1492): why a budget the agent can see beats a rate limit that cuts it off without saying why.
- [Agent SDK agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop): the result subtypes for a turn cap and a budget cap, and when the budget is checked.

## Evidence for

- 2026-11-22: GitHub's team logged token use per agentic workflow run and found, in workflows already in production, a 64-turn fallback loop and a tool called 342 times in one run ([GitHub Blog](https://github.blog/ai-and-ml/github-copilot/improving-token-efficiency-in-github-agentic-workflows/), via [limits and cost unmeasured](../docs/classes/limits-and-cost-unmeasured.md)).
- 2026-11-22: on 100 tasks, a turn cap set at the 75th percentile cut cost by 24% to 68% across three models with a small change in solve rate ([Gao and Peng](https://arxiv.org/html/2510.16786v2), via the class doc; single runs per setting).
- 2026-11-22: one project's design record split stop reason from status after a budget stop and an iteration cap could not be told apart, and an agentic-workflow tool began failing the workflow at the cap, where before it raised no error ([limits and cost unmeasured](../docs/classes/limits-and-cost-unmeasured.md)).
- 2026-11-22: the three talks above are case studies from production systems, not measurements.

## Evidence against

- 2026-11-22: in one GitHub Action, the file with the turn count and cost was never written on the run that hit the turn cap, the one run that needed it; and the SDK's cost fields are client-side estimates, not billing data ([limits and cost unmeasured](../docs/classes/limits-and-cost-unmeasured.md)).
- 2026-11-22: a budget is checked after a response arrives, so one response can overshoot it; a test with a $0.01 cap ended at about $0.084 after one turn ([LinuxJedi](https://linuxjedi.co.uk/when-the-docs-fall-short-investigating-claude-codes-budget-cap/), via the class doc).
- 2026-11-22: a cap cuts off expensive runs that would have succeeded: in one benchmark run, 20 of the 22 instances costing over $10 each were resolved, and runs on the same task can differ thirtyfold in tokens ([limits and cost unmeasured](../docs/classes/limits-and-cost-unmeasured.md)). A stop reason that is recorded but never reaches the gate changes nothing (INC-757).

## Guards

- [limits-and-cost-unmeasured](../docs/classes/limits-and-cost-unmeasured.md)
