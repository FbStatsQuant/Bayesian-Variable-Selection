# L4 — Theorem D (delivery reduction), Corollary D′ (joint consistency with the delivery term), Proposition F (fallback)

Status: PROVED (by this seat); R04 VERIFIED-WITH-AMENDMENTS — amendments applied (Corollary D′ pathwise proof,
Remark D.1 cutoff and wording). Uses L1 (Lemma R, Corollary R), L2 (Lemma S), L3 (grid lemmas).

## Setting
𝔐 = v3.1 + LS0 (STATEMENT.md §0); premises EX-A, EX-S, SR, OP-LS0 (cap ℓ_n = ℓ), e4, GUARD-W, IDEAL-W, MACH, CONFIG,
TDP-IMPL (the last two via Corollary R); model G; (IND-T is not used by these proofs);
n ≥ 3; declared allocation as in Corollary R. CAL is NOT assumed. 𝒰_n = no output; 𝒮ℒ_n = {status `schedule_limit`}.
For a construction c (a call of `build_grid`) write V_c for its candidate set, k_c for its tier's pilot count
(k_c ≤ T_e, Lemma 3.3), N_b^app(c) for its number of appended bisection steps, T(c) ∈ {T₀, T₁} for its tier's cap.

## Theorem D (reduction). For every n ≥ 3:
(i) 𝒰_n ⊆ 𝒮ℒ_n ∪ 𝒩_n with P(𝒩_n) = 0 (and 𝒮ℒ_n ⊆ 𝒰_n, so P(𝒰_n) = P(𝒮ℒ_n));
(ii) 𝒮ℒ_n = {calibration escalates to tier 1, and some tier-1 construction c fails};
(iii) a construction c fails iff one of: (α) N′_p(c) + N_b^app(c) > T(c) (`too_many_intervals`; appended intervals, L3 3.4(b)); (β) `non_progress`, which
     under EX-A requires ρ(u, u + (b − u)2⁻⁶⁰) < 0.90 at some step, hence sup_t Var_{q_t^{V_c}}(d) > c₀·4⁶⁰ and
     max_{V_c} d − min_{V_c} d > 2√c₀·2⁶⁰ ≈ 7.5·10¹⁷; (γ) a failed validation at a point snapped to 1 (ρ(u, 1) < 0.90
     while ρ(u, v) ≥ 0.90 at the unsnapped v ∈ [1 − 10⁻¹², 1)). Here N′_p(c) ≤ k_c ≤ T(c).
(iv) If (α)–(γ) fail for every tier-1 construction (in particular if every tier-1 V_c satisfies the dominance condition
     of Proposition 3.5(a)), the fit returns output.
Hence P(𝒰_n) ≤ P(∪_{c at tier 1} {(α) ∨ (β) ∨ (γ)}) and P(𝒰_n) → 0 iff P(𝒮ℒ_n) → 0.

