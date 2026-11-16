# READER_DELTA.md — W3-PSHARP-R (draft v0.4, 2026-11-16, post-CP3, HQ items 1–6 of 11-16; rebased on W3-READER §3 section 0.3 @e20d287f; RIDER_RULES §5, PROTOCOL_v4 H6)

For HQ → W3-READER. Read-only source: W3-READER `READER_VERSIONS.md` at commit e20d287f, §3 "Theorem 3 — The rate cannot
be improved" (section version 0.3, lines 314-372), and §1 Theorem 1 (lines 84-112) for the named cases. Nothing here is
written in W3-READER's folder. v0.3 is frozen in this ticket's council manifest (`READER_DELTA.md`, MANIFEST fdfd4562…);
this v0.4 lives in `reviews/post_cp3/` and supersedes it for W3-READER. Master claims: `W3-PSHARP-R:AE`,
`W3-PSHARP-R:A2C` (`STATEMENT.md` v1.1 of this ticket), each "PROVED (by this seat, unchecked)" in its proof file and
council-passed (R2, MANIFEST fdfd4562…, sol 9.5 PASS, opus 9.2 PASS), **pending recorded acceptance**; on top of
`W3-PSHARP:A`@1.0.0 and `W3-PSHARP:B`@1.0.0 ("PROVED-CHECKED; council R2, MANIFEST 4513e05a…"). New bridge B3.8:
`reviews/post_cp3/BRIDGE_orth_thm1.md`.

## 1. Current reader text (W3-READER `READER_VERSIONS.md` @e20d287f, §3, section version 0.3, lines 314-372)
(b) (`:325-334`) *(Orthogonal or Gaussian null columns.)* Assume (S1), s₀ fixed, **p → ∞**, ‖Xθ*‖² ≤ nM and
‖θ*‖² ≤ nM′ with fixed M, M′, and either (N-orth) … or (N-gauss) … and p ≤ n^A. Then
  1 − π(S₀ | y) ≥ (1 − o_P(1)) (s₀ + 1) √(log p/(πn)).
Consequences (`:336-344`, one paragraph, for sequences with s₀ ≤ min(K − 1, p/2) [S1-F5]): rates from (a); "By (b) with
p = n^a, the factor √(log n) is attained. On the two witness sequences … the rate √(log n/n) is exact (conditional on
Theorems 1 and 2) [S1-F6]. On a general design only the order n^{−1/2} of part (a) is proved as a lower bound; a matching
lower bound … in expectation, under a floor on S₀ ∪ {j}, is open (post-freeze rider POST2-R1) [H5-6, S3-N4]." Why each
assumption (`:346-350`). Honest limits (`:363-364`): "the expectation form of (b) for every p (sharp2 rider T12) is not
yet proved".

## 2. What changes
1. (b) gains an **expectation** display valid for **every p** (bounded p allowed); "p → ∞" moves to the in-probability
   display only.
2. A headline sentence (HQ wording, H5 card 8): the rate of Theorem 1 cannot be improved under its assumptions, in
   expectation, for every p, on orthogonal or Gaussian null columns. Never "on every design".
3. The consequences paragraph becomes four numbered remarks: (i) what is attained where, with the **named cases** of
   exactness (in expectation: fully orthogonal designs, every p ≤ n − 1, via new bridge B3.8; in probability: the two
   current sequences); (ii) growing s₀; (iii) the critical scale (body remark, not headline); (iv) what is open.
4. "Why each assumption" gets the corrected mechanism sentence (R1 erratum: the sum of truncated fit factors, not their
   maximum).
5. Honest limits and status lines updated: proved and independently checked (council R2), pending recorded acceptance.

## 3. New reader text (proposed)

