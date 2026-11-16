# LC4 reply — Claude Opus 5.5 (high), new general-purpose agent aaa6cabe8aef4e0af, 2026-11-16 ~17:54 CST (verbatim)

**LC4 review: re-check of the LC2 and LC3 repairs to T3–T10 (Claude Opus 5.5, high, new agent)**

I read the LC2 and LC3 replies and dispositions, the current STATEMENT and PROOF of T3–T10, and the v2 diffs against `1ff88651`. I checked the core at `4676af6`; `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` passes. I also read the cited sources:
- T1 PROOF Steps 3–4
- W3-SAMP STATEMENT §0–§2
- W3-START2 lines 176–189 and W3-START2-R lines 95–145 and 200–244
- W3-START §3.1 for the definition of (AL)
- AUDIT.md §4 and TRACK_B B11
- the reader Theorem 5 (A5) and bridge B5.1′ in `W3-READER/READER_VERSIONS.md`
- N9 PROOF lines 250–287
- TDP_E
- C-DLV TDP-IMPL

All paths below are relative to `Theory_work/Wave3/W3-AUDIT/track_A/`, and code paths to `Scripts/SMC_BVS/core/`.

## A. Status of each LC2 and LC3 finding

**LC2**

| # | item | result | evidence at HEAD |
|---|---|---|---|
| 1 | T3 C | RESOLVED | `T3_OPC/PROOF.md:9-10, 20-21` no longer use an inequality. The validators "have passed on a run that returns a fit". `v3_final_run` is called with no `tryCatch` (`v3_fit.R:162`), and a `stop` at `cpp/v3_core.cpp:474` is not a `NumericalFailure`, so it escapes the `try`. |
| 2 | T3 F | RESOLVED | See §B for the check of the new line. |
| 3 | T3 S | RESOLVED | `PROOF.md:67-70` defines 𝒪̄ := 𝒪° and 𝒮̄⁺ ⊇ 𝓜. The inclusion 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ 𝒦_nᶜ follows. |
| 4 | T3 E | RESOLVED | `STATEMENT.md:42` now says "same sequence of centres". |
| 5 | T4 S | RESOLVED | The only non-const `Data` writer is `data_init` (`cpp/v3_core.cpp:96`). `cpp_setup` and `cpp_start` share it by `shared_ptr`. `start_mode` reads only `D.K`, `D.logprior` (`mode_dp`) and `D.p` (`mode_tie_dp`). The `mutable` counters are at `cpp/v3_score.h:20-21`. |
| 6 | T4 E | RESOLVED | `PROOF.md:42-43` cites `cpp/v3_core.cpp:178-181`. |
| 7 | T4 E | RESOLVED | `PROOF.md:32-33`. |
| 8 | T4 F | RESOLVED | `STATEMENT.md:30` and `PROOF.md:9-10` (w(k) > 0, W_K > 0). |
| 9 | T5 F | RESOLVED | `STATEMENT.md:42-43` and `PROOF.md:62-64`. T1 `PROOF.md:129-130` does contain the (⊇) induction "to the return of `v3_calibrate`". |
| 10 | T5 S | **PARTLY RESOLVED** | The new sentence over-states the transfer for 𝒜; see finding S1. |
| 11 | T5 S | RESOLVED | `calibration_seed` (`v3_calib.R:171`) is the only seed field of the output. The seed otherwise reaches only `cpp_cal_new` (`cpp/v3_core.cpp:606`). |
| 12 | T5 E | RESOLVED | `STATEMENT.md:40-41`. |
| 13 | T10 C | RESOLVED | Every `get_holder` call on the fit path gets `ctx` or `tctx`, which come from `cpp_context` as a list with an EXTPTRSXP `ptr` (`cpp/v3_core.cpp:102`), or `setup$ptr`. The one small inaccuracy is finding E3. |
| 14 | T10 F | RESOLVED | (TDP-e) is now stated (`T9_TDP/STATEMENT.md:30-31`) and proved (`PROOF.md:23-28`); see §B. |
| 15 | T10 S | **PARTLY RESOLVED** | The X2-imp line covers only some of the implicit sources; see finding S2. |
| 16 | T10 S | RESOLVED | `PROOF.md:89-92` checks out: `v3_budgets` converts n and p to double (`v3_preprocess.R:20`), so n + p + 1 cannot overflow in R; ℓ_n ≤ 32; and 32 + 2³⁰ < 2³¹ − 1. This now agrees with T3. |
| 17 | T10 E | RESOLVED | `check_blocks` is called at `cpp/v3_core.cpp:179` and `:209`, with the rethrow at `:209`. |
| 18 | T10 E | RESOLVED | `:714`, `:538`/`:553` and `:126` are verified. |
| 19 | T10 E | RESOLVED | Citations added. D1 in binary64 holds: the progress check `v > u` is at `cpp/v3_calib.h:89`, the loop runs until u = 1.0, the pilot steps are ≥ 1/T_e or snap to 1, and T_e ≤ 4·max(1000, ℓ²) keeps φ + 1/T_e > φ in binary64. |

