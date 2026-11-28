# LC2 reply — Claude Opus 5.5 (high), fresh general-purpose agent a99e76252c16f7275, 2026-11-16 ~17:31 CST (verbatim)

## LC2 review: T3 (OPC), T4 (ENC), T5 (CAL-C), T10 (P1/S.3)

I read the four STATEMENT and PROOF pairs, the T1, T2 and T9 statements, every cited source span, and the whole core at the pin. `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` passes. I checked every code citation in the four proofs against the code myself. Unless a finding below says otherwise, each citation lands on the right line and says what the proof claims.

---

### T3 · Lemma OPC — **VERIFIED WITH AMENDMENTS**

These points hold in the code:
- **Status:** status is assigned only at `cpp/v3_core.cpp:413, 451, 459, 480, 484`, and nothing sets it back to `"completed"`.
- **LS0 call:** the gates at `:453` and `:465` lead to `start_mode(st, 1000000, o.ls0_tie_dp)` at `:469`. The only `PH_LS0` search is at `:476`, with `emit_centre = true`.
- **Search rules match the abstract search:**
  - flips at `v3_engine.h:394-399`, with additions skipped when |C| = K;
  - swaps at `:401-406`;
  - ties go to the lexicographically smaller index list (`:392`); internal and original index order agree because `orig` is increasing;
  - a move requires a strict improvement (`:408`); the cap, plus one further scan, is at `:409-410`; the stop is at `:413-414`.
- **No uniforms and no interruption:** there is no `vs->u` call and no guard check inside `local_search`.
- **Every LS0 model is offered:** this follows from CC2 together with `v3_ledger.h:104-113` and `:84-94`.
- **Reported HPM:** `out$hpm <- led$hpm$model` at `v3_run.R:142`.

1. **C** — `T3_OPC/PROOF.md:20-21` (and `:9`).
   - **What fails:** "the range check at `:474` passes since ℓ_n + |S̃₀| ≤ ℓ_n + K < 2³¹ − 1" is asserted without any hypothesis. Line `:9` likewise asserts that the `v3_run.R:96-97` validation passes. This contradicts T10 and the INVENTORY erratum, which treat X7 and X8 as reachable on large inputs and excluded only by A:IDEAL-W⁺ or 𝔇.
   - **Fix:** neither inequality is needed. On {status = "completed"}, both validators passed, because each failure is an R error and returns no fit object. Alternatively, cite 𝔇 or A:IDEAL-W⁺ explicitly.
2. **F** — `T3_OPC/STATEMENT.md:45-48` and Not claimed `:52`.
   - **What fails:** RM-0(b) (`W3-RM/STATEMENT.md:168-169`) uses 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ on every output run. OPC-d proves it only on the sampler branch, and nothing names who covers the exact branch.
   - **Fix:** add one line. On {status = "exact"}, Ŝ⁺ is the `hpm_better` maximum over all of Ω (`cpp/v3_core.cpp:548`, `v3_fit.R:123`). So under EX-A, 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} holds trivially there.
3. **S** — `T3_OPC/PROOF.md:66-68`.
   - **What fails:** the step from {S₀ ∈ 𝓜} to [OP]'s 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ 𝒦_nᶜ needs 𝓜 ⊆ 𝒮̄⁺. 𝒮̄⁺ is never defined in T3.
   - **Fix:** define 𝒮̄⁺ as the potential run's all-scored set, and note that 𝓜 ⊆ 𝒮̄⁺ (tables, inherited models and final-run evaluations are all scored), with 𝒪̄ = 𝒪° (T1 GW-iv).
4. **E** — `T3_OPC/STATEMENT.md:42`.
   - **What fails:** "in the order of LS(…)" has no content, because the definition of LS (`:25-30`) fixes no scan order.
   - **Fix:** either define the scan order in LS (flips with j ascending, then swaps (j ascending) × (l ascending)) or say "with the same sequence of centres".

### T4 · Lemma ENC — **VERIFIED WITH AMENDMENTS**

These points hold in the code:
- **Data fields:**
  - `D.K = min(p, n/2)` (`v3_score.h:40`);
  - log w(k) = −log 2 − log C(2p−1, k), which equals the BB(1, p) per-model prior;
  - `logprior` (`:61-70`).
- **Inverse maps:** `blk`/`pos` at `v3_start.h:79-80`.
- **Tables:**
  - `logr` length and value 0 at code 0 (`:85-95`);
  - nothing is skipped at `:92`, since B ≤ K for n ≥ 3;
  - `codes_by_size` order and `logprof` length (`:107-113`).
- **One object:** the same `g->st` is used at `:392, 410, 611, 704`, always as `const Start&` on the fit path.

5. **S** — `T4_ENC/STATEMENT.md:36-38` (ENC-b).
   - **What fails:** "One object, never changed" covers only the `Start`. `start_mode` also reads `st.D->K`, `->logprior` and `->p`, and the `Data` is shared with the context holder (`cpp/v3_core.cpp:275`).
   - **Fix:** add that `Data` is written only by `data_init` (`cpp/v3_core.cpp:96`). Every later access is `const Data&` or `const Data*`, and the only fields that change are the `mutable` counters at `v3_score.h:20-21`, which `start_mode` does not read.
