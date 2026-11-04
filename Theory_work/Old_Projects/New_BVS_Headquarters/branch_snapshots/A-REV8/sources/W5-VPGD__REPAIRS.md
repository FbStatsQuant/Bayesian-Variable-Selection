# W5-VPGD — repairs and additions to W3-PGD (Theorem W)

Gaps G1–G4 are those of `REFEREE.md`. R6 is new: it comes from goal 4 (LH) and is the most important item here.
Notation: W3-PGD PROOF §0–§3, STAR.md. Every item is a **candidate**.

---------------------------------------------------------------------------------------------------------

## R0. Vanishing margin (refines Prop P4's "only the boundary is open"). Status: PROVED (re-reading of constants)

Theorem W stays true with η = η_n → 0, provided η_n² · nθ²_min / log n → ∞ (under BM-∞ this holds when η_n²M_n → ∞).
*Proof.* In the m ≥ 1 part of Theorem W, γ_n = η_nNφ₀⁴θ²_min and C₁ = 2 + 4s₀/(η_nφ₀²). Lemma G needs
|N₁| ≤ 2σ√(2C₁g(L_n+ω_n)) ≤ g/4 for g ≥ γ_n, i.e. γ_n ≥ 128σ²C₁(L_n+ω_n). This holds when η_n²Nθ²_min/log n → ∞, since
L_n = O(log n). The other requirements (|N₂| ≤ g/4 and min{g/(24(M+σ²)), N/4} > 2c̄_n + 2C₀) need only γ_n/log n → ∞,
which is implied. Lemma S does not involve η. ∎
So the band left open between Theorem W and Prop P4 is: ratio max ρ⁰/ρ⁺ = 1 − η_n with η_n = O(√(log n/(nθ²_min))),
and ratios in [1, 1 + o(1)]. Exact population ties (ratio = 1) are a real case: see R6.

## R1. (H1) is a special case of (H2). Status: PROVED (presentational, G1)

For d = 1, (|𝒟|+1)^{d−1} = 1 ≤ n^{1/2−ε}. Keep (H1) as a named case for readability, but say that it is (H2) with d = 1.
STAR.md Prop. S′ also contains it.

## R2. Uniformity, needed for Cor P6 and Cor W′ (random designs). Status: PROVED (by inspection; G2)

**Theorem W (uniform form).** Fix (s₀, a, d, A, φ₀, η, M, σ, B′, ρ*, ε) and a sequence M_n → ∞. There is δ_n → 0,
depending only on these, such that for every n and every fixed design X (and deterministic 𝒟) that satisfies G, R,
SE_λ(d+1), BM-∞ with M_n, PGD(η) on R_{a,d}(𝒟), and one of (H1)–(H3) (or (★′)) with these constants:
P₀(TD′_P(R_{a,d}(𝒟)) fails) ≤ δ_n.
*Proof.* Every probability bound in Lemmas Q, R, G, U, S and Theorem W is a sum of a bounded number of terms e^{−ω_n}
(ω_n = log log n). Every "for n large" threshold depends only on the listed constants and on the counts p ≤ n^A,
|𝒟| ≤ p (or the (H2) bound). Nothing depends on X beyond the hypotheses. ∎
**Cor P6, repaired composition.** With E_X := {the realised design satisfies the hypotheses with (φ₀²/2, η/2)},
P(TD′_P fails) ≤ P(E_Xᶜ) + δ_n → 0, where P is joint over X and ε (X independent of ε). This is what Cor P6 and
Cor W′ need. Without it, "w.p. → 1 over X" and "P₀(·) → 1 for each fixed design" do not combine.

## R3. Stability of LD♭ under Gram perturbations (Lemma P5's last sentence). Status: PROVED (G3)

With ε := max{‖R̂_I − R_I‖_op : I = S₀ ∪ J, |J| ≤ d + 1} ≤ φ₀²/2 and λ_min(R_I) ≥ φ₀² on these I:
for every null l and T ⊆ S₀ᶜ∖{l} with |T| ≤ d, A = S₀ ∪ L, F = T∖𝔑(l),

  |ρ̂²(l, F | A) − ρ²(l, F | A)| ≤ 8ε/φ₀⁸.

