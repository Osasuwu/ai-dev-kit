# Step 8: commit (the credentialed step)

Run by the session itself, the only step that holds the maintainer's credentials. It commits
files the earlier steps produced; it does not open, edit or summarise them.

Allowed: git's status, add, commit and push, each with `-c core.fsmonitor=false` as written
below; `gh pr create --draft`; and the scripts below, each run as `python -I -B`. Not allowed:
any edit under `.github/`, a push to `main`, `gh pr merge` in any form, `gh api`, changing
labels, settings or branch protection, opening any file in `<scratch>`.

The counts below come from the scripts' own summary lines only: talks picked (`batches.py`),
claims added (`merge_claims.py`). The group letter is the one the session chose in step 5.
Nothing an agent returned goes into a commit message, `CHANGELOG.md` or the pull request.

1. When `CHANGELOG.md` exists, add one dated entry with those counts: talks picked, claims
   added, group letter.
2. The unchanged check (`README.md`: the tree, then the snapshot line), then
   `git -c core.fsmonitor=false status --porcelain`. Every changed or new
   path must be one of: `data/claims.jsonl`, `data/talks.jsonl`,
   `data/clusters/<letter>.json`, `data/cluster-index.tsv`, and `CHANGELOG.md` when step 1
   added to it. A rerun writes no card; the guard allows `cards/` for the card steps of the
   kit, not for this run. Anything else, a deletion included: stop, commit nothing, and name
   the path in the run's note.
3. Stage those paths by name:
   `git -c core.fsmonitor=false add <paths>`. Run
   `python -I -B data/pipeline/commit_guard.py`; a non-zero exit stops the run.
4. Make two new empty folders outside the repository and `<scratch>` (for example with
   `mktemp -d`): `<empty>` and `<body>`. Commit with `<empty>` as the hooks folder, so no
   hook an agent planted runs:
   `git -c core.hooksPath=<empty> -c core.fsmonitor=false commit -m "data: rerun <YYYY-MM-DD>, <n> talks, <m> claims, group <letter>"`.
5. `python -I -B scripts/pre_push_leak_gate.py --range origin/main..HEAD`; a non-zero exit
   stops the run.
6. Write `<body>/pr-body.md` yourself, a new file in the folder you just made, which no agent
   knows: talks picked, claims added, the group letter, and the line "Cluster and match
   details are in the maintainer's run folder, not here." Copy no agent-written text into it.
7. Push the branch with the same two settings
   (`git -c core.hooksPath=<empty> -c core.fsmonitor=false push -u origin <branch>`) and open
   a draft pull request with
   `gh pr create --draft --title "data: rerun <YYYY-MM-DD>" --body-file <body>/pr-body.md`.

The run ends there. Review and merge are the human's.
