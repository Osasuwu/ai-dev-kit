---
kind: config
why: An agent given a ticket without testable acceptance criteria decides for itself what done means, and reports done against a target nobody wrote down.
applies_when: agents start work from issues or tickets, written by people or by other agents
last_reviewed: 2026-11-22
---

# Make the issue form require acceptance criteria, and turn each criterion into a test

## Check

Look at the form an agent's ticket comes from, and at the tickets themselves:

```
ls .github/ISSUE_TEMPLATE/
grep -n -B4 "required: true" .github/ISSUE_TEMPLATE/*.yml
gh issue list --label <the label your agents pick up> --json number,body --limit 20
```

The form an agent's work starts from should have an acceptance-criteria field marked required,
and blank issues should be switched off in the template `config.yml`. Each ticket's criteria
should be ones you could write a test for, and should say whether a criterion can only be seen
after deploy. Then open the pull request for one of those tickets: each criterion should map to
a test in it, or to a separate tracked item when it can only be checked in the running system.

## Fix

Add an issue form with a required acceptance-criteria field, and a note asking for criteria a
test can check. Set `blank_issues_enabled: false`. Because the form shapes only issues opened in
the web form, add a readiness check where work starts: the dispatcher, the agent's first step or
a workflow on the issue refuses a ticket with no criteria section and labels it back for a
person. In the pull request, link each criterion to the test that checks it; a criterion about
the deployed system becomes its own item with an owner.

## Learn

- [GitHub form schema syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema): the `validations: required` key on a form field, and its limits.
- [Best results with Copilot coding agent](https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results): what an issue handed to a coding agent should carry, acceptance criteria included.
- [Definition of Ready (Agile Alliance)](https://agilealliance.org/glossary/definition-of-ready): why work should not start on an item without clear completion criteria.
- [Cucumber, behaviour-driven development](https://cucumber.io/docs/bdd/): turning each example in a criterion into an automated test.

## Evidence for

- 2026-11-22: GitHub's guidance for its coding agent asks issues to carry complete acceptance criteria, such as whether unit tests are expected ([GitHub Docs](https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results)); vendor guidance.
- 2026-11-22: a Definition of Ready exists to avoid starting work without clear completion criteria, and INVEST's testable story is one you could write a test for ([Agile Alliance](https://agilealliance.org/glossary/definition-of-ready), [Wake](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/)); long-standing practice, not a measurement.
- 2026-11-22: [spec not grounded in current state](../docs/classes/spec-not-grounded-in-current-state.md) records agent tickets whose criteria were unreachable by construction, contradicted the code outside the ticket's scope, or could only be checked after deploy.

## Evidence against

- 2026-11-22: a required field on an issue form works only in public repositories ([GitHub form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)), and an issue created through the API or the CLI with a body skips the form.
- 2026-11-22: a form checks that criteria exist, not that they are true: a criterion stated plainly and wrong about the system passes it ([spec not grounded in current state](../docs/classes/spec-not-grounded-in-current-state.md)).
- 2026-11-22: an executable criterion cannot run before deploy when it is about the deployed system, and a test scoped to the ticket misses a change that reaches further.
- 2026-11-22: it costs minutes per ticket and engineering time per criterion, and a suite to keep.

## Guards

- [spec-not-grounded-in-current-state](../docs/classes/spec-not-grounded-in-current-state.md)
- [done-is-not-the-effect](../docs/classes/done-is-not-the-effect.md)
