---
kind: config
why: When the agent's formatter differs from the repository's, its diff reformats whole files, and the change you asked for hides among hundreds of lines nobody reviews.
applies_when: an agent edits code in a repository that has, or should have, one code formatter
last_reviewed: 2026-11-22
---

# Pin the formatter to an exact version and check formatting in CI

## Check

Two things must both hold.

- The formatter's version is exact wherever it is installed: no range such as `^3.0.0` or
  `>=24` in the package manifest, requirements file or pre-commit config, and the lockfile
  agrees. The agent's environment, CI and people's machines install that same version.
- CI fails on unformatted code, with the formatter's check mode:

```
grep -n -- "--check" .github/workflows/*.yml
```

`ruff format --check .`, `prettier --check .` and `black --check .` are the usual forms. Then
look at an agent pull request: its diff should hold no hunk that only changes whitespace,
quotes, wrapping or import order in lines the task did not touch.

## Fix

Install the formatter at one exact version (for npm, `--save-exact`), in the same file every
environment installs from. Add a CI step that runs it in check mode on the whole repository and
fails. Bring the repository in line with one formatting-only commit, merged on its own; git's
`blame.ignoreRevsFile` setting can hide that commit from blame. Run the same pinned formatter in
the agent's loop, after its edits, so its diff arrives already formatted.

## Learn

- [Prettier, install](https://prettier.io/docs/install): why even a patch release can change output, and the advice to pin an exact version and check it in CI.
- [Google engineering practices, what to look for in a review](https://google.github.io/eng-practices/review/reviewer/looking-for.html): why style changes go in their own change, not mixed with others.

## Evidence for

- 2026-11-22: Prettier's own documentation says a patch release can format slightly differently, so an unpinned formatter changes untouched lines on its own ([Prettier](https://prettier.io/docs/install)).
- 2026-11-22: Google's reviewer guide asks authors not to combine major style changes with other changes, since they hide what the change does ([Google eng-practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html)).
- 2026-11-22: whole files reformatted, so the real change is hard to find, is one of the listed shapes of [scope overreach](../docs/classes/scope-overreach.md).

## Evidence against

- 2026-11-22: it removes formatting noise only; a rename, a deletion, an extra feature or a changed default in the same diff passes it ([scope overreach](../docs/classes/scope-overreach.md)).
- 2026-11-22: it costs a CI step and one large formatting commit to bring the repository in line, which touches every open branch.
- 2026-11-22: a pinned version has to be upgraded deliberately, and each upgrade is its own formatting commit.

## Guards

- [scope-overreach](../docs/classes/scope-overreach.md)
