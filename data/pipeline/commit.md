# Step 8: commit (the credentialed step)

Run by the session itself, the only step that holds the maintainer's credentials. It commits
files the earlier steps produced; it does not open, edit or summarise them.

Allowed: `git status`, `git add <named paths>`, `git commit`, `git push -u origin <branch>`,
`gh pr create --draft`, and the scripts below. Not allowed: any edit under `.github/`, a push
to `main`, `gh pr merge` in any form, `gh api`, changing labels, settings or branch
protection, opening any file in `<scratch>`.

1. `git status --porcelain`. Every changed or new path must be one of: `data/claims.jsonl`,
   `data/talks.jsonl`, `data/clusters/<letter>.json`, `data/cluster-index.tsv`, and
   `CHANGELOG.md` when step 2 adds to it. Anything else: stop, commit nothing, and name the
   path in the run's note.
2. When `CHANGELOG.md` exists, add one dated entry with the counts from the scripts' summary
   lines: talks picked, claims added, new clusters, group letter.
3. Stage those paths by name. Run `python data/pipeline/commit_guard.py`; a non-zero exit
   stops the run.
4. Commit: `data: rerun <YYYY-MM-DD>, <n> talks, <m> claims, group <letter>`.
5. `python scripts/pre_push_leak_gate.py --range origin/main..HEAD`; a non-zero exit stops
   the run.
6. Push the branch and open a draft pull request with
   `gh pr create --draft --title "data: rerun <YYYY-MM-DD>" --body-file <scratch>/pr-body.md`.

The run ends there. Review and merge are the human's.
