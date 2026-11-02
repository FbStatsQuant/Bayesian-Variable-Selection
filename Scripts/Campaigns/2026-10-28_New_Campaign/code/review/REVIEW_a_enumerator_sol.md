# Review (a): exact enumerator and SMC-score equivalence

**Verdict: ACCEPT WITH FIXES.** The default score computation and complete-enumeration HPM/certificate logic pass independent checks. Findings 1–2 block use of the current output contract/completion protocol as production reference artifacts. They do not invalidate the tested F values. Fix the remaining correctness and reporting issues before campaign integration.

Reviewer: independent Sol 6.1; 2026-10-28 America/Chicago (checks completed 2026-10-29 02:07:48 UTC). No subagents, SSH, or edits to reviewed files. All runs were local, with at most three threads; no full p=30 enumeration was rerun.

## Scope, reproducibility, and limits

Read the named enum tree, contract/specification, permitted master sections, reference core files, and T37 definition. Scratch, generated synthetic inputs, scripts, compiled modules, raw RDS results, logs, source snapshots, and SHA-256 manifests are under:

`<PC_TEMP_PATH>`

Entry points: `review_checks.R`, `td_cli_checks.R`, `parallel_checks.R`; corresponding `.log` and `.exit` files; all final exit statuses are 0. `launch_commands.txt` records commands. `reviewed_sha256_before.csv`, `snapshot_sha256.csv`, and `readonly_check.txt` provide source identity and confirm **zero changes to reviewed files**. Seeds and synthetic-data construction are in the scripts; generated inputs/masks are saved in `random_*.rds`. R 4.4.1, Windows x64, Rtools GCC 13.2.0; core flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`, plus OpenMP for enum. Startup locale warnings did not affect the checks.

**Reference-build limitation:** an unmodified full `v3.R` build would read unlisted headers/R files. I did not do that. `build_ref.R` extracts `cpp_context`, `cpp_score`, `cpp_enumerate`, index conversion, and output conversion bodies verbatim from the permitted `v3_core.cpp`, compiling against the permitted core score/util headers. It supplies minimal Holder/pointer plumbing and an independently reconstructed bounded ordered TopStore using `v3::hpm_better`. The named `v3_setup.R` and `v3_exact.R` wrap these extracted entry points. Thus the brute-force comparison executes the core's actual enumeration/scoring/accumulation/certificate bodies, but is **not an independent rerun of the full production TopStore implementation**, whose defining header was outside the read list. Full top-1000 order was separately checked by sorting every feasible model in R.

Current enum source hashes agree with VALIDATION.md for C++ and R loader. The CLI hash has changed; see finding 8. Both vendor headers match the production core byte for byte and match `VENDOR_SHA256.txt`:

- `v3_score.h`: `41173ac1460e180e7a30da98260e1e338efb4a685a5052a6cd815aa7cbe26df7`
- `v3_util.h`: `1841122ef2ad6d963b1e0f1d622e1bc154f23fd9e5d347e2b7e02890334d2e15`

## Numbered findings

1. **[blocking] `size_logmass` is joint mass, contrary to §I2's posterior-mass definition.**  
   **Location:** `lowp/enum/lowp_enum.cpp:388`; propagated by `lowp_enum.R:154`; contract `lowp/INTERFACES.md:27` (the `size_logmass` field).  
   The returned value is `log(sum_{|S|=k} exp(F(S)))`; it never subtracts `log_Z`. In my p=14 c100 case, `logsumexp(size_logmass) = -59.160773536742788`, exactly `log_Z`, rather than 0. Subtracting `log_Z` gives `2.22e-16`. All six brute-force cells show this issue. Existing tests explicitly expect the unnormalized identity, so they validate the wrong contract quantity.  
   **Fix:** return `g.mx + log(g.sizem[k]) - logZ` for finite masses; retain the joint quantity under a separately named field if needed. Test posterior normalization and compare each size probability to an independent all-model calculation. Update README/VALIDATION wording accordingly. `cpp_enumerate` itself has no size-mass output to inherit.

2. **[blocking] A failed forced rewrite leaves a stale `.done`, and resume silently accepts it.**  
   **Location:** `lowp/enum/run_enum_dataset.R:32`, `:87`, `:91–93`.  
   Fresh writes use staged files and put `.done` last, which passed. However, `--force` does not invalidate an existing marker before replacing `EXACT.rds`. I first completed a synthetic p=20 job, successfully reran with `--force`, then made the scratch destination `EXACT.sha256` a directory to inject a rename failure. The next forced job replaced the RDS and exited 1 on the SHA rename. Result: `done_exists=TRUE`, `done_matches_current_rds=FALSE`. A normal rerun exited 0 with “EXACT.done exists, nothing to do.” A crash between the two renames produces the same class of failure without the injected obstruction.  
   **Fix:** serialize writers for a destination; remove/invalidate the old completion marker before replacing any committed artifact, and publish a new marker only after both files verify. On the skip path, verify the marker, sidecar, and current RDS hash before declaring completion. Add failure-injection/recovery coverage, including concurrent writers if they are supported.

3. **[should-fix] Partial task runs can claim an exact posterior and a global certificate.**  
   **Location:** `lowp/enum/lowp_enum.cpp:402`, `:414`; `lowp_enum.R:126–127`, `:160`.  
   `lowp_exact(..., p=12, task_bits=3, task_subset=0L)` scored **512 of 4,096** models, yet returned `status="exact"` and `global_certified=TRUE`. The API comment says these outputs are partial, but no corresponding status/flag is applied. The bound compares only visited competitors. The production CLI avoids this hook and checks the final count, so its normal full run is unaffected.  
   **Fix:** determine full feasible-model coverage; label incomplete results `partial`, prevent `global_certified`, and label their normalizers/PIPs as restricted-set quantities. A separately named restricted certificate is reasonable. Cover both `task_subset` and `prefix_fraction`.

4. **[should-fix] TD parameter validation allows a negative depth to defeat `max_scores`; duplicate supports are also accepted.**  
   **Location:** `lowp/enum/lowp_enum.R:181–205`; `lowp_enum.cpp:566–579`.  
   At n=10, p=8, truth `{2,4,7}`, `d=-1`, `max_scores=1000`, the formula predicted **144 scores / 8 centres** and allowed execution; C++ actually used **4,995 scores / 219 centres**. Its recursion never reaches `cur.size()==-1`, so it generates all pool subsets before the size cap filters centres. With truth `{2,2,4}`, d=0, it returned 8 centres but only 6 distinct centre strings; non-set models can reach the scorer. These are invalid inputs, but they should fail before enumeration rather than invalidate the resource guard or score interpretation.  
   **Fix:** validate scalar finite integer `d >= 0`, finite nonnegative margin, unique integer truth/pool indices, feasible truth size, and valid thread/score-limit controls before counting. Use the same validated depth in R and C++; guard count overflow before allocation. For valid inputs the count formula is correct (see below).

5. **[should-fix] Certificate outputs omit the mandatory heuristic label.**  
   **Location:** `lowp/enum/lowp_enum.cpp:403–410`; `lowp_enum.R:151–157`; `run_enum_dataset.R:73–80`.  
   Neither the returned scale record nor its RDS envelope labels η / `certificate_bound` as **“heuristic (not a validated interval bound)”**. The named core does return this label (`v3_core.cpp:568`), and master lines 241 and 251 require it. The numeric comparison rule itself passed.  
   **Fix:** preserve an explicit bound-kind field in every scale record and describe it in README and §I2. Do not imply that `global_certified` is a rigorous interval proof.

6. **[should-fix] Production input verification becomes optional if the manifest is absent.**  
   **Location:** `lowp/enum/run_enum_dataset.R:37–47`.  
   A wrong manifest hash correctly aborted before creating output. Removing the production manifest instead allowed exit 0 and a completed result with `extra$manifest_checked=FALSE`. Computing a file's hash records identity; it does not verify that identity against the sealed inputs. This behavior is disclosed in the current README, so it is an operational verification gap rather than concealed behavior.  
   **Fix:** require the production inputs manifest and exactly one matching hash row for campaign runs. If unsealed synthetic input is useful, make that a clearly named test option and record that mode. The dataset reader otherwise uses `inputs/` and the inputs manifest only; it does not open truth.

7. **[minor] The stated memory bound omits pending task results; configurable hooks can allocate exponentially.**  
   **Location:** `lowp/enum/README.md:41`; `lowp_enum.cpp:321–339`, `:366–374`; `lowp_enum.R:136`.  
   Default production runs have no per-model array: factors/workspace are polynomial, top storage is bounded, and `task_bits=min(p,10)` limits the number of tasks to 1,024. However, completed tasks wait in `res` for earlier tasks, so the worst-case bound includes `ntasks × scales × (top+p+K)`, not just `threads × (p²+top)`. Also, `collect_F=TRUE` explicitly allocates `2^p` doubles per scale, and `task_bits=p` makes the task metadata itself proportional to `2^p`. At p=30, just tasks/res/done/timing/count metadata is roughly 49 GiB on this ABI before accumulator payloads. I did not attempt that allocation. Negative `task_bits` is also not rejected before the shift.  
   **Fix:** qualify the memory claim with the default split and disabled collection hook; document pending-result storage. Validate/cap `task_bits` or add a preflight; bound the reorder queue if an O(threads) claim is desired. The default p=20/30 streaming design is acceptable.

8. **[minor] Validation evidence is substantial and mostly candid, but its current-source and timing descriptions need correction.**  
   **Location:** `lowp/enum/VALIDATION.md:5`, `:57`, `:61–63`; `tests/t6_extrapolate.R:12–17`; `tests/t6_time_p30.R:10`.  
   The logged full p=30 run really reports **1,073,741,824 models, 221.9 s wall, 1,083.8 process CPU seconds**, and zero sampled score mismatches. Thus the full-run timing claim is supported by the supplied log and is clearly separated from extrapolation. I inspected that log, but the raw timing RDS files referenced under the implementer's scratch directory were outside this review's permitted paths. The following details need repair:
   - VALIDATION's CLI SHA prefix `908262f2f2355df2` is stale; reviewed `run_enum_dataset.R` is `2f970fc369e34611224024d778cb2244c93645764c7652d78a5e609ab14d883e`. My current-source CLI smoke test passed apart from findings 2 and 6.
   - The 1,019-second projection comes from `omp_get_wtime()` task durations, so it estimates single-thread **elapsed** time under the sampled load, not measured CPU/core-seconds. Shared-machine descheduling makes the distinction material.
   - The subset timing uses the default `recheck_stride=1009`; the assertion that the projection excludes production rechecks is unsupported by its script.
   - The extrapolation prints process CPU as the literal constant `1084`, rather than reading it from its saved full-run record. The full-run script prints CPU but does not save that field.
   - The 3.03× slowdown multiplier is fitted using the completed full run; recovering its 222 seconds is a retrospective calibration, not an independent predictive check. The ±31 seconds is conditional regression uncertainty, not a campaign wall-time guarantee. The document does acknowledge large machine-load uncertainty, which is appropriate.
   **Fix:** save/read measured process CPU, source hashes, settings and environment with timing results; label elapsed and CPU costs separately; refresh source identity; correct recheck wording and describe the calibrated schedule calculation accurately. Existing logs do not suggest fabricated timing, but the core-hour campaign projection is too definite as written.

## Answers to the numerical and algorithmic questions

**Score and bit-identity argument.** For valid numeric inputs, `lowp_prepare` calls the actual core `v3_preprocess(..., dup_components=FALSE)` on each response and checks identical preprocessed X/index maps. `build_data` calls the unchanged `data_init`: K=min(p,floor(n/2)), g=n, unit ridge, IG(0.01,0.01), ν=0.01+n/2, and `logprior=logw-logWK`, so W_K occurs once. The duplicate-component diagnostic is skipped; standardization and predictor retention are shared.

The append algorithm changes the global traversal order from column-wise to row-wise Cholesky, but preserves the dependency graph and ordered subtraction sequence for **each factor entry**. Matrix entries use the same `n1*g+0/1` and `g+0/1`; Gram symmetry is copied bitwise. Earlier sorted rows do not depend on future rows. Forward solves subtract in ascending index order; prefix log-diagonal sums and prefix sums of squared solve entries preserve the core accumulation order. Multiplication by two, subtraction for Q, the `arg > 0` guard, and logm expression match. The diagonal extrema reproduce the same condition estimates, and η calls the core's actual `error_bound`. With these compiler flags there is no FMA contraction. Failed append pivots propagate slow mode to descendants; low-Q/nonfinite finishes and slow models route to thread-private `Scorer::score`, preserving the core fallback chain and exceptions. The forced-Q tests below check this routing, not a naturally triggered `q_nonneg` or QR failure.

Independent checks:

| Check | Saved evidence | Result |
|---|---|---|
| p=20 and 30, n=96; 20,000 random masks plus empty/full/singletons per dataset; ordinary and extreme column scales (1e120, 1e-120, negative 1e60); four latent columns with 1e-10 perturbations, exact duplicate/sign duplicate; c100/c050 | `review_checks.log`, `review_results.rds`, `random_*.rds` | **160,216** F/η comparisons: **0 differing double bit patterns**, max absolute ΔF=0; no natural fallbacks |
| Complete brute force: n=80,p=14; n=14,p=12,K=7; n=80,p_raw=12 with dropped constant → p=11; both scales | `brute_*.rds`, `review_results.rds` | Counts **16,384 / 3,302 / 2,048** per scale; every feasible collected F matches Scorer bits |
| Same six cells vs extracted core `v3_enumerate` | same | ΔlogZ=0; max PIP difference **5.55e-17**; identical HPM, F/η/second-F bits, margins, certificate bounds/booleans; entire top-1000 matches independent full sorting |
| Independent R aggregation from all feasible F | same | max PIP difference **1.11e-16**; max joint-size-logmass difference **1.42e-14**; normalization defect is finding 1 |
| Forced append failures at internal indices 1 and 8, p=12; forced Q routing `qthr=2` | `review_checks.log` | **3,072** pivot/subtree fallbacks per scale as independently counted; **4,095** Q-route fallbacks per scale; every F bit unchanged |
| Full p=20; p=30 subset tasks 0 and 1023 (duplicate task input deduplicated); threads 1 vs 2 | `parallel_checks.log`, `parallel_*.rds` | **1,048,576 / 2,097,152** models; scale records `identical()`; **1,024 / 2,078** rechecks per scale, zero F/η mismatches |
| Three brute-force datasets at threads 1/2/3 | `review_checks.log` | All scale records `identical()` at fixed task split |

**Aggregates, ties, certificate, and coverage.** HPM and heap ordering use exact F equality, then smaller size, then the lowest differing mask bit; since preprocessing preserves sorted original indices, this is the required lexicographic rule. The independent full sort includes tied scores and dropped-index cases. The second top entry supplies second F, including an equal-F distinct model. The two largest model-tagged F+η values correctly identify the strongest competitor even when the HPM is not the largest adjusted score. Strict `F_HPM-η_HPM > runner_up` matches the core for a complete pass; findings 3 and 5 concern scope and labelling.

Each feasible model has exactly one prefix pattern and one increasing-index suffix path. Patterns exceeding K are skipped; the suffix recursion stops at K. Sorting/deduplicating task subsets avoids duplicate visits. Task-local accumulation is independent of workers, and merges happen in task order, giving thread-invariant statistical/numerical records at fixed split. Timings, requested thread fields, and run attributes naturally differ. Different task splits can change last-bit sums.

The aggregate arithmetic is mathematically equivalent, **not bit-identical to the core in general**: enum normally uses double `exp` cast to long double (`cpp:74–78`), while the core uses long-double exp; subtree PIP sums, prefix partitioning, and merging also change addition order. The observed tiny PIP differences are consistent with that distinction. At campaign n=200,p≤30, uint64 counters/masks and double-reported counts represent 2^30 exactly. Default task indices fit Windows `long`/R integers. Max-shifting prevents exponential overflow; long-double totals prevent a billion weights from overflowing. The unit ridge implies Q≥yty/(n+1), bounding the likelihood-score spread; double-exp underflow is not a concern for these campaign dimensions. This is not a universal precision guarantee for arbitrary n or the advertised p≤62: double masks beyond 53 bits, counts beyond 2^53, very large task splits, and double-exp underflow require narrower supported-domain claims or additional safeguards. No full-billion-model accuracy rerun was attempted in this modest review.

**TD definition and count.** For valid sets/depths, the literal implementation matches the three supplied T37 bullets. For clauses a/b it compares the best designated target move with every *other* move, including the second-best target; ties give zero margin. At truth, margin is minus the best feasible gain. Additions require k<K; deletions and all k(p−k) swaps are scored at K as well. `toward` correctly groups exactly additions of truths, deletions of nulls, and null-out/truth-in swaps as strict symmetric-difference reductions. It is a separately defined diagnostic, not the literal T37 assertion.

My independent neighbour-set implementation at n=10,p=8,K=5,truth `{2,4,7}`,d=2 evaluated **128 centres / 2,914 scorer calls**, agreeing exactly with C++ and `lowp_td_count`; this included **10 centres at K and 150 swaps from those centres**. Both literal and toward margins had maximum difference 0. For valid inputs the count is

`Σ_{u,i:u+i≤K} choose(s0,u) choose(npool,i) × [1+k+k(p−k)+1{k<K}(p−k)]`, k=u+i, i=0..min(d,npool).

The p=1000,K=100,s0=14,npool=986 dry counts independently reproduced **130,228,224**, **144,447,561,728**, and **79,041,632,043,008** scorer calls for d=0,1,2; these large audits were not run. Finding 4 concerns invalid inputs. With a restricted pool, the result concerns that restricted centre region; it should not be described as full-pool TD.

**CLI and evidence sufficiency.** The fresh synthetic p=20 CLI run wrote the required envelope and both c100/c050 scale records, with 1,048,576 models in one traversal. The RDS hash matched both sidecar and marker; both scale records were identical to direct single-thread `lowp_exact`. Wrong input-manifest hashes aborted before output. It reads no truth, and fresh writes follow the intended staging order. Findings 1,2,5,6 prevent unconditional §I2/authority conformance. VALIDATION provides strong empirical score-equivalence evidence and a logged full p=30 timing, but does not establish universal bit identity, normalized size probabilities, crash-safe forced writes, or deployment-platform performance.

## Compact summary

**ACCEPT WITH FIXES:** score arithmetic, valid-input TD, complete model coverage, ordering, and complete-pass certificate numerics passed. **2 blocking:** normalize size posterior masses; fix stale completion markers/recovery. **4 should-fix:** label partial runs; validate TD controls/sets; retain heuristic certificate labels; require sealed-input verification. **2 minor:** correct memory-bound/support claims and validation provenance/timing language. Full production-wrapper/TopStore recompilation and a fresh full p=30 run were outside this restricted, modest review; no reviewed file was changed.
