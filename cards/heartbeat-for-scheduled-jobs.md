---
kind: config
why: A scheduled job that stops running, or fails without telling anyone, produces no red, so weeks pass before someone notices that nightly checks or cleanups did nothing.
applies_when: you rely on scheduled jobs (nightly tests, cron scripts, scheduled workflows, agent runs on a timer) whose silence nobody would see
last_reviewed: 2026-11-22
---

# Give every scheduled job an external heartbeat, and watch the alerting itself

## Check

List your scheduled jobs and, for each, name the monitor that alerts when it has not reported:

```
grep -ln "schedule:" .github/workflows/*.yml
crontab -l
```

For each job the answer must be a check outside the job (a dead man's switch service, a cron
monitor) that expects a ping in a window and alerts a person when it does not arrive. Then
check three details: the ping is sent only when the job succeeded; a job added last month is
registered too; and something alerts when the alerting itself goes quiet.

## Fix

Register each scheduled job with an external heartbeat monitor and send the ping as the last
step, after the job's own success check, so a failed run sends no ping. Set the window to the
schedule plus a margin. Add the same for checks that report on a schedule: no positive result in
N days while changes keep merging is an alert. Then watch the watcher: keep one alert that
always fires and have an outside receiver page someone when it stops. On GitHub, note that
scheduled workflows in a public repository are switched off after 60 days without repository
activity, which a heartbeat catches and nothing else reports.

## Learn

- [Healthchecks.io, monitoring cron jobs](https://healthchecks.io/docs/monitoring_cron_jobs/): how a missing ping turns into an alert, and how to set the period and grace time.
- [Sentry Crons, job monitoring](https://docs.sentry.io/product/crons/job-monitoring/): the same check inside an error tracker, with missed and failed check-ins.
- [Prometheus Operator, Watchdog runbook](https://runbooks.prometheus-operator.dev/runbooks/general/watchdog/): an always-firing alert that an outside receiver expects, so a dead alerting pipeline is noticed.
- [GitHub, events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): when scheduled workflows are disabled for inactivity.

## Evidence for

- 2026-11-22: [silent fallback](../docs/classes/silent-fallback.md) records a scheduled job that failed for 12 weeks with nothing watching its outcome, and a process whose only checks ran inside it, so they stopped when it did.
- 2026-11-22: GitHub disables scheduled workflows in a public repository after 60 days without activity, with nothing failing ([GitHub Docs](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [absence read as success](../docs/classes/absence-read-as-success.md)).
- 2026-11-22: it is cheap: free for 20 monitored jobs (as of 2026-10, [Healthchecks.io pricing](https://healthchecks.io/pricing/)) and about an hour of setup.

## Evidence against

- 2026-11-22: it covers only the jobs someone registered; a sibling job added later goes unwatched until it is added ([silent fallback](../docs/classes/silent-fallback.md)).
- 2026-11-22: it tells you a job ran, not that its output was right; a ping sent regardless of the result reports a broken job as healthy.
- 2026-11-22: for checks on pull requests it finds the gap after the merge, not before, since one missing result falls inside the window.
- 2026-11-22: the receiver can share a failure with what it watches, and a watchdog nobody is paged for when it goes quiet watches nothing.

## Guards

- [silent-fallback](../docs/classes/silent-fallback.md)
- [absence-read-as-success](../docs/classes/absence-read-as-success.md)
