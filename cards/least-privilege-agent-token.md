---
kind: config
why: An agent that reads text others write acts with whatever its token and tools reach, so a planted instruction or a plain mistake can push code, leak private data or post outside.
applies_when: an agent runs in CI or as a bot with a token, triggered by issues, pull requests or comments that people outside the team can write
last_reviewed: 2026-11-22
---

# Give the agent the least-privileged token, the fewest tools, and only trusted people to start it

## Check

Read what each agent workflow can do, from the platform and the workflow files:

```
gh api repos/OWNER/REPO/actions/permissions/workflow
grep -n -A8 "permissions:" .github/workflows/*.yml
grep -n "secrets\.\|allowed_non_write_users\|allowed_tools\|allowedTools" .github/workflows/*.yml
```

The repository default for the workflow token should be read-only. Each job that runs an agent
should declare its own `permissions:` with only the scopes its task needs. No personal access
token should reach the agent. The agent's tool list should be explicit and should not give a
triage or review agent a shell, or a way to write where it reads. Nobody without write access
should be able to start it: the setting that lets other users trigger it should be absent.

## Fix

Set the default workflow token to read, and grant write scopes per job. Replace a personal token
with a GitHub App or a fine-grained token scoped to one repository and the job. List the agent's
tools explicitly, leave out the shell and the write tools a read-only task does not need, and
keep the tool that posts its result separate from the one that reads outside text. Let only
people with write access start the agent, and have a maintainer start runs on outsiders' issues
or pull requests. Production credentials are a separate card.

## Learn

- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): minimum permissions for the workflow token, and how to set them per job.
- [claude-code-action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md): who can trigger the action, the risk of letting other users in, and why not to use a personal token.
- [How Many Credentials Should Your AI Agent Have? Zero. (Docker), 10:21](https://www.youtube.com/watch?v=ZUZVNKFSmTM&t=621): capabilities handed to the agent for one task through a gateway that holds the credentials.
- [Real AI Agent Attacks and What Would Have Stopped Them (Bloomberg), 14:06](https://www.youtube.com/watch?v=5O6jLtoeKrg&t=846): a short priority list drawn from incidents: a broker on tool calls, one identity, short-lived tokens.

## Evidence for

- 2026-11-22: researchers showed an agent with a user's broad token steered by a public issue into leaking private repositories, and recommend one repository per session ([Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability)).
- 2026-11-22: a write-up of prompt injection through issues into CI agents advises restricting the agent's toolset and not letting it write to issues or pull requests ([Aikido, PromptPwnd](https://www.aikido.dev/blog/promptpwnd-github-actions-ai-agents)).
- 2026-11-22: a practitioner talk that sets real agent incidents against the controls that would have stopped them ends on a priority list led by a broker on tool calls, one identity per agent and short-lived tokens ([Real AI Agent Attacks and What Would Have Stopped Them (Bloomberg), 14:06](https://www.youtube.com/watch?v=5O6jLtoeKrg&t=846)); a case catalogue, not a measurement.
- 2026-11-22: another practitioner talk argues the agent's sandbox should hold no credentials at all, with a gateway holding them and granting a capability per task ([How Many Credentials Should Your AI Agent Have? Zero. (Docker), 10:21](https://www.youtube.com/watch?v=ZUZVNKFSmTM&t=621)); a design argument, not a measurement.

## Evidence against

- 2026-11-22: the token the task needs may already reach the data: a user's own token covers their private repositories, and a database role can bypass row-level security ([untrusted content steers the agent](../docs/classes/untrusted-content-steers-the-agent.md)).
- 2026-11-22: a CI token stays valid until the job ends, and a task that needs the leaking tool, such as a triage agent that must comment, keeps it; even tools chosen before reading untrusted data left a residual attack rate in a benchmark (same class doc).
- 2026-11-22: the trigger check can be switched off, and allowed bots are not checked for repository permissions ([claude-code-action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)); a maintainer who starts a run checks who starts it, not what the agent will read.
## Guards

- [untrusted-content-steers-the-agent](../docs/classes/untrusted-content-steers-the-agent.md)
- [irreversible-effects](../docs/classes/irreversible-effects.md)
