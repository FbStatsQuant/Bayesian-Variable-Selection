# L4 — Theorem LOC-d (d-dimensional local designs) and Theorem LOC-BF (one-factor / bounded groups)

Status: **PROVED (by this seat, unchecked)** (given L1–L3 of this folder and the cited inputs). Delta proof to APP
`lemmas/L3_LOC.md` (Theorem LOC §L3.2–L3.5, LOC-B §L3.8B; itself a delta to GROW `lemmas/L6_random_AR1.md`). Every
step of the source is listed with the fact it used and its replacement. Check record: R04 (Codex gpt-6.1-sol high, `reviews/R04_L4L5L7_check_sol.md`): see `reviews/R04_disposition.md` (L4, L5 VERIFIED-WITH-AMENDMENTS, applied; L7 VERIFIED).
Falsification numerics: `numerics/d1_diag.py` (sandwich: S₀ ⊆ start mode in all 74 runs; extras' distances are ℓ∞ grid
distances, not the theorem's Euclidean ones [R07-16]; numerics/D1_SUMMARY.md), `numerics/n4_nar_check.py` (frames/atoms decomposition, (R3) ratio ≤ 1.0009).

## Part A — Theorem LOC-d

**Hypotheses.** Setting of STATEMENT §1; Σ_n ∈ LOC_d(c, C, K, a) (L3_CTd §L3.2; K = K_dec, the decay constant) with fixed constants and fixed d ≥ 1;
PTV(a₀): |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀ for every j ∈ S₀, U ⊆ [p] ∖ {j}, |U| ≤ 15. (K₂, t₂) of Lemma CD_d;
distances d(j, k) := ‖x(j) − x(k)‖.
**Relevance set.** d_n := ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉, Q⁰ := S₀ ∪ {l ∉ S₀ : min_{k∈S₀}d(l, k) ≤ d_n};
Q := Q⁰ if p ≥ 2|Q⁰| + 32s₀ + 1, else Q := [p]. By packing (L3.0), |Q⁰| ≤ s₀(2d_n + 3)^d, so
|Q| ≤ 2s₀(2d_n + 3)^d + 32s₀ ≤ (log n)^{d+1} for n ≥ n₀. 𝓛 := {T : S₀ ⊆ T ⊆ Q}.

**Theorem LOC-d.** P(Sand_n) → 1, P(NA(𝓛)) → 1, P(TL(𝓛)) → 1; hence (L5_assembly) D_n → 0,
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1), with the shipped LS0 cap ℓ_n + |S̃₀|.

### A.1 Regularity (APP L3.2) — L1_toolkit §L1.2 with κ = d + 1, (P1) → spectrum in [c, C], (P3) → CD_d(b), (P4) → CD_d(a).
TV from PTV verbatim. Lattice family A_score by L0′.

### A.2 Selection removal (APP L3.3)
R_n := ⌈(2 log n + log K₂ + log(1 + s₀θ_hi))/t₂⌉, H_l := {j : min_{k∈{l}∪S₀}d(j, k) ≤ R_n}. By packing,
|H_l| ≤ (s₀ + 1)(2R_n + 3)^d = O((log n)^d) (was O(log n)), so |I_l| ≤ (|H_l| + 1)^{15} = O((log n)^{15d}) =: N^ref_n [C1-Opus-7] — still
exp(O(log log n)), which is all APP L3.3/L3.4 and GROW L6.4 use. Population inputs (i)–(iii) of APP L3.3 by CD_d(a)
(e^{−t₂d} ≤ n^{−2}/(K₂(1 + s₀θ_hi)) for d > R_n; ≤ n^{−1/2}/(1 + s₀θ_hiK₂) for d > d_n) and CD_d(b) (residual variances
≥ min(c, σ²)). The recursive partial-correlation algebra uses only bounded dimensions (|U| ≤ 15) and the entrywise
event. Conclusion (6.4) unchanged: |h_{U,l} − h_{U∩H_l,l}| ≤ ϖ_n = C(log n)^{3/2}/√n, h_{U,l} ≤ C log n, uniformly over
l ∉ Q, |U| ≤ 15.

