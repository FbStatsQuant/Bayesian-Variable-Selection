# W3-DIST helper brief — PRIOR PROBE (P5) — Claude Opus 5.5, Claude Third, effort high

You are a helper of ticket W3-DIST (lead: Claude Fable 5.2). Repo clone `/home/fb31/Bayesian-Variable-Selection`.
**Write only under `Theory_work/Wave3/W3-DIST/work/prior_probe/`.** Run no git command. Start no agents. No cluster jobs.
Effort high at most. Deliver one file `REPORT.md` (≤ 3 pages + a proofs appendix), then end with a 15-line summary.
Every claim carries a label: `DERIVED (unchecked)`, `REFUTED`, or `OPEN`. Do not upgrade any status. Be critical of the
lead's preliminary readings below: they are hypotheses to test, not facts.

## Context (read these, targeted)
- Song & Liang (2015): `Papers/Core_bibliography/32_2015_Song_Liang_*.pdf`, PDF pages 4–8 (journal pp. 950–954):
  prior (6), posterior (7), Theorem 1 with conditions (8)–(14), Theorem 2, Corollary 1, Condition 2 and (16).
- The coded target: `Theory_work/Wave3/W3-POST/STATEMENT.md` §0 (prior, slab, IG, cap K) and §1 (Lemma 1a, 1a′).
- `Docs/Theory/proofs/T04_A3_contraction/STATEMENT.md` and `PROOF_v2.tex` (master theorem; how the size tail is used).
- `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md` (design-free size tail; note its weak tail in L).
- `Theory_work/Wave3/W3-POST2/STATEMENT.md` (interfaces (OS), (ADG), (DG)) and `lemmas/A_occam.md` (truncated Occam sums).

The coded posterior on models: π(S) ∝ w(|S|) D_S^{−1/2} (2b₀ + Q_S)^{−ν} on Ω = {|S| ≤ K}, K = min(p, ⌊n/2⌋),
w(k) = ½/C(2p−1, k) (BB(1,p)), H_S = (n+1)G_S + I, D_S = det H_S/det(G_S + I), ν = 0.01 + n/2, slab
β_S | S, σ² ~ N(0, nσ²(G_S + I)⁻¹) on sample-standardised columns, σ² ~ IG(0.01, 0.01) on the standardised response
(so on the response scale the IG rate is b₀ s_y², data-dependent). Truth: Gaussian noise, s₀ fixed, p ≤ n^A.

## Questions
**Q1 (Song–Liang (8)–(14) for the coded prior).** Map λ_n = r_n/P_n ↔ BB(1,p), r̄_n ↔ K, V_ξ ↔ n(G_S + I)⁻¹,
IG(a₀, b₀) ↔ the coded IG. Check each of (8)–(14) and Theorem 2's extra "r_n ≻ 1" at ε_n² = M log n / n and at
ε_n² = M log² n / n, p = n^A. Lead's preliminary reading: (11) and (14) hold for every design (B̃_n ≤ n because of the
ridge +I; B(r) ≤ r + 1 by standardisation); (9), (10) fail because r̄_n = ⌊n/2⌋; "r_n ≻ 1" fails (prior mean size O(1)).
Confirm or refute each with the computation shown. Also say which of their conditions are purely proof devices.

**Q2 (testing/sieve route with the coded prior).** With sieve {|S| ≤ m}: compute the BB(1,p) size law exactly
(lead: P(|S| = k) = ½ C(p,k)/C(2p−1,k) ≈ 2^{−k−1}), its tail, and decide whether "prior mass of the sieve complement
≤ e^{−C nε²}" and "sieve entropy ≲ m log p ≲ nε²" are compatible when log p → ∞ (lead: not compatible; the coded prior
is the boundary case κ = 1 of Castillo–van der Vaart's Beta(1, p^u) and fails their complexity-prior condition).
State precisely what fails. Separately: does the dependence of the prior on X (slab, standardisation) and on y
(through s_y) take the problem formally outside the iid framework of Jiang (2007) / Ghosal–Ghosh–van der Vaart?

**Q3 (the repair: direct conjugate route).** Fixed design, Gaussian noise, ‖μ‖² ≤ nM, coefficient bound ‖θ*‖² ≤ nM′.
Target: an exponential-form size tail. Under (DG; c_D) [D_{S₀∪J}/D_{S₀} ≥ (c_D(n+1))^{|J|} for 1 ≤ |J| ≤ m♯_n] or the
weaker (OS)/(ADG), prove or break:
  there are c > 0, C, M₀ (depending on s₀, A, σ*², M, M′, c_D) such that for M ≥ M₀ and n ≥ n₀(M):
  P( π(|S| > s₀ + C·M) > n^{−cM} ) ≤ n^{−cM}.
Lead's sketch: (a) supersets S₀ ∪ J: truncated-moment bound E[BF_J ; ‖P_{S₀∪J} e‖² ≤ τ] ≤ (eτ/(|J| n))^{|J|/2}-type
(as a_J in (OS)), then Markov at level n^{−cM}, with the truncation event at probability 1 − n^{−cM} (threshold
τ_j = (C_A j + cM) log n); (b) non-supersets S: compare with S ∪ S₀ ([T03R] (C6)/(C8) style) or note that models with
small ridge loss L_S and small size are harmless and need no mass bound; (c) the unknown variance: the factor is
((2b + Q_{S₀})/(2b + Q_S))^ν, not an exponential — find the cleanest way to get the truncated-moment bound (e.g. on the
event |‖e‖²/(Nσ*²) − 1| ≤ √(cM log n/n), or by conditioning on ‖(I − P)e‖). Identify the exact step that fails, if any,
and the assumption that fixes it. Then: what does the same argument give with **no** floor at all (lead: only
P(π(|S| > C M log n) > n^{−cM}) ≤ n^{−cM} via E[m_S / p_{θ*}] = 1 and Markov, i.e. a dimension bound of order log n)?
Is a design-free bound "Π(|S| > s₀ + j) ≤ poly(j) 2^{−j} · O_P(1)" plausible? Give either a proof idea or a
counterexample design (near-collinear columns at Gram-eigenvalue scale log n / n are the lead's suspected worst case).

## Output format (REPORT.md)
1. Table: Song–Liang condition | coded-prior counterpart | holds / fails / n.a. | one-line reason.
2. Q2 verdict with the computation.
3. Q3: statement you can support, proof sketch with every inequality explicit, the failure point(s), and the
   recommended statement for the lead's key lemma. 4. Risks the lead has not seen.
