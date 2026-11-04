# W3-PGD — PROOF.md (statements and proofs)

All results here are **candidates**. They have not been reviewed and are not adopted. Status words follow
PROTOCOL.md. Notation follows `Docs/Theory/theorems/00_COMMON.md` and `theory_campaign/W1-T37R/PROOF.md`
(branch `theory/W1-T37R`). Every new symbol is defined where it first appears.

---------------------------------------------------------------------------------------------------------

## 0. Setting, notation, imported results

**Design and response (G).** We work in contrast coordinates: N := n − 1, X ∈ ℝ^{N×p} with ‖x_j‖² = N,
R := XᵀX/N, G_T := X_TᵀX_T = N R_T. The raw contrast response is Y := y_c = μ + e with e ~ N(0, σ²I_N),
σ² = σ*², μ = X_{S₀}θ, θ := θ*_{S₀} ∈ ℝ^{s₀}. The method's standardised response is y = Y/s_y,
s_y² = ‖Y‖²/N. For T ⊆ [p]: P_T is the projection onto col X_T, r_T := (I − P_T)μ (population residual),
Δ_T = ‖r_T‖²/N, RSS_T := ‖(I − P_T)Y‖².

**Reductions.** For T and x ∉ T, a_x(T) := ‖r_T‖² − ‖r_{T∪x}‖² ≥ 0 (residual reduction from adding x
to T; unnormalised, i.e. N times the Δ-reduction). For a move S → S′, red(S′) := ‖r_S‖² − ‖r_{S′}‖².

**Imported from W1-T37R** (definitions; the proofs there are PROVED unless stated):
m(S) = |S₀∖S|, e(S) = |S∖S₀|, Φ = m + e; the progress / neutral / regressive move classes
𝒫(S), 𝒩(S), ℛ(S) (progress = add truth, delete extra, swap extra→truth; everything else is non-progress);
the greedy map M(S) (best strict improvement among feasible flips and swaps, lexicographic ties);
Lemma 0 (monotonicity; Ŝ = S₀ after a certified repair); the event
D_S := {max_{S′∈𝒫(S)} F(S′) > max(F(S), max_{S″∈𝒩(S)∪ℛ(S)} F(S″))};
TD′_P(𝓡) := (L) ∧ ⋂_{S∈𝓡∖S₀} D_S with (L) := {M(S₀) = ⊥}; PGD and LD (Theorem C).

**New region notation.** For a deterministic (X-measurable) set 𝒟 ⊆ S₀ᶜ of admissible extras,

  R_{a,d}(𝒟) := {U ∪ P : U ⊆ S₀, |S₀∖U| ≤ a, P ⊆ 𝒟, |P| ≤ d},  R_{a,d} = R_{a,d}(S₀ᶜ).

It is closed under progress moves (W1-T37R Lemma 2(a): progress moves only add truths and remove extras),
and Φ ≤ a + d on it.

**PGD in unnormalised form.** For S with m(S) ≥ 1:
ρ⁺(S) := max_{S′∈𝒫(S)} red(S′), ρ⁰(S) := max_{S″∈𝒩(S)∪ℛ(S)} red(S″) (feasible neighbours).
**PGD(η) on 𝓡**: ρ⁰(S) ≤ (1 − η)ρ⁺(S) for every S ∈ 𝓡 with m(S) ≥ 1. (This is W1-T37R's PGD(η):
R⁺ = ρ⁺/N, R⁰ = ρ⁰/N.)

**Hypotheses** (00_COMMON unless stated).
- R: s₀ fixed; p ≤ n^A; ‖μ‖² ≤ nM; s₀ + d + 1 ≤ K eventually; p ≥ s₀ + d + 1.
- **SE_λ(j₀)** (anchored; W1-T03R notation): λ_min(R_{S₀∪J}) ≥ φ₀² for every J ⊆ S₀ᶜ with |J| ≤ j₀.
  By Cauchy interlacing λ_min(R_T) ≥ φ₀² for every T ⊆ S₀ ∪ J. We use j₀ = d + 1, and write
  𝒯 := {T : T ⊆ S₀ ∪ J, J ⊆ S₀ᶜ, |J| ≤ d + 1}. Every set compared below lies in 𝒯.
- BM-∞: θ²_min := min_j θ_j² ≥ M_n σ² log n/(nφ₀²) with M_n → ∞.
- Penalty: w(k) = ½/C(2p−1, k); pen(k) := ½k log(n+1) − log w(k); c_k := pen(k+1) − pen(k)
  = ½ log(n+1) + log((2p−1−k)/(k+1)). For k ≤ s₀ + d and p ≥ s₀ + d + 1:
  c_k ≥ c_* := ½ log n + log p − log(s₀ + d + 1), and c̄_n := max_{k<K} c_k ≤ ½ log(n+1) + log(2p).
- ω_n := log log n (a slowly diverging slack used in union bounds).

---------------------------------------------------------------------------------------------------------

## 1. Population side (deterministic: X and θ fixed)

### Lemma 1.1 (move algebra). Status: PROVED.
(a) a_x(T) = ⟨x̃, r_T⟩²/‖x̃‖² with x̃ = (I − P_T)x (a_x(T) = 0 if x̃ = 0).
(b) (swap identity) for i ∈ S, x ∉ S: red(S − i + x) = a_x(S − i) − a_i(S − i) = a_x(S) − a_i(S − i + x).
(c) If A ⊆ B then ‖r_A − r_B‖² = ‖r_A‖² − ‖r_B‖²; for any A, B,
    ‖r_A − r_B‖² ≤ 2(‖r_A‖² − ‖r_{A∪B}‖²) + 2(‖r_B‖² − ‖r_{A∪B}‖²).

*Proof.* (a) P_{T∪x} = P_T + uuᵀ with u = x̃/‖x̃‖, so r_{T∪x} = r_T − u⟨u, r_T⟩ and Pythagoras.
(b) Telescope through S − i (first form) or through S + x (second form).
(c) For A ⊆ B, r_A − r_B = (P_B − P_A)μ and P_B − P_A is a projection orthogonal to r_B, so
‖r_A‖² = ‖r_B‖² + ‖r_A − r_B‖². In general r_A − r_B = (r_A − r_{A∪B}) − (r_B − r_{A∪B}); use the nested case
and (u − v)² ≤ 2u² + 2v². ∎

### Lemma 1.2 (best truth addition; W1-T37R Lemma 3 with a residual bound). Status: PROVED.
Let M := S₀∖S ≠ ∅, m := |M|, and λ_min(G_{S∪S₀}) ≥ Nφ₀². Then
  ‖r_S‖² ≥ Nφ₀²‖θ_M‖²  and  max_{j∈M} a_j(S) ≥ (φ₀²/m)‖r_S‖² ≥ Nφ₀⁴‖θ_M‖²/m ≥ Nφ₀⁴θ²_min.
Hence ρ⁺(S) ≥ (φ₀²/m)‖r_S‖² and ρ⁺(S) ≥ Nφ₀⁴θ²_min.