**LC3**

| # | item | result | evidence at HEAD |
|---|---|---|---|
| T6-1 | S | RESOLVED | `cpp/v3_engine.h:299` is `logZ = D.logm0 + st.logZbar0`. |
| T6-2 | F | RESOLVED | The quote is at N9 `PROOF.md:254-255`. |
| T6-3 | E | RESOLVED | |
| T6-4 | E | RESOLVED | `start_summary` returns `st.logZbar0` at `cpp/v3_core.cpp:198`. `v3_setup.R:73` is `start <- r$start` (`:72` is the failure return, as the disposition says). `cpp/v3_core.cpp:515` is the final run's `log_Zbar0`. |
| T6-5 | F | RESOLVED | `STATEMENT.md:35-37`. |
| T6-6 | E | RESOLVED | The comments at `cpp/v3_start.h:139, 147, 155-156` are as described. I re-derived the telescoping with s_b: the factor for block b is F_b(s_{b−1})/F_{b+1}(s_b), and the product equals F₀(0)/F_J(k). |
| T7-1 | S | RESOLVED | `ScoreCache::find` (`cpp/v3_score.h:274-282`) compares the hash and then `same()` (`:271-273`). The only insert is in `eval` (`cpp/v3_engine.h:93`), with the scorer's value. |
| T7-2 | E | RESOLVED | |
| T7-3 | E | RESOLVED | |
| T8-1 | S | RESOLVED | (A5) is defined. A small gloss problem remains; see finding E2. The definition is consistent with W3-START §3.1 ("'No leakage' is Q = S₀") and with the reader version (B5.1′: reader (A5) = (L-R⁺⁺) with Q = S₀, the hypothesis of IF-START's (T3⁺⁺)(b) route). |
| T8-2 | S | RESOLVED | |
| T8-3 | S/F | RESOLVED | The hypothesis list matches `W3-START2/STATEMENT.md:181-189` and the two substitutions at `W3-START2-R:212-213`. "Word for word" is gone. |
| T8-4 | E | RESOLVED | `v3_run.R:225`. |
| T8-5 | E | RESOLVED | |
| T9-1 | F | RESOLVED | `PROOF.md:75-78`. |
| T9-2 | F | RESOLVED | Direct proof; see §B. |
| T9-3 | F | RESOLVED, with one residual sentence | See finding E4. |
| T9-4 | E | RESOLVED | |

## B. Attempts to break the new or rewritten text

- **T3 (OPC-d), enumeration branch** (`STATEMENT.md:48-49`, `PROOF.md:72-73`). The step holds:
  - `cpp_enumerate` (`cpp/v3_core.cpp:524-556`) visits every sorted S ⊆ {0..p−1} with |S| ≤ K exactly once, because `rec` stops at |S| ≥ K (`:553`).
  - The HPM is updated by `hpm_better` (`:548`), and `fit$hpm <- e$hpm` (`v3_fit.R:123`).
  - 𝒪 on this branch is {status = "exact"} (T1 `STATEMENT.md:52-53`).
  - Under EX-A, π(S₀) > ½ makes S₀ the strict F-maximum on Ω, so Ŝ⁺ = S₀.

  One scope slip in the lemma's header is finding E1.
- **T5 (CAL-d).** Correct. It is the prefix form of T1's induction, which the cited text contains.
- **T5, upper-bounds-only paragraph.** The 𝒜 half is wrong as written; finding S1.
- **T9 (TDP-c), slack telescoping** (`PROOF.md:47-57`). Correct:
  - Each M[b−1][r_{b−1}] is finite, since the tuple (U_c)_{c<b−1} witnesses it. So d_b ≥ 0 is well defined, including j = 0 where v = M[b−1][r] exactly.
  - Σ_b d_b = M[J][k̂] − Σ_b mb[b][j_b], because M[0][0] = 0 and r_J = k̂.
  - Σ_b ρ_b(U_b) = M[J][k̂] − Σ_b d_b − Σ_b (mb − ρ). Both slacks are nonnegative, so equality holds exactly when every code is in `arg` and every edge is tight.
  - k̂ = k* follows from the strict `>` scan.

  I also confirmed `git diff 39db138 4676af6 -- cpp/v3_start.h`: the old inline DP is the same arithmetic, moved into `ModeDP`.
- **T9 (TDP-e).** Correct: M[b][0] = M[b−1][0] = 0, `logprior` is finite, `mode_tight` recomputes the same expression as `cpp/v3_start.h:217`, and the forward induction finite M[b][r] ⇒ `reach[b][r]` goes through when IN = OUT = ∅.
- **T9 fast-path cost** (`PROOF.md:67-70`). Correct:
  - Every entered call has finite M, and every tight edge into level 0 has r − j = 0. So every call's first descent reaches a counted leaf before any return.
  - After `trunc`, no new call is entered (`cpp/v3_start.h:297`).
  - Distinct leaves are distinct elements of E, so the number of calls is at most J·(number of leaves) ≤ J·min(|E|, cap).
  - A leaf costs O(p + k̂ log k̂).
- **T10, `get_holder`, X7/X8 and D1.** All hold (table above). X2-imp is finding S2.
- **T8's definition of (A5).** Sound; one gloss is finding E2.
- **Did any repair break something LC2 or LC3 verified?** No. The edits to T3 Steps 0–1 and 4, T4 ENC-b, T6 (Z), T7 Step 0, the T8 proof, T9 (TDP-b) and the T10 §1–§2 additions leave the earlier arguments intact. Every new code citation lands on the line it names.

## C. New findings

**S1 — `T5_CAL/STATEMENT.md:48-49`.**
- **The text:** "upper bounds on P(𝒜° ∩ A°), P(𝒪° ∩ A°), for events A defined by statistical state, transfer to P(𝒜 ∩ A), P(𝒪 ∩ A) since 𝒜 ⊆ 𝒜° and 𝒪 ⊆ 𝒪°".
- **What is wrong:** for 𝒪 the step holds, because T1 GW-iv gives 𝒪 ∩ A ⊆ 𝒪° ∩ A° pathwise. For 𝒜 it does not follow from 𝒜 ⊆ 𝒜°. On 𝒜 the actual and potential statistical states agree only up to the return of `v3_calibrate` (CAL-d).
- **Counterexample:** take an allocation just large enough for calibration, so the final-run guard fires in island 1 (`cpp/v3_engine.h:335`, `cpp/v3_core.cpp:451`). Let A = {S₀ ∉ ∪_r 𝓜_r} for the actual run. Then 𝒜 ∩ A can have probability near P(𝒜), while P(𝒜° ∩ A°) ≤ E[1_𝒜°(1 − π₀(S₀))^{D_r}] is small.
- **Downstream impact:** none. W3-SAMP uses potential quantities on 𝒜 (`W3-SAMP/STATEMENT.md:32-33`) and actual outputs only on {completed}.
- **Fix:** state the 𝒜 half for potential events, P(𝒜 ∩ A°) ≤ P(𝒜° ∩ A°), and for events of the calibration-time state (σ(𝓒°), using CAL-d). Actual final-run events transfer only on 𝒪.

**S2 — `T10_P1S3/PROOF.md:80-85` against `STATEMENT.md:30` and `PROOF.md:3-4`.**
- **The text:** (S.3′) says "the implicit Rcpp/R errors (X2-imp) are unreachable", and the method lists "the implicit error sources of §2" as a source of the inventory.
- **What is wrong:** X2-imp enumerates only some implicit sources on the fit path. Not covered:
  - `runtime_ptr`'s `XPtr<RuntimeGuard>` (`cpp/v3_runtime.h:30`, reached at `cpp/v3_core.cpp:411, 609, 771, 778`);
  - `as<double>(ro["cache_capacity"])` (`cpp/v3_core.cpp:610`);
  - the Rcpp argument coercions of `cpp_cal_pilot`, `cpp_cal_diag` and `cpp_build_grid` (`v3_calib.R:6, 44, 86`);
  - `v3_assemble_final`'s `do.call(cbind, …)` and terminal `data.frame` (`v3_run.R:159, 164-168`);
  - R computations in `v3_cal_tier`.

  All of these are unreachable by the same reading, but P1′ as stated is not checkable from the list.
- **Fix:** state X2-imp as a class: "every implicit Rcpp conversion, XPtr construction, name lookup and base-R shape error on the fit call graph; e.g. …". Alternatively, add the sites above.

**E1 — `T3_OPC/STATEMENT.md:37-38` against `:48-49`.** The lemma's preamble restricts it to "every valid input on the sampler branch … on {final-run status = "completed"}", but the last sentence of (OPC-d) is a claim on the enumeration branch. **Fix:** widen the preamble, e.g. "…; the last sentence of (OPC-d) concerns the enumeration branch". The title, "on every completed sampler run", could note this too.

**E2 — `T8_OVL/STATEMENT.md:15-16`.** The gloss "(no null column leaks onto the truths)" is stronger than the fixed-design form of the hypothesis. (AL) at Q = S₀ bounds an average over nulls and "does not bound the largest gain" (`W3-START/STATEMENT.md:152-157`). Only the Gaussian-row form, reader (A5) = (L-R⁺⁺) with Q = S₀ (B5.1′), is per-null. **Fix:** "(AL) at Q = S₀ in fixed design, (L-R⁺⁺) with Q = S₀ in Gaussian rows — the reader's (A5), B5.1′".

**E3 — `T10_P1S3/PROOF.md:78-79`.** "or `setup$ptr` / the calibration state" is not quite accurate. The calibration state never goes through `get_holder`: `cpp_cal_*` use `CPtr` (`cpp/v3_core.cpp:624, 658, 704, 729`), and `cpp_cal_new` gets `setup$ptr`. **Fix:** delete "/ the calibration state". Those sites belong to X2-imp.

**E4 — `T9_TDP/STATEMENT.md:35-39`.** The fast-path bound is proved, but the statement never links it to TDP-IMPL or to the delivery clause, which LC3 #3 asked for. With the shipped cap of 10⁶:
- the fast-path time 10⁶·(J(B+2) + p log p) is within O(p·Σ_b 2^{|C_b|}), since Σ_b 2^{|C_b|} ≥ p ≥ log p, at a constant factor of 10⁶;
- its storage (`choice`, recursion depth J, and `bestS`) is within O(Σ_b 2^{|C_b|} + J(K+1)).

**Fix:** add one sentence saying so, and that the whole `start_mode` call is then inside TDP-IMPL's envelope, with an explicit 10⁶ factor.

**No C or F findings.** No repair broke anything LC2 or LC3 verified.

LC4-VERDICT: T3=VERIFIED WITH AMENDMENTS; T4=VERIFIED; T5=VERIFIED WITH AMENDMENTS; T6=VERIFIED; T7=VERIFIED; T8=VERIFIED WITH AMENDMENTS; T9=VERIFIED WITH AMENDMENTS; T10=VERIFIED WITH AMENDMENTS
