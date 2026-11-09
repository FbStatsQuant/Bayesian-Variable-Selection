# L3 — The probability event E_n

Status: **PROVED-CHECKED** (Tier 1: lemma checks, mid-point CONTINUE, sweep fixed, council round 2 passed — R09 Sol 8.8, R10 Opus 8.8, all gates PASS). Lemma check R02 (Codex Sol high): VERIFIED-WITH-AMENDMENTS, applied; R06 item 1 (E_S block-local) fixed.
Falsification: the components are standard Gaussian/χ² bounds; the
quantities they control are monitored in numerics/S3_summary.txt and s1_out/.

Setting: STATEMENT §1–2, L1 (Υ_n = I). L_n := log log n, G_n := (2 log(2p) + 2L_n)^{1/2} (a deterministic envelope; the random maximum max_i|g_i| is written
G_n^obs, and E1 says G_n^obs ≤ G_n — R06 item 14),
H_q := (2 log(2^{q̄}p) + 2L_n)^{1/2}. Random inputs (L1.1): η, (ζ_g), (ξ_j), r independent.

**E_n := E1 ∩ E2 ∩ E3 ∩ E_A ∩ E_S**, where
* **E1** |η| ≤ L_n and max_{j∈[p]}|g_j| ≤ G_n; hence max_j|y_j| ≤ G_n + L_n.
* **E2** ‖e‖²/σ² ∈ [n − 1 − n^{2/3}, n − 1 + n^{2/3}]; gᵀΣ⁻¹g ≤ p + n^{2/3}; |θ*ᵀg| ≤ L_n(θ*ᵀΣθ*)^{1/2}.
* **E3** (bounded statistics of the truths) for every j ∈ S₀ and U ⊆ G_{g(j)} ∖ {j}: |A_j(U)| ≤ L_n.
* **E_A** for every j ∈ [p] ∖ S₀ and every U ⊆ G_{g(j)} ∖ {j}: |A_j(U)| ≤ H_q.
* **E_S** (zero pairs of the block containing S₀, as FACB L2.2): in the (unique, if any) method block C_b ⊇ S₀, for every
  U with S₀ ⊆ U ⊆ C_b ∖ {l} and every l ∈ C_b ∖ S₀ (block-local: |U| ≤ 15; R06 item 1), |g_l − β̃_{lU}ᵀg_U|/ṽ_{l|U}^{1/2} ≤ 2(20 + L_n)^{1/2} (β̃, ṽ as in L1.4 with R = U).

**Lemma L3.1.** P(E_n) → 1.
*Proof.* E1: g_j ~ N(0, 1), union over p: P(max|g_j| > G_n) ≤ 2pΦ̄(G_n) ≤ p e^{−G_n²/2} = 1/(2 log n). E2: as FACB L3
(Laurent–Massart with t = log n; gᵀΣ⁻¹g ~ χ²_p, gᵀΣ⁻¹g + r ~ χ²_{n−1}; θ*ᵀg ~ N(0, θ*ᵀΣθ*)). E3: s₀·2^{q̄−1} standard
normals (A_j(U) ~ N(0, 1), L1.3(iii)). E_A: at most p·2^{q̄−1} standard normals; P ≤ p2^{q̄−1}·2Φ̄(H_q) ≤
p2^{q̄}e^{−H_q²/2}/2 ≤ 1/(2 log n). E_S: each quantity is a centred Gaussian; with β̃ the Σ̃-predictor, Var(g_l − β̃ᵀg_U) = Σ_ll − 2β̃ᵀΣ_Ul + β̃ᵀΣ_UUβ̃ =
ṽ_{l|U} − (1 + ‖β̃‖²)/a ≤ ṽ_{l|U}, so the standardised quantity has variance ≤ 1; at most 2¹⁵·16 pairs; union
≤ 2²⁰·2e^{−2(20 + L_n)} → 0. ∎

**Consequences on E_n** (n ≥ n₀):
(c1) For every p ≤ ⌊n/2⌋: s² ∈ [σ²/2, 2(θ*ᵀΣθ* + σ²)] (θ*ᵀΣθ* = ϑᵀΣ_{S₀S₀}ϑ ≤ ‖ϑ‖²·(1 + s₀) is bounded).
(c1′) **Only when p ≤ n^α for a fixed α < 1** (in particular under (P_α), the path regime): M_T = ½(1 + η_T) for every
T ⊇ S₀, |η_T| ≤ η_n (L1.4.2). (For p/n → c ∈ (0, 1/2] this fails: M_{[p]} → 1/(2(1 − c)) in probability, = 1 at c = 1/2; R02 item 2, R06 item 4. L2 does
not use (c1′).)
(c2) For every R ⊆ [p]: |e_R| ≤ |h| + max_j|y_j| ≤ G_n + 2L_n (L1.3(i)) — the crude "lattice" bound, O(√log n).
(c3) For every null j and every T ⊇ S₀ (j ∈ T or not): |τ_j(T)| ≤ H_q + κ₀|e_R| (L1.3.1, E_A), R = T ∖ {j}.
(c4) For j null, T ⊇ S₀, and p ≤ n^α with α < 1: the error ε_j of L1.4 satisfies
|ε_j| ≤ C_d[(1 + H_q + κ₀(G_n + 2L_n) + G_n)p/n² + √p/n^{3/2}] ≤ n^{−1/2} for n ≥ n₀, uniformly (R02 item 1).
