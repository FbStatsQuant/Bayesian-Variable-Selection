# W3-FAMC — A. Assembly proof of Corollary FAMC (v1.0, 2026-11-17; lead Claude Opus 5.5, high)

This file proves `STATEMENT.md` §1 (v1.1). It introduces no new lemma: every step is either a citation (with path:line)
or a finite linear-algebra computation written out in full. Aliases are as in `STATEMENT.md` (header). In addition:
[RM2] §3.2 = `Theory_work/Wave3/W3-RM2/STATEMENT.md:172-202`.

**Target.** It suffices to verify, for every n ≥ n₀, the hypotheses of `W3-RM2-R:RM2-R-plus@1.0.1` ([RM2R] `:177-182`):
the hypotheses of RM2-R, namely (T1-R), (FL-R), (V-R), (L-R^b) with 15ϱ + b < ½, and (W-R) ([RM2] `:172-202`). These
are conditions on (Σ_n, θ*) and a deterministic Q only. Setting R ([RM2] `:49-58`, the standing setting) is §0 of the
statement. RM2-R-plus then gives [SAND(Q)], [TL(Q)], [NA(Q)], [POST] and [MODE], and hence RM0-plus (a) and (b⁺): a data
event 𝒢⁺_n = 𝓜_n ∩ 𝒦_n with P(𝒢⁺_n) → 1 on which every admissible output run reports Ŝ⁺ = S₀. Under (D), which is (S4)
(identity B6.6′, [RV] row thm6), it also gives delivery and P(Ŝ⁺ = S₀) → 1. These are the conclusions of reader
Theorem 6 as stated in `STATEMENT.md` §1. In both families we fix **b = ¼ and ϱ = 1/120**, so 15ϱ + b = ⅜ < ½.

Notation: Γ^U_{lk} := Cov(W_l, W_k | W_U) for l, k ∉ U ([VIS] `:22`); Γ^U_{ll} = Var(W_l | W_U).

---

## A.1 Block family (BLK)

Let G(l) denote the group containing l. Put Q₀ := ∪{G_i : G_i ∩ S₀ ≠ ∅}; then S₀ ⊆ Q₀ and |Q₀| ≤ g s₀. Set Q := Q₀ if
p ≥ 2|Q₀| + 32s₀ + 1, and Q := [p] otherwise.

**B.0 (localisation to groups).** Let U ⊆ [p] and l, k ∉ U.
(a) If G(l) ≠ G(k), then Γ^U_{lk} = 0.
(b) If G(l) = G(k) =: G, then Γ^U_{lk} = Γ^{U∩G}_{lk}. The right side is computed from Σ_{n,GG} alone. In particular,
Var(W_l | W_U) = Var(W_l | W_{U∩G(l)}).
*Proof.* Order U by groups. Σ_{UU} is block-diagonal with diagonal blocks Σ_{U_i U_i}, U_i := U ∩ G_i, each positive
definite (λ_min(Σ_n) ≥ c > 0). Hence Σ_{UU}⁻¹ is block-diagonal with blocks Σ_{U_iU_i}⁻¹. The row Σ_{lU} vanishes outside
U ∩ G(l), and the column Σ_{Uk} vanishes outside U ∩ G(k). Therefore
Σ_{lU}Σ_{UU}⁻¹Σ_{Uk} = Σ_{l,U_{G(l)}} Σ⁻¹_{U_{G(l)}U_{G(l)}} Σ_{U_{G(l)},k}.
In (a), the last factor is 0 because U_{G(l)} ⊆ G(l) ≠ G(k); also Σ_{lk} = 0, so Γ^U_{lk} = 0. In (b), the right side is
Σ_{lk} − Σ_{l,U∩G}Σ⁻¹_{U∩G,U∩G}Σ_{U∩G,k} = Γ^{U∩G}_{lk}. (For U ∩ G = ∅, read Γ^∅_{lk} = Σ_{lk}.) ∎

