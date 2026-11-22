"""Weekly poll: is a data rerun due? (#347)

Usage:
    python -I -B poll/poll.py decide [--state-dir DIR] [--events FILE] [--dry-run] [--now ISO]
    python -I -B poll/poll.py outcome done|failed "<note>" [--state-dir DIR] [--now ISO]

`decide` reads the talk digest's state folder (default `~/briefings/aie/`) and nothing else
there: `seen.txt` (one talk or video id per line), `state.json` (its `publishedAt`) and
`runs.log`. It prints one line, `start <reason>`, `exit <reason>` or `skip <reason>`, and for
`start` and `exit` appends the same decision to `runs.log`. `skip` means a decision was
already recorded this ISO week (a catch-up run or a manual run after the weekly one); it
writes nothing. `--dry-run` prints the decision and writes nothing.

`outcome` closes the rerun the last `start` line opened, with `done` (the run ended in a draft
pull request, or found nothing new) or `failed` (it stopped before that). Until one is
recorded, `decide` starts no second rerun.

A rerun is due when either holds:
- at least NEW_TALKS_THRESHOLD lines were added to `seen.txt` since the baseline: the `seen`
  count of the last `start` closed as `done`, or of the poll's first line when no rerun has
  finished yet;
- an event in `events.json` ended WEEKS_AFTER_EVENT weeks ago or more, that moment falls
  after the poll's first line, and no rerun started since then has finished.

A failed rerun moves neither: its talks still count as new and its events stay due.

runs.log lines written here are tab-separated:
    <UTC time>  poll  <start|exit|done|failed>  seen=<count or ->  <reason>
Lines whose second field is not `poll` belong to other writers and are ignored.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple

NEW_TALKS_THRESHOLD = 100
WEEKS_AFTER_EVENT = 4
STALE_DIGEST_DAYS = 21

DEFAULT_STATE_DIR = Path("~/briefings/aie")
DEFAULT_EVENTS = Path(__file__).with_name("events.json")
KINDS = ("start", "exit", "done", "failed")


class Line(NamedTuple):
    when: date
    kind: str
    seen: int | None


def parse_date(text: str) -> date | None:
    try:
        return date.fromisoformat(text[:10])
    except (TypeError, ValueError):
        return None


def read_log(path: Path) -> list[Line]:
    """The poll's own lines from runs.log, oldest first. Raises ValueError on a bad one."""
    if not path.exists():
        return []
    lines = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fields = raw.split("\t")
        if len(fields) < 2 or fields[1] != "poll":
            continue
        when = parse_date(fields[0])
        if len(fields) < 5 or when is None or fields[2] not in KINDS:
            raise ValueError(
                f"runs.log line {number} is a poll line this poll cannot read"
            )
        seen = fields[3].removeprefix("seen=")
        lines.append(Line(when, fields[2], int(seen) if seen.isdigit() else None))
    return lines


def count_seen(path: Path) -> int | None:
    if not path.exists():
        return None
    return len(
        {x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()}
    )


def digest_note(path: Path, today: date) -> str | None:
    try:
        published = parse_date(
            json.loads(path.read_text(encoding="utf-8"))["publishedAt"]
        )
    except (OSError, ValueError, KeyError, TypeError):
        published = None
    if published is None:
        return "state.json has no readable publishedAt"
    age = (today - published).days
    if age > STALE_DIGEST_DAYS:
        return f"digest last published {published} ({age} days ago)"
    return None


def open_start(lines: list[Line]) -> Line | None:
    """The last start line, when no done/failed line follows it."""
    for line in reversed(lines):
        if line.kind in ("done", "failed"):
            return None
        if line.kind == "start":
            return line
    return None


def finished_starts(lines: list[Line]) -> list[Line]:
    """Start lines whose outcome is done."""
    result = []
    for i, line in enumerate(lines):
        if line.kind != "start":
            continue
        outcome = next(
            (x for x in lines[i + 1 :] if x.kind in ("done", "failed")), None
        )
        if outcome is not None and outcome.kind == "done":
            result.append(line)
    return result


