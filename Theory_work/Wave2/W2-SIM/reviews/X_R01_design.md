# X_R01 — design review (Codex gpt-6.1-sol, reasoningEffort high, delegate_task, fresh), received 2026-11-09 ~10:40 CST
# Reply saved verbatim below.

**SOUND-WITH-CHANGES**

The Bartlett data law, CS reference centre, CS deletion-excess and excursion formulas, and use of the unchanged ticket path code are sound. The planned seed tuples are distinct: I checked 1,920 main-run tuples without collisions; seed 900 is separate. Wilson’s formula and duplicate detection are correct. No FATAL finding, but the following changes are needed before interpreting a large batch.

Paths below are relative to the repository root.

1. **[MAJOR] Unequal-loading excursion statistics evaluate an invalid deletion statistic outside the current set.**  
   **Files:** `Theory_work/Wave2/W2-SIM/X/scripts/x_paths.py:119`, `:139–143`; `Theory_work/Wave2/W2-SIM/X/DESIGN.md:53–56`.

   The denominator in \(s_j(T)\) is valid for deletion candidates \(j\in T\). Replay evaluates it for every variable, including deleted variables. For the planned `unif02_09`, \(p=2000\) case, at \(T=S_0\),
   \[
   \|\ell_T\|^2+1=3.442106,\qquad \max_j\ell_j^2=4.239310.
   \]
   Thus 59 outside variables have negative radicands when \(\kappa'=1\); the actual \(\kappa'=N/\phi^2\) is close to one. A synthetic replay reproduced the square-root warning. Subsequent `.min()`/`.max()` calculations propagate NaNs, while the outer Python `max(previous, nan)` can silently retain the previous value.

   **Fix:** Compute reference deletion ranks only for current candidates. For finite loading classes, measure holes directly in the class’s fixed \(\xi\) coordinates around \(\ell_cX_T\). Remove or separately derive the global deleted-variable `s` excursion, especially for continuous loadings. Add explicit validity flags and finite-value checks; clipping the radicand would not repair the statistic.

2. **[MAJOR] Full-start records report the mode’s start size.**  
   **File:** `Theory_work/Wave2/W2-SIM/X/scripts/x_paths.py:212–226`, `:272–275`.

   `rec` receives `start_size=len(St)` and is copied into both paths. `path_part` never replaces this with the actual path’s start size. The supplied pilot therefore reports `start_size=565` for the full path at \(p=1000\). I independently reproduced a small paired run with full-start size reported as 13 at \(p=32\), despite 28 pure null deletions.

   The path and `cap_mr1` use the correct actual start, so this is a reporting defect, not an explanation for successful paths. It nevertheless corrupts start-size summaries and checks relating start size to move count.

   **Fix:** Set `rec["start_size"]=len(start)` inside `path_part`; preserve the DP size separately as `mode_size`.

3. **[MAJOR] The summary cannot detect missing experimental units, allowing failure-dependent attrition.**  
   **File:** `Theory_work/Wave2/W2-SIM/X/scripts/summarize.py:21–39`.

   Duplicate records correctly cause an error, but missing seeds, paths, cells, or failed tasks are invisible. The denominator is simply the number of surviving records. A timeout or numerical exception on difficult paths could therefore improve the apparent success rate.

   **Fix:** Reconcile against an explicit expected manifest of `(cell, seed, path_from)` units. Report missing units and task failures, check provenance consistency, and mark incomplete cells before calculating interpretable rates. Preserve the existing duplicate rejection.

4. **[MAJOR] The proposed fixed-exponent trend analysis is neither implemented nor adequately specified.**  
   **Files:** `Theory_work/Wave2/W2-SIM/X/scripts/gen_grid.py:22–30`; `Theory_work/Wave2/W2-SIM/X/scripts/x_paths.py:195`; `Theory_work/Wave2/W2-SIM/X/scripts/summarize.py:34–90`; `Theory_work/Wave2/W2-SIM/X/DESIGN.md:45–47`, `:64–72`.

   At nominal \(A=0.9\), batch 1 contains only \(n=1000,3000,10000\); the optional extension adds \(n=30000\). These are limited finite-sample comparisons. With 20 independent seeds, zero observed failures still has a Wilson upper bound of 0.161. Moreover, the promised logistic analysis is absent. The driver discards nominal \(A\), retaining a rounded realized exponent, which changes with rounding and the \(n/2\) cap.

   **Fix:** Store both `A_target` and unrounded `A_actual`, plus a cap indicator. Specify the trend estimand, uncertainty, treatment of separation, and detectable effect size; implement the analysis or remove its promise. With the present high-\(A\) coverage, describe outcomes as finite-sample evidence. Failure to detect a decline cannot establish a nondecreasing rate or an asymptotic obstruction.

