# L4 — Visibility bridges (B-V2), (B-V1) ⇒ [VIS(κ; Q)]

Status: **PROVED (by this seat, unchecked)**.
Statement proved: `STATEMENT.md` §4 [VIS(κ; Q)]; §5.2 (B1) (visibility part), (B-V1), (B-V2).
Uses `lemmas/L2_TK.md` (𝓔^blk, (TK-a), (TK-d)–(TK-f), κ_E, ω_n ≤ ω̄_n, ϑ_n, n₁) and `lemmas/L1_AGG_FLOOR.md` (AGG-d).

## L4.0 Setting and the event 𝓧

Setting F, (E), (GF-16), s₀ ≥ 1 (for s₀ = 0: Ξ(Q) = 0 = e_n by definition and [VIS] is trivial), a deterministic Q ⊇ S₀ with
|Q| ≤ K, the actual partition (blocks ≤ 16). A truth block is a b with U*_b = S₀ ∩ C_b ≠ ∅; there are at most s₀.
  ζ_n := 4 log(2^8·3^{16}·s₀·log n)   (= 4 log log n + O(1)),
  **𝓧 := {‖(P_W − P_U)ε‖² ≤ σ²ζ_n for every truth block b and all U ⊆ W ⊆ C_b}.**
**P(𝓧ᶜ) ≤ 1/log n.** *Proof.* P_W − P_U is a deterministic projection of rank d = |W| − |U| ≤ 16 ((TK-e)), so
P(‖(P_W − P_U)ε‖² > σ²ζ) ≤ 2^{d/2}e^{−ζ/4} ≤ 2^8e^{−ζ/4}; a block has at most 3^{16} nested pairs; union over ≤ s₀·3^{16} pairs. ∎
In particular, on 𝓧: Z²_{U,j} ≤ ζ_n for every truth block b, U ⊆ C_b, j ∈ C_b ∖ U.
For vectors a, b and ε₁ ∈ (0, 1): **(Q±)** (1 − ε₁)‖a‖² − (1/ε₁ − 1)‖b‖² ≤ ‖a + b‖² ≤ (1 + ε₁)‖a‖² + (1 + 1/ε₁)‖b‖²
(from 2|⟨a, b⟩| ≤ ε₁‖a‖² + ‖b‖²/ε₁).

**(B1), visibility.** (GF-16), (V-c) and (V-m) quantify over all small sets of [p]; the sets used below (subsets of one
block of size ≤ 16) are among them, for every partition with blocks of size ≤ 16.

## L4.1 Bridge (B-V2): margin visibility

**Proposition L4.1.** Assume (V-m) at n with constants (c_m, ε₀) for Q, and let κ ∈ (0, c_m/2). There is
n₃ = n₃(κ, A, M, σ², g_*, s₀, c_m, ε₀) such that for n ≥ n₃, on 𝓔^blk ∩ 𝓧:
  **ω^Q(U)·r_b(U)/r_b(T_b(U)) ≤ 2^{−16}n^{−κ} for every truth block b and every U ⊆ C_b with U*_b ⊄ U; hence Ξ(Q) ≤ n^{−κ}.**
Consequently P(Ξ(Q) > n^{−κ}) ≤ P((𝓔^blk)ᶜ) + 1/log n → 0 for every κ < c_m/2: [VIS(κ; Q)] with κ_V = c_m/2.

*Proof.* Fix b and U. Put V := U*_b, D := V ∖ U ≠ ∅, R := (U ∩ Q) ∖ S₀, N := U ∖ Q, d := |D|, a := |N|, T := V ∪ R = T_b(U),
W := V ∪ R ∪ N = U ∪ D. Then U = (V ∖ D) ∪ R ∪ N (as U ∩ S₀ = V ∖ D), |V| + |R| + |N| = |W| ≤ 16, U ⊆ W, T ⊆ W, all inside C_b,
and |U| − |T| = a − d. This is an instance of the quantifier of (V-m); write L₁ := Λ_U − Λ_W, L₂ := Λ_T − Λ_W and
P := (1 + 2A)(d − a)₊ + c_m, so that (V-m) reads
  L₁/τ²_U ≥ P·log n + (1 + ε₀)·L₂/τ²_W.                                                                   (4.1)
