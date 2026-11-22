---
kind: belief
why: Faster code generation adds little to what ships when review, CI or release is the constraint, and the extra output waits there unseen.
applies_when: you adopt or scale coding agents expecting faster delivery, or judge their effect by how much code they produce
last_reviewed: 2026-11-22
---

# Faster generation moves the bottleneck to review and delivery

## Check

Take the changes merged over the last few months and split each one's lead time by stage:
writing, waiting for a first review, review rounds, waiting for CI, waiting to merge, waiting to
release. Compare the split before and after agents took on the writing. If the writing stage
shrank while the waiting stages grew, the constraint moved. Watch the count of open pull
requests and the issue backlog over the same period; a steady rise is the queue in front of
the new constraint.

## Learn

- [AI Writes the Code. So What's Left for Engineers? (Arize AI), 2:12](https://www.youtube.com/watch?v=kspZP5BgkEU&t=132): why the code written and the code shipped grow at very different rates, and the review limit behind the gap.
- [The State of AI in Software Development: Data from 400+ Orgs (DX), 15:10](https://www.youtube.com/watch?v=Se8jHLliLXE&t=910): the theory-of-constraints reading, and the view that the constraint is the whole delivery stream, not review alone.
- [How VS Code Went from Monthly to Weekly Releases with AI, 0:12](https://www.youtube.com/watch?v=I2LL_wd89-A&t=12): a small team fixing build, review and feedback loops one after another as agent output grew.

## Evidence for

- 2026-11-22: the Arize AI talk reports that developers with autonomous agents wrote 741% more code and shipped only about 30% faster, and puts the gap on review: people cannot read code faster, and a cited Cisco study finds comprehension drops past roughly 450 lines an hour. The sources appear on slides only; seen second-hand.
- 2026-11-22: the DX talk's data from over 400 organisations puts the median gain in pull request throughput at 7.7% and the mean at 13%, with the best near 70% and none doubling. Measured, on proxy metrics, by a vendor of developer-productivity measurement.
- 2026-11-22: in the VS Code talk, the share of agent code that survived rose from 55% to 86%, and with it the inflow of issues, some of them AI-generated noise, and the number of open pull requests. A case study: success created the next bottleneck.
- 2026-11-22: when review cannot keep up, merges lean on a model's verdict; [LLM as the measuring instrument](../docs/classes/llm-as-measuring-instrument.md) records pull requests merged on review rounds that had read only part of the diff.

## Evidence against

- 2026-11-22: the DX talk gives a different cause for the small gain: time saved is eaten by factors that have nothing to do with AI, such as meetings, context switching and friction around the code. That supports a moved constraint, not one that is always review.
- 2026-11-22: every figure above counts pull requests, lines or surviving code; none of the talks measures delivered value directly, and none is a controlled comparison.
- 2026-11-22: the VS Code case shows the constraint can be found and fixed repeatedly, so the belief describes a step to manage, not a ceiling on what agents add.

## Guards

- [llm-as-measuring-instrument](../docs/classes/llm-as-measuring-instrument.md)
- [limits-and-cost-unmeasured](../docs/classes/limits-and-cost-unmeasured.md)