### A.3 Spherical tail (APP L3.4)
Unchanged with CD_d: ‖α‖ ≤ C K₂ s₀^{1/2}e^{−t₂d_n}/c (each truth residual covariance with W_l given U₀ is ≤ K₂e^{−t₂d_n},
the conditional truth covariance has eigenvalues ≥ c), ‖b_j‖ ≤ √15/c, τ² ∈ [c, 1]; ‖m‖ ≤ C√n e^{−t₂d_n} ≤ C.
(6.5)–(6.7) and the counting p·N^ref_n·exp(−t_n(k)/2) ≤ Ck n^{−1/2+o(1)} hold since N^ref_n = n^{o(1)}.

### A.4 Sandwich incl. the global size ladder (APP L3.5 = GROW L6.5)
Unchanged; the only size facts it uses are: k₀ := |Q| + 16s₀ (now O((log n)^{d+1})); the ladder m_i = 2^{i+1}k₀ with at most
O(log n) indices below K_n ≤ n/2, giving P(some maximiser has k > 2k₀) ≤ O(log n)·n^{−1/2+o(1)} → 0; feasibility of a
truth addition when k ≤ 2k₀ < K_n (Q ≠ [p], K_n ≥ 2|Q| + 32s₀ + 1 by L1.2) or Q = [p]; and junk exclusion, where
deleting l ∈ S̃ ∖ Q gains ≥ ¼ log n − log k − 2κ_E − o(1) with log k ≤ log(2k₀) = O(log log n). All hold.
So P(Sand_n) → 1.

### A.5 NA via Lemma NA-R
(N0): |Q| ≤ (log n)^{d+1}, |Q| ≤ K_n (L1.2), p ≤ n^A. (N1): λ_min(Σ_n) ≥ c. Put r_n := log log n and
B_l := {v ≠ l : d(v, l) ≤ r_n}; |B_l| ≤ (2r_n + 3)^d.
* (R1) For (T, l) ∈ 𝔓 let T′ := T ∩ B_l; frame ι(T, l) := the single functional ψ_{T,l} := e_l − Σ_{v∈T′}β_{T′}(l)_v e_v
  (e_v coordinate functionals; r_{T,l} = W_l − W_{T′}β_{T′}(l) = e_{T′,l}). Frames are indexed by (l, T′ ⊆ B_l):
  N_n ≤ p·2^{(2r_n+3)^d}, log N_n ≤ log p + (2 log log n + 3)^d log 2 = log p + o(log n). m₀ = 1.
* (R2) Atoms 𝒜_n := {e_v : v ∈ Q} (Var = 1, |𝒜_n| ≤ |Q|). Since W_Tβ_T(l) − W_{T′}β_{T′}(l) = Σ_{v∈T}λ_{T,l,v}W_v with
  λ_{T,l} := β_T(l) − β̄_{T′}(l) (zero-padded), e_{T,l} = r_{T,l} − Σ_v λ_{T,l,v}W_v, and by Lemma RB
  ‖λ_{T,l}‖₁ ≤ 2L₀ =: L. Then L²(log(|𝒜_n| + 1) + log log n) = O(log log n) = o(log n).
* (R3) By Lemma TAIL (b), (a) with r = r_n: ϱ²_{T,l} = Var(W_l | W_{T′}) ≤ τ²_{T,l} + κ(r_n) ≤ (1 + κ(r_n)/c)τ²_{T,l};
  η_n := κ(r_n)/c → 0.
Lemma NA-R gives P(max_𝔓 Z²_{T,l} ≤ c_n) → 1, and with GROW L2.2 on 𝓔_n (L1_toolkit L1.1), P(NA(𝓛)) → 1.

### A.6 TL — GROW L2.1 on 𝓔_n (L1_toolkit L1.1), conditional on X ∈ A_X, integrated (as APP L3.7). ∎ (Part A, with L5.)