**B.1 (T1-R), (FL-R) [reader (A5)].** By Cauchy interlacing, λ_min(Σ_{n,S}) ≥ λ_min(Σ_n) ≥ c for every S ⊆ [p]. This
gives (FL-R) (sets of size ≤ 16 + s₀ and Q ∪ {l}). It also gives (T1-R) through its stated sufficient form
"λ_min(Σ_n) ≥ c" ([RM] `:129-133`).

**B.2 (V-R) [reader (A3)].** Fix j ∈ S₀ and U ∌ j with |U| ≤ 15. By (VIS-0) ([VIS] `:30-31`),
Cov(W_j, Wᵀθ* | W_U) = Σ_{k∈S₀∖U} θ*_k Γ^U_{jk} (the terms k ∈ U vanish by convention). By B.0(a), the terms with
G(k) ≠ G(j) vanish. With G := G(j) and B.0(b):
  Cov(W_j, Wᵀθ* | W_U) = Σ_{k∈(G∩S₀)∖U} θ*_k Γ^{U∩G}_{jk} = Cov_G(W_j, Σ_{k∈G∩S₀} θ*_k W_k | W_{U∩G}),   (B.2.1)
where Cov_G is the partial covariance of the Gaussian vector W_G ~ N(0, Σ_{n,GG}).
- *(BLK-1), or |G ∩ S₀| = 1 under (BLK-s).* Then (B.2.1) equals θ*_j Var(W_j | W_{U∩G}). Its absolute value is
  ≥ θ_lo λ_min(Σ_{(U∩G)∪{j}}) ≥ θ_lo c (the variance bound of (VIS-0), [VIS] `:31`).
- *(BLK-s), |G ∩ S₀| ≥ 2.* Apply (VIS-a) ([VIS] `:32-35`) to the positive definite correlation matrix Σ_{n,GG} (dimension
  |G| ≤ g), the coefficient vector (θ*_k)_{k∈G} (support G ∩ S₀, with entries in [θ_lo, θ_hi] in absolute value), the
  signs (d_l)_{l∈G} of (BLK-s), and the conditioning set U ∩ G ∌ j. (BLK-s) asks d_k sgn θ*_k to be constant on all of
  G ∩ S₀, which implies VIS-a's alignment on each connected component of the graph of Σ_{n,GG}⁻¹. VIS-a gives
  |(B.2.1)| ≥ |θ*_j| Var(W_j | W_{U∩G}) ≥ θ_lo c.
- *(BLK-g).* Apply (VIS-b) ([VIS] `:36-40`) to Σ_n directly: c₁₆(Σ_n) ≥ λ_min(Σ_n) ≥ c, so c̲ ≥ c, and δ :=
  inf_{n≥n₀} dist(ϑ_n, B) > 0 by hypothesis. This gives |Cov(W_j, Wᵀθ* | W_U)| ≥ c·δ for every n ≥ n₀.

So (V-R) holds with a₀ = θ_lo c, or a₀ = c δ under (BLK-g). The smallness of B in (BLK-g) (finitely many group matrices
⇒ finitely many local patterns) is (VIS-d)(i), [VIS] `:46-51`. It is explanatory only and is not used.

**B.3 (L-R^b) [reader (A4)].**
- *Q ⊇ S₀, (L-size^b), (L-feas).* In both cases |Q| ≤ max(g s₀, 2g s₀ + 32 s₀) =: q̄, a constant, so |Q| ≤ n^{1/4}
  eventually. If Q = Q₀ (p ≥ 2|Q₀| + 32s₀ + 1), then K = min(p, ⌊n/2⌋) ≥ 2|Q| + 32s₀ + 1 once ⌊n/2⌋ ≥ q̄ + 32s₀ + 1, and so
  |Q| ≤ K. If Q = [p], then p ≤ q̄ and K = p = |Q| once ⌊n/2⌋ ≥ q̄. This is (L-feas) ([RM2] `:134`) for n ≥ n₀.