6. **E** — `T4_ENC/PROOF.md:40-41`.
   - **What fails:** "The only non-const writers of a `Start` are …" leaves out `cpp_tables` (`cpp/v3_core.cpp:178-181`, a local `Start` passed to `build_tables`).
   - **Fix:** add it. It is a different object and is off the fit path, so the conclusion is unaffected.
7. **E** — `T4_ENC/PROOF.md:31-32`.
   - **What fails:** "enforced again by `check_B`" overstates what `check_B` does. It bounds B, not |C_b|; |C_b| ≤ B comes from BLK-b.
   - **Fix:** say exactly that.
8. **F** — `T4_ENC/STATEMENT.md:29-30` and `PROOF.md:45-47`.
   - **What fails:** TDP_E's (H1) (`C-ENG/lemmas/TDP_E.md:29-32`) requires "`D->logprior` of length K+1 finite". ENC-a gives the value λ(k) but never states that it is finite.
   - **Fix:** add "finite (w(k) > 0)".

### T5 · Lemma CAL-C — **VERIFIED WITH AMENDMENTS**

These points hold in the code:
- **Where streams are seeded:** only `cpp/v3_core.cpp:241` (off the fit path), `:444` and `:596`.
- **Where `vs` is set:** `:627` and `:668`, with sid ∈ {0, 5} ∪ {1..4, 6..9}.
- **Tiers:** e ∈ {0, 1} (`v3_calib.R:149-158`).
- **Final-run settings:** they come from `b` and `frozen$tier` (`v3_run.R:88-104`); the final streams are 9 + r.
- **Bounded computation (Step 3):**
  - each pilot step advances φ by at least 1/T_e or reaches 1 (`v3_calib.h:32-45`);
  - a diagnostic grid has at most T_e intervals (`:94`);
  - at most ℓ rebuilds (`v3_calib.R:85`);
  - the round and step uniform counts are as cited.

9. **F** — `T5_CAL/STATEMENT.md:40-41` and `PROOF.md:62`.
   - **What fails:** "on 𝒜 the actual calibration record equals 𝓒° (T1 GW-iii)". GW-iii is stated only on 𝒪, and on 𝒜 ∖ 𝒪 (for example, a final-run guard stop) it says nothing. GW-iv gives only the event identity 𝒜 = 𝒜° ∩ G, not equality of the record.
   - **Fix:** cite the prefix form of T1's argument: on G, every Boolean evaluated before `v3_calibrate` returns is FALSE, so the execution matches P° up to that point. Better still, have T1 state this as a clause (for example GW-iii′: "on G the statistical fields of the actual `v3_calibrate` output equal 𝓒°").
10. **S** — `T5_CAL/STATEMENT.md:46-47`.
    - **What fails:** "conclusions P(𝒜° ∩ ·), P(completed ∩ ·) transfer to the actual 𝒜 since 𝒜 ⊆ 𝒜°" is true only for upper bounds, and only for events defined by statistical state (T1 GW-iv). Lower bounds, statements of the form P(𝒜 ∩ good) → P(𝒜), and conditional statements P(· | 𝒜) do not transfer.
    - **Fix:** write "upper bounds on P(𝒜° ∩ A°), P(𝒪° ∩ A°) transfer to P(𝒜 ∩ A), P(𝒪 ∩ A)". Also flag any W3-SAMP clause stated as a lower bound or conditionally on 𝒜.
11. **S** — `T5_CAL/STATEMENT.md:33` vs `PROOF.md:28-33`.
    - **What fails:** the statement writes 𝓒° = Ψ(X, y, U⁽⁰⁾, …, U⁽⁹⁾), yet the proof admits the seed enters as `calibration_seed` (`v3_calib.R:171`). That field is statistical under T1's definitions and part of "every statistical field" of the output.
    - **Fix:** write Ψ(X, y, seed, U⁽⁰⁾, …, U⁽⁹⁾), with the seed entering only through that label, or exclude `calibration_seed` from 𝓒°.
12. **E** — `T5_CAL/STATEMENT.md:39`.
    - **What fails:** "remaining inputs (`setup`, seed)" leaves out the `runtime` argument of `cpp_final_run` (`v3_run.R:227`).
    - **Fix:** name it as operational (the guard; its Boolean is FALSE in P°, per T1).

### T10 · Re-audit P1/S.3 — **VERIFIED WITH AMENDMENTS**