**Remarks.** (1) d = 1 with integer sites π_n(j) is APP Theorem LOC (whose NA lemma L3.6 is also replaced by NA-R
here). (2) Covered examples: Gaussian fields on ℤ^d ∩ box_n or on separated irregular sites with exponentially
decaying covariance and bounded spectrum (e.g. exponential/Matérn-type covariances with a fixed range in site units,
separable AR(1) products, GMRFs with fixed-range precision and bounded spectrum — (LOC_d-Θ) with K := e^{a b}/c for range
b); increasing-domain asymptotics only. (3) The proof gives |S̃₀ ∖ S₀| ≤ |Q| = O((log n)^d) (an upper bound; no matching
lower-bound construction for LOC-d is claimed — component-port runs in d = 2 suggest superlogarithmic growth, observations
only) [R07-3]; the former/smaller cap ℓ_n alone is not claimed to suffice; the shipped cap ℓ_n + |S̃₀| is used.

## Part B — Theorem LOC-BF (growing one-factor groups; middle regime)

**Hypotheses.** Setting of STATEMENT §1. Σ_n is block-diagonal w.r.t. a deterministic partition 𝒢_n of [p]; each
G ∈ 𝒢_n is (i) *bounded*: |G| ≤ g₀ and λ_min(Σ_GG) ≥ c, or (ii) *one-factor*: Σ_GG = b_Gb_Gᵀ + diag(1 − b_v²)_{v∈G},
b_v ∈ {0} ∪ [b_lo, b̄], 0 < b_lo ≤ b̄ < 1, |G| ≤ g_n ≤ (log n)^κ (κ ≥ 1 fixed). |G ∩ S₀| ≤ 1 for all G.
Q⁰ := ⋃_{j∈S₀}G(j); Q by the enlargement rule; |Q| ≤ 2s₀ max(g₀, g_n) + 32s₀ ≤ (log n)^{κ+1}.
(Compound symmetry with ρ ∈ [b_lo², b̄²] is type (ii) with b_v ≡ √ρ.)

**Theorem LOC-BF.** P(Sand_n) → 1, P(NA(𝓛)) → 1, P(TL(𝓛)) → 1, and the conclusions of L5.

### B.0 Population facts
(F1) For U ⊆ [p] and v, w in different groups: Cov(W_v, W_w | W_U) = 0 (independent groups stay conditionally
independent); E[W_l | W_T] = E[W_l | W_{T∩G(l)}]. (F2) λ_min(Σ_n) ≥ c_B := min(c, 1 − b̄²) (type (ii):
Σ_GG ≽ diag(1 − b_v²)). (F3) PTV(c_Bθ_lo) holds automatically: for j ∈ S₀, U ∌ j, the other truths lie in other groups,
so |Cov(W_j, Σθ*_kW_k | W_U)| = |θ*_j|Var(W_j | W_U) ≥ c_Bθ_lo [R04-1].

### B.1 Sandwich — APP L3.8B delta with polylog sizes
APP L3.8B replaces CD(a) by the exact zeros (F1) and CD(b) by Var(W_j | W_U) ≥ c_B (Schur complement ≥ λ_min(Σ_n)); the
upper spectral bound is used nowhere else (λ_max ≍ g_n is allowed). Steps: (L3.2) L1_toolkit §L1.2 with c_B;
(L3.3) H_l := G(l) ∪ Q⁰, |H_l| ≤ (s₀ + 1)max(g₀, g_n) = O((log n)^κ), |I_l| = O((log n)^{15κ}) = n^{o(1)}; for l ∉ Q
(truth-free group) and v ∉ H_l the population covariances of W_v with W_l and with V given W_{U₀} are 0, and the
population residual correlation of W_l and V given U₀ is 0; (L3.4) α = 0, ‖b_j‖ ≤ √15/c_B, τ² ∈ [c_B, 1], m = 0;
(L3.5) unchanged with k₀ = O((log n)^{κ+1}) as in A.4. So P(Sand_n) → 1.

