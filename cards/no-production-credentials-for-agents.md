---
kind: config
why: Whatever credential sits in the agent's environment or files is one the agent can use, so a mistaken or steered command in a dev session reaches production data and the backups beside it.
applies_when: an agent runs with access to environment variables, config files or a shell profile that hold tokens for databases, clouds, registries or code hosts
last_reviewed: 2026-11-22
---

# Give the agent scoped, per-environment credentials, and none for production

## Check

List what the agent could pick up, by name only, never printing values:

```
env | cut -d= -f1 | grep -iE 'token|key|secret|passw|database_url|dsn'
ls -a .env* 2>/dev/null; ls ~/.aws ~/.kube ~/.config/gcloud 2>/dev/null
```

Run it in the shell the agent uses. For each credential found, ask which environment it
reaches, what it can delete, and when it expires. Any credential that reaches production, or a
token that can write to every repository you own, fails the check, and so does one in a file
the agent can read even if no task uses it.

## Fix

- Issue the agent its own credentials per environment: a development database user, a
  fine-grained token scoped to the repositories it works on, with an expiry.
- Keep production credentials out of the agent's machine, profile and workspace. Production
  changes go through a pipeline whose environment requires a person's approval.
- Block reads of credential files the agent does not need: deny rules for `.env` and cloud
  config paths, or the sandbox's `credentials` settings that deny or mask files and variables.
- Where an agent must call a service, have a proxy or gateway outside its environment add the
  credential to the request, so the token never sits where the agent runs.

## Learn

- [Decoupling the Brain from the Hands: Claude Managed Agents (Part 1 of 4) (Anthropic), 8:52](https://www.youtube.com/watch?v=Uv0nAf_7tyU&t=532): why credentials were moved out of the sandbox into a proxy that adds them to outgoing calls.
- [How Many Credentials Should Your AI Agent Have? Zero. (Docker), 8:21](https://www.youtube.com/watch?v=ZUZVNKFSmTM&t=501): granting a capability only for the minutes of the task that need it.
- [Who Is Making This Request? Agent Auth 101 (Keycard), 12:24](https://www.youtube.com/watch?v=58ulJViGFgU&t=744): the rule that a token in the agent's execution environment is a token the agent can reach.
- [GitHub fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens): repository scope and expiry, and what these tokens cannot cover.

## Evidence for

- 2026-11-22: an agent working in a development session deleted data from the production database (INC-004); in another case an agent found an infrastructure token in a file unrelated to its task and used it on a volume it took to be staging, where the backups also sat (INC-006) ([irreversible effects](../docs/classes/irreversible-effects.md)).
- 2026-11-22: Anthropic's talk describes rebuilding its managed agents so the model never sees the token; it is an architecture case study, not a measurement.
- 2026-11-22: the Docker and Keycard talks argue the same rule from engineering experience; both companies sell products in this space.

## Evidence against

- 2026-11-22: a scoped credential does not help when a broader one is reachable somewhere the agent can read, as in INC-006; and fine-grained tokens have gaps, such as packages and some APIs ([irreversible effects](../docs/classes/irreversible-effects.md)).
- 2026-11-22: it costs more credentials to issue, rotate and keep apart, and a task that does need production is slower because a person has to do or approve that part.
- 2026-11-22: a gateway that adds credentials becomes a high-value target, brings TLS complications and needs someone to keep its routes and policies, by the Keycard talk's own account ([15:24](https://www.youtube.com/watch?v=58ulJViGFgU&t=924)).

## Guards

- [irreversible-effects](../docs/classes/irreversible-effects.md)
