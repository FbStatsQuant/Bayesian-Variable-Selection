# ABL-CONF runbook

Status at hand-off (2026-11-03 18:55 CST): **running.** 118 fits queued, no result read, rule not applied.
Design, seeds, cap and rule: `PREREG.md` (commit 1 = 49b3496, made before any fit ran). The rule must not change.

## Where things are

| what | path |
|---|---|
| run checkout (detached, scripts the jobs execute) | `/home/fb31/ablconf_work/checkout` → `theory_campaign/ABL-CONF/` |
| work dir (outside git) | `/home/fb31/ablconf_work` (`fits/*.rds`, `logs/`, `status/`, `claims/`, `progress.log`, `killed.log`, `launch/`) |
| queue (118 lines, fixed) | `results/queue.txt` |
| compiled core (hash-verified copy of production + ABL-START export) | `/home/fb31/ablconf_work/core_abl` |

Launched 2026-11-03 18:54 CST, fully detached (`setsid nohup owls_run -j 2 … < /dev/null`), 3 jobs × 2 workers:

| owls_run job ID | wrapper PID | cores |
|---|---|---|
| 20261103-185401-3108473 | 3108473 | 2,4 |
| 20261103-185406-3108585 | 3108585 | 1,6 |
| 20261103-185411-3108707 | 3108707 | 5,7 |

Per-fit wall cap 4,500 s (75 min). Expected about 60 core-hours, **ETA ≈ 05:00 CST on 2026-11-04** (10.2 h on ABL-START
timings; `results/schedule_estimate.txt` lists the expected finish of each fit). Preflight: the synthetic smoke fit of
arm A in this core was bitwise identical to ABL-START's (`log_Z_r`, `pip_r`, `hpm`).

## Check progress (read-only, no compute)

```bash
cd /home/fb31/ablconf_work/checkout/theory_campaign/ABL-CONF
bash scripts/progress.sh          # terminal outcomes n/118, running claims and their age, live jobs, Owls load, last lines
bash scripts/progress.sh 30       # more lines of progress.log
grep -E "185401-3108473|185406-3108585|185411-3108707" ~/.config/bvs-hq/owls/jobs.log   # START / END rc per job
```

Each fit appends one line to `progress.log`: `completed`, `capped` (hit the 75-min cap; a delivery failure, never re-run)
or `failed` (R error; terminal). A fit killed from outside before the cap is logged to `killed.log` instead and re-run
by `relaunch.sh`. A claim older than 4,600 s means a stuck worker (it should have been capped).

## Re-launch missing fits (after a server restart, reboot, or jobs ending early)

```bash
cd /home/fb31/ablconf_work/checkout/theory_campaign/ABL-CONF
bash scripts/relaunch.sh
```

It releases claims whose worker is gone and starts (3 − live) new detached jobs; fits with a status file are never re-run,
so it is safe to run at any time. If `owls_run` prints `REFUSED`, another fb31 job holds the slots: wait and rerun (do
not bypass). If the guard is not running: `~/.config/bvs-hq/owls/owls_guard.sh start`.

To stop everything (only if needed; the fits in progress become "killed" and are re-run on relaunch):
`kill -TERM -- -3108473 -3108585 -3108707` (process groups of the wrappers; use the PIDs of later launches from
`/home/fb31/ablconf_work/launch/launches.log` if relaunched). Log who stopped it and why in REPORT.md.

## Produce the report (when progress.sh shows 118 / 118 terminal and no live jobs)

```bash
cd /home/fb31/ablconf_work/checkout
git fetch origin && git checkout --detach origin/theory/ABL-CONF       # only RUNBOOK/REPORT files change; scripts are fixed
cd theory_campaign/ABL-CONF
bash scripts/finalize.sh results/final
#  -> results/final/per_fit.csv, reference.csv, rule_designs.csv, rule_verdict.txt, REPORT_TABLES.md
```

`finalize.sh` runs `summarise.R` through `owls_run -j 1` (a few seconds), then `apply_rule.py` and `report_tables.py`.
Then write `REPORT.md`:
1. Status line, run history (launch times, any relaunch / killed fits from `killed.log`), deviations (none expected).
2. The reference table and guard result (from `REPORT_TABLES.md`), with se_ref.
3. Per design × arm table and per-pair table (copy from `REPORT_TABLES.md`).
4. **One paragraph per claim**: the verdict word exactly as `rule_verdict.txt` gives it (LICENSED / REFUSED /
   INCONCLUSIVE), the per-design verdicts, and the numbers that decided it (cost wins and sign-test p, UCB/LCB values from
   `rule_designs.csv`, delivery failures by arm). If Claim 1 is licensed with a `holds_nondeliv` design, the sentence must
   say that singleton factors did not deliver within the 75-min cap there, not that accuracy was equal.
5. Descriptive notes (evaluations, rebuilds, tiers, island SD, PIP, HPM): reported, decide nothing.

Commit `results/final/` (small CSV/MD only; no .rds) and `REPORT.md`, then `git push origin HEAD:theory/ABL-CONF`.
An interim reading before 118/118 is allowed only labelled as interim (`apply_rule.py` prints a NOTE when fits are
pending and cannot return LICENSED).
