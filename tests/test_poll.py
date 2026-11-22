"""Tests for the weekly rerun poll under poll/ (#347).

The poll reads the talk digest's state files and decides once a week whether a data rerun is
due: on enough new talks since the last finished rerun, or a set number of weeks after an
event ends. It appends one decision line per week to runs.log, with the reason. Every test
runs on synthetic state in a temporary folder; nothing reads the real digest.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
POLL = ROOT / "poll"


def load():
    spec = importlib.util.spec_from_file_location("poll", POLL / "poll.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


poll = load()


def make_state(tmp_path, seen, published="2026-11-29T10:00:00Z", log=""):
    state = tmp_path / "aie"
    state.mkdir()
    (state / "seen.txt").write_text(
        "".join(f"talk-{i}\n" for i in range(seen)), encoding="utf-8"
    )
    if published is not None:
        (state / "state.json").write_text(
            json.dumps({"publishedAt": published, "corpusVersion": "x"}),
            encoding="utf-8",
        )
    if log:
        (state / "runs.log").write_text(log, encoding="utf-8")
    return state


def make_events(tmp_path, events):
    path = tmp_path / "events.json"
    path.write_text(json.dumps(events), encoding="utf-8")
    return path


FUTURE = [{"id": "conference:far/2099", "end": "2099-01-01"}]


def run(tmp_path, state, now, events=FUTURE, extra=()):
    ev = make_events(tmp_path, events)
    return poll.main(
        ["decide", "--state-dir", str(state), "--events", str(ev), "--now", now]
        + list(extra)
    )


def log_lines(state):
    path = state / "runs.log"
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()


INSTALL = "2026-11-23T09:00:00Z\tpoll\texit\tseen=1000\tfirst poll: baseline set at seen=1000\n"


def test_first_poll_sets_baseline_and_exits(tmp_path, capsys):
    state = make_state(tmp_path, 1000)
    assert run(tmp_path, state, "2026-11-23T09:00:00Z") == 0
    assert capsys.readouterr().out == "exit first poll: baseline set at seen=1000\n"
    assert log_lines(state) == [
        "2026-11-23T09:00:00Z\tpoll\texit\tseen=1000\tfirst poll: baseline set at seen=1000"
    ]


def test_starts_when_new_talks_reach_threshold(tmp_path, capsys):
    state = make_state(tmp_path, 1100, log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    reason = "100 new talks since 2026-11-23 (threshold 100)"
    assert capsys.readouterr().out == f"start {reason}\n"
    assert (
        log_lines(state)[-1]
        == f"2026-11-30T09:00:00Z\tpoll\tstart\tseen=1100\t{reason}"
    )


def test_exits_below_threshold_and_records_why(tmp_path, capsys):
    state = make_state(tmp_path, 1099, log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    reason = "99 new talks since 2026-11-23 (threshold 100); no event due"
    assert capsys.readouterr().out == f"exit {reason}\n"
    assert (
        log_lines(state)[-1] == f"2026-11-30T09:00:00Z\tpoll\texit\tseen=1099\t{reason}"
    )


def test_starts_four_weeks_after_an_event_ends(tmp_path, capsys):
    events = [{"id": "conference:x/2026", "end": "2026-11-12"}] + FUTURE
    state = make_state(tmp_path, 1010, log=INSTALL)
    # 2026-11-12 + 4 weeks = 2026-12-10: not due on the 9th, due on the 10th.
    run(tmp_path, state, "2026-12-09T09:00:00Z", events=events, extra=["--dry-run"])
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-11-23 (threshold 100); no event due\n"
    )
    run(tmp_path, state, "2026-12-10T09:00:00Z", events=events)
    assert capsys.readouterr().out == (
        "start conference:x/2026 ended 2026-11-12, due 2026-12-10;"
        " 10 new talks since 2026-11-23 (threshold 100)\n"
    )


def test_event_due_before_the_poll_was_installed_does_not_start(tmp_path, capsys):
    events = [{"id": "conference:old/2026", "end": "2026-10-01"}] + FUTURE
    state = make_state(tmp_path, 1010, log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z", events=events)
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-11-23 (threshold 100); no event due\n"
    )


def test_event_due_on_the_install_day_does_not_start(tmp_path, capsys):
    # 2026-10-26 + 4 weeks = 2026-11-23, the day of the poll's first line.
    events = [{"id": "conference:edge/2026", "end": "2026-10-26"}] + FUTURE
    state = make_state(tmp_path, 1010, log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z", events=events)
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-11-23 (threshold 100); no event due\n"
    )


def test_event_covered_by_a_finished_rerun_does_not_start_again(tmp_path, capsys):
    events = [{"id": "conference:x/2026", "end": "2026-11-12"}] + FUTURE
    log = INSTALL + (
        "2026-12-14T09:00:00Z\tpoll\tstart\tseen=1010\tconference:x/2026 ended\n"
        "2026-12-14T11:00:00Z\tpoll\tdone\tseen=1010\tdraft PR\n"
    )
    state = make_state(tmp_path, 1020, published="2026-12-18T10:00:00Z", log=log)
    run(tmp_path, state, "2026-12-21T09:00:00Z", events=events)
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-12-14 (threshold 100); no event due\n"
    )


def test_failed_rerun_keeps_the_old_baseline_and_the_event_due(tmp_path, capsys):
    events = [{"id": "conference:x/2026", "end": "2026-11-12"}] + FUTURE
    log = INSTALL + (
        "2026-12-14T09:00:00Z\tpoll\tstart\tseen=1010\tconference:x/2026 ended\n"
        "2026-12-14T11:00:00Z\tpoll\tfailed\tseen=1010\tstopped at step 1\n"
    )
    state = make_state(tmp_path, 1020, published="2026-12-18T10:00:00Z", log=log)
    run(tmp_path, state, "2026-12-21T09:00:00Z", events=events)
    assert capsys.readouterr().out == (
        "start conference:x/2026 ended 2026-11-12, due 2026-12-10;"
        " 20 new talks since 2026-11-23 (threshold 100)\n"
    )


def test_open_rerun_blocks_a_second_start(tmp_path, capsys):
    log = INSTALL + "2026-11-30T09:00:00Z\tpoll\tstart\tseen=1100\t100 new talks\n"
    state = make_state(tmp_path, 1300, log=log)
    run(tmp_path, state, "2026-12-07T09:00:00Z")
    reason = (
        "rerun started 2026-11-30 has no outcome line;"
        " record one with poll.py outcome done|failed"
    )
    assert capsys.readouterr().out == f"exit {reason}\n"
    assert (
        log_lines(state)[-1] == f"2026-12-07T09:00:00Z\tpoll\texit\tseen=1300\t{reason}"
    )


def test_second_run_in_the_same_week_writes_nothing(tmp_path, capsys):
    state = make_state(tmp_path, 1100, log=INSTALL)
    # Monday 2026-11-23 and Sunday 2026-11-29 are the same ISO week.
    run(tmp_path, state, "2026-11-29T20:00:00Z")
    assert capsys.readouterr().out == "skip already decided this week (2026-11-23)\n"
    assert log_lines(state) == [INSTALL.rstrip("\n")]


def test_week_is_the_iso_week_across_a_year_boundary(tmp_path, capsys):
    # 2026-12-28 and 2027-01-03 are both in ISO week 2026-W53; 2027-01-04 is 2027-W01.
    log = "2026-12-28T09:00:00Z\tpoll\texit\tseen=1000\tfirst poll\n"
    state = make_state(tmp_path, 1010, published="2027-01-01T10:00:00Z", log=log)
    run(tmp_path, state, "2027-01-03T09:00:00Z")
    assert capsys.readouterr().out == "skip already decided this week (2026-12-28)\n"
    run(tmp_path, state, "2027-01-04T09:00:00Z", extra=["--dry-run"])
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-12-28 (threshold 100); no event due\n"
    )


def test_same_week_number_in_another_year_is_not_this_week(tmp_path, capsys):
    # 2026-01-05 is 2026-W02; 2027-01-11 is 2027-W02.
    log = "2026-01-05T09:00:00Z\tpoll\texit\tseen=1000\tfirst poll\n"
    state = make_state(tmp_path, 1010, published="2027-01-08T10:00:00Z", log=log)
    run(tmp_path, state, "2027-01-11T09:00:00Z", extra=["--dry-run"])
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-01-05 (threshold 100); no event due\n"
    )


def test_seen_list_that_shrank_exits_without_starting(tmp_path, capsys):
    state = make_state(tmp_path, 900, log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    assert capsys.readouterr().out == (
        "exit seen.txt shrank from 1000 to 900 since 2026-11-23; baseline not trusted\n"
    )


def test_missing_seen_list_exits_and_records_why(tmp_path, capsys):
    state = make_state(tmp_path, 0, log=INSTALL)
    (state / "seen.txt").unlink()
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    assert capsys.readouterr().out == "exit seen.txt missing\n"
    assert (
        log_lines(state)[-1]
        == "2026-11-30T09:00:00Z\tpoll\texit\tseen=-\tseen.txt missing"
    )


def test_quiet_corpus_and_stale_event_list_are_named_in_the_reason(tmp_path, capsys):
    events = [{"id": "conference:x/2026", "end": "2026-10-01"}]
    state = make_state(tmp_path, 1010, published="2026-11-01T10:00:00Z", log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z", events=events)
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-11-23 (threshold 100); no event due;"
        " upstream corpus last published 2026-11-01 (29 days ago);"
        " events.json lists no event ending after 2026-11-30\n"
    )


def test_recent_corpus_adds_no_note(tmp_path, capsys):
    state = make_state(tmp_path, 1010, published="2026-11-09T10:00:00Z", log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-11-23 (threshold 100); no event due\n"
    )


def test_blocked_update_still_records_the_week(tmp_path, capsys):
    state = make_state(tmp_path, 1100, log=INSTALL)
    run(
        tmp_path,
        state,
        "2026-11-30T09:00:00Z",
        extra=["--blocked", "git switch: dirty"],
    )
    reason = "clone not updated: git switch: dirty"
    assert capsys.readouterr().out == f"exit {reason}\n"
    assert (
        log_lines(state)[-1] == f"2026-11-30T09:00:00Z\tpoll\texit\tseen=1100\t{reason}"
    )
    run(tmp_path, state, "2026-12-01T09:00:00Z", extra=["--blocked", "again"])
    assert capsys.readouterr().out == "skip already decided this week (2026-11-30)\n"


def test_baseline_resets_a_shrunk_seen_list(tmp_path, capsys):
    state = make_state(tmp_path, 900, log=INSTALL)
    rc = poll.main(
        [
            "baseline",
            "seen.txt rebuilt",
            "--state-dir",
            str(state),
            "--now",
            "2026-11-30T08:00:00Z",
        ]
    )
    assert rc == 0
    assert (
        log_lines(state)[-1]
        == "2026-11-30T08:00:00Z\tpoll\tbaseline\tseen=900\tseen.txt rebuilt"
    )
    # A baseline line is not a weekly decision: the same week still decides.
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    assert capsys.readouterr().out == (
        "exit 0 new talks since 2026-11-30 (threshold 100); no event due\n"
    )


def test_dry_run_writes_nothing(tmp_path, capsys):
    state = make_state(tmp_path, 1100, log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z", extra=["--dry-run"])
    assert (
        capsys.readouterr().out
        == "start 100 new talks since 2026-11-23 (threshold 100)\n"
    )
    assert log_lines(state) == [INSTALL.rstrip("\n")]


def test_outcome_closes_the_open_rerun_after_blocked_weeks(tmp_path, capsys):
    log = INSTALL + (
        "2026-11-30T09:00:00Z\tpoll\tstart\tseen=1100\t100 new talks\n"
        "2026-12-07T09:00:00Z\tpoll\texit\tseen=1150\trerun started 2026-11-30 ...\n"
    )
    state = make_state(tmp_path, 1150, log=log)
    rc = poll.main(
        [
            "outcome",
            "done",
            "draft PR opened",
            "--state-dir",
            str(state),
            "--now",
            "2026-12-08T11:00:00Z",
        ]
    )
    assert rc == 0
    assert (
        log_lines(state)[-1]
        == "2026-12-08T11:00:00Z\tpoll\tdone\tseen=1100\tdraft PR opened"
    )


def test_outcome_without_an_open_rerun_is_refused(tmp_path, capsys):
    state = make_state(tmp_path, 1000, log=INSTALL)
    rc = poll.main(
        [
            "outcome",
            "failed",
            "x",
            "--state-dir",
            str(state),
            "--now",
            "2026-11-30T11:00:00Z",
        ]
    )
    assert rc == 2
    assert capsys.readouterr().err == "no open rerun: every start line has an outcome\n"
    assert log_lines(state) == [INSTALL.rstrip("\n")]


def test_other_writers_lines_in_runs_log_are_ignored(tmp_path, capsys):
    log = "2026-11-20\tdigest\tpublished 12 posts\n" + INSTALL
    state = make_state(tmp_path, 1100, log=log)
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    assert (
        capsys.readouterr().out
        == "start 100 new talks since 2026-11-23 (threshold 100)\n"
    )


def test_stated_thresholds(tmp_path):
    # The numbers the issue asks to be written down (#347): poll/README.md states them.
    assert (
        poll.NEW_TALKS_THRESHOLD,
        poll.WEEKS_AFTER_EVENT,
        poll.QUIET_CORPUS_DAYS,
    ) == (
        100,
        4,
        21,
    )
    readme = (POLL / "README.md").read_text(encoding="utf-8")
    for line in (
        "- **New talks:** 100",
        "- **Weeks after an event ends:** 4",
        "- **Corpus quiet after:** 21 days",
    ):
        assert line in readme.splitlines()


def test_task_prompt_hardens_every_git_call_and_runs_the_copied_poll():
    # A file an agent planted in the clone must not run through the task's own commands.
    text = (POLL / "task.md").read_text(encoding="utf-8")
    git_calls = [x for x in text.split("`") if x.startswith("git ")]
    assert len(git_calls) == 9
    bad = [
        x
        for x in git_calls
        if not x.startswith(
            "git -C ~/aie-poll/ai-dev-kit -c core.fsmonitor=false -c core.hooksPath=<empty> "
        )
    ]
    assert bad == []
    runs = [x for x in text.split("`") if x.startswith("python ")]
    assert len(runs) == 5
    assert [x for x in runs if not x.startswith("python -I -B <poll>/poll.py ")] == []
    assert "status --porcelain --ignored`" in text


def test_shipped_event_list_is_well_formed():
    events = json.loads((POLL / "events.json").read_text(encoding="utf-8"))
    assert events, "events.json is empty"
    bad = [
        e
        for e in events
        if set(e) != {"id", "end"}
        or not e["id"].startswith("conference:")
        or poll.parse_date(e["end"]) is None
    ]
    assert bad == []


def test_missing_state_folder_is_an_error_not_a_decision(tmp_path, capsys):
    rc = poll.main(
        [
            "decide",
            "--state-dir",
            str(tmp_path / "nope"),
            "--events",
            str(make_events(tmp_path, FUTURE)),
            "--now",
            "2026-11-30T09:00:00Z",
        ]
    )
    assert rc == 2
    assert capsys.readouterr().err.startswith("state folder not found: ")


def test_unreadable_poll_line_exits_and_names_it(tmp_path, capsys):
    log = INSTALL + "2026-11-30T09:00:00Z\tpoll\tbogus\n"
    state = make_state(tmp_path, 1200, log=log)
    run(tmp_path, state, "2026-12-07T09:00:00Z")
    reason = "runs.log line 2 is a poll line this poll cannot read"
    assert capsys.readouterr().out == f"exit {reason}\n"
    assert (
        log_lines(state)[-1] == f"2026-12-07T09:00:00Z\tpoll\texit\tseen=1200\t{reason}"
    )


def test_unreadable_event_entry_exits_and_names_it(tmp_path, capsys):
    state = make_state(tmp_path, 1200, log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z", events=FUTURE + [{"id": "x"}])
    assert capsys.readouterr().out == (
        "exit events.json entry 2 has no id or no readable end date\n"
    )


def test_unreadable_input_still_writes_one_line_a_week(tmp_path, capsys):
    log = INSTALL + "2026-11-30T09:00:00Z\tpoll\tbogus\n"
    state = make_state(tmp_path, 1200, log=log)
    run(tmp_path, state, "2026-12-07T09:00:00Z")
    capsys.readouterr()
    run(tmp_path, state, "2026-12-08T09:00:00Z")
    assert capsys.readouterr().out == "skip already decided this week (2026-12-07)\n"
    run(tmp_path, state, "2026-12-09T09:00:00Z", events=FUTURE + [{"id": "x"}])
    assert capsys.readouterr().out == "skip already decided this week (2026-12-07)\n"
    assert len(log_lines(state)) == 3


def test_unreadable_seen_list_exits_and_records_why(tmp_path, capsys):
    state = make_state(tmp_path, 0, log=INSTALL)
    (state / "seen.txt").write_bytes(b"talk-1\n\xff\xfe\n")
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    assert capsys.readouterr().out == "exit seen.txt unreadable\n"
    assert (
        log_lines(state)[-1]
        == "2026-11-30T09:00:00Z\tpoll\texit\tseen=-\tseen.txt unreadable"
    )
    rc = poll.main(["baseline", "rebuilt", "--state-dir", str(state)])
    assert rc == 2
    assert len(log_lines(state)) == 2


def test_seen_count_is_distinct_non_blank_ids(tmp_path, capsys):
    state = make_state(tmp_path, 0)
    (state / "seen.txt").write_text("a\nb\na\n\n   \n c \nc\n", encoding="utf-8")
    run(tmp_path, state, "2026-11-23T09:00:00Z")
    assert capsys.readouterr().out == "exit first poll: baseline set at seen=3\n"


def test_outcome_refuses_an_unreadable_log(tmp_path, capsys):
    log = INSTALL + "2026-11-30T09:00:00Z\tpoll\tstart\tseen=1200\tx\n"
    log += "2026-12-01T09:00:00Z\tpoll\tbogus\n"
    state = make_state(tmp_path, 1200, log=log)
    rc = poll.main(["outcome", "failed", "why", "--state-dir", str(state)])
    assert rc == 2
    assert (
        "runs.log line 3 is a poll line this poll cannot read"
        in capsys.readouterr().err
    )
    assert len(log_lines(state)) == 3


def test_missing_digest_state_is_named_in_the_reason(tmp_path, capsys):
    state = make_state(tmp_path, 1010, published=None, log=INSTALL)
    run(tmp_path, state, "2026-11-30T09:00:00Z")
    assert capsys.readouterr().out == (
        "exit 10 new talks since 2026-11-23 (threshold 100); no event due;"
        " state.json has no readable publishedAt\n"
    )
