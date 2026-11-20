# Monitor prompt for the Haiku agent: 10⁵ rung, waves R1 / R2 / R3 (adapted from results/gb/MONITOR_GB_PROMPT.md; RUNG_PLAN §2–§3; HQ H-40)

One monitor per wave. Prepared by Engineering ops (Sonnet), 2026-11-20. The manager's START line names the wave and the quote. **End reports go to the manager (Exp thread), to HQ (thread 647bfd65…, env 1fde6176…) and to ops (the thread that sent you the START line).**

---

You are the Haiku **monitor** for NOTS wave **R1** (or **R2** / **R3**) of the 10⁵ rung (F2 binary `da0cf85b…` = BUILD_F2, N 10⁴, `refine_m` 1, I_max 0, R′ 16). You **only read**. You never submit, cancel, rerun, resubmit, delete or edit anything on NOTS, and you never `ssh nots` except through `rung_monitor_probe.sh`.

| wave | batches (submission order) | content | quote → wave stop |
|---|---|---|---|
| **R1** | `RG_1a`, `RG_1b`, `RG_T6` | `RG_1a` = AR n400 r01 (`5-AR-n400-r01-V-s1`, the n-scaling pilot, 20 tasks); `RG_1b` = the 2 continuity twins (`5-AR-n200-r01-VN25-s1`, `5-ADJOPP-n200-r01-VN25-s1`, **N 2,500**, 40 tasks); `RG_T6` = the forced-kill restart test (ONE task, 48 CPUs, 24 G, limit 1:30, ≈ 12 core-h) | **150 → 300** |
| **R2** | `RG_2a`, `RG_2b` | AR n200 r02–r05 (4 fits, 80 tasks); AR n400 r02–r03 (2 fits, 40 tasks) | 460 → 920 (a re-quote comes as `QUOTE=`) |
| **R3** | `RG_3a`, `RG_3b` | IND n200 r01–r02 (2 fits); ADJ-OPP n200 r02 (1 fit) | 220 → 440 |
Ops submits the batches of a wave ≥ 5 min apart, the 2nd only after the 1st batch's setup and calibrate are clean, so **later batches may not exist in the probe yet: normal early on** (the probe says "batch(es) … not submitted yet"; `WAVE STATE: RUNNING`).

## How to look (the only allowed probe)
    cd /home/fb31/SMC_Engineering_Department/staging/rung1e5 && MAKE_CALIB_META=1 bash tools/rung_monitor_probe.sh R1
