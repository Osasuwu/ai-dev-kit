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

- `seen.txt` — one talk or video id per line. Its line count is the talk count.
- `state.json` — only `publishedAt`, to say in the decision when the digest has gone quiet.
- `runs.log` — the poll's own earlier decisions (lines whose second field is `poll`; other
  writers' lines are skipped).

## The numbers

- **New talks:** 100
- **Weeks after an event ends:** 4
- **Digest stale after:** 21 days

A rerun is due when 100 or more ids were added to `seen.txt` since the last rerun that
finished, or when an event in `events.json` ended 4 weeks ago or more and no rerun has
finished since that date. 100 is two extraction batches of 50
(`data/pipeline/batches.py`), so a count-triggered rerun has enough new talks to form new
clusters. 4 weeks gives the event's recordings time to be published; a talk published later
is picked up by the next rerun, since a rerun skips only talks already in `data/talks.jsonl`.
A digest that has not published for over 21 days (three weekly cycles) is named in every
decision line, since its `seen.txt` no longer grows.

Before the first rerun finishes, the baseline is the poll's first line: that run records the
current count and exits. Events that came due before that line do not trigger a rerun.

## runs.log

One line per decision, tab-separated:

```
<UTC time>  poll  <start|exit|done|failed>  seen=<count>  <reason>
```

- `start` and `exit` — the weekly decision. At most one per ISO week: a second run in the
  same week (a catch-up, a manual run) prints `skip` and writes nothing.
- `done` and `failed` — the outcome of the rerun the last `start` opened, written by the task
  (`poll.py outcome done|failed "<note>"`). While a `start` has no outcome, every decision is
  `exit` with that as its reason, so a crashed run cannot start a second one. A `failed` rerun
  moves no baseline: its talks still count as new and its events stay due.

## Setup, once per device

1. A clone of this repo used only by the task, at `~/aie-poll/ai-dev-kit`. The task switches it
   to `origin/main` every week, so do no work in it.
2. The rerun's own setup ([`../data/pipeline/README.md`](../data/pipeline/README.md) § Setup),
   done for that clone.
3. A desktop scheduled task: weekly, Monday 09:00 local time, whose prompt is the text of
   [`task.md`](task.md) below its heading.

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
