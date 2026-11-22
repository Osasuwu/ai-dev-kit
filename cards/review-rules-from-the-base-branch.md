---
kind: config
why: A review bot that takes its rules from the pull request can be told by the change to pass it, and a script that reads its free text as a verdict counts a garbled or missing reply as clean.
applies_when: a model reviews pull requests and a script turns its reply into a check that gates the merge
last_reviewed: 2026-11-22
---

# Read the review rules from the base branch, and gate on a fixed verdict line

## Check

Open the workflow that runs the review and find two steps.

```
grep -n -i "review\|prompt\|checkout\|ref:" .github/workflows/*.yml
```

The step that loads the rules, the prompt and the parser script should take them from the base
commit or the default branch, not from the checkout of the pull request. The step that turns the
reply into pass or fail should read one line in a fixed format, and a reply without that line
should end as no verdict, never as zero findings. To probe it, open a scratch pull request that
edits the rules file to wave everything through: the review of that pull request should still
apply the old rules.

## Fix

If you use a hosted reviewer, check that it reads its rules from the base branch; Claude Code
code review does this for its `REVIEW.md`. In your own workflow, read the rules from the base
ref, for example `git show origin/<base>:REVIEW.md`, and do the same for the prompt file and the
parser, so a change to any of them needs its own merge before it applies. Ask the model for one
last line in a set shape, such as counts of findings by severity. The parser reads that line only,
fails the run when it is missing or malformed, and leaves a rerun to a person or a retry rule
you set in advance.

## Learn

- [Claude Code code review](https://code.claude.com/docs/en/code-review.md): where `REVIEW.md` is read from, and that a review advises rather than approves or blocks.
- [Claude Code code review in pull requests](https://code.claude.com/docs/en/code-review-pull-requests.md): the last-line contract for scripts that read the check run, and why a missing line means no verdict.

## Evidence for

- 2026-11-22: a vendor reviewer reads its rules from the base or default branch so that a pull request cannot rewrite the rules it is judged by ([Claude Code code review](https://code.claude.com/docs/en/code-review.md)).
- 2026-11-22: the same vendor tells script authors to take the counts from the last line only, and to treat a run without that line as no verdict ([code review in pull requests](https://code.claude.com/docs/en/code-review-pull-requests.md)).
- 2026-11-22: [a gate checks a satisfiable proxy](../docs/classes/gate-checks-a-proxy.md) records a bot approval produced through a workflow the pull request itself changed; [LLM as the measuring instrument](../docs/classes/llm-as-measuring-instrument.md) records a parser that mistook a wrapped prose line for a finding and failed a clean run.

## Evidence against

- 2026-11-22: the rules file is one part of the instrument; the model, the workflow's prompt and the parser change it too, and a review pass changed after calibration measures something else ([LLM as the measuring instrument](../docs/classes/llm-as-measuring-instrument.md)).
- 2026-11-22: a well-formed line can still be wrong: the contract checks the shape of the answer, and a no-findings line written without a review behind it passes.
- 2026-11-22: a parser reads more than the line it was written for unless it is strict about position, so prose can still trip it.
- 2026-11-22: a change to the rules waits for its own merge, which slows tuning the reviewer.

## Guards

- [llm-as-measuring-instrument](../docs/classes/llm-as-measuring-instrument.md)
- [gate-checks-a-proxy](../docs/classes/gate-checks-a-proxy.md)
