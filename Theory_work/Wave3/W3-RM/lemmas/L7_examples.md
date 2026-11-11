# L7 — Examples (bridge (B10) and the examples table, claim (C4))

Status: **PROVED (by this seat, unchecked)** for the verifications written out below; check R06 (Codex gpt-6.1-sol
high, `../reviews/R06_batch2_check_sol.md`): WRONG as first written (4 MAJOR — one missing hypothesis in (E-F2) and three
overstated rows of table 7.3 — and 2 MINOR), all corrected here [R06-#]; everything else is a citation
with the source's status copied verbatim. Families appear here only (PROTOCOL item 4). Notation `../STATEMENT.md`.

## 7.1 Form R instances

### (E-R1) Metric-local designs = the class of Theorem UNI-0 (main example)
Class (UNI `STATEMENT.md:103-110`): Gaussian rows, Σ_n unit-diagonal in 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) — spectrum in [c, C]
and exponential decay of Σ_n or Σ_n⁻¹ along a pseudometric of polynomial growth (banded/AR, separated sites in ℝ^d,
graphs of polynomial growth, bounded blocks); fixed s₀, |θ*_j| ∈ [θ_lo, θ_hi]; **signal condition: PTV(a₀)**.
Verification of the hypotheses of Theorem RM-R, with Q, d_n as in UNI `lemmas/L2_k0.md:66-77`, R_n and
H_l := ⋃_{k∈{l}∪S₀}B(k, R_n) as in `L2_k0.md:95-99`, and the exponent κ enlarged to max(1, d₀ + 1):
* (T1-R): λ_min(Σ_n) ≥ c (sufficient form). (FL-R): the same floor. (V-R): PTV(a₀) is assumed.
* (L-size): |Q| = O((log n)^{d₀}) (`L2_k0.md:69-72`); |H_l| ≤ (s₀ + 1)C₀(1 + R_n)^{d₀} = O((log n)^{d₀})
  (`L2_k0.md:96-97`). (L-feas): `L2_k0.md:73-75`.
* (L-gain-R): for l ∉ Q, every truth j has δ(l, j) > d_n, so by CD_M(a) |Cov(W_l, W_j | W_{U₀})| ≤ K₂e^{−t₂d_n} ≤
  K₂n^{−1/2} for every U₀ ∌ l, j (`L2_k0.md:76-77`): C_L := K₂.
* (L-loc-R): for v ∈ U ∖ H_l, δ(v, l) > R_n and δ(v, k) > R_n for every k ∈ S₀, so by CD_M(a) both conditional
  covariances are ≤ K₂e^{−t₂R_n} ≤ n^{−2} (`L2_k0.md:106-109`). (A fortiori (L-loc-R′) of `L3b_rate.md`.)
* (D-R), in the form (D-loc) of `L4_formR.md`: N_l := Q ∩ (B(l, r_n) ∖ {l}), r_n = log log n,
  |N_l| ≤ C₀(1 + log log n)^{d₀} = o(log n); ‖β̄_{T,l} − β̄_{T∩N_l,l}‖₁ ≤ 2L₀ by RB_M; Var(W_l | W_{T∩N_l}) ≤
  (1 + κ(r_n)/c)Var(W_l | W_T) by TAIL_M (`L2_k0.md:139-149`).
Hence UNI-0's reported-model conclusion is the instance of RM-R for this class (UNI-0: "PROVED-CHECKED", council
Astra 9.0 / Opus 8.9; its lemma L2 "PROVED (by this seat, unchecked)", R02 "VERIFIED-WITH-AMENDMENTS").
Sub-instances recorded in UNI `STATEMENT.md:182-184`: APP Theorem LOC (1-D ordering), LOC2 LOC-d (sites in ℝ^d),
GROW (C5)(c) (iid-row AR(1) = study S2; separation gives PTV), GEN study S1/S3/S4/S6 bounded-block layouts with at
most one truth per independent group (PTV(cθ_lo)).

### (E-R2) Block-diagonal designs with growing one-factor groups = the class of Theorem LOC-BF
Class (LOC2 `STATEMENT.md:76-85`; `lemmas/L4_LOCd.md:70-74`): Σ_n block-diagonal; each group bounded with floor c, or
one-factor (b_v ∈ {0} ∪ [b_lo, b̄], incl. compound symmetry) of size ≤ (log n)^κ; **signal condition: at most one
truth per group** (then PTV(c_Bθ_lo) is automatic, `L4_LOCd.md:81-82`). Verification, with Q⁰ := ⋃_{j∈S₀}G(j), Q by
the enlargement rule, H_l := G(l) ∪ Q⁰ (`L4_LOCd.md:73, 87`):
* (T1-R), (FL-R): λ_min(Σ_n) ≥ c_B = min(c, 1 − b̄²) (`L4_LOCd.md:80`); no upper spectral bound (λ_max ≍ g_n allowed).
* (V-R): PTV(c_Bθ_lo). (L-size), (L-feas): `L4_LOCd.md:73`, LOC2 `lemmas/L1_toolkit.md:57-59`.
* (L-gain-R), (L-loc-R): independent groups stay conditionally independent (`L4_LOCd.md:79-80`); l ∉ Q lies in a
  truth-free group and v ∉ H_l lies in a group that is neither G(l) nor a truth group, so all three conditional
  covariances are exactly 0.
