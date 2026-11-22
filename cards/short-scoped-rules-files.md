---
kind: config
why: A long rules file is followed less, a capped loader drops its tail without a word, and a rule for one corner of the code competes with every other rule in every session.
applies_when: you steer an agent with rules files it loads by itself (CLAUDE.md, AGENTS.md, Cursor or Copilot instruction files, a memory index)
last_reviewed: 2026-11-22
---

# Keep the always-loaded rules file short, scope the rest to its files, and make a cut visible

## Check

Measure each file the agent loads every session, in lines and in bytes:

```
wc -lc CLAUDE.md AGENTS.md .claude/CLAUDE.md ~/.claude/CLAUDE.md 2>/dev/null
```

Compare against your tool's documented limits: Claude Code suggests under 200 lines per
CLAUDE.md and loads only the start of its memory index; Codex caps the combined size of its
AGENTS.md files. Count bytes, not characters: non-ASCII text takes more than one byte each.
Then read the file and mark every rule that applies only to some paths (a framework, a
directory, a file type). Each of those is a candidate to move. Finally, find out how you would
learn that a file was cut or not loaded; if the answer is that you would not, the check fails.

## Fix

- Keep the always-loaded file to short, concrete rules that apply to every task, well under the
  tool's cap.
- Move rules for part of the code into scoped files: Claude Code path-scoped rules with a
  `paths:` pattern, a nested AGENTS.md in the directory it governs, Copilot instruction files
  with `applyTo`.
- Replace a sentence that tells the agent to read another file with an import, where the tool
  has one; a file named in prose is read only if the model decides to open it.
- Make a cut visible: log loads with Claude Code's `InstructionsLoaded` hook, or have your own
  loader print how much it dropped inside the text it injects. Add a size check in CI for the
  capped files.

## Learn

- [Claude Code memory](https://code.claude.com/docs/en/memory): the size guidance, path-scoped rules, imports, the memory index cap, and the `InstructionsLoaded` hook.
- [AGENTS.md](https://agents.md/): nested files and the nearest-first rule.
- [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md): the combined size cap and splitting large files across directories.
- [Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions): path-specific instruction files with `applyTo`.

## Evidence for

- 2026-11-22: on an instruction-following benchmark, the best frontier models reached 68% accuracy at 500 instructions, with a bias toward earlier ones ([Jaroslawicz et al.](https://arxiv.org/abs/2507.11538), via [knowledge not at the point of action](../docs/classes/knowledge-not-at-point-of-action.md)).
- 2026-11-22: Claude Code's docs state that longer CLAUDE.md files consume more context and reduce adherence.
- 2026-11-22: in one operator's incidents, a capped index cut off its newest entries first, because new entries were appended at the end, and nobody saw the cut ([knowledge not at the point of action](../docs/classes/knowledge-not-at-point-of-action.md), INC-660, INC-661).

## Evidence against

- 2026-11-22: across 1,650 Claude Code sessions, file size and instruction position had no detectable effect on compliance; what mattered was how much code the agent had written in the session ([McMillan](https://arxiv.org/abs/2605.10039), via the class doc). A short file does not fix a long session.
- 2026-11-22: context files did not generally improve task success and raised inference cost by over 20% on average, though their instructions were followed ([Gloaguen et al.](https://arxiv.org/abs/2602.11988), via the class doc).
- 2026-11-22: a scoped rule can be summarized away by compaction until a matching file is read again, a rule about a commit or a merge is tied to no file, and `InstructionsLoaded` does not fire for every load path. Actors that load no rules file, such as a CI job, never see any of it.

## Guards

- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
