# NOTS readiness for the 2,400-unit SMC-BVS v3 run (Campaign 2 OPS, Claude)

Author: Campaign 2 OPS lead (Claude Opus 5.5), 2026-10-23. Contract: BRIEF_CLAUDE.md, "Required fixes and readiness" items 1–3. **Status: COMPLETE. Every required check passed. Four items are put to HQ (§9).**

**In plain words:**
- The frozen method code builds on NOTS.
- It passes A's regression and B's independent test battery.
- On small problems where the exact answer can be computed by brute force, its estimates agree with that answer within Monte Carlo error.
- On the two development datasets it gives bit-for-bit the same answers on NOTS as it did on Owls.
- One real benchmark fit ran through the production machinery and came back to the laptop verified.

Code under test: the v2.1 snapshot (HANDOFF_v2_1.md), SHA256SUMS `908a70ca…309b`, core byte-identical to A v2. NOTS: cluster nots, partition commons, GCC/14.3.0 + R/4.5.2 (module library: Rcpp 1.1.0, digest 0.6.37, jsonlite 2.0.0). Code at `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/claude/`; outputs at `/scratch/fb31/smcbvs_v3_deploy_20261022/claude/`. Note: the `…T0235Z` labels in the early output paths came from a wrong local clock; the real UTC times are given below.

## Summary

