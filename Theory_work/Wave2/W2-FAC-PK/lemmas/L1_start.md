# L1 — The start mode for K < p ≤ n − 1 (claim (P1))

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol xhigh, reviews/R03_L0L1L2_check_sol.md):
VERIFIED-WITH-AMENDMENTS (items 2, 3), applied. Falsification numerics: numerics/N2_*.json
(`blocks_where_excluded_below_kept` = number of mixed blocks in all three data sets; lowest 50 nulls excluded),
N1/N3 (`start` = K wherever the start is saturated), numerics/l12_check.py → L12_check.jsonl (direct check of (a)–(d));
reviewer scratch reviews/R03_scratch/ (closed forms vs direct scoring, all feasible sets at n = 14, p = 13).

Setting: STATEMENT §1–2: G, (CS) with Υ_n = I (FACB L1.0), (θ) with θ̄ > 0, blocks of size ≤ 16; parts (a), (b) use only
(PK′); parts (c), (d) use in addition (PK) and (PB) [R03-3]. L0 notation. Regular blocks:
𝔅 := blocks of size 16 containing no truth. Nulls outside regular blocks: at most 16(J₀ + s₀) (PB). For a truth-free
U ⊆ C_b, u := |U|.

## L1.1 The event E^S_n
L_n := log log n, H̄ := (2 log(2p) + 2L_n)^{1/2}.
* (S1) |η| ≤ L_n and max_{j∈[p]}|ξ_j| ≤ H̄;
* (S2) |‖e‖²/σ² − (n − 1)| ≤ n^{2/3} and |θ*ᵀg| ≤ L_n(θ*ᵀΣθ*)^{1/2}.
P(E^S_n) → 1: (S1) Gaussian tails and a union over p ≤ n terms (P(max|ξ_j| > H̄) ≤ 2p Φ̄(H̄) ≤ e^{−L_n}); (S2)
‖e‖²/σ² ~ χ²_{n−1} (L0.1; Laurent–Massart with t = log n) and θ*ᵀg ~ N(0, θ*ᵀΣθ*).
**Consequences** (n ≥ n₀(ρ, ϑ, σ)): s² = ‖Y‖²/(n − 1) ∈ [s²_∞ − n^{−1/4}, s²_∞ + n^{−1/4}], s²_∞ := ϑᵀΣ̄ϑ + σ²
(Σ̄ := (1 − ρ)I + ρ11ᵀ on S₀); κ_c = [(n − 1)ρθ̄ + σ√((n − 1)ρ)η]/s ∈ [c_κ n, C_κ n] with c_κ > 0 (θ̄ > 0);
κ₁ = σ√((n − 1)(1 − ρ))/s ≤ C√n.

## L1.2 Population part of a truth-free block table
For truth-free U, z_j = κ_c + κ₁ξ_j (j ∈ U), B_U = uκ_c + κ₁Σ_Uξ, and with 1 − uγ_u = κ/(u + κ):
  α·quad_U = A_U − γ_uB_U² = uκ_c²κ/(u + κ) + 2κ_cκ₁(κ/(u + κ))Σ_Uξ + κ₁²[Σ_Uξ² − γ_u(Σ_Uξ)²].
Put P_n(u) := nκ_c²uκ/(α(u + κ)) = (nκ_c²/β)·u/(u + κ) and N_U := n·quad_U − P_n(u). On E^S_n, |N_U| ≤ C√n H̄ for every
truth-free U with u ≤ 16 (nκ_cκ₁/α = O(√n), nκ₁²/α = O(1)). Write A_n := nκ_c²/(β(n − 1)); on E^S_n,
A_n → A := ρθ̄²/s²_∞ ∈ (0, 1) (A < 1 because s²_∞ ≥ ρθ̄² + (1 − ρ)‖ϑ‖² + σ² > ρθ̄²). With ψ(u) := 0.02 + (n − 1)(1 − A_n u/(u + κ))
(≥ (n − 1)(1 − A_n) ≥ c n), log r_b(U) = g_n(u) + ν log ψ_∅ − ν log(1 − N_U/ψ(u)), where g_n(u) := −½L_u − ν log ψ(u) is the
same function for every truth-free block, and |ν log(1 − N_U/ψ(u))| ≤ C√n H̄.
**Concavity.** h(u) := −log(1 − Au/(u + κ)) = log(u + κ) − log((1 − A)u + κ) has
h″(u) = −(u + κ)⁻² + (1 − A)²((1 − A)u + κ)⁻² < 0 on [0, 16] (because (1 − A)(u + κ) < (1 − A)u + κ), so
max_{u∈[0,16]} h″ ≤ −c_h(A, κ_∞) < 0, uniformly for A_n in a compact subset of (0, 1). The 0.02 term and the
second differences of L_u (O(1/n), L0.5(a)) are negligible: for 1 ≤ v ≤ 15,
  g_n(v + 1) − 2g_n(v) + g_n(v − 1) ≤ −(n/2)c_h/2 =: −c_g n   (n ≥ n₀).

## L1.3 Lemma START
**No-ties event** [R03-2]. 𝒟_n := {ξ_j ≠ ξ_l for all distinct j, l}; P(𝒟_n) = 1.

