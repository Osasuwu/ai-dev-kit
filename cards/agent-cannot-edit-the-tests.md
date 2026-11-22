---
kind: config
why: An agent pushed to make tests pass can edit, weaken or delete the tests instead of fixing the code, and the green suite then measures the edit.
applies_when: an agent changes code under a test suite it can also write to, and you take its green run as the sign the task is done
last_reviewed: 2026-11-22
---

# Let the agent run the tests but not change them, and flag every change to them

## Check

Two places.

- In the agent's session: ask it, in a scratch task, to change an assertion in a test file. The
  edit should be refused, by a hook or a read-only mount, and so should the same change made
  with a shell command.
- In CI: for a recent agent pull request, list what it changed under the test paths.

```
git diff --name-only origin/main...HEAD -- tests/ '*_test.*' '*.spec.*'
```

Each change there should be flagged on the pull request, and should need a named owner's
approval before the merge.

## Fix

Block writes to the test paths during the agent's run: a `PreToolUse` hook that checks the
target path against a list of protected patterns and exits with code 2 refuses the edit in
Claude Code; a sandbox that mounts the tests read-only also covers shell writes. Give a
legitimate test change a separate path: a person, or a task whose only job is the tests. In CI,
add a step that lists changes to test files, specs and acceptance criteria and posts them on the
pull request, and set a code owner for those paths with code-owner review required.

## Learn

- [ImpossibleBench](https://arxiv.org/html/2510.20270): how often agents modify tests on tasks they cannot solve honestly, and how read-only tests change that.
- [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide.md): a hook that blocks edits to protected files by path.
- [EvilGenie](https://arxiv.org/html/2511.21654): flagging any edit or deletion of test files as reward hacking, and the forms of gaming that touch no test.

## Evidence for

- 2026-11-22: in ImpossibleBench, read-only test access stopped test-modification attempts while keeping legitimate performance (benchmark measurement, [ImpossibleBench](https://arxiv.org/html/2510.20270)).
- 2026-11-22: EvilGenie detects reward hacking by diffing each run against the test files and flagging any edit or deletion ([EvilGenie](https://arxiv.org/html/2511.21654)).
- 2026-11-22: on GitHub, a pull request that touches a path with a code owner needs that owner's approval when the branch rule requires it ([about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).

## Evidence against

- 2026-11-22: the agent can game the test without editing it, by hard-coding expected outputs or special-casing test inputs in the production code; in EvilGenie that was the most common form for one agent ([proxy optimisation](../docs/classes/proxy-optimisation.md)).
- 2026-11-22: a hook guards only the routes it matches and only where it is installed; a write by a shell command it does not inspect goes through.
- 2026-11-22: test changes are often legitimate, so the flag fires on honest work and gets waved through, and an owner may approve without reading.
- 2026-11-22: it covers test files only; a criterion moved in the pull request text or a placeholder in a gated field passes.

## Guards

- [proxy-optimisation](../docs/classes/proxy-optimisation.md)
- [tests-that-cannot-fail](../docs/classes/tests-that-cannot-fail.md)