5. **[MAJOR] Numerical validation does not cover the new path lengths, refresh boundary, or largest \(n\).**  
   **Files:** `Theory_work/Wave2/W2-SIM/X/DESIGN.md:11–12`; `Theory_work/Wave2/W2-FAC-X/numerics/iid_selftest.py:8–24`; `Theory_work/Wave2/W2-FAC-X/numerics/iid_core.py:203`, `:231–259`.

   The existing self-test uses \(p\le60\), so it never exercises the default refresh after 200 deletions. Its largest \(n\) is \(10^7\); the new design reaches \(10^8\) and thousands of deletions. Exact-equality tie counts do not measure near-ties or numerical uncertainty. The path output also lacks a termination reason distinguishing a stationary endpoint from the safety move limit.

   **Fix:** Add read-only validation at representative new regimes: compare gains and selected moves against fresh recomputation around refresh boundaries, near the endpoint, and where competing gains are close. Record termination reason, endpoint margins, and numerical validity. Keep the imported scorer unchanged; unresolved discrepancies should make the run numerically inconclusive.

6. **[MINOR] The conditional batch-2 start policy drops the paired full path on mode seeds.**  
   **Files:** `Theory_work/Wave2/W2-SIM/X/scripts/x_paths.py:297–301`; `Theory_work/Wave2/W2-SIM/X/scripts/gen_grid.py:30`; `Theory_work/Wave2/W2-SIM/X/DESIGN.md:71–72`.

   `mode_seeds` changes selected seeds to `"mode"`, even when `start=both`. Thus requesting mode computation on seeds 0–2 removes their full-start paths. Separately, the grid generator hard-codes 20 seeds and both starts for item A, so widening its \(p\) range does not implement the documented batch-2 policy.

   **Fix:** Generate the stated batch-2 seed allocation explicitly. Use `"both"` on selected mode seeds and `"full"` otherwise, with the expected paths recorded in the manifest.

7. **[MINOR] C2 diagnostics need explicit eligibility and scope labels.**  
   **Files:** `Theory_work/Wave2/W2-SIM/X/scripts/x_paths.py:112–119`, `:225–226`; `Theory_work/Wave2/W2-SIM/X/DESIGN.md:29–47`.

   The full path is a valid C2 experiment with \(N=\varnothing\), and pairing it with the mode path on the same data is meaningful. But a mode that omits truths or differs substantially from \(S^*(N_0)\) does not test the stated production-start C2 instance. Replay currently continues reporting theorem-style diagnostics after truth loss. Neither path comparison tests the simultaneous claim over every \(|N|\le15\).

   **Fix:** Report C1 failures separately; flag C2 eligibility at the start and each replay state. Describe full-start evidence explicitly as \(N=\varnothing\). If testing the realized-\(N_0\) path claim independently of C1 matters, add an oracle start \(S^*(N_0)\).

8. **[MINOR] Growth after normalization by `w0` is not literally a violation of the stated band scale.**  
   **Files:** `Theory_work/Wave2/W2-SIM/X/scripts/x_paths.py:100–101`, `:176–178`; `Theory_work/Wave2/W2-SIM/X/DESIGN.md:43–47`.

   The CS excursion and approximate-argmin excess are appropriate empirical counterparts. However, `w0` omits the \(n^{-1/3}\) floor, and the theorem allows an unknown \(C_0(\rho)\). Growth of excursion/`w0` alone does not establish that the full \(\varpi_n\) scaling is wrong.

   **Fix:** Also record the floor-to-`w0` ratio and normalized distances using `w0 + n**(-1/3)`. Treat these as scaling diagnostics, with the unknown constant explicit.

9. **[MINOR] The published uncertainty output falls short of the design.**  
   **File:** `Theory_work/Wave2/W2-SIM/X/scripts/summarize.py:49–51`, `:82–90`.

   Only upper Wilson bounds for final failure and non-pure paths are exported to CSV; neither appears in Markdown. The other promised binary outcomes lack intervals.

   **Fix:** Export successes, denominators, and both interval endpoints for each prespecified outcome, including C1 and cap-related outcomes. Show uncertainty in the human-readable summary.

10. **[MINOR] Unequal-loading conclusions need to remain conditional on the chosen loading arrays and signal placement.**  
    **Files:** `Theory_work/Wave2/W2-SIM/X/scripts/x_paths.py:63–74`; `Theory_work/Wave2/W2-SIM/X/DESIGN.md:50–56`.

    Continuous loadings use one deterministic array per \(p\), regenerated with seed `99+p`. Changing \(p\) also changes the four truth loadings. In alternating designs, the grid fixes positive coefficients on low-loading truths and negative coefficients on high-loading truths. These are legitimate specified cases, but they do not isolate dispersion from signal placement.

    **Fix:** Record truth loadings and state this conditional scope. If attributing behavior broadly to unequal loadings, add a small prespecified sensitivity set that reverses the coefficient/loading assignment and varies the continuous loading-array seed.
