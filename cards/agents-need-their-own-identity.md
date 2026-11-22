---
kind: belief
why: An agent acting under its user's login cannot be told apart from the user or cut off alone, and it inherits every permission the user holds.
applies_when: agents act through accounts, tokens or OAuth grants on your systems, and you are choosing between an agent identity and running under the user's own
last_reviewed: 2026-11-22
---

# An agent should act under an identity of its own, not its user's

## Check

Pick a recent week of commits, comments and API calls on a system your agents touch. For each,
can you tell from the record alone whether an agent or the person made it? Then ask two
questions of the setup: could you revoke one agent's access without ending the person's session,
and can the agent reach any permission the person holds that its task does not need? If you
cannot tell agent from person in the record, you have neither a separate identity nor
attribution, whichever side of the argument you take.

## Learn

- [You didn't ship a bug. You just wrote it for a human, 9:10](https://www.youtube.com/watch?v=lMCxVorb9wM&t=550): why the trust model built for deterministic programs breaks for agents.
- [How to let AI agents sign up for your app safely (WorkOS), 12:38](https://www.youtube.com/watch?v=uTrY8slys0w&t=758): an agent token limited to the overlap of the user's rights and a ceiling set for the agent; a vendor's demo.
- [Tethered: our agents are us (Two Sigma), 7:16](https://www.youtube.com/watch?v=wCIYViPd4SU&t=436): the opposite choice, agents running as the employee, why separate agent accounts were dropped and what covers the risk instead.

## Evidence for

- 2026-11-22: a talk argues that a broad OAuth grant was acceptable for an ordinary program because its code is fixed and can be reviewed, while an agent is probabilistic and uses whatever it can reach, so it needs its own identity, bound to the user, with narrow rights that expire (the first talk above). An argument, not a measurement.
- 2026-11-22: WorkOS shows a scheme where the agent's token holds the intersection of the user's rights and a ceiling set for the agent: actions are attributed to the agent, it can be revoked without touching the person's session, and it cannot raise its own ceiling (the WorkOS talk). A vendor's design.
- 2026-11-22: [gate checks a proxy](../docs/classes/gate-checks-a-proxy.md) records review requirements met by an approval from the same account that pushed the change; when agent and person share a login, an approval cannot show that someone independent decided.

## Evidence against

- 2026-11-22: the claim is contested. Two Sigma found separate agent accounts cumbersome and runs its cloud agents under the employee's identity, covering the risk with an attribution header every agent must add, like a trace ID, and with controlled web access (the Two Sigma talk). A deployed case on the other side.
- 2026-11-22: what settles the choice is whether a downstream service must tell the agent apart and revoke it separately: if so, a separate identity is needed; if an audit trail is enough and the access machinery already exists, attribution is cheaper. Neither side reports measured incidents.
- 2026-11-22: a separate identity is something to set up and keep narrow, and it limits what is allowed, not which allowed action is wise ([pattern-matched boundaries](../docs/classes/pattern-matched-boundaries.md), identity rung).

## Guards

- [irreversible-effects](../docs/classes/irreversible-effects.md)
- [gate-checks-a-proxy](../docs/classes/gate-checks-a-proxy.md)
