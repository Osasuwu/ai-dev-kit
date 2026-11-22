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
  "<why>"`, which records `exit clone not updated: <why>`.
- `done` and `failed` — the outcome of the rerun the last `start` opened, written by the task
  (`poll.py outcome done|failed "<note>"`). While a `start` has no outcome, every decision is
  `exit` with that as its reason, so a crashed run cannot start a second one. A `failed` rerun
  moves no baseline: its talks still count as new and its events stay due.
- `baseline` — written by hand (`poll.py baseline "<why>"`), below. Not a weekly decision.

Other writers' lines (the digest's own) are skipped. Lines are only ever appended.

## When a line needs a person

- **A rerun that never recorded its outcome.** The session stopped part way: the app closed,
  or it waited on a permission prompt nobody answered. Every week then exits with
  `rerun started <date> has no outcome line`. Look at what the run left (its `rerun/<date>`
  branch in the task's clone, its draft pull request if any), then, from the clone, record it:
  `python -I -B poll/poll.py outcome failed "<why>"`, or `outcome done "<pull request URL>"`
  when it did finish.
- **`seen.txt shrank`.** The digest's list was rebuilt or trimmed, and a count since the old
  baseline would be wrong. Every week exits until a new baseline is set:
  `python -I -B poll/poll.py baseline "<why>"` records today's count. Events are unaffected.
- **`clone not updated`.** The task's clone could not be switched to `origin/main`. Its reason
  names the command; a failed rerun's work is kept on its `rerun/<date>` branch (`task.md`
  step 4), so the cause is usually elsewhere: no network, or a change made in the clone by
  hand.

## Setup, once per device

1. A clone of this repo used only by the task, at `~/aie-poll/ai-dev-kit`. The task switches it
   to `origin/main` every week, so do no work in it.
2. The rerun's own setup ([`../data/pipeline/README.md`](../data/pipeline/README.md) § Setup),
   done for that clone.
3. A desktop scheduled task: weekly, Monday 09:00 local time, whose prompt is the text of
   [`task.md`](task.md) below its heading. It runs unattended, so a tool call that asks for
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
