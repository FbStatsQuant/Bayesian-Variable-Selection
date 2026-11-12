# W3-PSHARP — CHECKPOINT 1 (target fixed) — 2026-11-12 04:20 CST

**Locked statement:** `STATEMENT.md` v1.2 — Lemma S; Claim A (Proposition A, Corollaries A1–A2, Remark A3); Claim B
(Corollary B, B1–B3); Claim C (Proposition C).

**Reviews (both clean after fixes; no open FATAL/MAJOR).**
- L01 statement lock, gpt-6.1-sol high (blind): LOCK-WITH-AMENDMENTS, 0 FATAL / 1 MAJOR / 2 MINOR — B3 overclaimed
  (needs the A2 witness and log p ≍ log n); all applied (`reviews/L01_disposition.md`). Sol derived every item.
- K01 break review, gpt-6-astra high (blind): **no claim broken** (12 items derived independently); 0 / 2 MAJOR / 1
  MINOR, the MAJORs in the evidence layer (experiment E2 violated (E); ASSUMPTION_MAP overstated a one-step boundary
  experiment); all applied (`reviews/K01_disposition.md`).

**Target relative to the brief (dispositions).**
- (a) **Stronger than briefed — adopted.** The lower bound δ_n ≥ (1 − o_P(1))(s₀+1)√(log p/(πn)) holds on two witness
  classes: an orthogonal null block (p ≤ n − 1, as briefed) and a spherical null block independent of ε (iid Gaussian
  columns), which covers **p ≫ n** ((log p)² = o(n)). So Theorem 1's rate is exact for every p = n^a, a > 0.
- (b) Corrected reading of the brief: on every design π(S₀) → 1 needs s₀ = o(√n) and the rate r_n needs
  s₀ = O(√log n); "bounded s₀" is forced on the witness designs with log p ≍ log n. Adopted from K01 (P1): at
  s₀ ~ λ√n, limsup π(S₀) ≤ e^{−λ/2} on every design.
- (c) Counterexample with a quantitative threshold: reference cost ≫ (log n)² breaks Lemma 1a′/1a″'s conclusion.
- K01-P2 adopted ((W-sph) restriction in terms of rank X_{S₀}).
- Deferred as named open items: an upper bound of order √((1 ∨ log p)/n) when log p = o(log n); whether the witness
  condition is necessary for the log factor (one-step evidence only); the gap O(1) vs (log n)² in (c).

**Assumption readings:** `ASSUMPTION_MAP.md` (domain s₀ ≤ K − 1 NECESSARY; (E), (C) WEAKENABLE; witness conditions
are witnesses; constants in C are ARTEFACTS).

**Numerics:** (a) exact odds/Λ_n → 1.003–1.007 at n = 25600 (orthogonal); one-step odds/Λ_n medians 0.97–1.09 for
p up to 4·10⁷ (spherical). (b) 55,740 cases, min odds/bound 1.033; equality case attained. (c) π(|S| > cutoff) ≈ 1
against ≤ 3·10⁻¹³ on the control arm.

Next (pre-approved): CP2 — Sol line checks of the four lemma files, council (Sol + Opus 5.5), REPORT.
