---
kind: belief
why: Two pull requests that each pass on their own can break the main branch together, and at agent pace that pair stops being rare, while testing every combination slows merging.
applies_when: agents open pull requests against one main branch faster than people did, and each is tested only against the branch it started from
last_reviewed: 2026-11-22
---

# At agent pace, pull requests that pass alone break the main branch together

## Check

Go through the red runs on your main branch over the last few months. For each, find whether it
came from two changes that were each green and were never tested together: different files,
merged close in time, the later one tested against a main branch without the earlier one. Count
those against the number of pull requests merged per week, and see whether the share grows as
agents open more of them. Then measure the time from approval to merge over the same months; a
rising wait is the other half of the same pressure.

## Learn

- [AI writes code faster than Uber can merge it (Uber), 2:11](https://www.youtube.com/watch?v=hX140a5klW0&t=131): how two green changes break trunk once merged, and why the rate grows with agents.
- [AI writes code faster than Uber can merge it (Uber), 5:54](https://www.youtube.com/watch?v=hX140a5klW0&t=354): a merge queue that tests the possible future states of main, and what keeping trunk green cost in waiting time.
- [Your team's agents are all shipping to the same code at once (Tessl), 5:20](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=320): ways to isolate parallel agents and to settle their collisions; a vendor's framing.
- [Rebuilding CI for AI-scale commit volume (Sonar), 10:10](https://www.youtube.com/watch?v=7b9tov5Uc5s&t=610): where faster CI comes from under agent volume; a vendor's talk.

## Evidence for

- 2026-11-22: at Uber, requests to merge rose about 44%, from 90 to 130 an hour, between January and March 2026; its queue builds candidate states of main (each change alone and together) and merges what keeps trunk green, and the 95th-percentile time to merge rose from 30 minutes to 3 to 4 hours (the Uber talk above). One measured case, at one large company's scale.
- 2026-11-22: GitHub's merge queue exists for this pair: it tests each pull request against the target branch plus the pull requests ahead of it ([shared state without ownership](../docs/classes/shared-state-without-ownership.md), serialize rung).
- 2026-11-22: a vendor reports CI steps of about 10 minutes brought under a minute on warm incremental builds through caching, less recompilation and sharding (the Sonar talk). Vendor data; it bears on the cost of testing combinations, not on how often they break.

## Evidence against

- 2026-11-22: the only measured case is one large company at high request rates; no source counts how often two green changes break main in a typical repository, where the pair may stay rare.
- 2026-11-22: a green trunk is paid for in waiting: Uber's answer brought admission control, a deferred secondary queue and looser conflict rules, and a merge queue costs a CI run per entry and a rebuild of the entries behind one that jumps the queue ([shared state without ownership](../docs/classes/shared-state-without-ownership.md)).
- 2026-11-22: isolation and merge by feature rather than by line are offered as alternatives (the Tessl talk), from a vendor with a product in the space; no comparison of the approaches was found.

## Guards

- [shared-state-without-ownership](../docs/classes/shared-state-without-ownership.md)
- [limits-and-cost-unmeasured](../docs/classes/limits-and-cost-unmeasured.md)
