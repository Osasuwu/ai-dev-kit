"""Split a fetched talk list into batch files for claim extraction (#341).

Usage: python data/pipeline/batches.py <talk list> <out dir> <batch size>
           --event-pattern <regex> [--known data/talks.jsonl]

The talk list is what the fetch step wrote outside the repo: a JSON array, or a CSV with a
header, of records with `slug`, `title`, `url`, `event`, `durationMs`, `speakers`, `topics`,
`summary` and `slideText`. A talk is picked when its event matches the pattern, or when it
has no event. The pattern is the caller's: the tool holds no year. With `--known`, talks
whose id is already in the published talk records are skipped, so a rerun extracts only new
talks. Writes `index.json` and `batch-NN.json` to the out dir, which stays outside the repo:
both hold text fetched from the conference site.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


def load_rows(src: Path) -> list[dict]:
    if src.suffix == ".json":
        return json.loads(src.read_text(encoding="utf-8"))
    csv.field_size_limit(10**9)
    with open(src, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def known_ids(path: Path | None) -> set[str]:
    if path is None:
        return set()
    lines = path.read_text(encoding="utf-8").splitlines()
    return {json.loads(x)["id"] for x in lines if x.strip()}


def as_list(value) -> list:
    if isinstance(value, list):
        return value
    return json.loads(value or "[]")


def select(rows: list[dict], pattern: str, known: set[str]) -> list[dict]:
    event = re.compile(pattern)
    return [
        r
        for r in rows
        if (not r.get("event") or event.search(r["event"]))
        and "talk:" + r["slug"] not in known
    ]


def talk_record(r: dict) -> dict:
    return {
        "id": "talk:" + r["slug"],
        "title": r.get("title"),
        "url": r.get("url"),
        "event": r.get("event") or None,
        "minutes": round(int(r.get("durationMs") or 0) / 60000),
        "speakers": [s.get("name") for s in as_list(r.get("speakers"))],
        "topics": [t.get("slug") for t in as_list(r.get("topics"))],
        "summary": r.get("summary") or "",
        "slides": (r.get("slideText") or "")[:2500],
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("batch_size", type=int)
    ap.add_argument("--event-pattern", required=True)
    ap.add_argument("--known", type=Path)
    args = ap.parse_args(argv)

    rows = load_rows(args.src)
    picked = select(rows, args.event_pattern, known_ids(args.known))
    print("picked", len(picked), "of", len(rows))
    talks = [talk_record(r) for r in picked]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    index_keys = ("id", "title", "url", "event", "minutes", "speakers")
    index = [{k: t[k] for k in index_keys} for t in talks]
    (args.out_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False), encoding="utf-8"
    )
    n = 0
    for i in range(0, len(talks), args.batch_size):
        n += 1
        (args.out_dir / f"batch-{n:02d}.json").write_text(
            json.dumps(talks[i : i + args.batch_size], ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
    print("batches", n)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv[1:]))
