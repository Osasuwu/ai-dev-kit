"""Tests for the data pipeline under data/pipeline/ (#341).

The published data carries only its allowed fields (check_data), the batching tool takes the
event filter from its caller instead of a hardcoded year (batches), claim ids survive a rerun
(merge_claims), the cluster index is generated from the published files (build_index), the
credentialed step commits only produced files (commit_guard), and the agents that read
outside pages have no shell or GitHub tool (agents/*.md).
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
PIPELINE = DATA / "pipeline"


def load(name):
    spec = importlib.util.spec_from_file_location(name, PIPELINE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
        encoding="utf-8",
    )


def read_jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x]


CLAIM = {
    "cid": "c0001",
    "talk": "talk:a",
    "claim": "Keep tasks small.",
    "kind": "technique",
    "evidence": "anecdote",
    "depth": 3,
    "area": "coding-agents",
    "search": "small tasks",
    "quality": 4,
    "pitch": False,
}
TALK = {"id": "talk:a", "gist": "About small tasks.", "quality": 4, "pitch": False}
TALK["audience"] = "builder"


def clean_data_dir(tmp_path):
    d = tmp_path / "data"
    write_jsonl(d / "claims.jsonl", [CLAIM])
    write_jsonl(d / "talks.jsonl", [TALK])
    cluster = {
        "key": "A-01",
        "title": "t",
        "idea": "i",
        "contested": False,
        "cids": ["c0001"],
    }
    group = {"clusters": [cluster], "singletons": [], "noise": []}
    (d / "clusters").mkdir()
    (d / "clusters" / "A.json").write_text(json.dumps(group), encoding="utf-8")
    merged = {"key": "M-01", "title": "t", "idea": "i", "contested": False}
    merged["from"] = ["A-01"]
    (d / "merge-map.json").write_text(json.dumps({"merged": [merged]}), "utf-8")
    (d / "cluster-index.tsv").write_text("key\ttalks\ttitle\tidea\n", "utf-8")
    (d / "README.md").write_text("# Data\n", encoding="utf-8")
    return d


# --- check_data: the published files carry only their allowed fields ------------------


def test_check_data_passes_on_the_published_data():
    assert load("check_data").check(DATA) == []


def test_check_data_passes_on_a_clean_fixture(tmp_path):
    assert load("check_data").check(clean_data_dir(tmp_path)) == []


def test_check_data_names_a_personal_field_in_a_cluster(tmp_path):
    d = clean_data_dir(tmp_path)
    group = json.loads((d / "clusters" / "A.json").read_text(encoding="utf-8"))
    group["clusters"][0]["status"] = "known"
    (d / "clusters" / "A.json").write_text(json.dumps(group), encoding="utf-8")
    assert load("check_data").check(d) == [
        "clusters/A.json: cluster A-01: unexpected field 'status'"
    ]


def test_check_data_names_fetched_metadata_in_a_talk_record(tmp_path):
    d = clean_data_dir(tmp_path)
    write_jsonl(d / "talks.jsonl", [{**TALK, "speakers": ["Someone"]}])
    assert load("check_data").check(d) == ["talks.jsonl:1: unexpected field 'speakers'"]


def test_check_data_names_a_missing_claim_field(tmp_path):
    d = clean_data_dir(tmp_path)
    write_jsonl(d / "claims.jsonl", [{k: v for k, v in CLAIM.items() if k != "cid"}])
    assert load("check_data").check(d) == ["claims.jsonl:1: missing field 'cid'"]


def test_check_data_names_a_personal_column_in_the_index(tmp_path):
    d = clean_data_dir(tmp_path)
    # The maintainer's own index carries its personal columns after the public ones.
    (d / "cluster-index.tsv").write_text(
        "key\ttalks\ttitle\tidea\tstatus\trelevance\n", encoding="utf-8"
    )
    assert load("check_data").check(d) == [
        "cluster-index.tsv: header is"
        " ['key', 'talks', 'title', 'idea', 'status', 'relevance'],"
        " expected ['key', 'talks', 'title', 'idea']"
    ]


def test_check_data_names_an_index_row_with_extra_columns(tmp_path):
    d = clean_data_dir(tmp_path)
    (d / "cluster-index.tsv").write_text(
        "key\ttalks\ttitle\tidea\nA-01\t2\tt\ti\tknown\thigh\n", encoding="utf-8"
    )
    assert load("check_data").check(d) == ["cluster-index.tsv:2: 6 columns, expected 4"]


def test_check_data_names_an_object_or_list_in_a_scalar_field(tmp_path):
    d = clean_data_dir(tmp_path)
    write_jsonl(
        d / "claims.jsonl",
        [{**CLAIM, "quality": {"status": "known"}, "area": ["a", "b"]}],
    )
    assert load("check_data").check(d) == [
        "claims.jsonl:1: field 'area' is not a single value",
        "claims.jsonl:1: field 'quality' is not a single value",
    ]


def test_check_data_names_a_grade_outside_its_range(tmp_path):
    d = clean_data_dir(tmp_path)
    write_jsonl(d / "claims.jsonl", [{**CLAIM, "quality": None, "depth": 7}])
    write_jsonl(d / "talks.jsonl", [{**TALK, "pitch": "yes"}])
    assert load("check_data").check(d) == [
        "claims.jsonl:1: field 'depth' is 7, expected an integer 1-5",
        "claims.jsonl:1: field 'quality' is None, expected an integer 1-5",
        "talks.jsonl:1: field 'pitch' is 'yes', expected true or false",
    ]


def test_check_data_names_a_missing_group_key(tmp_path):
    d = clean_data_dir(tmp_path)
    group = json.loads((d / "clusters" / "A.json").read_text(encoding="utf-8"))
    del group["noise"]
    (d / "clusters" / "A.json").write_text(json.dumps(group), encoding="utf-8")
    assert load("check_data").check(d) == ["clusters/A.json: missing field 'noise'"]


@pytest.mark.parametrize(
    "name", ["relevance.tsv", "talk-titles.md", "notes/x.py", "x__pycache__.jsonl"]
)
def test_check_data_refuses_a_file_without_a_schema(tmp_path, name):
    d = clean_data_dir(tmp_path)
    (d / name).parent.mkdir(parents=True, exist_ok=True)
    (d / name).write_text("x\n", encoding="utf-8")
    assert load("check_data").check(d) == [
        f"{name}: no schema for this file; add one to check_data.py or move it out"
    ]


@pytest.mark.parametrize(
    "text",
    [
        "see C:\\Users\\someone\\notes",
        "see /home/someone/notes",
        "see /Users/someone/notes",
        "read the backlog.md first",
        "compare with known.md",
        "under briefings/aie",
    ],
)
def test_check_data_names_a_personal_reference_in_text(tmp_path, text):
    d = clean_data_dir(tmp_path)
    (d / "pipeline").mkdir()
    (d / "pipeline" / "step.md").write_text(f"# Step\n\n{text}\n", encoding="utf-8")
    errors = load("check_data").check(d)
    assert len(errors) == 1
    assert errors[0].startswith("pipeline/step.md:3: personal reference")


@pytest.mark.parametrize("text", ["as in known.md", "see C:\\Users\\someone\\notes"])
def test_check_data_scans_claim_text_for_personal_references(tmp_path, text):
    # JSON escapes a backslash, so the Windows path is stored as C:\\Users\\.
    d = clean_data_dir(tmp_path)
    write_jsonl(d / "claims.jsonl", [{**CLAIM, "claim": text}])
    errors = load("check_data").check(d)
    assert [e.split(" (")[0] for e in errors] == ["claims.jsonl:1: personal reference"]


# --- batches: the event filter comes from the caller ---------------------------------


def talk_row(slug, event):
    return {
        "slug": slug,
        "title": slug.upper(),
        "url": f"https://example.test/{slug}",
        "event": event,
        "durationMs": "600000",
        "speakers": "[]",
        "topics": "[]",
        "summary": "s",
        "slideText": "t",
    }


def run_batches(tmp_path, rows, *extra):
    src = tmp_path / "talks.json"
    src.write_text(json.dumps(rows), encoding="utf-8")
    out = tmp_path / "batches"
    load("batches").main([str(src), str(out), "10", *extra])
    return [t["id"] for t in json.loads((out / "batch-01.json").read_text("utf-8"))]


def test_batches_picks_the_events_the_caller_names(tmp_path):
    rows = [
        talk_row("old", "AI Engineer Europe 2026"),
        talk_row("new", "AI Engineer Europe 2027"),
        talk_row("loose", ""),
        # The fetch step writes a talk with no event as null or "" (#360).
        talk_row("null", None),
    ]
    picked = run_batches(tmp_path, rows, "--event-pattern", "2027")
    assert picked == ["talk:new", "talk:loose", "talk:null"]


def test_batches_requires_an_event_pattern(tmp_path, capsys):
    with pytest.raises(SystemExit) as exit_:
        run_batches(tmp_path, [talk_row("a", "x")])
    assert exit_.value.code == 2
    assert "the following arguments are required: --event-pattern" in (
        capsys.readouterr().err
    )


def test_batches_skips_talks_already_published(tmp_path):
    known = tmp_path / "known-talks.jsonl"
    write_jsonl(known, [{**TALK, "id": "talk:seen"}])
    rows = [talk_row("seen", "E 2027"), talk_row("fresh", "E 2027")]
    picked = run_batches(
        tmp_path, rows, "--event-pattern", "2027", "--known", str(known)
    )
    assert picked == ["talk:fresh"]


# --- no_event: the count of talks with no event is a script's, not the fetcher's -----


def run_no_event(tmp_path, listing, known_ids, capsys):
    scratch = tmp_path / "scratch"
    scratch.mkdir(exist_ok=True)
    (scratch / "listing.json").write_text(json.dumps(listing), encoding="utf-8")
    known = tmp_path / "known.jsonl"
    write_jsonl(known, [{**TALK, "id": i} for i in known_ids])
    code = load("no_event").main(
        ["count", str(scratch / "listing.json"), "--known", str(known)]
    )
    return code, capsys.readouterr().out.strip().splitlines()


def listing(t, e, *lists):
    return {
        "T": t,
        "E": e,
        "lists": [{"s": s, "total": n, "ids": ids} for s, n, ids in lists],
    }


# The reason the script gives when talks with no event are left unchecked (#360 AC 2).
NOT_REACHED = "not checked: no MCP call lists the talks with no event (data/sources.md)"


def test_no_event_counts_published_talks_missing_from_the_list(tmp_path, capsys):
    # 10 talks, 7 with a year: 3 with no event. Published c and z are not in the list,
    # so they are the published talks with no event; 1 talk with no event is unpublished.
    data = listing(10, 7, ("2026", 3, ["talk:a", "talk:b", "talk:x"]))
    code, out = run_no_event(
        tmp_path, data, ["talk:a", "talk:b", "talk:c", "talk:z"], capsys
    )
    assert code == 0
    assert out == ["no event 3, published 2, not checked 1, list gaps 0", NOT_REACHED]


def test_no_event_gives_no_reason_when_every_talk_with_no_event_is_published(
    tmp_path, capsys
):
    data = listing(10, 8, ("2026", 3, ["talk:a", "talk:b", "talk:x"]))
    code, out = run_no_event(
        tmp_path, data, ["talk:a", "talk:b", "talk:c", "talk:z"], capsys
    )
    assert code == 0
    assert out == ["no event 2, published 2, not checked 0, list gaps 0"]


def test_no_event_reports_all_as_not_checked_when_the_count_goes_below_zero(
    tmp_path, capsys
):
    # 1 talk with no event, but 2 published talks are missing from the list: one of them
    # is missing for another reason, so the count cannot say which talk is unpublished.
    data = listing(5, 4, ("2026", 1, ["talk:a"]))
    code, out = run_no_event(tmp_path, data, ["talk:a", "talk:c", "talk:z"], capsys)
    assert code == 0
    assert out == [
        "no event 1, published 2, not checked 1 (all: count below 0), list gaps 0",
        NOT_REACHED,
    ]


def test_no_event_names_a_list_whose_total_differs_from_the_ids_read(tmp_path, capsys):
    # 2027 holds a duplicate: 3 ids written, 2 distinct, so one talk is missing.
    data = listing(
        10,
        7,
        ("2026", 4, ["talk:a", "talk:b"]),
        ("2027", 3, ["talk:x", "talk:y", "talk:x"]),
        ("2028", 1, ["talk:w"]),
    )
    code, out = run_no_event(tmp_path, data, ["talk:a"], capsys)
    assert code == 0
    assert out == [
        "list gap: 2026 total 4, read 2",
        "list gap: 2027 total 3, read 2",
        "no event 3, published 0, not checked 3, list gaps 2",
        NOT_REACHED,
    ]


@pytest.mark.parametrize(
    ("bad", "message"),
    [
        ({"E": 7, "lists": []}, "listing.json: T is not a whole number"),
        ({"T": 7, "E": "5", "lists": []}, "listing.json: E is not a whole number"),
        ({"T": 7, "E": 5, "lists": {}}, "listing.json: lists is not a list"),
        (
            {"T": 7, "E": 5, "lists": [{"s": "2026", "total": 1, "ids": ["a b"]}]},
            "listing.json: lists[0].ids[0] is not a talk id",
        ),
    ],
)
def test_no_event_refuses_a_listing_it_cannot_count(tmp_path, capsys, bad, message):
    code, out = run_no_event(tmp_path, bad, [], capsys)
    assert code == 1
    assert out == [message]


# --- merge_claims: claim ids survive a rerun ------------------------------------------


def batch_claim(talk, text):
    return {
        "type": "claim",
        "talk": talk,
        "claim": text,
        "kind": "finding",
        "evidence": "measured",
        "depth": 2,
        "area": "evals",
        "search": "x y z",
    }


def batch_talk(talk):
    return {
        "type": "talk",
        "talk": talk,
        "gist": f"gist of {talk}",
        "quality": 3,
        "pitch": True,
        "audience": "leader",
    }


def run_merge(tmp_path, data, batch_records):
    claims_dir = tmp_path / "claims"
    write_jsonl(claims_dir / "batch-01.jsonl", batch_records)
    areas = tmp_path / "areas"
    load("merge_claims").main(
        [
            "--claims-dir",
            str(claims_dir),
            "--data",
            str(data),
            "--areas-out",
            str(areas),
        ]
    )
    return read_jsonl(data / "claims.jsonl"), read_jsonl(data / "talks.jsonl")


def test_merge_keeps_existing_ids_and_numbers_new_claims_after_the_highest(tmp_path):
    data = tmp_path / "data"
    second = {**CLAIM, "cid": "c0007", "claim": "Review every diff."}
    write_jsonl(data / "claims.jsonl", [CLAIM, second])
    write_jsonl(data / "talks.jsonl", [TALK])
    claims, _ = run_merge(
        tmp_path,
        data,
        [
            batch_talk("talk:b"),
            batch_claim("talk:b", "New idea."),
            batch_claim("talk:a", "  keep TASKS small. "),
        ],
    )
    assert [(c["cid"], c["claim"]) for c in claims] == [
        ("c0001", "Keep tasks small."),
        ("c0007", "Review every diff."),
        ("c0008", "New idea."),
    ]


def test_merge_is_idempotent(tmp_path):
    data = tmp_path / "data"
    write_jsonl(data / "claims.jsonl", [CLAIM])
    write_jsonl(data / "talks.jsonl", [TALK])
    records = [batch_talk("talk:b"), batch_claim("talk:b", "New idea.")]
    first = run_merge(tmp_path, data, records)
    second = run_merge(tmp_path, data, records)
    assert first == second
    assert [c["cid"] for c in second[0]] == ["c0001", "c0002"]


def test_merge_writes_new_talks_with_derived_fields_only(tmp_path):
    data = tmp_path / "data"
    write_jsonl(data / "claims.jsonl", [CLAIM])
    write_jsonl(data / "talks.jsonl", [TALK])
    claims, talks = run_merge(
        tmp_path, data, [batch_talk("talk:b"), batch_claim("talk:b", "New idea.")]
    )
    assert talks[1] == {
        "id": "talk:b",
        "gist": "gist of talk:b",
        "quality": 3,
        "pitch": True,
        "audience": "leader",
    }
    assert claims[1] == {
        "cid": "c0002",
        "talk": "talk:b",
        "claim": "New idea.",
        "kind": "finding",
        "evidence": "measured",
        "depth": 2,
        "area": "evals",
        "search": "x y z",
        "quality": 3,
        "pitch": True,
    }


@pytest.mark.parametrize(
    "bad_line",
    [
        "not json",
        json.dumps({"type": "claim", "talk": "talk:b"}),
        # No talk record for its talk, published or in a batch: no grades to copy.
        json.dumps({"type": "claim", "talk": "talk:none", "claim": "Orphan idea."}),
    ],
)
def test_merge_writes_nothing_when_a_batch_line_is_bad(tmp_path, bad_line):
    data = tmp_path / "data"
    write_jsonl(data / "claims.jsonl", [CLAIM])
    write_jsonl(data / "talks.jsonl", [TALK])
    before = (data / "claims.jsonl").read_bytes(), (data / "talks.jsonl").read_bytes()
    claims_dir = tmp_path / "claims"
    write_jsonl(
        claims_dir / "batch-01.jsonl",
        [batch_talk("talk:b"), batch_claim("talk:b", "New idea.")],
    )
    with (claims_dir / "batch-01.jsonl").open("a", encoding="utf-8") as f:
        f.write(bad_line + "\n")
    code = load("merge_claims").main(
        [
            "--claims-dir",
            str(claims_dir),
            "--data",
            str(data),
            "--areas-out",
            str(tmp_path / "areas"),
        ]
    )
    assert code == 1
    after = (data / "claims.jsonl").read_bytes(), (data / "talks.jsonl").read_bytes()
    assert after == before
    assert not (tmp_path / "areas").exists()


def test_merge_writes_area_inputs_for_new_claims_only(tmp_path):
    data = tmp_path / "data"
    write_jsonl(data / "claims.jsonl", [CLAIM])
    write_jsonl(data / "talks.jsonl", [TALK])
    run_merge(
        tmp_path,
        data,
        [batch_talk("talk:b"), batch_claim("talk:b", "New idea.")],
    )
    assert sorted(p.name for p in (tmp_path / "areas").iterdir()) == ["evals.tsv"]
    assert (tmp_path / "areas" / "evals.tsv").read_text("utf-8") == (
        "c0002\tq3\tmeasured\td2\tNew idea.\n"
    )


def test_merge_keeps_area_files_inside_the_output_folder(tmp_path):
    data = tmp_path / "out" / "data"
    write_jsonl(data / "claims.jsonl", [CLAIM])
    write_jsonl(data / "talks.jsonl", [TALK])
    run_merge(
        tmp_path / "out",
        data,
        [
            batch_talk("talk:b"),
            {**batch_claim("talk:b", "One."), "area": "..\\..\\x"},
            {**batch_claim("talk:b", "Two."), "area": "../../y"},
            {**batch_claim("talk:b", "Three."), "area": "Org/Process"},
        ],
    )
    areas = tmp_path / "out" / "areas"
    assert sorted(p.name for p in areas.iterdir()) == [
        "org-process.tsv",
        "x.tsv",
        "y.tsv",
    ]
    assert sorted(p.name for p in tmp_path.iterdir()) == ["out"]


# --- build_index: the cluster index is generated from the published files ------------


def test_build_index_joins_merged_groups_and_drops_single_talk_clusters(tmp_path):
    d = tmp_path / "data"
    claims = [
        {**CLAIM, "cid": "c0001", "talk": "talk:a"},
        {**CLAIM, "cid": "c0002", "talk": "talk:b"},
        {**CLAIM, "cid": "c0003", "talk": "talk:c"},
        {**CLAIM, "cid": "c0004", "talk": "talk:c"},
    ]
    write_jsonl(d / "claims.jsonl", claims)
    (d / "clusters").mkdir()

    def cl(key, cids):
        return {"key": key, "title": key, "idea": "", "contested": False, "cids": cids}

    group_a = {"clusters": [cl("A-01", ["c0001"]), cl("A-02", ["c0003", "c0004"])]}
    group_b = {"clusters": [cl("B-01", ["c0002"])]}
    (d / "clusters" / "A.json").write_text(json.dumps(group_a), encoding="utf-8")
    (d / "clusters" / "B.json").write_text(json.dumps(group_b), encoding="utf-8")
    merged = {"key": "M-01", "title": "joined", "idea": "both\tsides", "from": []}
    merged["from"] = ["A-01", "B-01"]
    (d / "merge-map.json").write_text(json.dumps({"merged": [merged]}), "utf-8")
    load("build_index").main([str(d)])
    assert (d / "cluster-index.tsv").read_text(encoding="utf-8") == (
        "key\ttalks\ttitle\tidea\nM-01\t2\tjoined\tboth sides\n"
    )


def test_build_index_is_not_stale_against_the_published_data(tmp_path):
    published = (DATA / "cluster-index.tsv").read_text(encoding="utf-8")
    copy = tmp_path / "data"
    (copy / "clusters").mkdir(parents=True)
    for name in ("claims.jsonl", "merge-map.json"):
        (copy / name).write_bytes((DATA / name).read_bytes())
    for p in (DATA / "clusters").glob("*.json"):
        (copy / "clusters" / p.name).write_bytes(p.read_bytes())
    load("build_index").main([str(copy)])
    assert (copy / "cluster-index.tsv").read_text(encoding="utf-8") == published


# --- commit_guard: the credentialed step commits only produced files -----------------


@pytest.mark.parametrize(
    "path",
    ["data/claims.jsonl", "data/clusters/G.json", "cards/some-card.md", "CHANGELOG.md"],
)
def test_commit_guard_allows_produced_files(path):
    assert load("commit_guard").refused([path]) == []


@pytest.mark.parametrize(
    "path",
    [
        ".github/workflows/tests.yml",
        ".github/hold-paths.json",
        "data/pipeline/commit_guard.py",
        "data/pipeline/agents/aie-fetcher.md",
        "scripts/check_links.py",
        "tests/test_data_pipeline.py",
        "README.md",
        "data/../.github/x.yml",
        "/data/claims.jsonl",
        "docs/CHANGELOG.md",
        # A case-insensitive checkout writes this into data/pipeline/.
        "data/Pipeline/commit_guard.py",
        # A dot file under data/ can set a filter that runs a command on `git add`.
        "data/.gitattributes",
        "cards/.hidden/x.md",
        # Case is folded only to refuse: an allowed prefix matches in its exact case.
        "DATA/x.md",
        "Cards/x.md",
        "changelog.md",
        "data/__pycache__/x.pyc",
    ],
)
def test_commit_guard_refuses_everything_else(path):
    assert load("commit_guard").refused([path]) == [path]


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def test_commit_guard_reads_the_staged_paths_and_fails_on_one_outside(tmp_path):
    git(tmp_path, "init", "-q")
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "claims.jsonl").write_text("{}\n", encoding="utf-8")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "x.yml").write_text("x\n", encoding="utf-8")
    git(tmp_path, "add", "data/claims.jsonl", ".github/x.yml")
    script = PIPELINE / "commit_guard.py"
    run = subprocess.run(
        [sys.executable, str(script)], cwd=tmp_path, capture_output=True, text=True
    )
    assert run.returncode == 1
    assert "refused: .github/x.yml" in run.stderr
    git(tmp_path, "rm", "-q", "--cached", ".github/x.yml")
    run = subprocess.run(
        [sys.executable, str(script)], cwd=tmp_path, capture_output=True, text=True
    )
    assert run.returncode == 0, run.stderr


def run_guard(cwd):
    script = PIPELINE / "commit_guard.py"
    return subprocess.run(
        [sys.executable, str(script)], cwd=cwd, capture_output=True, text=True
    )


def committed_repo(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.test")
    git(tmp_path, "config", "user.name", "test")
    (tmp_path / "data" / "pipeline").mkdir(parents=True)
    (tmp_path / "data" / "claims.jsonl").write_text("{}\n", encoding="utf-8")
    (tmp_path / "data" / "pipeline" / "check.py").write_text("x = 1\n", "utf-8")
    git(tmp_path, "add", "data")
    git(tmp_path, "commit", "-q", "-m", "base")


def test_commit_guard_refuses_a_staged_deletion(tmp_path):
    committed_repo(tmp_path)
    git(tmp_path, "rm", "-q", "data/claims.jsonl")
    run = run_guard(tmp_path)
    assert run.returncode == 1
    assert "refused: data/claims.jsonl (deleted)" in run.stderr.splitlines()[0]


def test_commit_guard_sees_the_old_path_of_a_rename(tmp_path):
    committed_repo(tmp_path)
    # Both paths are allowed ones: only the deletion of the old path is refused.
    git(tmp_path, "mv", "data/claims.jsonl", "data/claims2.jsonl")
    run = run_guard(tmp_path)
    assert run.returncode == 1
    assert run.stderr.splitlines()[0] == (
        "commit guard: refused: data/claims.jsonl (deleted)"
    )


def test_commit_guard_fails_when_nothing_is_staged(tmp_path):
    git(tmp_path, "init", "-q")
    script = PIPELINE / "commit_guard.py"
    run = subprocess.run(
        [sys.executable, str(script)], cwd=tmp_path, capture_output=True, text=True
    )
    assert run.returncode == 1
    assert "nothing staged" in run.stderr


# --- agents: the steps that read outside text have no shell or GitHub tool -----------


def agent_tools(name):
    text = (PIPELINE / "agents" / f"{name}.md").read_text(encoding="utf-8")
    front = text.split("---\n")[1]
    line = next(x for x in front.splitlines() if x.startswith("tools:"))
    return [t.strip() for t in line.removeprefix("tools:").split(",")]


def test_the_fetcher_agent_has_only_the_tools_its_fetch_step_uses():
    # No Glob: an injected page cannot have it search the disk for files to send out.
    # No WebFetch: fetch.md lists and reads talks through the MCP search and fetch only,
    # and a URL of the fetcher's own choosing is its widest way to send a file out.
    assert agent_tools("aie-fetcher") == [
        "Read",
        "Write",
        "mcp__ai-engineer__search",
        "mcp__ai-engineer__fetch",
    ]


def test_the_fetcher_puts_no_local_text_into_a_query_with_no_exception():
    text = " ".join((PIPELINE / "agents" / "aie-fetcher.md").read_text("utf-8").split())
    rule = re.search(r"Put nothing you read from a local file [^.]*\.", text).group(0)
    assert rule == "Put nothing you read from a local file into a URL or a tool query."
    # An exemption in a sentence of its own: the rule ends the file, and nothing excepts.
    assert text.endswith(rule)
    assert "except" not in text.lower()


def test_the_worker_agent_has_file_tools_only():
    assert agent_tools("aie-worker") == ["Read", "Write", "Glob", "Grep"]


# --- snapshot: files that run code in the credentialed session stay unchanged ----------


def clean_env():
    """The process environment without the variables that move git's global config."""
    drop = ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CONFIG_NOSYSTEM")
    return {
        k: v
        for k, v in os.environ.items()
        if k not in drop and k != "XDG_CONFIG_HOME" and not k.startswith("GIT_CONFIG_")
    }