**Lemma L1.** For n ≥ n₀, on E^S_n ∩ 𝒟_n, every maximiser S of γ₀ on Ω satisfies:
(a) |S| = K;
(b) in every truth-free block C_b, every kept null has larger ξ than every excluded null;
(c) for regular blocks b, b′: |u_b − u_{b′}| ≤ 1 (u_b := |S ∩ C_b|);
(d) no regular block is entirely kept; hence every regular block's minimum-ξ null is excluded.
Hence (any emitted maximiser, e4′) S̃₀ has properties (a)–(d) w.p. → 1.

*Proof.* (a) Suppose |S| < K. If every truth-free block were entirely kept, |S| ≥ p − 16s₀ ≥ K + 1 (this needs only
p ≥ K + 16s₀ + 1, which is (PK′) [R09-E4]; (PB) is not used in (a), (b)); so some truth-free block has an excluded
null l. With U := S ∩ C_b, (U, l) is a positive pair in FACB's sense: c(U, l) =
(1 − ρ)ρθ̄/(1 + (u − 1)ρ) ≥ (1 − ρ)ρθ̄/(1 + 15ρ) > 0 (FACB L2.1; U is truth-free, so V = S₀). FACB L2.3(i) — whose proof
uses only S ∪ l ∈ Ω, ψ_U ≤ n, 1 − γ_{u+1} ≥ (1 − ρ)/2, w(k + 1)/w(k) ≥ 1/(2p) and max|g_j| ≤ √ρL_n + √(1 − ρ)H̄ = O(√log n)
(all valid here) — gives log γ₀(S ∪ l) − log γ₀(S) ≥ (n/2)c₂ − 3 log n > 0: S is not a maximiser.
(b) Let l ∈ S ∩ C_b and l′ ∈ C_b ∖ S be nulls of a truth-free block with ξ_{l′} > ξ_l. S′ := S ∖ {l} ∪ {l′} ∈ Ω has
the same size and the same intersections with the other blocks. With U := S ∩ C_b, U′ := U ∖ {l} ∪ {l′} (both of size u):
  α(quad_{U′} − quad_U) = (z_{l′} − z_l)[z_{l′} + z_l − γ_u(2B_U + z_{l′} − z_l)]
                        = κ₁(ξ_{l′} − ξ_l)[2κ_c κ/(u + κ) + κ₁E],
E := ξ_{l′} + ξ_l − 2γ_uΣ_Uξ − γ_u(ξ_{l′} − ξ_l), |E| ≤ 6H̄ (γ_uu ≤ 1) [R09-E2]. Since κ/(u + κ) ≥ κ/(16 + κ) ≥ (1 − ρ)/(1 + 15ρ)
and κ_c ≥ c_κn ≫ κ₁H̄ = O(√(n log n)), the bracket is positive; so quad_{U′} > quad_U, hence ψ_{U′} < ψ_U and
log r_b(U′) > log r_b(U) (log r_b(U) = −½L_u − ν log(ψ_U/ψ_∅) for fixed u), and γ₀(S′) > γ₀(S).
(c) Suppose u_b ≥ u_{b′} + 2 for regular b, b′. Then u_b ≥ 2 and u_{b′} ≤ 14. Let l be the kept null of C_b with the
smallest ξ and l′ an excluded null of C_{b′}; S′ := S ∖ {l} ∪ {l′} has the same size. By L1.2,
  log γ₀(S′) − log γ₀(S) = [g_n(u_{b′} + 1) − g_n(u_{b′})] − [g_n(u_b) − g_n(u_b − 1)] + O(√n H̄)
                          = −Σ_{v=u_{b′}+1}^{u_b−1}[g_n(v + 1) − 2g_n(v) + g_n(v − 1)] + O(√n H̄) ≥ c_g n − C√n H̄ > 0.
(d) If a regular block is entirely kept (u_b = 16), (c) gives u_{b′} ≥ 15 for every regular b′, so
K = |S| ≥ 15·|𝔅| ≥ 15(p − 16(J₀ + s₀))/16, contradicting liminf p/K > 16/15 for n ≥ n₀. So u_b ≤ 15 for every regular
block, and by (b) its minimum-ξ null (unique on 𝒟_n) is excluded. ∎

## L1.4 Remarks
1. **Uniqueness** is not used: (P2) holds for every maximiser, hence for any e4′-emitted centre.
2. **Why (b) is exact although the objective has a ξ² term.** The exchange changes quad by a product
   (ξ_{l′} − ξ_l) × (order-n positive factor + O(√(n log n))); the ξ² terms only enter the second factor.
3. **Partition — sketch suggesting (PB) for the coded partition; not used as a proved implementation property (the
   theorems assume (PB))** [R07-10]. Under EX-A, for an exactly equicorrelated Gram: all off-diagonal
   distances 1 − |r̂| equal 1 − ρ, so every candidate merge is tied; the union-lexicographic rule merges {0, …, m} with
   {m + 1} at each stage (its sorted list is the smallest), giving a chain dendrogram; the top-down cut at B retains
   {0, …, B − 1} and singletons, and next-fit packing yields consecutive blocks of size B (last p mod B). Checked against
   the C-GROW reimplementation of the coded rules (numerics/pk_selftest_out.txt, 5/5). Not needed for the claims, which
   hold for every (PB) partition.
4. Truth keeping is not claimed or used (v1's (TK) was dropped; a start missing truths is handled in L3.4, phase A).
