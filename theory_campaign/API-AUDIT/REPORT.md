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

## 3. emit_centre / LS0 logging: HOLDS in the only LS0 implementation; production has none

- **Production has no LS0.** All three `local_search` calls (`cpp/v3_core.cpp:447, 610, 657`) start at `led->hpmS`
  with `emit_centre = false`. No call starts at the start mode S̃₀.
- **The only LS0 is the O-LS0 test export** (`theory/O-LS0:theory_campaign/O-LS0/scripts/ls0_exports.cpp`).
  - `cpp_final_run_ls0` is `cpp_final_run` plus one block after the final local search, run only if
    `status == "completed"`: `ModeResult m = start_mode(st); E.local_search(m.S, o.ell, o.tier, true, -2);`.
  - It runs on the **same** `Ledger` and `ScoreCache`, followed by a guard check labelled `"ls0"`.
  - So S̃₀ is a ledger event (`cpp/v3_engine.h:381` with `emit = true`), and so is every scanned neighbour (`:390`).
  - LS0 reads no uniforms and runs after the islands, so it does not perturb any stream.
- **`emit_centre = true` is required, not cosmetic.** With `false`, a fresh centre is scored and inserted in the
  cache (`cpp/v3_engine.h:91–94`) but never offered. Later hits on it are not fresh (`cpp/v3_ledger.h:110`), so it
  would stay out of the HPM and stores until the cache is next cleared. The export sets `true`.
- **Verdict for the paper.** "LS0's centre is logged" holds for `cpp_final_run_ls0`. If the theorem is about
  "v3 + LS0", the supplement must cite that export as the reference implementation, or the block must be merged into
  `cpp/v3_core.cpp`. As committed, the production core is v3 without LS0.

## 4. Scan before limit: HOLDS