*Constants.* ε₁ := min{ε₀/(2(2 + ε₀)), (c_m − 2κ)/(2[16(1 + 2A) + c_m])} ∈ (0, ½). Then
(1 − ε₁)(1 + ε₀) ≥ (1 + ε₁) + ε₀/2 ≥ (1 + ε₁)(1 + ε₀/3) and (1 − ε₁)P ≥ (1 + 2A)(d − a)₊ + κ + c_m/2 ((d − a)₊ ≤ 16).
*Step 1 (table ratio).* By (TK-d): log[r_b(U)/r_b(T)] = ½(d − a) log(n + 1) − (A₁ − A₂) + (R_U − R_T), where
A₁ := ν log(RSS_U/RSS_W) ≥ 0, A₂ := ν log(RSS_T/RSS_W) ≥ 0, |R_U − R_T| ≤ 2κ_E.
*Step 2 (A₁ from below).* By (TK-e), (Q±) and 𝓧: RSS_U − RSS_W = ‖(P_W − P_U)(μ + ε)‖² ≥ (1 − ε₁)L₁ − σ²ζ_n/ε₁. By (f1) and
σ² ≤ τ²_U: A₁ ≥ (1 − ε₁)L₁/(2τ²_U(1 + ω_n)) − ζ_n/(2ε₁).
*Step 3 (A₂ from above).* RSS_T − RSS_W ≤ (1 + ε₁)L₂ + (1 + 1/ε₁)σ²ζ_n; by (f2) and σ² ≤ τ²_W:
A₂ ≤ (1 + ϑ_n)(1 + ε₁)L₂/(2τ²_W) + (1 + ϑ_n)(1 + 1/ε₁)ζ_n/2. (No smallness of the gains of N is needed: (f2) is exact in
this direction, and it is the reason why τ²_W stands on the right of (V-m).)
*Step 4.* Put 1 + ϑ̄_n := (n + 0.02)/((n − 1)(1 − ω̄_n)) for n ≥ n₁; then ϑ_n ≤ ϑ̄_n → 0, and ϑ̄_n depends only on (n, A).
Insert (4.1) in Step 2 and subtract Step 3:
  A₁ − A₂ ≥ (1 − ε₁)P log n/(2(1 + ω_n)) + [L₂/(2τ²_W)]·[(1 − ε₁)(1 + ε₀)/(1 + ω_n) − (1 + ϑ_n)(1 + ε₁)] − C₁ζ_n,
C₁ := 1/(2ε₁) + (1 + 1/ε₁) (for ϑ_n ≤ 1). For n ≥ n₃ we have (1 + ω̄_n)(1 + ϑ̄_n) ≤ 1 + ε₀/3, so the second bracket is ≥ 0
(L₂ ≥ 0), and A₁ − A₂ ≥ [(1 + 2A)(d − a)₊ + κ + c_m/2]·log n/(2(1 + ω_n)) − C₁ζ_n.
*Step 5 (price).* Π := log ω^Q(U) + ½(d − a) log(n + 1). If d ≥ a: Π = (d − a)[log(2p) + ½ log(n + 1)]
≤ ½(1 + 2A)(d − a) log n + 16(log 2 + ½ log(5/4)) (p ≤ n^A, n ≥ 4). If a > d: Π = (a − d)[log(c_Q/p) − ½ log(n + 1)] ≤ 15 log(16s₀),
since c_Q/p = (|Q| + 15s₀)/p ≤ 1 + 15s₀ ≤ 16s₀ (|Q| ≤ K ≤ p). In both cases Π ≤ ½(1 + 2A)(d − a)₊ log n + C₂, C₂ := 16 log(32s₀).
*Step 6.* log[ω^Q(U)r_b(U)/r_b(T)] = Π − (A₁ − A₂) + (R_U − R_T)
  ≤ ½(1 + 2A)(d − a)₊ log n·[1 − 1/(1 + ω_n)] − (κ + c_m/2) log n/(2(1 + ω_n)) + C₂ + C₁ζ_n + 2κ_E
  ≤ −(κ + c_m/2) log n/(2(1 + ω̄_n)) + 8(1 + 2A)ω̄_n log n + C₂ + C₁ζ_n + 2κ_E.
Since (κ + c_m/2)/2 > κ, ω̄_n log n → 0 and ζ_n = o(log n), the right side is ≤ −κ log n − 16 log 2 for n ≥ n₃.
*Step 7.* For fixed T′ the sum defining Ξ_b(Q) has at most 2^{16} terms (U ⊆ C_b), each ≤ 2^{−16}n^{−κ}. ∎

## L4.2 Bridge (B-V1): constant-level visibility