*Proof.* Walk the fit (`v3_fit.R:49-144`). Entry and preprocessing: by Lemma S the statuses `invalid_input`,
`no_predictors`, `y_constant` (and spec `degenerate_n`, `unsupported_size`) occur on a null set or are excluded by
declaration. Preflight (:88-90): does not fire (Corollary R). Exact branch (:93-105): enumeration never throws (Lemma S),
the guard is not consulted on this branch, and the time/memory budget is covered (Corollary R), so it returns status
`exact` with estimates (:98-102). SMC branch: setup tables never throw (Lemma S) (:106-111). Calibration
(`v3_calib.R:135-175`): within a tier, `fail()` is reached only via `numerical_failure` (impossible, Lemma S) or
`resource_limit` (impossible, Corollary R) (:57, :80-81, :100, :112-113); so every tier returns status ok, with a grid
unless some construction of the tier failed (:82, :114, :120). The escalation preflight (:148) does not fire (Corollary
R). Therefore the calibration status is `ok` unless the final tier has no grid; if the final tier is 0, it has a grid
(L2 S.3: a tier-0 construction failure forces escalation); if it is 1 and some construction failed, the status is
`schedule_limit` (:153). This proves (ii) and that the only non-null no-output path through calibration is 𝒮ℒ_n. When
calibration is ok, `v3_frozen` accepts the grid (a successful construction: starts at 0, ends at 1, strictly
increasing — L3 Lemma 3.4) and the final run (`cpp/v3_core.cpp:388-480`) returns `completed`: its only other statuses
are `resource_limit` (Corollary R) and `numerical_failure` (Lemma S). LS0 (spec) is a capped local search from the exact
start mode (OP-LS0, e4): it reads no uniforms, scores ≤ 1 + (ℓ+1)(p + p²/4) models (centre included), ends with or without `local_limit`
(not a stop, SoP/02_method.tex:404-405), and its only stops are guard stops (Corollary R). `v3_assemble_final` then sets
`estimates_available = TRUE` (`v3_run.R:166`). This proves (i). (iii) is L3 Lemma 3.4(c) with Lemma 3.2: if
ρ(u, u + h) < 0.90 then c₀ < Δ(u, u+h) ≤ h² sup Var with h ≤ 2⁻⁶⁰ (b − u) ≤ 2⁻⁶⁰, and Var ≤ (max d − min d)²/4. (iv)
follows from (ii)–(iii) and Proposition 3.5. ∎

*Remark D.1 (size of (β)).* For a k-variable model, −(k/2) log(n + 1) ≤ log BF(S) ≤ ν log(n + 1) with ν = n/2 + 0.01
(1 ≤ det H_S/det(G_S + I) ≤ (n + 1)^k; (2b₀ + yᵀy)/(2b₀ + Q_S) ∈ [1, n + 1] by L2 S.2), d(S) = log BF(S) −
Σ_b log r_b(S ∩ C_b) (`cpp/v3_core.cpp:681-683`) with at most K occupied blocks, so max_V d − min_V d ≤
2(K + 1)[ν log(n + 1) + (K/2) log(n + 2)]. With K ≤ n/2 this is below 2√c₀·2⁶⁰ = 7.4846·10¹⁷ for all
n ≤ 2.277·10⁸ (n_β ≈ 2.2772·10⁸, R04 recomputation, rounded down), so (β) is impossible there. Beyond n_β this crude bound no longer excludes
(β); (β) is kept in the reduction, and its attainability on the classes is neither claimed nor excluded.

