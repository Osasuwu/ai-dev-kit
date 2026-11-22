---
kind: config
why: A test marked as expected to fail, skipped, or written with no assertion stays green whatever the code does, and an agent adds such tests or markers without anyone noticing the count.
applies_when: an agent writes or changes tests in a suite whose green run you treat as evidence
last_reviewed: 2026-11-22
---

# Make expected failures strict, count the skips, and lint for tests that assert nothing

## Check

For pytest, read the configuration and the skip list:

```
grep -n "xfail_strict" pyproject.toml pytest.ini setup.cfg tox.ini
python -m pytest -rsx -q | tail -n 30
```

`xfail_strict = true` should be set, so an expected failure that passes fails the run. The
skip and expected-failure counts should be compared with the base branch in CI, and a test file
that collects nothing should fail. Then check that the linter flags tests with no assertion, an
assertion under a condition or inside an `except`, and disabled tests: Ruff's `PT` rules for
pytest, `jest/expect-expect`, `jest/no-conditional-expect` and `jest/no-disabled-tests` for
Jest. Finally, look for `|| true` or `continue-on-error` around the test step.

## Fix

Set `xfail_strict = true` in the pytest configuration, and give each expected failure a
`raises=` with the exception it expects, so it does not pass for an unrelated error. Add a short
CI step that counts skipped and expected-failure tests on the pull request and on the base, and
fails when the count grows without a matching note in the pull request. Keep pytest's own exit
code for a run that collects no tests; do not mask it. Turn on the assertion lint rules for your
framework and run them in CI on test files.

## Learn

- [pytest, how to use skip and xfail](https://docs.pytest.org/en/stable/how-to/skipping.html): the `strict` option, and why a non-strict expected failure that passes stays green.
- [eslint-plugin-jest `expect-expect`](https://github.com/jest-community/eslint-plugin-jest/blob/main/docs/rules/expect-expect.md): a test with no assertion, and how to tell the rule about helper functions that assert.
- [Ruff PT017](https://docs.astral.sh/ruff/rules/pytest-assert-in-except/): an assertion inside `except` that runs only when the code fails.
- [Test smells catalogue](https://testsmells.org/pages/testsmells.html): the wider list of tests that cannot fail, behind tsDetect for Java.

## Evidence for

- 2026-11-22: by default pytest reports an expected failure that passes as a pass; strict mode makes it fail the suite ([pytest docs](https://docs.pytest.org/en/stable/how-to/skipping.html)).
- 2026-11-22: [tests that cannot fail](../docs/classes/tests-that-cannot-fail.md) records non-strict expected-failure markers that hid failing tests until CI caught them, and a test whose assertion sat under an `if` that skipped it in exactly the case it was written for; both are private records, not verifiable.
- 2026-11-22: test-disabling changes are rarely undone: in a study of 15 Java systems, 41% of disabled tests were never brought back (as of 2021-08, [ESEC/FSE 2021](https://2021.esec-fse.org/details/fse-2021-papers/78/How-Disabled-Tests-Manifest-in-Test-Maintainability-Challenges-)).

## Evidence against

- 2026-11-22: it catches tests that do not run, not tests that run and cannot fail; an assertion true for nearly any result, or an expected value copied from the code's output, passes every rule here ([tests that cannot fail](../docs/classes/tests-that-cannot-fail.md)).
- 2026-11-22: a strict marker without `raises=` still passes when the test fails for an unrelated reason.
- 2026-11-22: an assertion in a helper the lint rule does not know reads as no assertion, and the rules differ by framework, so check yours covers the shape you fear.
- 2026-11-22: a new skip with a plausible reason gets through unless something counts skips and a person reads the list when it grows.

## Guards

- [tests-that-cannot-fail](../docs/classes/tests-that-cannot-fail.md)
- [absence-read-as-success](../docs/classes/absence-read-as-success.md)
