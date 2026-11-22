---
kind: config
why: A change checked only on the agent's machine or one Linux runner passes there and breaks on the operating system, device or environment it actually runs on.
applies_when: code an agent changes runs somewhere other than where it is tested: another OS, a device, people's machines or a differently configured service
last_reviewed: 2026-11-22
---

# Run the checks where the change will run, from one environment definition

## Check

Write down where the code runs (operating systems, shells, devices, Python or Node versions,
services), then compare it with where CI runs it:

```
grep -n "runs-on\|matrix\|os:" .github/workflows/*.yml
ls .devcontainer/devcontainer.json
grep -rn "setdefault\|os.environ.get\|process.env" tests/ | head
```

Every target on your list should appear in a job, by a matrix entry or a self-hosted runner
label. The agent, CI and people should build their toolchain from one definition. Tests should
set every variable they read, so a value from a developer's `.env` or the runner's environment
cannot fill a gap, and should refuse to start when a URL points at production.

## Fix

Add a matrix entry per target operating system and runtime version, and route jobs that need
a device or a GPU to a self-hosted runner by label. Turn off `fail-fast` when one target's
failure should not hide the others. Put the toolchain in a `devcontainer.json` that the agent
uses, and run CI in the same container. In test fixtures, set each variable the code reads
unconditionally rather than with a default, start real dependencies in containers where they
exist, and abort when a configured endpoint is a production one.

## Learn

- [Running variations of jobs in a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations): a matrix over operating systems and versions, and what `fail-fast` cancels.
- [Using self-hosted runners in a workflow](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow): sending a job to a runner with the device or hardware it needs.
- [Development containers](https://containers.dev/): one environment definition used by editors, agents and CI, and [devcontainers/ci](https://github.com/devcontainers/ci) to run CI inside it.
- [Testcontainers](https://testcontainers.com/): tests against the real engine in a container instead of a mock or the host's setup.

## Evidence for

- 2026-11-22: [the world differs from the assumed one](../docs/classes/world-differs-from-assumed.md) records changes that passed where they were written and broke on people's own machines, on a phone OS, and on Windows devices whose `python3` was a store stub.
- 2026-11-22: a firmware write-up makes the same point for hardware: a passing build does not show the firmware runs on the board, so the tests move onto real hardware ([errata hunter](https://dev.to/erratahunter/the-build-passed-so-why-doesnt-it-run-automating-firmware-tests-on-real-hardware-2m5i)); a practitioner's account.
- 2026-11-22: the twelve-factor guidance asks for the same backing services in development and production, for the same reason ([twelve-factor](https://12factor.net/dev-prod-parity)).

## Evidence against

- 2026-11-22: it covers only the targets someone listed; a target missing from the matrix is untested, and with `fail-fast` one failure cancels the jobs still running ([GitHub Docs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)).
- 2026-11-22: a shared container gives parity between the agent and CI only; the code still runs on machines and devices outside it ([the world differs from the assumed one](../docs/classes/world-differs-from-assumed.md)).
- 2026-11-22: a container's version or configuration can differ from production's, a hosted service does not run in one, and a self-hosted runner that keeps state between jobs brings its own failures.
- 2026-11-22: it costs runner minutes times the matrix size, Docker on every device, and the upkeep of any self-hosted runner or rig.

## Guards

- [world-differs-from-assumed](../docs/classes/world-differs-from-assumed.md)