*Proof.* For a set T′ ∌ l with I = T′ ∪ {l} in the family, the Schur complement is s_{T′}(l) = 1/u, u = (R_I⁻¹)_{ll}. Also
|û − u| ≤ ‖R̂_I⁻¹ − R_I⁻¹‖ ≤ ‖R̂_I⁻¹‖‖R_I⁻¹‖ε ≤ 2ε/φ₀⁴, and s, ŝ ≤ 1, so |ŝ − s| = |u − û|ŝs ≤ 2ε/φ₀⁴. Now
ρ² = 1 − s_{A∪F}/s_A with s_A ≥ φ₀² and ŝ_A ≥ φ₀²/2. Then
|ŝ_{AF}/ŝ_A − s_{AF}/s_A| ≤ |ŝ_{AF} − s_{AF}|/ŝ_A + s_{AF}|ŝ_A − s_A|/(ŝ_As_A) ≤ (2ε/φ₀⁴)(2/φ₀²) + (2ε/φ₀⁴)(2/φ₀⁴) ≤ 8ε/φ₀⁸.
Every I used, A ∪ F ∪ {l} = S₀ ∪ (L ∪ F ∪ {l}), has |L ∪ F ∪ {l}| ≤ d + 1, so it is in the family. ∎
Hence ρ̂*_k² ≤ ρ*_k² + 8ε/φ₀⁸ (k = d − 1, d). A strict (★) or (★′) for Σ survives for the realised design once
ε = O_P(√(log p/n)) is small enough. (W3 wrote O(ε/φ₀⁴); the power of φ₀ is immaterial.)

## R4. C-LD for p ≍ n^A, A > 1. Status: downgraded to CONJECTURE (G4)

W3's "with p ≍ n^A the same computation needs r > 1/(2A)" cannot use the exact orthonormal construction (p ≤ N).
It needs a random-design version, which is not written. Replace it with STAR.md §4: proved counterexamples at A = 1
(C-LD at r > 1/2, Prop. G at r > 1/3); for A > 1 a formula comparison only.

## R5. The "factor 3–4" sentence. Status: replaced

Replace "the constant in (★) is off by a factor ≈ 3–4 from C-LD's 1/(2A)" with STAR.md's summary. At A = 1, d = 2,
for grouped equicorrelated nulls: (★) certifies r < 0.111 and (★′) (proved) certifies r < 0.143. Failure is proved for
r > 1/3 (Prop. G; C-LD only gives r > 1/2). On the (α)/(γ) statistic the remaining loss is intrinsic to the local/far
method but second order in r. The loss in (β) is probably removable (CONJECTURE).

---------------------------------------------------------------------------------------------------------

## R6. Region form vs lattice form; the masked regime. Status: COUNTEREXAMPLE (region form) + PROVED (lattice form)

### R6.1 The region form of PGD fails, with an exact tie, whenever a truth can be worthless

**Proposition T (tie).** Suppose there are distinct truths u, v, j and a state S ∈ R_{a,d}(𝒟) with j ∈ M(S), u ∈ S,
such that u is worthless at S + j given the other variables, i.e. a_u(S + j − u) = 0 (population). Then
red(S → S − u + j) = a_j(S) − a_u(S − u + j) = a_j(S). Hence ρ⁰(S) ≥ max_j a_j(S) = ρ⁺(S) (W3 Remark (a): ρ⁺ = max add), and
PGD(η) fails on R_{a,d}(𝒟) for every η > 0. Moreover, if S, S + j, S − u + j ∈ 𝒯 and BM-∞ holds, then the neutral swap
u → j beats the progress move "add j" w.p. → 1, because S − u + j ⊂ S + j have equal Δ:
F(S − u + j) − F(S + j) ≥ c_{|S|} − ½Z²_{S−u+j, u}(1 + o_P(1)) − 2C₀ → +∞ (Lemma U, whose proof uses S₀ ⊆ A only through (P_B − P_A)μ = 0, which holds here).
Applying this to every missing j at once (when each add-j is matched by such a swap) shows that D_S fails. (Proof:
Lemma 1.1(b) and Lemma U/R.) Status: PROVED.