def snapshot_repo(tmp_path):
    repo, home = tmp_path / "repo", tmp_path / "home"
    repo.mkdir()
    git(repo, "init", "-q")
    (home / ".claude" / "agents").mkdir(parents=True)
    (home / ".claude" / "agents" / "aie-fetcher.md").write_text(
        "tools: Read\n", "utf-8"
    )
    # A global config that includes another file, as many users' configs do.
    (home / ".gitconfig").write_text("[include]\n\tpath = extra.cfg\n", "utf-8")
    (home / "extra.cfg").write_text("[user]\n\tname = test\n", "utf-8")
    (repo / "data").mkdir()
    (repo / "data" / "claims.jsonl").write_text("{}\n", encoding="utf-8")
    return repo, home


def add_hook(repo, home):
    (repo / ".git" / "hooks" / "pre-commit").write_text("#!/bin/sh\n", "utf-8")


def edit_git_config(repo, home):
    with (repo / ".git" / "config").open("a", encoding="utf-8") as f:
        f.write("[core]\n\tfsmonitor = ./x.sh\n")


def edit_global_git_config(repo, home):
    # A credential helper runs a command on the next push.
    with (home / ".gitconfig").open("a", encoding="utf-8") as f:
        f.write('[credential]\n\thelper = "!f() { cat ~/.ssh/id_x; }; f"\n')