`Engine::local_search`, `cpp/v3_engine.h:378–418` (spec comment `:370–377`; the task's "369–420" brackets it).

- Each pass of `while (true)` (`:384`) does the following, in order:
  - scores every feasible flip (`:393–398`; additions are skipped only when |C| ≥ K, `:396`);
  - scores every swap j ∈ C, l ∉ C (`:399–405`);
  - writes the archive with `scan_complete = 1` (`:406`);
  - **only then** tests whether there is a strict improvement (`:407`) and the move limit `A.moves >= ell` (`:408`).
- At the limit, it returns `best` *after* the complete scan (`:409`). Otherwise it moves (`:411`). With no strict
  improvement, it is certified (`:413`).
- So there are at most ℓ moves and ℓ + 1 complete scans, and every neighbour of every scanned centre is a ledger
  event (`:390`).
- Ties are broken lexicographically (`:391`); an exact F tie is not a move (`:407`).
- There is no `VariateSource` in the function, so it uses no RNG.
- *Executed corroboration:* local-search path, scanned centres and termination agree exactly in all 110 replays.

## 5. IND-T sequential stream reading: HOLDS

- **One stream per final island.** A fresh `RngSource`, seeded `seed_stream(seed, 9 + r)`, is created per island
  (`cpp/v3_core.cpp:434–437`; streams 10–13). The calibration uses streams 0–9 (`:594–595, 635–636`).
- **Order of reads in `run_island_s`** (`cpp/v3_engine.h:274–368`), all from the one `vs`:
  1. N initial draws, particle 1 first (`:286–292`);
  2. per stage: the reweighting (no uniforms, `:317–322`), then N resampling uniforms (`:250`), then
     `population_round` (`:331`);
  3. then the L + Hm rounds (`:343–360`).
- **Within a round:** particle i finishes its whole round before particle i + 1 starts (`:215–218`). Each round reads
  its m − 1 order uniforms first (`:195–200`, m = p + B + 2, `:72`), then the step uniforms (`:202–214`).
- No other object reads the stream: there are no per-particle streams, no reseeding, and neither the guard (§2) nor
  the local search (§4) reads a uniform. So W5's Lemma STREAM applies as stated.
- *Executed:* `position_end` and `init_draws_hash` of all four final streams agree in all 110 fp/ld replays and in the
  10 guarded/guard-free pairs.

## 6. VAL-FP (Proposition 2(f)): MEASURED

**Contract measured.** VAL-FP(η, ε) says the floating-point run is within η of the exact run outside an event of
probability ε (W5 `PROOF.md:175`). The calibration grid is continuous, so the exact run cannot be required to
reproduce 𝓒 literally. I therefore state and measure the contract **given the frozen object 𝓒^fp**:
- the final run under 𝓒^fp in double, against the same final run in long double, on the same streams;
- G_fp = {every discrete decision of the final run agrees};
- ε = P(G_fp^c);
- η = max |log Ẑ_fp − log Ẑ_ld| on G_fp.

The long-double core has 11 more mantissa bits, so its own error is about 2⁻¹¹ of the double error. Its outputs stand in
for exact arithmetic, and η as measured is accurate to well under 1%.

### 6.1 Replays (`results/compare_output.txt`, `results/valfp_table.csv`, `results/valfp_seeds.csv`)

| Run | Paths that agree | η, pooled log Ẑ | η_r, island log Ẑ_r | max \|ΔPIP\| | HPM |
|---|---|---|---|---|---|
| 10 production fits; ld replay of the final run on 𝓒^fp | 10/10 | ≤ 2.26e-13 | ≤ 2.49e-13 | ≤ 2.0e-13 | same model; ΔF ≤ 2.3e-13 |
| 10 fits × 10 further final-run seeds (100 replays) | 100/100 | ≤ 2.59e-13 | ≤ 2.86e-13 | ≤ 2.0e-13 | same in all |
| 10 fits, full ld fit (calibration too) | 10/10 | ≤ 2.32e-13 | — | — | same |

- "Paths that agree" compares the full discrete path:
  - stream end positions and init-draw hashes;
  - every per-stage move and acceptance count;
  - the terminal table, score counts and cache counters;
  - the HPM and its provenance, the MPM;
  - the local-search path, scanned centres and termination;
  - the top store and near ties.
- *Full ld fit* (`ld_full`): the long-double calibration froze the same status, tier, T, inherited set and calibration
  HPM on 10/10 fits. Its grid differed by at most 5.8e-14. So on these fits 𝓒^ld and 𝓒^fp differ only by continuous
  rounding, and the given-𝓒^fp statement loses nothing.
- **η.** |log Ẑ| ≈ 140–290 here, so η ≈ 2.6e-13 is a few ulp of log Ẑ (ulp ≈ 5.7e-14 at 250). This is about
  1e-15 *relative* in log Ẑ, and about 2.6e-13 relative in Ẑ.
- **ε from replays alone:** 0 disagreements in 110 paths. The one-sided Clopper–Pearson 95% upper bound, 1 − 0.05^(1/n), is 0.027 (0.0295 on the
  100). This is weak, which is why the threshold measurement below was added.

### 6.2 Threshold logs: first-order ε (`results/thr_table.csv`, `results/eps_table.csv`)

**Instrumented cores.** `scripts/make_log_cores.sh` builds copies of both cores that write out, during
`cpp_final_run` only, every threshold a uniform is compared with:
- the Gibbs o_j;
- the three swap/independence acceptance probabilities;
- all N normalised cumulative weights before each resampling;
- the two π₀ cumulative boundaries of each categorical draw.

No arithmetic changes. Checked: the logging fp core reproduces the production `log_Z_r` bit for bit on 10/10 fits
(`results/run_thr.log`). Logs from the two cores are aligned entry by entry. Every fit's tag sequences matched, i.e. the
path agreed.

**Estimate.** Under EX-S, a uniform is U(0,1) and independent of the threshold it meets. So, given agreement up to that
point, a comparison flips with probability |t_fp − t_ld|:
- a resampling draw flips with probability Σ_k |ΔW_k|;
- a π₀ draw flips with probability Σ_k |Δc_k|, estimated without bias at the drawn k (`scripts/analyze_thr.py`).

**Index draws** floor(u·k) (`cpp/v3_engine.h:150, 151, 167, 171, 199`) cannot be logged as thresholds, so they were
counted exactly (`scripts/index_draw_flips.py` → `results/index_draw_flips.csv`):
- In long double, u·k is exact (x·k < 2⁶⁴). In double, it can round up onto an integer.
- The number of 53-bit uniforms where this happens is at most 31 for every k ≤ 64, i.e. ≤ 1.2e-15 to 2.0e-15 per draw
  for the round lengths here (k ≤ m = p + B + 2 ≤ 48).
- The resampling bucket `floor(ue·N)` (`:252`) is only a starting guess, corrected by `:254–255`, so it cannot flip.

| Channel (sum over one final run, max over the 10 fits) | ε contribution |
|---|---|
| resampling (N draws × Σ_k \|ΔW_k\| per stage) | 1.6e-7 – **2.1e-6** |
| index draws (bound: all uniforms × max_k P_k) | ≤ 7.3e-8 |
| π₀ categorical draws | ≤ 3.3e-8 |
| Gibbs o_j | ≤ 1.4e-8 |
| neighbour swap / independence / uniform swap α | ≤ 7.0e-9 / 2.9e-9 / 7.0e-10 |
| **total, first order (union bound)** | **2.4e-7 – 2.2e-6 per final run** |

So **ε ≈ 2e-6 per final run** on these fits. It is dominated by the N² boundary comparisons of multinomial
resampling. It grows roughly with N² × (number of resamplings) × (cumulative-sum rounding). The first-order sum is an
upper bound up to O(ε²).

**Caveats.**
1. *Grid granularity.* Uniforms lie on the 2⁻⁵³ grid, while |Δt| is about 1e-16. The flip probability at one comparison
   is |Δt| only on average over where t lies relative to the grid. This is the right quantity for an expected count.
2. *Scope: final run only.* Calibration decisions are inside 𝓒^fp by construction (§6 contract). The full-ld check
   above found them unchanged on 10/10 fits.
3. *Deterministic F comparisons are a separate channel, not part of ε.* These are the HPM order, the local-search
   best/move tests (`cpp/v3_engine.h:391, 407`) and `hpm_better`. Here precision flips a decision only when two F
   values are within about 1e-13 of each other. That is a property of the data (near ties, which the fit reports as
   `near_ties`), not a probability over uniforms. Observed: 0 such flips in 110 replays.
4. *Size and form of the test fits.* p ≤ 40 and n = 200. ε scales with N and T, so production-size fits (larger N, T)
   should be expected to have proportionally larger ε. The bound is still many orders below any statistical error.

## 7. Corrections to earlier records, and what is left open

**Corrections.**
- Task text "local_search lines 369–420": the function is `cpp/v3_engine.h:378–418`.
- The task names `run_island_s`. The final run calls `run_island` (`cpp/v3_core.cpp:437`), a thin wrapper that calls
  `run_island_s` (`cpp/v3_engine.h:269–272`). The pilot and diagnostics call `run_island_s` directly
  (`cpp/v3_core.cpp:600, 638`).
- W5's VAL-FP repair ("the exact run has the same status and 𝓒") is replaced by the contract **given 𝓒^fp** (§6).
- SR-3 (AUDIT.md §1) is new and harmless: table and inherited models enter the stores without entering the cache.

**New hazard.** `fit$log_Z` on a stopped fit returns `log_Zbar0` (§2b). The proofs are unaffected. A one-line fix is
recommended to the core owner.

**Open / not done.**
1. The stop path *inside the final run* (`v3_run.R:111–116`) was not executed; it is verified by code reading only.
   Forcing it needs an allocation that passes calibration but not the final run, which depends on timing.
2. LS0 was not executed in this run. Its audit is code reading of the O-LS0 export (§3).
3. No sweep of campaign consumers for unguarded `$log_Z` reads (§2b).
4. ε and η were measured at p ≤ 40, n = 200, tier 0. Production-size fits were not replayed.

**Reproduction.** `make_cores.sh` → `run_valfp.sh` → `run_extra.sh` → `compare_valfp.R` → `make_log_cores.sh` →
`run_thr.sh` → `index_draw_flips.py 256` → `eps_table.R`. All scripts are in `scripts/`, and all were run through
`owls_run -j 2` (or `-j 1`). The working directory `~/api_audit_work` is outside git. The threshold logs (0.15–0.44 GB
per fit) were deleted after analysis.
