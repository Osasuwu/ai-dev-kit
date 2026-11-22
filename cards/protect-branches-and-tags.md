---
kind: config
why: A force-push or a branch or tag deletion rewrites shared history that others have built on, and an agent with push rights can do it in one command it thought was routine.
applies_when: an agent can push to a shared GitHub repository, under its own token or a person's
last_reviewed: 2026-11-22
---

# Protect shared branches and release tags against force-push and deletion

## Check

Read the rules back from the platform. For a branch protection rule:

```
gh api repos/OWNER/REPO/branches/BRANCH/protection --jq '{force_push: .allow_force_pushes.enabled, deletion: .allow_deletions.enabled, admins_bound: .enforce_admins.enabled}'
```

For rulesets, list the rule types that apply to the branch, and check the tag rulesets too:

```
gh api repos/OWNER/REPO/rules/branches/BRANCH --jq '.[].type'
gh api repos/OWNER/REPO/rulesets --jq '.[] | [.name, .target, .enforcement] | @tsv'
```

The practice holds when force-push and deletion are off (`non_fast_forward` and `deletion` are
in the ruleset list), a tag ruleset covers your release tags, and the identity the agent pushes
as is neither an administrator exempt from the rule nor on a ruleset's bypass list.

## Fix

In the repository settings, add a ruleset (or a branch protection rule) on the default branch
and every long-lived shared branch that blocks force pushes and deletion, with enforcement
active. Add a tag ruleset on your release tag pattern (for example `v*`) that blocks deletion
and updates. Apply the rule to administrators, and keep the agent's identity off the bypass
list; if the agent runs under a person's admin token, give it its own token or app instead.

## Learn

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): the force-push and deletion settings, and who is exempt by default.
- [About rulesets](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets): rules for branches and tags, bypass lists, and how rulesets combine with protection rules.

## Evidence for

- 2026-11-22: an agent rewrote the history of a branch with an open public pull request; it asked first, but the force-push showed only as an aside inside an option the person picked for another reason (INC-002, [irreversible effects](../docs/classes/irreversible-effects.md)). A rule on the platform does not depend on how the question was worded.
- 2026-11-22: the class doc's ordering puts reversibility before approval: limit the reach, then make what it can reach restorable, then ask a person at the effect ([irreversible effects](../docs/classes/irreversible-effects.md)).

## Evidence against

- 2026-11-22: an administrator or an identity on the bypass list is exempt, so an agent running under an owner's token inherits the exemption ([irreversible effects](../docs/classes/irreversible-effects.md)).
- 2026-11-22: it protects the remote only; local, uncommitted work the agent deletes is outside it (INC-003). Protecting every feature branch would also block the agent's routine rebases, so INC-002's case, a force-push to a working branch with an open pull request, is not covered by a rule on the default branch alone.
- 2026-11-22: for private repositories the feature needs a paid plan tier, and administrators lose the shortcut of rewriting a branch directly.

## Guards

- [irreversible-effects](../docs/classes/irreversible-effects.md)