**On LH (W4-T38FULL §3.4) with c ≥ 2 linked pairs:** the hub b_i is worthless without a_i (⟨μ_{unit i}, x_{b_i}⟩ = 0).
At S = S₀ ∖ {a_1, a_2} ∈ R_{2,0}, the swap b_2 → a_1 ties "add a_1", and b_1 → a_2 ties "add a_2". So
- population PGD on R_{c,0}: η = 0 exactly in **20/20** LH cases (`scripts/lh_pgd.py`, `results/lh_pgd.txt`);
- TD′_P(R_{2,0}) fails w.p. → 1: D_S fails at S₀∖{a_1, a_2} in **200/200** realised fits at each of n = 200, 2000,
  20000 (exact Gram; `scripts/lh_tie.py`, `results/lh_tie.txt`). At S° = S₀∖{b_1, b_2} it holds in 200/200.
- This is the masked regime, T38(b)'s case. So **Theorem W in its region form R_{a,d}(𝒟), a ≥ 2, does not apply to
  the masked families on which Thm 5(b1) is proved.** TRC fails there with η₂ = 0, as W3's Prop P3 remark predicted
  ("TRC is a genuine no-masking condition"). Note what is not claimed: W3 never claimed Theorem W covers LH. The gap is
  in how F-REFINE's ARCHITECTURE/CARDS describe Theorem W ("the general sufficient condition for (M2)"); that is true
  only in the lattice form below.
- The greedy path is not stuck: after the swap b_2 → a_1 it adds a_2, then b_2 (3 moves for Φ = 2). So TD′_∞ can
  still hold. TD′_P is too strict for this move, because a truth-for-truth swap that removes a worthless truth is
  classified as neutral. (Outside scope: a potential that counts "effective" truths would restore progress.)

### R6.2 Theorem W_Lat (lattice form). Status: PROVED (candidate)

**Statement.** Regime R1, s₀ and d fixed. Let S° = U° ∪ P° be deterministic (X-measurable), with U° ⊆ S₀, P° ⊆ S₀ᶜ,
|P°| ≤ d. Assume EX-A, G, R, SE_λ(d+1), BM-∞, and PGD(η) on Lat(S°), i.e. ρ⁰(S) ≤ (1−η)ρ⁺(S) for every
S ∈ Lat(S°) with m(S) ≥ 1, for a fixed η > 0 (or η_n as in R0). Then w.p. → 1 the lattice condition

  (L) ∧ ⋂_{S ∈ Lat(S°)∖{S₀}} D_S

holds. Consequently, for ℓ_n ≥ Φ(S°) and every data-dependent centre S_c,
P(the production search from S_c does not return S₀ with local_certified) ≤ P(S_c ∉ Lat(S°)) + o(1),
and on the complement Ŝ = S₀ after the search (up to exact ties). **No LD condition is needed.**

*Proof.* Lat(S°) is closed under progress moves and contains S₀ (W1-T37R Lemma 2(a)); Φ ≤ Φ(S°) on it.
(i) States with m ≥ 1: the m ≥ 1 part of Theorem W's proof, verbatim, with R_{a,d}(𝒟) replaced by Lat(S°). All
compared sets lie in 𝒯 (they are ⊆ S₀ ∪ P° ∪ {x}). The pair count is ≤ 2^{Φ(S°)}(1 + (s₀+d+1)(p+1)), so L_n = O(log n).
(ii) Superset states S₀ ∪ P′ (P′ ⊆ P°) and (L): Lemma S with 𝒟 := P°, which has |𝒟| ≤ d fixed. So (H2) holds:
(d+1)^{d−1} ≤ n^{1/2−ε} eventually.
(iii) Lemma A′ applied to 𝓡 = Lat(S°). Every S′ ∈ Lat(S°) has Lat(S′) ⊆ Lat(S°), so every centre in Lat(S°) is
covered. ∎

**Relation to T38.** T38's Theorem b1 uses Lemma M with POP-LAT(S°, m_n) (absolute margins m_n ≫ √(log n/n) in Δ
units, no BM-∞), and it concludes *scoring* of S₀ (LS-score). W_Lat uses PGD (a relative margin) plus BM-∞, and it
concludes certification and (L). On a fixed-θ family the two premises are equivalent up to constants (R6.3).

