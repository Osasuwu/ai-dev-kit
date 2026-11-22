---
kind: config
why: When every action asks, people approve by habit; when nothing asks, a force-push, a recursive delete or a publish runs on the agent's judgment alone.
applies_when: an agent runs tool calls in a harness with permission rules or pre-call hooks (Claude Code or the like), and some commands it can reach have effects you could not undo
last_reviewed: 2026-11-22
---

# Ask or deny at the tool call for the irreversible kinds only

## Check

Read the ask and deny rules and the pre-call hooks the agent loads:

```
jq '{ask: .permissions.ask, deny: .permissions.deny, pre: .hooks.PreToolUse}' .claude/settings.json .claude/settings.local.json ~/.claude/settings.json 2>/dev/null
```

Write down the irreversible effects the agent could cause in this project: a force-push, a
recursive delete outside the workspace, a database migration or drop, an infrastructure apply,
a package publish, a change of access. Each should map to an ask rule or a hook that denies it.
Then count how many prompts you approved in your last few sessions: if you cannot remember
reading one, the asks are too many for any of them to be read.

## Fix

- Sort the actions the agent takes by whether they can be undone, and whether the damage is
  acceptable if they go wrong. Let undoable ones run without a prompt; keep prompts for the rest.
- Add an ask rule for each irreversible kind, so the prompt names that effect rather than
  arriving as one of many routine approvals.
- For the kinds that should never run from the agent, add a `PreToolUse` hook that parses the
  command and denies it (exit 2 with a reason on stderr). Test it against the spellings it must
  catch: flags in another order, `bash -c`, a script that wraps the command.
- Have the hook catch its own errors and exit 2 on them; a hook that crashes some other way or
  times out lets the call through.

## Learn

- [Give the Agent a Budget, Not a Token (Anthropic), 4:41](https://www.youtube.com/watch?v=rbjWzZK2LU0&t=281): the undo test, whether the agent could roll the action back and whether the blast radius is acceptable, as the way to decide which actions need a second key.
- [Give Your On-Call Its Own AI Teammate (Meta), 4:21](https://www.youtube.com/watch?v=_NBx2NNOuA4&t=261): autonomy granted per action, from shadow to approval to autonomous, by how cheap a mistake is.
- [What a $900M Bank Error Teaches Us About AI Agents (Two Sigma), 3:44](https://www.youtube.com/watch?v=iniryju23Sk&t=224): three people approved a costly mistake; why an approval holds only when the approver can check the work.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks): `PreToolUse`, exit code 2, and what happens when a hook fails.

## Evidence for

- 2026-11-22: Anthropic reports that Claude Code users approve 93% of permission prompts, which suggests a prompt on every action is approved by reflex ([irreversible effects](../docs/classes/irreversible-effects.md), from [Anthropic, auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode)).
- 2026-11-22: an agent force-pushed over a branch with an open pull request after a question that mentioned the force-push only as an aside (INC-002), and another deleted uncommitted files before asking (INC-003) ([irreversible effects](../docs/classes/irreversible-effects.md)).
- 2026-11-22: the Meta and Anthropic talks describe per-action approval by cost of error as practice in their own systems; they are case studies, not measurements.

## Evidence against

- 2026-11-22: a hook that reads the command's raw text misses what the shell expands later; one survey found quote removal alone defeated every raw-text guard it tested, and a delete through `$HOME` reads the same whatever `$HOME` holds ([irreversible effects](../docs/classes/irreversible-effects.md), [destructive op on a computed target](../docs/classes/destructive-op-on-computed-target.md)).
- 2026-11-22: Claude Code's own docs say an ask or deny rule covers the usual spelling of a command and is not a security boundary, and a mode that skips prompts removes most asks; a hook that crashes or times out lets the call go on.
- 2026-11-22: approval itself can be empty: in the bank-error case the approvers overrode a warning that matched what they expected; an agent can also present an action so the person approves without seeing the effect.

## Guards

- [irreversible-effects](../docs/classes/irreversible-effects.md)
- [destructive-op-on-computed-target](../docs/classes/destructive-op-on-computed-target.md)
