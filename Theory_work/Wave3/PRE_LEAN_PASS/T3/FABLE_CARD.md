# T3 Fable card: domination transfer (`W3-DIST:P6`, DIST-C deterministic clauses, Cor-C), Hellinger reduction (`W3-DIST:H`), Lemma D0 (`W3-POST2:D`)

Inputs: packet; Astra (FLAWS-FOUND, 2 points, with evidence trail). Snapshot: `origin/theory/PRE-LEAN` 6850c3a5.

**Verdict:** no recorded statement is affected and nothing blocks Lean shortlist item 3. T3-1 is a real but one-clause gap in a proof-file justification; its conclusion is true. T3-2 is Lean-only.

## 1. Rulings

| Point | Ruling | (a) Kind | (b) Recorded STATEMENT affected? | (c) Exact fix |
|---|---|---|---|---|
| **T3-1** (`P6_DISTC.md:70-72`, Positivity) | AGREE | Genuine gap in a justification, not an overclaim: "positive likelihood against a proper prior" gives m(S) > 0 but not m(S) < ∞. The conclusion m(S) ∈ (0, ∞) is true. | **No.** The paragraph is in the proof file `work/D_output/P6_DISTC.md` §0. The registry spans (`W3-DIST/STATEMENT.md:381-382`, `:289-318`, `:217-238`, `:322-326`) do not contain it. | Replace "and m(S) is the integral of a strictly positive likelihood against a proper prior: m(S) ∈ (0, ∞)." by: "and m(S) > 0, as the integral of a strictly positive likelihood against a proper prior. Also m(S) < ∞, by the closed form m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν} ([P1] `prop:closed`), since D_S ∈ (0, ∞), Q_S ≥ 0 and b₀ > 0." |
| **T3-2** (`P6_DISTC.md:157-158`, Jensen in P6(c)) | AGREE, Lean-only | Not a flaw. Read in [0, ∞] the step is correct: where f̄_Q(x, y) = ∞ the inequality is trivial, and elsewhere √g ≤ 1 + g is integrable. | No. | No paper change. In Lean, write the mixture with `lintegral` and replace Jensen by Hölder with p = q = 2 (`ENNReal.lintegral_mul_le_Lp_mul_Lq`), which needs no integrability and no almost-everywhere argument. |

Notes on the two rulings:
- **T3-1, where it is used.** Positivity feeds only "π(Ŝ) > 0" and "π(𝒯) > 0" in (C-0) and Cor-C. The fix is CORRECTION-ONLY on a file in MANIFEST_R2r, so it needs a re-freeze. Astra's own fix (likelihood ≤ C_n·v^{−n/2}, finite inverse-gamma moments) is also correct; the closed form is shorter and already locked.
- **T3-1 and Lean.** Lean is unaffected: there π(S) = e^{F(S)}/Z with real F, so positivity is automatic, and the identification of F with the marginal likelihood is the hypothesis (H-ID).
- **T3-2, simpler than Astra's route.** Astra proposes finiteness almost everywhere and then real Jensen. The Hölder form avoids both.

## 2. Correctness (focused; Astra's trail covers the edge cases)

Nothing further. Re-derived by hand:
- **P6(a), (b):** finite sums with (TP); a > 0 is the only division.
- **Affinity** (`H.md` Claim 1): the completed square gives α + β = (s₁+s₂)/(4s₁s₂) and exponent 1/(4(s₁+s₂)), so the integral is A·B.
- **Pointwise bound:** 1 − AB ≤ (1 − A) + (1 − B); 1 − A ≤ 1 − A² = (√r − 1)²/(r + 1) ≤ (r − 1)²; 1 − B ≤ min{1, Δ²/(4(v + σ*²))} ≤ min{1, Δ²/(4σ*²)}.
- **D0** is the same inequality without the truncation, averaged over i; it is stated for the centred means, and (H-in) adds the ε̄² intercept term correctly.
- **C-i°:** Π̂^𝒯(B_n) ≤ Π(B_n | D_n)/π(𝒯) ≤ ϱ_n/a.
- **(C-iii):** π(Ŝ) ≥ π(S′) > ϱ_n^{1/2} ≥ π(𝔅_n), so Ŝ ∉ 𝔅_n.
- **Cor-C (C1):** one data-only event G_n from Theorem A(i); n^{−cM}/n^{−cM/2} = n^{−cM/2} for every completed run at once.

## 3. Lean readiness (ranked)

**Level-2 named axioms: none** (all Level 1). No item changes a statement.

1. **Domination transfer as finite sums of weights.** Finite type Ω; π, Q : Ω → ℝ≥0; k : Ω → [0, 1] standing for S ↦ Π(B | S, D_n).
   - (a) Q ≤ L·π ⇒ ΣQk ≤ L·Σπk. (b) π{k > a} ≤ Σπk/a.
   - Store form: Q = π restricted to 𝒯 and renormalised, with hypothesis π(𝒯) ≥ a > 0, giving ΣQk ≤ ϱ/a.
   - Gain: no kernels, no measurability, no Positivity lemma. Cost: none.
2. **HPM clauses (C-ii)(α), (C-iii):** reuse the order lemma of T2 item 4. Cost: none.
3. **Lemma H and D0 in three layers.**
   - Scalar inequality (pure real analysis): for r > 0 and z ≥ 0, 1 − A(r)·e^{−z} ≤ (r − 1)² + min{1, z·(1 + r)}, which is (H.1) after z = Δ²/(4(v + σ*²)).
   - Gaussian affinity closed form, from Mathlib's Gaussian integral; it can be time-boxed as a separate lemma because D0 already takes H² = 1 − A·B as given.
   - Integration against ν_x (Tonelli, Claim 2).
   - Gain: D0 and the pointwise half of H are certified without any integration.
4. **P6(c) by Hölder on `lintegral`** (see T3-2), with `lintegral_lintegral_swap` for the two Tonelli steps. Stay in ℝ≥0∞ until the last line.
5. **Define d_H² once.** Mathlib has no Hellinger distance (I searched the pinned checkout). Put d_H²(f, g) := 1 − ∫√(fg) for densities in a shared file; T3 and T5 both use it.
