# LOC_R01 — design review (Codex gpt-6.1-sol, reasoningEffort high, fresh delegate_task, 2026-11-09 ~10:35–11:00 CST)
Reviewed: LOC/DESIGN.md v1, LOC/scripts/*, results/LOC/pilot_summary.md, pilot01/, validation_*.txt. Reply verbatim below.

---

References below are relative to `Theory_work/Wave2/W2-SIM/`; `scripts/` means `LOC/scripts/`.

1. **MAJOR — `fast_partition` does not exactly reproduce the reference.**  
   `scripts/loc_core.py:157`, `DESIGN.md:18`; reference `W2-FAC-B/numerics/bvs_core.py:155–179`. The reference treats distances within `1e-10` as tied; SciPy uses their actual ordering. Thus distinct continuous correlations do **not** guarantee equivalence. Confirmed locally with a positive-definite correlation matrix having \(r_{01}=0.5,\ r_{12}=0.50000000005,\ r_{02}=0.1\): at B=2, reference blocks are `[[0,1],[2]]`, fast blocks `[[0],[1,2]]`. **Fix:** reproduce the reference tolerance and tie rule, or explicitly designate and validate a production-equivalent partition instead.

2. **MAJOR — screening does not certify the selected move or stopping decision.**  
   `scripts/loc_core.py:295–322,347–348`. `fast_err_max` checks only selected neighbors and the center. An excluded neighbor underestimated by more than the window could be the exact winner, including a tied lexicographically preferred winner. Small observed errors among included candidates do not bound excluded errors. Nonfinite fast scores also lack a fallback. **Fix:** use exhaustive exact scoring, or a justified error bound for every excluded candidate with exact fallback whenever exclusion cannot be certified. Keep heuristic and exact certification flags separate.

3. **MAJOR — validation misses the cases needed to support large-run equivalence.**  
   `scripts/loc_validate.py:12–30,42`; `results/LOC/validation_local.txt`, `validation_nots.txt`. Both logs show no accepted additions, start modes at most 21, and no move-limit stops; the pilot reaches mode size 552. Adding three nulls neither forces additions nor reliably forces swaps. There are no constructed tie/near-tie cases or exhaustive neighbor-score comparisons. Validation failure also merely prints `ALL_EQUAL False` and exits successfully. **Fix:** add missing-truth/empty starts, large correlated starts, K-boundary and cap-zero cases, exact/near ties, and all-neighbor score checks; exit nonzero on failure.

4. **MAJOR — Q2 confounds two truths with a known PTV failure.**  
   `scripts/loc_core.py:85–88`, `DESIGN.md:83–86`. For group A at ρ=0.8, the second truth has marginal signal \(0.8(1)-0.8=0\), violating PTV already at \(U=\varnothing\). Moreover, `one` versus `two` changes support size, occupied groups, coefficients, and total signal. `two` correctly places two truths in each of two occupied groups, but its failures cannot isolate multiplicity. **Fix:** retain masking as a separately labeled stress arm; add a PTV-verified two-truth arm and matched one-/two-truth controls with the same coefficients and support size.

5. **MAJOR — `pure_deletion` can report successful stripping after deleting a truth.**  
   `scripts/loc_run.py:119`. Starting with S₀ plus one null and deleting one true variable satisfies the implemented predicate: one deletion equals one extra, with no initial missing truths. **Fix:** require `final == S0` as well, or require every deleted index to be an initial extra. Separate “deletions only” from “pure deletion to S₀.”

6. **MAJOR — the path addition margin does not test no-addition.**  
   `scripts/loc_run.py:94–101`, `DESIGN.md:65–79`. On accepted moves, `best_F − best_add_F` is nonnegative by construction, even when an addition improves the center. For example, center=0, best deletion=2, best addition=1 yields margin +1 despite an NA violation. The path also does not cover the theorem’s whole lattice, and exceeding the stated approximate h threshold is not itself proof of NA failure. **Fix:** additionally record `F(T) − max_add F(T+l)` at S₀ and every scanned superset center; distinguish observed path violations, whole-lattice claims, and h proxies.

7. **MAJOR — the proposed growth comparison ignores saturation and selection bias.**  
   `DESIGN.md:69–78`. For α=0.2, the benchmark exponent is 2.5, while extras cannot exceed p, growing only as \(n\) or \(n^{0.6}\). Visibility counts also saturate at p. Consequently these cells cannot distinguish the proposed uncapped exponent from slower growth. Excluding every sequence with any zero mean further selects the slope sample; changing B at smaller n adds another transition. **Fix:** fit separately by p rule, mark saturated regimes, compare against finite-p visibility predictions, prespecify treatment of zeros and polylog powers, and restrict exponent comparisons to unsaturated ranges with stable B.

8. **MAJOR — production and port have different move-cap return semantics.**  
   `scripts/loc_core.py:330–334`; production `Scripts/SMC_BVS/core/cpp/v3_engine.h:410`; `DESIGN.md:91–93`. At the cap, the port returns the last center; production returns the best improving neighbor from the extra scan without incrementing moves or appending that neighbor to the path. A production/port endpoint mismatch therefore need not implicate SMC, calibration, or final search. **Fix:** retain separate last-center and production-returned endpoints, test capped cases, and compare exact model paths after index conversion. Matching move types alone is insufficient.

9. **MAJOR — timeout exclusion can bias the recovery and growth analyses.**  
   `DESIGN.md:94`, `scripts/loc_batch.py:19–30`, `scripts/make_tasks.py:19–22`. Difficult runs can disappear through wall-time kills or `.err` files; the production shell command also returns the fit command’s status even if extraction fails. Dropping incomplete observations can preferentially remove large modes or difficult searches. **Fix:** prespecify cell eligibility independently of recovery outcomes, retain a row for every scheduled seed with failure/censoring status, report completion denominators, and propagate extractor failures.

10. **MINOR — saved diagnostics omit advertised information and truncate reconstructable paths.**  
    `scripts/loc_run.py:78,111–115,130–133`; `DESIGN.md:82–83`. `truth_blocks` counts blocks containing true variables, not all blocks intersecting each truth group. Extras beyond 400 and moves beyond 500 are discarded; the existing 549-move pilot already loses part of its saved trajectory. CSG distances use undocumented numeric sentinel 99. **Fix:** save complete initial/final models and move deltas, compute block intersections per truth group, and use explicit group-membership diagnostics instead of sentinel distances.

11. **MINOR — the declared main grid is not generated.**  
    `scripts/make_tasks.py:33–49`. Only `pilot` and `pilot2` branches exist; advertised `main`/`prod` invocations silently produce nothing. **Fix:** implement the declared grids, reject unknown modes, and assert expected task counts and unique seed keys.

12. **MINOR — the “proved boundary” reference is outside the proved range.**  
    `DESIGN.md:43–44`. D3 requires α **>** 17/2; α=8.5 is still open. **Fix:** relabel 8.5 and add an α>8.5 positive-control cell.

**Overall verdict: NO-GO** for the large batch until the algorithm-equivalence, diagnostic-definition, and Q2-identifiability issues are resolved.