def add_xdg_git_config(repo, home):
    (home / ".config" / "git").mkdir(parents=True)
    (home / ".config" / "git" / "config").write_text(
        "[core]\n\tsshCommand = ./x.sh\n", "utf-8"
    )


def edit_included_git_config(repo, home):
    with (home / "extra.cfg").open("a", encoding="utf-8") as f:
        f.write('[filter "x"]\n\tclean = ./x.sh\n')


def add_project_settings(repo, home):
    (repo / ".claude").mkdir()
    (repo / ".claude" / "settings.local.json").write_text("{}", encoding="utf-8")


def add_project_agent(repo, home):
    # A project agent takes precedence over the installed one of the same name.
    (repo / ".claude" / "agents").mkdir(parents=True)
    (repo / ".claude" / "agents" / "aie-fetcher.md").write_text(
        "tools: Bash\n", "utf-8"
    )


def add_project_rules(repo, home):
    (repo / ".claude" / "rules").mkdir(parents=True)
    (repo / ".claude" / "rules" / "x.md").write_text("Run x.sh.\n", "utf-8")


def add_project_rules_file(repo, home):
    (repo / "CLAUDE.md").write_text("Run x.sh.\n", "utf-8")


def add_agents_md(repo, home):
    (repo / "AGENTS.md").write_text("Run x.sh.\n", "utf-8")


