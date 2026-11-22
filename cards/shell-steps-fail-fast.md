---
kind: config
why: A shell step keeps going after a failed command, a failed pipe stage or an empty variable, so a check ends green and a delete built from `$VAR/` runs on a path that lost its first part.
applies_when: an agent writes or runs shell scripts and CI steps, especially cleanups and deletes whose target comes from a variable, a glob or a `cd`
last_reviewed: 2026-11-22
---

# Run shell steps fail-fast, and make an empty expansion stop the script

## Check

In GitHub Actions, find steps that run bash without `pipefail`:

```
grep -rnE '^\s*(run:|shell:)' .github/workflows/ | grep -v 'shell: bash'
```

A `run:` step with no `shell:` on Linux runs `bash -e`, without `pipefail`; `shell: bash` adds
it. In committed scripts, run `shellcheck` and look for SC2115 (a
delete path built from a variable that may be empty) and SC2164 (a `cd` with no `|| exit`). Then
read the head of each script for `set -euo pipefail` or its equivalent.

## Fix

- Set `defaults: run: shell: bash` at the top of each workflow, so every step runs with
  `-eo pipefail`.
- Start each bash script with `set -euo pipefail`. `-u` fails on an unset variable.
- In any path that a delete or a move uses, write `${VAR:?}` instead of `$VAR`: an unset or
  empty value then stops the script instead of shrinking `"$VAR/"*` to `/*`.
- Write `cd dir || exit 1` before anything that depends on the directory.
- In bash, `shopt -s failglob` refuses a command whose glob matches nothing; in PowerShell,
  `Set-StrictMode -Version Latest` refuses uninitialized variables.
- Run ShellCheck in CI over committed shell scripts.

## Learn

- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): the exact command line each `shell:` value runs, and which ones include `pipefail`.
- [ShellCheck SC2115](https://www.shellcheck.net/wiki/SC2115): the `${VAR:?}` fix for a delete whose path starts with a variable.
- [ShellCheck SC2164](https://www.shellcheck.net/wiki/SC2164): why a failed `cd` lets the rest of the script run in the wrong directory.
- [BashFAQ/105](https://mywiki.wooledge.org/BashFAQ/105): the places where `set -e` does not stop the script.

## Evidence for

- 2026-11-22: a shipped launcher script ran `rm -rf "$STEAMROOT/"*` with the variable empty and deleted users' files across the system; the class predates agents ([destructive op on a computed target](../docs/classes/destructive-op-on-computed-target.md), from [steam-for-linux#3671](https://github.com/ValveSoftware/steam-for-linux/issues/3671)).
- 2026-11-22: bash leaves `pipefail` off by default, so a failure early in a pipeline is lost and the step reports the last command's status ([absence read as success](../docs/classes/absence-read-as-success.md), from the Bash manual).

## Evidence against

- 2026-11-22: none of these stop a variable that is set and wrong. In the agent incidents where `rm -rf "$HOME"` hit the real home directory, `$HOME` held a real path, so `${HOME:?}` and `set -u` would not have fired ([destructive op on a computed target](../docs/classes/destructive-op-on-computed-target.md)).
- 2026-11-22: `set -e` is ignored inside `if` and `while` conditions, in all but the last member of an `&&` or `||` list, and in command substitutions; ShellCheck stops reporting SC2164 once `set -e` appears ([BashFAQ/105](https://mywiki.wooledge.org/BashFAQ/105)).
- 2026-11-22: a `cd` into a directory that exists but is the wrong one passes `|| exit`. A one-off command an agent types carries these guards only if the agent writes them, and `cmd` or PowerShell steps fail differently.

## Guards

- [destructive-op-on-computed-target](../docs/classes/destructive-op-on-computed-target.md)
- [absence-read-as-success](../docs/classes/absence-read-as-success.md)