| Check | Job | Result |
|---|---|---|
| 1. Build (GCC 14.3.0 / R 4.5.2) + compiled cache | 2358209 | PASS |
| 2. A's 32-seed prototype regression | 2358209 | **PASS 32/32** (896 checks) |
| 2b. v2.1 adapter contract test | 2358209 | **PASS, 77 checks** (incl. new F1 + F3 checks) |
| 3. B's frozen battery | 2358210 | **PASS** (17/17 summary checks; R-6 canary = accepted phenotype) |
| 4. Tiny-p SMC versus exact (40 fits, B's oracle) | 2358265/66/67 | **PASS** (0 pre-declared rules fired; \|Δlog Z\| ≤ 0.027; PIP err ≤ 0.0051; HPM 40/40) |
| 5. Two dev smokes via the production runner | 2358268 | **completed; bit-identical to the Owls v2 baselines** |
| 6. Unit limits (3 × NOTS wall, ↑5 min) | — | **L500 = 1,500 s, L1000 = 5,400 s** |
| 7. One real e2e fit + transfer | 2358611 | **ok/ok; pulled, SHA-verified 9/9, RDS/CSV deleted on NOTS with journal** |
| Runner fixes (brief item 2) | — | done (§8) |

## 1–2. Build, regression and contract test (job 2358209, node bb2u12c1, 01:49:26–01:57:23Z, 7 min 58 s, MaxRSS 672 MB)

- Snapshot sums OK before and after (`908a70ca…`).
- Module initialisation from `runner/env.sh`: it initialises Lmod explicitly, runs `module use /opt/apps/modules/Core`, and asserts the GCC and R versions. No GNU time is used anywhere.
- **Regression:** A's NOTS harness (`build/nots_regression.sh`) with only its two path guards adapted. A diff against A's file confirms this; Sonnet review 2026-10-23. Its prepare/worker/compare/summarize steps are unchanged.
  - `SUITE_SUMMARY.md`: "Overall: PASS", 32 seed rows (method seeds 1 … 2147483647), each with 28 inspected checks PASS. Wall time 445 s.
  - The "Owls audit PID" column header is a literal inherited from A's summarizer; the host is NOTS.
- **Contract test** (`smoke/test_adapter_contract.R`, v2.1): exit 0, 78 PASS lines, ending in "adapter fixture contract 77 checks". It includes:
  - "v2.1 F3: R-level OOM is a recorded failed unit";
  - "v2.1 F1: aggregate source hash is independent of the collation locale", with locales tested C, en_US.UTF-8, en_US.utf8 and C.UTF-8. The test asserts that some tested locale collates the paths differently from C, so it has power.
- **Cache:** the first load compiled in 16 s. A second process loaded from the shared cache in 0.47 s. CPP key `41ee124a…0936`.
- **Defect found and fixed:** making the whole snapshot read-only also made the cache read-only, and v3_compile copies the cache with its modes into a private tempdir where Rcpp writes. The first tiny-p job (2358211) failed on this. The cache is now owner-writable (it is not part of SHA256SUMS); the code stays read-only. Logged in FAILED_ATTEMPTS.md.

## 3. B's frozen battery (job 2358210, 01:49–01:51Z, 1 min 36 s)

- C's prepared NOTS packaging (`suites_r3`), used unchanged except for:
  - the output and suite paths (the old `/projects` N0 tree was retired);
  - GNU time replaced by `os.wait4` rusage.
- Payload: 117/117 files match `STAGING_MANIFEST.json` (`0f203566…`), before and after.
- The B payload's `a_code` is A **v2**, because B pins v2's 24-file digest b2abaea2…. v2.1 has the same core.
- Python 3.13 with the SciPy-bundle/2025.07 module (numpy, scipy, mpmath). This environment difference from Owls is recorded. All frozen tolerances are unchanged.
- `BATTERY_SUMMARY.json`: `passed: true`.

| Command | exit | wall (s) | peak RSS (KiB) |
|---|---|---|---|
| reference (7 suites) | 0 | 12.6 | 115,620 |
| comparison (251 + start-law G-tests) | 0 | 18.7 | 492,424 |
| preprocessing | 0 | 0.8 | 82,400 |
| orchestration | 0 | 0.9 | 81,240 |
| adapter | 0 | 0.8 | 81,244 |
| smokes (saved-record extraction) | 0 | 1.1 | 181,460 |
| auxcheck | 0 | 2.0 | 99,016 |
| kernel | 0 | 18.3 | 490,736 |
| kernel_oracle (14 groups) | 0 | 0.5 | 59,904 |
| semantics (10) | 0 | 1.7 | 82,784 |
| containment (6) | 0 | 6.2 | 286,656 |
| supplement (13) | 0 | 0.7 | 80,292 |
| timing_replay | 0 | 17.2 | 493,324 |
| nearconstant_R5 | 1 | 0.9 | 82,248 |

- The summary checks all pass: ordinary exits, 7 reference suites, 251 comparisons, preprocessing, orchestration, 36 + 1 adapter, smoke scores, kernel, kernel oracle 14, semantics 10, containment 6, supplement 13, timing replay, and payload/working source unchanged.
- `nearconstant_R5` exits 1 by design. Its X/y phenotype equals the saved accepted evidence exactly, giving the disposition `ACCEPTED_LIMITATION_B-N1-R2_PER_R-6`.

## 4. Tiny-p SMC versus exact enumeration (jobs 2358265 fit, 2358266 exact, 2358267 compare; 01:58–02:09Z)

Design and rules were fixed before the run in `readiness/tinyp/CRITERIA.md`, following the Fable review in PLAN_REVIEW.md.
- 5 designs × 2 datasets × 4 method seeds = **40 fits** of the public `v3_fit`, using the v2.1 core at its fixed production budgets: N₀ = 2500, 4 islands, `allocation = list(mem_gb = 2, hours = 1)`.
- They are compared with **B's frozen Python oracle** `oracle_score.enumerate_exact`, which enumerates every model with |S| ≤ K:
  - 1,042,380 models (p = 20, K = 15);
  - 261,972 models (p = 18, K = 15);
  - 263,950 models (p = 20, n = 16, K = 8; intended as a cap test, but see the correction below).
- The family-wise false-alarm rate is 0.05, split between the log Z and PIP families, with Bonferroni within each.

**Outcome: PASS.** 0 rules fired, 0 hard failures. All 40 fits are `completed` and took the SMC branch.

| Design | What it stresses | s_D (island sd) | mean Δlog Z | max \|Δlog Z\| | t_B (threshold) | F_A (thr.) | Q_C (thr.) | max \|mean PIP err\| | max PIP t (thr.) |
|---|---|---|---|---|---|---|---|---|---|
| D1 | clear signal | 0.0173 | −0.0040 | 0.0160 | −1.31 (3.54) | 1.31 (5.11) | 1.28 (4.61) | 1.6e-4 | 1.44 (4.31) |
| D2 | correlated X, intermediate PIPs | 0.0201 | −0.0072 | 0.0196 | −2.03 (3.54) | 0.38 (5.11) | 1.30 (4.61) | 4.1e-4 | 1.25 (4.31) |
| D3 | weak signal, diffuse posterior | 0.0065 | +0.0008 | 0.0061 | 0.70 (3.54) | 1.51 (5.11) | 1.48 (4.61) | 2.9e-4 | 2.15 (4.31) |
| D4 | intended cap test, K = 8 (cap NOT reached, see below) | 0.0180 | −0.0080 | 0.0269 | −2.51 (3.54) | 1.53 (5.11) | 2.31 (4.61) | 9.0e-4 | 2.02 (4.31) |
| D5 | null y | 0.0021 | −0.0004 | 0.0020 | −0.99 (3.54) | 1.07 (5.11) | 0.93 (4.61) | 1.7e-4 | 2.07 (4.31) |

In plain words:
- The SMC evidence estimate is within 0.027 nat of the exact value on every fit.
- Every posterior inclusion probability is within 0.0051 of the exact one. The largest error, 5.1e-3, is in D2_rep1, the most correlated design.
- The estimated HPM equals the exact HPM in **40/40** fits, and its score agrees with B's to within 1e-9 nat.
- Differences between the four islands are as large as the method-seed differences (Rule A), so the islands behave as independent replicates.
- The deterministic pooling checks hold in every fit: pooled PIP = rowMeans(pip_r) exactly, and it lies inside the island range.
- The two codes' score scales agree: |log m(∅)_v3 − log m(∅)_B| ≤ 3.9e-14.

**Correction (GO_2400 / gate review M1).** Design D4 did **not** exercise the size cap:
- the exact posterior has E|S| = 2.41 and 2.60 (HPM ∅ and {2}), far below K = 8;
- with n = 16 the seven planted effects were not identifiable.

The cap is therefore untested by this gate. In production, K = 100 against 14 true signals, so the cap is not binding there.

Also, **none of the 40 tiny-p fits escalated** to tier 1 (`escalated` FALSE in 40/40). Tier-1 calibration and final runs are covered only by A's regression, at tiny budgets.

Power: the smallest detectable systematic log Z shift (q·√(var/n_D)) is 0.001 (D5) to 0.013 (D2) nat per design (`min_detectable_shift` in RESULT.json).

What this cannot detect:
- errors smaller than that;
- behaviour that only appears at n = 200, p ≥ 500, such as escalation to tier 1, long schedules and runtime.

Those are covered by A's regression (tier-1 paths at tiny budgets) and by the smokes and the e2e fit.

Evidence: `scratch/.../claude/tinyp_20261023T0158Z/` (`result/RESULT.json`, `REPORT.md`, `fits/*.json|rds`, `exact/*.json`), pulled to `E_ops_claude/evidence/`. The Sonnet review of compare.py against CRITERIA.md found no defect.

## 5. Two dev smokes through the production runner (array 2358268, node bb2u18c1, 01:58–02:27Z)

- Run `smoke_20261023T0158Z`: the production `runner/submit.sh` + `task.sh`, frozen into the run directory, with dev mode, 2 tasks and `%2`.
- Each unit ran as its own `srun` step under `timeout`; the in-run `--hours 4` was a generous smoke allocation.
- Inputs are C's dev inputs, whose RDS hashes equal PILOT.md: `2ba5c283…`, `c4724d92…`.
- The adapter source hash under v2.1 is `b28719e6…4e23`, the same on both units.

| Unit | Whole-process wall (runner) | sacct step | Step MaxRSS | Native runtime_s (Owls v2) | Native peak (KiB) | Status | diag |
|---|---|---|---|---|---|---|---|
| dev_p0500_S4_r001 c100 | **470 s** | COMPLETED 00:07:50 | 266 MB | 466.6 (753.8) | 218,240 | completed; ok/ok | FALSE, `cut_group` |
| dev_p1000_S4_r001 c100 | **1,702 s** | COMPLETED 00:28:21 | 383 MB | 1,694.3 (2,598.7) | 363,996 | completed; ok/ok | TRUE, `final_check_E2;cut_group` |

**Compared with the Owls v2 baselines (C's pilot `smoke_v2_20261022T2315Z`), the statistical outputs are bit-identical across toolchains** (GCC 11.5 / R 4.6.0 on Owls, GCC 14.3 / R 4.5.2 on NOTS) and across v2 → v2.1:
- native status;
- both rule rows' status, support, k, diag_flag and diag_codes;
- HPM, with `hpm_F` difference 0;
- the full primary PIP vector (`identical()`);
- pooled log Ẑ and all four island log Ẑ_r: p500 −78.92629; p1000 −76.29899, with islands −78.026, −75.166, −77.403, −77.255;
- the frozen grid and stage-table row counts (582 and 1,265);
- all final flags.

The p1000 smoke reproduces the known genuine E2 diagnostic (island log-Z sd 1.24 > 1). It is reported, not acted on.

Only runtimes differ: NOTS is about 1.55× faster on this node. Peak memory is under 0.4 GB, against the 2 GB allocation.

## 6. Unit limits (brief rule: 3 × NOTS whole-process wall, rounded up to 5 min)

| p | Smoke wall | 3× | **Unit limit L** | In-run `--hours` | Hard kill (L + 5 min) | Slurm task wall (2 units) |
|---|---|---|---|---|---|---|
| 500 | 470 s | 1,410 s | **1,500 s (25 min)** | 0.41667 | 30 min | — |
| 1000 | 1,702 s | 5,106 s | **5,400 s (90 min)** | 1.5 | 95 min | 2·(5,400 + 300 + 60) + 600 s = **3 h 22 min** (one `--time` for the whole array) |

## 7. One real end-to-end fit through the production runner and transfer (array 2358611, node bb2u12c1, 02:27:42–02:56:52Z)

**Run.** `e2e_20261023T0227Z` is a production-mode `submit.sh` run, separate from production by its run ID and never mixed into it. It ran the real benchmark input p1000_S4_r001 at **c050** with limits L500 = 1500 s and L1000 = 5400 s (`--hours 1.5`, hard kill 5,700 s).

**Result.**
- `.done` written; both rows ok. The `.sha256` file verifies.
- sacct: step `p1000_S4_r001_c050` COMPLETED in 00:29:10, MaxRSS 368 MB.
- Whole-process wall time **1,750 s**; native runtime_s 1,740.4 (calibration 970.7 s, final run 769.3 s); peak 339,304 KiB.
- Native status `completed`, tier 0. `checks_passed_final` TRUE; island log Ẑ sd 0.043; `diag_flag` FALSE; `diag_codes = cut_group`.
- HPM k = 12 and MPM k = 12. They differ in two columns (1 vs 3, 784 vs 783), which is ordinary.

**Independent checks on the laptop copy** (R 4.4.1):
- the input path is `$STUDY/inputs/p1000/p1000_S4_r001.rds`;
- `inputs_sha256 = 6d4b8b5f…`, which equals the study manifest row;
- data seed 1,550,001 and method seed 5,550,001 (= data seed + 4,000,000), scale c050;
- the R-1 rows are hpm/primary ok and pip05/S0 ok;
- the MPM equals {PIP > 0.5} (1,000 PIPs);
- fold and truth fields are NA;
- adapter `2.1-R1`, source hash `b28719e6…` (identical to the smokes);
- allocation 2 GB / 1.5 h.

**Limit guard (PLAN_REVIEW decision 3).** The ratio k = W_e2e / W_smoke = 1,750 / 1,702 = **1.03**. The c050 condition therefore uses 3 % of the factor-3 margin, leaving 2.9× on this scenario and node type.

**Transfer** (C's tool, `E_ops_claude/nots/transfer/`, with the fixes listed in §8):
1. `inspect`: no applicable remote AGENTS.md instructions.
2. `pull`: 9 files streamed, each SHA-checked remotely and locally, then all re-hashed. Receipt `status: verified`, 9/9.
3. `delete`: the allowlist (SMCBVS.rds, SMCBVS.csv) was checked against the verified receipt and re-hashed on NOTS before unlinking. The journal shows `intent` → `deleted` for both, then `complete`.

The tool keeps logs, `.sha256`, `.done` and attempt journals by design.

Laptop copy: `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\claude\e2e_20261023T0227Z\`. Audit trail: `…\.transfer_audit\20261023T1050*` and `…T1051*`.

## 8. Runner fixes (brief item 2) and other repairs

| Required | Done |
|---|---|
| No GNU time | Memory comes from R's own `/proc` VmHWM (`fit$peak_memory_kb`, inside the record) plus `sacct` per unit: each unit is its own `srun` step with State, Elapsed and MaxRSS. B's wrapper uses `os.wait4` rusage. |
| Explicit `module` initialisation | `runner/env.sh`: sources `modules.sh`, or the Lmod `init/bash` file; runs `module use /opt/apps/modules/Core`; purges and loads GCC/14.3.0 and R/4.5.2; asserts both versions; pins single-thread variables, the module R library and `LC_ALL=C.UTF-8`. Exercised by every job above. |
| Resource kills = infrastructure, rerun with the same seed | `runner/reconcile.py` (tested on the smoke and e2e runs) classes: `done`, `pulled` (data deleted after a verified pull), `timeout` (hard kill at L + 5 min; recorded, never rerun), `infra` (OOM, node or wall kill, srun failure, adapter exit 1 without `.done`), `running`, `not_run`. An infra unit gets one rerun with the same seed, run ID and native allocation; if the same kill recurs, it is reported to HQ (ASSUMPTIONS #5). |
| Unit limits from the NOTS smokes | §6: L500 = 1500 s, L1000 = 5400 s. |
| In-run `--hours` = unit limit | `--hours` = L/3600. The hard kill comes at L + 5 min inside the same step, to cover R start-up, core loading and output writing, which run outside the in-run guard's clock (ASSUMPTIONS #3). So the guard, not the kill, ends a slow fit, with `resource_limit` and partial results kept. |
| Status-line check (C-OPS finding 10) | The transfer gate accepts the managing lead's line in any letter case, with remarks. |

Further repairs made here:
- **Lean runner** (ASSUMPTIONS #1) in place of C's backends: `make_tables.py`, `submit.sh`, `task.sh`, `env.sh`, `reconcile.py`.
- **Independent Sonnet review** (`checks/REVIEW_runner_sonnet.md`): 10 findings, all dispositioned. Fixed: lock removal only for locks made by the attempt itself; the runner frozen into each run directory; a GO gate for production; clean-up if sbatch fails; a Python 3.9-safe writer; fatal snapshot check.
- **Unit table** (2,400 units, 1,200 tasks): independently cross-checked by Haiku against the study manifest and C's units_2400.csv. 0 failures, and 3/3 planted canaries were caught. It was re-checked after the final ordering. Ordering: p1000 first, cycling S1…S6 within each replicate, so every scenario is timed in the first wave. Hashes: `chunks.tsv 5a484c96…`, `units.tsv eb59eb56…`.
- **Cache-permission defect** (§1), fixed.
- **Transfer tool from Windows.**
  - The inline base64 helper failed: first on argv double quotes, then on payload truncation ("Incorrect padding").
  - The identical `remote.py` (`bfe4bbdc…`) is now staged at `deploy/claude/transfer/remote.py`, and every call verifies its SHA-256 before running it.
  - The tool's 15-minute back-off file was cleared after these two failures, because they were helper errors on a working connection, not network timeouts.

## 9. Decisions for HQ before GO_2400

1. **Node type.** The commons partition mixes **72 Cascade Lake nodes** (80 CPUs) and **70 Sapphire Rapids nodes** (192 CPUs). The smokes, the e2e fit, and therefore the limits were all measured on Sapphire Rapids.
   - **Recommended:** pin production to `--constraint=sapphirerapids`. `submit.sh` supports this through the `CONSTRAINT` variable, recorded in the manifest. That pool has 13,440 CPUs, so a %100 array is a small share of it.
   - Alternative: measure one Cascade Lake smoke first (about 35 min) and allow both node types if the slowdown is within the margin.
2. **Limit adequacy.**
   - **Basis:** the limits rest on one scenario (S4) per p; the brief requires this. The c050 effect is measured at k = 1.03.
   - **Mitigation:** the task order puts all six scenarios in the first wave, and any timeout is reported in STATUS at the next poll.
   - **Rule:** timeouts are recorded and never extended. If HQ wants a stop rule, for example "pause the array and consult if more than N of the first 100 tasks time out", it should state it in GO_2400.
3. **Confirm the F5 interpretation:** in-run `--hours` = L, with the hard kill at L + 5 min.
4. **NOTS clean-up after the pull.** C's tool deletes only data files (rds, csv, json). The retained small files (logs, `.sha256`, `.done`, Slurm output; a few MB) would be removed after OUTPUTS.md with a separate SHA-checked step, unless HQ wants them kept.

## 10. Production plan (Phase 2, only after GO_2400.md)

**Submission.** `CONSTRAINT=sapphirerapids bash runner/submit.sh prod_<ts> tables/production prod 1500 5400 100`. This requires `deploy/claude/GO_2400.md` and creates:
- a 1,200-task array, `%100`;
- 1 CPU and 2 GB per task;
- `--time 3:22:00` per task.

**Run record.**
- **Frozen snapshot:** the code is v2.1, read-only (SHA256SUMS `908a70ca…`); the runner is copied read-only into the run directory.
- **Run directory:** `manifest.json` (code, runner and table hashes, inputs manifest `1a42b919…`, sbatch arguments, job ID).
- A row in RUNS_CANDIDATES.md.

**Expected cost (S4 proxy, Sapphire Rapids).**
- Per dataset: p500 ≈ 2 × 470 s and p1000 ≈ 1,702 + 1,750 s.
- Total about 2.64 Ms ≈ **732 core-hours**. NOTS counts 2 logical CPUs per core.
- At %100 that is about **7.5–8.5 h** of wall time, excluding queue waits.
- Outputs: about 2.4 MB per p1000 unit RDS (about 4 GB in total, scratch only).

**Monitoring and finish.**
- Poll at most every 10 min, one ssh connection; reconcile with `reconcile.py --sacct`.
- Infrastructure reruns as in §8.
- Then pull with the transfer tool (copy → sha256 → verify), write OUTPUTS.md, and only then delete on NOTS (PLAN_REVIEW decision 4b).
