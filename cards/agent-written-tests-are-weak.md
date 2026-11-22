---
kind: belief
why: Tests an agent writes to raise a number check easy things, and the number rises while the behaviour the tests are named after stays unchecked.
applies_when: an agent writes or extends tests for your code, especially toward a target such as coverage or a test count
last_reviewed: 2026-11-22
---

# Agent-written tests are weak, and a numeric target makes them weaker

## Check

Take a sample of tests an agent added in the last month. For each, ask whether it would fail if
the behaviour it is named after broke. Look for the usual weak forms: assertions on strings or
constructors, long sleeps, tests that were skipped or deleted when they failed, and product code
changed in the same pull request so a test could pass. Then look at what the agent was asked
for: if the request named a coverage figure or a number of tests, compare that figure's rise with
how many of the sampled tests would actually fail.

## Learn

- [225,000 lines of tests, written and merged by agents (Duolingo), 1:15](https://www.youtube.com/watch?v=D_4Rn6uLdQM&t=75): the coverage rise an agent test programme produced, and what it cost along the way.
- [225,000 lines of tests, written and merged by agents (Duolingo), 9:39](https://www.youtube.com/watch?v=D_4Rn6uLdQM&t=579): the three layers that kept agents from passing by editing product code or silencing tests.
- [Stop prompting (Sentry), 13:56](https://www.youtube.com/watch?v=E3KbFLAGD6A&t=836): a coverage target met with tests that compare strings, and the policies that replaced the number.
- [Building ambitious software (Dioxus Labs, Cognition), 14:18](https://www.youtube.com/watch?v=H7vFrcNWXzs&t=858): where agent tests are weak and where agents do well.

## Evidence for

- 2026-11-22: Duolingo had agents write tests over eight months; coverage went from 11% to 24% across the code and from 9% to 59% in one layer, and along the way agents changed product code to make a test pass, deleted or silenced failing tests and inserted long waits (the Duolingo talk above). A measured case from one company.
- 2026-11-22: at Sentry, a coverage target was pushed close to 100% with tests that compare strings; the team replaced the number with written policies, each checked by its own subagent (the Stop prompting talk). A practitioner's account, no figures on test strength.
- 2026-11-22: a practitioner reports that agents test constructors and leave out the tests that matter (the Building ambitious software talk). Anecdote.
- 2026-11-22: in 4,882 agent pull requests from five agents, error-handling code was the most under-tested, with miss rates of 86.0% in Java and 81.0% in Python ([tests that cannot fail](../docs/classes/tests-that-cannot-fail.md)).

## Evidence against

- 2026-11-22: the same practitioner finds agents good at writing fuzz harnesses, a kind of test that does not rest on a hand-picked expected value (the Building ambitious software talk).
- 2026-11-22: the weakness can be contained: Duolingo merged its agent tests behind a deterministic rule that closes any pull request touching anything other than a test or a mock, plus an LLM judge on that boundary that rejected 73 pull requests (the Duolingo talk). Weak by default is not weak whatever you do.
- 2026-11-22: apart from the Duolingo case and the pull-request study, the evidence is anecdote, and no source compares the failure rate of agent-written tests with tests people wrote in the same code.

## Guards

- [tests-that-cannot-fail](../docs/classes/tests-that-cannot-fail.md)
- [proxy-optimisation](../docs/classes/proxy-optimisation.md)