def add_local_rules_file(repo, home):
    (repo / "CLAUDE.local.md").write_text("Run x.sh.\n", "utf-8")


def add_mcp_config(repo, home):
    (repo / ".mcp.json").write_text('{"mcpServers": {}}', "utf-8")


def add_user_settings(repo, home):
    (home / ".claude" / "settings.json").write_text("{}", encoding="utf-8")


def add_user_rules_file(repo, home):
    (home / ".claude" / "CLAUDE.md").write_text("Run x.sh.\n", "utf-8")


def add_user_rules(repo, home):
    (home / ".claude" / "rules").mkdir()
    (home / ".claude" / "rules" / "x.md").write_text("Run x.sh.\n", "utf-8")


def add_installed_agent(repo, home):
    agent = home / ".claude" / "agents" / "general-purpose.md"
    agent.write_text("tools: Bash\n", encoding="utf-8")


def widen_installed_agent(repo, home):
    agent = home / ".claude" / "agents" / "aie-fetcher.md"
    agent.write_text("tools: Read, Bash\n", encoding="utf-8")


@pytest.mark.parametrize(
    "change",
    [
        add_hook,
        edit_git_config,
        edit_global_git_config,
        add_xdg_git_config,
        edit_included_git_config,
        add_project_settings,
        add_project_agent,
        add_project_rules,
        add_project_rules_file,
        add_agents_md,
        add_local_rules_file,
        add_mcp_config,
        add_user_settings,
        add_user_rules_file,
        add_user_rules,
        add_installed_agent,
        widen_installed_agent,
    ],
)
def test_snapshot_changes_when_a_file_that_runs_code_changes(tmp_path, change):
    repo, home = snapshot_repo(tmp_path)
    snapshot = load("snapshot")
    before = snapshot.fingerprint(repo, home, clean_env())
    change(repo, home)
    assert snapshot.fingerprint(repo, home, clean_env()) != before


