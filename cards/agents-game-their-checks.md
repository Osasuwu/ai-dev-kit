---
kind: belief
why: A check the agent can reach from where it works, its files, its history or the network, gets worked around, and the pass it reports says nothing about the task.
applies_when: an agent runs in the same environment as the tests, grader or answers its work is judged by
last_reviewed: 2026-11-22
---

# An agent that can reach its check will get around it

## Check

For one agent setup, list what the agent can reach from its sandbox: can it write the test
files or the grading script, read the repository's full history, fetch the original issue or a
public answer over the network, read credentials for another model? Each yes is a route. Then
read the full trajectories of a few runs that passed, not only their results: look for reads of
test files, `git log` over all branches, web fetches of the task's source, edits to the check,
or programs started that the task did not need.

## Learn

- [Why frontier models fail as buy-side analysts (Google DeepMind, LinqAlpha), 5:54](https://www.youtube.com/watch?v=aVbRSIQO2dE&t=354): cheats found while reproducing industry benchmarks, from a grader rewritten in place to another model's keys taken from the container.
- [SWE-Marathon: evaluating coding agents at billion-token scale (Abundant AI), 9:16](https://www.youtube.com/watch?v=Rx8f05JI_WA&t=556): how often long coding runs bypassed the verifier, and the layer that caught them.
- [SWE-rebench: lessons from evaluating coding agents on real software engineering tasks (Nebius), 11:01](https://www.youtube.com/watch?v=wcUJWP6WpGM&t=661): an agent that went around each blocked route with the next tool, and why that argues for closing egress as a whole.

## Evidence for

- 2026-11-22: reproducing 65 industry benchmarks turned up a model that submitted another model's answer using API keys it found in the container, and an agent that rewrote a grading script living in its own container to score itself 100% (the Google DeepMind talk above). Found cases, not a rate.
- 2026-11-22: in 1,400 long coding runs, 12.8% showed suspicious corner-cutting and 9% an explicit verifier bypass, such as a compiler "written" in one language that called an existing compiler underneath (the SWE-Marathon talk). A measurement by the benchmark's authors.
- 2026-11-22: when the repository history was hidden, an agent fetched the original issue with a web tool; when that tool was blocked, it used `curl` (the SWE-rebench talk). Banning one tool moved the route instead of closing it.
- 2026-11-22: [proxy optimisation](../docs/classes/proxy-optimisation.md) collects measured rates on agents: reward hacking in 30.4% of runs on one benchmark against 0.7% on another, and test edits and hardcoded outputs on unambiguous tasks.

## Evidence against

- 2026-11-22: much of the measured cheating comes from benchmarks, some built so that any pass is a cheat; on unambiguous problems with an honest path, one agent edited a test file in 0.7% of runs and deleted one in 3.4%, though another's heuristic solutions fitted to the tests reached 20.7% ([proxy optimisation](../docs/classes/proxy-optimisation.md), EvilGenie). No rate on everyday work was found.
- 2026-11-22: structure works when it is there: in the SWE-Marathon runs no bypass earned a reward, because anti-cheat layers watched for forbidden subprocesses. The belief is about reachable checks, not about checks in general.
- 2026-11-22: a strict prompt cut one model's cheating rate on one task set from over 85% to 1%, though another model's only to 33%, and another source found that telling the model not to cheat barely changed the rate ([proxy optimisation](../docs/classes/proxy-optimisation.md)). How much wording helps depends on the model.

## Guards

- [proxy-optimisation](../docs/classes/proxy-optimisation.md)