* (D-R): the latent-factor frames and idiosyncratic atoms of `L4_LOCd.md:93-112` ((R1) N_n ≤ p2^{g₀} + p; (R2)
  L = 1/b_lo; (R3) η_n = 0). The supplied construction verifies (D-R) directly, through the latent extension; (D-loc)
  is not needed (and no claim is made about whether the class satisfies it) [R06-9].
LOC-BF: inside W2-LOC2 "PROVED-CHECKED". The class contains sequences with |start mode ∖ S₀| ≫ log n (APP
`lemmas/L5_VN.md:74-106`, (V2) with g_n/log n → ∞ and Lemma VN) [R08-16].

## 7.2 Form F instances

### (E-F1) Exact-Gram AR(1) with separated truths (GROW (C5)(a))
GROW `STATEMENT.md:119-126`: XᵀX = (n − 1)Σ, Σ_ij = ρ^{|i−j|}, fixed ρ with 0 < |ρ| < 1, p ≤ n − 1, fixed s₀ and
**fixed nonzero coefficients θ*** (so BM-∞ and ‖μ‖² ≤ Mn hold) [R07-2]; **signal condition: separation**
Σ_{k∈S₀∖{j}}|θ*_k||ρ|^{|j−k|} ≤ ½|θ*_j|(1 − ρ²)/(1 + ρ²); the source proves (H0), (G1)–(G3), (G4-dir) for
"any block partition with blocks of size ≤ 16". By Lemma B1′ (`L1_fixed.md`) "(G3) for every partition" is
(FL-16) + (V) + (L-gain); (G2) = (FL-Q); (G4-dir) is (N-D)(i) with ρ_n = 0; |Q| = O(log n), so BM-∞ gives (BM-Q).
Hence it is an instance of RM-F (GROW "PROVED-CHECKED"; L5 R04 "VERIFIED-WITH-AMENDMENTS").

### (E-F2) Exact-Gram orthogonal groups of bounded size, one truth per group
XᵀX/(n − 1) block-diagonal with groups of size ≤ γ̄ (fixed) and floor φ₀² on every group, p ≤ n − 1; at most one
truth per group; **signal condition: BM-∞ and bounded energy ‖μ‖² ≤ Mn** (e.g. bounded coefficients: ‖μ‖² =
(n − 1)Σ_{S₀}θ*²_j here, the truths being mutually orthogonal) [R06-5]. Q := ⋃_{j∈S₀}G(j) (|Q| ≤ s₀γ̄). Verification [written out here]:
* (FL): a principal submatrix of a block-diagonal matrix with blockwise floor φ₀² has floor φ₀²; so (FL-16), (FL-Q)
  and the floors of (T1-F) hold (SE_λ for every size; SE_w with any fixed g₀ once (n − 1)φ₀² ≥ g₀). The remaining
  parts of (T1-F) — ‖μ‖² ≤ Mn and BM-∞ — are the assumed signal condition; fixed s₀ and p ≤ n^A are in Setting F.
* For any U and l, P_U = P_{U∩G(l)} + P_{U∖G(l)} (orthogonal groups) and P_{U∖G(l)}x_l = 0, so u_{U,l} ∈
  span X_{(U∪{l})∩G(l)}. (V): for a truth j, μ = θ*_jx_j + (terms in other groups, orthogonal to span X_{G(j)}), so
  δ_{U,j} = θ*_j‖(I − P_U)x_j‖ and δ²_{U,j} ≥ θ*²_j(n − 1)φ₀² ≥ M_n log n by BM-∞. (L-gain): for l ∉ Q the group G(l)
  has no truth, μ ⊥ span X_{G(l)}, so δ_{U,l} = 0 (η = 0).
* (L-feas): |Q| ≤ s₀γ̄ bounded; if p < 2|Q| + 32s₀ + 1 take Q := [p] instead (then (L-gain) is vacuous and |Q| is
  still bounded); otherwise K ≥ 2|Q| + 32s₀ + 1 for n large. (N-χ): |Q ∖ S₀| is bounded, hence ≤ (1 − δ₀) log n eventually.