def test_snapshot_reads_the_global_config_git_config_global_names(tmp_path):
    repo, home = snapshot_repo(tmp_path)
    named = tmp_path / "global.cfg"
    named.write_text("[user]\n\tname = test\n", "utf-8")
    env = {**clean_env(), "GIT_CONFIG_GLOBAL": str(named)}
    snapshot = load("snapshot")
    before = snapshot.fingerprint(repo, home, env)
    with named.open("a", encoding="utf-8") as f:
        f.write("[core]\n\tsshCommand = ./x.sh\n")
    assert snapshot.fingerprint(repo, home, env) != before


def test_snapshot_ignores_the_data_a_rerun_writes(tmp_path):
    repo, home = snapshot_repo(tmp_path)
    snapshot = load("snapshot")
    before = snapshot.fingerprint(repo, home, clean_env())
    (repo / "data" / "claims.jsonl").write_text('{"cid": "c0001"}\n', encoding="utf-8")
    assert snapshot.fingerprint(repo, home, clean_env()) == before


def test_snapshot_prints_one_line_to_compare(tmp_path, capsys, monkeypatch):
    repo, home = snapshot_repo(tmp_path)
    snapshot = load("snapshot")
    for k in set(os.environ) - set(clean_env()):
        monkeypatch.delenv(k)
    assert snapshot.main(["--repo", str(repo), "--home", str(home)]) == 0
    expected = snapshot.fingerprint(repo, home, clean_env())
    assert capsys.readouterr().out == f"snapshot {expected}\n"


