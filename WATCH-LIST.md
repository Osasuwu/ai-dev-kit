# Watch list

Generated from the `Learn` sections in `cards/` by `python scripts/generate_card_index.py`; do not edit. The talks and pages each card learns from, with what to look for in each.

## [Require every check you merge on, and pin it to the app that reports it](cards/require-and-pin-checks.md)

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): what a required check blocks, and which statuses count as passing.
- [Troubleshooting required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks): why a required job that is skipped, or whose dependency failed, can still let the merge through.
- [Required checks from the intended app (GitHub changelog, 2021-11-30)](https://github.blog/changelog/2021-11-30-ensure-required-status-checks-provided-by-the-intended-app/): how pinning a check to an app works, and that older required checks stay unpinned until edited.

## [Have the agent use the running app before it calls the work done](cards/agent-uses-the-running-app.md)

- [Your agent is blindfolded, 2:12](https://www.youtube.com/watch?v=iRcX54EO5g8&t=132): why an agent that cannot see the running app cannot tell a working feature from a broken one.
- [Teach your agent to prove it's done (WorkOS), 20:51](https://www.youtube.com/watch?v=q4WC4TowkBo&t=1251): proof of done in two layers, a deterministic check and a model judge on top.
- [Teach your agent to prove it's done (WorkOS), 46:10](https://www.youtube.com/watch?v=q4WC4TowkBo&t=2770): why a proof goes stale once later changes land, and has to be redone.
- [How to build an AI code review agent (Greptile), 13:34](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=814): what an agent needs to test a change by using it: a sandbox, written scenarios, a one-command start.

## [Pass rate does not see maintainability erosion](cards/pass-rate-misses-erosion.md)

- [Why software factories fail, 12:03](https://www.youtube.com/watch?v=Ib5GBkD555M&t=723): why a reward for passing tests cannot account for how easy the code is to change.
- [AI writes the code, so what's left for engineers? (Arize AI), 6:01](https://www.youtube.com/watch?v=kspZP5BgkEU&t=361): a measurement where asking whether a maintainer would merge cut the success rate well below the test pass rate.
- [AI-generated code is already competing with human code (Greptile), 5:58](https://www.youtube.com/watch?v=474j-n1Ltxc&t=358): review data comparing agent and human pull requests, which finds no clear gap.
