# L2 — The start mode is S* = [p] ∖ N₀ (claim (C1))

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high): VERIFIED-WITH-AMENDMENTS (item 3,
the case U = ∅), applied. Falsification numerics: numerics/n4_start.py → N4_out.txt (exact-Gram
compound symmetry, coded partition, ρ ∈ {0.3, 0.7}, p ∈ {100, 200, 400}, layouts "spread", "oneblock" (all truths
in one block, N₀ ≠ ∅) and s₀ = 1: start mode = S* and unique (n_optimal = 1) in 66/72 data sets; the 6 misses are all
at n = 10⁵, p = 100 (one null still out — finite n); every data set with n ≥ 10⁷ matches). Also N1 (S̃₀ = [p] for S5/F1/F2 in most sampled
cases at n = 10⁶, with exceptions — F2 p = 200 c = 0.5 (size 193), S5 p = 400 c = 0.5 (396–397) — and in all sampled cases
at n = 10⁸; R07 item 8).

Setting: STATEMENT §1–2 including (FS); L1 (Υ_n = I). Blocks C_b with |C_b| ≤ 16 (any partition). N₀ :=
⋃{C_b ∖ S₀ : S₀ ⊆ C_b} (at most one block can contain S₀). K = p by (P).

## L2.1 Increments of the block tables

For U ⊆ C_b, |U| = u ≤ 15, and l ∈ C_b ∖ U, by L1.2–L1.3 (the algebra of L1.3 holds for every U, not only U ⊇ S₀):

  log r_b(U ∪ l) − log r_b(U) = −½(L_{u+1} − L_u) − ν log(1 − n(1 − γ_{u+1}) t_{U,l}²/(α ψ_U)),
  t_{U,l} := z_l − γ_u B_U,  ψ_U := 0.02 + Q_U.

With z = [(n − 1)Σθ* + σ√(n − 1)g]/s (L1.1):

  t_{U,l} = ((n − 1)/s)·[(Σθ*)_l − γ_u Σ_{j∈U}(Σθ*)_j] + (σ√(n − 1)/s)·[g_l − γ_u Σ_{j∈U} g_j].

**Population part.** For l ∉ U, Σ_{lU}Σ_UU⁻¹ = (ρ/(1 + (u − 1)ρ))1ᵀ, and γ_u = ρ/(1 − ρ + uρ + 1/a); hence
(Σθ*)_l − γ_uΣ_U(Σθ*)_j = c(U, l) + O(1/n²), where

  c(U, l) := Cov(x_l, μ | x_U) = (1 − ρ)[θ*_l + ρ ϑ(S₀ ∖ U)/(1 + (u − 1)ρ)]

(computation: (Σθ*)_j = (1 − ρ)θ*_j + ρθ̄; ρ1ᵀΣ_UU⁻¹Σ_{U·}θ* = ρ[ρθ̄u + (1 − ρ)ϑ(U ∩ S₀)]/(1 + (u − 1)ρ); subtract from
(1 − ρ)θ*_l + ρθ̄). c(U, l) depends only on (S₀ ∖ U, u, and the identity of l if l ∈ S₀): finitely many values.
* If U ⊇ S₀ and l is null, c(U, l) = 0 ("zero pair").
* Otherwise c(U, l) ≠ 0 by (FS): for l null, c = (1 − ρ)ρϑ(V)/(1 + (u − 1)ρ) with V = S₀ ∖ U ≠ ∅ (FS-a); for l ∈ S₀,
  c = (1 − ρ)[ϑ_l + ρϑ(V)/(1 + (u − 1)ρ)] with l ∈ V (FS-b). Let c_FS := min |c| over the finitely many nonzero values;
  c_FS > 0 is a constant.

**Noise part.** For u ≥ 1, γ_uu ≤ 1 gives |g_l − γ_uΣ_Ug_j| ≤ 2 max_{j∈[p]}|g_j|. **U = ∅** (R03 item 3):
B_∅ := 0 and t_{∅,l} = z_l; the noise part is g_l and the population part is (Σθ*)_l = c(∅, l) (the displayed formula
with u = 0, V = S₀; empty-vector conventions).

