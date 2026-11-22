---
kind: habit
why: An agent writing against a library from training memory uses options, parameters and APIs that do not exist or have changed, and the code looks right until it runs.
applies_when: an agent writes code or commands against libraries, CLIs or APIs that change faster than the model's training data, or that the model rarely saw
last_reviewed: 2026-11-22
---

# Give the agent the documentation for the versions you use

## Check

Read the logs of a few recent agent sessions for errors on unknown options, missing functions or
changed signatures, and look for fixes that removed an API the agent made up. Then, for the
libraries it touched, check whether it had documentation for the exact version in your lockfile
(a documentation server, docs kept in the repository, a small reference project that uses the
library correctly) and whether the session log shows it read that documentation before writing
the call. Documentation that was available and never opened fails the check as surely as none.
Also look at what you give it: exact parameters, values and steps help; a long restatement of
general ideas the model already knows mostly costs tokens.

## Learn

- [Context7](https://github.com/upstash/context7): a server that fetches version-specific documentation and examples for the agent on request, and its own note that it cannot vouch for the accuracy of every library's docs.
- [Skill issue: lessons from skilling up coding agents to use Langfuse, 9:15](https://www.youtube.com/watch?v=vNCY9kXXyDQ&t=555): finding the CLI options agents invent for your tool by reading traces of their real sessions.
- [Your SKILL.md is 70% stuff the model already knows (Intel), 6:54](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=414): a measurement of what a model already knows about a document, which separates general ideas from exact details.
- [How I deleted 95% of my agent skills and got better results (WorkOS), 8:26](https://www.youtube.com/watch?v=vy7o1g2iHY8&t=506): a case where thousands of lines of skills generated from documentation made the agent worse.

## Evidence for

- 2026-11-22: on a benchmark of cloud APIs, retrieving documentation raised the share of valid calls to rarely used APIs from about 39% to about 48% for one model ([claims from plausibility](../docs/classes/claims-from-plausibility.md), citing arXiv 2407.09726). The authors tested their own retriever, not a product, on Python with short synthetic prompts.
- 2026-11-22: Langfuse found that coding agents invented parameters of its CLI, by reading traces of real sessions, and gave agents a skill pointing at current documentation ([Skill issue](https://www.youtube.com/watch?v=vNCY9kXXyDQ&t=555)). A practitioner's case.
- 2026-11-22: quizzing a model on a document's claims without context, one measurement found frontier models knew about 70% of the general ideas but only about 22% of the exact details such as parameters and values ([Your SKILL.md is 70% stuff the model already knows](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=414)). Measured on the author's own set, without outside replication.

## Evidence against

- 2026-11-22: the same benchmark found that retrieval of mediocre precision cost about 39 points on APIs the model already knew well, so the authors retrieve only for APIs the model is unsure of ([claims from plausibility](../docs/classes/claims-from-plausibility.md)).
- 2026-11-22: more documentation can make results worse: in one case a skill generated from documentation took a task from 97% correct without it to 77% with it, and only evals showed that ([How I deleted 95% of my agent skills](https://www.youtube.com/watch?v=vy7o1g2iHY8&t=506)). One person's own evals.
- 2026-11-22: the agent may not ask for the documentation, and the documentation can be wrong; Context7 states that it cannot guarantee the accuracy or completeness of the docs it serves ([Context7](https://github.com/upstash/context7)).

## Guards

- [claims-from-plausibility](../docs/classes/claims-from-plausibility.md)
- [knowledge-not-at-point-of-action](../docs/classes/knowledge-not-at-point-of-action.md)
