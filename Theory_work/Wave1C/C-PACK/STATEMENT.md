# C-PACK — STATEMENT (targets of the five items)

Ticket C-PACK, Theory Wave 1C (brief from Theory HQ, 2026-11-08). Lead: Claude Opus 5.5.
**LOCKED v2 (2026-11-08)** after statement-lock review R30 (`reviews/R30_statement_lock_sol.md`, LOCK-WITH-CHANGES; all 8
required changes applied verbatim, disposition in `reviews/R30_disposition.md`). v1 → v2 = R30's replacement texts.
Aliases: `W1/` = `Theory_work/Wave1/`; `SoP/` = `Theory_work/State_of_Project/sections/`; `CODE/` =
`Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`. `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`.

## Item 1 — N3-USE (e4 is not needed for consistency)
T1.a (audit) Catalogue every occurrence and substantive use of e4, N3 and start-mode tie selection in W1-PXN, W1-GEN and
M5(b1-LH), including T38 Theorem b1 and Corollary b1-LH (`NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md`). Distinguish
method definitions and premise lists from deductions, and distinguish start-mode ties from LS0 move ties and
reported-HPM ties. The target audit conclusion is that the consistency deductions requiring identification of the LS0
centre with a reference R use that identification only on {π₀(R) > 1/2}, where R is feasible and deterministic given X
(and the fixed model parameters). Any use outside this event must be listed and resolved or retained explicitly as an
obligation.

T1.b (Lemma UM) Use the instance, feasible set Ω_K, objective f and normalized start law π₀ of `W1/W1-N3/STATEMENT.md`
§1. Under its (H1), (H2), (H3), (H4), if argmax_{S∈Ω_K} f(S) = {R}, then `start_mode(st, cap).S = R`. In particular this
holds on {π₀(R) > 1/2}. The implication follows from N3(c) with N = 1 (also from N3(a)); it requires cap ≥ 1 and does not
require a false truncation flag.

T1.c (Lemma UM-FP) Under W1-N3 (H1), (H2-FP), (H3), (H4), let ĝ(S) be the coded `st.log_gamma0(S)`. If
argmax_{S∈Ω_K} ĝ(S) = {R}, then `start_mode(st, cap).S = R`, by N3(e). To relate this to the mathematical objective f*,
let f̂ be the exact-real evaluation of the stored double tables, η = max_{Ω_K}|f̂−f*|, and let ε be a finite uniform bound
on |ĝ−f̂|. For feasible R, define Δ(R) = f*(R) − max_{S∈Ω_K\{R}} f*(S), with maximum of an empty set equal to −∞. The
sufficient condition FP-TAB is Δ(R) > 2(η+ε). If ε is supplied by the recursive-summation γ_k formula in I1 §3,
explicitly assume every index used satisfies ku < 1, where u = 2^−53. No claim is made that FP-TAB holds for the coded
scorer, or with probability tending to one under fixed binary64 precision.

T1.d (premise replacement) Supply a source-by-source replacement of the mathematical e4 obligation by W1-N3(c) +
uniqueness, together with the retained integration premise: LS0 starts from and emits the coded `start_mode(st, cap).S`,
on correctly encoded tables (H1), with cap ≥ 1 and execution hypothesis (H4). Under the consumers' existing EX-A, their
events {π₀(R) > 1/2} give uniqueness and T1.b identifies that centre with R. Supply the replacement text and affected
locations as patches inside C-PACK. LS0 integration remains an implementation obligation for C-ENG. T1.c is a separate
conditional native-binary64 start-mode result; it does not replace EX-A elsewhere in PXN, GEN or M5(b1-LH), and does not
establish those theorems for floating-point execution.

## Item 2 — LH-iid without the two candidate inputs
T2 (LH-iid without the two candidate inputs) Work in precisely the common LH-iid family of `W1/W1-PXN/STATEMENT.md` §1 and
`W1/W1-GEN/lemmas/L6_instances.md` (b): fixed g, c, v, ρ, ψ_i, nonzero signal coefficients and σ² with the restrictions in
PXN §1; iid Gaussian raw design rows, independent Gaussian noise; 18 ≤ p_n = gG_n ≤ n^A, p_n → ∞, fixed A ≥ 1; and
eventual SIZE g ≤ B_n < 2g for the actual method's B_n and complete-linkage/top-down-cut/next-fit partition. Retain GEN's
method, implementation and random-design hypotheses, including its uniform constants and deterministic envelopes.
Compare Theorem B as used by GEN with PXN's repaired Theorem R, including partition definitions, parameter domain, SIZE
onset and exact-branch convention. Prove that repaired (R-c), or the independently checked route (R′), supplies
P(blocks ≠ groups) → 0. Replace the [CONC] correlation-rate use by [CONC′]'s δ_n = 32√(2(A+1)log n/(n−1)), giving uniform
operator error O(log n)δ_n = o(1). Combine this with GEN's fixed-signal SLLN arguments for the remaining components of 𝒞_n
and retain GEN's separate verification of its other X-event components. Conclude GEN (C5)(b) under the joint law of
(X,ε), without assuming candidate Theorem B or [CONC] as additional inputs. "Unconditional" means removal of these two
input conditions, not removal of GEN's remaining assumptions or a delivery claim. Record any domain mismatch explicitly
and prove an extension or state the resulting common-domain restriction. Deliver Lemma I2 and exact citation/replacement
patches.