*Proof.* r_S = Σ_{j∈M}θ_j x̃_j, x̃_j := (I − P_S)x_j (truths in S are annihilated). For v ∈ ℝ^M,
vᵀX_Mᵀ(I − P_S)X_M v = min_w ‖X_M v − X_S w‖² ≥ λ_min(G_{S∪M})‖v‖² and S ∪ M = S ∪ S₀; take v = θ_M.
Next ‖r_S‖² = Σ_j θ_j⟨x̃_j, r_S⟩ and |⟨x̃_j, r_S⟩| = ‖x̃_j‖√a_j(S) ≤ √N √a_j(S), so
‖r_S‖² ≤ ‖θ_M‖₁√N max_j √a_j(S), i.e. max_j a_j(S) ≥ ‖r_S‖⁴/(N‖θ_M‖₁²) ≥ ‖r_S‖²·φ₀²‖θ_M‖²/‖θ_M‖₁²
≥ (φ₀²/m)‖r_S‖². Adding j ∈ M is a progress move, so ρ⁺ ≥ max_j a_j(S). ∎

### Definitions: GERC and TRC
For S with M = M(S) ≠ ∅ and X̃_M := (I − P_S)X_M of full column rank, and a null l ∉ S with
x̃_l := (I − P_S)x_l, let c(S, l) := (X̃_MᵀX̃_M)⁻¹X̃_Mᵀx̃_l (coefficients of the projection of x̃_l on
span X̃_M) and

  ERC(S, l) := Σ_{j∈M} |c_j(S, l)|·‖x̃_j‖/‖x̃_l‖     (:= 0 if x̃_l = 0).

- **GERC(𝓡; η)** (greedy exact-recovery condition): ERC(S, l) ≤ √(1 − η) for every S ∈ 𝓡 with m(S) ≥ 1
  and every null l ∉ S. It is θ-free: it depends on X and S₀ only. It is the normalised-atom form of
  Tropp's exact recovery condition used for orthogonal least squares (Soussen–Gribonval–Idier–Herzet,
  IEEE-TIT 2013: "ERC is sufficient for OLS"); here it is anchored at the states actually visited,
  including states with extras. (External precedent: not re-checked here.)
- **TRC(𝓡; η)** (truth retention): a_u(S − u + j) ≥ η·a_j(S) for every S ∈ 𝓡 with m(S) ≥ 1, every
  u ∈ S ∩ S₀ and every j ∈ M(S). (θ-dependent; it fails when missing truths mask included ones.)
- For 𝓡 = R_{a,d}(𝒟) put 𝓡⁺ := R_{min(a+1,s₀),d}(𝒟).

### Lemma 1.3 (ERC controls null leakage). Status: PROVED.
Under the definitions above, a_l(S) ≤ ERC(S, l)²·max_{j∈M} a_j(S).

*Proof.* r_S ∈ span X̃_M, so ⟨x̃_l, r_S⟩ = ⟨P_{span X̃_M} x̃_l, r_S⟩ = Σ_j c_j⟨x̃_j, r_S⟩. Dividing by ‖x̃_l‖,
|⟨x̃_l, r_S⟩|/‖x̃_l‖ ≤ Σ_j |c_j|(‖x̃_j‖/‖x̃_l‖)·|⟨x̃_j, r_S⟩|/‖x̃_j‖ ≤ ERC(S,l)·max_j √a_j(S). Square (Lemma 1.1(a)). ∎

### Proposition P1 (PGD from GERC and TRC). Status: PROVED.
Assume SE_λ(d) (so every X̃_M below has full rank). If GERC(𝓡⁺; η₁) and TRC(𝓡; η₂) hold for
𝓡 = R_{a,d}(𝒟), then PGD(η) holds on 𝓡 with η = min(η₁, η₂).

*Proof.* Fix S = U ∪ P ∈ 𝓡 with M ≠ ∅. By Lemma 1.2, ρ⁺(S) ≥ max_{j∈M} a_j(S) > 0. Every move is an
add, a delete, or a swap with outgoing element in {truth, extra} and incoming element in {truth, null};
the non-progress ones are exactly (N1)–(N5) below. Write η = min(η₁, η₂).
(N1) add a null l: red = a_l(S) ≤ (1 − η₁)max_j a_j(S) ≤ (1 − η)ρ⁺ (Lemma 1.3, GERC at S).
(N2) delete a truth u: red = −a_u(S − u) ≤ 0.
(N3) swap truth u → null l: red = a_l(S − u) − a_u(S − u) (Lemma 1.1(b)). S − u ∈ 𝓡⁺ misses M ∪ {u}.
     By GERC at S − u, a_l(S − u) ≤ (1 − η₁)a_k(S − u) for the maximising k ∈ M ∪ {u}. If k = u, red ≤ −η₁a_u ≤ 0.
     If k = j ∈ M, red ≤ (1 − η₁)a_j(S−u) − a_u(S−u) ≤ (1 − η₁)[a_j(S−u) − a_u(S−u)] when the bracket is ≥ 0
     (and red ≤ 0 otherwise); the bracket is the reduction of the swap u → j, which by Lemma 1.1(b) equals
     a_j(S) − a_u(S − u + j) ≤ a_j(S) ≤ ρ⁺. So red ≤ (1 − η)ρ⁺.
(N4) swap extra e → null l: red = a_l(S − e) − a_e(S − e). S − e ∈ 𝓡 has the same M. Let
     A := max_{j∈M} a_j(S − e). GERC gives a_l(S − e) ≤ (1 − η₁)A. The progress swap e → j* (j* the maximiser)
     has reduction A − a_e(S − e) ≤ ρ⁺. If A ≥ a_e(S−e), red ≤ (1 − η₁)A − a_e ≤ (1 − η₁)(A − a_e) ≤ (1 − η)ρ⁺;
     otherwise red < 0.
(N5) swap truth u → truth j ∈ M: red = a_j(S) − a_u(S − u + j) ≤ (1 − η₂)a_j(S) ≤ (1 − η)ρ⁺ (TRC). ∎

### Remarks on GERC. Status: PROVED.
(a) *Tightness over θ.* For fixed S, l and M, sup over θ_M ≠ 0 of a_l(S)/max_{j∈M} a_j(S) equals ERC(S, l)².
Indeed, with x̂_j := x̃_j/‖x̃_j‖, Ĝ := X̂_MᵀX̂_M and b := X̂_Mᵀx̂_l, ERC(S, l) = ‖Ĝ⁻¹b‖₁ (since c_j‖x̃_j‖/‖x̃_l‖ =
(Ĝ⁻¹b)_j); r_S = X̃_Mθ_M ranges over all of span X̃_M, so the vector t := X̂_Mᵀr_S ranges over ℝ^M; then
⟨x̂_l, r_S⟩ = (Ĝ⁻¹b)ᵀt and max_j a_j = ‖t‖²_∞, and sup_t ((Ĝ⁻¹b)ᵀt)²/‖t‖²_∞ = ‖Ĝ⁻¹b‖₁². Hence GERC(𝓡; η) is
*equivalent* to "the add-null part of PGD(η) holds on 𝓡 for every θ with support S₀".
(b) *A coherence sufficient condition (restricted-isometry type).* Let μ_S := max_{l null, j∈M}|⟨x̂_l, x̂_j⟩| and
ν_S := max_{j≠k∈M}|⟨x̂_j, x̂_k⟩| (residualised, normalised atoms at S). If (m − 1)ν_S < 1 then
ERC(S, l) ≤ mμ_S/(1 − (m − 1)ν_S) (Ĝ is diagonally dominant, ‖Ĝ⁻¹‖_{1→1} ≤ 1/(1 − (m−1)ν_S), ‖b‖₁ ≤ mμ_S).
So GERC(𝓡; η) holds if mμ_S ≤ √(1 − η)(1 − (m−1)ν_S) on 𝓡; for near-truth regions (a small) this is a mild,
anchored coherence bound. (c) The combination look-alike of W1-T37R Exp 3 has ERC(∅, 3) = √2·a = 1.20 > 1:
GERC fails exactly where PGD fails.

