"""Field check for the published data (#341): every file carries only its allowed fields.

Usage: python data/pipeline/check_data.py [data dir]   (default: the data/ beside this file)

Each data file has a schema below: the exact fields of its records, each a single value
except the key lists, the grades (`quality`, `depth`, `pitch`) in their range, or the exact
columns of its table, header and rows. A field outside the schema (a maintainer's status or
relevance column, a talk's title or speakers fetched from the conference site), a value that
nests more fields or falls outside its range, and a file with no schema fail the check. The only text files allowed are data/README.md, data/sources.md and the
pipeline's own .md and .py files; they and every data file are also scanned for references
to the maintainer's private material: a home path or one of the private file names, in the
text of the prose, code and index files and in every decoded string of the JSON files, so no
escape hides one. A JSON
record that is not an object is reported, not a crash. Prints
one line per problem; exit 1 when there is any.
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
# The only fields that hold a list, and each list holds strings (claim or cluster keys).
LIST_FIELDS = ("cids", "from", "singletons", "noise")
# Grades the extraction step gives: a value outside these is a broken record, for example a
# claim whose talk had no talk record to copy its grades from.
GRADE = (lambda v: type(v) is int and 1 <= v <= 5, "an integer 1-5")
FLAG = (lambda v: type(v) is bool, "true or false")
VALUE_RULES = {"quality": GRADE, "depth": GRADE, "pitch": FLAG}

# Prose and code, not data: scanned for personal references only. Only these two files and the
# pipeline's own folder; any other .md or .py under data/ has no schema.
TEXT_FILES = ("README.md", "sources.md")
TEXT_DIR = "pipeline/"
TEXT_SUFFIXES = (".md", ".py")

# The source of each pattern escapes its dot or backslash, so this file does not match itself.
# A Windows home path is matched with single or doubled backslashes: JSON escapes them.
PERSONAL = [
    re.compile(r"[A-Za-z]:\\{1,2}Users\\{1,2}", re.I),
    re.compile(r"/(?:home|Users)/\w[\w.-]*/"),
    re.compile(r"\bknown\.md\b", re.I),
    re.compile(r"\bbacklog\.md\b", re.I),
    re.compile(r"\bbriefings[/\\]", re.I),
]


def single_or_listed(key, value):
    if key in LIST_FIELDS:
        return isinstance(value, list) and all(isinstance(x, str) for x in value)
    return not isinstance(value, (dict, list))


def fields(where, record, allowed):
    errors = [f"{where}: missing field '{k}'" for k in allowed if k not in record]
    errors += [f"{where}: unexpected field '{k}'" for k in record if k not in allowed]
    errors += [
        f"{where}: field '{k}' is not a single value"
        for k in sorted(record)
        if k in allowed and not single_or_listed(k, record[k])
    ]
    errors += [
        f"{where}: field '{k}' is {record[k]!r}, expected {VALUE_RULES[k][1]}"
        for k in sorted(record)
        if k in allowed
        and k in VALUE_RULES
        and single_or_listed(k, record[k])
        and not VALUE_RULES[k][0](record[k])
    ]
    return errors


def personal(where, text):
    for n, line in enumerate(text.splitlines(), 1):
        for pat in PERSONAL:
            if pat.search(line):
                return [f"{where}:{n}: personal reference ({pat.pattern})"]
    return []


def strings(value):
    """Every string in a parsed JSON value, keys included."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield k
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def personal_values(where, value):
    """The decoded text: a doubled or `\\u005c` escape hides a path from the raw line."""
    for s in strings(value):
        for pat in PERSONAL:
            if pat.search(s):
                return [f"{where}: personal reference ({pat.pattern})"]
    return []


def check_jsonl(rel, text, allowed):
    errors, found = [], []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"{rel}:{n}: not JSON")
            continue
        if not isinstance(record, dict):
            errors.append(f"{rel}:{n}: not an object")
            continue
        errors += fields(f"{rel}:{n}", record, allowed)
        found = found or personal_values(f"{rel}:{n}", record)
    return errors + found


def check_group(rel, text):
    group = json.loads(text)
    if not isinstance(group, dict):
        return [f"{rel}: not an object"]
    errors = [f"{rel}: missing field '{k}'" for k in GROUP_FIELDS if k not in group]
    errors += [f"{rel}: unexpected field '{k}'" for k in group if k not in GROUP_FIELDS]
    errors += [
        f"{rel}: field '{k}' is not a list of keys"
        for k in ("singletons", "noise")
        if k in group and not single_or_listed(k, group[k])
    ]
    for cluster in group.get("clusters", []):
        errors += fields(
            f"{rel}: cluster {cluster.get('key')}", cluster, CLUSTER_FIELDS
        )
    return errors + personal_values(rel, group)


def check_merge_map(rel, text):
    doc = json.loads(text)
    if not isinstance(doc, dict):
        return [f"{rel}: not an object"]
    errors = [f"{rel}: unexpected field '{k}'" for k in doc if k != "merged"]
    if "merged" not in doc:
        errors.append(f"{rel}: missing field 'merged'")
    for m in doc.get("merged", []):
        errors += fields(f"{rel}: {m.get('key')}", m, MERGED_FIELDS)
    return errors + personal_values(rel, doc)


def check_index(rel, text):
    header = text.splitlines()[0].split("\t") if text else []
    if header != INDEX_HEADER:
        return [f"{rel}: header is {header}, expected {INDEX_HEADER}"]
    errors = [
        f"{rel}:{n}: {len(cols)} columns, expected {len(INDEX_HEADER)}"
        for n, line in enumerate(text.splitlines()[1:], 2)
        if line and len(cols := line.split("\t")) != len(INDEX_HEADER)
    ]
    return errors + personal(rel, text)


def is_text_file(rel):
    in_place = rel in TEXT_FILES or rel.startswith(TEXT_DIR)
    return in_place and rel.endswith(TEXT_SUFFIXES)


def check(data_dir: Path) -> list[str]:
    errors = []
    for path in sorted(p for p in data_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(data_dir).as_posix()
        # Bytecode only where the pipeline's own scripts are; anywhere else it has no schema.
        if rel.startswith(TEXT_DIR) and "__pycache__" in rel.split("/")[:-1]:
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
        elif is_text_file(rel):
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
