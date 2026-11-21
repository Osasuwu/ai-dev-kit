---
kind: habit
why: A green build does not show that the feature works.
applies_when: an agent changes code that a person uses
last_reviewed: 2026-10-15
---

# Run the app before calling it done

## Check

Ask the agent what it ran, and look for the run in its log.

## Learn

- [A talk on feedback, 2:12](https://example.com/talk?t=132): why the agent needs to see the result.
- [A second talk, 20:51](https://example.com/other?t=1251): proof that goes stale.

## Evidence for

- 2026-10-15: a change passed its tests and failed on the device.
- 2026-10-15: a second case from the same team.

## Evidence against

- 2026-10-15: running the app costs a sandbox with every dependency.

## Guards

- [alpha](../docs/classes/alpha.md)
- [irreversible-effects](../docs/classes/cross.md)