### Proposition P2 (exact block reduction). Status: PROVED.
Let 𝒢 be a partition of [p] such that (BO) X_gᵀX_h = 0 for distinct groups g ≠ h, and every group contains
at most one truth. For a truth group g write j_g for its truth, N_g := g∖{j_g}, and for P ⊆ N_g
  D_g(P) := θ_{j_g}²‖(I − P_P)x_{j_g}‖²  (= Nθ²_{j_g}(1 − R²(j_g | P))).
Let a ≥ 1. Then PGD(η) holds on R_{a,d}(𝒟) **if and only if**
- (B1) D_g(P + l) ≥ ηD_g(P) for every truth group g, P ⊆ N_g ∩ 𝒟 with |P| ≤ d, l ∈ N_g∖P
  [equivalently: squared partial correlation pcorr²(j_g, l | P) ≤ 1 − η];
- (B2) D_g(P − e + l) ≥ ηD_g(P) for every truth group g, P ⊆ N_g ∩ 𝒟 with 1 ≤ |P| ≤ d, e ∈ P, l ∈ N_g∖P;
- (B3) D_h(Q) ≥ ηD_g(P) for all distinct truth groups g ≠ h and P ⊆ N_g ∩ 𝒟, Q ⊆ N_h ∩ 𝒟 with
  |P| + |Q| ≤ d.
(Moves are assumed feasible, i.e. s₀ + d + 1 ≤ K.)

*Proof.* Under BO, P_S = Σ_g P_{S∩g} and μ = Σ_g θ_{j_g}x_{j_g}, so
‖r_S‖² = Σ_{g truth group, j_g ∉ S} D_g(S ∩ N_g): additive over groups, with zero contribution from groups
whose truth is in S and from pure-null groups. Fix S with m ≥ 1 and write P_g := S ∩ N_g, "g out" if j_g ∉ S,
D* := max_{g out} D_g(P_g).
*Progress moves.* Add j_g (g out): red = D_g(P_g). Swap e → j_g: if e ∈ g the group residual becomes 0,
red = D_g(P_g); if e lies in another group h, red = D_g(P_g) − [increase in h] ≤ D_g(P_g). Delete an extra:
red ≤ 0. Hence ρ⁺(S) = D*.
*Non-progress moves.* Add null l ∈ g: red = D_g(P_g) − D_g(P_g + l) if g out, else 0. Delete j_h: red = −D_h(P_h).
Swap j_h → l: red = −D_h(P_h + l) if l ∈ h; = [D_g(P_g) − D_g(P_g+l)] − D_h(P_h) if l ∈ g out; = −D_h(P_h)
otherwise. Swap j_h → j_g (g out): red = D_g(P_g) − D_h(P_h). Swap e → l with e ∈ P_h, l ∈ g: if h = g out,
red = D_g(P_g) − D_g(P_g − e + l); if h ≠ g, red ≤ [D_g(P_g) − D_g(P_g + l)]·1{g out} (the change in h is an
increase); 0 if g is in or pure.
*Sufficiency.* (B1) bounds every "add null" and every cross-group swap into a missing group by (1 − η)D_g ≤
(1 − η)D*; (B2) bounds within-group null swaps; (B3) bounds truth → truth swaps; the rest are ≤ 0.
*Necessity.* If (B1) fails at (g, P, l), take S = (S₀∖{j_g}) ∪ P ∈ R_{a,d}(𝒟) (m = 1 ≤ a). Then ρ⁺ = D_g(P)
and adding l reduces by D_g(P) − D_g(P + l) > (1 − η)ρ⁺. (B2): same S, swap e → l. (B3): take
S = (S₀∖{j_g}) ∪ P ∪ Q, so ρ⁺ = D_g(P), and the swap j_h → j_g reduces by D_g(P) − D_h(Q) > (1 − η)ρ⁺. ∎

**Corollary P2′ (equicorrelated groups; S1, S3, S4, S6). Status: PROVED.** If, in addition, every truth group
g has b_g ≥ 2 members with within-group correlation ρ_g ∈ [0, 1), and 𝒟 contains all mates, then for |P| = k
R²(j_g | P) = kρ_g²/(1 + (k−1)ρ_g) and pcorr(j_g, l | P) = ρ_g/(1 + kρ_g), so
  η*(d) := sup{η : PGD(η) on R_{a,d}(𝒟)} = min{ min_g (1 − ρ_g²),  min_{g≠h} (θ_h²/θ_g²)(1 − κ_h(d)) },
  κ_h(d) := kρ_h²/(1 + (k−1)ρ_h), k = min(d, b_h − 1),
for every a ≥ 1 (B2 holds with η = 1 by exchangeability; the worst (B1) case is k = 0, the worst (B3) case
puts all d extras into group h). *Proof:* the two formulas are the equicorrelation identities
1ᵀ((1−ρ)I + ρJ)⁻¹1 = k/(1+(k−1)ρ) and the Schur complement for one more mate; plug into (B1)–(B3). ∎
For S1 (ρ = 0) this gives η* = θ²_min/θ²_max = 0.64/3.24 = 0.198 for every d (a pure θ-ratio effect of the
truth → truth swap).

