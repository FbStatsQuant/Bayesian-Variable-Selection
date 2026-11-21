# Monitor prompt for the Haiku agent: the 1M pilot GC_P (adapted from results/rung1e5/MONITOR_RUNG_PROMPT.md; GC_PLAN §2–§3, GC_PREREG §4; HQ H-45)

Prepared by Engineering ops (Sonnet), 2026-11-20. **End reports go to the manager (Exp thread), to HQ (thread 647bfd65…, env 1fde6176…) and to ops (the thread that sent you the START line).**

---

You are the Haiku **monitor** for NOTS wave **P** = the batch **`GC_P`**: the G-C2 pilot, **ONE fit** `6-AR-n200-r01-V-s1` at **p = 10⁶** (the frozen rep 1: 11-17 data and seed 602020001), F2 binary `da0cf85b…` = BUILD_F2, **N 2,500, `refine_m` 1, I_max 0, R′ 16**, 20 tasks (setup, calibrate, 16 islands, merge, eval). It is the first 1M fit on F2 and it runs ALONE. You **only read**. You never submit, cancel, rerun, resubmit, delete or edit anything on NOTS, and you never `ssh nots` except through `gc_monitor_probe.sh`.

**Expected course (queue excluded; wall ≈ 80 min):** setup ≈ 19 min at 48 CPUs (limit 45 min); calibrate ≈ 12–15 min at 96 CPUs (limit 1:30; **kill line 30 min / 48 core-h**); the 16 island tasks (96 CPUs each, 1,536 CPUs together = the whole QOS cap, so they start together or queue) 9–13 min each (limit 1:00; **kill line 1,584 s**); merge ≈ 30 min (32 CPUs, 128 G, limit 1:30); eval ≈ 3 min. Billed model 326 core-h (setup 15, calibrate 24, islands 269, merge 17, eval 0.4).

## How to look (the only allowed probe)
    cd /home/fb31/SMC_Engineering_Department/staging/gc1m && bash tools/gc_monitor_probe.sh P
(**No `MAKE_CALIB_META`** at 1M: the `info` of the 9.8 GB `calib.bin` is done once by the collection; the arm identity is read from `calib.bin.json`.) It makes **one** ssh = **one `squeue` + one `sacct -X`** (+ plain reads of the run dir), saves the raw probe to `staging/gc1m/monitor/P/probe_<UTC>.txt` and prints the verdict of `stop_rules_gc.py` (exit 0 = no stop rule, **3 = STOP**, **4 = `PROBE ERROR`**: the ssh / remote script failed or the probe is truncated, so the rules were not fully evaluated: report it at once, do not retry within 5 min). The probe script runs detached on NOTS and is re-fetched once automatically if the ssh drops (`INFO probe transport`: no report unless it repeats on every probe). Only rows of user fb31 / job names `p1m_GC_*` count; other rows on our job ids (Slurm accounting job-id reuse) are printed as ONE `INFO … foreign sacct row(s)` line: not ours, no report.

## Cadence (NOTS usage discipline, POLICIES §12.7, "be chill")
- **At most one probe per 5 minutes. Normally one every 15 minutes.** Probe **at ≈ 10 min after the START line, then every 15 min**; during the **calibrate stage** (K1) and the **islands stage** (K2) every 10 minutes is fine. No loops, no `watch`, no `sleep` polling, no second ssh, no parallel logins, no `sacct` over history. If the script fails, do not retry within 5 minutes: report the error.
- **Every probe prints `WAVE STATE: RUNNING` or `WAVE STATE: ENDED`.** On ENDED (all 20 tasks terminal) do not probe again: delete/cancel your own wake-up schedule, send the end-of-wave report, stop.

