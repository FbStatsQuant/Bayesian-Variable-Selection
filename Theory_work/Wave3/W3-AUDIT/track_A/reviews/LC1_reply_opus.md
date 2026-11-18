# LC1 reply — Claude Opus 5.5 (high), fresh general-purpose agent a003e4ec07bcd7661, 2026-11-16 ~16:39 CST (verbatim)

LC1 review of track-A lemmas T1 (GW) and T2 (BLK). I wrote no files and changed no git state. The core has no diff from 4676af6 to HEAD (`git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` succeeds). I read the code myself and checked every cited source line.

## T1 · Lemma GW — VERIFIED WITH AMENDMENTS

All three claims hold in substance. Every check site the proof lists is the complete set at the pin:
- engine.h:335
- core.cpp:459, 480, 645, 692 and 770-775
- v3_calib.R:75-76 and 157
- v3_fit.R:117

None of them draws a uniform, and every firing ends in `"resource_limit"` with estimates NA. `estimates_available = TRUE` is set only at v3_fit.R:129 and v3_run.R:218. The guard is sticky (runtime.h:25), and no later code turns a fired run back into "ok" or "completed". I also traced the R code that runs after each kind of firing (`fail`, `cpp_cal_export`, `v3_stage_table` with NULL island slots, `v3_assemble_final`'s incomplete branch). None of it can raise an R error, so a fired run does return a fit with status `"resource_limit"`. The findings below are about the definitions and the interface with downstream statements, not about a failing step.

1. **C/S** — STATEMENT:37-39 and 56-59; PROOF:3-4. `fit$peak_memory_kb` is a reported field. It comes from `/proc/self/status` VmHWM (v3_fit.R:2-7, 80) and is not in the archival list. So "every reported field equals that of P°" is false as written: this field is not reproducible even between two identical runs. The proof's premise "deterministic function of the input, the option values and the clock readings" also leaves out environment readings (`Sys.getenv`, `R.version`, v3_fit.R:56-57). Those are harmless because they sit inside `fit$preflight`. **Fix:** add `fit$peak_memory_kb` to the archival fields, and change the premise to "clock and machine-environment readings". Then show they reach only v3_fit.R:80 and 56-57.

2. **S** — STATEMENT:37-39. "Statistical state" excludes only the guard, three named fields, `*seconds*`, `fit$timings` and `tcache`. Many clock-valued variables are not named `*seconds*`, so "statistical state at every point of the execution equals P°'s" fails literally:
   - R: `t_start` (v3_fit.R:74); `t0` (:121, 133, 149, 162); `t_all`, `t_build`, `t_grid` (v3_calib.R:30, 65, 63/74)
   - C++: `t0`, `t1`, `t_all`, `stage_start`, `sec_isl`, `sec_ls`, `sec_local`, `sec_ls0`
   - `s` in `cpp_time_scores`
   - the preflight local `pf` (v3_fit.R:115, 145) and `tctx`

   **Fix:** define an operational set 𝒱_op as every variable assigned, directly or transitively, from a clock or environment reading or from a check body. Statistical state is its complement. Step 1 then becomes "no variable outside 𝒱_op is assigned from 𝒱_op except through a check outcome". That is exactly what Step 1 already argues.

3. **S** — STATEMENT:36 vs PROOF:66-67. P° is defined as "every operational check replaced by the constant FALSE", which suggests the check bodies (the preflight and the `v3_time_scores` benchmark) are dropped. Step 3 instead says "both programs execute the same statements in the same order". If P° skips the bodies, Step 3 also needs "check bodies terminate normally". That is true at the pin: `cpp_time_scores` catches `NumericalFailure` (core.cpp:134), k is clamped to ≤ K so there is no `runtime_error` (:126), and there is no `stop()` path, with MACH excluded. The proof does not say this. **Fix:** define P° as executing each check body and discarding its value, or add the termination argument.

4. **F** — CAL/𝒜 interface. Two downstream statements need GW in a form it does not yet state:
   - W3-SAMP defines 𝒜 in code terms, as `v3_calibrate` returning "ok" with the guard active (W3-SAMP STATEMENT:39-41). It also needs 𝒜 ∈ σ(𝓒) with 𝓒 a function of the data and streams 0–9 (CAL; W1-N1 STATEMENT:79). For the guarded record that fails, because the status depends on the clock.
   - The TLF uses potential-run notation 𝒪̄ in D_n and transfers bounds by intersecting with 𝒪 (TLF:74, 86).

   GW handles this only in PROOF:79-83 ("Relation"). **Fix:** add a clause (GW-iv):
   - P°'s statistical state, in particular 𝓒° and 𝒜° := {P° calibration "ok"}, is a function of (X, y, seed) alone, so CAL holds for 𝓒°.
   - Actual 𝒜 = 𝒜° ∩ {no check fires during calibration} ⊆ 𝒜°.
   - 𝒪 ⊆ 𝒪°, and P(𝒪 ∩ A) ≤ P(𝒪° ∩ A°) for every statistical event A.
   - 𝒪̄ in TLF:86 and the "potential uninterrupted record" in W1-N1:86-88 are read as P°'s.

   All of this follows from Steps 1–3 as written.

5. **S/F** — GW holds pathwise, for every sequence of clock readings. Downstream statements of the form P(𝒪 ∩ ·) need 𝒪 to be an event on a space that carries the clock, and the clock depends on the streams through run time. No premise supplies this. **Fix:** add to Not claimed: "a probability model for clock readings. If one exists (clock jointly measurable with the streams), 𝒪 is an event. Otherwise the transfers in item 4 hold as outer-probability bounds."

6. **E** — PROOF:11-20. The "every clock reading" list is incomplete. Conclusions are unchanged, since all of these are timing or guard values. Missing entries:
   - `cpp_build_grid`, core.cpp:579, 582 → `g$seconds` → v3_calib.R:73-74 (`grids[[·]]$seconds`, `t_grid`, `grid_construction$seconds`)
   - runtime.h:14, 19
   - core.cpp:789
   - engine.h:336

7. **E** — PROOF:23-26.
   - The grep claim "finds only core.cpp:459, 480" misses the `?:` checks at core.cpp:645 and 692 (`sec_ls`) and the `&&` check at v3_calib.R:75-76. All three are checks.
   - "never read by … `v3_cal_tier`" is false. v3_calib.R:40 and 132-135 read `t_grid`, `pil$seconds` and `x$seconds[["islands"]]`, but only to compute other timing fields. **Fix:** say "read only to compute timing fields".

8. **E** — STATEMENT:45-48 (GW-i) says a check reads "only" a listed set and writes "only" the guard and archival fields. Both lists are short:
   - The preflight also reads `branch`, `tier`, `ls0_worst_case` (option `v3.ls0_cap`, v3_fit.R:114) and, for exact, `b$exact_count`.
   - The benchmark reads the preprocessed (X, y) columns (v3_fit.R:12). Only `seconds_per_score` leaves it; `sink` is discarded.
   - Writes also include the local `pf`, `g$resource_limit`, and `fit$status` or the returned `status` on firing.

9. **F (optional)** — GW also discharges the TLF premise "complete scans" on 𝒪. `local_search` has no check inside it (engine.h:379-419); checks run only after a search returns (core.cpp:459, 480, 645, 692). So on 𝒪 every search scan is complete. Worth stating, since TLF:86 lists this premise next to GUARD-W.

## T2 · Lemma BLK — VERIFIED WITH AMENDMENTS

All three claims are correct.
- **(BLK-a):** `v3_isqrt` is exact. `v3_budgets(ctx$n, ctx$p)` uses n = `nrow` and p = the kept columns. `check_B` is at :146 and :274. `D.K = min(p, n/2)` is at score.h:40.
- **(BLK-b):** the tree is full binary. After each merge, rows pointing at a or b are recomputed (blocks.h:99-103), so `best[x]` is always active and different from x. The cut keeps the first node of size ≤ B on each leaf's path. In next-fit packing, the closed `cur` is nonempty because |c| ≤ B. This uses only tree structure, as the proof says.
- **(BLK-c):** `make_blocks` reads only `correlation_matrix(D)` and `D.p`, with no y and no `VariateSource`. Both branches of `v3_standardise` give (x − x̄)/s_x under EX-A, so G_jj = n − 1 and r = R̂. The Borel decision-tree argument is sound.

I found no empty or oversize block, no dependence on y or a stream, and no wrong B. Engine, tables, start law and neighbour labels all use `h->B` = `g->B` = B (core.cpp:275, 410).

1. **F** — STATEMENT:27-28. `st.blocks` is built only on runs that reach `cpp_setup`: the SMC branch, with non-constant y and C1 passed (v3_fit.R:99-103, 117, 120-133). The exact branch has no partition. Downstream treats "the method's partition" as a function of X for every X (C-GROW:65-67; W3-RM:46-48; the start mode in 𝒦_n). **Fix:** define C(X) := `make_blocks`(D(X), B(n, p)) as a map on the whole setting, which the BLK-c proof already shows is a function of (n, p, R̂). Note that the coded run computes it only on that path.

2. **F** — STATEMENT:22-23 (Setting). The lemma assumes non-constant columns. Under W3-RM/RM2 Setting R (Gaussian rows), that holds only almost surely, and "X-measurable" also needs the map defined on the null set. **Fix:** add one line: under Setting R, columns are non-constant a.s. (n ≥ 2); extend C to the null set by any Borel choice; X^r ↦ X is continuous on the non-constant domain. Then BLK-c gives σ(X)-measurability and independence from ε.

3. **S/E** — STATEMENT:41-42. A "Not claimed" bullet makes a positive claim: "In binary64, (BLK-a), (BLK-b) hold verbatim". The PROOF never argues it. It is true:
   - n ≤ 2^31 − 1, so ⌊√n⌋ ≤ 46341 and the squares in `v3_isqrt` are exact.
   - The BLK-b argument uses only that a ≠ b, that `best` is active and the size arithmetic, and these hold whatever the comparisons return, NaN included.

   **Fix:** add these two lines to the PROOF, or reword the bullet as unproved.

4. **E** — STATEMENT:8-10. The registry's `C-GROW/STATEMENT.md:61` is stale; the "Blocks" bullet is at :65-67. Cite :65-67 directly instead of "the bullet after :61".

5. **E** — PROOF:59-61 ("Use downstream") cites only the final-run engine (core.cpp:410). Row 3.6 also depends on the same `st` in:
   - the calibration engine (core.cpp:611)
   - `cpp_cal_V`'s `st.comp` (core.cpp:714)
   - LS0's `start_mode(st, …)` (core.cpp:469)

   Cite all of them.

6. **E (code note, not a lemma defect)** — core.cpp:144 comment says "1 <= B <= 20", but `B_MAX = 16` (:145) and `check_B` enforces 16. The lemma correctly relies on `check_B` and `v3_budgets`.

LC1-VERDICT: T1=VERIFIED WITH AMENDMENTS; T2=VERIFIED WITH AMENDMENTS
