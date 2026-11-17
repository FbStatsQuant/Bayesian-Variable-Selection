# LC1R — reply of the repair re-checker (Claude Opus 5.5, effort high, Claude Personal), verbatim
<!-- received 2026-11-17 via delegate_task; brief reviews/LC1R_brief_opus.md; diff a91eb7cb..113c351e -->

# LC1R: re-check of the LC1 repairs (diff `a91eb7cb..113c351e`, STATEMENT.md and lemmas/)

**Scope.** I read the diff and opened every newly cited `file:line`. Under `Scripts/SMC_BVS/core/` that was `v3_core.cpp`, `v3_engine.h`, `v3_score.h`, `v3_util.h`, `v3_blocks.h`, `v3_start.h`, `v3_fit.R`, `v3_run.R` and `v3_preprocess.R`. On the theory side it was RM2R `:39-41, :126-142, :151-152, :180`, W3-RM2 `:60-68`, RM `:50-68`, `CC_code_check.md:44-62` and READER §6 bridges `READER_VERSIONS.md:752-760`.

`git diff 4676af6 113c351e -- Scripts/SMC_BVS/core` is empty, so the code lines are those at the pin. The only commit after `113c351e` adds the LC1R brief. I wrote no files.

## 1. Resolution of the LC1 findings

| LC1-# | status | note |
|---|---|---|
| LC1-1 | RESOLVED | STATEMENT:113-114. P(𝒢⁺_n) → 1 (b⁺, RM2R `:131-132`) gives P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0. The Markov step is correct: t < ½ gives P(ε_n ≥ ½) ≤ 2Eε_n ≤ Eε_n/t = Eε_n/min(t,½), and P(ε_n > t) ≤ Eε_n/t. |
| LC1-2 | RESOLVED | STATEMENT:43-44 adds the convention and L3:19-20 adds the matching sentence. The convention is the natural reading: π lives on Ω, LS0 only scores \|S\| ≤ K, and no S₀ ∉ Ω can maximise on Ω. Wording nit in LC1R-4. |
| LC1-3 | RESOLVED | The sentence left the claim span (STATEMENT:99-100) and became §5 remark 5 (:139-142), which §5 marks "not part of any claim". Wording gap in LC1R-3. |
| LC1-4 | RESOLVED | L2:74-79 cites W3-RM2 `STATEMENT.md:60-67` via RM2R `:39-41` (which imports `:60-68`; ending at `:67` correctly leaves out the E4 line `:68`). The cited code pins match the code: `v3_core.cpp:465-476` (LS0 centre, start_mode, cap, call), `v3_engine.h:394-406` (flips, then swaps), `:392` (F, then `lex_less`), `:408` (strict improvement), `:409-414` (cap stop and no-improvement stop). E4 is now marked context only. |
| LC1-5 | RESOLVED | L3 (0.3a). The conclusion and the code line `v3_preprocess.R:111-112` are correct, but the stated reason misdescribes Setting R (LC1R-2). |
| LC1-6 | RESOLVED | L3:33-35. I checked all the cites: `v3_fit.R:129` (TRUE, exact branch), `:171` (copies `fr`), `v3_run.R:218` (the only other TRUE; grep shows no other writer), `:106` (`branch_run`), `:89` and `:102` (return through `finish`), `:78` (initial FALSE). |
| LC1-7 | RESOLVED | L3:41-44. RM2R `:151-152` is Lemma S.2 ("scorer never fails under EX-A, … yᵀy > 0"). The sentence sits in Step 1's context (a data set in 𝒢⁺_n), so S₀ ∈ 𝒯 holds there. |
| LC1-8 | RESOLVED | All eight ranges are corrected and correct: `v3_core.cpp:483-508`, `v3_engine.h:379-419`, `:381, :386, :390`, `v3_score.h:274-282` / `:271-273`, `v3_core.cpp:524-568`, `:537-555`, `:539`, `:542-547`. The new explicit-file cites in A5, B1 and Step E are also correct: `v3_core.cpp:382`, `:426-427`, `:548`, `v3_fit.R:171, :173`. |
| LC1-9 | RESOLVED | (b) is correct: `v3_fit.R:99-102`, and `v3_preprocess.R:114` returns `no_predictors` before `:106`. (c) is correct: the first offer goes in with no erasure. (a) uses exactly the citations LC1 proposed, and each is correct (`v3_core.cpp:34`, `v3_blocks.h:141`, `v3_start.h:287`, `v3_util.h:129-130`, `v3_core.cpp:554`). However, the list of sources is incomplete (LC1R-1). |
| LC1-10 | RESOLVED | L2:50. `o.islands` is read at `v3_core.cpp:396`, is `4L` at `v3_run.R:91`, and drives the loop at `:443`. Nothing in the argument needs a particular value; with ≤ 0 islands the loop is simply skipped. |
| LC1-11 | RESOLVED | L2:91-94. `CC_code_check.md:48-54` covers (a) cache hits and (b) `held`. `:55-57` covers "Other offers". The reverse direction is correct: `v3_start.h:93` (tables scored), `v3_core.cpp:426` (inherited models scored), `v3_engine.h:92` (offer only when `fresh`, i.e. after a scorer call at `:92`). |
| LC1-12 | RESOLVED | L1 (0.5) now sits before (c), and (c) and (e) both cite (0.5), so the circular reference is gone. L1 Setting and STATEMENT (C1) now carry "F real-valued". |
| LC1-13 | RESOLVED | L3 (0.1) and STATEMENT:100 cite (b⁺). RM2R `:180` lists "(a), (b⁺)" and `:131-132` gives P(𝒢⁺_n) → 1. A range carried over on the same line is slightly off (LC1R-5). |

