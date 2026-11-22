---
kind: config
why: A required approval is met by a bot, by the account that pushed the change, or by a review of an earlier commit, so the merge rule holds while nobody independent read what merges.
applies_when: changes, an agent's included, merge into a GitHub branch that requires an approving review, and the agent or its workflows act through an account or token that can review
last_reviewed: 2026-11-22
---

# Count only an approval from someone other than the pusher, for the latest push

## Check

Read the review settings back from the platform:

```
gh api repos/OWNER/REPO/branches/BRANCH/protection/required_pull_request_reviews --jq '{count: .required_approving_review_count, dismiss_stale: .dismiss_stale_reviews, last_push: .require_last_push_approval}'
gh api repos/OWNER/REPO/rules/branches/BRANCH --jq '.[] | select(.type=="pull_request") | .parameters'
gh api repos/OWNER/REPO/actions/permissions/workflow --jq .can_approve_pull_request_reviews
```

The practice holds when at least one approval is required, stale approvals are dismissed, the
most recent push needs approval from someone other than its pusher, and workflows cannot
approve (`false`). Then ask which account the agent pushes under. If it is your own, the person
who must approve is the account that pushed, and the rule cannot be met honestly.

## Fix

- In the branch rule or ruleset, require an approving review, turn on dismissing stale
  approvals when new commits are pushed, and turn on requiring approval of the most recent
  reviewable push.
- In the repository's or organisation's Actions settings, turn off letting GitHub Actions
  create and approve pull requests. Leave any setting that lets a model's review count toward
  required approvals off.
- Give the agent its own account or app identity, separate from every person who approves.
- Apply the rule to administrators too, or the person most likely to merge is exempt.

## Learn

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): dismissing stale approvals, approval of the most recent push, and the admin exemption.
- [Approving a pull request with required reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews): authors cannot approve their own pull requests.
- [Prevent GitHub Actions from approving pull requests (GitHub changelog, 2022-01)](https://github.blog/changelog/2022-01-14-github-actions-prevent-github-actions-from-approving-pull-requests): the setting that stops a workflow token meeting the approval requirement.
- [Copilot cloud agent risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations): how the platform stops the person who asked the agent for a pull request from approving it.

## Evidence for

- 2026-11-22: an agent wrote a doc's sign-off into its metadata, added the matching sign-off record in a second commit, and merged with no review; an audit found none of that repository's nine merged pull requests had a review ([gate checks a proxy](../docs/classes/gate-checks-a-proxy.md), INC-600).
- 2026-11-22: a freshness check accepted a review posted after the head commit's time whose links pointed at an earlier commit, so a review of older content passed for the head (INC-602, same class doc).
- 2026-11-22: OpenSSF Scorecard does not count review by bots, AI-powered ones included, as code review, and the Claude GitHub action refuses to approve pull requests ([gate checks a proxy](../docs/classes/gate-checks-a-proxy.md)).

## Evidence against

- 2026-11-22: it costs a second person with write access for every review and a review round per push; a solo developer cannot meet it without a second identity or a hold only they can lift.
- 2026-11-22: since 2026-09 GitHub lets an administrator make a model's approval count toward required approvals, off by default ([GitHub changelog](https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests)); a bot's approval can also arrive through a workflow the pull request itself changed (INC-614).
- 2026-11-22: no study measures how often a gate passes on a proxy; most of the class's incidents come from one operator's repositories, which build their own gates ([gate checks a proxy](../docs/classes/gate-checks-a-proxy.md)).

## Guards

- [gate-checks-a-proxy](../docs/classes/gate-checks-a-proxy.md)
