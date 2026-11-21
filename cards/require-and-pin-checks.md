---
kind: config
why: A check that is not required can fail or never run and the merge still goes through, and a required check any app can report can be turned green by a status the change posts itself.
applies_when: changes, an agent's included, merge into a GitHub branch through a branch protection rule or a ruleset
last_reviewed: 2026-11-22
---

# Require every check you merge on, and pin it to the app that reports it

## Check

Read the required list back from the platform, not from memory or a workflow file:

```
gh api repos/OWNER/REPO/branches/BRANCH/protection/required_status_checks --jq '.checks[] | [.context, .app_id] | @tsv'
gh api repos/OWNER/REPO/rules/branches/BRANCH
```

The first command covers a branch protection rule, the second a ruleset. Every check you would
refuse to merge without must be on one of the lists, under the name its job reports today. A
check with no app id, or `-1`, accepts a status of that name from any app or from a commit
status anyone with write access can post.

## Fix

In the repository settings, add each check to the branch rule or ruleset as required, and set
its expected source to the app that runs it (GitHub Actions for a workflow job). Through the
API, send the `checks` list with an `app_id` for each entry. After renaming a job, add the new
name and remove the old one in the same change.

## Learn

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): what a required check blocks, and which statuses count as passing.
- [Troubleshooting required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks): why a required job that is skipped, or whose dependency failed, can still let the merge through.
- [Required checks from the intended app (GitHub changelog, 2021-11-30)](https://github.blog/changelog/2021-11-30-ensure-required-status-checks-provided-by-the-intended-app/): how pinning a check to an app works, and that older required checks stay unpinned until edited.

## Evidence for

- 2026-11-22: GitHub blocks a merge until every required check reports a passing status, so a required check that is cancelled, times out or never reports holds the pull request ([about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).
- 2026-11-22: once a required check is pinned to an app, a status of the same name from another app or from a commit status no longer satisfies it ([GitHub changelog](https://github.blog/changelog/2021-11-30-ensure-required-status-checks-provided-by-the-intended-app/)).
- 2026-11-22: several incidents behind [absence read as success](../docs/classes/absence-read-as-success.md) come from repositories with no branch protection at all, where nothing a check reported could stop a merge.

## Evidence against

- 2026-11-22: a required job skipped by a condition, or skipped because a job it needs failed, reports success and does not block; requiring it is not enough without an aggregating job that always runs ([troubleshooting required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)).
- 2026-11-22: a renamed job silently drops out of the required list, so the rule protects nothing until someone reads the list back.
- 2026-11-22: a check made required before pinning existed keeps accepting any app until the rule is edited ([GitHub changelog](https://github.blog/changelog/2021-11-30-ensure-required-status-checks-provided-by-the-intended-app/)).
- 2026-11-22: pinning does not help when the pinned app runs a definition the change can edit, such as a workflow taken from the branch under review; [a gate checks a satisfiable proxy](../docs/classes/gate-checks-a-proxy.md) records an approval produced that way.

## Guards

- [absence-read-as-success](../docs/classes/absence-read-as-success.md)
- [gate-checks-a-proxy](../docs/classes/gate-checks-a-proxy.md)