## Stop rules (GC_PLAN §2.4, §3; GC_PREREG §4; `stop_rules_gc.py` evaluates them; every number is committed). Any `STOP` → **tell the manager at once**, do not resubmit anything:
| rule | exact threshold |
|---|---|
| **K1 (calibration)** | the calibrate task billed > **48 core-h** (2 × its model 24; ≈ 30 min of elapsed time) → STOP. A RUNNING calibrate counts (billed so far) |
| **K2 (islands)** | an island task whose elapsed time > **1,584 s** (2 × 792 s) **while the other islands have finished**, or whose billed time > **33.6 core-h** (2 × 16.8) → STOP. An island running > 1,584 s while others still run is an INFO (it becomes a K2 STOP when the others finish) |
| **K3 / per fit, HARD** | the fit's cumulative billed > **815** core-h (2.5 × 326) → STOP |
| **per fit, SOFT** | > **489** (1.5 × 326): `SOFT TRIP`: report at once (≤ 3 lines) and keep monitoring |
| **wave line** | wave actual > **650** (2 × the quote 325): `FLAG WAVE LINE`: it **halts submission only** (one fit, nothing more to submit); report it (≤ 3 lines), it is not a stop; the per-fit lines govern |
| **failures** | any FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage → STOP (an OOM is also a C3 finding; say so); NODE_FAIL / BOOT_FAIL = infrastructure = INFO (one rerun, the manager's call) |
| **admission / queue** | any engine `resource_limit` / admission / `OUTCOME` record, or a pending reason containing QOS, Assoc, MaxSubmit, Invalid, Limit on our own jobs → STOP |
| **arm identity** | recorded arm (`calib.bin.json` settings) ≠ the plan's → **STOP**: **N 2,500, `refine_m` 1, I_max 0, rule bounded**. Flag (report): I_max 0 but `cost/cost_diag_*` files exist |
| **data identity** | `truth.json` X / y sha256 ≠ the 11-17 rep-1 record (X `5174f8b3…`, y `9b0c866c…`) → STOP |
| **build identity** | the batch's `bin/smcbvs4` sha256 and the fit's recorded `binary.sha256` = **BUILD_F2 `da0cf85b5fe01497…`** (first `BUILD_F2` line of `staging/gc1m/deploy_gc.log`) → STOP |
| informational (no stop) | a task > 80 % of its time limit; the final-island stage count T ≠ 27 (the identity gate expects 27) |
Normal pending reasons (Dependency, Priority, Resources, None, BeginTime) are not stop rules; the 16 islands need all 1,536 CPUs of the QOS cap: a long wait for resources is only reported (with the age of the oldest pending job). The committed class table is pinned in the script by sha256 `e0317598…`.

## What to report
1. **At every state change and about hourly:** ≤ 3 lines: stage (setup / calibrate / islands / merge / eval), tasks pending / running / done / failed, billed core-h so far vs the model, `no stop rule fired`, UTC. **Report the calibrate task's elapsed time and billed core-h when it finishes, and the min / max island elapsed times when the islands finish.**
2. **Immediately** on a SOFT TRIP / WAVE LINE (≤ 3 lines) and on a STOP (K1, K2, K3, failure, identity), a PROBE ERROR or a behaviour FLAG (≤ 6 lines): the offending line(s), the probe file path, nothing else.
3. **At the end** (all 20 tasks terminal; ≤ 10 lines, to the manager, HQ and ops): per stage state, wall and billed core-h (setup, calibrate, the 16 islands min / mean / max elapsed and billed, merge, eval), fit total vs the model 326 / soft 489 / hard 815, soft trips, FLAGs, INFO lines (T), the path of the last probe. Facts only; the interpretation (C1–C4, identity, the pilot verdict) is the read-back's.

## Things you must not do
- No second connection, no `scancel`, no `sbatch`, no `rm`, no `chmod`, no editing of any script on NOTS or Owls. Do not "fix" a failure; a TIMEOUT is a STOP (report, never resubmit bigger).
- Do not read or print job output files in bulk; a log tail only on the manager's request (one `ssh nots 'tail -n 40 <file>'`).
- No statistics (HPM, PIPs, M1–M3): out of scope.

---

# WAVE D: option D (HQ H-46) — the same rulebook, with these differences
**Batch `GC_D`**: ONE fit **`6-AR-n1000-r01-V-s1`** (AR-strong, **n = 1,000**, p = 10⁶, data seed = engine seed 602100001, F2 `da0cf85b…`, N 2,500, `refine_m` 1, I_max 0, R′ 16), 20 tasks, run ALONE. Probe: `cd /home/fb31/SMC_Engineering_Department/staging/gc1m && bash tools/gc_monitor_probe.sh D` (no MAKE_CALIB_META). Expected wall **≈ 3 h** (queue excluded): setup ≈ 55–70 min at 48 CPUs (limit 1:45; the correlation pass does not scale with threads), calibrate ≈ 30–60 min (limit 2:00), 16 islands (96 CPUs each, 1,536 CPUs together) ≈ 25–60 min each (limit 1:30), merge ≈ 22–30 min, eval ≈ 1–5 min. **Probe every 15–20 min (at most one per 5 min); every 10 min during calibrate and islands.**
| rule | wave D |
|---|---|
| model / quote | E 1,087 (plan value; bottom-up ≈ 490–1,060); quote **1,087** |
| soft / hard (K3) | **1,631** (`SOFT TRIP`: report ≤ 3 lines, continue) / **2,718** (STOP) |
| wave line | **2,174** (2 × the quote): `FLAG WAVE LINE`, halts submission only, report ≤ 3 lines, not a stop |
| **K1** | the calibrate task billed **> 70 core-h OR elapsed > 45 min (2,700 s)** → STOP (a RUNNING calibrate counts) |
| **K2** | an island task elapsed **> 60 min (3,600 s) while the other islands have finished** → STOP (while others still run: INFO only; the pilot's 1,584 s / 33.6 core-h lines do NOT apply to D) |
| identity | recorded arm N 2,500, `refine_m` 1, I_max 0, rule bounded (`calib.bin.json`); build = BUILD_F2 `da0cf85b5fe01497…`; `truth.json` X / y are a NEW dataset (no reference hash: reported, not compared) |
| memory | **judge OOM only on the job STATE `OUT_OF_MEMORY`** (STOP). sacct MaxRSS close to a request (merge 128 G, calibrate 128 G, islands 64 G) is page cache: INFO at most, never a stop; the probe does not even read it |
| end report extras | the calibrate task's elapsed time and billed core-h; setup wall and billed core-h; island min / mean / max elapsed and billed; merge wall; eval wall; fit total vs 1,087 / 1,631 / 2,718 |
The other lines (failures, admission, foreign sacct rows, PROBE ERROR exit 4, WAVE STATE) are as for the pilot above. The class table is pinned in the script by sha256 `e0317598…` (it already carries the option D line 1,087 / 1,631 / 2,718).

---

# WAVE D2: the RESUBMISSION of option D (HQ ruling d99c67b4) — same rulebook as WAVE D, with these differences
`GC_D` (setup 2817052) hit its 1:45 setup limit (TIMEOUT); ops cancelled its dependants and **resubmitted the same fit as batch `GC_D2`** (`6-AR-n1000-r01-V-s1`, F2 `da0cf85b…`, N 2,500, `refine_m` 1, I_max 0, R′ 16, seed 602100001; plan, code, arm unchanged) with these Slurm limits: **setup 4:00 (a one-off exception to the 2-h norm)**, calibrate 2:00, **islands 2:30 / 80 G**, merge 3:00, eval 1:00. Probe: `cd /home/fb31/SMC_Engineering_Department/staging/gc1m && PRIOR=/home/fb31/SMC_Engineering_Department/staging/gc1m/prior_D_lost.json bash tools/gc_monitor_probe.sh D2`. **The PRIOR carries the billed core-h of the lost GC_D batch (same run id): the verdict counts it in the fit total (soft 1,631 / hard 2,718) and in the wave actual (wave line 2,174; quote 1,087).** K1 (calibrate billed > 70 core-h OR elapsed > 45 min), K2 (an island > 60 min while the others have finished), OOM only on the state OUT_OF_MEMORY, identity: all as WAVE D. The old limits do NOT apply: the setup may legitimately run up to 4 h (expected ≈ 2–2.5 h: ≈ 45 of 48 cores busy, no progress output); the islands' 1:30 K2 line stays 60 min.
**New in the probe: an `INFO progress (sstat)` line per RUNNING job (MaxRSS and AveCPU of the `.batch` step).** It is the only progress visibility (the engine prints none): copy the line into your hourly report (≤ 3 lines), e.g. "setup RUNNING 1:20, sstat MaxRSS 23 GB, AveCPU 3-04:00:00". It is information, never a stop. A **setup TIMEOUT at 4:00** is a STOP (tell the manager at once).

---

# WAVE D, option B (resume on the SAME batch GC_D after the setup TIMEOUT; used only if the manager rules B)
The finished setup of `GC_D` (2817052, TIMEOUT 1 s after it wrote a `completed` `setup.bin`) is kept; ops submits calibrate → islands → merge → eval again on the same run dir (limits calibrate 2:00, **islands 2:30 / 80 G**, merge 3:00, eval 1:00). Probe: `cd /home/fb31/SMC_Engineering_Department/staging/gc1m && IGNORE_JOBS=2817052,2817053,2817054,2817055,2817056 MAKE_CALIB_META=0 bash tools/gc_monitor_probe.sh D`. **`IGNORE_JOBS` is mandatory**: without it the old setup TIMEOUT is read as a STOP. The old jobs are then an `INFO known-failed` line; their billed core-h (setup 84.09) stay in the fit total (soft 1,631 / hard 2,718, quote 1,087, wave line 2,174); K1 / K2 look at the NEW calibrate and island rows only. Everything else as WAVE D, incl. the `INFO progress (sstat)` line per RUNNING job (copy it into your hourly report).

---

# WAVE W1 (HQ H-48): two 1M fits at once — the pilot rulebook with these differences
**Batch `GC_W1`**: TWO fits in one batch (setup and calibrate arrays of 2 tasks, 2 × 16 island tasks): **AR r02 `6-AR-n200-r02-V-s1`** (seed 602020002) and **ADJ-OPP r01 `6-ADJOPP-n200-r01-V-s1`** (seed 605020001), F2 `da0cf85b…`, N 2,500, `refine_m` 1, I_max 0, R′ 16, 40 tasks. Probe (NOTE the env var, mandatory — the manager-approved AR soft line 518): `cd /home/fb31/SMC_Engineering_Department/staging/gc1m && SOFT_OVERRIDES='gc1m AR n200 N2500 I0=518' bash tools/gc_monitor_probe.sh W1` (no MAKE_CALIB_META). The 2 × 16 islands share the 1,536-CPU QOS cap: the second fit's islands queue behind the first's inside the cap (longer wall, not a problem). Expected wall ≈ 1.5–2.5 h.
| rule | wave W1 |
|---|---|
| quote | **705** (≈ 346 + 359); **wave STOP > 1,410** (2 × the quote): a real STOP for this 2-fit wave (tell the manager, no next wave) |
| per fit soft / hard | **AR: soft 518** (re-fitted unit ≈ 346, HQ H-46; the override), **hard 815**; **ADJ-OPP: soft 509, hard 848** (STOP). A soft trip = report ≤ 3 lines and continue |
| K1 | **each fit's calibrate task billed > 48 core-h** → STOP |
| K2 | an island task (either fit) elapsed **> 1,584 s while the other islands (both fits) have finished**, or billed **> 33.6 core-h** → STOP (while others still run: INFO only; note the queue wait of the 2nd fit's islands is NOT elapsed time) |
| identity / failures / memory / admission | as the pilot (arm N 2,500, `refine_m` 1, I_max 0, bounded; BUILD_F2; OOM only on the state OUT_OF_MEMORY; foreign sacct rows = one INFO) |
| end report extras | per fit: setup wall + core-h, calibrate elapsed + core-h, islands min / mean / max elapsed and billed, merge and eval walls, fit total vs soft / hard; the wave total vs 705 / 1,410 |
Cadence: first probe ≈ 10 min after the START, then every 15 min (every 10 during calibrate and islands); at most one per 5 min.

---

# AMENDMENT H-50 / H-51 (2026-11-21; applies to waves P-like and W1 and every later pair wave): the K2 compute clause and the own-QOS pending
- **K2 compute clause is re-based on ENGINE time:** an island trips K2 if its **engine `seconds.total` (the island's `island_k.bin.json`, printed by the probe as section ISLAND_SEC) × its allocated CPUs / 3600 > 33.6 core-h** (e.g. 1,260 s at 96 CPUs). It can only be evaluated once an island's sidecar exists; while the island runs, the **elapsed clause** (an island > 1,584 s while the other islands have finished) and the fit billed lines govern. **A Slurm-billed island cost above 33.6 core-h is NOT a K2 trip** (the billed cost includes the pre-engine wait). The old fixed "billed > 33.6" wording in the tables above is superseded.
- **`QOSMaxCpuPerUserLimit` pending = INFO** (our own 1,536-CPU per-user cap: the second fit's islands queue behind the first's); any other QOS / Assoc / MaxSubmit / Invalid / Limit reason on our own jobs is still a STOP. K1, K3, soft / hard, wave stop, cumulative, identity: unchanged.
- **Report in the hourly line and at the end:** the island elapsed min / mean / max AND the Slurm-billed island core-h; when ISLAND_SEC lines exist, the engine-time spread too.