# --- data checks found by the review of #351 -------------------------------------------


@pytest.mark.parametrize("line", ["3", "[1, 2]", '"text"', "null"])
def test_check_data_names_a_record_that_is_not_an_object(tmp_path, line):
    d = clean_data_dir(tmp_path)
    (d / "claims.jsonl").write_text(line + "\n", encoding="utf-8")
    assert load("check_data").check(d) == ["claims.jsonl:1: not an object"]


@pytest.mark.parametrize("key", ["singletons", "noise"])
def test_check_data_names_a_group_list_that_is_not_keys(tmp_path, key):
    d = clean_data_dir(tmp_path)
    group = json.loads((d / "clusters" / "A.json").read_text(encoding="utf-8"))
    group[key] = [1]
    (d / "clusters" / "A.json").write_text(json.dumps(group), encoding="utf-8")
    assert load("check_data").check(d) == [
        f"clusters/A.json: field '{key}' is not a list of keys"
    ]


def test_check_data_names_a_merge_map_without_its_list(tmp_path):
    d = clean_data_dir(tmp_path)
    (d / "merge-map.json").write_text("{}", encoding="utf-8")
    assert load("check_data").check(d) == ["merge-map.json: missing field 'merged'"]


@pytest.mark.parametrize(
    "raw",
    [
        # Two backslashes in the text, four in the JSON line.
        json.dumps({**CLAIM, "claim": "see C:\\\\Users\\\\someone"}),
        # A backslash written as a unicode escape.
        json.dumps(CLAIM).replace("Keep tasks small.", "see C:\\u005cUsers\\u005cx"),
    ],
)
def test_check_data_reads_escaped_text_for_personal_references(tmp_path, raw):
    d = clean_data_dir(tmp_path)
    (d / "claims.jsonl").write_text(raw + "\n", encoding="utf-8")
    errors = load("check_data").check(d)
    assert [e.split(" (")[0] for e in errors] == ["claims.jsonl:1: personal reference"]