(b) *(Orthogonal or Gaussian null columns.)* Assume (S1), s₀ fixed, ‖Xθ*‖² ≤ nM and ‖θ*‖² ≤ nM′ with fixed M, M′, and
either (N-orth) or (N-gauss) (as now). Then, for every p with s₀ < p (bounded or growing),
$$
\mathbb E\big[1-\pi(S_0\mid y)\big]\ \ge\ (1-o(1))\,(s_0+1)\,\frac{2(p-s_0)}{2p-1-s_0}\,\sqrt{\frac{\log\!\big(p\sqrt n/(s_0+1)\big)}{\pi n}},
$$
and, if moreover p → ∞,
$$
1-\pi(S_0\mid y)\ \ge\ (1-o_P(1))\,(s_0+1)\sqrt{\frac{\log p}{\pi n}}.
$$

*In words (headline).* The rate of Theorem 1 cannot be improved under its assumptions: on orthogonal or Gaussian null
columns, E[1 − π(S₀ | y)] ≥ c·(s₀ + 1)·√(log n/n), for every p. Here c > 0 depends only on s₀, and does not depend on s₀
when s₀ ≤ p/2. The √(log n) bounds hold on these null-column designs only; on every design only the order n^{−1/2} of
part (a) is proved.

*Remarks.*
(i) *What is attained where.* By (a), for true models with s₀ ≤ min(K − 1, p/2), no design gives a rate faster than
n^{−1/2}; π(S₀ | y) → 1 requires s₀ = o(√n); the rate √(log n/n) requires s₀ = O(√(log n)). (Without the size
restriction (a) is false: e.g. S = [p] with p = 2.) By (b), on orthogonal or Gaussian null columns, the factor √(log n)
is present **in expectation for every p**, bounded p included (with p = n^a the constant is √((a+½)/π)), and **in
probability whenever log p ≍ log n**. The rate √(log n/n) of Theorem 1 is exact in the following named cases:
- **in expectation**, on fully orthogonal designs (all columns mutually orthogonal, any p with s₀ < p ≤ n − 1, bounded or
  growing) with fixed nonzero coefficients: these designs satisfy the assumptions of Theorem 1 and of the expectation
  display in (b), so
  E[1 − π(S₀ | y)] is of exact order √(log n/n), with constants depending only on s₀, the coefficients and the noise
  variance (conditional on Theorem 1);
- **in probability**, on fully orthogonal designs with p = min(n − 1, ⌊n^a⌋) and on raw designs with i.i.d. N(0, 1)
  entries and p = ⌊n^a⌋, both with fixed nonzero coefficients (conditional on Theorems 1 and 2).
The extra √(log n) in expectation at bounded p comes from rare large gains of a single extra variable, not from the
number of competitors.

(ii) *Growing s₀.* Keep the energy and coefficient bounds of (b), let all columns outside S₀ be null columns of type
(N-orth), or of type (N-gauss) with the columns in S₀ and the coefficients fixed (nonrandom), and let s₀ ≤ p/2 grow with
n. Then a posterior mean error E[1 − π(S₀ | y)] of order √(log n/n) forces s₀ to stay bounded, for every p.

(iii) *Critical scale (orthogonal null columns only).* Keep the energy and coefficient bounds of (b) and (N-orth), let
p → ∞ and let s₀ grow with s₀/p → 0 and (s₀ + 1)√(log p/(πn)) → λ ∈ (0, ∞). Then π(S₀ | y) ≤ e^{−λ} + o_P(1).

(iv) *What is open.* On a general design only the order n^{−1/2} of part (a) is proved as a lower bound; a matching lower
bound E[1 − π(S₀ | y)] ≳ √(log n/n) under a floor on S₀ ∪ {j} is open (post-freeze rider POST2-R1). When
log p = o(log n), nothing is claimed **in probability**: the in-probability display gives only order √(log p/n), and
whether the √(log n) is present in probability there is open. On raw Gaussian designs the matching upper bound **in
expectation** is open (Theorem 2 is an in-probability statement). Whether the constant of the expectation display is
attained is not proved.

*Why each assumption* (replaces the (b) sentence at `:348-350`): the witness conditions make the one-variable supersets
behave as independent χ²₁ competitors; for the expectation display a single such competitor already suffices (its heavy
upper tail gives the √(log n)); for the in-probability display p → ∞ competitors are used (the sum of their truncated fit
factors gives the √(log p)); energy and coefficient bounds keep the variance posterior on scale. These are witnesses, not
claimed necessary.