### R6.3 PGD vs POP-LAT on a lattice; Proposition LH-PGD. Status: PROVED (candidate); sharpness numerical

**General equivalence (any design).** Put R⁺_min := min{R⁺(S) : S ∈ Lat(S°), m(S) ≥ 1} (≥ φ₀⁴θ²_min by Lemma 1.2) and
R⁺_max := max of the same (≤ Δ(S°)). Then:
(a) PGD(η) on Lat(S°) ⇒ POP-LAT(S°, ηR⁺_min), with A_S := the best progress neighbour.
(b) POP-LAT(S°, m) ⇒ PGD(m/R⁺_max) on Lat(S°) ∩ {Φ ≥ 2}.
*Proof.* PGD(η) at S ⟺ Δ(B) − Δ(A*_S) ≥ ηR⁺(S) for all non-progress B (A*_S the best progress neighbour). For (b):
Δ(A*_S) ≤ Δ(A_S), so Δ(B) − Δ(A*_S) ≥ m ≥ (m/R⁺_max)R⁺(S). ∎
POP-LAT only constrains Φ ≥ 2 (T38 needs scoring, not certification). PGD also needs the Φ = 1 states S₀ − j.

**Proposition LH-PGD.** On LH (exact Gram; W4-T38FULL §3.4 setting, S° = S₀∖M), PGD(η_LH) holds on Lat(S°)∖{S₀},
with

  η_LH := min{ 1, 1 − κ_max, D_min/R_max },   D_min := min{ min_i R_i, min_i β_i²(1−ψ_i²)², min_h θ_h² },

where R_i, κ_i, κ_max are those of LH-LAT and R_max = max_i R_i. Also m₀ ≤ η_LH·R_max, so LH-LAT's POP-LAT(S°, m₀)
implies PGD(m₀/R_max) ≤ PGD(η_LH): consistent.
*Proof.* Take S ∈ Lat(S°) with I(S) := {i : b_i ∉ S} ≠ ∅ (this includes |I| = 1, i.e. Φ = 1). The only progress
moves are the additions of the missing truths b_i, with Δ(S + b_i) = Δ(S) − R_i (LH-LAT unit algebra). So
R⁺(S) = R_{i*} := max_{i∈I}R_i. LH-LAT's case analysis never uses |I| ≥ 2, and it gives, for A* = S + b_{i*}:
B = S: R_{i*}; B = S + l: ≥ (1−κ_max)R_{i*}; B = S − t: ≥ R_{i*}; B = S − t + l: ≥ (1−κ_max)R_{i*};
B = S − t + b_i: ≥ (deletion increase of t in S + b_i) ≥ D_min, where the deletion increases are R_k (b_k with a_k
present), β_k²(1−ψ_k²) ≥ β_k²(1−ψ_k²)² (a_k with b_k present or absent) and θ_h². Divide by R⁺(S) = R_{i*} ≤ R_max. ∎
*Sharpness.* The brute-force PGD constant on Lat(S°) equals η_LH in **20/20** LH cases, including W4's referee set
(`results/lh_pgd.txt`). Analytically: (1 − κ_max) is attained at S missing only b_i with κ_i = κ_max, by adding a
mate of b_i. D_min/R_max is attained by the swap t → b_{i*} with t of minimal deletion increase (the a_k-with-b_k-absent
value needs c ≥ 2). Not written out in full.

**Answer to the task's question 4.** On LH, Theorem W's PGD on Lat(S°) **is** implied by POP-LAT(S°, m₀): with
η = m₀/R_max on Φ ≥ 2, and with the sharper η_LH on all of Lat(S°)∖{S₀}. So Theorem W_Lat (R6.2) re-derives T38's
(M2) conclusion on LH, and adds certification and (L). The **discrepancy** is in the region form: PGD on R_{c,0} fails
with an exact tie on LH whenever c ≥ 2 (R6.1). Any citation of "Theorem W" for the masked regime must use W_Lat.
