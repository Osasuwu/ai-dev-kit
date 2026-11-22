---
kind: config
why: A new test that passes before the fix as well as after it proves nothing about the fix, and an agent's tests often pass on both because their expected values came from the code.
applies_when: an agent adds tests with a bug fix or a feature, and you take the new tests going green as evidence the change works
last_reviewed: 2026-11-22
---

# Require each new test to fail on the parent commit, and mutate the code the diff touched

## Check

For a recent pull request that added tests, run the new tests against the old code:

```
git diff --name-only BASE...HEAD -- tests/
git checkout BASE -- $(git diff --name-only --diff-filter=M BASE...HEAD | grep -v '^tests/')
python -m pytest <the new test files> -q
git checkout HEAD -- .
```

Each test the pull request added for a fix should fail there, on an assertion, not on an
import error or a missing name. If they all pass, they do not test the fix. Then check whether CI
does this for you, and whether a mutation-testing job runs on the changed lines with a threshold
that can fail the build.

## Fix

Add a CI job that finds the tests a pull request added, checks out the parent commit's
non-test code beside them, runs them, and fails when any of them passes or fails for a reason
other than an assertion. Exempt refactors explicitly, since they have no expected red. Add
diff-scoped mutation testing, such as `cargo mutants --in-diff`, Stryker with a `break`
threshold, or mutmut on the changed modules; start it as a report in review and make it blocking
on the paths where a missed bug cannot be undone.

## Learn

- [SWE-bench dataset card](https://huggingface.co/datasets/princeton-nlp/SWE-bench/blob/main/README.md): the `FAIL_TO_PASS` field, tests that fail before the fix and pass after it.
- [cargo-mutants, `--in-diff`](https://mutants.rs/in-diff.html): mutating only the code a diff touched.
- [Stryker configuration](https://stryker-mutator.io/docs/stryker-js/configuration/): the `break` threshold, which by default never fails the build.
- [State of mutation testing at Google](https://research.google/pubs/state-of-mutation-testing-at-google/): how mutation testing scoped to a change runs at the scale of a large company.

## Evidence for

- 2026-11-22: SWE-bench defines a fix's tests as the ones that fail before it and pass after it, so a test that passes on the parent does not count for the fix ([SWE-bench](https://huggingface.co/datasets/princeton-nlp/SWE-bench/blob/main/README.md)).
- 2026-11-22: Google runs mutation testing on the code changes its engineers author or review ([Google](https://research.google/pubs/state-of-mutation-testing-at-google/)), an industrial report.
- 2026-11-22: [tests that cannot fail](../docs/classes/tests-that-cannot-fail.md) records tests whose expected value or mock was taken from the implementation, so a wrong implementation matched its own test; a test of that kind written for a fix often passes on the parent too, which is what this check catches.

## Evidence against

- 2026-11-22: failing on the parent does not make a test strong: differential testing found 29.6% of plausible patches on a public benchmark behaved differently from the reference fix while passing its fail-to-pass tests (as of 2025-03, [PatchDiff](https://arxiv.org/abs/2503.15223)).
- 2026-11-22: a test can fail on the parent for the wrong reason, a refactor has no expected red, and a mock that flips from red to green can still disagree with the real dependency.
- 2026-11-22: mutation testing is the costliest CI rung, growing with mutants times covering tests, and needs triage of mutants that change nothing observable.
- 2026-11-22: a diff-scoped run checks the changed code, not tests weakened elsewhere, and cannot mutate a security control that is missing ([tests that cannot fail](../docs/classes/tests-that-cannot-fail.md)).

## Guards

- [tests-that-cannot-fail](../docs/classes/tests-that-cannot-fail.md)
