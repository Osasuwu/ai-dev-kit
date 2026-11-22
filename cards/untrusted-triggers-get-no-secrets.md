---
kind: config
why: A workflow started by outsiders' pull requests, issues or comments that also holds secrets, or shares a cache with a release, hands those secrets or that release to whoever wrote the text.
applies_when: GitHub Actions workflows, an agent's included, run on events people outside the team can cause
last_reviewed: 2026-11-22
---

# Keep untrusted triggers away from secrets and release workflows, and scan for them

## Check

List the workflows that outsiders can start, and what each one holds:

```
grep -n "pull_request_target\|workflow_run\|issue_comment\|issues:\|discussion" .github/workflows/*.yml
zizmor .github/workflows/
```

For each match, three questions. Does it check out the pull request's code, or run anything
from it, while secrets or a write token are in scope? Is outside text (an issue title, a comment,
a branch name) placed into a shell line or an agent's prompt through a `${{ }}` expression?
Does it write a cache that a release or publish workflow restores? Any yes fails the check.
zizmor's `dangerous-triggers`, `template-injection` and `cache-poisoning` audits flag the common
forms.

## Fix

Run untrusted code under `pull_request`, which gets no secrets and a read-only token, and keep
`pull_request_target` and `workflow_run` for steps that never check out or execute the pull
request's code. Pass outside text to a script through an environment variable, not an
expression in the script line. Give release and publish workflows their own triggers and no
shared cache with workflows outsiders can start. Add zizmor, and rules that find issue text
placed into an AI prompt, as a CI step on changes to `.github/workflows/`.

## Learn

- [GitHub Security Lab, preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/): why `pull_request_target` plus a checkout of the pull request is dangerous, and why a label gate races.
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): which triggers to avoid with untrusted code, and the environment-variable pattern for untrusted input.
- [Cache poisoning in GitHub Actions](https://adnanthekhan.com/2024/05/06/the-monsters-in-your-build-cache-github-actions-cache-poisoning/): how a cache written by one workflow reaches a release in another.
- [zizmor audits](https://docs.zizmor.sh/audits/): the dangerous-triggers, template-injection and cache-poisoning rules.

## Evidence for

- 2026-11-22: GitHub's own guidance tells workflow authors to avoid `pull_request_target` and `workflow_run` with untrusted code, and to route untrusted input through environment variables ([GitHub Docs](https://docs.github.com/en/actions/reference/security/secure-use)).
- 2026-11-22: a researcher's write-up describes an issue-triage agent, started by any account, whose workflow shared a cache with nightly release workflows, so what a steered agent left in the cache could reach the release ([untrusted content steers the agent](../docs/classes/untrusted-content-steers-the-agent.md)).
- 2026-11-22: a security vendor published open rules that find issue text placed into an AI agent's prompt in workflows ([Aikido, PromptPwnd](https://www.aikido.dev/blog/promptpwnd-github-actions-ai-agents)).

## Evidence against

- 2026-11-22: the environment variable stops shell injection, not prompt injection: the text still reaches the agent, which reads it as text ([untrusted content steers the agent](../docs/classes/untrusted-content-steers-the-agent.md)).
- 2026-11-22: a scanner matches expressions in the workflow file; an agent that fetches the issue with its own tools leaves nothing in the file to match, and the token and tool list are a separate question.
- 2026-11-22: gating a run on a label races, since the author can push after the label is set ([GitHub Security Lab](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)).
- 2026-11-22: it costs split workflows, slower release builds without the cache, and triage of the scanner's findings.

## Guards

- [untrusted-content-steers-the-agent](../docs/classes/untrusted-content-steers-the-agent.md)
