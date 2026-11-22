---
kind: config
why: A fact written in several files, or a workflow copied into several repositories, gets changed in some copies and not others, and each copy passes its own checks until they meet at run time.
applies_when: one value, list, schema, generated file or config template lives in more than one file or repository, and an agent edits any of them
last_reviewed: 2026-11-22
---

# Generate the copies from one source, and fail CI when a copy is stale

## Check

List what you keep in more than one place: a version number, a list of allowed values, a
schema, a section of a README built from code, a workflow or config copied into other
repositories. For each, ask which file is the source and what fails when a copy disagrees with
it. Then probe: edit one copy by hand on a throwaway branch and push. If CI stays green, the
copies can drift. For a generated file, this should go red:

```
<your generator command> && git diff --exit-code
```

## Fix

- Pick one source per fact and generate the other copies from it: a script, `cog` for text
  blocks inside files, `embedme` for code blocks in markdown that come from source files.
- Add a CI step that regenerates and fails on any difference, either `git diff --exit-code`
  after the generator or the tool's own check mode (`cog --check`). Make that step required.
- For a template or config copied into several repositories, record the source and check it:
  `cruft check` in each target's CI, or a sync action that opens a pull request in every
  repository whose copy is out of date.
- Where the platform lets you reference one definition instead of copying it (reusable
  workflows, shared presets), do that and delete the copies.

## Learn

- [cog: running and checking](https://cog.readthedocs.io/en/latest/running.html): `--check`, which fails when the generated blocks would change if run again.
- [cruft](https://cruft.github.io/cruft/): `cruft check` in CI, to catch a project drifting from the template it was made from.
- [repo-file-sync-action](https://github.com/BetaHuhn/repo-file-sync-action): pull requests that bring copied files in other repositories back in line.
- [Kubernetes verify-codegen.sh](https://github.com/kubernetes/kubernetes/blob/master/hack/verify-codegen.sh): a large project's check that committed generated code is current.

## Evidence for

- 2026-11-22: on a benchmark of multi-file refactors, incomplete refactoring is the dominant failure, and the best agent resolves 41.2% ([SWE-Bench ProMax](https://arxiv.org/html/2608.09802), via [copies of one truth drift](../docs/classes/copies-of-one-truth-drift.md)).
- 2026-11-22: on multi-hunk repairs, agents' accuracy fell as the hunks were further apart ([Nashid et al.](https://arxiv.org/abs/2511.11012), via the class doc).
- 2026-11-22: a review gate copied into two repositories had the same fail-open hole; it was fixed in one and kept passing unreviewed pull requests in the other until a cross-repository comparison found it (INC-165, one operator's record).
- 2026-11-22: in one operator's private audit, fixes that corrected only the one copy were nearly always followed by a recurrence (10 of 11); the audit is not verifiable.

## Evidence against

- 2026-11-22: the check compares only what the generator writes; a copy written by hand elsewhere is never compared, and a check not wired into CI does not run ([copies of one truth drift](../docs/classes/copies-of-one-truth-drift.md), "Breaks when").
- 2026-11-22: a sync pull request that nobody merges leaves the copy stale, a target that adapted the file needs a hand merge, and a retired sync leaves the copies behind.
- 2026-11-22: none of the studies on agents missing copies tests a protection, so the evidence that this one works is practice, not measurement. The Python packaging guide notes that some projects choose to live with duplication and rely on tests instead ([single-source version](https://packaging.python.org/en/latest/discussions/single-source-version/)).

## Guards

- [copies-of-one-truth-drift](../docs/classes/copies-of-one-truth-drift.md)
