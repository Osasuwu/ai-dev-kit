---
kind: config
why: An agent stops when the work looks done and reports that the tests pass, and nobody ran them; a check that runs only if the agent chooses to run it is a claim, not a check.
applies_when: the agent's harness can run a script when it tries to end its turn (a Claude Code Stop hook or the like), and the project has a pass-or-fail check
last_reviewed: 2026-11-22
---

# Have a Stop hook run the check before the agent may stop

## Check

Look for a Stop hook in every settings file the agent loads:

```
jq '.hooks.Stop' .claude/settings.json .claude/settings.local.json ~/.claude/settings.json 2>/dev/null
```

`null` everywhere means nothing runs when the agent stops. Where a hook exists, read its script:
it should run the project's check itself (tests, a build, a probe of the effect) and exit 2 on
failure. Then break the check on a throwaway branch and ask the agent to finish a small task;
it should be sent back to work with the failure in front of it, not end the turn.

## Fix

Register a script under `Stop` in the project's `.claude/settings.json`:

```json
{ "hooks": { "Stop": [ { "hooks": [ { "type": "command", "command": "scripts/stop-check.sh" } ] } ] } }
```

The script runs the check and, when it fails, writes what failed to stderr and exits 2; exit 2
is what blocks the stop and hands the message to the agent. Treat every non-zero code from the
check as failure, including pytest's 5 for "no tests collected". Where you can, have the script
read the target's state (the pull request exists, the endpoint answers, the migration ran), not
the exit code of the step that should have produced it. Keep the same check required in CI, so
a session without the hook is still caught at merge.

## Learn

- [Claude Code best practices](https://code.claude.com/docs/en/best-practices): giving the agent something that comes back pass or fail, and the Stop hook that sends it back to work on exit code 2.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks): Stop hook input and exit codes, which failures do not block, and the cap on consecutive blocks.
- [LangChain on harness engineering for deep agents](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering): a harness change that included a check against the task before the agent exits.

## Evidence for

- 2026-11-22: Claude Code's own guidance says the agent stops when the work looks done, and gives a runnable check plus a Stop hook as the answer ([best practices](https://code.claude.com/docs/en/best-practices), via [done is not the effect](../docs/classes/done-is-not-the-effect.md)).
- 2026-11-22: a vendor reports a harness change, which included a pre-exit check against the task, raising its Terminal Bench 2.0 score from 52.8 to 66.5; the figure is for the whole change, not the check alone, and it is vendor data ([LangChain](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)).
- 2026-11-22: in one study, agents that did not read every file they were asked to review gave a misleading account of the review most of the time, which is what a report-only stop rests on ([claims from plausibility](../docs/classes/claims-from-plausibility.md)).

## Evidence against

- 2026-11-22: after eight blocks in a row Claude Code overrides the next one and ends the turn; the count resets when the agent calls a tool, and an environment variable raises the cap ([Claude Code hooks](https://code.claude.com/docs/en/hooks)).
- 2026-11-22: a script that exits 1 without valid JSON output does not block; it is a non-blocking error and the agent stops anyway.
- 2026-11-22: the hook checks only what its script checks. In one incident a supervisor marked six worker runs done on exit code 0, and none had opened a pull request ([done is not the effect](../docs/classes/done-is-not-the-effect.md), INC-456).
- 2026-11-22: it costs the check's run time at every stop, and a slow suite makes each turn end slowly.

## Guards

- [claims-from-plausibility](../docs/classes/claims-from-plausibility.md)
- [done-is-not-the-effect](../docs/classes/done-is-not-the-effect.md)
