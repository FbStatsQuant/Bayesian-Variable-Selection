# VR1 council — seat `opus` (Claude Opus 5.5, high) — blind first read — W3-AUDIT track V, V1 (Lemma VIS)

Manifest: `MANIFEST_VR1.txt`, `MANIFEST c271cfac4cb87cdd05448fd54f9f83ee217390294cdf6844338ab30b210b7e98`;
`manifest.py verify` → `verify: OK` (run before reading). Files read: `V1_VIS/STATEMENT.md` v1.2, `V1_VIS/PROOF.md` v1.2,
`V1_VIS/CITECHECK.txt`, `track_V/citecheck.py`, `TRACK_B.md:209-233`, `track_C/RESULTS.md` (whole file, allowed),
`READER_VERSIONS.md` on origin/main (Thm 5: 565-600; Thm 6: 660-700; Thm 10: 1282-1295), `NOTATION.md` on origin/main
(155-175, plus its `## ` headings to resolve "§6"). Nothing else in `W3-AUDIT/` was opened.

## Verdict summary
The mathematics is correct. I tried to break each part and could not: (VIS-0) is the Schur complement plus
1/(Σ_V⁻¹)_{jj} ≥ λ_min(Σ_V); (VIS-a) is the standard MTP₂ / Stieltjes argument (DΓ^U D = (M_{RR})⁻¹ ≥ 0), with the
component split done correctly; (VIS-b) is exact (|⟨γ, ϑ⟩| = |γ|·dist(ϑ, ν^⊥) ≥ γ_{i(j)}·dist(ϑ, B)), B is closed by
compactness of 𝒩, and the margin c̲·δ is uniform in n **by construction**: B pools the hyperplanes of every n and their
limits, which is exactly the owner's requirement (the "Not claimed" bullet at STATEMENT:71-73 names the failure mode
of per-n avoidance correctly). (VIS-c) is right (closed + null ⇒ nowhere dense). (VIS-d) is right, including the subtle
point that countability of ℒ alone would not suffice: the proof pushes the *closure* ℒ̄ through the continuous map
L ↦ γ/|γ| on the closed set ℳ, and for stationary designs uses the one-point compactification of the gaps, where
r(d) → 0 is precisely continuity at ∞. The (VIS-e) constants are all correct (checked below). The two-route remark
(Sol's example) is correct: (VIS-a) works n by n while (VIS-b) has δ = 0 there.

One blocking finding, F-1 (gate G6): the proof remark that lists track C's designs as instances of (VIS-a) cites the
track C lines that report the **spread** placement, which track C defines as signs + − + − (RESULTS.md:24-25). For
AR(0.5) and the block designs that placement is **not** aligned (the graph of Σ⁻¹ is connected inside each block or
along the path), so it is a (VIS-b) case, not a (VIS-a) instance. The list also includes "aligned factors", which in
track C comprise three-factor designs (k = 3: D11, D13, D15) that (VIS-e) does not cover (one factor only). The lemma's
statement is unaffected; the repair is a rewording of the remark. Five E findings (non-blocking).

## Gates
| gate | result | basis |
|---|---|---|
| G1 correctness of every step | PASS | every step re-derived; numerical spot checks (below) agree |
| G2 hypotheses used = stated | PASS | PD used only in (VIS-a) and stated there; c₁₆ > 0 per n for γ ≠ 0; c̲, δ for uniformity; c_m for (VIS-d) |
| G3 no hidden assumptions | PASS | E-2 (domain of n in 𝒩) and E-1 ("all large n") are presentation, conservative or harmless |
| G4 theorems' visibility hypotheses and notation quoted faithfully | PASS | Thm 5 (A4) 581-582, Thm 6 (A3) 672-673, Thm 10 (A4) 1292, NOTATION 161-164: identical at 029bb748 and at origin/main 95e1f9cc; E-1 |
| G5 scope (uniformity in n, n ≥ n₀, PD, which designs) | PASS | margin uniform for n ≥ n₀; PD premise of (VIS-a) disclosed for Thms 5, 10 (STATEMENT:61); design classes correctly delimited |
| G6 fidelity of examples / design statements to B8 and track C | **FAIL** | F-1 |

## Claim table
| claim | verdict |
|---|---|
| V1 | ACCEPT (statement (VIS-0)–(VIS-e) and every proof step correct; lock after the F-1 rewording of PROOF.md:95-97) |

## Findings

**F-1 [F] — `PROOF.md:95-97` (Remarks, first bullet): track C's examples misattributed to (VIS-a).**
The sentence "Track C's aligned designs (IND, AR(0.5), blocks, cs, aligned factors; `track_C/RESULTS.md:63-68`) … are
instances" has two fidelity problems.
(a) The cited lines 63-67 are the **spread**-truth results ("Visibility, spread truth: yes by n = 800 in 15 designs:
IND, AR(0.5), …, both fixed blocks, …"), and track C defines spread as "study positions, signs + − + −"
(`RESULTS.md:24-25`). For AR(ρ > 0) the graph of Σ⁻¹ is a path (connected), so (VIS-a) needs all truths of one sign;
for BLK5-0.7 / BLK√p-0.5 / S6 two spread truths sharing a block need equal signs. Mixed signs violate alignment, so these
spread cases are (VIS-b) cases (track C's positive population margins, e.g. AR(0.5) pop .6, are consistent with
ϑ ∉ B). Concretely (AR(0.5), p = 8, S₀ = {1, 4, 6, 8}, ϑ = (1, −1, 1, −1), |U| ≤ 3): min over (j, U) of
|vis|/(|θ_j| Var(W_j | W_U)) = 0.504 < 1, so the (VIS-a) inequality itself fails there. Only line 68 (clustered,
"aligned") supports the remark, and only for designs with D-alignment.
(b) "aligned factors" in track C includes FAC k = 3 (D11, D13, D15; `RESULTS.md:41, 43, 45`); (VIS-e) proves the sign
pattern only for one factor (Sherman–Morrison). For k ≥ 2 the off-diagonals of Σ⁻¹ are
−ψ_l⁻¹ψ_{l′}⁻¹ λ_lᵀ(I + ΛᵀΨ⁻¹Λ)⁻¹λ_{l′}, whose signs need not be of the form −d_l d_{l′}·(≥ 0): in a random 3-factor
check with mixed-sign loadings (p = 8) no D ∈ {±1}⁸ made DΣ⁻¹D's off-diagonals nonpositive.
*Repair:* "Track C's **clustered** placements (four adjacent columns, aligned signs, `RESULTS.md:24-25, 68`) are (VIS-a)
instances for IND, AR, the equicorrelated block designs and the one-factor designs (D10, D12, D14 = cs 0.5); the
three-factor designs (k = 3) are not covered by (VIS-e). The **spread** placements (signs + − + −) of AR and the block
designs are not aligned; they fall under (VIS-b) (ϑ fixed, stationary or finitely-many-pattern designs, (VIS-d))." Keep
the B8 sentence, but see E-4.

**E-1 [E] — `STATEMENT.md:9-12`: "and all large n" is not in the quoted hypotheses.** Theorem 5 (A4) says "for a fixed
a > 0", Theorem 6 (A3) "≥ a > 0"; neither says "for all large n". The lemma delivers n ≥ n₀ (necessarily, since for
Theorems 6, 10 the floor on 16-sets only starts at 5(A + 1)(s₀ + 1) log n ≥ 16 + s₀). Harmless for the asymptotic
conclusions, but say so: "(A4)/(A3) enter only the n → ∞ conclusions, so n ≥ n₀ suffices" — or, for Theorem 6 (Σ_n PD
for every n), note that a := min(c̲δ, min_{n<n₀} margin_n) extends to every n where each margin_n > 0.

**E-2 [E] — `STATEMENT.md:26-27` vs `:39-40`, `:45`: domain of n in 𝒩.** 𝒩 is "the closure of ∪_n 𝒩_n" (all n), but
𝒩_n is "well defined by (VIS-0)" only where c₁₆(Σ_n) > 0, which the theorems give only for n ≥ n₀; (VIS-d) says "𝒩
formed over n ≥ n₀", (VIS-b) does not. Including small n only enlarges B (conservative), but where c₁₆(Σ_n) = 0 it is
undefined. *Repair:* define 𝒩 := closure of ∪_{n≥n₀} 𝒩_n throughout.

**E-3 [E] — `STATEMENT.md:53-54`: state the AR alignment explicitly for ρ < 0.** With d_l = s^l the alignment reads
sgn θ*_k = σ·s^k: one sign for ρ > 0, sign alternating with the parity of the index for ρ < 0. The brief advertises
"AR(ρ) of either sign"; writing the condition out avoids readers taking "aligned" as "same sign".

**E-4 [E] — `PROOF.md:96-97`: garbled sentence.** "B8's cs/fac-aligned/s5 cases are instances or (s5, fac2) have their
own M-matrix/explicit computations in B8" does not parse. Suggested: "B8's cs(ρ) and s5 (Σ⁻¹ with negative
off-diagonals, an M-matrix, `TRACK_B.md:225-227`) are (VIS-a) instances with D = I under P6's aligned signs; fac2 is
covered by B8's own explicit computation (`:227-229`), not by (VIS-e)." ("fac-aligned" is not a B8 label.)

