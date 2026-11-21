# Practice cards

A card is one practice, one file in `cards/`: a setting to change, a habit to keep, or a belief
to hold loosely. Each card says why it matters, when it applies, how to check it in your own
setup, where to learn more, and what speaks for and against it, with dates.

Two files are generated from the cards and never edited by hand:

- [`INDEX.md`](../INDEX.md): one line per card, for an agent to read first.
- [`WATCH-LIST.md`](../WATCH-LIST.md): every card's learn links, the talks and pages to watch or read.

Add a card by writing one file here and running `python scripts/generate_card_index.py`.
Nothing else is edited.

This file is the card format. The structure gate (`tests/structure_gate.py`) reads the kinds,
the index line limit and the field table below from this file, so a change here changes what
the gate checks. The gate selects cards through `.github/hold-paths.json`, the same path
definition the link check reads.

## Kinds

- **Kinds:** config, habit, belief
- **Index line limit:** 100

- **config**: a setting in your agent, repository or CI. Comes from a failure-class doc's
  protections, so it has a fix you can apply.
- **habit**: something you do each time. No fix to apply: you either do it or you do not.
- **belief**: a claim about how agent work behaves, with the evidence for and against it.

The index line limit counts every line of `INDEX.md`, header included. The generator refuses
to write an index longer than that: merge or retire cards first (rules below).

## Fields

A card opens with a frontmatter block, then a `# <title>` line, then its sections as `## `
headings. A frontmatter field is a `key: value` line; a section field is a `## ` heading with
text under it. Kinds says which cards carry the field: `all`, `optional`, or the kinds named.
A field named for some kinds is required on those and not allowed on the others.

| Field | Where | Kinds | Meaning |
|---|---|---|---|
| `kind` | frontmatter | all | One of the kinds above. |
| `why` | frontmatter | all | One sentence: what goes wrong without the practice. It is the card's line in the index. |
| `applies_when` | frontmatter | all | One sentence: the setup the card is for. A reader whose setup does not match skips the card. |
| `last_reviewed` | frontmatter | all | The date, `YYYY-MM-DD`, someone last read the card against its sources. |
| `Check` | section | all | How to tell, in your own setup, whether the practice holds. A command where one exists. |
| `Fix` | section | config | How to apply the setting. Only config cards have one. |
| `Learn` | section | all | Links to talks, docs or pages, at least one, each with a line on what to look for. A talk link carries its timestamp. |
| `Evidence for` | section | all | Bullets, each opening with a date `YYYY-MM-DD:`: what supports the card, with its source. |
| `Evidence against` | section | all | Bullets, each opening with a date: what speaks against the card or limits it. None found is a bullet too, dated. |
| `Guards` | section | optional | Links to the failure-class docs in `docs/classes/` the practice protects against. |

The gate also checks the values it can read: `kind` is a listed kind, `last_reviewed` is a real
date, `Learn` has a link, every evidence bullet opens with a date, every `Guards` link names a
class doc, and every relative link resolves to a file. The link check (`link-check`) reports a
web link in a changed card that is dead.

The date on an evidence bullet is the day the entry was written or last checked against its
source, not the day the source was published.

A card that names failure classes under `Guards` gets the caveat that the class evidence is
one operator's practice on its index line, added by the generator: the incident base behind the
classes comes mostly from the maintainer's own repositories (see the class map in the
[README](../README.md)).

## Staleness, retiring and merging

- **Stale.** A card whose `last_reviewed` is more than 6 months old is stale. Review it: open
  each source, re-date the evidence that still holds, drop what no longer does, set
  `last_reviewed` to today. If nobody can review it, retire it.
- **Retire** a card when its evidence against outweighs its evidence for, when the setting or
  tool it names no longer exists, or when its check can no longer fail. Delete the file and
  regenerate; the history keeps it.
- **Merge** two cards when one's check also checks the other, or both fix the same thing.
  Keep one file, carry both evidence lists into it with their dates, delete the other, and
  regenerate.
- **Index full.** When a new card would push `INDEX.md` over the line limit, merge or retire
  before adding. The limit is raised only by editing it above, in its own pull request.
