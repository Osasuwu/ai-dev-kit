---
kind: config
why: A check that is not required can fail and the merge still goes through.
applies_when: changes merge through a branch rule
last_reviewed: 2026-11-01
---

# Require the checks you merge on

## Check

Read the required list back from the platform.

## Fix

Add each check to the branch rule.

## Learn

- [Protected branches](https://example.com/protected-branches): what a required check blocks.

## Evidence for

- 2026-11-01: a change merged while its check was red.

## Evidence against

- 2026-11-01: none found.

## Guards

- [alpha](../docs/classes/alpha.md)