- *(L-gain-R), ϖ_n = 0.* If Q = [p], it is vacuous. Otherwise let l ∉ Q = Q₀; then G(l) ∩ S₀ = ∅. For j ∈ S₀ ∖ U,
  G(j) ≠ G(l), so Γ^U_{lj} = 0 by B.0(a).
- *(L-loc-R), r_n = 0.* For l ∉ Q put H_l := Q ∪ G(l) ⊇ {l} ∪ S₀, so |H_l| ≤ q̄ + g ≤ n^{1/120} eventually. Let
  U ⊆ [p] ∖ {l}, |U| ≤ 15, U₀ := U ∩ H_l, and v ∈ U ∖ H_l. Then v ∉ G(l), so Γ^{U₀}_{lv} = 0 by B.0(a). For j ∈ S₀ ∖ U₀,
  G(j) ⊆ Q ⊆ H_l while v ∉ H_l, so G(v) ≠ G(j) and Γ^{U₀}_{jv} = 0.

**B.4 (W-R) [reader (A6)].** For every l put N_l := (G(l) ∩ Q) ∖ {l}, so |N_l| ≤ g − 1 =: ν_n = o(log n). Let T ∈ 𝓛
(S₀ ⊆ T ⊆ Q) with l ∉ T, and put A := T ∩ N_l = T ∩ G(l) (since T ⊆ Q and l ∉ T). Order T as (A, T ∖ A). Σ_{TT} is
block-diagonal with blocks Σ_{AA}, Σ_{T∖A,T∖A}, because the cross entries join different groups. Also Σ_{T∖A,l} = 0.
Hence the population regression is
  β̄_{T,l} = Σ_{TT}⁻¹Σ_{Tl} = (Σ_{AA}⁻¹Σ_{Al}, 0) = β̄_{A,l} (zero-padded; = 0 if A = ∅).
So ‖β̄_{T,l} − β̄_{T∩N_l,l}‖₁ = 0 =: L_n. By B.0(b), Var(W_l | W_{T∩N_l}) = Var(W_l | W_T), so η_n = 0. This is RM's
(D-loc) ([RM] `:154-156`) with ν_n = g − 1, L_n = 0, η_n = 0. Since L_n² log(|Q| + 1) = 0, it is also (D-loc^b)
([RM2] `:201-202`). `W3-RM2:D-to-W@1.0.3` ((P9): "(D-loc^b) ⇒ (D-R^b)" and "(D-R^b) ⇒ … (W-R)") then gives (W-R).
In the reader's form: (A6) holds with N_l, ν_n = g − 1 and L_n = 0.

**B.5 Conclusion (BLK).** By B.1–B.4, all hypotheses of RM2-R hold with b = ¼ and ϱ = 1/120. Apply RM2-R-plus. ∎

---

## A.2 AR family (AR)

