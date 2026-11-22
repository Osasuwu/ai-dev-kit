"""Merge extracted claims into the published claim and talk records, keeping claim ids (#341).

Usage: python data/pipeline/merge_claims.py --claims-dir <dir> --data <data dir>
           --areas-out <dir> [--index <batches/index.json>]

Reads the extraction step's `batch-*.jsonl` files from the claims dir (talk records and claim
records, see extract.md) and the published `claims.jsonl` and `talks.jsonl` in the data dir.

Claim ids are stable across runs. A published claim keeps its id and its record. An
extracted claim that matches a published one (same talk, same text after collapsing
whitespace and case) is the same claim and is not added again. Every other extracted claim
gets the next id after the highest one published, so an id is never reused or renumbered and
the clusters that list claims by id stay valid. Running the merge twice on the same input
changes nothing the second time.

New talk records are added with the extraction step's own fields only (`gist`, `quality`,
`pitch`, `audience`); nothing fetched from the conference site goes into the data dir.
The area files written to --areas-out (outside the repo) hold the new claims only, one
TSV per area, as the input of the clustering step. With --index, talks of the batch index
with no talk record are counted: talks whose source had no text, which the next run tries
again, plus any extraction missed.

A batch line that is not JSON, a record without its `type` and the string fields it needs
(`talk`; a claim also `claim`), or a claim whose talk has no talk record (published or in a
batch) is a bad line: the merge writes nothing and exits 1. An area becomes a file name of
lower-case letters, digits and dashes only, so no area writes outside --areas-out.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

CLAIM_FIELDS = ("talk", "claim", "kind", "evidence", "depth", "area", "search")
TALK_FIELDS = ("gist", "quality", "pitch", "audience")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x]


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
        encoding="utf-8",
    )


def same_claim_key(talk: str, text: str) -> tuple[str, str]:
    return talk, re.sub(r"\s+", " ", text).strip().casefold()


def id_number(cid: str) -> int:
    return int(cid.removeprefix("c"))


def read_batches(claims_dir: Path) -> tuple[dict, list, list]:
    talks, claims, bad = {}, [], []
    for p in sorted(claims_dir.glob("batch-*.jsonl")):
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                bad.append(f"{p.name}:{n}")
                continue
            kind = rec.get("type") if isinstance(rec, dict) else None
            needs = {"talk": ("talk",), "claim": ("talk", "claim")}.get(kind)
            if needs is None or not all(isinstance(rec.get(k), str) for k in needs):
                bad.append(f"{p.name}:{n}")
            elif kind == "talk":
                talks[rec["talk"]] = rec
            else:
                claims.append(rec)
    return talks, claims, bad


def merge(data: Path, claims_dir: Path) -> tuple[list, list, list, list]:
    """Return (claims, talks, added claims, bad lines) after merging the batches."""
    claims = read_jsonl(data / "claims.jsonl")
    talks = read_jsonl(data / "talks.jsonl")
    batch_talks, batch_claims, bad = read_batches(claims_dir)

    known_talks = {t["id"] for t in talks}
    for tid, rec in batch_talks.items():
        if tid not in known_talks:
            talks.append({"id": tid, **{k: rec.get(k) for k in TALK_FIELDS}})
            known_talks.add(tid)
    talk_meta = {t["id"]: t for t in talks}

    seen = {same_claim_key(c["talk"], c["claim"]) for c in claims}
    next_n = max((id_number(c["cid"]) for c in claims), default=0) + 1
    added = []
    for rec in batch_claims:
        if rec["talk"] not in talk_meta:
            # Its grades come from the talk record; without one the claim would carry none.
            bad.append(f"claim for {rec['talk']}: no talk record")
            continue
        key = same_claim_key(rec["talk"], rec["claim"])
        if key in seen:
            continue
        seen.add(key)
        meta = talk_meta[rec["talk"]]
        claim = {"cid": f"c{next_n:04d}", **{k: rec.get(k) for k in CLAIM_FIELDS}}
        claim["quality"] = meta.get("quality")
        claim["pitch"] = meta.get("pitch")
        next_n += 1
        added.append(claim)
    return claims + added, talks, added, bad


def area_slug(area) -> str:
    """The area as a file name: lower-case letters, digits and dashes, nothing else."""
    slug = re.sub(r"[^a-z0-9]+", "-", str(area or "").lower()).strip("-")
    return slug or "other"


def write_areas(out: Path, added: list[dict]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    by_area = collections.defaultdict(list)
    for c in added:
        # The area is extraction output: a path in it must not reach outside `out`.
        by_area[area_slug(c.get("area"))].append(c)
    for area, cs in sorted(by_area.items()):
        rows = [
            "\t".join(
                (
                    c["cid"],
                    f"q{c['quality']}",
                    str(c.get("evidence", "?")),
                    f"d{c.get('depth', '?')}",
                    re.sub(r"[\t\n]", " ", c["claim"]),
                )
            )
            for c in cs
        ]
        (out / f"{area}.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--claims-dir", type=Path, required=True)
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--areas-out", type=Path, required=True)
    ap.add_argument("--index", type=Path)
    args = ap.parse_args(argv)

    claims, talks, added, bad = merge(args.data, args.claims_dir)
    if bad:
        # Writing now would publish the good lines, and a rerun after the fix would then
        # see them as published and leave them out of the clustering input.
        print(f"bad lines {len(bad)}: {', '.join(bad)}; nothing written")
        return 1
    args.data.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.data / "claims.jsonl", claims)
    write_jsonl(args.data / "talks.jsonl", talks)
    write_areas(args.areas_out, added)
    print(f"claims {len(claims)} (added {len(added)}) | talks {len(talks)}")
    if args.index:
        index = json.loads(args.index.read_text(encoding="utf-8"))
        have = {t["id"] for t in talks}
        missing = [t["id"] for t in index if t["id"] not in have]
        print("talks in the batch index without a talk record:", len(missing))
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv[1:]))