@pytest.mark.parametrize("name", ["clusters/A.json", "merge-map.json"])
def test_check_data_scans_group_files_for_personal_references(tmp_path, name):
    d = clean_data_dir(tmp_path)
    doc = json.loads((d / name).read_text(encoding="utf-8"))
    first = doc["clusters"][0] if "clusters" in doc else doc["merged"][0]
    first["idea"] = "see C:\\Users\\someone\\notes"
    (d / name).write_text(json.dumps(doc), encoding="utf-8")
    errors = load("check_data").check(d)
    assert [e.split(" (")[0] for e in errors] == [f"{name}: personal reference"]


def test_check_data_skips_bytecode_only_in_the_pipeline(tmp_path):
    d = clean_data_dir(tmp_path)
    (d / "pipeline" / "__pycache__").mkdir(parents=True)
    (d / "pipeline" / "__pycache__" / "x.pyc").write_bytes(b"\x00")
    (d / "clusters" / "__pycache__").mkdir()
    (d / "clusters" / "__pycache__" / "x.pyc").write_bytes(b"\x00")
    assert load("check_data").check(d) == [
        "clusters/__pycache__/x.pyc: no schema for this file;"
        " add one to check_data.py or move it out"
    ]


def test_merge_keeps_an_area_file_name_short(tmp_path):
    data = tmp_path / "data"
    write_jsonl(data / "claims.jsonl", [CLAIM])
    write_jsonl(data / "talks.jsonl", [TALK])
    run_merge(
        tmp_path,
        data,
        [batch_talk("talk:b"), {**batch_claim("talk:b", "One."), "area": "a b" * 200}],
    )
    assert [p.name for p in (tmp_path / "areas").iterdir()] == ["a-b" * 20 + ".tsv"]