**Proposition L4.2.** Assume (V-c) at n with c_V > 1 + 2A; κ_V := (c_V − 1 − 2A)/2; let κ ∈ (0, κ_V). There is
n₄ = n₄(κ, A, M, σ², g_*, s₀, c_V) such that for n ≥ n₄, on 𝓔^blk ∩ 𝓧: **e_n ≤ 2^{−16}n^{−κ}**, and therefore, on
𝓔^blk ∩ 𝓧 ∩ {c_QU_Q ≤ 1}: **Ξ(Q) ≤ n^{−κ}**.

*Proof.* Let b be a truth block, U ⊆ C_b, j ∈ U*_b ∖ U. Then U ⊆ [p] ∖ {j}, |U| ≤ 15, so (V-c) gives δ²_{U,j} ≥ c_Vτ²_U log n. By
(TK-d), log[r_b(U)/r_b(U ∪ j)] = ½ log(n + 1) − ν log(RSS_U/RSS_{U∪j}) + (R_U − R_{U∪j}). By (TK-e), (Q±), 𝓧:
RSS_U − RSS_{U∪j} = (δ_{U,j} + σZ_{U,j})² ≥ (1 − ε₁)δ²_{U,j} − σ²ζ_n/ε₁ ≥ τ²_U[(1 − ε₁)c_V log n − ζ_n/ε₁]. With (f1) and
ε₁ := min{½, (κ_V − κ)/(2c_V)}:
  log[r_b(U)/r_b(U ∪ j)] ≤ ½ log(n + 1) − [c_V − (κ_V − κ)/2] log n/(2(1 + ω̄_n)) + ζ_n/(2ε₁) + 2κ_E
   ≤ −[(c_V − 1)/2 − (κ_V − κ)/4] log n + (c_V/2)ω̄_n log n + ζ_n/(2ε₁) + 2κ_E + ½ log(5/4)
   ≤ −[(c_V − 1)/2 − (κ_V − κ)/2] log n − 17 log 2   for n ≥ n₄.
Now let U ⊆ C_b with a′ := |U*_b ∖ U| ≥ 1; add the missing truths one at a time, U = U⁰ ⊂ U¹ ⊂ ⋯ ⊂ U^{a′} = U ∪ U*_b. Each
step is of the kind just bounded, so [r_b(U)/r_b(U ∪ U*_b)]^{1/a′} ≤ 2^{−17}n^{−(c_V−1)/2+(κ_V−κ)/2}, and with 2p ≤ 2n^A:
e_n ≤ 2^{−16}n^{A−(c_V−1)/2+(κ_V−κ)/2} = 2^{−16}n^{−(κ_V+κ)/2} ≤ 2^{−16}n^{−κ}. In particular e_n ≤ 1, and (AGG-d) (which needs
c_QU_Q ≤ 1) gives Ξ_b(Q) ≤ 2^{16}max(e_n, e_n^{16}) = 2^{16}e_n ≤ n^{−κ}. ∎

**Corollary L4.3 ([VIS(κ; Q)] under (V-c)).** If moreover (AL) holds for Q with level vector h, then
P(Ξ(Q) > n^{−κ}) → 0 for every κ < κ_V. *Proof.* By Proposition L3.4(a) (`lemmas/L3_LEAK.md`) and (B1),
U_Q = O_P(n^{−1/2}𝔏^b_n(Q; h)), and c_Q ≤ 16s₀(|Q| + 1), so c_QU_Q = O_P(ϱ_n(Q; h)) → 0 in probability; apply L4.2. ∎
(The explicit form is in `lemmas/L5_ASM_STARTF.md`.)

## L4.3 Remarks
1. (V-c) asks the gain of each truth at level c_V > 1 + 2A given **every** 15-set; L4.2 uses it only for subsets of the
   truth's own block. (V-m) asks only for a margin of the missing truths' joint gain over the gain of the substituting
   nulls; L4.1 uses every instance (V, D, R, N) inside a truth block.
2. Both propositions hold on 𝓔^blk ∩ 𝓧, an event that does not depend on (κ, c_V, c_m, ε₀); the thresholds n₃, n₄ depend
   only on the fixed constants. This gives the uniformity used in (T1)(d).
3. 𝓧 controls only the at most s₀·3^{16} projections inside truth blocks, at the level ζ_n = O(log log n) = o(log n). The
   cruder bound σ²t_n of 𝒟₂ would cost a constant multiple of log n and is not used here.
