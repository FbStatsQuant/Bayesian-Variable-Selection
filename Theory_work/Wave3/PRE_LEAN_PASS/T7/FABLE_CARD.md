# T7 Fable card: Thm 4, omitted variables (`W3-MISR` R′, MIS(i), (i′), (ii); `W3-MISR-R` CorG-min, CorGb-plus, CorH-plus, CorH-U)

Inputs: packet; Astra (FLAWS-FOUND, 3 local points, all in the reader, with evidence trail). Snapshot: `origin/theory/PRE-LEAN` c91ef664.

**Verdict:** no flaw in the masters or in the presented Theorem 4. No recorded statement is affected. Two reader sentences each need one phrase (T7-1, T7-2); T7-3 is already answered by a registered lemma outside Astra's packet.

## 1. Rulings

| Point | Ruling | (a) Kind | (b) Recorded STATEMENT affected? | (c) Exact fix |
|---|---|---|---|---|
| **T7-1** Example at `READER_VERSIONS.md:466-470`: "(A0) holds" needs σ²_𝒞 > 0 | AGREE | Unstated hypothesis in a reader example. The master has it: CorG-min allows σ² ≥ 0 and requires σ² + τ² > 0 (`W3-MISR-R/STATEMENT.md:57-60`). | No (reader prose) | Replace "then (A0) holds with" by "then (A0) holds, provided the $\sigma^2_{\mathcal C}$ below is positive (for instance $\sigma^2>0$), with". |
| **T7-2** Remark at `:480-482`: "For a fixed design the contraction needs only that the posterior mass of S₀ tends to one …" | AGREE | Wording: "needs only" omits two premises of CorH-plus, the Gaussian model for the responses and the size conditions (SZ). Both are implicit in context, but the sentence claims sufficiency. | No (reader remark) | Replace "For a fixed design the contraction needs only" by "For a fixed design, under the same Gaussian model for the responses and (A1), the contraction needs only". |
| **T7-3** Bridge B4.1 at `:537` has no explicit constant | **OBJECT** | Neither | No | No change needed. Optional pointer in the B4.1 row: "(`W3-READER:R1@1.0.4`, `lemmas/R1_set_sizes.md` B4.1)". |

Reasons:
- **T7-1.** Astra's example is correct: an omitted column equal to a candidate with ε = 0 gives a zero Schur complement and a deterministic response.
- **T7-2.** I checked CorH-plus (a′): it assumes κ_n in the floor-only class (size conditions, energy, floor on S₀) under the Gaussian contrast law at v, plus δ_n → 0 in probability. Astra's variance-mismatch example leaves that model, so it shows an unstated premise, not a wrong result.
- **T7-3.** B4.1 is a registered claim with a written proof: for s ≤ K and every n ≥ 3, s + max(j₀, m♯_n) ≤ 3(A+1)(s+1)·log n. That is explicit and stronger than the "for all large n" the reader row asks for. Its m♯_n branch is B1.3, which the T4 walk recomputed. The file was outside Astra's packet.

## 2. Correctness (focused; Astra's trail covers the chain)

Nothing further. I checked the reader statement against CorGb-plus:
- (A0) gives the CorGb-plus setting with no explicit omitted columns (bridge B4.0); (A2) covers its sets by B4.1; (A3) is the "→ ∞" branch of its signal condition.
- The display is E δ_n ≤ C·r_n + (2 + 2k_n)·n⁻² + n⁻¹ for n ≥ n*, which is O(√(log n/n)); the HPM bound is twice that. n* depends on the sequence, as the master says, so the reader's O(·) form is the right one.
- The registry conditions (W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P) are disclosed in the reader's master block; I found none hidden.

## 3. Lean readiness (ranked; no item changes a statement)

1. **Theorem 4 as a corollary of the T4 Lean headline at unit noise.** MIS(i) is `W3-POST2:C` applied to (x, β/√v, σ*² = 1) after two deterministic reductions: posterior invariance under y ↦ a·1 + c·y (Lemma R′), and the rescaling of the class conditions by v.
   - Gain: no new probabilistic work; uniformity in v is free. Cost: R′ is Level-1 algebra on the closed-form score.
   - Named axioms: only those of T4.
2. **Make the fixed-design MIS(i) the Lean statement; derive the reader theorem** through bridges B4.0–B4.2, importing B4.1 from `W3-READER:R1` (explicit for n ≥ 3).
   - Gain: one event layer instead of two.
3. **Random-design layer (CorGb-plus) as "bound on a design event, plus its complement".** E δ_n ≤ C·r_n + P(𝒜_nᶜ).
   - Named axioms: the two conditional inputs C-MIS:GDb and C-MIS:Prop-P (they are the registry conditions), and Gaussian sample-variance concentration.
4. **Example (E1) in two parts:** the Schur-complement algebra (Level 1), and "jointly Gaussian and uncorrelated implies independent" as a named axiom unless Mathlib has it (not checked). Carry σ² + τ² > 0 as a hypothesis (T7-1).
5. **Cor H clauses:** the (KL) identity for two normals is deterministic (Level 1) and the Hellinger part reuses Lemma D0 from T3.