## 4. Honest limits (replaces `:363-364`)
"The √(log n) lower bounds hold on the two witness designs only; on every design only order n^{−1/2} is proved (part (a)).
Exactness in expectation is shown on fully orthogonal designs only. Whether the constant of the expectation display is
attained is not proved." Status line: "the expectation display, remarks (ii)–(iii): proved and independently checked
(council R2) — pending recorded acceptance". (Note for HQ, not reader text: numerically the expectation constant looks
attained at fixed p, `numerics/ae_fixed_p_out.txt`.)

## 5. Bridges

| # | bridge | mark | detail |
|---|---|---|---|
| B3.3 | (N-orth), s₀ fixed ⇒ (W-orth-E) with 𝒩 = [p]∖S₀ | NEW one line (council-checked inside R2 as READER_DELTA v0.3) | (N-orth) gives N = p − s₀ ≤ n − 1 − r₀, so p ≤ 2n and (log p)² = o(n) (`STATEMENT.md` §2) |
| B3.4 | (N-gauss), (S2) p ≤ n^A, s₀ fixed ⇒ (W-sph-E) | NEW one line (as B3.3) | (log p)² ≤ A²(log n)² = o(n); (r₀ + 1) log(pn) ≤ (s₀ + 1)(A + 1) log n = o(n); any number of null columns ≥ 1 |
| B3.5 | expectation display ⇐ Cor A1-E (`STATEMENT.md:74-84`) | EXISTS, council-passed (R2), pending recorded acceptance | display = A1-E main line; under (N-gauss) via the random-(X_{S₀}, θ*) clause (`STATEMENT.md:70-72`) with P(𝒜_n) → 1 (= 1 if the energy and coefficient bounds are assumed surely). Headline constant: (s₀ + 1)·2(p − s₀)/(2p − 1 − s₀) ≥ 2 for s₀ ≥ 1, ≥ (s₀ + 1)/2 for s₀ ≤ p/2, and ℓ_n ≥ ½ log n (B3.8 step 3) |
| B3.6 | in-probability display needs p → ∞ | EXISTS-CHECKED | `W3-PSHARP:A`@1.0.0, Cor A1 (PARENT STATEMENT :71-73), unchanged |
| B3.7 | remark (ii) ⇐ Cor A2-E(ii) (`STATEMENT.md:86-92`); remark (iii) ⇐ A2C (`STATEMENT.md:94-100`) | EXISTS, council-passed (R2), pending recorded acceptance | A2-E: all nulls, s₀ ≤ p/2, s₀ + 1 ≤ K, fixed (σ*², M, M′), and (N-orth) or (N-gauss) with X^r_{S₀} (hence θ*) deterministic; (log p)² = o(n) from (S2) or from p ≤ 2n. A2C: (N-orth), p → ∞, s₀/p → 0, Λ_n = (1 + o(1))(s₀ + 1)√(log p/(πn)) → λ |
| B3.8 | fully orthogonal designs, fixed nonzero coefficients, s₀ < p ≤ n − 1 ⇒ Theorem 1 (A1)–(A6) and the hypotheses of the expectation display of (b) (the in-probability display needs p → ∞ in addition); hence exact order √(log n/n) in expectation, every such p | NEW, `reviews/post_cp3/BRIDGE_orth_thm1.md`; informal read L05 (low effort; GAP, repaired), Sol line check L06 high (`reviews/post_cp3/L06_bridge_sol.md`): CORRECT-WITH-FIXES, C 0, its one S (scope of Claim 2, p → ∞) applied verbatim | (A1)–(A6) with A = 1, θ̄ = max|θ*_j|, φ₀ = 1, g₀ = 1, second form of (A6); upper half carries Theorem 1's master status (row 1.1) |

No internal ids appear in §3's reader text; (N-orth), (N-gauss), (S1), (S2), (A1)–(A6) are W3-READER's own labels.