## Corollary D′ (joint consistency with the delivery term; pathwise proof after R04 #1). (The delivery-free form holds
only for the patched method of Proposition F.)
Let 𝒦_n be the event that the prescribed LS0 search — the §6.10 local search with cap ℓ_n from the exact start mode S̃₀
(e4 tie rule), viewed as a deterministic function of the data (X, y), defined on every data set whether or not the fit
delivers — scores S₀. On the classes, the cited results give P(𝒦_nᶜ) → 0 and E[1 − π(S₀ | y)] → 0. Exact sources
(Opus C1 #7): for the W1-GEN class (which covers LH with exact Gram as its instance (C5)(a)), P(𝒦_nᶜ) → 0 is W1-GEN
(C1) + (C2): on Ω_n ∩ {S̃₀ = S*} the capped search scores S₀ once ℓ_n ≥ τ(S*) − 1, which holds eventually since
τ(S*) ≤ 2^{v̄} − 1 and ℓ_n = ⌈log₂(n+p+1)⌉ → ∞, under (H0)–(H2) and n ≥ n₀; for LH-iid it is W1-PXN (T) under that
ticket's hypotheses (SIZE, p_n → ∞, (OP)). (W1-GEN: D_n ≤ P(S̃₀ ≠ S*) + O(1/log n) → 0 and T03♯, Theory_work/Wave1/W1-GEN/STATEMENT.md:84-85, :99-113, lemmas/L5_assembly.md:11-16,
:31-39; W1-PXN: D_n ≤ P(LS0 misses S₀) → 0 and (P), Theory_work/Wave1/W1-PXN/STATEMENT.md:58-66,
lemmas/LS_P6_repair.md:29-35; statuses verbatim in those reports: "PROVED-CHECKED"; for LH with exact Gram the W1-GEN instance row (C5)(a) records its
input "W1-EXP Lemma 4.2 via Thm5-LH, SAME-FAMILY-ONLY", W1-GEN REPORT.md:64, and that instance-level status is
carried here). These are statements about the
data and the deterministic search; they do not involve calibration.
*Claim.* 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ (for n large enough that S₀ is feasible, |S₀| ≤ K).
*Proof.* On a delivered SMC fit, OP-LS0, e4 and the absence of interruption (delivery) imply that LS0 ran to completion
from S̃₀ and every model it scored joined the all-scored set (SoP/02_method.tex:490-501); on the exact branch every
feasible model is scored. So on 𝒪 ∩ 𝒦_n, S₀ is scored; if moreover π(S₀ | y) > ½ then F(S₀) > F(S) for every S ≠ S₀,
and the reported HPM Ŝ⁺ — the ≻-maximum of the scored set — equals S₀. ∎
Hence, under the original (unconditioned) data law and for either calibration law,
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E[1 − π(S₀ | y)] + P(𝒦_nᶜ) → 0,  and  P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − o(1) − P(𝒰_n)
                                                                           = 1 − o(1) − P(𝒮ℒ_n)
by Theorem D (P(𝒰_n) = P(𝒮ℒ_n) up to a null set). No bound is conditioned on delivery or on calibration success, and
CAL is not used: both cited theorems list CAL among their premises, but only their data/deterministic-search clauses
are used here — W1-PXN STATEMENT.md:52-53 states that (S), (E), (T), (P) concern the data and the deterministic LS0, and
W1-GEN (C1), (C2) and T03♯ are data-level — while the CAL-bearing assembly step of those tickets is replaced by the
pathwise Claim above. (The proof uses the premises EX-A, EX-S, SR, OP-LS0, e4 as the cited theorems do.)

## Proposition F (finding: a one-line fallback removes the last path; a change to a SHIPPED component).
Suppose that whenever a tier-1 construction fails, calibration froze the tier-1 pilot schedule (φ₀, …, φ_k) as the
grid (instead of returning `schedule_limit`) — or, alternatively, the last successful construction of that tier when
one exists (it also starts at 0, ends at 1, is strictly increasing, has ≤ T₁ intervals and passes `v3_check_grid`, by
L3 Lemma 3.4). Then under the premises of Theorem D, P(𝒰_n) = 0 for every n ≥ 3, and on
the classes above P(Ŝ⁺ = S₀) → 1 unconditionally.
*Proof.* The pilot schedule starts at 0, ends at 1, is strictly increasing and has k ≤ T₁ intervals (Lemma 3.3), so it
passes `v3_check_grid` (`v3_run.R:77-82`) and respects the T_e cap of the calibration contract; it is frozen before any
final randomness (it is a function of streams 0–9). The rest of the proof of Theorem D applies verbatim with 𝒮ℒ_n = ∅
(the stage cap also keeps Lemma R's resource bounds). The consistency conclusion follows from Corollary D′, whose proof
does not depend on the calibration law. The fallback keeps the contract's T_e cap but need not satisfy the candidate
grid's restricted-ESS property; an implementation should keep the tier budgets, inherited models and the frozen-record
hash, and label the grid source as a fallback (R04). ∎
This changes the calibration law (a shipped component), so it is reported as a finding, not made (Wave1C protocol,
"Method-side changes"). The not-yet-shipped components (LS0, e4 tie fallback) have no influence on `schedule_limit`.