## L2.2 The event

E_n^S: max_{j∈[p]}|g_j| ≤ G_n := √(2 log(2p) + 2L_n); |θ*ᵀg| ≤ L_n(θ*ᵀΣθ*)^{1/2}; ‖e‖²/σ² ∈ [n − 1 − n^{2/3},
n − 1 + n^{2/3}] (so s² = θ*ᵀΣθ* + σ² + O(n^{−1/3}) ∈ [s_min², s_max²] with s_min² := σ²/2, s_max² := 2(θ*ᵀΣθ* + σ²));
and, for every zero pair (U, l) of the block containing S₀ (if any; at most 2¹⁵·16 pairs),
|g_l − γ_uΣ_{j∈U}g_j| ≤ 2√(2(20 + L_n)).
P(E_n^S) → 1: g_j ~ N(0, 1) (union over p); the χ² bounds as in L3 E2; each g_l − γ_uΣ_Ug_j is centred Gaussian with
variance Σ_ll − 2γ_uΣ_{lU}1 + γ_u²1ᵀΣ_UU1 ≤ 1 + 2γ_uuρ + γ_u²u(1 + (u − 1)ρ) ≤ 4 (γ_uu ≤ 1), and the union over
≤ 2²⁰ pairs costs ≤ 2²⁰·2e^{−(20 + L_n)} → 0.

## L2.3 Single-flip improvements

On E_n^S and for n ≥ n₀, let S ∈ Ω, k := |S| ≤ p, b a block, U := S ∩ C_b.
(i) **Positive pair** (l ∈ C_b ∖ U, c(U, l) ≠ 0, k < p). |t_{U,l}| ≥ (n − 1)(c_FS − O(1/n²))/s − 2σ√(n − 1)G_n/s ≥ c₁n with
c₁ := c_FS/(2s_max) (G_n = O(√log n)). With α ≤ (n² − 1)(1 − ρ) + 1, ψ_U ≤ n (Q_U ≤ yᵀy = n − 1) and
1 − γ_{u+1} ≥ 1 − γ₁ ≥ (1 − ρ)/2: n(1 − γ_{u+1})t²/(αψ_U) ≥ c₂ := c₁²/4 > 0, hence
  log γ₀(S ∪ l) − log γ₀(S) = log[w(k + 1)/w(k)] + log r_b(U ∪ l) − log r_b(U)
   ≥ −log(2p) − ½log(n + 2) − 1 + ν log(1/(1 − c₂)) ≥ (n/2)c₂ − 3 log n > 0
(w(k + 1)/w(k) = (k + 1)/(2p − 1 − k) ≥ 1/(2p); L_{u+1} − L_u ≤ log(n + 1) + o(1), L1.5(a)).
(ii) **Zero pair** (U ⊇ S₀, l ∈ C_b ∖ U null; then b is the block containing S₀ and l ∈ N₀). The population part of
t_{U,l} is O(1/n), so |t_{U,l}| ≤ 2σ√(n − 1)·2√(2(20 + L_n))/s + O(1). Since U ⊇ S₀, Q_U ≥ RSS_U/s² (L1.5(b)) with
RSS_U = ‖e‖² − σ²Φ(U), Φ(U) = g_UᵀΣ_UU⁻¹g_U ≤ 16G_n²/(1 − ρ) = O(log n); so ψ_U ≥ σ²n/(2s_max²) and
n(1 − γ)t²/(αψ_U) ≤ C(L_n + 20)/n. The increment of adding l is therefore ≤ −½(L_{u+1} − L_u) + C(L_n + 20)
≤ −½log(n + 1) + C(L_n + 21) < −¼log n. Equivalently, for l ∈ S ∩ N₀ with (S ∩ C_b) ∖ {l} ⊇ S₀, removing l changes
log γ₀ by ≥ log[w(k − 1)/w(k)] + ¼log n ≥ ¼log n > 0 (w(k − 1)/w(k) = (2p − k)/k ≥ 1 for k ≤ p).

