# The weekly rerun poll

Decides once a week whether the data rerun ([`../data/pipeline/README.md`](../data/pipeline/README.md))
is due, from the talk digest's local state alone. It reads no claim, cluster or card, and no
threshold here is about claims. Issue #347.

- [`poll.py`](poll.py) — the decision, and the only writer of the poll's `runs.log` lines.
- [`events.json`](events.json) — conference end dates, from the official conference registry
  (the `ai-engineer` MCP's `list_conferences`). Kept by hand, by pull request.
- [`task.md`](task.md) — the prompt the weekly desktop task runs.

## What it reads

The digest's state folder, `~/briefings/aie/` on the maintainer's machine, and nothing else
in it:

- `seen.txt` — one talk or video id per line. The number of distinct non-blank ids is the
  talk count.
- `state.json` — only `publishedAt`: when the upstream corpus the digest copies last
  published, to say in the decision when it has gone quiet.
- `runs.log` — the poll's own earlier decisions (lines whose second field is `poll`; other
  writers' lines are skipped).

## The numbers

- **New talks:** 100
- **Weeks after an event ends:** 4
- **Corpus quiet after:** 21 days

A rerun is due when 100 or more ids were added to `seen.txt` since the last rerun that
finished, or when an event in `events.json` ended 4 weeks ago or more and no rerun has
finished since that date. 100 is two extraction batches of 50
(`data/pipeline/batches.py`), so a count-triggered rerun has enough new talks to form new
clusters. 4 weeks gives the event's recordings time to be published; a talk published later
is picked up by the next rerun, since a rerun skips only talks already in `data/talks.jsonl`.
An upstream corpus that has not published for over 21 days (three weekly cycles) is named in
every decision line, since `seen.txt` does not grow while it is quiet.

Before the first rerun finishes, the baseline is the poll's first line: that run records the
current count and exits. Events that came due before that line do not trigger a rerun.

Every date and ISO week here is UTC: the line's timestamp, "this week", and "4 weeks after".
Monday 09:00 local time is a Monday in UTC wherever local time is less than 9 hours ahead of
UTC; further east it is the previous UTC Sunday, which still gives one decision per week.

## runs.log

One line per decision, tab-separated:

```
<UTC time>  poll  <start|exit|done|failed|baseline>  seen=<count>  <reason>
```

- `start` and `exit` — the weekly decision. At most one per ISO week: a second run in the
  same week (a catch-up, a manual run) prints `skip` and writes nothing. A week whose clone
  could not be updated still gets its line: the task runs `poll.py decide --blocked
  "<why>"`, which records `exit clone not updated: <why>`. Two cases write no line, since the
  task then has no `poll.py` to run: the clone is missing (after a tamper stop it is moved
  aside), or the poll cannot be copied out of it.
- `done` and `failed` — the outcome of the rerun the last `start` opened, written by the task
  (`poll.py outcome done|failed "<note>"`). While a `start` has no outcome, every decision is
  `exit` with that as its reason, so a crashed run cannot start a second one. A `failed` rerun
  moves no baseline: its talks still count as new and its events stay due.
- `baseline` — written by hand (`poll.py baseline "<why>"`), below. Not a weekly decision.

Other writers' lines (the digest's own) are skipped. Lines are only ever appended.

## When a line needs a person

- **A tamper stop.** The rerun stopped at its snapshot, an unchanged check, `commit.md`'s
  path list or `commit_guard.py`, or before it had a snapshot line. The task's last line
  starts `held:` and names what changed. It records no outcome, commits nothing, and moves
  the clone, as it is, to `~/aie-poll/held-<date>` without running git in it, since a changed
  git config can run code through any git command. Every later week ends with "clone
  missing" and writes no line. Look at the held folder, outside the task (its git config,
  hooks, Claude Code settings, agents, files the run left), and find the cause. Then clone
  the repo afresh to `~/aie-poll/ai-dev-kit`, do its setup (below), and from a clean
  checkout of `main` record `python -I -B poll/poll.py outcome failed "<why>"`.
- **A rerun that never recorded its outcome otherwise.** The session stopped part way: the
  app closed, or it waited on a permission prompt nobody answered. Every week then exits with
  `rerun started <date> has no outcome line`, or `clone not updated` while the clone is
  dirty. Check the clone first as above. Then, from a clean checkout of `main`, record the
  outcome: `outcome failed "<why>"`, or `outcome done "<pull request URL>"` when the run did
  finish. A stopped run's work is on its `rerun/<date>` branch in the task's clone.
- **`seen.txt shrank`.** The digest's list was rebuilt or trimmed, and a count since the old
  baseline would be wrong. Every week exits until a new baseline is set:
  `python -I -B poll/poll.py baseline "<why>"` records today's count. Events are unaffected.
- **`clone not updated`.** The task's clone could not be fetched or switched to
  `origin/main`, or holds uncommitted or ignored files. Its reason names the command. A
  failed rerun's work is kept on its `rerun/<date>` branch (`task.md` step 4) and a
  tamper-stopped clone is moved aside, so the cause is no network, a session that stopped
  part way, or a change made in the clone by hand. The task never cleans the clone itself:
  the files are what a person needs to see.

The task runs `poll.py` from a copy it takes out of `origin/main` each week, never from the
clone's working tree, and runs every git command in the clone with
`-c core.fsmonitor=false -c core.hooksPath=<empty>` (an empty folder), as the rerun's commit
step does. That stops planted hooks and file monitors, not code that git config runs
(a credential helper, `core.sshCommand`, a clean or smudge filter;
[`../data/pipeline/README.md`](../data/pipeline/README.md) § What this split does not stop).
The rerun's snapshot and unchanged checks catch a changed config; after one of them stops a
run, the task moves the clone aside so no later week runs git in it.

## Setup, once per device

1. A clone of this repo used only by the task, at `~/aie-poll/ai-dev-kit`. The task switches it
   to `origin/main` every week, so do no work in it.
2. The rerun's own setup ([`../data/pipeline/README.md`](../data/pipeline/README.md) § Setup),
   done for that clone.
3. A desktop scheduled task: weekly, Monday 09:00 local time, whose prompt is the text of
   [`task.md`](task.md) below its heading. Its working folder is `~/aie-poll`, never the
   clone: a session loads the Claude Code settings, hooks and agents of the folder it starts
   in, before the task can check the clone. It runs unattended, so a tool call that asks for
   permission stalls it; see *When a line needs a person*.

## A missed week

The desktop app runs a scheduled task that came due while the app was closed when the app
next opens. That catch-up is the app's, not the poll's. It is one run however many weeks were
missed, so a missed week leaves no line of its own; the catch-up run decides on everything
accumulated since. The once-per-week rule keeps a catch-up early in the week from being
followed by a second line from the regular run.

## Fallback

If the poll does not work out, the rerun runs on a fixed schedule instead: 1 February, May,
August and November, first run 2027-02-01. Record the reason in the issue that switches it.

## Keeping events.json current

An event missing from `events.json` triggers nothing by date; only the new-talk count catches
its talks. When no listed event ends after today, every decision line says
`events.json lists no event ending after <date>`. Add the next events' end dates when the
registry publishes them.