## Item 3 — dedicated checks of W1-GEN Lemma SEL (L6(d)) and L8 (C1′)
T3 One fresh Codex gpt-6.1-sol (xhigh) line-by-line check of each, plus falsification numerics; fixes as patches in
`patches/` referencing the original files (Wave1 files are not edited); any repair is independently re-checked; an actual
counterexample triggers the protocol's stop-and-report rule.

## Item 4 — Song–Liang corollaries
T4.a `SONG_LIANG_MAP.md` maps Song & Liang (2015) Thm 1–2, Cor 1, Thm 3, thresholded ξ_q, Thm S, Thm 4/Cor 2, Conditions
3/5 and §6 to our corresponding result or explicit gap. Each entry records the original conclusion and hypotheses actually
inspected, our regime, important differences, verbatim status and source location. Inspect the online supplement for
Thm S if accessible; otherwise mark its exact statement/hypotheses NOT INSPECTED and compare only the MAP-consistency
description in the main paper. Selection consistency does not supply their Hellinger/predictive theorem, exponential
probability rates, exponential-p regime, or algorithmic equivalence. Thm 4/Cor 2 is referred to C-MIS.

T4.b Define π to be the exact D0 posterior, PIP_j = π(j∈S), and δ_n = 1−π(S₀), with π(S₀)=0 outside Ω. For every n, prove
max_j|PIP_j−1{j∈S₀}| ≤ δ_n and max_{j∈S₀}(1−PIP_j)+max_{j∉S₀}PIP_j ≤ 2δ_n (maxima over empty index sets are zero). Any
attainment example must state its feasible support and is a sharpness example among probability laws on Ω, not a claim
that a D0 posterior generated by data attains equality. When S₀∈Ω, prove the uniform bound sup_{h:Ω→[0,1]}|π(h)−h(S₀)| ≤
δ_n. If δ_n = O_P(r_n), r_n→0, then these posterior errors are O_P(r_n); {j:PIP_j>q_n}=S₀ with probability tending to one
when r_n=o(min(q_n,1−q_n)); exact MPM and every exact-posterior MAP/HPM are consistent. Here HPM in this clause means the
posterior maximiser, distinct from the method's best-scored reported model.

Instantiate r_n=√(log n/n) only under all T03♯ hypotheses R1, G, R, SE_λ(j₀), SE_w(m♯_n;g₀), and BM-∞ or BM(c>c₀), as
defined in the TH09 card, under its fixed-design noise law; or under all W1-PXN (P) hypotheses with its joint data law.
Any further random-design instance must exhibit the required uniform design events and envelopes. Without beta-min,
retain the other hypotheses of T03♯'s large-signal clause and obtain only max_{j∈J_n(c)}(1−PIP_j) ≤ π(S⊉J_n(c)) =
O_P(√(log n/n)), with J_n(c) and c>c₀ as in TH09; no specificity or full-support recovery follows from that clause alone.

Reported summaries retain their own premises and statuses. Quote M1(i)'s status verbatim, "(h), (i): PROVED (by this seat,
unchecked)"; retain its T03♯ hypotheses, osc d ≤ D*=O_P(1), declared summaries, implementation premises and pending IND-T
extension audit. Its logarithmic stacking R′_n=4⌈log₂(n+p+1)⌉ is for a fixed finite declared list, and does not assert
simultaneous sure screening over growing p_n reported PIPs. Quote separately the card's larger stacking configuration if
used for a growing declared list. W1-N1 gives the islandwise evidence-weighted bound under its named premises on the
successful-calibration/island-existence event; it does not establish consistency of pooled shipped R′=4 PIPs.
Reported-HPM consistency remains joint with output, with no delivery claim.

SL2 is conditional on M4(b),(c), exact score ordering, a positive-capacity store updated as top_c(T_old∪S_added), truth
discovery with output, and δ_n=O_P(r_n) under the chosen law: P(O∩{max_j|PIP^T_j−1{j∈S₀}|>2δ_n})→0; consequently the same
probability with threshold t_n tends to zero whenever r_n=o(t_n). State the input statuses verbatim; store-restricted PIPs
are distinct from the sampler's reported PIPs. Misspecification (Song–Liang Thm 4/Cor 2) is routed to C-MIS and is not
proved here.

## Item 5 — PXN consolidated supplement
T5 Produce a consolidated supplement in `item5_PXN_consolidated/` for every clause (R),(S),(E),(T),(P),(C),(K) of
`W1/W1-PXN/STATEMENT.md` v2, with its superseding §5 notes, as mapped by FINAL_PROOF.md and REPORT.md. Apply E-1..E-22 and
every later council/sweep correction recorded by that baseline. Include the definitions, hypotheses, repaired arguments
and dependency-status ledger needed to read the proof without consulting API-PXNGAP PROOF.md for omitted steps; explicitly
name any retained external theorem inputs. Preserve all method/integration premises, exact-branch convention, onsets,
joint events, rate and cost qualifications, and exclusions. Provide a clause/repair-to-location manifest. One fresh Codex
xhigh fidelity check compares the consolidated text against this complete baseline for omissions, strengthened claims
and changed premises. Expository additions are allowed; C-PACK's new e4 and LH-iid replacements are separately identified
addenda with their own review status, not silently incorporated as council-passed PXN claims.

## Not claimed
No delivery claim (P(𝒪) → 1); no floating-point guarantee for the coded scorer; no Hellinger/predictive contraction; no
exponential-p result; no consistency theorem for the shipped (R′ = 4) pooled reported PIPs; no status upgrade of any input.