**A.0 (membership in E2's class).** E2 ([L6] `:164-263`) applies to unit-diagonal positive definite Σ_n indexed by an
injection π: [p] → ℤ, with spectrum in [c, C] and |Σ_{jk}| ≤ K_dec(1 + d(j, k))^{−α} for some α > 2 ([L6] `:35-38`). It
also needs Gaussian rows, independent Gaussian noise, fixed s₀, p ≤ n^A, fixed standardised signals in [θ_lo, θ_hi], and
PTV(a₀) ([L6] `:170-174`). For Σ_{lk} = ρ^{|l−k|} take π = id and α = 3.
- Unit diagonal: ρ⁰ = 1.
- Spectrum: by [GROW5] (P1) (`:23-25`), λ(Σ) ∈ [(1 − |ρ|)/(1 + |ρ|), (1 + |ρ|)/(1 − |ρ|)]. For ρ < 0, Σ = DΣ_{|ρ|}D with
  D = diag((−1)^i) has the same spectrum ([GROW5] `:18-20`). For ρ = 0, Σ = I.
- Decay: K_dec := sup_{d≥0} |ρ|^d(1 + d)³ < ∞ (it is 1 for ρ = 0).
The remaining E2 inputs are §0 of the statement and (A2).

**A.1 (T1-R), (FL-R), (L-size^b), (L-feas), (L-gain-R), (L-loc-R), (W-R).** These are exactly E2's verified list
([L6] `:211-248`), for every fixed b ∈ [1/(2α), ½) = [1/6, ½). Take b = ¼ and E2's ϱ = (½ − b)/30 = 1/120. E2 uses no
truth-separation condition beyond PTV ([L6] `:174`).
*Cross-check, AR-specific:* by [GROW5] (P4) (`:31-42`, after the sign reduction), 0 ≤ Cov(W_l, W_k | W_U) ≤ |ρ|^{|l−k|} for
every U. So E2's (L-gain-R) and (L-loc-R) bounds hold in this case with K_15 replaced by 1. The PROVED-CHECKED C-GROW
facts thus confirm the leakage half independently of Lemma BC.

**A.2 (V-R) = PTV(a₀)** ([RM] `:135-136`).
- *(AR-s), ρ ≠ 0.* Apply (VIS-a) through its instance (VIS-e) ([VIS] `:54-58`): d_l = s^l with s = sgn ρ. The graph of
  Σ⁻¹ (tridiagonal, off-diagonal entries −ρ/(1 − ρ²) ≠ 0) is a path, so alignment is required globally; this is (AR-s).
  Then |Cov(W_j, Wᵀθ* | W_U)| ≥ |θ*_j| Var(W_j | W_U) ≥ θ_lo c₁₆ ≥ θ_lo(1 − |ρ|)/(1 + |ρ|).
- *ρ = 0.* Apply (VIS-a) with D = I: Σ⁻¹ = I has no nonzero off-diagonal entries, so the graph has no edges and the
  alignment condition is vacuous. Margin θ_lo.
- *(AR-sep).* [GROW5] (G3b) (`:58-61`): for j ∈ S₀ and **any** U ∌ j,
  |Cov(x_j, μ | x_U)| ≥ |θ*_j| Var(x_j | x_U) − Σ_{k∈S₀∖(U∪{j})} |θ*_k| |ρ|^{|j−k|} ≥ ½|θ*_j|(1 − ρ²)/(1 + ρ²),
  with μ = Σ_k θ*_k x_k the population signal ([GROW5] (P5), `:43-46`), i.e. Cov(W_j, Wᵀθ* | W_U). The inequality uses only the
  population facts (P3), (P4) and separation; it is part of the proof of claim (a), `C-GROW:C5a` (PROVED-CHECKED). The
  sign reduction θ* → Dθ* leaves |Cov| and the separation condition unchanged. Margin ½θ_lo(1 − ρ²)/(1 + ρ²).
- *(AR-g).* (VIS-b) with c̲ ≥ (1 − |ρ|)/(1 + |ρ|) (the bound of (VIS-e)) and δ > 0: margin c̲δ. B is a countable union of
  hyperplanes by (VIS-d)(ii) ([VIS] `:52-53`); this is explanatory only.

**A.3 Conclusion (AR).** E2 verifies the remaining hypotheses of RM2-R given PTV(a₀), which A.2 supplies. Apply
RM2-R-plus. ∎ The status of this half is that of E2 together with its inputs (`STATEMENT.md` §4); see DP1.

---

## A.3 Reader hypotheses, for the record (not used by the proof)

In both families: (A3) is A.2 / B.2, (A4) is B.3 / E2, (A5) is B.1 / E2, and (A6) is B.4 / E2's (0.1) with
N_l = Q ∩ {v ≠ l : |v − l| ≤ ⌊√log n⌋} ([L6] `:97-103`). These are the reader's sufficient forms; the proof above goes
directly to the master and does not use the bridges B6.1–B6.5.