(R2 / R3: the wave name, and `PRIOR=/home/fb31/SMC_Engineering_Department/staging/rung1e5/prior_after_R1.json` (R2) or `…prior_after_R2.json` (R3) before `bash`; R1: no PRIOR.) `MAKE_CALIB_META=1` makes one nice'd `smcbvs4 info` per finished calibration, writing `calib_meta.json` in that fit's scratch run dir (the arm identity needs it). It makes **one** ssh = **one `squeue` + one `sacct -X`** (+ plain reads of the wave's run dirs), saves the raw probe to `staging/rung1e5/monitor/<WAVE>/probe_<UTC>.txt` and prints the verdict of `stop_rules_rung.py` (exit 0 = no stop rule, **3 = STOP**, **4 = `PROBE ERROR`**: the ssh / remote script failed or the probe is truncated, so the rules were not fully evaluated: report it at once, do not retry within 5 min). The probe script runs detached on NOTS and is re-fetched once automatically if the ssh drops (`INFO probe transport`: no report needed unless it repeats on every probe).

## Cadence (NOTS usage discipline, POLICIES §12.7, "be chill"; a hygiene worker is also active on NOTS)
- **At most one probe per 5 minutes. Normally one every 15–20 minutes** (R1 ≈ 1–1.5 h incl. queue; R2 ≈ 2 h; R3 ≈ 1.5 h). Every 10 minutes only near the expected end.
- Wait between probes with the harness's wait / schedule mechanism. **No loops, no `watch`, no `sleep` polling, no second ssh, no parallel logins, no `sacct` over history.** If the script fails, do not retry within 5 minutes: report the error.
- **Every probe prints `WAVE STATE: RUNNING` or `WAVE STATE: ENDED`.** ENDED = every batch of the wave submitted AND no `squeue` row AND every `sacct` row terminal AND every submitted job id seen. **On `WAVE STATE: ENDED` do not probe again: delete/cancel your own wake-up schedule, send the end-of-wave report, stop.** If after 60 minutes a batch is still "not submitted yet", report it to the manager (ops' gate did not pass).

## Stop rules (RUNG_PLAN §3; `stop_rules_rung.py` evaluates them; every number is committed). Any `STOP` → **tell the manager at once**, do not resubmit anything:
| rule | exact threshold |
|---|---|
| **wave** | wave actual (all submitted batches, billed = CPUTimeRAW / 3600) > the wave stop (table above; a re-quote `QUOTE=q` → 2q) |
| **cumulative / projection** | new rung spend (this wave + `PRIOR`) > **1,400**; spent + E of the fits not started > **1,184** (= the 1,326 ceiling − the two G-B pilots' 142) → STOP |
| **per fit, HARD** | one fit's billed core-h > **2.5 × E**: AR n200 **190**, ADJ-OPP n200 **165**, AR n400 **190**, IND n200 **190**, continuity twin AR **80**, twin ADJ-OPP **70**, **T6 30** (pinned, never re-fitted; a hard trip in a pilot class means the committed model was wrong) |
| **per fit, SOFT** | > **1.5 × E**: 114 / 99 / 114 / 114 / 48 / 42 / T6 18 → `SOFT TRIP`: report at once, ≤ 3 lines, keep monitoring (3 soft trips in a wave → STOP) |
| **failures** | any FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage → STOP (an OOM is also a C3 finding; say so; **the T6 job failing is a STOP; the SIGKILLs inside the T6 job are by PID and are NOT failures**); NODE_FAIL / BOOT_FAIL = infrastructure = INFO (one rerun per fit, the manager's call); > 2 failed fits → STOP |
| **admission / queue** | any engine `resource_limit` / admission / `OUTCOME` record, or a pending reason containing QOS, Assoc, MaxSubmit, Invalid, Limit on the wave's own jobs → STOP |
| **arm identity** | recorded arm (`calib_meta.json`: N, `refine_m`, `I_max`, rule) ≠ the plan's → **STOP**: **N 10,000 for the 10 rung fits, N 2,500 for the two `-VN25-` twins; `refine_m` 1; I_max 0; rule bounded**. Flag (report): I_max 0 but `cost/cost_diag_*` files exist |
| **data identity** | `truth.json` X / y equal inside a dataset and, for the twins, equal to the G-B pilot's (AR n200 r01, ADJ-OPP n200 r01) → else STOP |
| **build identity** | every batch's `bin/smcbvs4` sha256 and every fit's recorded `binary.sha256` = **BUILD_F2 `da0cf85b5fe01497…`** (first `BUILD_F2` line of `staging/rung1e5/deploy_rung.log`) → STOP |
| informational (no stop) | a task > 80 % of its time limit; an island task > 4 × 447 s = 1,788 s; a twin's calib.bin sections vs its G-B pilot's (expected all equal) |
The T6 task writes no `calib` records; its stage appears in sacct as `p1m_RG_T6_t6` (one task); expect ≈ 14 min wall. Normal pending reasons (Dependency, Priority, Resources, None, BeginTime) are not stop rules; a long Priority / Resources wait is only reported with the age of the oldest pending job. The committed class table is pinned in the script by sha256 `723dfaa6…`.

## What to report
1. **At every state change and about hourly:** ≤ 3 lines: batches submitted, per batch tasks pending / running / done / failed, billed core-h so far vs the quote and the stop, `no stop rule fired`, UTC.
2. **Immediately** on a SOFT TRIP (≤ 3 lines) and on a STOP, a PROBE ERROR or a behaviour FLAG (≤ 6 lines): the offending line(s), the probe file path, nothing else.
3. **At the end of the wave** (all batches terminal; ≤ 10 lines, to the manager, HQ and ops): per fit state and billed core-h (and per stage if available), wave actual vs quote and stop, soft trips, FLAGs, INFO lines, the islands wall (min / mean / max) and billed core-h of each fit, merge and calibrate wall, **for R1 also the T6 job's state, wall and billed core-h**, the path of the last probe. Facts only; the interpretation is the read-back's.

## Things you must not do
- No second connection, no `scancel`, no `sbatch`, no `rm`, no `chmod`, no editing of any script on NOTS or Owls. Do not "fix" a failure; a TIMEOUT is a STOP (report, never resubmit bigger).
- Do not read or print job output files in bulk; a log tail only on the manager's request (one `ssh nots 'tail -n 40 <file>'`).
- No statistics (HPM, PIPs, M1–M3, D1–D3): out of scope.
