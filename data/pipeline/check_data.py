"""Field check for the published data (#341): every file carries only its allowed fields.

Usage: python data/pipeline/check_data.py [data dir]   (default: the data/ beside this file)

Each data file has a schema below: the exact fields of its records, or the exact header of
its table. A field outside the schema (a maintainer's status or relevance column, a talk's
title or speakers fetched from the conference site) fails the check, and so does a file with
no schema. Every text file under the data directory, the pipeline's own instructions
included, is also scanned for references to the maintainer's private material: a home path
or one of the private file names. Prints one line per problem; exit 1 when there is any.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CLAIM_FIELDS = (
    "cid",
    "talk",
    "claim",
    "kind",
    "evidence",
    "depth",
    "area",
    "search",
    "quality",
    "pitch",
)
TALK_FIELDS = ("id", "gist", "quality", "pitch", "audience")
CLUSTER_FIELDS = ("key", "title", "idea", "contested", "cids")
GROUP_FIELDS = ("clusters", "singletons", "noise")
MERGED_FIELDS = ("key", "title", "idea", "contested", "from")
INDEX_HEADER = ["key", "talks", "title", "idea"]

# Files that are prose or code, not data: scanned for personal references only.
TEXT_SUFFIXES = (".md", ".py")

# The source of each pattern escapes its dot or backslash, so this file does not match itself.
PERSONAL = [
    re.compile(r"[A-Za-z]:\\Users\\", re.I),
    re.compile(r"/(?:home|Users)/\w[\w.-]*/"),
    re.compile(r"\bknown\.md\b", re.I),
    re.compile(r"\bbacklog\.md\b", re.I),
    re.compile(r"\bbriefings[/\\]", re.I),
]


def fields(where, record, allowed):
    errors = [f"{where}: missing field '{k}'" for k in allowed if k not in record]
    errors += [f"{where}: unexpected field '{k}'" for k in record if k not in allowed]
    return errors


def personal(where, text):
    for n, line in enumerate(text.splitlines(), 1):
        for pat in PERSONAL:
            if pat.search(line):
                return [f"{where}:{n}: personal reference ({pat.pattern})"]
    return []


def check_jsonl(rel, text, allowed):
    errors = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"{rel}:{n}: not JSON")
            continue
        errors += fields(f"{rel}:{n}", record, allowed)
    return errors + personal(rel, text)


def check_group(rel, text):
    group = json.loads(text)
    errors = [f"{rel}: unexpected field '{k}'" for k in group if k not in GROUP_FIELDS]
    for cluster in group.get("clusters", []):
        errors += fields(
            f"{rel}: cluster {cluster.get('key')}", cluster, CLUSTER_FIELDS
        )
    return errors + personal(rel, text)


def check_merge_map(rel, text):
    doc = json.loads(text)
    errors = [f"{rel}: unexpected field '{k}'" for k in doc if k != "merged"]
    for m in doc.get("merged", []):
        errors += fields(f"{rel}: {m.get('key')}", m, MERGED_FIELDS)
    return errors + personal(rel, text)


def check_index(rel, text):
    header = text.splitlines()[0].split("\t") if text else []
    if header != INDEX_HEADER:
        return [f"{rel}: header is {header}, expected {INDEX_HEADER}"]
    return personal(rel, text)


def check(data_dir: Path) -> list[str]:
    errors = []
    for path in sorted(p for p in data_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(data_dir).as_posix()
        if "__pycache__" in rel:
            continue
        text = path.read_text(encoding="utf-8")
        if rel == "claims.jsonl":
            errors += check_jsonl(rel, text, CLAIM_FIELDS)
        elif rel == "talks.jsonl":
            errors += check_jsonl(rel, text, TALK_FIELDS)
        elif rel == "merge-map.json":
            errors += check_merge_map(rel, text)
        elif rel == "cluster-index.tsv":
            errors += check_index(rel, text)
        elif re.fullmatch(r"clusters/[A-Z]\.json", rel):
            errors += check_group(rel, text)
        elif path.suffix in TEXT_SUFFIXES:
            errors += personal(rel, text)
        else:
            errors.append(
                f"{rel}: no schema for this file; add one to check_data.py or move it out"
            )
    return errors


def main(argv: list[str]) -> int:
    data_dir = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent
    errors = check(data_dir)
    for e in errors:
        print(e)
    print(f"{'FAIL' if errors else 'ok'}: {len(errors)} problem(s) in {data_dir}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
