# Sources and the refetch path

The data here is derived from the AI Engineer conference talks. Nothing fetched from
ai.engineer is stored in this repo: no talk title, URL, event, duration, speaker, summary,
slide text, transcript, chapter or citation. What is stored is derived from them (claims,
gists, clusters) plus each talk's id, which is the key to fetch the rest again.

## Talk ids

A talk id is `talk:<slug>`, where the slug is the conference's own. It appears in
`talks.jsonl` (`id`) and `claims.jsonl` (`talk`). It is the one value taken from the source,
kept because the refetch needs it. Some slugs contain speakers' names, as the conference wrote
them.

## Refetch

- **Talk lists and talk records**: the conference data API,
  `https://ai.engineer/api/data/<dataset>?format=json`. The datasets `status` (`publishedAt`,
  `corpusVersion`), `topics` and `chapters` were used before, by a script that sent a
  browser `User-Agent`. The 2026 talk list carried `slug`, `title`, `url`, `event`,
  `durationMs`, `speakers`, `topics`, `summary` and `slideText` per talk. Checked on
  2026-11-22 (#357): the talk list is most likely the dataset `talks`, by its name and size;
  its response was never read. `WebFetch` is not refused, but the `talks` response is over
  its 10 MB cap with each parameter tried (`limit`, `page`, `fields`, `event`,
  `format=csv`), so the rerun's fetcher does not use the data API and has no `WebFetch`;
  it uses the MCP `search` and `fetch` below. `status` works and gives `counts.talks`, the corpus size, but no count per
  event. `/api/data` and `/api/data/datasets` return 404.
- **Talk records and citations**: the `ai-engineer` MCP server. `fetch` with `id` =
  `talk:<slug>` returns the talk; with `section: "transcript"` and `query` = a claim's `search`
  phrase it returns transcript passages, each with a `citation` in Markdown, a link with the
  timestamp. A citation is copied verbatim, never computed or edited.
- `list_conferences`, `get_schedule` and `search` on the same server list conferences and
  their talks. `search(kind="talk")` needs a filter (event, topic, speaker or organization)
  and returns at most 10 talks per call (its `limit` maximum), with `pagination.total`. Its
  `event` filter matches part of the event name and never matches a talk with no event, and
  conference records list no talks, so the rerun counts the talks with no event rather
  than listing them (`pipeline/fetch.md`, step 3; the count is `pipeline/no_event.py`'s).
  A talk with no event has `"event": null` in search results and in its record.
- **Talks with no event: why the rerun does not list them** (#360; the rerun's fetcher does
  not use this route and does not open the page below). The topic filter and the topic
  records reach them, but no bounded call series lists them all. Checked on 2026-11-24:
  - `fetch` with `id` = `topic:<slug>` returns the topic's complete `talkIds`, unpaginated,
    with no event per id (on 3 topics, the same count as the topic filter's total: 8, 49
    and 532).
  - The topic filter's results carry each talk's `event`, 10 per call, so one topic of 532
    talks is 53 calls; a talk sits in several topics.
  - No MCP call lists every topic: `search(kind="topic")` needs a query, then reports 87
    topics with no pagination; keyword queries found 85 of them. The page
    `https://ai.engineer/topics` lists the slugs.
  - A talk record's `topics` are titles, not slugs. The `youtube-` slug prefix does not mark
    a talk with no event.

  A listing becomes possible if the MCP gains a topic list or a filter for talks with no
  event.

## A dropped talk

If the conference removes or renames a talk, its claims stay in `claims.jsonl` under the old
id, with no source to refetch: the claim keeps its text and its id, and its source is gone. A
rerun finds such claims as talk ids that the fetched list no longer has. Claims are never
deleted to hide this, because clusters list them by id.

## The rerun

How a rerun fetches, extracts and commits: [`pipeline/README.md`](pipeline/README.md).
