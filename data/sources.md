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
  browser `User-Agent`. The rerun's fetcher uses `WebFetch`, which cannot set one; if the API
  refuses it, the fetcher says so and the run uses the MCP tools below. The 2026 talk list
  carried `slug`, `title`, `url`, `event`, `durationMs`, `speakers`, `topics`, `summary` and
  `slideText` per talk. The talk list dataset's name and the API's current shape were not checked when this file was written:
  the first supervised rerun checks them and corrects this line.
- **Talk records and citations**: the `ai-engineer` MCP server. `fetch` with `id` =
  `talk:<slug>` returns the talk; with `section: "transcript"` and `query` = a claim's `search`
  phrase it returns transcript passages, each with a `citation` in Markdown, a link with the
  timestamp. A citation is copied verbatim, never computed or edited.
- `list_conferences`, `get_schedule` and `search` on the same server list conferences and
  their talks.

## A dropped talk

If the conference removes or renames a talk, its claims stay in `claims.jsonl` under the old
id, with no source to refetch: the claim keeps its text and its id, and its source is gone. A
rerun finds such claims as talk ids that the fetched list no longer has. Claims are never
deleted to hide this, because clusters list them by id.

## The rerun

How a rerun fetches, extracts and commits: [`pipeline/README.md`](pipeline/README.md).
