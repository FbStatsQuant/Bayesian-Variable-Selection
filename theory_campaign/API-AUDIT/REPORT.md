# API-AUDIT REPORT (referee task R10, CODE-AUDIT): verdicts on the implementation facts the proofs use

Run API-AUDIT, 2026-11-02, branch `theory/API-AUDIT`. **Not reviewed.** Status words follow PROTOCOL.md.
The detailed line-by-line audit is `AUDIT.md` (§1–6 static, §7–8 executed). This file gives one verdict per fact, with
the evidence. The task file names the deliverable `theory_campaign/CODE-AUDIT/AUDIT.md`; under the run's write rule it
is in `theory_campaign/API-AUDIT/`.

**Code version.** Branch base e58a949; the last commit touching `Scripts/SMC_BVS/core` is 39db138. The sha256 prefixes
of the nine audited files equal those recorded by W5-LOCKBOOK (NOTES.md), so W5's audit applies to this exact code.
Unless a path says otherwise, it is relative to `Scripts/SMC_BVS/core/`.

**What "executed" means here.** The testing copies were built outside git: `core_fp` is a hash-checked, byte-identical
copy, and `core_ld` is the same text with every C++ `double` replaced by x87 `long double`
(`scripts/make_cores.sh`). Both read bit-identical uniforms. The test data are 10 synthetic fits: n = 200,
p ∈ {20, 30, 40}, the dev-data covariance scenarios, and fixed seeds (`scripts/valfp_fit.R:1–30`). All 10 fits went
through the SMC branch, ended `completed`, and used tier 0 with T = 3–21 stages (`results/valfp_table.csv`).

## Verdict table

| # | Fact the proofs rely on | Verdict | Main evidence |
|---|---|---|---|
| 1 | **SR**: both configurations scored and offered before the accept draw; no call site disables emission | **HOLDS**, read as "both *feasible* configurations"; "offered" means a ledger event that reaches the stores on its first fresh evaluation | `cpp/v3_engine.h:118–130`; the only `emit=false` is `:381`, and every production caller passes `false` with the already-offered HPM (`cpp/v3_core.cpp:447, 610, 657`) |
| 2 | **GUARD**: no guard path reads an RNG or changes a setting; a run no guard stops is the R̄ computation | **HOLDS** (code reading + executed bitwise on 10/10 fits); **one hazard in the R layer, see 2b** | `cpp/v3_runtime.h:13–28`; check sites `cpp/v3_engine.h:335`, `cpp/v3_core.cpp:450, 613, 660, 738`; `results/guard_table.csv` |
| 2b | A stopped fit is "no output" | **HOLDS for the status and flags. HAZARD:** `fit$log_Z` on a stopped SMC fit silently returns `log_Zbar0` | `v3_fit.R:113, 122–127`, `v3_run.R:111–116`; executed on 10/10 stops (§2b) |
| 3 | **emit_centre / LS0 logging**: LS0's centre S̃₀ is scored and offered to the ledger | **HOLDS in the O-LS0 export only.** Production v3 has **no LS0**. In the export `emit_centre = true` (required: with `false`, a fresh centre would be cached unoffered) | `theory/O-LS0:…/ls0_exports.cpp` (`cpp_final_run_ls0`); `cpp/v3_engine.h:381, 91–94`, `cpp/v3_ledger.h:110` |
| 4 | **Scan before limit** in the local search | **HOLDS**: every scan is complete before the move limit is tested; no RNG use | `cpp/v3_engine.h:384–415` (scan `:393–405`, archive `:406`, limit `:407–409`) |
| 5 | **IND-T sequential stream reading** (`run_island_s`) | **HOLDS**: one stream per island, read sequentially particle by particle; no per-particle streams, no reseeding; guard and local search read none | `cpp/v3_core.cpp:434–437`; `cpp/v3_engine.h:195–218, 250, 274–368`; executed: stream end positions agree in all replays |
| 6 | **VAL-FP** (Prop. 2(f)): η, ε of the floating-point final run against an extended-precision run on the same uniforms | **MEASURED**: η ≤ 2.6e-13 (pooled log Ẑ); 0 path disagreements in 110 replays; first-order ε ≤ 2.2e-6 per final run (threshold logs, 10 fits) | `results/compare_output.txt`, `results/eps_table.csv`, §6 below |

---

## 1. SR: HOLDS (with the two readings stated)

- `Engine::step_gibbs` (`cpp/v3_engine.h:113–132`):
  - `:118` `held(P, ME_GIBBS_HELD)` logs the current state;
  - `:119–123` the other configuration S Δ {j} is built and scored by `eval(tmpQ, ME_GIBBS_FLIP)` with the default
    `emit = true` (`:89`), whenever it is feasible (`add_ok`, `:116`: an addition needs |S| < K);
  - `:124–126` o_j is computed from both scores;
  - `:128` the RB accumulator is updated;
  - **only then** `:129` reads the uniform and `:130–131` update the state.
  So scoring and emission come before the accept draw on every path, whatever the outcome.
- **Infeasible other configuration** (j ∉ S, |S| = K): nothing is scored, o_j = 0, one uniform is still read
  (`:129`), and the state cannot change. So the theorem's SR must say "both *feasible* configurations". This is the
  same reading as W5-LOCKBOOK IMPL-SR.
