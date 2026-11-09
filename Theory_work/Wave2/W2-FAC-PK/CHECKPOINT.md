# W2-FAC-PK — CHECKPOINT (2026-11-09, ~11:40)

**State.** Statement v3 LOCKED (R01 REJECT → v2; R02 LOCK-WITH-CHANGES → v3). Both key lemmas are written:
* **Key negative lemma (L2, Theorem NEG):** exact-Gram CS, liminf p/K > 16/15, (PB), θ̄ ≠ 0 — the start is saturated and
  the first ⌊n^β⌋ LS0 moves (any β < ½) are swaps, so LS0 with the merged cap ℓ_n + |S̃₀| (and any cap with allowance
  ≤ n^β over |S̃₀|) never scores S₀, w.p. → 1. Lemma check R03 (Sol xhigh) **pending**.
* **Key positive lemma (L3, Theorem PATH):** exact-Gram CS, K + 16s₀ + 1 ≤ p ≤ n − 1, θ̄ ≠ 0, blocks ≤ 16 — the uncapped
  LS0 path ends at S₀ (strict local max) after ≤ (1 + δ)|S̃₀| moves; static proof (gain lower bounds at every set above S₀
  + F-budget), no path dynamics. Lemma check R04 (Sol xhigh): **VERIFIED-WITH-AMENDMENTS**, applied.
* L0 (imports), L1 (start), L4 (assembly, delivery with re-charged LS0 terms, cost) drafted; L0–L2 under R03; L4 to check.
* METHOD_REQUIREMENTS.md: proposed LS0 cap rules ≥ max(ℓ_n, (1 + δ)|S̃₀|) (recommend ℓ_n + 2|S̃₀|); "minimal" = proved
  gap between n^β (fails) and δ|S̃₀| (suffices); cost ≤ ×2 on LS0 worst-case terms; operational finding: the merged
  preflight already charges ≈ 146 h at n = 600, p = 450.

**Left.** R03 + amendments; L4 check; mid-point (fresh Sol xhigh); sweep; council. P6 (full method) pending on W2-SIM R2
(local production fits infeasible). Frontiers: p ≫ n (W2-SIM R3), K < p ≤ (16/15)K for NEG, K < p < K + 16s₀ + 1 for PATH.

**Estimate.** P1–P5 should close to PROVED-CHECKED for the exact-Gram stage; the ticket as a whole will be reported as
PARTIAL relative to the brief (p ≫ n and the full-method question remain open, honestly flagged).