### B.2 NA via Lemma NA-R
*Latent extension.* For each type-(ii) group G let (F_G, (ξ_v)_{v∈G}) be iid N(0, 1), independent across groups, with
W_v = b_vF_G + √(1 − b_v²)ξ_v (v ∈ G), rowwise iid. This has the law of the rows of W restricted to G; realise it on an
enlarged probability space by drawing, row by row, (F_G, ξ_G) from its Gaussian conditional law given W_G using
auxiliary randomness independent of (W, ε). Then (W, Ξ) is jointly Gaussian with iid rows and independent of ε, and
the law of (X, ε) is unchanged. (For b_v = 0, ξ_v = W_v.)
(N0), (N1): q := |Q| ≤ p and q ≤ (log n)^{κ+1} = o(n), hence q ≤ ⌊n/2⌋ eventually and q ≤ min(p, ⌊n/2⌋) = K_n [R04-2]; λ_min ≥ c_B.
For (T, l) ∈ 𝔓 let G := G(l), A := T ∩ G (l ∉ A). By (F1), β_T(l) is supported on A and equals β_A(l).
* Type (i) G: frame := the single functional ψ_{T,l} := e_l − Σ_{v∈A}β_A(l)_v e_v, i.e. r_{T,l} = e_{T,l}; λ := 0.
  Frames indexed by (l, A ⊆ G): ≤ p·2^{g₀}.
* Type (ii) G: D_A := diag(1 − b_v²)_{v∈A}, s₂ := b_AᵀD_A⁻¹b_A. Σ_AA = D_A + b_Ab_Aᵀ, Σ_{Al} = b_lb_A, so by
  Sherman–Morrison β_A(l) = b_lD_A⁻¹b_A/(1 + s₂). Hence
    e_{T,l} = (b_l − β_A(l)ᵀb_A)F_G + √(1 − b_l²)ξ_l − Σ_{v∈A}β_A(l)_v√(1 − b_v²)ξ_v.
  Frame := (F_G, ξ_l) (m₀ = 2; one frame per l); r_{T,l} := the first two terms; atoms ξ_v (v ∈ Q in type-(ii)
  groups, Var 1), λ_{T,l,v} := β_A(l)_v√(1 − b_v²).
  ℓ¹ bound: for b_v ∈ [b_lo, b̄], b_v/(1 − b_v²) ≤ b_v²/(b_lo(1 − b_v²)); terms with b_v = 0 vanish; hence
  ‖λ_{T,l}‖₁ ≤ ‖β_A(l)‖₁ = b_l Σ_{v∈A}(b_v/(1 − b_v²))/(1 + s₂) ≤ b_l s₂/(b_lo(1 + s₂)) ≤ 1/b_lo.
  (R3): r_{T,l} is a function of (F_G, ξ_l), independent of (ξ_v)_{v∈A}; so τ²_{T,l} = ϱ²_{T,l} + Σ_vλ²_{T,l,v} ≥ ϱ²_{T,l}:
  η_n := 0.
(R1): N_n ≤ p·2^{g₀} + p, log N_n ≤ log p + O(1). (R2): |𝒜_n| ≤ |Q|, L := 1/b_lo; L²(log(|Q| + 1) + log log n) =
O(log log n) = o(log n). Lemma NA-R and GROW L2.2 on 𝓔_n give P(NA(𝓛)) → 1.

### B.3 TL — as A.6. ∎ (Part B, with L5.)

**Remarks.** (1) Content beyond APP LOC-B: no bound s₀(g_n − 1) ≤ (1 − δ₀) log n (B-χ) is needed, and no extra
condition in the enlarged case; groups may grow polylogarithmically. The class INCLUDES sequences where APP L5_VN (V2)
shows the start mode contains ≍ g_n visible nulls (compound-symmetric truth groups, fixed ρ ∈ [b_lo², b̄²], actual size
g_n with g_n/log n → ∞), so the GROW/LOC sandwich with |Q| = O(log n) fails there; the sandwich here has |Q| ≍ g_n,
consistent with VN. It also includes sequences without visible nulls (e.g. all b_v = 0), where no obstruction is
asserted [R01-4]. (2) Not covered: polynomially growing groups g_n = n^{b} — outside the theorem; they would need a polynomial-size NA and
assembly analysis (as L6 does for polynomial decay); the sandwich counting alone leaves slack when the reference count
O(n^{15b}) and the start-mode size O(n^b) satisfy 16b < 1/2 (cf. L6 (P6)/(P13)) [R07-9]; also not covered: groups with ≥ 2
truths, general (non-one-factor) growing groups, multi-factor groups.
