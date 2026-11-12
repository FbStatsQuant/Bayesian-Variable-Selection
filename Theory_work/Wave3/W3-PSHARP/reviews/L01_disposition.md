# L01 disposition (statement lock, gpt-6.1-sol high, codex; review `L01_statement_lock_sol.md`)

Verdict: LOCK-WITH-AMENDMENTS (0 FATAL / 1 MAJOR / 2 MINOR / 0 NIT). All applied → STATEMENT v1.1, **locked**.

| finding | disposition |
|---|---|
| M1 (B3 overclaims: growing s₀ alone does not rule out r_n; needs the A2 witness hypotheses and log p ≍ log n; reviewer's counterexample with log p = o(log n)) | **Applied.** B3 rewritten with the reviewer's wording; a sentence added that no obstruction is claimed when log p = o(log n); the every-design part now states its domain s₀ ≤ min(K − 1, p/2). |
| m1 (c(p, s₀)/(s₀+1) → ½ needs p → ∞) | **Applied** (line 93). |
| m2 (p = ⌊n^a⌋ = n at a = 1 is infeasible) | **Applied**: p = min(n − 1, ⌊n^a⌋). |
| Remarks in the body (no label): Lemma S items 3–4 need s₀ + 1 ≤ K when S = S₀; "any p" in the (W-sph) example must be read with the logarithmic restrictions; the E δ_n reading in Remark A3(ii) needs P(𝒜_nᶜ) = O(r_n) | **Applied** as wording (tags [L01]). |

Reviewer's own checks (recorded, not relied on as proof): derived Lemma S, Proposition A (both witnesses), A1, A2,
Corollary B (B1, B2), Proposition C items 1–3; numerics: 6,576 one-step comparisons, exact cutoff tail for every
n ∈ [200, 20000]. No claim was found false other than the B3 wording.