(For fixed p the enumeration branch eventually applies; the instance has content for p → ∞, cf. GROW's council
remark, GROW `STATEMENT.md:137-141`.)

### (E-F3) S5 population covariance at fixed p (GROW (C5)(b); illustration only)
GROW `STATEMENT.md:127-141`: block-relative form on the coded partition, Q = [p], (G4-χ) = (N-χ); (G3b) by the exact
rational certificate τ₀ > 0. Instance of the block-relative variant of RM-F; membership in the partition-free form is
not established by this certificate, which covers within-block conditioning sets only [R06-9].

## 7.3 Results whose own proofs do not go through (V) + (L) at polylogarithmic size [R06-6, 7, 8]

These rows describe what the cited *proofs* use; they are not claims that every member of the family violates the
assumptions (members can overlap with RM-F/RM-R: e.g. Σ = I satisfies polynomial decay for every α and is a UNI-0
instance with bounded Q).

| result (family as an example) | why it is not obtained from RM-F/RM-R as stated | how it relates |
|---|---|---|
| Polynomial decay α > 17/2 on a line (LOC2 (D3), `STATEMENT.md:87-93`) | its proof (LOC2 L6) uses a relevance set of radius ⌈Dn^{1/(2α)}⌉, an upper envelope of polynomial size — outside (L-size) | LOC2 L6 (inside W2-LOC2 "PROVED-CHECKED") proves Sand, NA, TL for that Q; then RM-0 applies |
| One common factor with limsup log p/log n < α₀(κ̄) (UNI-1, UNI `STATEMENT.md:112-134`); exact compound symmetry beyond that exponent is a separate family-specific result (FAC-B; UNI `STATEMENT.md:138, 187`) | its proof works on the full lattice Q = [p]; \|Q\| = p is polylogarithmic only if p is | full-lattice engine (U-LOC, k = 1), then RM-0 with Q = [p] |
| Masked hubs (W1-PXN), W1-GEN's masked cases | (V) fails by construction: a truth is masked inside its block | W1-PXN, W1-GEN ("PROVED-CHECKED"): LS0 re-adds the masked truth from a bounded centre |
| Exact-Gram compound symmetry with K < p ≤ n − 1 (FAC-PK, status "PARTIAL relative to the brief; (P1)–(P5) on the exact-Gram stage: PROVED-CHECKED"; Theorem NEG, `Theory_work/Wave2/W2-FAC-PK/REPORT.md:7-9, 24-31`: fixed ρ, nonzero sign-corrected total signal, (PK) liminf p/K > 16/15, (PB) all but boundedly many blocks of size 16, its execution premises) | every start maximiser has size K (its (P1)); Q = [p] is infeasible when p > K, and no Q with K ≥ 2\|Q\| + 32s₀ + 1 contains the start mode | a limit of the route: LS0 with any cap ≤ \|S̃₀\| − s₀ − 2 + ⌊n^β⌋ (β < ½), hence with the shipped cap, never scores S₀; a statement about LS0 only — nothing is said about the full method, and p ≫ n is open |

## 7.4 The examples table (for the paper)

| # | family (example only) | form | Q | signal condition | lattice condition supplied by | source status |
|---|---|---|---|---|---|---|
| 1 | metric-local Σ: AR/banded, spatial in ℝ^d, graph-local, bounded blocks | R | radius-d_n neighbourhood of S₀, \|Q\| = O((log n)^{d₀}) | PTV(a₀) | (D-loc): balls of radius log log n | UNI-0 "PROVED-CHECKED" |
| 2 | block-diagonal, one-factor groups of size ≤ (log n)^κ (incl. compound-symmetric groups) | R | the truths' groups | ≤ one truth per group | (D-R) with latent factors | LOC-BF, W2-LOC2 "PROVED-CHECKED" |
| 3 | exact-Gram AR(1), 0 < \|ρ\| < 1 | F | radius ⌈log n/(2 log(1/\|ρ\|))⌉ around S₀ | fixed nonzero coefficients; separation of truths | (N-D)(i), ρ_n = 0 | GROW "PROVED-CHECKED" |
| 4 | exact-Gram orthogonal bounded groups | F | the truths' groups | BM-∞, ‖μ‖² ≤ Mn | (N-χ) | this file |
| 5 | S5 population covariance, fixed p | F, block-relative | [p] | certificate τ₀ > 0 | (N-χ) | GROW "PROVED-CHECKED" (illustration) |

In every row Q is taken with the feasibility enlargement: Q := [p] whenever p < 2|Q⁰| + 32s₀ + 1 for the displayed set
Q⁰ (so that (L-feas) holds) [R07-3].