- **No call site disables emission.** The only `eval` call that can pass `emit = false` is the local-search centre,
  `eval(C, ME_LOCAL, emit_centre)` (`cpp/v3_engine.h:381`). Its three production callers
  (`cpp/v3_core.cpp:447, 610, 657`) pass `emit_centre = false` with centre `led->hpmS`, the current HPM, which has
  already been offered. Every other `eval` uses the default: `:122, :153, :174, :186, :390`, and the initial draws
  `:291`. Every fit engine has a ledger (`cpp/v3_core.cpp:398–402, 579–580`).
- **"Offered" means: a ledger event, passed to the HPM and stores when fresh.** The ledger offers to the stores only on
  a cache miss (`cpp/v3_ledger.h:110`; freshness `cpp/v3_engine.h:90–99`). This loses nothing:
  - every cache insertion is inside an emitting `eval`, except the production centre, which is the HPM;
  - after the cache is cleared (`cpp/v3_score.h:284`), a model is re-scored fresh and re-offered, and the stores are
    idempotent (`cpp/v3_ledger.h:51`).
- Swap and independence proposals are also scored before their accept uniforms (`cpp/v3_engine.h:153<156, 174<177,
  186<189`).
- *Executed corroboration.* In all 110 fp/ld replays (§6), the score counts, cache counters, top store, HPM and HPM
  provenance agree exactly between the cores. This shows no event depends on the precision. It does not test SR by
  itself.

## 2. GUARD: HOLDS

- **Code reading.** `RuntimeGuard` (`cpp/v3_runtime.h:13–28`):
  - holds a clock origin, an allocation, a sticky flag and a record list;
  - `check` (`:21–27`) reads `steady_clock`, appends a record and returns the flag;
  - it has no reference to a `VariateSource`, the data, the start, the ledger, the cache or any setting.
- **The only generator** is `Xoshiro256ss` (`cpp/v3_util.h:43–61`), used only through `RngSource`
  (`cpp/v3_engine.h:20–23`). A search of `cpp/` for other generators finds none (AUDIT.md §2).
- **Check sites.** Each check runs *after* the operation it times. A non-firing check returns `false`, and execution
  then follows exactly the `guard == nullptr` path:
  - C++: `cpp/v3_engine.h:335`; `cpp/v3_core.cpp:450, 613, 660`; `cpp_runtime_check` at `cpp/v3_core.cpp:738`;
  - R: `v3_calib.R:57, 75, 81, 100, 113, 144, 148`; `v3_fit.R:90, 126–131`; `v3_run.R:111–116`.
- **Executed: no stop gives bitwise R̄.** On each of the 10 fits, the production fit (guarded, allocation 24 h / 8 GB)
  was compared with the guard-free pipeline (`runtime = NULL`, no preflight; `scripts/valfp_fit.R` mode
  `fp_nullguard`). On 10/10 fits these were bitwise identical (`results/guard_table.csv`):
  - frozen calibration object 𝓒;
  - full path signature (stream positions, init hashes, per-stage move counts, terminal table, local-search path);
  - `log_Z_r`, `pip_r`, `hpm_F`.
- **Executed: a forced stop ends the fit.** With allocation 0.05 s (mode `fp_stop`), on 10/10 fits:
  - status `resource_limit`, `estimates_available = FALSE`, `hpm_incomplete = TRUE`;
  - the stop fired at checkpoint `bridge_stage` in the pilot (`cpp/v3_engine.h:335`).
  - *Not executed:* a stop inside the final run (`v3_run.R:111–116`); that path is verified by code reading only.

### 2b. HAZARD (new): `fit$log_Z` on a stopped fit returns `log_Zbar0`

- A stopped SMC fit has **no** `log_Z` element. It does have `log_Zbar0`, set at `v3_fit.R:113` before calibration.
  The stop returns are `v3_fit.R:122–127` (calibration) and `v3_run.R:111–116` (final run).
- In such a fit, `log_Zbar0` is the only name starting with `log_Z`. R's `$` on a list partially matches, so
  **`fit$log_Z` returns `log_Zbar0`**, with no warning (unless `options(warnPartialMatchDollar = TRUE)`).
  `fit[["log_Z"]]` correctly returns `NULL`.
- **Executed.** On all 10 forced stops, `fit$log_Z` returned `log_Zbar0`, a positive number (e.g. 66.89 on fit 1,
  20.98 on fit 6) where a completed fit gives about −250 (`results/run_extra.log`; column
  `stop_dollar_log_Z_equals_log_Zbar0` of `results/guard_table.csv`).
- **Consequence for the proofs: none.** The theorem's convention "a stopped fit is no output" (W5 G1) is what the
  status and `estimates_available` say.
- **Consequence for any consumer that reads `fit$log_Z` without checking `status`:** it gets a wrong number, not
  `NULL`/`NA`. I did not sweep the campaign code for such consumers. A grep finds 55 R files using `$log_Z`.
- **Recommended fix** (one line, in `finish`, `v3_fit.R:55–62`): set `fit$log_Z <- NA_real_` (and `log_Z_r`,
  `log_Z_rel_m0`) whenever `estimates_available` is not `TRUE`. Alternatively, rename `log_Zbar0` so that it does not
  extend `log_Z`. This changes the R output structure, so it is not made here. It is flagged for the core owner.