# --- the step files: what the credentialed session runs -------------------------------


def step_text(name):
    return (PIPELINE / name).read_text(encoding="utf-8")


def script_calls(text):
    return re.findall(r"python(?: -\w+)* (?:data/pipeline|scripts)/\w+\.py", text)


@pytest.mark.parametrize("name", ["README.md", "commit.md"])
def test_every_script_step_runs_python_isolated(name):
    # -I leaves out the user's site-packages (usercustomize) and PYTHON* variables; -B
    # writes no bytecode into data/pipeline/.
    calls = script_calls(step_text(name))
    assert calls
    assert [c for c in calls if not c.startswith("python -I -B ")] == []


@pytest.mark.parametrize("name", ["README.md", "commit.md"])
def test_every_git_command_of_the_session_turns_off_fsmonitor(name):
    commands = re.findall(r"`(git [^`]*)`", step_text(name))
    assert commands
    assert [c for c in commands if "-c core.fsmonitor=false" not in c] == []


def test_the_unchanged_check_covers_the_tree_outside_data():
    assert (
        "git -c core.fsmonitor=false status --porcelain -- . "
        '":(exclude)data" ":(exclude)CHANGELOG.md"'
    ) in step_text("README.md")


def test_the_commit_step_takes_its_counts_from_the_scripts_only():
    # The match verdicts and the cluster count reach the session only in agent returns.
    text = step_text("commit.md").lower()
    assert "verdict" not in text
    assert "new clusters" not in text


def test_the_pull_request_body_is_written_outside_scratch():
    text = step_text("commit.md")
    assert "<scratch>/pr-body" not in text
    assert "--body-file <body>/pr-body.md" in text


def allowed_reads():
    text = step_text("agents/aie-fetcher.md")
    line = next(x for x in text.splitlines() if x.startswith("Read only these local"))
    return set(re.findall(r"`([^`]+)`", line))


def test_the_fetcher_may_read_every_local_file_its_steps_name():
    assert allowed_reads() == {
        "data/pipeline/fetch.md",
        "data/sources.md",
        "data/talks.jsonl",
    }
    named = set(
        re.findall(
            r"`?((?:\.\./|data/)[\w./-]+\.(?:md|jsonl))`?", step_text("fetch.md")
        )
    )
    assert named <= allowed_reads()
