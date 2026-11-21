# The data rerun

How `data/` is regenerated when new conference talks come out. The steps are agent-run
instruction files plus five small scripts; a run is an agent session that follows this file.
Where the data comes from and how to refetch it: [`../sources.md`](../sources.md).

## The split

A run reads text from outside pages, and the session that starts it holds the maintainer's
credentials. The two are kept apart:

- **Steps that read outside text run in subagents with no shell and no GitHub tool.**
  [`agents/aie-fetcher.md`](agents/aie-fetcher.md) fetches; it has file tools, `WebFetch` and
  the conference's MCP tools. [`agents/aie-worker.md`](agents/aie-worker.md) extracts,
  clusters and matches; it has file tools only. Their `tools:` lists are what the harness
  enforces, so the definitions must be installed (Setup), not pasted into a prompt.
- **The session itself (the credentialed step) does not read that text.** It runs the
  scripts, spawns the agents, reads only the scripts' summary lines and the agents' short
  returns, and commits produced files under `cards/`, `data/` (not `data/pipeline/`) and
  `CHANGELOG.md`, checked by [`commit_guard.py`](commit_guard.py). It never touches `.github/`,
  never pushes to `main` and never merges: a human reviews and merges the pull request.

## Setup, once per device

1. Copy `data/pipeline/agents/aie-fetcher.md` and `aie-worker.md` into `~/.claude/agents/`.
   Re-copy them when they change.
2. The `ai-engineer` MCP server is connected (the fetcher's `mcp__ai-engineer__*` tools).
3. The repo's pre-push leak gate is installed (`scripts/pre_push_leak_gate.py`, install steps
   in its docstring).

## A run

`<scratch>` is a new folder outside every repository, for example `~/aie-rerun/<YYYY-MM-DD>/`.
Everything fetched stays there; nothing fetched is committed. `<events>` is a regular
expression for the event names in scope, for example `2027`. Run from the repo root, on a new
branch cut from `origin/main`.

**Unchanged check, before every script.** The agents can write files, so before steps 2, 4,
6, 7 and 8 run, the session checks that the pipeline is still the one on `origin/main`: both
`git diff --quiet origin/main -- data/pipeline` and `git status --porcelain --ignored --
data/pipeline` print nothing and exit 0 (the second catches new and ignored files, such as
a planted module). Any output stops the run before the script runs: commit nothing and name
the paths in the run's note.

1. **Fetch.** Spawn `aie-fetcher` with `<scratch>` and `<events>`; it follows
   [`fetch.md`](fetch.md) and writes `<scratch>/talks.json`.
2. **Batch.** `python data/pipeline/batches.py <scratch>/talks.json <scratch>/batches 50 --event-pattern "<events>" --known data/talks.jsonl`.
   Talks already published are skipped. "picked 0" ends the run here with a note: nothing new.
3. **Extract.** One `aie-worker` per `<scratch>/batches/batch-NN.json`, in parallel, each
   following [`extract.md`](extract.md) and writing `<scratch>/claims/batch-NN.jsonl`.
4. **Merge.** `python data/pipeline/merge_claims.py --claims-dir <scratch>/claims --data data --areas-out <scratch>/areas --index <scratch>/batches/index.json`.
   Published claims keep their ids; new ones are numbered after the highest. A non-zero exit
   (bad batch lines, named in its output) stops the run; the merge has written nothing, so the
   step reruns cleanly once the batch is fixed.
5. **Cluster.** The new group letter is the next one after the last `data/clusters/?.json`
   (`G` on the first rerun). Spawn `aie-worker` with the letter and `<scratch>/areas/`; it
   follows [`cluster.md`](cluster.md) and writes `data/clusters/<letter>.json`.
6. **Index and match.** `python data/pipeline/build_index.py`, then spawn `aie-worker` with
   the letter and `<scratch>`; it follows [`match.md`](match.md) and writes
   `<scratch>/matches.jsonl` and `<scratch>/match-summary.md`, which stay on this machine for
   the maintainer.
7. **Check.** `python data/pipeline/check_data.py`. Any problem stops the run before the
   commit.
8. **Commit.** Follow [`commit.md`](commit.md).

A run ends with a draft pull request and a one-line note: talks picked, claims added, new
clusters, and the pull request URL, or the step where it stopped and why.

## What this split does not stop

- An agent's `Write` is not limited to a path. It could write outside `<scratch>` and `data/`,
  for example into `.git/hooks/` or `.claude/`, which run code in the credentialed session
  without any script step; the commit guard reads staged paths only. The unchanged check
  covers `data/pipeline/` alone.
- An agent's text reaches the public pull request only through the data files the scripts
  check (`check_data.py`); the description is written from counts. A data file can still
  carry injected text in a field, which `check_data.py` does not judge: the human review does.
- "The session does not read outside text" is an instruction to the session, not a limit.
- Spawned as a general-purpose agent instead of `aie-fetcher` or `aie-worker`, a step gets every
  tool the session has.
- The guard is a script the session runs; a session that skips it is stopped only by the
  human review of the pull request.