These points hold in the code:
- **Exit map:** every row's re-located pin line matches the code, including C3 `:649-650, 695-696, 717-721`, E1 `:637, 673-680, 451` and E2 `:645, 692, 459`.
- **v3_fit returns:** the statuses at `v3_fit.R:89, 100, 117, 122, 135, 155, 171` match the code.
- **D2 is unreachable:** a tier with no grid sets `fired`, so with e = 0 the loop either escalates or stops with `resource_limit`.
- **D1 is unreachable at the pin:** a fallback is always recorded at tier 1 when `grid_fallback` is on. A successful construction starts at 0.0, has v > u enforced at `v3_calib.h:90`, and ends exactly at 1.0. The pilot schedule increases strictly by the three cases. Since `v3_calib.h:90` enforces the progress check and the loop ends exactly at 1.0, this also holds in binary64, so "under EX-A" understates it.
- **Invariants (ii)–(v), (vi′), (vi″), (vii):** each checks out. In (iv), `hpm_mech` is always ≥ 0, so `"none"` never reaches `mech_index`.

13. **C** — `T10_P1S3/PROOF.md:38-40`.
    - **What fails:** "Every other `stop`/`throw` in the core is off the `v3_fit` call graph" is false for `cpp/v3_core.cpp:18` (`get_holder`'s stop). It is on the call graph through `cpp_setup`, `cpp_cal_new`, `cpp_final_run`, `cpp_cut_group`, `cpp_dup_components`, `cpp_numerical_routes`, `cpp_time_scores` and `cpp_enumerate`, and it is mapped to no row.
    - **Fix:** add it as an X2 invariant. It is unreachable because every call passes either `ctx` (a list with `ptr`, `cpp/v3_core.cpp:102`) or `setup$ptr` (an EXTPTRSXP).
14. **F** — `T10_P1S3/STATEMENT.md:31` and `PROOF.md:74`.
    - **What fails:** the proof quotes "E ≠ ∅" from T9 (TDP-b), but TDP-b (`T9_TDP/STATEMENT.md:97-98`) states only the return value. Neither E ≠ ∅ nor the root check `feasible()` with IN = OUT = ∅ is stated, so the argument is circular as cited.
    - **Fix:** prove it inline or add it to T9. The argument:
      - k̂ ≥ 0, because M[J][0] = 0 and `logprior` is finite;
      - a tight path from (J, k̂) to (0, 0) exists, because each finite M[b][r] is assigned from v(b, r, j) for some j, `mode_tight` recomputes the identical expression, and `-ffp-contract=off` applies;
      - `allowed[b][j]` holds with IN = OUT = ∅ whenever `arg[b][j]` is nonempty. That is true for j = 0 (code 0, value 0) and for every finite `mb[b][j]` (finite tables by ENC).
15. **S** — `T10_P1S3/PROOF.md:3-5`, against the claim at `STATEMENT.md:22-23` ("every error ending `v3_fit`").
    - **What fails:** the method greps only explicit `stop`/`throw`. Implicit runtime errors on the fit path are not inventoried:
      - Rcpp `as<>` and name-proxy lookups (`cpp/v3_core.cpp:396-404, 436-439, 494, 499-503`);
      - `XPtr` construction (`:624, 658, 704, 729`);
      - R `data.frame`/`rbind` in `v3_stage_table`/`v3_bind_records` (`v3_run.R:50-64`, `v3_fit.R:163`).
    - **Fix:** add an X2 line arguing them unreachable (fields always present, types fixed by construction, column sets identical), or restrict P1′ to explicit sites plus X1, X3 and X5.
16. **S** — `T10_P1S3/PROOF.md:75-76` (and `STATEMENT.md:30`).
    - **What fails:** "X7, X8 are reachable on very large inputs" holds only under IDEAL-W's unbounded-integer reading of n and p. For R-representable inputs (nrow, ncol ≤ 2³¹ − 1):
      - ℓ_n ≤ 32 ≪ 10⁶;
      - ls0_ell + ⌊n/2⌋ ≤ 10⁶ + 2³⁰ < 2³¹ − 1.

      So neither fires on the shipped path.
    - **Fix:** qualify the claim by the idealisation and note that both are dead for actual R inputs. This also reconciles T10 with T3's justification (finding 1).
17. **E** — `T10_P1S3/PROOF.md:51`.
    - **What fails:** "`check_blocks` is called only in `cpp_start`" is wrong; it is also called in `cpp_tables` (`cpp/v3_core.cpp:179`). Both are off the call graph. The rethrow at `:209` is also missing from the off-graph list.
    - **Fix:** correct both.
18. **E** — `T10_P1S3/PROOF.md:62-63` (invariant vi).
    - **What fails:** the caller list for `v3_score.h:230` leaves out `cpp_cal_V` (`cpp/v3_core.cpp:714`; leader-store models, in Ω), `cpp_enumerate` (`:538`; recursion stops at |S| = K, `:553`) and `cpp_time_scores` (`:126`, k clipped to K).
    - **Fix:** add them.
19. **E** — `T10_P1S3/STATEMENT.md:36-37`.
    - **What fails:** `C-DLV:Prop-F` and its status quote carry no file:line.
    - **Fix:** cite `Theory_work/Wave1C/C-DLV/REPORT.md:70` and `lemmas/L4_delivery.md:79-93`.

LC2-VERDICT: T3=VERIFIED WITH AMENDMENTS; T4=VERIFIED WITH AMENDMENTS; T5=VERIFIED WITH AMENDMENTS; T10=VERIFIED WITH AMENDMENTS