## L2.4 Lemma (C1)

**Lemma L2.** On E_n^S, n ≥ n₀: S* is the unique maximiser of γ₀ on Ω. Hence P(S̃₀ = S*, unique) → 1, and the start
mode contains S₀ and every null outside N₀.

*Proof.* Let S ∈ Ω, S ≠ S*. (a) If some l ∈ S* ∖ S exists, let b ∋ l and U := S ∩ C_b. (U, l) is not a zero
pair: a zero pair needs S₀ ⊆ U ⊆ C_b and l null, i.e. l ∈ C_b ∖ S₀ with S₀ ⊆ C_b, i.e. l ∈ N₀, but l ∈ S* = [p] ∖ N₀.
So (U, l) is a positive pair, |S| < p (l ∉ S), and γ₀(S ∪ l) > γ₀(S) by L2.3(i). (b) Otherwise no element of S*
is missing, i.e. S* ⊆ S, and S ≠ S* gives some l ∈ S ∩ N₀. Let b be the block containing S₀ (it contains l) and
U := (S ∩ C_b) ∖ {l}. If U ⊇ S₀, removing l increases γ₀ (L2.3(ii)). If U ⊉ S₀, some truth j ∈ S₀ ∖ S exists — impossible,
since S₀ ⊆ S* ⊆ S. So in every case S is not a maximiser; Ω is finite, hence S* is the unique maximiser. ∎

**Remarks.** (1) Uniqueness makes the e4/e4′ tie rules irrelevant (FINAL s5, Lemma UM): the coded routine and TDP
both return S*. (2) N₀ is deterministic (partition and S₀ are), so 𝒩* = S* ∖ S₀ is deterministic — used in L3/L4.
(3) The population increments are of order n while the size penalty is O(log n); this is the mechanism behind
"every null block absorbs the factor signal" — under compound symmetry the start mode is the whole model (minus N₀).

## L2.5 Corollary M (masked truths) — added after lock, flagged (STATEMENT §4 (C1-M))

Status: **PROVED (by this seat, unchecked)**; falsification numerics/n7_masked.py → N7_out.txt (masked truth, ρ ∈ {0.3, 0.5}, p ≤ 400, n ≥ 10⁷: start = S* and pure-deletion path to S₀ in 18/18); added 2026-11-09 after HQ's note on FAC-A's open item 4; checked only
through the council (not part of the R03-checked text).

**(FS′)** := (FS-a), and (FS-b) required only for u ∈ {1, …, 15}; in addition every block that contains a truth j
with c(∅, j) = 0 ("masked" truth: (1 − ρ)ϑ_j + ρϑ(S₀) = 0) also contains a null.

**Corollary M.** Lemma L2 holds with (FS) replaced by (FS′). In particular a masked truth (FAC-A's a = 1/2 instance
(1 − a)θ_j + aΘ = 0, in our notation u = 0, V = S₀) is in the start mode, and (C2)–(C4) are unchanged (L3–L5 do not use
(FS)).

*Proof.* Only L2.4(a) used (FS-b) at u = 0, for a pair (∅, l) with l a truth. Let S ∈ Ω, l ∈ S* ∖ S, b ∋ l,
U := S ∩ C_b. If U ≠ ∅, or c(∅, l) ≠ 0, (U, l) is a positive pair as before (FS-b with u ≥ 1, or the nonzero value).
If U = ∅ and c(∅, l) = 0, take a null l′ ∈ C_b (it exists by (FS′)). Since U = ∅, l′ ∉ S and (∅, l′) is not a zero
pair (a zero pair needs U ⊇ S₀ ≠ ∅); its value is c(∅, l′) = (1 − ρ)ρϑ(S₀)/(1 − ρ) = ρϑ(S₀) ≠ 0 by (FS-a). As |S| < p
(l ∉ S), adding l′ strictly increases γ₀ (L2.3(i)), so S is not a maximiser (whether or not l′ ∈ N₀ is irrelevant). The
rest of the proof of L2 is unchanged. ∎
