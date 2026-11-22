---
kind: config
why: A deny list of dangerous commands lets through every spelling nobody thought of, so the agent runs what the list was meant to stop through a path, a wrapper, a chain or a flag.
applies_when: an agent runs shell commands without asking, under permission rules or a hook that matches command text
last_reviewed: 2026-11-22
---

# Allow known commands, parse before matching, and test every rule

## Check

Read the agent's permission settings, at every level that applies (user, project, local), and
ask three questions.

- Is it an allow list? Commands not on it should prompt or be refused. A setup that runs
  everything except a deny list fails this check, as does a mode that skips prompts.
- Does the matcher split compound commands and ask when it cannot parse one? A rule that compares
  the raw text treats `a && b` as `a`.
- Is there a test for each rule? For Codex rules, `codex execpolicy check` shows how the rule file
  treats a given command; elsewhere, look for a test file that runs your hook against a list of
  spellings it must and must not match.

An allow rule that ends in a wildcard, such as one for a package runner or an environment
wrapper, approves whatever follows it: count those as unlisted.

## Fix

Start from an empty allow list and add the commands the agent runs, read from its logs, with the
arguments they take. Keep the wildcards narrow and off programs that run other programs. Use a
tool that parses the command into a list of programs and arguments before matching, and treats a
command it cannot parse as one to ask about. Put every rule's examples, and every bypass reported
against it, in a test that runs in CI, so a fixed bypass cannot come back.

## Learn

- [Claude Code permissions](https://code.claude.com/docs/en/permissions.md): how compound commands are split, which forms a rule misses, and why a rule is not a boundary around a program.
- [Codex rules](https://developers.openai.com/codex/rules): rules on the argument list, and `match` and `not_match` examples checked when the rules load.
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html): why allow lists beat lists of bad strings, and why to parse with a maintained parser.

## Evidence for

- 2026-11-22: after researchers showed a coding agent's auto-run denylist bypassed, they advised an allowlist and the vendor deprecated the denylist ([Backslash](https://www.backslash.security/blog/cursor-ai-security-flaw-autorun-denylist)).
- 2026-11-22: a researcher who found eight bypasses of one agent's command blocklist reports that its replacement moved to an allowlist ([Flatt Security](https://flatt.tech/research/posts/pwning-claude-code-in-8-different-ways/)).
- 2026-11-22: two agent vendors split chained commands before matching and fall back to asking, or to matching the whole invocation, when the command uses forms they cannot resolve ([Claude Code permissions](https://code.claude.com/docs/en/permissions.md), [Codex rules](https://developers.openai.com/codex/rules)).

## Evidence against

- 2026-11-22: an allowed command can do more than its name says; its flags, arguments and whatever is chained after it ride on the approval, and a study found many agents do not validate argument flags ([Trail of Bits](https://blog.trailofbits.com/2025/10/22/prompt-injection-to-rce-in-ai-agents/)).
- 2026-11-22: a parser misses forms the rule does not name: an absolute path, a shell given the command as a string, an option before the subcommand; a file deny rule does not cover a command that writes the file without naming it ([Claude Code permissions](https://code.claude.com/docs/en/permissions.md)).
- 2026-11-22: tests hold only the spellings someone already thought of; they stop an old bypass from returning and say nothing about the next one ([pattern-matched boundaries](../docs/classes/pattern-matched-boundaries.md)).
- 2026-11-22: it costs a prompt for every unlisted or unparsable command, and upkeep of the list.

## Guards

- [pattern-matched-boundaries](../docs/classes/pattern-matched-boundaries.md)