**E-5 [E] — `STATEMENT.md:46-50`: (VIS-d)(i) covers more than its examples.** Growing equicorrelated blocks (track C
D07, BLK√p-0.5) have finitely many local patterns (Σ_V depends only on the block-sharing pattern and ρ), although the
blocks are not "from a fixed finite list". Worth one clause, since D07's leakage grows but its visibility is then
covered by (VIS-b)/(VIS-c).

## Score
**8.4 / 10** (C, S, F only: no C, no S, one F confined to a proof remark; the lemma's statement and proof are sound).

## Checks performed
1. `manifest.py verify` → OK for `c271cfac…7e98`.
2. F1 (block inverse) and F2 (Stieltjes ⇒ inverse-nonnegative via Neumann series; PF gives ρ(P) = s − λ_min(M)).
3. (VIS-0): bilinearity, vanishing of k ∈ U and k ∉ S₀ terms; Var(W_j | W_U) = 1/(Σ_V⁻¹)_{jj} ≥ λ_min(Σ_V); locality of Γ^U_{jk} in U ∪ {j, k}.
4. (VIS-a): DΓ^U_{RR}D = (M_{RR})⁻¹, component split (Σ block diagonal ⇒ Γ^U_{jk} = 0 across components), sign
   factorisation σd_j·Σ(nonneg). Numerical (R; p = 8, all |U| ≤ 3): AR(−0.7) and AR(0.6) with sgn θ_k = σ s^k, one
   factor with mixed-sign loadings and a zero loading, five random signed M-matrix inverses: min |vis|/(|θ_j| Var) = 1
   in every case (attained at the j-only term), as the lemma predicts.
5. (VIS-b): distance to a union of hyperplanes, closedness of B, attainment of the minimum, compact-vs-closed distance.
6. (VIS-c): countable union of hyperplanes null; closed null ⇒ empty interior; s₀ = 1 gives B = {0}, consistent.
7. (VIS-d): continuity of L ↦ γ/|γ| on ℳ (|γ| ≥ c_m), ℒ̄ ⊆ ℳ, f(ℒ̄) compact ⊇ closure of f(ℒ); (ii) (ℕ̄)^{m−1}
   countable compact, continuity at ∞ ⇔ r(d) → 0; c_m ≤ c₁₆ since s₀ ≥ 1.
8. (VIS-e): AR Σ⁻¹ tridiagonal, off-diagonal −ρ/(1 − ρ²), D-signs; min of f(ω) = (1 − |ρ|)/(1 + |ρ|) (numerically
   λ_min 0.183 ≥ 0.176 at ρ = −0.7, 0.259 ≥ 0.25 at ρ = 0.6, p = 8); equicorrelation inverse and eigenvalues;
   Sherman–Morrison one-factor off-diagonals and Σ ⪰ Ψ.
9. Sol's example: (VIS-a) margin 3/4 at both parities; U = ∅, j = 1 at r = 1/2 gives ⟨(1, 1/2), (1, −2)⟩ = 0
   (numerically 0), so δ = 0.
10. Theorem quotes: lines 581-582, 672-673, 1292 and NOTATION 161-164 identical at 029bb748 and origin/main;
    NOTATION "§6" is "Design quantities used in the assumptions" (line 151), which contains 161-164.
11. Reading for the theorems: Thm 5 (A3) (|S| ≤ 16 + s₀) ⇒ c₁₆, c_m ≥ c; Thms 6 (A5), 10 (A3) ⇒ the same for n ≥ n₀.
12. CITECHECK.txt current: recomputed the four block hashes read-only (70f13b5ab5, 04ce79c82b, 0d5122835f, d9e1d973b7) — match. Did not run `citecheck.py` (it rewrites CITECHECK.txt).
13. B8 and track C consistency of "Not claimed" (D14, D15 pop 0 = ϑ ∈ B; D18 uncountable patterns) — consistent.

## Not checked
- `CHECK.md`, `INDEX.md`, `LOG.md`, other `reviews/` files (incl. the other seat's), and the VLC1/VSL1 dispositions (blind read).
- Track C's design definitions beyond RESULTS.md (exact block structure of BLK/S6, factor loadings of D10–D15, Toeplitz
  r(d)); P6 `DESIGN.md`; B8's fac2 and s5 computations themselves.
- Lean formalisation (none in the frozen content).
- Whether the theorems' other hypotheses ((A5)/(A4) leakage etc.) are compatible with the (VIS-b) designs.

COUNCIL-VERDICT round=R1 manifest=c271cfac4cb87cdd05448fd54f9f83ee217390294cdf6844338ab30b210b7e98 seat=opus score=8.4 gates=FAIL
