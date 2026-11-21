"""Generate data/cluster-index.tsv from the published claims and clusters (#341).

Usage: python data/pipeline/build_index.py [data dir]   (default: the data/ beside this file)

Reads `claims.jsonl`, `clusters/<group>.json` and `merge-map.json`. A merge-map entry joins
clusters from several groups under one `M-` key; every cluster not named in the merge map
stays under its own key. A cluster counts the distinct talks its claims come from, and only
clusters with two talks or more are listed, most talks first. Columns: key, talks, title,
idea. The matching step reads this file; it carries no judgement about the maintainer.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def clean(value) -> str:
    return str(value).replace("\t", " ").replace("\n", " ")


def build(data: Path) -> list[str]:
    lines = (data / "claims.jsonl").read_text(encoding="utf-8").splitlines()
    talk_of = {c["cid"]: c["talk"] for c in map(json.loads, filter(None, lines))}
    clusters = {}
    for p in sorted((data / "clusters").glob("?.json")):
        for c in json.loads(p.read_text(encoding="utf-8"))["clusters"]:
            clusters[c["key"]] = c
    joined, used = {}, set()
    merge_map = data / "merge-map.json"
    if merge_map.exists():
        for m in json.loads(merge_map.read_text(encoding="utf-8"))["merged"]:
            cids = [cid for k in m["from"] for cid in clusters[k]["cids"]]
            joined[m["key"]] = {**m, "cids": cids}
            used.update(m["from"])
    for key, c in clusters.items():
        if key not in used:
            joined[key] = c
    rows = []
    for c in joined.values():
        n_talks = len({talk_of[cid] for cid in c["cids"] if cid in talk_of})
        if n_talks >= 2:
            rows.append((n_talks, c))
    rows.sort(key=lambda r: -r[0])
    out = ["key\ttalks\ttitle\tidea"]
    out += [
        "\t".join((c["key"], str(n), clean(c["title"]), clean(c["idea"])))
        for n, c in rows
    ]
    return out


def main(argv: list[str]) -> int:
    data = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent
    rows = build(data)
    (data / "cluster-index.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(data / "cluster-index.tsv", len(rows) - 1, "clusters")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
