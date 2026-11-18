# IMPL check — does W3-PSHARP:B imply W3-POST:Prop-LB? (reviewer: Claude Opus 5.5, read-only, 2026-11-15)

Sources (all read on `origin/main` after `git fetch`):
- **B** = `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:90-114` (v1.2.2, locked; registry `W3-PSHARP:B`@1.0.0, PROVED-CHECKED,
  `Theory_work/INFRA/registry/claims.tsv:410`), proof `Theory_work/Wave3/W3-PSHARP/lemmas/B_sparsity.md:6-27`.
- **LB** = `Theory_work/Wave3/W3-POST/lemmas/LB_rate_lower_bound.md:9-17` (registry `W3-POST:Prop-LB`@1.0.0,
  PROVED (by this seat, unchecked), `claims.tsv:346`).
- Target definitions: `Theory_work/Wave3/W3-POST/STATEMENT.md:16-34` ([W3P] §0).

## 1. Same object (prior, Ω, π, δ)

- LB uses "the coded π of STATEMENT §0" (LB:7, LB:10), i.e. [W3P] §0 (W3-POST/STATEMENT.md:18-29).
- B's notation is "Exactly [W3P] §0" (PSHARP STATEMENT.md:18), and it writes the same objects out (lines 18-22): n ≥ 3,
  s_y > 0, standardised X with ‖x_j‖² = n − 1, p ≥ 2, Ω = {|S| ≤ K}, K = min(p, ⌊n/2⌋), H_S = (n+1)G_S + I,
  D_S = det H_S/det(G_S + I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, ν = 0.01 + n/2, b₀ = 0.01, w(k) = ½/C(2p−1, k),
  π(S) ∝ w(|S|)D_S^{−1/2}(2b₀ + Q_S)^{−ν}. [W3P] has ϖ = w/W_K (W3-POST/STATEMENT.md:23); W_K cancels in π. The two
  claims are about the same π. δ_n := 1 − π(S₀) (PSHARP:22) is LB's δ (LB:11).
- In both, S₀ is an **arbitrary** subset with no truth and no law: LB:10 ("any S₀ ⊆ [p]"); PSHARP:24-25 ("In Lemma S and
  Claim B, S₀ is **any** subset"), PSHARP:92-93.
- No circularity: B's proof starts from the definition of π and uses only Lemma S(1), S(2) (B_sparsity.md:4;
  PSHARP:12-14 says no registry parent, LB included, is used).

## 2. Hypotheses: LB's domain ⊆ B's domain

LB (LB:10-11): n ≥ 3, any standardised X with p ≥ 2, any data, S₀ ⊆ [p] with 1 ≤ s₀ < p and s₀ + 1 ≤ K.
B (PSHARP:92-93): n ≥ 3, every standardised design with p ≥ 2, every data set, every S₀ ⊆ [p] with 0 ≤ s₀ ≤ K − 1.

s₀ + 1 ≤ K ⟺ s₀ ≤ K − 1, and s₀ ≥ 1 ⇒ s₀ ≥ 0. So every LB instance is a B instance. (LB's condition s₀ < p is
implied by s₀ + 1 ≤ K ≤ p, so it is redundant in both.) Both are deterministic ("deterministically", LB:11; "no law,
no truth", PSHARP:93): the quantifiers match — for every design, data and S₀, a sure inequality.

## 3. Conclusion: B's bound is at least as strong as LB's, for every admissible (s₀, n, p, K)

B gives (PSHARP:94; proof B_sparsity.md:19-22) δ/(1 − δ) ≥ 𝒪^{lb}_n ≥ c(p, s₀)/√n, c(p, s) = (s+1)(p−s)/(2p−1−s)
(PSHARP:30). On LB's domain:
1. S₀ ∈ Ω (s₀ ≤ K), and every π(S) > 0 on Ω (w > 0, D_S finite, 2b₀ + Q_S ≥ 2b₀ > 0 since Q_S ≥ 0 by
   Lemma S(2), PSHARP:38), so 0 ≤ δ < 1 and the odds form is well defined.
2. c(p, s₀) ≥ 1 for s₀ ≥ 1 (stated PSHARP:95; proof B_sparsity.md:26). Re-verified:
   (s₀+1)(p−s₀) − (2p−1−s₀) = (s₀−1)(p−s₀−1) ≥ 0 since s₀ ≥ 1 and p ≥ s₀ + 1.
3. Hence δ/(1 − δ) ≥ 1/√n, i.e. δ ≥ 1/(1 + √n) (x ↦ x/(1+x) increasing). Equivalently B's own form
   π(S₀) ≤ √n/(√n + c) ≤ √n/(√n + 1) (PSHARP:95).
4. 1/(1 + √n) > 1/(1 + √(n+1)) for every n ≥ 3. So δ ≥ 1/(1 + √(n+1)), which is LB's display (LB:13). The inequality
   is **strict**: B is strictly stronger, uniformly in p, K and s₀ (it also drops the √(n+1) → √n and keeps the factor
   c and the full sum 𝒪^{lb}_n).

The mechanism matches the source of the gain: LB uses D_S/D_{S₀} ≤ n + 1 (LB:25-27); Lemma S(1) improves this to ≤ n
(PSHARP:37, 44). Sanity: at u ⟂ col X_{S₀}, LB's own formula LB:26 gives [1 + (n+1)(n−1)]/[1 + (n−1)] = n, so n + 1 was
never attained. B's j = 1 term is exactly LB's sum over j ∉ S₀ with n in place of n + 1 (PSHARP:113-114; B_sparsity.md
Remark 1, lines 50-52), and B's further terms (j ≥ 2) are ≥ 0.

## 4. The other sentences of Prop-LB

- **LB:15-16, "under any law … for every n with s₀ + 1 ≤ K: no rate o(n^{−1/2}) holds … under any design or signal
  condition".** This is a direct consequence of the deterministic display. From B: δ√n ≥ √n/(1 + √n) ≥ √3/(1 + √3)
  > 0.63 surely, so no rate o(n^{−1/2}) under any law. Covered.
- **LB:16-17, "Theorem 1's rate √(log n/n) is therefore sharp up to the factor √(log n)".** This reads the lower bound
  next to `W3-POST:Thm-1`'s upper bound; LB does not prove the upper half, it cites it ("therefore"). Its own content
  is the lower bound δ ≳ n^{−1/2}, which B gives with a better constant: r_n / (1/(1 + √n)) = O(√log n). The comparison
  with Thm-1 is the same reading in both. Covered (as far as LB itself establishes it). (Note: this sentence is now
  superseded in strength by `W3-PSHARP:A`/Remark A3, PSHARP:79-88, which shows the √log n factor is attained on witness
  designs; that is A, not B, and is not needed here.)
- **"Can fail at p = s₀" (registry summary, `claims.tsv:346`; LB:6, `numerics/lb_domain_out.txt`).** This is not in
  LB:9-17. It is a remark about a point **outside** LB's domain, and in fact outside its stated hypotheses: p = s₀
  contradicts s₀ + 1 ≤ K ≤ p (the numerics at p = s₀ = 2, n ∈ {6, 20, 100} have K = 2 < s₀ + 1 = 3). B's hypothesis
  s₀ ≤ K − 1 excludes the same point, so B neither needs to cover it nor contradicts it. The registry records the same
  necessity for both (A:EXT-FEAS NECESSARY, `sharpness.tsv:203` and `:231`). Not a clause for the implication.
- LB Remarks 1-3 (LB:34-40) are remarks; Remark 3's conjecture is outside the proposition (settled by A, not B).

## 5. Table

| Prop-LB clause | covered by B? | how |
|---|---|---|
| Hypotheses: n ≥ 3, standardised X, p ≥ 2, any data, any S₀, 1 ≤ s₀ < p, s₀ + 1 ≤ K; coded π of [W3P] §0 | yes | Same π/Ω/prior (PSHARP:18-22 = W3P:18-29); s₀ + 1 ≤ K ⟺ s₀ ≤ K − 1; s₀ ≥ 1 ⊂ s₀ ≥ 0 (PSHARP:92-93) |
| Deterministic display δ ≥ 1/(1 + √(n+1)) (LB:11-13) | yes, strictly stronger | δ/(1−δ) ≥ c(p,s₀)/√n with c ≥ 1 for s₀ ≥ 1 (PSHARP:94-95; re-verified (s₀−1)(p−s₀−1) ≥ 0) ⇒ δ ≥ 1/(1+√n) > 1/(1+√(n+1)) |
| "Under any law … no rate o(n^{−1/2}) under any design or signal condition" (LB:15-16) | yes | Sure bound δ√n > 0.63 for n ≥ 3, from the display above |
| "Theorem 1's rate √(log n/n) sharp up to √(log n)" (LB:16-17) | yes (lower half; upper half is Thm-1 in both) | Same lower bound order n^{−1/2} with constant ≥ 1; the comparison with Thm-1 is the identical reading |
| "Can fail at p = s₀" (registry note; LB:6, not in LB:9-17) | n/a — remark, not a clause | Outside LB's hypotheses (s₀ + 1 ≤ K ≤ p excludes p = s₀); B excludes it too; no conflict |

## 6. Verdict

Every instance of Prop-LB's hypotheses is an instance of B's hypotheses (same coded π, same Ω, same prior, arbitrary
S₀, deterministic), and there B's j = 1 bound with c(p, s₀) ≥ 1 gives δ ≥ 1/(1 + √n) > 1/(1 + √(n+1)). The edge
`implies W3-PSHARP:B ⇒ W3-POST:Prop-LB` can be recorded for the whole claim (the p = s₀ sentence is a remark outside
the domain, not a clause). This agrees with the note already in `claims.tsv:410` ("j = 1 term with c(p,s0) >= 1 and
n <= n+1, on LB's domain").

IMPL-VERDICT: IMPLIES
