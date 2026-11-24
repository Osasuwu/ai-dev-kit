"""Count the talks with no event that a rerun has not published (#360).

Usage: python data/pipeline/no_event.py count <scratch>/listing.json --known data/talks.jsonl

The fetch step lists talks through the MCP event filter, which never matches a talk with no
event, so those talks are counted, not listed (`fetch.md`, step 3). The fetcher writes the
ids it listed and two numbers it read, and this script does the counting:

- `T`, the corpus size, and `E`, the talks whose event names a year: `N0 = T - E` have none.
  `E` above `T` is refused.
- `P`: published ids (`--known`) that are not in any list. A published talk with an event
  in scope is in a list, so these are the published talks with no event.
- `N0 - P` talks with no event are not published yet, and the rerun does not check them:
  no bounded MCP call series lists them (`data/sources.md`), and the script says so
  whenever there are any. Below 0, some published talk is missing from the lists for
  another reason (an event out of scope, a gap, a renamed or dropped talk), and the count
  cannot say which: all `N0` are reported, with that reason (none when `N0` is 0).

Each id must be `talk:` and a slug of lowercase letters, digits and single hyphens, the form
every published id has; any other id refuses the whole listing. A list whose `total` differs from the distinct ids read is a gap, printed on a line of its
own and named by its place (`lists[0]`). The gap check compares two numbers the fetcher
wrote, so it catches a copying slip, not a wrong or injected listing.

`listing.json` stays outside the repo. The script prints numbers, list places and fixed
text only, never an id or other text read from either file: a file it cannot read is
named with the error's type, not its message.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TALK_ID = re.compile(r"talk:[a-z0-9]+(?:-[a-z0-9]+)*")
NOT_REACHED = (
    "not checked: no bounded MCP call series lists the talks with no event "
    "(data/sources.md)"
)
BELOW_ZERO = (
    "not checked: a published talk is missing from the lists for another reason "
    "(an event out of scope, a gap, a renamed or dropped talk), so the count cannot "
    "tell which talks are new"
)


class Refused(Exception):
    pass


def whole(value, name: str) -> int:
    if type(value) is not int or value < 0:
        raise Refused(f"{name} is not a whole number")
    return value


def talk_ids(value, name: str) -> list[str]:
    if not isinstance(value, list):
        raise Refused(f"{name} is not a list")
    for i, x in enumerate(value):
        if not isinstance(x, str) or not TALK_ID.fullmatch(x):
            raise Refused(f"{name}[{i}] is not a talk id")
    return value


def read_listing(path: Path) -> tuple[int, int, list[tuple[int, list[str]]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise Refused("not an object")
    t = whole(data.get("T"), "T")
    e = whole(data.get("E"), "E")
    if e > t:
        raise Refused("E is above T")
    lists = data.get("lists")
    if not isinstance(lists, list):
        raise Refused("lists is not a list")
    out = []
    for i, item in enumerate(lists):
        if not isinstance(item, dict) or not isinstance(item.get("s"), str):
            raise Refused(f"lists[{i}] has no event substring s")
        total = whole(item.get("total"), f"lists[{i}].total")
        out.append((total, talk_ids(item.get("ids"), f"lists[{i}].ids")))
    return t, e, out


def known_ids(path: Path) -> set[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return {json.loads(x)["id"] for x in lines if x.strip()}


def read(path: Path, reader):
    """Run reader on path; any failure becomes a Refused naming the file, not its text."""
    try:
        return reader(path)
    except Refused as err:
        raise Refused(f"{path.name}: {err}") from None
    # JSONDecodeError, UnicodeDecodeError and an over-long int are ValueErrors; deep
    # nesting is a RecursionError; a missing file is an OSError; a known line with no
    # id is a KeyError or TypeError.
    except (ValueError, RecursionError, OSError, KeyError, TypeError) as err:
        raise Refused(f"{path.name}: unreadable ({type(err).__name__})") from None


def count(listing: Path, known: Path) -> list[str]:
    t, e, lists = read(listing, read_listing)
    published_ids = read(known, known_ids)
    lines = []
    listed: set[str] = set()
    for i, (total, ids) in enumerate(lists):
        listed.update(ids)
        if total != len(set(ids)):
            lines.append(f"list gap: lists[{i}] total {total}, read {len(set(ids))}")
    n0 = t - e
    published = len(published_ids - listed)
    unchecked = n0 - published
    # Below 0 all N0 are reported; with N0 at 0 there is no talk to leave unchecked.
    below = unchecked < 0 and n0 > 0
    shown = f"{n0} (all: count below 0)" if below else f"{max(unchecked, 0)}"
    lines.append(
        f"no event {n0}, published {published}, not checked {shown}, "
        f"list gaps {len(lines)}"
    )
    if below:
        lines.append(BELOW_ZERO)
    elif unchecked > 0:
        lines.append(NOT_REACHED)
    return lines


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="command", required=True)
    c = sub.add_parser("count")
    c.add_argument("listing", type=Path)
    c.add_argument("--known", type=Path, required=True)
    args = ap.parse_args(argv)

    try:
        lines = count(args.listing, args.known)
    except Refused as err:
        print(err)
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
