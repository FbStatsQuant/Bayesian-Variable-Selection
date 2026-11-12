# L3 — Assembly of Form F: Theorem RM2-F (claim (C1)) and the containment of RM-F (claim (C4), first half)

Status: **PROVED (by this seat, unchecked)**, given the cited inputs with their recorded statuses. Ticket W3-RM2;
statement: `../STATEMENT.md` v1.3 §4. No new mathematics: this file assembles `L1_sandF_b.md`, `L2_width.md` and the
consumed claims W3-RM:RM-0@1.0.0, W3-RM:E4@1.0.0 ("PROVED-CHECKED") and SOP:TH09@1.0.0 (Theorem 1; status in
STATEMENT §5 — (C1) is **conditional on it**).

## Theorem RM2-F

Setting F, the method as coded, premises and configuration of STATEMENT §1. Assume (T1-F), (FL) = (FL-16) + (FL-Q),
(V), (L^b) = (L-size^b) + (L-feas) + (L-gain) with b < β(η, A), (BM-W) and (W).

*Proof.* (T1-F) contains ‖μ‖² ≤ Mn, p ≤ n^A, fixed s₀ ≥ 1 (GROW (H0), as quoted in RM `STATEMENT.md:91-92`).
(L-size^b) with b < β(η, A) ≤ ½ gives q = |Q| ≤ n^b, hence q log n/n → 0; (L-feas) gives q ≤ K.
* **[SAND(Q)]**: `L1_sandF_b.md`, Lemma B1 (partition-free ⇒ block-relative, for the method's partition, a
  deterministic function of the fixed X with blocks ≤ 16) and Lemma SAND-F^b.
* **[NA(Q)]**: `L2_width.md` §1, Lemma NA-W, from (F0), (FL-Q), (W).
* **[TL(Q)]**: `L2_width.md` §4, Lemma TL-W, from (F0), (FL-Q), (BM-W) and P(𝒵_n) → 1 (Lemma NA-W).
* **[POST]**: (T1-F) = (H0) ⇒ 1 − π(S₀) = O_P(√(log n/n)) (SOP:TH09@1.0.0), and 1 − π(S₀) ∈ [0, 1], so
  E[1 − π(S₀)] → 0 (bounded convergence).
* **[E4]**: W3-RM:E4@1.0.0 under its hypotheses (part of the premises of STATEMENT §1).
W3-RM:RM-0@1.0.0 (any design, any deterministic Q ⊇ S₀ with |Q| ≤ K) then gives every conclusion of (C1): on
Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛) LS0 from the coded start mode makes exactly |S̃₀ ∖ S₀| moves, each deleting an element of
S̃₀ ∖ S₀ ⊆ Q ∖ S₀ (so at most |Q ∖ S₀| ≤ n^b moves), ends at S₀ with a completed scan that finds no strict improvement,
and the cap ℓ_n + |S̃₀| is not binding (RM-0(a), with its archive corollary); and with 𝒢_n := 𝒦_n ∩ {π(S₀) > ½},
P(𝒢_nᶜ) ≤ 2E[1 − π(S₀)] + P(Sand_n(Q)ᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0, every admissible output run reports Ŝ⁺ = S₀ on
𝒢_n, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1) (RM-0(b)).
*Block-relative variant.* Lemma SAND-F^b is stated under (G3a), (V_b), (L_b) on the method's partition; the two
lattice lemmas do not involve the partition. So the same conclusions hold with (V), (L-gain), (FL-16) replaced by
(V_b), (L_b), (G3a) (and (FL-Q) kept). ∎

**The search event has an explicit bound** (not part of (C1); recorded for the report):
P(𝒦_nᶜ) ≤ P(Sand_n(Q)ᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) with P(Sand_n(Q)ᶜ) ≤ P(𝓔^blkᶜ) + 1/log n + C₂√(log n)n^{−ξ/(1+ε₂)}
(`L1_sandF_b.md` §4), P(NA(𝓛)ᶜ) ≤ exp(−(𝔴⁰_n)²/8) + P(𝓔_nᶜ), P(TL(𝓛)ᶜ) ≤ P(𝓔_nᶜ) + exp(−(𝔴⁰_n)²/8) + 3/n, for n ≥ n₀.

## Containment of RM-F (claim (C4), fixed design)

RM-F's hypotheses (RM `STATEMENT.md:178-185` with §3.1): (T1-F), (FL), (V), (L) with |Q| ≤ (log n)^κ, (L-feas),
(L-gain) with η < η_A, and (N): (N-χ), or (N-D) = (N-D)(i) + (N-D)(ii) = (BM-Q).
Claim: they imply the hypotheses of RM2-F (with the same Q and η and a suitable b).
* β(η, A) > 0 because η < η_A. Choose b ∈ (0, β(η, A)), and under (N-D) also b < ½ − h (h < ½ is the entropy
  exponent of (N-D)(i)). Then |Q| ≤ (log n)^κ ≤ n^b for large n: (L^b) holds with b < β(η, A).
* Under (N-χ) (|Q ∖ S₀| ≤ (1 − δ₀) log n): this is (W-χ) with δ₁ = δ₀, so (W) by `L2_width.md` §3 (iii), (i).
  (BM-W): d_n² ≤ 2(q + 1) + 4 log(2p) = O(log n) (Lemma d; q ≤ s₀ + log n), so (BM-W) is implied by BM-∞
  (θ*²_min nφ₀²/(σ² log n) → ∞), which is part of (T1-F).
* Under (N-D): (N-D)(i) gives a deterministic finite set 𝒰_n of unit vectors with log|𝒰_n| ≤ log p + h log n and,
  for every T ∈ 𝓛, l ∉ T, some v ∈ 𝒰_n ∩ span(X_{Q∪{l}}) with ‖u_{T,l} − v‖ ≤ ρ_n, ρ_n²(|Q| + log n) = o(log n). This is
  (W-ref) with m₀ = 1, 𝒱_n := {span(v) : v ∈ 𝒰_n}, 𝒜_n = ∅, η_n = 0, w := u_{T,l} − v ∈ span(X_{Q∪{l}}), and h + b < ½;
  so (W) by §3 (iv), (ii), (i). (N-D)(ii) is (BM-Q), which implies (BM-W) (Lemma d).
Hence RM2-F ⇒ RM-F: the conclusions of (C1) contain those of RM-F (RM `STATEMENT.md:178-185`: [SAND(Q)], [TL(Q)],
[NA(Q)], [POST] and the conclusions of RM-0). (RM-F's remark on the old cap under (N-χ) is a statement of RM-F
itself and is not re-derived here.) ∎