## 2. New findings

None of these is a correctness defect. Every one is tag E.

**LC1R-1: L2:106-109 (D2, [LC1-9a]) — E.** The list of where offered model vectors come from, given as the reason they are in sorted form, misses two sources:
- **π₀ draws.** `draw_pi0` sorts at `cpp/v3_start.h:174`. It is called through `draw_start` (`cpp/v3_engine.h:108`) for the initial island particles (`:289-290`) and at `:184-185`. In the final run `init_states` is `nullptr` (`v3_core.cpp:446`), so every island particle starts here.
- **LS0's tie-DP fallback.** `mode_tie_dp` (`cpp/v3_start.h:262-269`) builds S by appending i = 0..p−1 in increasing order. It replaces the sorted enumeration result whenever the tie enumeration is truncated and `tie_dp` is on (`:303`), which is the shipped `ls0_tie_dp = TRUE`.

Both produce sorted vectors, so the premise is true. Only the listed reasons are incomplete. Inherited models are already covered, because `models_from_R` calls `to_internal` (`v3_core.cpp:320-325`).

**Fix:** add "π₀ draws sort (`cpp/v3_start.h:174`); the tie-DP fallback of `start_mode` appends increasing i (`cpp/v3_start.h:263-266`, used at `:303`)".

**LC1R-2: L3:21-22 ((0.3a), [LC1-5]) — E.** The text calls Setting R "rows i.i.d. Gaussian with a positive-definite covariance, n ≥ 3". Setting R (W3-RM2 `STATEMENT.md:52-53`) is "raw rows iid N(m_n, Σ_n), unit diagonal", with no positive-definiteness clause.

The conclusion still holds, for a simpler reason. With unit diagonal, X₁ⱼ − X₂ⱼ ~ N(0, 2) for independent rows, so a column is constant with probability 0 for any n ≥ 2.

**Fix:** "(rows i.i.d. N(m_n, Σ_n) with unit diagonal, so each column has variance 1 and, with n ≥ 2 independent rows, is constant with probability 0)".