### Proposition P3 (sufficient conditions for TRC). Status: PROVED.
(a) Under SE_λ(d), TRC(R_{1,d}(𝒟); φ₀²θ²_min/θ²_max) holds (states missing exactly one truth).
(b) Under BO with one truth per group, TRC(R_{a,d}(𝒟); φ₀²θ²_min/θ²_max) holds for every a.
*Proof.* (a) If M = {j}, then S − u + j misses only u, so a_u(S − u + j) = θ_u²‖(I − P_{S−u+j})x_u‖² ≥ Nφ₀²θ_u²
(SE_λ(d) on S₀ ∪ P), while a_j(S) ≤ ‖r_S‖² = θ_j²‖x̃_j‖² ≤ Nθ_j². (b) a_u(T) = D_{g(u)}(T ∩ N_{g(u)}) ≥ Nφ₀²θ_u²
and a_j(S) = D_{g(j)}(P_{g(j)}) ≤ Nθ_j². ∎
*Remark.* For m ≥ 2 without block structure, a_u(S − u + j) = (θ_u‖x̌_u‖ + Σ_{k∈M∖j}θ_k⟨x̌_u, x̌_k⟩/‖x̌_u‖)² with
x̌ = (I − P_{S−u+j})x can vanish (missing truths cancel u's contribution): TRC is a genuine no-masking
condition, and it fails in the T27 masked regime far from S₀.

### Proposition P4 (PGD is sharp up to the boundary). Status: PROVED.
Assume G, R, SE_λ(d+1), BM-∞, with s₀, a, d fixed. Suppose that along a subsequence there are S_n ∈ R_{a,d}(𝒟)
with m(S_n) ≥ 1 and ρ⁰(S_n) ≥ (1 + ε)ρ⁺(S_n) for a fixed ε > 0. Then P₀(D_{S_n}) → 0 along it; in particular
P₀(TD′_P(R_{a,d}(𝒟))) → 0. So PGD(η) for some fixed η > 0 cannot be weakened to any condition allowing a
reverse margin; only the boundary case max ρ⁰/ρ⁺ → 1 is left open.

*Proof.* Let S″ be a non-progress neighbour attaining ρ⁰(S_n) > 0 (so ‖r_{S″}‖² < ‖r_S‖²). For each progress
neighbour S′ put g := ‖r_{S′}‖² − ‖r_{S″}‖² = ρ⁰ − red(S′) ≥ ρ⁰ − ρ⁺ ≥ ερ⁺ ≥ εNφ₀⁴θ²_min (Lemma 1.2). With U := S′ ∪ S″,
Lemma 1.1(c) and ‖r_{S′}‖² = g + ‖r_{S″}‖² give ‖r_{S′} − r_{S″}‖² ≤ 2g + 4(‖r_{S″}‖² − ‖r_U‖²) ≤ 2g + 4‖r_S‖²
≤ 2g + (4s₀/φ₀²)ρ⁺ ≤ (2 + 4s₀/(εφ₀²))g. Lemma G (§2) with (A, B) = (S″, S′), over the ≤ s₀ + d + s₀d progress
neighbours, gives F(S″) > F(S′) for all of them w.p. → 1; then D_{S_n} fails. ∎

### Lemma P5 (stability of Δ, PGD, SE and LD♭ under Gram perturbations). Status: PROVED.
Let R, R̂ be p × p unit-diagonal Gram matrices and ε := max{‖R̂_I − R_I‖_op : I = S₀ ∪ J, |J| ≤ d + 1}. Assume
λ_min(R_I) ≥ φ₀² on these I and ε ≤ φ₀²/2. Put L := 4s₀/φ₀². Then
(i) λ_min(R̂_I) ≥ φ₀²/2;
(ii) |Δ_T(R̂) − Δ_T(R)| ≤ Lε‖θ‖² for every T ∈ 𝒯;
(iii) if PGD(η) holds for (R, θ) on R_{a,d}(𝒟) and ε ≤ ηφ₀⁶θ²_min/(128 s₀‖θ‖²), then PGD(η/2) holds for (R̂, θ).
*Proof.* (i) Weyl. (ii) With I = S₀ ∪ T, Δ_T(R) = min_w vᵀR_I v over v := (θ on S₀) − (w on T) (coordinates in
S₀ ∩ T combine). At the R-minimiser v*, φ₀²‖v*‖² ≤ Δ_T(R) ≤ θᵀR_{S₀}θ ≤ s₀‖θ‖², so
Δ_T(R̂) ≤ v*ᵀR̂_I v* ≤ Δ_T(R) + εs₀‖θ‖²/φ₀². Conversely, at the R̂-minimiser v̂, (φ₀²/2)‖v̂‖² ≤ (s₀ + ε)‖θ‖², so
Δ_T(R) ≤ Δ_T(R̂) + 2ε(s₀ + ε)‖θ‖²/φ₀² ≤ Δ_T(R̂) + Lε‖θ‖². (iii) Unnormalised reductions are N times differences of
two Δ's of sets in 𝒯, so ρ̂⁺, ρ̂⁰ are within 2NLε‖θ‖² of ρ⁺, ρ⁰, and ρ̂⁰ ≤ (1 − η)ρ̂⁺ + 4NLε‖θ‖². By Lemma 1.2 for R̂,
ρ̂⁺ ≥ N(φ₀²/2)²θ²_min, and the bound on ε makes 4NLε‖θ‖² ≤ (η/2)ρ̂⁺. ∎ Partial correlations (hence LD♭, §3) are ratios
of such Schur complements with θ = e_l and denominators ≥ φ₀²/2, so they move by O(ε/φ₀⁴); a strict (★) survives
small ε.

### Corollary P6 (random Gaussian designs). Status: PROVED given a cited concentration bound.
Let the raw rows be iid N(0, Σ), diag Σ = 1, p ≤ n^A, X the column-standardised design, θ the coefficient
vector on the standardised scale with θ_max/θ_min ≤ κ (fixed). If Σ satisfies SE_λ(d+1) with φ₀² and PGD(η) on
R_{a,d}(𝒟) (for 𝒟 deterministic), then w.p. → 1 over X the realised design satisfies SE_λ(d+1) with φ₀²/2 and
PGD(η/2). *Proof.* max_{i,j}|R̂_ij − Σ_ij| = O_P(√(log p/n)) for Gaussian rows (standard; e.g. Bickel–Levina
2008, Lemma A.3, applied to the covariance and then to the standardisation — cited, not re-derived), so
ε ≤ (s₀ + d + 1)·max|R̂ − Σ| → 0; apply Lemma P5 ((iii) needs ε ≤ ηφ₀⁶/(128 s₀²κ²), which holds eventually). In the study's generator the signal
is formed on the standardised X, so the realised θ* equals cβ exactly. ∎

---------------------------------------------------------------------------------------------------------

## 2. Noise side: three lemmas

### Lemma Q (Gaussian maxima). Status: PROVED (standard).
Let V₁, …, V_L be deterministic subspaces of ℝ^N with dim V_i ≤ k, and v₁, …, v_L deterministic vectors.
(i) P(max_i ‖P_{V_i}e‖²/σ² > k + 2√(kt) + 2t) ≤ Le^{−t} (Laurent–Massart 2000), and k + 2√(kt) + 2t ≤ 2k + 3t.
(ii) P(max_i |v_iᵀe|/(σ‖v_i‖) > √(2t)) ≤ Le^{−t} for t ≥ 1 (2Φ̄(x) ≤ e^{−x²/2} for x ≥ √(2/π)).
(iii) If dim V = 2, ‖P_Ve‖²/σ² ~ χ²₂ and P(χ²₂ > x) = e^{−x/2}; for dim 1, P(χ²₁ > x) ≤ e^{−x/2} (x ≥ 1).

### Lemma R (score representation). Status: PROVED.
Let k̄ := s₀ + d + 1 and assume SE_λ(d+1). There is a random Ψ, common to all T, such that for every T ∈ 𝒯
  F(T) = Ψ − pen(|T|) − ν log RSS_T + ζ_T,
  |ζ_T| ≤ k̄/(2Nφ₀²) + (1 + 2b₀ + 1/(Nφ₀²))·‖Y‖²/RSS_T.
Moreover, on an event E₀ with P(E₀) → 1, sup_{T∈𝒯}|ζ_T| ≤ C₀ := 5 + 4M/σ² for all large n, and
RSS_T ≥ Nσ²(1 − δ_n) for every T ∈ 𝒯 with S₀ ⊆ T, where δ_n → 0 and δ_n log n → 0.

*Proof.* F(T) = log w(|T|) − log W_K + log C_n − ½ log D_T − ν log(2b₀ + Q_T(y)). Q_T is a quadratic form in its
argument, so Q_T(y) = Q_T(Y)/s_y², and −ν log(2b₀ + Q_T(y)) = ν log s_y² − ν log(2b₀s_y² + Q_T(Y)). Put
Ψ := −log W_K + log C_n + ν log s_y². Let g₁, …, g_{|T|} be the eigenvalues of G_T, g_i ≥ g_min ≥ Nφ₀².
*Determinant.* log D_T = Σ_i log[((n+1)g_i + 1)/(g_i + 1)] = |T| log(n+1) − Σ_i log[(g_i + 1)/(g_i + 1/(n+1))], and
0 ≤ log[(g + 1)/(g + 1/(n+1))] ≤ log(1 + 1/g) ≤ 1/g; so −½ log D_T = −½|T| log(n+1) + ε¹_T, 0 ≤ ε¹_T ≤ |T|/(2Nφ₀²).
*Quadratic form.* With z = X_TᵀY in the eigenbasis of G_T (z lies in range G_T),
ξ_T := Q_T(Y) − RSS_T = Σ_i (z_i²/g_i)(g_i + 1)/((n+1)g_i + 1) ∈ [0, ‖P_TY‖²(1 + 1/g_min)/(n+1)]
(because zᵀG_T⁻¹z = ‖P_TY‖² and (g+1)/((n+1)g+1) ≤ (1 + 1/g)/(n+1)). Hence
−ν log(2b₀s_y² + Q_T(Y)) = −ν log RSS_T − ε²_T with 0 ≤ ε²_T ≤ ν(2b₀s_y² + ξ_T)/RSS_T
≤ (ν/N)(2b₀ + 1 + 1/(Nφ₀²))‖Y‖²/RSS_T, and ν/N = (n/2 + a₀)/(n − 1) ≤ 1 (and ν/N ≥ ½). Combine: ζ_T = ε¹_T − ε²_T and
pen(|T|) = ½|T| log(n+1) − log w(|T|).
*The event E₀.* By Lemma Q(i) over the ≤ (p+1)^{d+1} spaces col X_{S₀∪J} (dim ≤ k̄) with t = (d+1)log(p+1) + ω_n,
max_J ‖P_{S₀∪J}e‖² ≤ σ²(2k̄ + 3t) = O(σ² log n). By Laurent–Massart, ‖e‖² ∈ Nσ²[1 − 2√(ω_n/N), 1 + 2√(ω_n/N) + 2ω_n/N]
w.p. ≥ 1 − 2e^{−ω_n}. For T ∈ 𝒯, RSS_T ≥ ‖(I − P_{T∪S₀})e‖² = ‖e‖² − ‖P_{T∪S₀}e‖² ≥ Nσ²(1 − δ_n) with
δ_n := 2√(ω_n/N) + O(log n/N), and δ_n log n → 0. Also ‖Y‖² ≤ 2‖μ‖² + 2‖e‖² ≤ 2nM + 3Nσ² ≤ N(3M + 3σ²). So
‖Y‖²/RSS_T ≤ (3M + 3σ²)/(σ²(1 − δ_n)) ≤ 3.1(1 + M/σ²) eventually, and |ζ_T| ≤ 1 + 1.03·3.1(1 + M/σ²) ≤ C₀. ∎

### Lemma G (population-gap comparisons). Status: PROVED.
Assume G, R, SE_λ(d+1). Let 𝒫_n be a deterministic family of ordered pairs (A, B) of sets in 𝒯 with
|A∖B|, |B∖A| ≤ 2 and |𝒫_n| ≤ e^{L_n}, where L_n ≥ log n. Suppose that for every pair
  g_{AB} := ‖r_B‖² − ‖r_A‖² ≥ γ_n  and  ‖r_A − r_B‖² ≤ C₁ g_{AB}
with C₁ fixed and γ_n/L_n → ∞. Then, with probability → 1, simultaneously for all pairs,
  F(A) − F(B) ≥ min{g_{AB}/(24(M + σ²)), N/4} − 2c̄_n − 2C₀,
and in particular F(A) > F(B) for all pairs once γ_n/log n → ∞ (since c̄_n ≤ (½ + A)log n + log 2 + 1).

*Proof.* RSS_T = ‖r_T‖² + 2r_Tᵀe + ‖e‖² − eᵀP_Te (r_T ∈ range(I − P_T)). Hence, with C := A ∩ B,
RSS_B − RSS_A = g_{AB} + N₁ − N₂, N₁ := 2(r_B − r_A)ᵀe, N₂ := ‖P_{B|C}e‖² − ‖P_{A|C}e‖², where P_{B|C} := P_B − P_C is the
projection onto col X_B ⊖ col X_C, of dimension ≤ 2. N₁ ~ N(0, 4σ²‖r_B − r_A‖²); by Lemma Q(ii) with
t = L_n + ω_n, |N₁| ≤ 2σ‖r_B − r_A‖√(2(L_n + ω_n)) ≤ 2σ√(2C₁g(L_n+ω_n)) for all pairs w.p. ≥ 1 − e^{−ω_n}. By Lemma
Q(i) over the 2e^{L_n} subspaces, |N₂| ≤ σ²(4 + 3(L_n + ω_n + 1)) w.p. ≥ 1 − e^{−ω_n}. Since g ≥ γ_n and
γ_n/(L_n + ω_n) → ∞, eventually |N₁| + |N₂| ≤ g/2 for all pairs, so RSS_B ≥ RSS_A + g/2. On E₀,
RSS_A ≤ ‖Y‖² ≤ N(3M + 3σ²); with x := g/(2N(3M + 3σ²)) and log(1 + x) ≥ ½min(x, 1),
ν log(RSS_B/RSS_A) ≥ (N/2)·½min(x, 1) ≥ min{g/(24(M + σ²)), N/4}. Finally
F(A) − F(B) = ν log(RSS_B/RSS_A) + pen(|B|) − pen(|A|) + ζ_A − ζ_B, ||A| − |B|| ≤ 2, |pen(|B|) − pen(|A|)| ≤ 2c̄_n,
|ζ| ≤ C₀ (Lemma R). ∎

### Lemma U (supersets of S₀). Status: PROVED.
For A ⊆ B in 𝒯 with S₀ ⊆ A put W(B | A) := ‖(P_B − P_A)e‖²/σ² (a χ² variable with dim(col X_B ⊖ col X_A)
degrees of freedom). Then RSS_A − RSS_B = σ²W(B | A), and on E₀
  F(B) − F(A) ≤ ½W(B | A)(1 + δ′_n) − Σ_{k=|A|}^{|B|−1} c_k + 2C₀,  δ′_n := (1 + 2/n)/(1 − δ_n) − 1,
so F(B) − F(A) ≤ ½W(B|A) − (|B| − |A|)c_* + 2C₀ + 1 whenever W(B|A) ≤ C log n (n large).
*Proof.* μ ∈ col X_A, so (I − P_A)Y − (I − P_B)Y = (P_B − P_A)e. Then −ν log(RSS_B/RSS_A) = −ν log(1 − x),
x := σ²W/RSS_A, and −log(1 − x) ≤ x/(1 − x) = σ²W/RSS_B. With RSS_B ≥ Nσ²(1 − δ_n) (Lemma R) and
ν/N ≤ ½(1 + 2/n), νσ²W/RSS_B ≤ ½W(1 + δ′_n). Add the penalty difference and |ζ_A − ζ_B| ≤ 2C₀. The last claim uses
δ′_n log n → 0. ∎
**Chain rule.** For T ⊆ nulls and x, l ∉ S₀ ∪ T: W(S₀∪T∪{x,l} | S₀∪T) = Z²_{S₀∪T,x} + Z²_{S₀∪T∪x, l}, where
Z_{B,l} := u_{B,l}ᵀe/σ and u_{B,l} := (I − P_B)x_l/‖(I − P_B)x_l‖ (Gram–Schmidt).

---------------------------------------------------------------------------------------------------------

## 3. The superset states (m = 0): where LD enters

### Definition LD♭(d; B′, ρ*) (local dependence, constant threshold).
There is a deterministic map 𝔑 assigning to each null l a set 𝔑(l) ⊆ S₀ᶜ∖{l} with |𝔑(l)| ≤ B′ (its
"neighbours"), such that for every null l and every T ⊆ S₀ᶜ∖{l} with |T| ≤ d, writing L := T ∩ 𝔑(l),
F := T∖𝔑(l), A := S₀ ∪ L,
  ρ(l, F | A) ≤ ρ*,   where ρ²(l, F | A) := ‖P_Ṽ x̌_l‖²/‖x̌_l‖², x̌_l := (I − P_A)x_l, Ṽ := col((I − P_A)X_F)
(the squared partial multiple correlation of x_l with X_F given X_A). The threshold condition is
  (★)  τ² < 1 + 1/(2A),   τ := (1 + ρ*√d)/√(1 − ρ*²).
W1-T37R's LD(d) with B′ = 0 (ρ² ≤ κ_n, κ_n log p → 0) implies LD♭ with ρ* → 0, hence (★). LD♭ allows a fixed
correlation level ρ* (e.g. ρ* ≈ 0.14/A for d = 2) and fixed-size correlated clusters (group-mates).

### Lemma LD (local/far decomposition). Status: PROVED.
With the notation of LD♭ and SE_λ(d+1): |Z_{S₀∪T, l}| ≤ (|Z_{A,l}| + ρ(l, F | A)·‖P_Ṽe‖/σ)/√(1 − ρ²(l,F|A)).
*Proof.* col X_{A∪F} = col X_A ⊕ Ṽ with Ṽ ⊆ range(I − P_A), so I − P_{S₀∪T} = (I − P_A) − P_Ṽ and
(I − P_{S₀∪T})x_l = x̌_l − P_Ṽx̌_l, of norm ‖x̌_l‖√(1 − ρ²) > 0 (SE). Then
u_{S₀∪T,l}ᵀe = (x̌_lᵀe − (P_Ṽx̌_l)ᵀ(P_Ṽe))/(‖x̌_l‖√(1 − ρ²)) and |(P_Ṽx̌_l)ᵀP_Ṽe| ≤ ρ‖x̌_l‖‖P_Ṽe‖. ∎

### Lemma S (superset states). Status: PROVED.
Assume G, R, SE_λ(d+1), BM-∞, and one of
- (H1) d ≤ 1 (any 𝒟 ⊆ S₀ᶜ, e.g. all nulls);
- (H2) (|𝒟| + 1)^{d−1} ≤ n^{1/2−ε} for some fixed ε > 0;
- (H3) LD♭(d; B′, ρ*) with (★), B′ fixed (any 𝒟).
Then with probability → 1: (L) F(S₀) > F(S″) for every feasible neighbour S″ of S₀; and for every P ⊆ 𝒟 with
1 ≤ |P| ≤ d, the event D_S holds at S = S₀ ∪ P.

*Proof.* Fix e₀(P) := min P (deterministic). At S = S₀ ∪ P the non-progress comparators are: S itself; S + l
(null l ∉ S); S − e′ + l (e′ ∈ P, null l ∉ S); and the truth-removing S − u, S − u + l (u ∈ S₀). The progress
moves are the deletions S − e, e ∈ P. It suffices to show, uniformly:
 (T)  F(S) > F(S − u), F(S − u + l)   [for all P ⊆ 𝒟 with |P| ≤ d, including P = ∅];
 (L′) F(S₀) > F(S₀ + l);
 (α)  F(S − e₀) > F(S);   (β) F(S − e₀) > F(S + l);   (γ) F(S − e′) > F(S − e′ + l).
Then max_e F(S − e) exceeds every comparator (for (T) chain with (α)), and at S₀, (T) and (L′) give (L).
*(T) by Lemma G.* Pairs (A, B) = (S, S″) with S″ ∈ {S − u, S − u + l}: since S ⊇ S₀, r_S = 0 and
r_{S″} = θ_u(I − P_{S″})x_u, so g = ‖r_{S″}‖² ≥ θ_u²λ_min(G_{S∪l}) ≥ Nφ₀²θ²_min (S ∪ {l} ∈ 𝒯), and ‖r_A − r_B‖² = g
(C₁ = 1). The family has ≤ (|𝒟| + 1)^d s₀(p + 1) pairs, so L_n = O(log n), while γ_n := Nφ₀²θ²_min ≥ M_nσ² log n·N/n
(BM-∞) gives γ_n/L_n → ∞.
*(L′).* Z²_{S₀,l} ~ χ²₁; on Ω_L := {max_l Z²_{S₀,l} ≤ 2 log p + 2ω_n} (P(Ω_Lᶜ) ≤ e^{−ω_n}, Lemma Q(iii)), Lemma U gives
F(S₀ + l) − F(S₀) ≤ log p + ω_n − c_* + 2C₀ + 1 = −½ log n + ω_n + O(1) → −∞.
*(α), (β), (γ) under (H1) or (H2).* Let D := |𝒟| and 𝒫_d := {P ⊆ 𝒟 : 1 ≤ |P| ≤ d}, |𝒫_d| ≤ (D + 1)^d.
 (α) W(S | S − e₀) ~ χ²₁, ≤ |𝒫_d| variables; on {max ≤ 2 log|𝒫_d| + 2ω_n}: F(S) − F(S − e₀) ≤ d log(D+1) + ω_n − c_* + O(1)
   = d log(D+1) − log p − ½ log n + ω_n + O(1).
 (β) W(S + l | S − e₀) = Z²_{S−e₀,e₀} + Z²_{S,l} is χ² with ≤ 2 d.f. (Lemma Q(iii): tail ≤ e^{−x/2}), ≤ |𝒫_d|p variables;
   on {max ≤ 2 log(|𝒫_d|p) + 2ω_n}: F(S + l) − F(S − e₀) ≤ d log(D+1) + log p + ω_n − 2c_* + O(1)
   = d log(D+1) − log p − log n + ω_n + O(1).
 (γ) W(S − e′ + l | S − e′) ~ χ²₁, indexed by (P − e′, l): ≤ (D+1)^{d−1}p variables; on the corresponding event:
   F(S − e′ + l) − F(S − e′) ≤ (d−1)log(D+1) + log p + ω_n − c_* + O(1) = (d−1)log(D+1) − ½ log n + ω_n + O(1).
 Under (H2): (d−1)log(D+1) ≤ (½ − ε)log n and, as D + 1 ≤ p, d log(D+1) ≤ log p + (½ − ε)log n, so all three bounds
 are ≤ −ε log n + ω_n + O(1) → −∞. Under (H1) (d = 1): (d − 1)log(D+1) = 0 and log(D+1) ≤ log p, the same bounds
 hold with ε = ½. All thresholds are O(log n), so Lemma U applies. The failure probability is ≤ 3e^{−ω_n} → 0.
*(α), (β), (γ) under (H3).* Every statistic above is of the form Z_{S₀∪T,l} with T ⊆ S₀ᶜ, |T| ≤ d, l ∉ T:
(α) T = P − e₀, l = e₀; (β) the same plus T = P; (γ) T = P − e′. By Lemma LD,
|Z_{S₀∪T,l}| ≤ (Z^loc + ρ*V)/√(1 − ρ*²) with Z^loc := max_{l, L⊆𝔑(l), |L|≤d}|Z_{S₀∪L,l}| (≤ p2^{B′} Gaussians) and
V := max_{(L,F)}‖P_{Ṽ(L,F)}e‖/σ (subspaces of dim ≤ d indexed by disjoint null sets with |L| + |F| ≤ d: ≤ (2p + 1)^d of
them). By Lemma Q, w.p. ≥ 1 − 2e^{−ω_n}: (Z^loc)² ≤ 2 log p + 2B′ log 2 + 2ω_n and
V² ≤ d + 2√(d t) + 2t, t := d log(2p + 1) + ω_n, i.e. V² ≤ d·(2 log p + o(log n)). Hence, with λ := log p ≤ A log n,
½Z²_{S₀∪T,l} ≤ τ²λ + o(log n) uniformly. Lemma U then gives
 (α), (γ): F(bigger) − F(smaller) ≤ τ²λ − c_* + o(log n) = (τ² − 1)λ − ½ log n + o(log n) ≤ [(τ² − 1)A − ½]log n + o(log n);
 (β): F(S + l) − F(S − e₀) ≤ 2τ²λ − 2c_* + o(log n) = 2[(τ² − 1)λ − ½ log n] + o(log n).
By (★), (τ² − 1)A < ½, so all bounds → −∞. (If log p stays bounded the right-hand sides are −½ log n + O(ω_n).) ∎

**Remark (why d = 1 needs nothing).** W1-T37R's route asked for NA_d: F(S₀ ∪ P′ ∪ l) < F(S₀ ∪ P′) for all
|P′| ≤ d, a union of p^{d+1} one-degree-of-freedom events, which for d = 1 already costs p²·p⁻¹n^{−1/2}. The
event actually needed at S₀ + e is weaker: the deletion S₀ must beat S₀ + e + l, a *two*-degree-of-freedom event
with penalty 2c, of probability ≍ p⁻²n⁻¹, so the p² union is harmless. In general the needed events are (α), (β),
(γ); only (γ) — "a null added on top of P − e′ is not worth its penalty" — is a one-d.f. event indexed by
p·|𝒟|^{d−1} sets, and it is the only place where the dimension of the extras class bites.

---------------------------------------------------------------------------------------------------------

## 4. The main theorem

### Lemma A′ (Theorem A(A2–A3) for progress-closed regions). Status: PROVED.
Let 𝓡 ∋ S₀ be closed under (feasible) progress moves with Φ ≤ Φ_max on 𝓡. If TD′_P(𝓡) holds, then from every
S ∈ 𝓡 the greedy path consists of progress moves, stays in 𝓡 and reaches S₀ after τ(S) ≤ Φ(S) moves; the production
local search with cap ℓ ≥ Φ_max started at any centre S_c ∈ 𝓡 returns S₀ with local_certified and without
local_limit, and after it Ŝ = S₀ up to exact score ties (W1-T37R Lemma 0(c)).
*Proof.* On D_S, max over progress neighbours > F(S), so M(S) ≠ ⊥, and the global argmax over all neighbours is
attained only at progress moves (ties among them are broken lexicographically, still progress); so M(S) ∈ 𝓡
(closure) and Φ drops by ≥ 1. By induction the path reaches a state with Φ = 0, i.e. S₀, after ≤ Φ(S) moves, and
M(S₀) = ⊥ by (L). The production search performs at most ℓ ≥ Φ_max moves and then scans once more; the scan at S₀
finds no improvement. ∎

### Theorem W (refined T37(iii): TD′ with probability → 1). Status: PROVED (candidate).
Regime R1 with s₀, a ≤ s₀ and d fixed. Let 𝒟 = 𝒟_n ⊆ S₀ᶜ be deterministic (X-measurable). Assume EX-A, G, R,
SE_λ(d+1), BM-∞, PGD(η) on R_{a,d}(𝒟) for a fixed η ∈ (0, 1], and one of (H1), (H2), (H3) of Lemma S. Then
  P₀(TD′_P(R_{a,d}(𝒟))) → 1.
Consequently, for every (data-dependent) centre S_c and all n with ℓ_n ≥ a + d (eventually, since ℓ_n → ∞),
  P(the production local search from S_c does not return S₀ with local_certified) ≤ P(S_c ∉ R_{a,d}(𝒟)) + o(1),
and on the complement Ŝ = S₀ after the search (up to exact ties, a null event under G).

*Proof.* *States with m(S) ≥ 1.* For each such S ∈ R_{a,d}(𝒟) fix S′(S) ∈ 𝒫(S) minimising ‖r_{S′}‖² (ties
lexicographic; deterministic). Consider the family 𝒫_n of pairs (A, B) = (S′(S), S″) with S″ ∈ {S} ∪ 𝒩(S) ∪ ℛ(S).
All sets lie in 𝒯 (they are ⊆ S₀ ∪ P ∪ {x}, |P| ≤ d). Both A and B are neighbours of S (or S itself), so
|A∖B|, |B∖A| ≤ 2. Gap: for B = S, g = ρ⁺(S); for B non-progress, g = ρ⁺(S) − red(B) ≥ ρ⁺ − ρ⁰ ≥ ηρ⁺ by PGD(η). So
g ≥ ηρ⁺(S) ≥ ηNφ₀⁴θ²_min =: γ_n (Lemma 1.2; λ_min(G_{S∪S₀}) ≥ Nφ₀² by SE_λ(d)). Geometry: with U := A ∪ B,
Lemma 1.1(c) gives ‖r_A − r_B‖² ≤ 2(‖r_A‖² − ‖r_U‖²) + 2(‖r_B‖² − ‖r_U‖²) = 2g + 4(‖r_A‖² − ‖r_U‖²) ≤ 2g + 4‖r_S‖²
≤ 2g + (4s₀/φ₀²)ρ⁺ ≤ (2 + 4s₀/(ηφ₀²))g =: C₁g (Lemma 1.2; ‖r_A‖² ≤ ‖r_S‖² because red(A) = ρ⁺ > 0). Count:
|𝒫_n| ≤ 2^{s₀}(|𝒟|+1)^d (1 + (s₀ + d + 1)(p + 1)), so L_n = O(log n). BM-∞ gives γ_n ≥ ηφ₀²M_nσ² log n·N/n, so
γ_n/L_n → ∞. Lemma G: w.p. → 1, F(S′(S)) > F(S″) for all pairs, i.e. D_S holds for every S ∈ R_{a,d}(𝒟) with m ≥ 1.
*States with m(S) = 0* (S = S₀ ∪ P, P ⊆ 𝒟, 1 ≤ |P| ≤ d) *and condition (L)*: Lemma S.
The intersection of the two events has probability → 1 and is TD′_P(R_{a,d}(𝒟)). The consequence follows from
Lemma A′ (R_{a,d}(𝒟) is progress-closed with Φ_max = a + d), applied on this single event — so the data dependence
of S_c is harmless. Exact ties have probability 0 under G (W1-T37R Prop 1's analyticity argument). ∎

**Which hypothesis does what.**
- PGD(η) is used only at states with a missing truth; SE_λ(d+1) and BM-∞ make the population gap
  ηNφ₀⁴θ²_min beat the noise √(gap·log n) and the penalties O(log n).
- At supersets of S₀ the population gap is zero and everything is a χ² tail against the BB(1,p) + g-prior
  penalty c ≈ ½ log n + log p. (H1)/(H2)/(H3) are three ways of paying for the union bound there.
- "Anchored SE" means SE_λ(d+1): only the sets S₀ ∪ J with |J| ≤ d + 1 are used.

### Corollary W′ (sufficient design conditions). Status: PROVED (composition).
Theorem W holds with PGD(η) replaced by either
 (i) GERC(R_{a+1,d}(𝒟); η₁) ∧ TRC(R_{a,d}(𝒟); η₂) (Prop P1), with η = min(η₁, η₂); or
 (ii) BO(𝒢) with one truth per group and (B1)–(B3) (Prop P2); for equicorrelated groups (Cor P2′) this is the
      explicit inequality η*(d) > 0, i.e. max_g ρ_g < 1 (θ ratios enter only through (B3)).
For Gaussian random designs (Cor P6) it suffices that the population Σ satisfies SE_λ(d+1) and one of these, with
bounded θ_max/θ_min; under (H3) also LD♭ for Σ with (★) strict (stability, Lemma P5).

---------------------------------------------------------------------------------------------------------

## 5. LD cannot be dropped for d ≥ 2 with unrestricted extras

### Proposition C-LD (equicorrelated nulls). Status: COUNTEREXAMPLE (proof + script `scripts/ld_counterexample.py`).
Fix r ∈ (½, 1) and θ ≠ 0. For each n let N = n − 1, m := N − 2, p := m + 1, and let v₀, f, g₁, …, g_m be orthonormal in
ℝ^N. Truth: x₁ = √N v₀ (s₀ = 1, θ₁ = θ). Nulls: x_{1+i} = √N(√r f + √(1−r) g_i), i = 1..m. Then G, R (p ≤ n),
SE_λ(j) for every j (λ_min = 1 − r), BM-∞ (θ fixed), PGD(1) on R_{1,d} for every d (nulls are orthogonal to x₁),
GERC with ERC ≡ 0, and TRC (vacuous, s₀ = 1) all hold; LD♭ fails for every ρ* satisfying (★) (here
ρ(l, {e₁,e₂} | S₀) = r√(2/(1+r))), and (H2) fails for 𝒟 = all nulls. Nevertheless
  P₀(∃ e₁ ≠ e₂ : F(S₀ ∪ {e₁, e₂}) > max_i F(S₀ ∪ {e₁,e₂}∖{e_i})) → 1,
so D_S fails at S = S₀ ∪ {e₁, e₂} ∈ R_{0,2}: TD′_P(R_{0,2}) fails w.p. → 1 (and so does the d = 2 conclusion of
Theorem W). For d = 1 Theorem W applies to this design ((H1)).

*Proof.* Put F₀ := ⟨f, e⟩/σ, G_i := ⟨g_i, e⟩/σ: iid N(0,1). The unit null directions x̂_i = √r f + √(1−r)g_i have
Z_i := ⟨x̂_i, e⟩/σ = √r F₀ + √(1−r)G_i, ⟨x̂_i, x̂_k⟩ = r (i ≠ k), and they are orthogonal to x₁, so residualising on S₀
does nothing to them. At S = S₀ ∪ {a, b} the deletion statistic of a is
t_a := Z_{S₀+b, a} = (Z_a − rZ_b)/√(1 − r²) = √(r(1−r)/(1+r))F₀ + (G_a − rG_b)/√(1+r),
and symmetrically for b. Let a := argmax_i G_i, b := argmin_i G_i, u_m² := 2 log m − log log m − 2ω_m. Since
Φ̄(u) ≥ φ(u)/(2u) for u ≥ 1 and φ(u_m) = √(log m)e^{ω_m}/(m√(2π)), mΦ̄(u_m) ≥ e^{ω_m}/(4√π) → ∞, so P(max G ≥ u_m, min G ≤ −u_m) → 1; then a ≠ b,
G_a − rG_b ≥ (1+r)u_m and |G_b − rG_a| ≥ (1+r)u_m, and with |F₀| ≤ ω_m,
min(t_a², t_b²) ≥ (1 + r)u_m² − 2√(1+r)u_m ω_m ≥ (1 + r)(2 log m) − O(√(log m)·ω_m).
By Lemma R (lower direction: RSS_S = RSS_{S−a} − σ²t_a², −ν log(1 − x) ≥ νx, ν/N ≥ ½ and
RSS_{S−a} ≤ ‖e‖² ≤ Nσ²(1 + δ_n)), F(S) − F(S − a) ≥ ½t_a²/(1 + δ_n) − c₂ − 2C₀, with c₂ = ½ log(n+1) + log((2p−3)/3) ≤ ½ log n + log m + O(1).
So F(S) − F(S − a) ≥ (1 + r)log m − ½ log n − log m − o(log n) = r log m − ½ log n − o(log n) → +∞ because r > ½ and
log m = log n + o(1); the same for b. ∎
*Interpretation.* With p ≍ n^A the same computation needs r > 1/(2A): the threshold scales like (★)'s
(τ² − 1)A < ½, so LD♭'s A-dependent constant is the right kind of condition (it is sufficient; C-LD shows the
order 1/A cannot be removed; the constant in (★) is off by a factor ≈ 3–4 from C-LD's 1/(2A)).

---------------------------------------------------------------------------------------------------------

## 6. What is "weakest" (summary of the logical position)

- For TD′_P(R_{a,d}(𝒟)) w.p. → 1 under G, R, SE, BM-∞: PGD(η) with η > 0 is sufficient (Theorem W) and its
  negation with a margin forces failure (Prop P4). So PGD is the sharp population condition, up to the boundary
  max ρ⁰/ρ⁺ → 1. The design conditions GERC (θ-free) + TRC, and the exact block conditions (B1)–(B3), are checkable
  sufficient conditions; (B1)–(B3) are also necessary under BO.
- LD is needed only at supersets of S₀ and only for d ≥ 2 extras drawn from an unrestricted class (C-LD). It can
  be dropped for d = 1, or when the extras come from a deterministic class of size n^{o(1)} — e.g. the nulls in the
  truth blocks of the start partition, |𝒟| ≤ s₀(B − 1) ≤ 15s₀ — and otherwise weakened to the constant-threshold
  LD♭ with (★).
