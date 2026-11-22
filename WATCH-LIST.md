# Watch list

Generated from the `Learn` sections in `cards/` by `python scripts/generate_card_index.py`; do not edit. The talks and pages each card learns from, with what to look for in each.

## [Let the agent run the tests but not change them, and flag every change to them](cards/agent-cannot-edit-the-tests.md)

- [ImpossibleBench](https://arxiv.org/html/2510.20270): how often agents modify tests on tasks they cannot solve honestly, and how read-only tests change that.
- [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide.md): a hook that blocks edits to protected files by path.
- [EvilGenie](https://arxiv.org/html/2511.21654): flagging any edit or deletion of test files as reward hacking, and the forms of gaming that touch no test.

## [Allow known commands, parse before matching, and test every rule](cards/allow-known-commands.md)

- [Claude Code permissions](https://code.claude.com/docs/en/permissions.md): how compound commands are split, which forms a rule misses, and why a rule is not a boundary around a program.
- [Codex rules](https://developers.openai.com/codex/rules): rules on the argument list, and `match` and `not_match` examples checked when the rules load.
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html): why allow lists beat lists of bad strings, and why to parse with a maintained parser.

## [Count only an approval from someone other than the pusher, for the latest push](cards/approvals-from-another-identity.md)

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): dismissing stale approvals, approval of the most recent push, and the admin exemption.
- [Approving a pull request with required reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews): authors cannot approve their own pull requests.
- [Prevent GitHub Actions from approving pull requests (GitHub changelog, 2022-01)](https://github.blog/changelog/2022-01-14-github-actions-prevent-github-actions-from-approving-pull-requests): the setting that stops a workflow token meeting the approval requirement.
- [Copilot cloud agent risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations): how the platform stops the person who asked the agent for a pull request from approving it.

## [Cap each agent run, and record its turns, cost, duration and stop reason](cards/cap-and-record-each-run.md)

- [Your Agent Didn’t Fail. Your Harness Did., 10:45](https://www.youtube.com/watch?v=BInpv7lGp1o&t=645): every external boundary needs an end (success, failure, timeout, cancel, max attempts), and a record of which one happened.
- [Agents in Orbit: Workflows, Not Autopilot (Flywire), 8:05](https://www.youtube.com/watch?v=rAUyRDOFyHU&t=485): per-agent timeouts, rate limits and duplicate locks on thousands of review runs.
- [An AI Agent Got Its User Banned From Resy (Keycard, JPMorgan Chase & AAuth), 24:52](https://www.youtube.com/watch?v=IavxrdVnwXM&t=1492): why a budget the agent can see beats a rate limit that cuts it off without saying why.
- [Agent SDK agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop): the result subtypes for a turn cap and a budget cap, and when the budget is checked.

## [Run the checks where the change will run, from one environment definition](cards/ci-runs-where-the-change-runs.md)

- [Running variations of jobs in a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations): a matrix over operating systems and versions, and what `fail-fast` cancels.
- [Using self-hosted runners in a workflow](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow): sending a job to a runner with the device or hardware it needs.
- [Development containers](https://containers.dev/): one environment definition used by editors, agents and CI, and [devcontainers/ci](https://github.com/devcontainers/ci) to run CI inside it.
- [Testcontainers](https://testcontainers.com/): tests against the real engine in a container instead of a mock or the host's setup.

## [Ask or deny at the tool call for the irreversible kinds only](cards/deny-irreversible-at-the-tool-call.md)

- [Give the Agent a Budget, Not a Token (Anthropic), 4:41](https://www.youtube.com/watch?v=rbjWzZK2LU0&t=281): the undo test, whether the agent could roll the action back and whether the blast radius is acceptable, as the way to decide which actions need a second key.
- [Give Your On-Call Its Own AI Teammate (Meta), 4:21](https://www.youtube.com/watch?v=_NBx2NNOuA4&t=261): autonomy granted per action, from shadow to approval to autonomous, by how cheap a mistake is.
- [What a $900M Bank Error Teaches Us About AI Agents (Two Sigma), 3:44](https://www.youtube.com/watch?v=iniryju23Sk&t=224): three people approved a costly mistake; why an approval holds only when the approver can check the work.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks): `PreToolUse`, exit code 2, and what happens when a hook fails.

## [Make every check fail when it had nothing to check or its tool is missing](cards/fail-when-nothing-was-checked.md)

- [pytest exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html): exit code 5, no tests collected, and why it is a failure by default.
- [Jest CLI](https://jestjs.io/docs/cli): `--passWithNoTests`, the flag that turns an empty run into a pass.
- [Mocha CLI](https://mochajs.org/running/cli/): `--fail-zero`, off by default.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks.md): which exit codes block a tool call, and that a hook which fails any other way lets the action go ahead.

## [Generate the copies from one source, and fail CI when a copy is stale](cards/generate-copies-from-one-source.md)

- [cog: running and checking](https://cog.readthedocs.io/en/latest/running.html): `--check`, which fails when the generated blocks would change if run again.
- [cruft](https://cruft.github.io/cruft/): `cruft check` in CI, to catch a project drifting from the template it was made from.
- [repo-file-sync-action](https://github.com/BetaHuhn/repo-file-sync-action): pull requests that bring copied files in other repositories back in line.
- [Kubernetes verify-codegen.sh](https://github.com/kubernetes/kubernetes/blob/master/hack/verify-codegen.sh): a large project's check that committed generated code is current.

## [Give every scheduled job an external heartbeat, and watch the alerting itself](cards/heartbeat-for-scheduled-jobs.md)

- [Healthchecks.io, monitoring cron jobs](https://healthchecks.io/docs/monitoring_cron_jobs/): how a missing ping turns into an alert, and how to set the period and grace time.
- [Sentry Crons, job monitoring](https://docs.sentry.io/product/crons/job-monitoring/): the same check inside an error tracker, with missed and failed check-ins.
- [Prometheus Operator, Watchdog runbook](https://runbooks.prometheus-operator.dev/runbooks/general/watchdog/): an always-firing alert that an outside receiver expects, so a dead alerting pipeline is noticed.
- [GitHub, events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): when scheduled workflows are disabled for inactivity.

## [Make the issue form require acceptance criteria, and turn each criterion into a test](cards/issue-form-requires-criteria.md)

- [GitHub form schema syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema): the `validations: required` key on a form field, and its limits.
- [Best results with Copilot coding agent](https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results): what an issue handed to a coding agent should carry, acceptance criteria included.
- [Definition of Ready (Agile Alliance)](https://agilealliance.org/glossary/definition-of-ready): why work should not start on an item without clear completion criteria.
- [Cucumber, behaviour-driven development](https://cucumber.io/docs/bdd/): turning each example in a criterion into an automated test.

## [Give the agent the least-privileged token, the fewest tools, and only trusted people to start it](cards/least-privilege-agent-token.md)

- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): minimum permissions for the workflow token, and how to set them per job.
- [claude-code-action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md): who can trigger the action, the risk of letting other users in, and why not to use a personal token.
- [How Many Credentials Should Your AI Agent Have? Zero. (Docker), 10:21](https://www.youtube.com/watch?v=ZUZVNKFSmTM&t=621): capabilities handed to the agent for one task through a gateway that holds the credentials.
- [Real AI Agent Attacks and What Would Have Stopped Them (Bloomberg), 14:06](https://www.youtube.com/watch?v=5O6jLtoeKrg&t=846): a short priority list drawn from incidents: a broker on tool calls, one identity, short-lived tokens.

## [Keep the guard's own configuration out of reach of the agent and the project](cards/lock-the-guard-configuration.md)

- [Claude Code sandboxing, protected paths](https://code.claude.com/docs/en/sandboxing.md#protected-paths): which files are protected and why a command that could edit them could grant itself permissions.
- [Claude Code permissions, managed settings](https://code.claude.com/docs/en/permissions.md#managed-settings): rules no other level can override, and when a project's allow rules apply.
- [Gemini CLI trusted folders](https://geminicli.com/docs/cli/trusted-folders/): what an untrusted folder's settings and `.env` files may not do.
- [Check Point on project-file RCE](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/): how repository settings read before trust became code execution.

## [Require each new test to fail on the parent commit, and mutate the code the diff touched](cards/new-test-fails-on-the-parent.md)

- [SWE-bench dataset card](https://huggingface.co/datasets/princeton-nlp/SWE-bench/blob/main/README.md): the `FAIL_TO_PASS` field, tests that fail before the fix and pass after it.
- [cargo-mutants, `--in-diff`](https://mutants.rs/in-diff.html): mutating only the code a diff touched.
- [Stryker configuration](https://stryker-mutator.io/docs/stryker-js/configuration/): the `break` threshold, which by default never fails the build.
- [State of mutation testing at Google](https://research.google/pubs/state-of-mutation-testing-at-google/): how mutation testing scoped to a change runs at the scale of a large company.

## [Give the agent scoped, per-environment credentials, and none for production](cards/no-production-credentials-for-agents.md)

- [Decoupling the Brain from the Hands: Claude Managed Agents (Part 1 of 4) (Anthropic), 8:52](https://www.youtube.com/watch?v=Uv0nAf_7tyU&t=532): why credentials were moved out of the sandbox into a proxy that adds them to outgoing calls.
- [How Many Credentials Should Your AI Agent Have? Zero. (Docker), 8:21](https://www.youtube.com/watch?v=ZUZVNKFSmTM&t=501): granting a capability only for the minutes of the task that need it.
- [Who Is Making This Request? Agent Auth 101 (Keycard), 12:24](https://www.youtube.com/watch?v=58ulJViGFgU&t=744): the rule that a token in the agent's execution environment is a token the agent can reach.
- [GitHub fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens): repository scope and expiry, and what these tokens cannot cover.

## [Pin the formatter to an exact version and check formatting in CI](cards/pin-the-formatter.md)

- [Prettier, install](https://prettier.io/docs/install): why even a patch release can change output, and the advice to pin an exact version and check it in CI.
- [Google engineering practices, what to look for in a review](https://google.github.io/eng-practices/review/reviewer/looking-for.html): why style changes go in their own change, not mixed with others.

## [Protect shared branches and release tags against force-push and deletion](cards/protect-branches-and-tags.md)

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): the force-push and deletion settings, and who is exempt by default.
- [About rulesets](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets): rules for branches and tags, bypass lists, and how rulesets combine with protection rules.

## [Require every check you merge on, and pin it to the app that reports it](cards/require-and-pin-checks.md)

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): what a required check blocks, and which statuses count as passing.
- [Troubleshooting required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks): why a required job that is skipped, or whose dependency failed, can still let the merge through.
- [Required checks from the intended app (GitHub changelog, 2021-11-30)](https://github.blog/changelog/2021-11-30-ensure-required-status-checks-provided-by-the-intended-app/): how pinning a check to an app works, and that older required checks stay unpinned until edited.

## [Read the review rules from the base branch, and gate on a fixed verdict line](cards/review-rules-from-the-base-branch.md)

- [Claude Code code review](https://code.claude.com/docs/en/code-review.md): where `REVIEW.md` is read from, and that a review advises rather than approves or blocks.
- [Claude Code code review in pull requests](https://code.claude.com/docs/en/code-review-pull-requests.md): the last-line contract for scripts that read the check run, and why a missing line means no verdict.

## [Run the agent's shell inside a filesystem and network allowlist](cards/sandbox-the-agent-shell.md)

- [Rethinking Claude Code Best Practices (Anthropic), 7:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=440): what should move out of the prompt into permissions and an OS-level sandbox.
- [Security Firewall for Agents, 2:32](https://www.youtube.com/watch?v=MkRYPFIMCSA&t=152): why a control at the tool level is bypassed once the agent runs a client program as a subprocess, and why the check has to sit outside the agent.
- [Real AI Agent Attacks and What Would Have Stopped Them (Bloomberg), 9:20](https://www.youtube.com/watch?v=5O6jLtoeKrg&t=560): incidents matched to controls, including data sent out over DNS while web access was closed.
- [Claude Code sandboxing](https://code.claude.com/docs/en/sandboxing): the settings, what the sandbox covers, and the escape hatch.

## [Serialize the CI runs that share state, and merge through a queue](cards/serialize-ci-runs-and-merges.md)

- [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency): what a group guarantees, what happens to the pending run, and that ordering is not guaranteed.
- [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue): how each entry is tested against the ones ahead of it, and why workflows must run on `merge_group`.

## [Run shell steps fail-fast, and make an empty expansion stop the script](cards/shell-steps-fail-fast.md)

- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): the exact command line each `shell:` value runs, and which ones include `pipefail`.
- [ShellCheck SC2115](https://www.shellcheck.net/wiki/SC2115): the `${VAR:?}` fix for a delete whose path starts with a variable.
- [ShellCheck SC2164](https://www.shellcheck.net/wiki/SC2164): why a failed `cd` lets the rest of the script run in the wrong directory.
- [BashFAQ/105](https://mywiki.wooledge.org/BashFAQ/105): the places where `set -e` does not stop the script.

## [Keep the always-loaded rules file short, scope the rest to its files, and make a cut visible](cards/short-scoped-rules-files.md)

- [Claude Code memory](https://code.claude.com/docs/en/memory): the size guidance, path-scoped rules, imports, the memory index cap, and the `InstructionsLoaded` hook.
- [AGENTS.md](https://agents.md/): nested files and the nearest-first rule.
- [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md): the combined size cap and splitting large files across directories.
- [Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions): path-specific instruction files with `applyTo`.

## [Have a Stop hook run the check before the agent may stop](cards/stop-hook-runs-the-check.md)

- [Claude Code best practices](https://code.claude.com/docs/en/best-practices): giving the agent something that comes back pass or fail, and the Stop hook that sends it back to work on exit code 2.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks): Stop hook input and exit codes, which failures do not block, and the cap on consecutive blocks.
- [LangChain on harness engineering for deep agents](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering): a harness change that included a check against the task before the agent exits.

## [Make expected failures strict, count the skips, and lint for tests that assert nothing](cards/strict-expected-failures-and-counted-skips.md)

- [pytest, how to use skip and xfail](https://docs.pytest.org/en/stable/how-to/skipping.html): the `strict` option, and why a non-strict expected failure that passes stays green.
- [eslint-plugin-jest `expect-expect`](https://github.com/jest-community/eslint-plugin-jest/blob/main/docs/rules/expect-expect.md): a test with no assertion, and how to tell the rule about helper functions that assert.
- [Ruff PT017](https://docs.astral.sh/ruff/rules/pytest-assert-in-except/): an assertion inside `except` that runs only when the code fails.
- [Test smells catalogue](https://testsmells.org/pages/testsmells.html): the wider list of tests that cannot fail, behind tsDetect for Java.

## [Publish with short-lived, workflow-bound credentials, and keep them out of every other job](cards/trusted-publishing.md)

- [npm trusted publishers](https://docs.npmjs.com/trusted-publishers): how a workflow publishes without a stored token, the setting that disallows tokens, and the runner limits.
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): OpenID Connect instead of long-lived secrets, and the triggers to keep away from untrusted code.
- [Nx s1ngularity postmortem](https://nx.dev/blog/s1ngularity-postmortem): how a publish token leaked through a workflow, and the move to trusted publishing afterwards.

## [Keep untrusted triggers away from secrets and release workflows, and scan for them](cards/untrusted-triggers-get-no-secrets.md)

- [GitHub Security Lab, preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/): why `pull_request_target` plus a checkout of the pull request is dangerous, and why a label gate races.
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): which triggers to avoid with untrusted code, and the environment-variable pattern for untrusted input.
- [Cache poisoning in GitHub Actions](https://adnanthekhan.com/2024/05/06/the-monsters-in-your-build-cache-github-actions-cache-poisoning/): how a cache written by one workflow reaches a release in another.
- [zizmor audits](https://docs.zizmor.sh/audits/): the dangerous-triggers, template-injection and cache-poisoning rules.

## [Vet a package before the agent installs it, and refuse versions that are too new](cards/vet-packages-before-install.md)

- [Agentic Security: Permissions, Provenance, and the Agent Supply Chain, 2:10](https://www.youtube.com/watch?v=yWS0udrIOc8&t=130): why a squatted package that does what was expected passes the build and the tests unnoticed.
- [AI Security Engineer Foundations + Certificate (Snyk), 1:43:08](https://www.youtube.com/watch?v=ZyC56eV8sVw&t=6188): how a hallucinated name gets registered, and a real case that was downloaded about two hundred times before removal.
- [Real AI Agent Attacks and What Would Have Stopped Them (Bloomberg), 11:50](https://www.youtube.com/watch?v=5O6jLtoeKrg&t=710): a malicious package that shipped many clean releases before one bad one, and why delaying intake works against it.
- [Exploits Now Beat Patches: Open Source Security in the AI Era (Chainguard), 12:43](https://www.youtube.com/watch?v=xZX3pmaB8Hk&t=763): CI, developer machines and agent tooling as the soft targets, and package cooldowns among the defences.
- [pnpm dependency resolution settings](https://pnpm.io/settings/dependency-resolution): `minimumReleaseAge`, its default and when it is strict.

## [Have the agent interview you before it writes code](cards/agent-interviews-you-first.md)

- [Your spec has bugs. Catch them before your agent codes. (AWS), 4:17](https://www.youtube.com/watch?v=0EnLxIbAvYk&t=257): a mechanical hunt for ambiguous and contradictory requirements, run before the agent writes code.
- [How forward deployed engineering is done at Ramp, 7:33](https://www.youtube.com/watch?v=ITMXwI6QL6A&t=453): an agent that asks scoping questions about each incoming request before any work starts.
- [One developer, two dozen agents, zero alignment: why we need collaborative AI engineering, 3:28](https://www.youtube.com/watch?v=ClWD8OEYgp8&t=208): why agreement on what to build slid from before the code to the pull request.
- [Spec Kit clarify step](https://github.com/github/spec-kit/blob/main/templates/commands/clarify.md): a ready-made prompt that asks the author about gaps before planning, with a cap on the number of questions.

## [Have the agent use the running app before it calls the work done](cards/agent-uses-the-running-app.md)

- [Your agent is blindfolded, 2:12](https://www.youtube.com/watch?v=iRcX54EO5g8&t=132): why an agent that cannot see the running app cannot tell a working feature from a broken one.
- [Teach your agent to prove it's done (WorkOS), 20:51](https://www.youtube.com/watch?v=q4WC4TowkBo&t=1251): proof of done in two layers, a deterministic check and a model judge on top.
- [Teach your agent to prove it's done (WorkOS), 46:10](https://www.youtube.com/watch?v=q4WC4TowkBo&t=2770): why a proof goes stale once later changes land, and has to be redone.
- [How to build an AI code review agent (Greptile), 13:34](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=814): what an agent needs to test a change by using it: a sandbox, written scenarios, a one-command start.

## [Write the agreed intent as criteria, and check the pull request against each one](cards/criteria-checked-against-the-pr.md)

- [How to kill the code review, 7:02](https://www.youtube.com/watch?v=YgEv7IQzGdM&t=422): a loop that turns the decisions made in an agent session into acceptance criteria and a test plan run against a preview.
- [BDD, ADR, PRD, WTF: capturing decisions for humans and AI alike (Safe Intelligence), 4:21](https://www.youtube.com/watch?v=504PvfXou5Y&t=261): executable scenarios that a person can read and a machine can run, as the link between the requirement and the check.
- [Why a one-line change can break your whole stack (Qodo), 11:04](https://www.youtube.com/watch?v=YqxpPI7YUjE&t=664): a demo of comparing a change with its ticket's criteria before the pull request opens. A vendor demo; watch this part only.

## [Give the agent the documentation for the versions you use](cards/give-the-agent-current-docs.md)

- [Context7](https://github.com/upstash/context7): a server that fetches version-specific documentation and examples for the agent on request, and its own note that it cannot vouch for the accuracy of every library's docs.
- [Skill issue: lessons from skilling up coding agents to use Langfuse, 9:15](https://www.youtube.com/watch?v=vNCY9kXXyDQ&t=555): finding the CLI options agents invent for your tool by reading traces of their real sessions.
- [Your SKILL.md is 70% stuff the model already knows (Intel), 6:54](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=414): a measurement of what a model already knows about a document, which separates general ideas from exact details.
- [How I deleted 95% of my agent skills and got better results (WorkOS), 8:26](https://www.youtube.com/watch?v=vy7o1g2iHY8&t=506): a case where thousands of lines of skills generated from documentation made the agent worse.

## [Give the agent the history of the code it changes: decisions, reverts and incidents](cards/give-the-agent-the-team-history.md)

- [What your coding agent can't see in the code (Linear), 7:02](https://www.youtube.com/watch?v=Xw9utONfhIY&t=422): a review agent that starts from the issue and its intent, then searches the same area's past decisions, reverts, regressions and incidents.
- [What your coding agent can't see in the code (Linear), 14:15](https://www.youtube.com/watch?v=Xw9utONfhIY&t=855): what else such a reviewer pulls in: overlapping changes, the authoring agent's session and the owner of the product trade-off.
- [Mergeable by default: building the context engine to save time and tokens, 9:36](https://www.youtube.com/watch?v=5ID22ACI7IM&t=576): satisfaction of search, where an agent stops at the first plausible explanation while the right one sits in an old incident or discussion, and a demo of one task with and without that context; a vendor talk, the first quarter hour is enough.
- [How to build an AI code review agent (Greptile), 13:34](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=814): how knowledge about the codebase narrows which files a review agent has to read.

## [Give a long agent task a checkable goal, a budget and checkpoints against the goal](cards/goals-with-done-criteria-and-budget.md)

- [Cooking with Codex (OpenAI), 31:57](https://www.youtube.com/watch?v=FwiS44-xyYw&t=1917): a multi-hour task driven by a goals file and a progress page, with separate threads at milestones that review the code and audit whether the main thread has drifted from its goals.
- [Harness engineering: how to build software when humans steer, agents execute (OpenAI), 43:21](https://www.youtube.com/watch?v=am_oeAoUhew&t=2601): steering agents by a budget, priorities and success measures instead of step-by-step instructions, and what had to be built for that.
- [Lifestyles of the AI-native (WorkOS), 56:59](https://www.youtube.com/watch?v=AgBAOXVxt4A&t=3419): the difference between a goal that stops when done and a loop that repeats on a schedule, and when the agent should call a person.

## [Mine the agent's sessions for lessons, write them back, and measure whether each helped](cards/mine-sessions-for-lessons.md)

- [Giving AI agents memory that learns (LangChain), 7:45](https://www.youtube.com/watch?v=KGFyOtl5ktI&t=465): why a trace becomes memory only after a filter picks the signal and writes it back.
- [Your AI agent is hiding its mistakes from you (Warp), 1:42](https://www.youtube.com/watch?v=pz74r-4dGfQ&t=102): a nightly pass that grades conversations against a rubric, proposes skill edits, and matches score changes to the dates the edits merged.
- [How Lovable self-improves every hour, 5:17](https://www.youtube.com/watch?v=KA5kPbdkK2E&t=317): implicit signals that a session got stuck, and ranking fixes by project success instead of complaint count.
- [Claude for long-horizon tasks, 10:27](https://www.youtube.com/watch?v=9QebvrrY3KY&t=627): an offline pass over transcripts that corrects what the agent wrote into memory during the work.

## [Give each agent its own workspace](cards/one-workspace-per-agent.md)

- [Your team's agents are all shipping to the same code at once (Tessl), 5:20](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=320): the ways to isolate agents (worktree, own machine, mocked APIs, database snapshots) and to settle the collisions that remain. Product-leaning.
- [Claude Code worktrees](https://code.claude.com/docs/en/worktrees): a separate copy of the files per session, and what the isolation does not track.
- [Codex worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees): why one branch can be checked out in only one place at a time.
- [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams): splitting work so that each agent owns a different set of files.

## [Let production signals start an agent that reproduces the failure and opens a fix for a person to approve](cards/production-signals-open-fix-prs.md)

- [Self driving products: product signals to pull requests, 3:26](https://www.youtube.com/watch?v=zMiSRliEzv4&t=206): a full pipeline from errors, replays, logs and support messages through filtering, grouping and research to a pull request built in a sandbox.
- [Self driving products: product signals to pull requests, 5:04](https://www.youtube.com/watch?v=zMiSRliEzv4&t=304): the engineering failures on the way: public signals as an injection route, and grouping that clustered by format instead of by problem.
- [The missing layer after launch, 6:43](https://www.youtube.com/watch?v=kZsf_Sfm7RU&t=403): a separate review agent with a fresh context that judges the fix agent's pull requests before a person sees them.
- [The self-improving OSS agent stack (Langfuse), 12:11](https://www.youtube.com/watch?v=TeErpYBUIeM&t=731): reproducing the problem on the current version and backtesting the new one on an updated dataset before the agent opens a pull request.

## [Turn each repeated review comment into a rule a tool enforces](cards/review-comments-become-rules.md)

- [Stop prompting (Sentry), 4:26](https://www.youtube.com/watch?v=E3KbFLAGD6A&t=266): why agents made custom lint rules cheap enough to write for one repeated comment, and where the candidates come from.
- [Stop prompting (Sentry), 12:03](https://www.youtube.com/watch?v=E3KbFLAGD6A&t=723): the line between a rule and a policy left to a model reviewer, with one reviewer subagent per policy.
- [Harness engineering: how to build software when humans steer, agents execute (OpenAI), 36:13](https://www.youtube.com/watch?v=am_oeAoUhew&t=2173): a weekly cleanup that removes noticed slop as a category and feeds it back into docs, a failing test or a reviewer agent.
- [How to kill the code review, 7:02](https://www.youtube.com/watch?v=YgEv7IQzGdM&t=422): the principle in short form, and a register of repeated review findings.
- [Building uReview, Uber's multi-agent code review engine (Uber), 3:37](https://www.youtube.com/watch?v=EL123UNokkI&t=217): team standards run as reviewer policies at scale, with each policy judged by whether developers act on its comments.

## [Review the agent's work in a fresh context, against criteria written before the code](cards/review-in-a-fresh-context.md)

- [The multi-agent architecture that actually ships (Factory), 4:27](https://www.youtube.com/watch?v=ow1we5PzK-o&t=267): a validation contract written before the code, and validators that never saw the implementation.
- [Claude for long-horizon tasks, 5:08](https://www.youtube.com/watch?v=9QebvrrY3KY&t=308): a build-then-verify loop with the grader kept apart from the generator, and why grading in the same context drifts.
- [How to build an AI code review agent (Greptile), 7:34](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=454): a set of pull requests that caused incidents, used to measure what a reviewer from another model family catches.
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices): the built-in review that runs in a subagent which never saw the conversation.

## [Keep progress in a file, and start the next session fresh from it](cards/save-progress-and-restart-fresh.md)

- [How to build agents that run for hours (without losing the plot), 12:58](https://www.youtube.com/watch?v=mR-WAvEPRwE&t=778): a progress file, an init script and a feature list, with each iteration in a fresh window.
- [Context engineering in 2026: compaction, memory & cost, 40:57](https://www.youtube.com/watch?v=WP3hjUXd918&t=2457): a comparison against keeping the full history, and why dropped tool output gets fetched again.
- [How we solved context management in agents, 5:45](https://www.youtube.com/watch?v=esY99nYXxR4&t=345): why free-form summarisation was dropped and what replaced it.

## [Schedule agents only for narrow chores with an outside check, and let code do the writes](cards/schedule-agents-for-bounded-chores.md)

- [We gave an agent production code access and then tried to sleep at night, 3:41](https://www.youtube.com/watch?v=LqLoYksJ6do&t=221): a CVE-fixing setup where a deterministic orchestrator does the work around the agent and the agent only reasons.
- [We gave an agent production code access and then tried to sleep at night, 5:21](https://www.youtube.com/watch?v=LqLoYksJ6do&t=321): why the agent cannot commit, push or open a pull request, and how the controller checks and writes its edits.
- [Realtime multiplayer, automation, and you!, 11:12](https://www.youtube.com/watch?v=iQ5xldZ9StU&t=672): guardrails for scheduled agent workflows: no secrets for the agent, a checking stage before every write, a log of everything.
- [Agents, codebases, and teams: what it actually takes to ship together, 9:14](https://www.youtube.com/watch?v=aeTb5BdmTTc&t=554): a nightly code-tidying agent and a long-running shipping workflow inside a team's routine.

## [Keep agent changes small and owned, with the why written by a person](cards/small-legible-changes.md)

- [The state of AI in software development: data from 400+ orgs (DX), 4:42](https://www.youtube.com/watch?v=Se8jHLliLXE&t=282): how pull request size and engineers' confidence in their changes moved over a year.
- [The state of AI in software development: data from 400+ orgs (DX), 6:12](https://www.youtube.com/watch?v=Se8jHLliLXE&t=372): the widening spread of change failure rate between companies.
- [Generation is cheap, review is expensive: how to stop shipping AI slop (G2i), 11:02](https://www.youtube.com/watch?v=6qkzlT962es&t=662): why conventions, small review surfaces and clear ownership lower the cost of understanding a change.
- [How to get your org to adopt coding agents (without shipping garbage) (Figma), 12:30](https://www.youtube.com/watch?v=5Bn0xro2ol8&t=750): opening each pull request description with lines the author wrote, and reading the generated part with suspicion.
- [Small CLs (Google engineering practices)](https://google.github.io/eng-practices/review/developer/small-cls.html): why small changes review better, and keeping refactors apart from feature changes.

## [Send noisy work to a subagent that returns a short summary](cards/subagents-for-noisy-work.md)

- [If we want them to do knowledge work, design them as knowledge agents (Mixedbread), 12:09](https://www.youtube.com/watch?v=O84lhGc1OOI&t=729): searcher subagents that return short memos to a lead agent, measured on a public benchmark.
- [How we solved context management in agents, 10:00](https://www.youtube.com/watch?v=esY99nYXxR4&t=600): the path from truncation to summarisation to an external store plus subagents, and why each earlier step failed.
- [Building agent interfaces: lessons from Chrome DevTools (MCP) for agents, 3:44](https://www.youtube.com/watch?v=_B4Pv9ttFgY&t=224): a tool that handed the agent a raw trace of several megabytes, and the digest that replaced it.
- [Your sub-agents are a distributed system. Treat them like one. (Microsoft), 4:25](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=265): why a subagent's confident verdict looks the same whether it investigated or made the answer up.

## [Test each skill with and without it, and prune what the model no longer needs](cards/test-and-prune-skills.md)

- [How I deleted 95% of my agent skills and got better results (WorkOS), 8:26](https://www.youtube.com/watch?v=vy7o1g2iHY8&t=506): a measured case where a skill lowered accuracy, and the short list of gotchas that replaced it.
- [Don't ship skills without evals, 11:51](https://www.youtube.com/watch?v=0vphxNt4wyk&t=711): ablation with and without a skill over repeated runs, trigger tests, and when to retire a skill.
- [Your SKILL.md is 70% stuff the model already knows (Intel), 6:54](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=414): quizzing the model on each claim in a skill, without the skill, to find what it already knows.
- [Your old prompts are making Claude worse (Anthropic), 1:58](https://www.youtube.com/watch?v=ys6YQ2yfBpM&t=118): the measured cost of stale and contradictory instructions on a newer model, and an audit procedure.

## [Review skills and plugins like code before they load, and again after they change](cards/vet-skills-and-plugins.md)

- [We vetted 2,000 AI skills before they reached developers, 7:20](https://www.youtube.com/watch?v=iKQ78wyJEXU&t=440): a vetting pipeline from local scan to pull request, a deterministic scanner, model review for context, and a policy decision.
- [We vetted 2,000 AI skills before they reached developers, 9:40](https://www.youtube.com/watch?v=iKQ78wyJEXU&t=580): why the deterministic scan comes first, and why skills are scanned again after upload.
- [Skills are new features: building skill-centric harness (FactSet), 14:01](https://www.youtube.com/watch?v=7jjudsEhBtM&t=841): running skills like features: admission gates, owners, versions, deprecation, audits, a tool allowlist per skill.
- [Through the AI fog: the architectural decision the next 24 months of agentic security depends on, 18:55](https://www.youtube.com/watch?v=1EZdpEhwmNc&t=1135): a shared skill that echoes an authorization header and loads its rules from a file on the internet.

## [Widen the agent's autonomy in stages, on its measured record per kind of action](cards/widen-autonomy-on-track-record.md)

- [The agent works. Does anyone trust it? (Leading at Scale), 10:13](https://www.youtube.com/watch?v=-a2oTS9J67U&t=613): four stages from shadow to exceptions only, and why a falling override rate can mean the review got shallower.
- [60% of our data PRs now merge with no human review (Robinhood), 3:58](https://www.youtube.com/watch?v=MQiojLnK-E0&t=238): scripts check the facts, an agent judges the remaining risk, and people keep the protected decisions.
- [Deploying AI inside a bank is not an engineering problem (Applied AI Engineers), 8:07](https://www.youtube.com/watch?v=3ZlQk4-knWM&t=487): starting from the least authority that is still useful, and promotion on observed errors.
- [Give your on-call its own AI teammate (Meta), 4:21](https://www.youtube.com/watch?v=_NBx2NNOuA4&t=261): an autonomy ladder per action rather than per agent.

## [An agent's done report is a claim, not evidence](cards/a-done-report-is-a-claim.md)

- [Your Agent Hates Your CLI (Allos AI), 1:48](https://www.youtube.com/watch?v=rS36lYuvXQ8&t=108): how piping a command into `tail` or `head` hides its failing exit code and its error, and the agent then reports success.
- [What Does Done Even Mean? Agents and Paperclip's Liveness Model (Paperclip), 0:00](https://www.youtube.com/watch?v=7P0elyLIxXo&t=0): done split into separate claims, merged, deployed, announced, each with its own evidence and owner.
- [Your PR Says the Tests Passed. Prove It., 15:21](https://www.youtube.com/watch?v=gbeuC0ud1p4&t=921): why a test command in the session log does not show which code the tests ran against.

## [At agent pace, pull requests that pass alone break the main branch together](cards/agent-pr-volume-breaks-serial-merging.md)

- [AI writes code faster than Uber can merge it (Uber), 2:11](https://www.youtube.com/watch?v=hX140a5klW0&t=131): how two green changes break trunk once merged, and why the rate grows with agents.
- [AI writes code faster than Uber can merge it (Uber), 5:54](https://www.youtube.com/watch?v=hX140a5klW0&t=354): a merge queue that tests the possible future states of main, and what keeping trunk green cost in waiting time.
- [Your team's agents are all shipping to the same code at once (Tessl), 5:20](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=320): ways to isolate parallel agents and to settle their collisions; a vendor's framing.
- [Rebuilding CI for AI-scale commit volume (Sonar), 10:10](https://www.youtube.com/watch?v=7b9tov5Uc5s&t=610): where faster CI comes from under agent volume; a vendor's talk.

## [Agent-written tests are weak, and a numeric target makes them weaker](cards/agent-written-tests-are-weak.md)

- [225,000 lines of tests, written and merged by agents (Duolingo), 1:15](https://www.youtube.com/watch?v=D_4Rn6uLdQM&t=75): the coverage rise an agent test programme produced, and what it cost along the way.
- [225,000 lines of tests, written and merged by agents (Duolingo), 9:39](https://www.youtube.com/watch?v=D_4Rn6uLdQM&t=579): the three layers that kept agents from passing by editing product code or silencing tests.
- [Stop prompting (Sentry), 13:56](https://www.youtube.com/watch?v=E3KbFLAGD6A&t=836): a coverage target met with tests that compare strings, and the policies that replaced the number.
- [Building ambitious software (Dioxus Labs, Cognition), 14:18](https://www.youtube.com/watch?v=H7vFrcNWXzs&t=858): where agent tests are weak and where agents do well.

## [An agent that can reach its check will get around it](cards/agents-game-their-checks.md)

- [Why frontier models fail as buy-side analysts (Google DeepMind, LinqAlpha), 5:54](https://www.youtube.com/watch?v=aVbRSIQO2dE&t=354): cheats found while reproducing industry benchmarks, from a grader rewritten in place to another model's keys taken from the container.
- [SWE-Marathon: evaluating coding agents at billion-token scale (Abundant AI), 9:16](https://www.youtube.com/watch?v=Rx8f05JI_WA&t=556): how often long coding runs bypassed the verifier, and the layer that caught them.
- [SWE-rebench: lessons from evaluating coding agents on real software engineering tasks (Nebius), 11:01](https://www.youtube.com/watch?v=wcUJWP6WpGM&t=661): an agent that went around each blocked route with the next tool, and why that argues for closing egress as a whole.

## [An agent should act under an identity of its own, not its user's](cards/agents-need-their-own-identity.md)

- [You didn't ship a bug. You just wrote it for a human, 9:10](https://www.youtube.com/watch?v=lMCxVorb9wM&t=550): why the trust model built for deterministic programs breaks for agents.
- [How to let AI agents sign up for your app safely (WorkOS), 12:38](https://www.youtube.com/watch?v=uTrY8slys0w&t=758): an agent token limited to the overlap of the user's rights and a ceiling set for the agent; a vendor's demo.
- [Tethered: our agents are us (Two Sigma), 7:16](https://www.youtube.com/watch?v=wCIYViPd4SU&t=436): the opposite choice, agents running as the employee, why separate agent accounts were dropped and what covers the risk instead.

## [The cost of agent work is the cost of an accepted change, people included](cards/cost-per-accepted-change.md)

- [Tokens are the cheap part (Jellyfish), 4:02](https://www.youtube.com/watch?v=U7ZYBCcdJPg&t=242): cost per merged pull request across many companies, salaries included.
- [Tokens are the cheap part (Jellyfish), 16:29](https://www.youtube.com/watch?v=U7ZYBCcdJPg&t=989): the limits of the figure, which is observational, not causal.
- [Tokens should have jobs (Anthropic), 7:37](https://www.youtube.com/watch?v=PXj0p_mW9nI&t=457): computing the cost of a fully correct answer when only those count, across strategies.
- [What technical due diligence finds when the deck says "70% automated", 3:49](https://www.youtube.com/watch?v=gDRCpTMCqEU&t=229): a full formula for the cost of an accepted autonomous task, with failure, escalation and rework priced in.

## [Reviewing the diff misses what breaks downstream](cards/diff-review-misses-downstream-effects.md)

- [How to Build an AI Code Review Agent (Greptile), 3:11](https://www.youtube.com/watch?v=4UtrRVtUN_g&t=191): why a naive reviewer, a model given the diff by a webhook, misses bugs and does not understand how the codebase fits together.
- [60% of Our Data PRs Now Merge With No Human Review (Robinhood), 8:08](https://www.youtube.com/watch?v=MQiojLnK-E0&t=488): deterministic checks that walk the data lineage and ask each registered consumer of a changed column whether it breaks.
- [We Mapped 115 Microservices for Our Coding Agents (Postman), 12:53](https://www.youtube.com/watch?v=k2ClBT4aqAg&t=773): a dependency graph given to the agent, and what happened when the graph fell behind the code.

## [Faster generation moves the bottleneck to review and delivery](cards/generation-moves-the-bottleneck-to-review.md)

- [AI Writes the Code. So What's Left for Engineers? (Arize AI), 2:12](https://www.youtube.com/watch?v=kspZP5BgkEU&t=132): why the code written and the code shipped grow at very different rates, and the review limit behind the gap.
- [The State of AI in Software Development: Data from 400+ Orgs (DX), 15:10](https://www.youtube.com/watch?v=Se8jHLliLXE&t=910): the theory-of-constraints reading, and the view that the constraint is the whole delivery stream, not review alone.
- [How VS Code Went from Monthly to Weekly Releases with AI, 0:12](https://www.youtube.com/watch?v=I2LL_wd89-A&t=12): a small team fixing build, review and feedback loops one after another as agent output grew.

## [Judging each action against the task catches what a static list cannot, but does not replace a deny](cards/judging-each-action-beats-static-lists.md)

- [300 agents, 60 people: how we secured our own AI agents (Runlayer), 7:42](https://www.youtube.com/watch?v=BgLdvF7Qkh8&t=462): why drift shows only across a whole session, and a classifier that reads the session before each tool call.
- [Unlock agent autonomy: the runtime for AI-native systems, 8:13](https://www.youtube.com/watch?v=zaGyGgLW3SM&t=493): access granted by the task's intent, with a worked example, and the admission that it is not solved yet.
- [Stop making your customers click approve (Wise), 4:05](https://www.youtube.com/watch?v=V2UqEUA8NjM&t=245): the counterpoint, where "looks safe" is the wrong question for an action that needs authorisation.

## [Several agents working together are a distributed system](cards/many-agents-is-a-distributed-system.md)

- [Your Sub-Agents Are a Distributed System. Treat Them Like One. (Microsoft), 4:25](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=265): why a confident verdict and a lost answer look alike without explicit states and checks in code.
- [From Chaos to Choreography: Multi-Agent Orchestration Patterns That Actually Work, 3:40](https://www.youtube.com/watch?v=2czYyrTzILg&t=220): an incident with a shared cache, and why coordination grows harder faster than the number of agents.
- [What Does Done Even Mean? Agents and Paperclip's Liveness Model (Paperclip), 1:34](https://www.youtube.com/watch?v=7P0elyLIxXo&t=94): keeping work moving against checking all of it, and where checking everything stops being real.

## [More context is not better context](cards/more-context-is-not-better-context.md)

- [The unreasonable effectiveness of BM25 for agentic search (Hornet.dev), 5:54](https://www.youtube.com/watch?v=fZH97QHHYjY&t=354): context as a small, fixed space, where what you put in decides the result.
- [How I deleted 95% of my agent skills and got better results (WorkOS), 8:26](https://www.youtube.com/watch?v=vy7o1g2iHY8&t=506): a measured case where loaded skill text lowered accuracy, and what replaced it.
- [Context Engineering in 2026: Compaction, Memory & Cost, 40:57](https://www.youtube.com/watch?v=WP3hjUXd918&t=2457): the counter-case, where keeping the full history beat cutting it.
- [How to Build Agents That Run for Hours (Without Losing the Plot), 41:55](https://www.youtube.com/watch?v=mR-WAvEPRwE&t=2515): fresh windows against one long session, and why the authors' answer changed with newer models.

## [One run of an agent is a sample, not a measurement](cards/one-run-is-not-a-measurement.md)

- [Computer use at the edge of the statistical precipice, 2:03](https://www.youtube.com/watch?v=CTLa_p6iOiY&t=123): why pass@k can measure the number of attempts rather than ability.
- [Computer use at the edge of the statistical precipice, 11:27](https://www.youtube.com/watch?v=CTLa_p6iOiY&t=687): intervals that account for variation between tasks as well as between runs.
- [From zero to leaderboard: agent evaluation (Weights & Biases), 39:22](https://www.youtube.com/watch?v=YIxzNZDDy1A&t=2362): a five-run report with mean, best, worst, ceiling and the share solved in every run.
- [Why frontier models fail as buy-side analysts (Google DeepMind, LinqAlpha), 5:54](https://www.youtube.com/watch?v=aVbRSIQO2dE&t=354): reproduced benchmarks whose scores moved widely on the same infrastructure.

## [Pass rate does not see maintainability erosion](cards/pass-rate-misses-erosion.md)

- [Why software factories fail, 12:03](https://www.youtube.com/watch?v=Ib5GBkD555M&t=723): why a reward for passing tests cannot account for how easy the code is to change.
- [AI writes the code, so what's left for engineers? (Arize AI), 6:01](https://www.youtube.com/watch?v=kspZP5BgkEU&t=361): a measurement where asking whether a maintainer would merge cut the success rate well below the test pass rate.
- [AI-generated code is already competing with human code (Greptile), 5:58](https://www.youtube.com/watch?v=474j-n1Ltxc&t=358): review data comparing agent and human pull requests, which finds no clear gap.

## [Some changes still need a person to read the code](cards/people-still-read-the-code.md)

- [The friction is your judgment, 14:28](https://www.youtube.com/watch?v=_Zcw_sVF6hU&t=868): a review step that splits findings into mechanical ones the agent fixes and explicit calls a person must make.
- [The friction is your judgment, 17:32](https://www.youtube.com/watch?v=_Zcw_sVF6hU&t=1052): why removing all friction hands judgment to the agent along with the typing.
- [The Z/L continuum: should AI engineers still read code?, 11:53](https://www.youtube.com/watch?v=ZpK5PWX2YRM&t=713): the read-every-line and fix-the-system positions recast as a choice made per task, not per person.
- [I let agents refactor my codebase for 3 weeks. Then I read the code (Microsoft), 4:35](https://www.youtube.com/watch?v=6TjFjHPjVH0&t=275): what reading the code found after weeks of approving plans.

## [A rule in the prompt is not a control](cards/prompt-rules-are-not-controls.md)

- [We let an AI agent execute Bash and lived to talk about it (PostHog), 9:17](https://www.youtube.com/watch?v=4lXks428C9o&t=557): why detection and blocking stay deterministic and the model is only allowed to triage afterwards.
- [Build a Platform and Watch It Burn (Accenture, Datadog), 41:52](https://www.youtube.com/watch?v=1tpqdglI3T0&t=2512): a live attack on an agent in a platform workshop, and how far the presenters trust the model's own refusals.
- [Claude Code memory](https://code.claude.com/docs/en/memory): the vendor's own statement that rules files are context for the model, not enforced configuration.

## [Agents are reliable where the result can be checked](cards/reliability-follows-checkability.md)

- [State of Data, 6:22](https://www.youtube.com/watch?v=ZyIoTOAbRfs&t=382): three ways to rate how checkable a task is: how easily it splits into checkable steps, whether people agree on what correct means, and how often the world supplies fresh checked examples.
- [Perception Agents (Amazon AGI Lab), 5:29](https://www.youtube.com/watch?v=2JX6JYyQG4Y&t=329): why code was the first field where agents became dependable, and where checking runs into a wall.
- [Jev CEO: I made ChatGPT, now I'm building what's next, 7:19](https://www.youtube.com/watch?v=cJ0EOzey--o&t=439): why a reward built on human preference teaches a model to sound right rather than be right.
- [Reinforcement Learning without Verifiable Rewards (Prime Intellect), 5:50](https://www.youtube.com/watch?v=AQv3qRCG6Gw&t=350): what reward hacking looks like when the reward is a loose stand-in for the goal.

## [Volume metrics reward the wrong work](cards/volume-metrics-reward-the-wrong-work.md)

- [ReviewDebt: a practical framework for scoring every pull request (eBay), 0:00](https://www.youtube.com/watch?v=TJPInBjhE4Q&t=0): industry data on review load as volume grows, and a deterministic score for the review burden of each pull request.
- [From Tokenmaxxing to Trusted Throughput (Ironclad), 5:47](https://www.youtube.com/watch?v=dSg0pu8d6qg&t=347): how one team's metric moved from lines, to open pull requests, to code verified in review and in customers' use.
- [How Building with AI Can Double the Throughput of Your Engineering Team, 3:25](https://www.youtube.com/watch?v=4_VQBbs2iQA&t=205): the other side, a volume target set on purpose by a team that knew it would distort.
