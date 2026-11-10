# LB — the rate n^{−1/2} cannot be beaten (deterministic lower bound; W3-POST)

Status: **PROVED (by this seat, unchecked)** — new in council round C1 → C2 (prompted by C1 seat B, F2). Check record
[C2B-N6]: council C2 seat A (`../reviews/C2_council_astra.md`, gpt-6-astra high) checked every proof step (correct;
reproduced `lb_check` exactly); seat B (`../reviews/C2_council_opus.md`, Opus 5.5 high) checked it line by line
(correct; adversarial minimum ratio 1.00005 at n = 10⁴). Domain counterexample (p = s₀): `../numerics/lb_domain_out.txt`. Notation of
`../STATEMENT.md` §0; [P1], [P3] as there.

## Proposition LB
Let n ≥ 3, any standardised design X with p ≥ 2, any data y (the coded π of STATEMENT §0), and any S₀ ⊆ [p] with
1 ≤ s₀ < p and s₀ + 1 ≤ K. Put δ := 1 − π(S₀). Then, deterministically,

  δ ≥ 1/(1 + √(n + 1)).

In particular, under any law, 1 − π(S₀) ≥ (1 + √(n+1))⁻¹ for every n with s₀ + 1 ≤ K: no rate o(n^{−1/2}) holds for
the coded target under any design or signal condition. Theorem 1's rate √(log n/n) is therefore sharp up to the factor
√(log n).

## Proof
Fix j ∉ S₀ and S := S₀ ∪ {j} ∈ Ω (|S| = s₀ + 1 ≤ K). With the common factor of m(·) cancelled,

  π(S)/π(S₀) = [w(s₀+1)/w(s₀)] · (D_{S₀}/D_S)^{1/2} · ((2b₀ + Q_{S₀})/(2b₀ + Q_S))^{ν}.

(i) Prior: w(s₀+1)/w(s₀) = (s₀+1)/(2p−1−s₀) ([P1] `lem:prior`(b)).
(ii) Determinant: D_S/D_{S₀} ≤ n + 1 ([P3] `lem:det`, first part, no eigenvalue condition; also directly: by the Schur
complement, D_S/D_{S₀} = [1 + (n+1)uᵀ(I − P_H)u]/[1 + uᵀ(I − P_A)u] with u = x_j, P_H = (n+1)X_{S₀}H⁻¹X_{S₀}ᵀ,
P_A = X_{S₀}(G_{S₀}+I)⁻¹X_{S₀}ᵀ; since I − P_H ⪯ I − P_A (eigenvalues 1/((n+1)λ+1) ≤ 1/(λ+1)), the ratio is ≤ n + 1).
(iii) Fit: Q_S ≤ Q_{S₀} ([P1] `lem:spec`(d): adjoining a column cannot increase Q), so the last factor is ≥ 1.
Hence π(S) ≥ π(S₀) r with r := (s₀+1)/((2p−1−s₀)√(n+1)). Summing over the p − s₀ choices of j (disjoint models, none
equal to S₀): δ ≥ (p − s₀) r (1 − δ). The map p ↦ (p − s₀)/(2p − 1 − s₀) is nondecreasing for s₀ ≥ 1 (derivative
∝ s₀ − 1 ≥ 0), so at p = s₀ + 1 its value 1/(s₀+1) is its minimum and (p − s₀) r ≥ 1/√(n+1). Thus
δ ≥ (1 − δ)/√(n+1), i.e. δ ≥ 1/(1 + √(n+1)). ∎

## Remarks
1. The bound uses no noise law, no design condition and no signal condition: it is a property of the coded prior and
   ridge score (per-variable Occam factor ≥ (n+1)^{−1/2}, prior multiplicity (p − s₀)·(s₀+1)/(2p−1−s₀) ≥ 1).
2. Numerics E0 (`../numerics/post_exact_out.txt`, p = 10): median δ√n ≈ 2.1–2.6, consistent with the bound
   δ√(n+1) ≳ 1 and with order n^{−1/2} at fixed p.
3. Whether the additional √(log n) is attained when p = n^A (sum over p null additions with e^{χ²/2} weights) remains a
   **conjecture** (ASSUMPTION_MAP, sharpness record item 4).
