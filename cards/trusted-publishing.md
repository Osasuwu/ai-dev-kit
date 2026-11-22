---
kind: config
why: A long-lived publish token stored as a CI secret can be read by any job that untrusted text or an agent reaches, and a release published with it goes out under the project's name to everyone who installs it.
applies_when: you publish packages to a registry from CI, and agents or outside contributors can trigger or influence a workflow in that repository
last_reviewed: 2026-11-22
---

# Publish with short-lived, workflow-bound credentials, and keep them out of every other job

## Check

Search the workflows for stored publish tokens, and see which jobs can reach them:

```
grep -rnE 'NPM_TOKEN|NODE_AUTH_TOKEN|PYPI_(API_)?TOKEN|TWINE_PASSWORD|_PUBLISH_TOKEN' .github/workflows/
gh secret list
```

Any hit means a long-lived token exists and a job holds it. The practice holds when the publish
job gets its credential through OpenID Connect (`permissions: id-token: write` in that job
only), the registry is configured to trust exactly that workflow, the package refuses
token-based publishing, and no job triggered by a pull request, an issue or a comment shares
the release workflow, its secrets or its cache.

## Fix

- Set up trusted publishing on the registry: name the repository, the workflow file and, where
  supported, the environment allowed to publish. Remove the stored token and revoke it.
- On npm, set the package to require two-factor authentication and disallow tokens.
- Run the publish job in its own workflow, triggered by a tag or a release, behind an
  environment with a required reviewer. Grant `id-token: write` to that job alone.
- Keep agent and triage workflows out of it: no shared secrets, and no cache that the release
  build restores.

## Learn

- [npm trusted publishers](https://docs.npmjs.com/trusted-publishers): how a workflow publishes without a stored token, the setting that disallows tokens, and the runner limits.
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): OpenID Connect instead of long-lived secrets, and the triggers to keep away from untrusted code.
- [Nx s1ngularity postmortem](https://nx.dev/blog/s1ngularity-postmortem): how a publish token leaked through a workflow, and the move to trusted publishing afterwards.

## Evidence for

- 2026-11-22: a pull request title echoed into a shell step of a workflow that ran with the repository's secrets exposed the registry publish token; malicious versions went out under the project's name for four hours, and their install script tried to use AI command-line tools on victims' machines to look for secrets (INC-005, [untrusted content steers the agent](../docs/classes/untrusted-content-steers-the-agent.md)). The project adopted trusted publishing after the incident.
- 2026-11-22: an inappropriately scoped token in a build configuration let an outsider commit code to an extension's repository that shipped in an automatic release (INC-554), and in another case an agent was the route to a publish credential (INC-556) ([untrusted content steers the agent](../docs/classes/untrusted-content-steers-the-agent.md)).

## Evidence against

- 2026-11-22: npm's trusted publishing does not support self-hosted runners yet, so a pipeline that publishes from one cannot use it ([irreversible effects](../docs/classes/irreversible-effects.md)).
- 2026-11-22: it does not help when the release job itself runs what untrusted input left behind: in INC-556 the release workflows shared a cache with the triage workflow. A workflow that hands untrusted input to a job with write permission gives the same reach to whoever writes the input.
- 2026-11-22: a token not revoked after the move stays valid; in INC-556 one was not properly revoked after disclosure. The setup is per package and per registry.

## Guards

- [irreversible-effects](../docs/classes/irreversible-effects.md)
- [untrusted-content-steers-the-agent](../docs/classes/untrusted-content-steers-the-agent.md)
