# C-GROW — Main theorem and proof map

Statement: STATEMENT.md v2.4 (R08 sweep fixes; locked v2; v2.1 piecewise AR(1) relevance set (R04); v2.2 wording (R05); v2.3 extension
(C5)(c) random-design AR(1) (L6, checked R06/R07)).

## Theorem GROW (reported-HPM consistency with a growing relevance set)

Fixed-design Gaussian model G, standardized design, fixed s₀ ≥ 1, p ≤ n^A; the shipped score/prior/blocks of SMC-BVS
v3.1 with LS0 run under **method requirement MR1** (LS0 cap ℓ_n + |S̃₀|), and the named implementation premises
(EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, e4 [N3 OPEN], complete scans; IND-T and the c₄ search when R′ > 4). Suppose
(H0) (the T03♯ hypotheses) and, for a deterministic set 𝒫_n of nulls with Q = S₀ ∪ 𝒫_n of size O(log n):
(G1) feasibility (|Q| ≤ K and either Q = [p] or K ≥ 2|Q| + 32s₀ + 1); (G2) a Gram floor on Q ∪ {l} for every l;
(G3) on the method's blocks: within-block SE, every truth block-visible given any subset of its block (TV), every
variable outside Q block-negligible given any subset containing its block's truths (NEG(η), η < (√(2A+1) − √(2A))²);
(G4) either |𝒫_n| ≤ (1 − δ₀) log n, or the add directions over the lattice [S₀, Q] number at most p·n^{o(1)}.
Then D_n ≤ P(sandwich fails) + P(NAᶜ) + P(TLᶜ) → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and
liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n). Under |𝒫_n| ≤ (1 − δ₀) log n the production cap ℓ_n suffices.
Mechanism: w.p. → 1 every start-mode maximiser lies between S₀ and Q; on the lattice [S₀, Q] no addition improves
F (NA) and no truth-removing move improves F (TL); then LS0 deletes the extras one at a time — exactly |S̃₀ ∖ S₀|
moves (GEN used the sufficient upper bound 2^{v̄} − 1 and a bounded 𝒱 containing the centre).
Instances: AR(1) with exact Gram (fixed ρ ≠ 0, separated truths, any p ≤ n − 1; relevance envelope of radius
⌈log n/(2 log(1/|ρ|))⌉ around the truths); **AR(1) with iid Gaussian rows** — the study generator's S2 design —
with p ≤ n^A including p ≫ n (L6, proved under the joint law); and S5's population covariance at fixed p = 100
(diagnostic layout, illustration).

**Where the theorem has content (council R10 F1).** For fixed p (or p growing slower than about log₂ n) the
production run eventually enumerates all models (SoP `02_method.tex:167`), and T03♯ alone then gives the conclusion.
Theorem GROW's content beyond T03♯ + enumeration is the regime p ≫ log n: (C5)(a) with growing p ≤ n − 1 and
(C5)(c) with p ≤ n^A.

**Remark (R10 S1, not adopted as a change of premises).** L4 and L6.1 use e4 only through "the emitted LS0 centre is
some maximiser of γ₀ on Ω" (the sandwich holds for every maximiser), so the N3 tie-rule invariant is not needed for
this theorem; e4 is kept in the premise list verbatim, and HQ may weaken it.

## Proof map

| Claim | Content | File | Check record |
|---|---|---|---|
| L0 | score expansion / Gaussian events for sets of size O(log n) | L0_toolkit.md | R03 Sol: VERIFIED (reviews/R03_L0L1L2_check_sol.md) |
| (C1) | deterministic lattice descent on NA ∩ TL; capped-search bookkeeping | L1_descent.md | R03 Sol: VERIFIED (reviews/R03_L0L1L2_check_sol.md) |
| (C2) | P(TL) → 1; P(NA) → 1 under (G4-χ) / (G4-dir) | L2_NA_TL.md | R03 Sol: VERIFIED-WITH-AMENDMENTS (2), applied (reviews/R03_L0L1L2_check_sol.md, R03_disposition.md) |
| (C3) | centre sandwich (size ladder; truths in; junk out) | L3_sandwich.md | R02 Sol xhigh: VERIFIED (reviews/R02_L3_check_sol.md) |
| (C4) | assembly with [OP], M5(0), T03♯, MR1 | L4_assembly.md | R04 Sol: VERIFIED-WITH-AMENDMENTS (1), applied (reviews/R04_L4L5_check_sol.md, R04_disposition.md) |
| (C5) | AR(1) exact Gram; S5 fixed p | L5_instances.md | R04 Sol: VERIFIED-WITH-AMENDMENTS (2–7), applied (reviews/R04_L4L5_check_sol.md, R04_disposition.md) |
| (C5)(c) | AR(1) with iid rows (study S2), p ≤ n^A incl. p ≫ n: sandwich, NA, TL under the joint law | L6_random_AR1.md (author: parallel prover, Codex Sol) | R07 Sol xhigh: VERIFIED (reviews/R07_L6_check_sol.md); R06 Opus high (cross-family): VERIFIED-WITH-AMENDMENTS (A1–A9 presentation), applied (reviews/R06_L6_check_opus.md, R06_R07_disposition.md) |
| (C6) | frontier: random-design S5/factor designs; factor designs with p ≫ log n; finite-n onsets | REPORT | — |

Falsification numerics: numerics/SUMMARY_DIAG.md (D1–D4), numerics/F3_summary.md, numerics/F2_exact_tau0.txt,
numerics/SUMMARY_FALSIF.md (F1–F3, F1X), numerics/G1_summary.md (iid AR(1), p up to 2000).
