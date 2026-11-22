---
kind: config
why: A test runner that collected no tests, a linter that matched no files or a step whose tool was not installed exits 0, and the check reads green without having looked at the change.
applies_when: CI jobs or hooks run test runners, linters, scanners or uploaders on an agent's changes, and a green result is what lets the change merge
last_reviewed: 2026-11-22
---

# Make every check fail when it had nothing to check or its tool is missing

## Check

Search the workflows and hook scripts for the flags and habits that turn "nothing checked" into
a pass:

```
grep -rnE 'passWithNoTests|no-error-on-unmatched-pattern|\|\| *true|exit 0' .github/ .husky/ scripts/ 2>/dev/null
```

Then, for each required job, ask what it does when its input is empty. A quick probe: on a
throwaway branch, point the test command at a directory with no tests, or rename the tool it
calls, and push. The job should go red. If it goes green, the check passes on absence.

## Fix

Use each tool's fail-on-empty behaviour: pytest already exits non-zero when it collects no
tests, so do not map that code back to 0; drop `--passWithNoTests` from Jest; add `--fail-zero`
to Mocha; leave ESLint's error on an unmatched pattern on; set `fail_ci_if_error` on the
Codecov action; give a pre-commit hook that must always run `always_run`. Before the step that
needs a tool, add a preflight that fails the job when the tool is absent, for example
`command -v semgrep >/dev/null || { echo "semgrep missing"; exit 1; }`. For a hook launcher,
turn its own start-up failure into the exit code that blocks (exit 2 for a Claude Code
`PreToolUse` hook), because any other failure lets the call through.

## Learn

- [pytest exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html): exit code 5, no tests collected, and why it is a failure by default.
- [Jest CLI](https://jestjs.io/docs/cli): `--passWithNoTests`, the flag that turns an empty run into a pass.
- [Mocha CLI](https://mochajs.org/running/cli/): `--fail-zero`, off by default.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks.md): which exit codes block a tool call, and that a hook which fails any other way lets the action go ahead.

## Evidence for

- 2026-11-22: whether an empty run fails is a per-tool default, and the defaults differ: pytest fails, Mocha and Jest (with its flag) pass ([absence read as success](../docs/classes/absence-read-as-success.md), from each tool's docs).
- 2026-11-22: in the incidents behind [absence read as success](../docs/classes/absence-read-as-success.md), a hook whose interpreter was missing let every tool call through, and a reviewer that lost its shell kept posting verdicts; neither step failed, so nothing turned red. These are one operator's incidents.
- 2026-11-22: a study of about 142,000 industrial CI jobs describes jobs marked successful that did not finish all their tasks, though the jobs were not agent-written ([Aïdasso et al.](https://arxiv.org/abs/2509.14347v1), via the class doc).

## Evidence against

- 2026-11-22: a change that really has nothing to check now goes red, and the usual relief, mapping the exit code back to 0, brings the original gap back ([absence read as success](../docs/classes/absence-read-as-success.md), "Breaks when").
- 2026-11-22: some tools have no fail-on-empty option and report success on empty input; the preflight cannot see that.
- 2026-11-22: a tool that is present but degraded passes the preflight. A fail-closed hook launcher also blocked all legitimate work on machines where the interpreter was a stub, in one operator's record.

## Guards

- [absence-read-as-success](../docs/classes/absence-read-as-success.md)
