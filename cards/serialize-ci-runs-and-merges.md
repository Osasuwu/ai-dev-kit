---
kind: config
why: Parallel runs that write the same branch, deployment or record interleave, and pull requests that each passed alone break the branch once merged together.
applies_when: several agents or jobs push to one repository, and CI runs on overlapping pushes or merges land faster than a person can watch
last_reviewed: 2026-11-22
---

# Serialize the CI runs that share state, and merge through a queue

## Check

Find the workflows that write something shared (a deployment, a release, a branch, a status
file, a cache) and look for a concurrency group on each:

```
grep -n -A2 "concurrency:" .github/workflows/*.yml
```

Then check whether merges go through a merge queue, and whether every required workflow also
runs on the queue's event:

```
gh api repos/OWNER/REPO/rules/branches/main --jq '.[].type'
grep -ln "merge_group" .github/workflows/*.yml
```

A `merge_queue` rule with a required workflow that lacks `merge_group` stalls every merge; no
queue at all means two pull requests can each pass on their own base and break the branch
together.

## Fix

Give each workflow that writes shared state a `concurrency` group keyed by what it writes, such
as the workflow and the branch, so at most one run in the group runs at a time. Set
`cancel-in-progress` to cancel stale test runs, and keep it off for deploys and releases, which
should finish rather than stop halfway. Turn on the merge queue in the branch rule or ruleset,
and add `merge_group` to the triggers of every required workflow, so the checks run on the
target branch plus the pull requests ahead in the queue.

## Learn

- [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency): what a group guarantees, what happens to the pending run, and that ordering is not guaranteed.
- [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue): how each entry is tested against the ones ahead of it, and why workflows must run on `merge_group`.

## Evidence for

- 2026-11-22: a concurrency group allows at most one running job or workflow in the group at any time ([GitHub Docs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)).
- 2026-11-22: a merge queue runs the required checks on the merged result before it lands; Uber reports keeping its mainline green with a queue of this kind ([Ananthanarayanan et al., EuroSys 2019](https://dl.acm.org/doi/pdf/10.1145/3302424.3303970)), an industrial case report, not a controlled comparison.
- 2026-11-22: [shared state without ownership](../docs/classes/shared-state-without-ownership.md) records a review check still running when a bot's push started a second run of it; the second run took a skip path and passed, auto-merge fired within a minute, and the real review failed after the merge.

## Evidence against

- 2026-11-22: a newer pending run replaces the older one in the group, and GitHub does not guarantee the order, so a group is not a FIFO queue ([GitHub Docs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)).
- 2026-11-22: a group covers runs inside Actions only, not a local session or a manual run on the same state.
- 2026-11-22: a queue serializes merges, not review verdicts, and costs a CI run per entry plus a rebuild of the entries behind one that leaves; flaky tests block it and get retried until green ([absence read as success](../docs/classes/absence-read-as-success.md)).

## Guards

- [shared-state-without-ownership](../docs/classes/shared-state-without-ownership.md)