**LC1R-3: STATEMENT:139-142 (§5 remark 5, [LC1-3]) — E.** The remark says (A1)–(A6) reach the hypotheses of RM2-R-plus "through Theorem 6's own bridges B6.1–B6.4". Those bridges cover only (T1-R), (FL-R), (L-R^b) and (W-R) (`READER_VERSIONS.md:755-758`). Setting R and (V-R) come from the identities of (A1)–(A3), which the old v1.0 sentence named and the remark has dropped.

The remark is outside every claim, so this is editorial only. **Fix:** restore "… B6.1–B6.4 and the identities of (A1)–(A3) with Setting R and (V-R) …". If wanted, the remark could also say that B6.1 and B6.3 are marked NEW, as LC1-3 suggested.

**LC1R-4: STATEMENT:44 (convention, [LC1-2]) — E (optional).** "Every statement below holds trivially for such n" claims too much for (C2)(ii)–(iv). Those parts do not involve S₀; they hold by their own proofs, not trivially. The statements that do involve S₀ are fine:
- (C1) is vacuous because S₀ ∈ 𝒯 ⊆ Ω fails.
- (C2)(i) last clause and (v) are vacuous because 𝒦_n = 𝓜_n = ∅.
- (C3)(i) is vacuous, and (C3)(ii)'s bounds have right side ≥ 1.

**Fix:** "every statement below that involves S₀, 𝓜_n or 𝒦_n holds trivially for such n".

**LC1R-5: L3:16 ((0.1), [LC1-13]) — E (optional, carried over).** The rewritten line still contains the old citation "RM0-plus (b⁺), RM2R `STATEMENT.md:128-137`". (b⁺) is RM2R `:126-134`, and `:135-137` is (c⁺). **Fix:** `:126-134`.

## 3. STATEMENT changelog row v1.1: tag verdict per change

| change | lead's tag | verdict |
|---|---|---|
| (C1) hypothesis "F real-valued on Ω (so 0 < Z < ∞)" (was "Z < ∞") | EQUAL | **EQUAL, confirmed.** Under §1's F, ϖ > 0 is finite (`v3_score.h:61-70`) and the coded m is strictly positive. So Z < ∞ ⇔ every m(S) < ∞ ⇔ F is real-valued on Ω. The admissible data sets are unchanged, and the old hypothesis already implied Z > 0. |
| §1 convention for S₀ ∉ Ω | EQUAL | **EQUAL, confirmed.** It writes down the natural extension of the imported objects: π is supported on Ω, LS0 scores only \|S\| ≤ K, and no S₀ ∉ Ω maximises on Ω. It changes nothing for s₀ ≤ K, and the extra n are finitely many under (L-feas), where every claim is vacuous or has right side ≥ 1. Strictly, (C3)(i)–(ii) now also cover n that were undefined before, but only with trivially true content, so this does not count as STRONGER. |
| (C3) preamble: reader-form sentence moved to §5 remark 5 | EQUAL | **EQUAL, accepted.** LIST-R's hypotheses and conclusions are unchanged. The removed text was a side assertion, not a hypothesis or a conclusion. This matches v1.0, which tagged inserting the same sentence EQUAL. A strict reading of the "claim span" text would call it WEAKER, because the span now asserts less, but nothing consumed or concluded changes. |
| P(𝒢⁺_n) → 1 attributed to RM0-plus (b⁺) | EQUAL | **EQUAL, confirmed.** Citation only, and correct (RM2R `:131-132`, `:180`). |
| (C3)(ii) reason for "every right side tends to 0" completed | EQUAL | **EQUAL, confirmed.** The conclusion is unchanged. The new reason is mathematically correct (§1 above). |

The diff contains no other STATEMENT change: the title line is version bookkeeping, and remark 5 is in §5, outside every claim. No quantifier in a claim span changed.

LC1R-VERDICT: VERIFIED-WITH-AMENDMENTS