def decide(
    seen: int | None, lines: list[Line], events: list[tuple[str, date]], today: date
):
    """Return (kind, reason) for this week. kind is start, exit or skip."""
    week = today.isocalendar()[:2]
    for line in lines:
        if line.kind in ("start", "exit") and line.when.isocalendar()[:2] == week:
            return "skip", f"already decided this week ({line.when})"
    if seen is None:
        return "exit", "seen.txt missing"
    counted = [line for line in lines if line.seen is not None]
    if not counted:
        return "exit", f"first poll: baseline set at seen={seen}"
    running = open_start(lines)
    if running is not None:
        return "exit", (
            f"rerun started {running.when} has no outcome line;"
            " record one with poll.py outcome done|failed"
        )
    finished = finished_starts(lines)
    base = finished[-1] if finished else counted[0]
    if seen < base.seen:
        return "exit", (
            f"seen.txt shrank from {base.seen} to {seen} since {base.when};"
            " baseline not trusted"
        )
    installed = counted[0].when
    last_done = finished[-1].when if finished else None
    due = []
    for event_id, end in events:
        when_due = end + timedelta(weeks=WEEKS_AFTER_EVENT)
        if installed < when_due <= today and (
            last_done is None or last_done < when_due
        ):
            due.append(f"{event_id} ended {end}, due {when_due}")
    new = seen - base.seen
    count = f"{new} new talks since {base.when} (threshold {NEW_TALKS_THRESHOLD})"
    if due:
        return "start", "; ".join(due + [count])
    if new >= NEW_TALKS_THRESHOLD:
        return "start", count
    return "exit", count + "; no event due"


def load_events(path: Path) -> list[tuple[str, date]]:
    """(id, end date) per event. Raises ValueError on an entry without both."""
    events = []
    for number, entry in enumerate(json.loads(path.read_text(encoding="utf-8")), 1):
        end = parse_date(entry.get("end")) if isinstance(entry, dict) else None
        if end is None or not isinstance(entry.get("id"), str):
            raise ValueError(
                f"events.json entry {number} has no id or no readable end date"
            )
        events.append((entry["id"], end))
    return events


def stamp(now: datetime) -> str:
    return now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append(path: Path, now: datetime, kind: str, seen: int | None, reason: str) -> None:
    seen_field = "-" if seen is None else str(seen)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"{stamp(now)}\tpoll\t{kind}\tseen={seen_field}\t{reason}\n")


def parse_now(text: str | None) -> datetime:
    if text is None:
        return datetime.now(timezone.utc)
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def run_decide(args) -> int:
    state = args.state_dir.expanduser()
    if not state.is_dir():
        print(f"state folder not found: {state}", file=sys.stderr)
        return 2
    now = parse_now(args.now)
    today = now.astimezone(timezone.utc).date()
    seen = count_seen(state / "seen.txt")
    events = []
    try:
        lines = read_log(state / "runs.log")
        events = load_events(args.events)
    except ValueError as err:
        kind, reason = "exit", str(err)
    else:
        kind, reason = decide(seen, lines, events, today)
    if kind != "skip":
        notes = [digest_note(state / "state.json", today)]
        if events and not any(end > today for _, end in events):
            notes.append(f"events.json lists no event ending after {today}")
        reason = "; ".join([reason] + [n for n in notes if n])
    print(f"{kind} {reason}")
    if kind != "skip" and not args.dry_run:
        append(state / "runs.log", now, kind, seen, reason)
    return 0


def run_outcome(args) -> int:
    state = args.state_dir.expanduser()
    lines = read_log(state / "runs.log")
    running = open_start(lines)
    if running is None:
        print("no open rerun: every start line has an outcome", file=sys.stderr)
        return 2
    append(
        state / "runs.log", parse_now(args.now), args.result, running.seen, args.note
    )
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    d = sub.add_parser("decide")
    d.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    d.add_argument("--dry-run", action="store_true")
    o = sub.add_parser("outcome")
    o.add_argument("result", choices=("done", "failed"))
    o.add_argument("note")
    for p in (d, o):
        p.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
        p.add_argument("--now", help="ISO time to decide at (tests); default: now")
    args = parser.parse_args(argv)
    return run_decide(args) if args.command == "decide" else run_outcome(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
