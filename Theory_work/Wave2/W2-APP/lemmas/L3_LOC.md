# L3 — Theorem LOC: reported-model consistency for random exponentially-local Gaussian designs

Status: **PROVED (by this seat, unchecked)** — a generalisation of GROW `lemmas/L6_random_AR1.md` (cited as [L6];
status there: PROVED (by this seat, unchecked); checks R07 Codex Sol xhigh VERIFIED, R06 Opus
VERIFIED-WITH-AMENDMENTS, applied; inside C-GROW "PROVED-CHECKED"). This file is written as a **delta proof**: each
step of [L6] is listed with exactly which AR(1)-specific fact it used and the replacement. One step ([L6] L6.6, NA)
uses the AR(1) Markov property essentially and is re-proved in full (§L3.6). Check record: R03 (Codex gpt-6.1-sol xhigh, `reviews/R03_L3_check_sol.md`): Theorem LOC
VERIFIED-WITH-AMENDMENTS (no FATAL; NA window argument passed); LOC-B VERIFIED-WITH-AMENDMENTS as stated here (the
GAP concerned STATEMENT v1.1's omission of the enlarged-Q bound, now fixed); all four amendments applied [R03-#].
Falsification numerics: `numerics/n1_*` (approximate innovations), `numerics/n2_*` (sandwich and LS0 on local
designs); summary `numerics/NUMERICS_LOC_VN.md`.

## L3.0 Statement

**Zero-mean reduction [R03-2].** Replace the raw matrix by W − 1mᵀ and call it W. This leaves CW, X, Y, the
partition and every scored model unchanged; hence WLOG m = 0, and all Gaussian regression/norm statements below
(e_A, D_{T,l} with iid centred entries, χ² laws) hold as written.

**Setting.** STATEMENT §1 (raw rows iid N(m, Σ_n), Σ_n unit-diagonal, p ≤ n^A, A ≥ 1, p ≫ n allowed; fixed s₀ and
fixed coefficients θ*_j, |θ*_j| ∈ [θ_lo, θ_hi] on S₀; Y = Xθ* + Cε, ε ~ N(0, σ²I) independent of the raw design, σ²
fixed; response scaled inside the score). The method: v3.1 as merged at 4676af6, whose LS0 move cap is
ℓ^{LS0} = ℓ_n + |S̃₀| (= GROW's MR1); premises EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete scans, and "the emitted
LS0 centre is some maximiser of γ₀" (FIN `s5_hpm.tex:16`; satisfied by the coded routine by W1-N3(a), as in GROW).

**Hypotheses.**
* (LOC) Σ_n ∈ LOC(c, C, K, a) with fixed constants (L2_CT §L2.2): spectrum in [c, C] and exponential decay of Σ_n or of
  Σ_n⁻¹ along a bijection π_n : [p] → [p]; d(j, k) := |π_n(j) − π_n(k)|. (K₂, t₂) are the constants of Lemma CD.
* (PTV(a₀)) for every j ∈ S₀ and every U ⊆ [p] ∖ {j} with |U| ≤ 15: |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀, a₀ > 0 fixed.

**Relevance set.** d_n := ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉, 𝒫⁰ := {l ∉ S₀ : min_{k∈S₀} d(l, k) ≤ d_n},
Q⁰ := S₀ ∪ 𝒫⁰; Q := Q⁰ if Q⁰ = [p] or p ≥ 2|Q⁰| + 32s₀ + 1, else Q := [p]. Then |Q| ≤ s₀(2d_n + 1) ∨ (2|Q⁰| + 32s₀)
= O(log n); 𝓛 := {T : S₀ ⊆ T ⊆ Q}.

**Theorem LOC.** Under the setting and (LOC), (PTV), for any X-measurable partition with blocks of size ≤ 16 (in
particular the coded partition), under the joint law of (X, ε):
  P(S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω) → 1,  P(NA(𝓛)) → 1,  P(TL(𝓛)) → 1;
and with the premises: D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1).
Also 1 − π(S₀) = O_P(√(log n/n)) (by L1_POST, since (LOC) gives λ_min(Σ_n) ≥ c).

## L3.1 Inputs (statuses verbatim)
[L6] and its inputs: GROW L0 (toolkit), L1 (descent), L2.1, L2.2, L4 (assembly) — PROVED (by this seat, unchecked),
checks R03/R04 as recorded in [L6] §0; [OP] PROVED (by this seat, unchecked) inside GEN PROVED-CHECKED; T03♯ PROVED;
SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2); M5(0)/T38-(0) PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5)).
New inputs from this ticket: L2_CT (Lemma CT, Lemma CD), L1_POST.
**AR(1) facts used by [L6]** (GROW L5 (P1)–(P4)): (P1) spectrum in [c₋, c₊]; (P2) Markov nearest-neighbour regression;
(P3) Var(W_l | W_U) ≥ c₋-type floor; (P4) |Cov(W_j, W_k | W_U)| ≤ r^{|j−k|} for all U. **Replacements:** (P1) → spectrum
in [c, C]; (P3) → Lemma CD(b) (Var(W_j | W_U) ≥ c, and every conditional covariance matrix has spectrum in [c, C]);
(P4) → Lemma CD(a) (|Cov(W_j, W_k | W_U)| ≤ K₂e^{−t₂d(j,k)} for all U); (P2) → not available; §L3.6 replaces its
only use. The separation condition (6.0) of [L6] was used only through "the population residual covariance of W_j with
Σθ_kW_k given W_U is ≥ a₀ for |U| ≤ 15" — this is exactly PTV(a₀).
**Linear-growth fact (replaces "index line" counting).** Because π_n is a bijection onto [p] ⊂ ℤ, for every l and
R ≥ 0, |{v : d(v, l) ≤ R}| ≤ 2R + 1, and for every d ≥ 1 at most two v have d(v, l) = d.

## L3.2 Regularity (= [L6] L6.2)
[L6] L6.2 proves: an entrywise event (raw centred columns + noise column, error ħ_n = C_A√(log n/n)), X-events A_X
and a joint event A_cov, on which (H0), (G1), (G2), (G3a), (G3b) hold with common constants and bounded-size sample
partial correlations are within O(ħ_n) of population values. Step by step:
* entrywise concentration, polarisation, union over (p + 1)² entries: Gaussian + unit variances only — unchanged
  (the noise coordinate is independent with unit variance after division by σ).
* Gram submatrices of size ≤ C_m log n have operator error o(1); "population eigenvalues in [c₋, c₊]" → in [c, C];
  sample floor c/2: unchanged with c. Covers (G2) (|Q ∪ {l}| = O(log n)), all blocks (G3a), and SE.
* m♯_n = O(log n), SE_w with g₀ = 1, φ₀² = c/2, energy, BM-∞: unchanged (also L1_POST).
* TV (G3b): [L6] uses P3/P4 + (6.0) to get a population residual covariance ≥ a₀ for every j ∈ S₀, |U| ≤ 15; here
  PTV gives it directly. The perturbation argument (bounded dimension, inverse norms ≤ 2/c, fixed coefficients θ*_j,
  sample-scale coefficients θ*_j/t_j within O(ħ_n) of θ*_j) is unchanged, with residual column variance ≤ 1. Hence
  δ²_{U,j} ≥ N a₀²/4 eventually, M_n := N a₀²/(4 log n).
* A_cov (bounded-size sample conditional covariances/partial correlations involving Y within O(ħ_n)): uses only that
  conditional design variances are ≥ c (CD(b)) and the residual variance of Y given any design subset is ≥ σ² —
  unchanged.
* (G1): |Q| = O(log n) and the dichotomy "Q = [p] or K ≥ 2|Q| + 32s₀ + 1" by construction of Q, as in [L6] §0.
* A_score (L0 events for the two families of [L6] §1): their sizes (≤ 17(p + 1)^{16}, ≤ Cp2^{|Q|}) are polynomial in n
  since |Q| = O(log n); Gram floors from the regularity event — unchanged.

## L3.3 Selection removal (= [L6] L6.3)
Replace R_n := ⌈2 log n/log(1/r)⌉ by R_n := ⌈(2 log n + log K₂ + log(1 + s₀θ_hi))/t₂⌉ and the neighbourhood by
H_l := {j : min_{k∈{l}∪S₀} d(j, k) ≤ R_n}; |H_l| ≤ (s₀ + 1)(2R_n + 1) = O(log n) by the linear-growth fact, so
|I_l| ≤ C(1 + log n)^{15}. The proof's population inputs: (i) |Cov(W_l, W_v | W_{U₀})| ≤ K₂e^{−t₂d(l,v)} ≤ n^{−2} for
v ∉ H_l (CD(a)); (ii) |Cov(Y, W_v | W_{U₀})| ≤ Σ_{k∈S₀∖U₀} |θ*_k/t_k| K₂e^{−t₂d(k,v)} ≤ C n^{−2} (CD(a); on the
entrywise event θ*_k/t_k is bounded; noise has zero population covariance); (iii) the population residual
correlation of W_l and Y given U₀ is ≤ C s₀θ_hiK₂e^{−t₂d_n} ≤ C n^{−1/2} for l ∉ Q, since d(l, k) > d_n for all
k ∈ S₀ (CD(a)) and residual variances are ≥ min(c, σ²) (CD(b)). The rest (recursive partial-correlation formula,
‖a‖ + ‖b‖ ≤ Cħ_n, ‖R⁻¹‖ ≤ C) is algebra on the common event. Conclusion (6.4) unchanged:
|h_{U,l} − h_{U∩H_l,l}| ≤ ϖ_n = C(log n)^{3/2}/√n and h_{U,l} ≤ C log n, uniformly over l ∉ Q, |U| ≤ 15.

## L3.4 Spherical tail (= [L6] L6.4)
Regression W_l = W_{U₀}b + m_raw + e with D := U₀ ∪ S₀: (i) ‖α‖ ≤ C e^{−t₂d_n}·K₂ s₀^{1/2}/c, because the covariance
of W_l with the truth residuals given U₀ has entries ≤ K₂e^{−t₂d_n} (CD(a)) and the conditional truth covariance has
eigenvalues ≥ c (CD(b)); (ii) the b_j (regressions of truths on U₀, |U₀| ≤ 15) are bounded: ‖b_j‖ ≤ ‖Σ_{U₀U₀}⁻¹‖‖Σ_{U₀j}‖
≤ √15/c; (iii) e is independent of W_D with iid N(0, τ²) entries, τ² = Var(W_l | W_D) ∈ [c, 1] (CD(b)). Then
‖m‖ ≤ C√n e^{−t₂d_n} ≤ C by the choice of d_n, which is (6.8). The sphere argument, the integration (CN_D), (6.5)–(6.7)
and the counting p·L_n·exp(−t_n(k)/2) ≤ Ck n^{−1/2} are unchanged (they use |I_l| = exp(O(log log n)), p ≤ n^A).

## L3.5 Sandwich incl. the global size ladder (= [L6] L6.5)
Unchanged: it uses (6.10) (from L0.2(c) and L3.3), per-block optimality and the exact prior ratio, block size ≤ 16,
the counts J(t) of L3.4, the TV part of L3.2, and the construction of Q (feasibility of additions when Q ≠ [p]; Q = [p]
case). No AR(1) fact is used beyond those replaced in L3.2–L3.4. Conclusion: P(S₀ ⊆ S̃ ⊆ Q for every maximiser) → 1.

## L3.6 NA without the Markov property (replaces [L6] L6.6) — new
**Lemma L3.6.** Under the hypotheses of Theorem LOC (PTV not needed), P(NA(𝓛)) → 1.

*Proof.* By GROW L2.2 (on the L0 event for the lattice family, which holds w.p. → 1 under the joint law as in [L6]
§1 / L3.2), it suffices to show P(max_{T∈𝓛, l∉T} Z²_{T,l} ≤ c_n) → 1, where c_n := log(n + 1) + 2 log p − 2 log(|Q| + 1)
− 4κ_E − 2 and Z_{T,l} := u_{T,l}ᵀε/σ, u_{T,l} the normalised residual of x_l on X_T (it exists on the regularity event
by (G2)). All index pairs (T, l) below range over the **deterministic** family 𝔓 := {(T, l) : T ∈ 𝓛, l ∈ [p] ∖ T},
|𝔓| ≤ p·2^{|Q|} = n^{O(1)}. If 𝔓 = ∅ (e.g. p = s₀, Q = S₀ = [p]) NA(𝓛) holds vacuously; assume 𝔓 ≠ ∅ below [R07-17].

*Step 1 (exact identity).* For A ⊆ [p] ∖ {l} let β_A := Σ_{AA}⁻¹Σ_{Al} and e_A := W_l − W_Aβ_A ∈ ℝⁿ (raw columns; rows
iid). e_A has iid N(0, τ_A²) entries, τ_A² = Var(W_l | W_A) ∈ [c, 1] (CD(b)), and e_A is independent of W_A. Fix the
window radius r_n := ⌈log log n/t₂⌉ and B_l := {v : d(v, l) ≤ r_n}; for (T, l) ∈ 𝔓 put T′ := T ∩ B_l. Since
CW_l − Ce_{T′} = CW_{T′}β_{T′} ∈ span(CW_T) = span(X_T) (column scaling does not change spans),
  (I − P_T)x_l = t_l⁻¹(I − P_T)g,  g := Ce_{T′},  so u_{T,l} = h/‖h‖, h := (I − P_T)g.
(Exact; population coefficients, no Markov property.)

*Step 2 (reference statistics; few directions).* For each l, T′ ranges over subsets of B_l ∖ {l}; by linear growth
|B_l| ≤ 2r_n + 1, so the set 𝒲 := {(l, A) : l ∈ [p], A ⊆ B_l ∖ {l}} has N := |𝒲| ≤ p·2^{2r_n+1} elements and
log N = log p + O(log log n). For (l, A) ∈ 𝒲 put g_{l,A} := Ce_A and Z′_{l,A} := g_{l,A}ᵀε/(σ‖g_{l,A}‖). g_{l,A} is a
function of the raw design W and ε is independent of W, so conditionally on W each Z′_{l,A} is N(0, 1) (on
{g_{l,A} ≠ 0}, a probability-one event). A conditional union bound and integration give
  P(max_𝒲 Z′² > 2 log(2N) + 2 log log n) ≤ 1/log n.   (E1)
Also ‖g_{l,A}‖²/τ_A² ~ χ²_{n−1} in distribution (equivalently conditionally on W_A) (C is a rank-(n − 1) projection and e_A is isotropic); by the
χ² lower tail and a union bound over 𝒲: P(min_𝒲 ‖g_{l,A}‖² < c(n − 1)/2) ≤ N e^{−c′n} → 0.   (E2)

*Step 3 (the part of g inside span X_T).* Write e_{T′} = e_T + D_{T,l} with D_{T,l} := W_Tβ_T − W_{T′}β_{T′}
(= E[W_l | W_T] − E[W_l | W_{T′}] row-wise). Rows of D_{T,l} are iid N(0, v_{T,l}) with
  v_{T,l} = cᵀM⁻¹c,  c := Cov(W_l, W_{T∖T′} | W_{T′}),  M := Cov(W_{T∖T′} | W_{T′}).
[Proof: (e_{T′}, V), V := W_{T∖T′} − E[W_{T∖T′} | W_{T′}], is jointly Gaussian and independent of W_{T′}; W_T is a linear
bijective image of (W_{T′}, V); hence E[e_{T′} | W_T] = E[e_{T′} | V] = Cov(e_{T′}, V)M⁻¹V, and Cov(e_{T′}, V) = cᵀ;
moreover E[e_{T′} | W_T] = E[W_l | W_T] − E[W_l | W_{T′}] = D_{T,l}.] By CD(b), λ_min(M) ≥ c; by CD(a) and since every
v ∈ T ∖ T′ has d(v, l) > r_n with at most two v per distance,
  v_{T,l} ≤ ‖c‖²/c ≤ (2K₂²/(c(1 − e^{−2t₂}))) e^{−2t₂r_n} ≤ κ_D (log n)^{−2},  κ_D := 2K₂²/(c(1 − e^{−2t₂})).
Now P_TC = P_T (range P_T ⊆ span X_T ⊥ 1), CD_{T,l} ∈ span X_T, so
  P_Tg = P_Te_T + CD_{T,l},   ‖P_Tg‖ ≤ ‖P_Te_T‖ + ‖D_{T,l}‖.
(i) Conditionally on W_T, e_T has iid N(0, τ_T²) entries independent of the W_T-measurable projection P_T of rank
≤ |T| ≤ |Q|, so ‖P_Te_T‖²/τ_T² ~ χ²_{rank P_T}; with P(χ²_d > v) ≤ 2^{d/2}e^{−v/4} and v := 4[log|𝔓| + |Q| + 2 log n]
= O(log n), a union bound over 𝔓 gives P(max_𝔓 ‖P_Te_T‖² > v) ≤ n^{−2}. (ii) ‖D_{T,l}‖²/v_{T,l} ~ χ²_n (or D = 0);
Laurent–Massart with x = n/2 and a union bound over 𝔓 give P(max_𝔓 ‖D_{T,l}‖²/(v_{T,l} ∨ 0⁺) > 4n) ≤ |𝔓|e^{−n/2} → 0.
Hence, w.p. → 1, simultaneously over 𝔓:
  ‖P_Tg‖ ≤ √v + 2√(κ_D n)/log n =: b_n,  b_n² = O(log n + n/(log n)²).   (E3)

*Step 4 (comparison).* σZ_{T,l} = hᵀε/‖h‖ = (gᵀε − (P_Tg)ᵀP_Tε)/‖h‖. With Z′ := Z′_{l,T′} and ‖h‖ ≤ ‖g‖:
  |Z_{T,l} − Z′| ≤ |Z′|(‖g‖/‖h‖ − 1) + ‖P_Tg‖‖P_Tε‖/(σ‖h‖) ≤ |Z′|·‖P_Tg‖²/‖h‖² + ‖P_Tg‖‖P_Tε‖/(σ‖h‖),
using ‖g‖/‖h‖ − 1 ≤ ‖g‖²/‖h‖² − 1 = ‖P_Tg‖²/‖h‖². On (E2)–(E3), ‖h‖² = ‖g‖² − ‖P_Tg‖² ≥ c(n − 1)/2 − b_n² ≥ cn/4 for
n ≥ n₀. ‖P_Tε‖ ≤ ‖P_Qε‖ (span X_T ⊆ span X_Q), and conditionally on X, ‖P_Qε‖²/σ² ~ χ²_{≤|Q|}, so
P(‖P_Qε‖² > 4σ²(|Q| + log n)) → 0. On (E1)–(E3) and this event, uniformly over 𝔓,
  |Z_{T,l} − Z′| ≤ C√(log n)·(log n/n + (log n)^{−2}) + C(√(log n) + √n/log n)√(log n)/√n =: η_n → 0.
*Step 5 (threshold).* Z²_{T,l} ≤ (|Z′| + η_n)² ≤ 2 log(2N) + 2 log log n + 2η_n√(2 log(2N) + 2 log log n) + η_n²
= 2 log p + O(log log n) + o(√(log n)), while c_n = 2 log p + log n − O(log log n) (|Q| = O(log n)). Hence
max_𝔓 Z²_{T,l} ≤ c_n for n ≥ n₀ on events of probability → 1, and GROW L2.2 gives NA(𝓛). ∎

Remarks. (1) The only structural inputs are CD(a) (summable, exponentially small influence of far conditioning
variables), CD(b), and linear growth (window patterns: 2^{O(log log n)} = polylog). (2) [R03-3] For AR(1), [L6] L6.6 uses at most two nearest
conditioned neighbours, selected by their positions in T (their distances need not be one), giving at most p(|Q| + 1)²
reference innovations; the window construction here does NOT reduce to that with r_n = 1 (radius-one windows fail
already for AR(1), R03 item 3) — the growing window r_n = ⌈log log n/t₂⌉ is essential. (3) In dimension d ≥ 2
(|B_l| ≍ r_n^d) Step 2 still gives log N = log p + o(log n), but |Q| ≍ (log n)^d breaks |𝔓| = n^{O(1)} and GROW L0/L2;
not claimed.

## L3.7 TL (= [L6] L6.7)
Unchanged: conditional on X in A_X the hypotheses of GROW L2.1 hold with common constants; missing-truth signal ≥ cn
by (G2)-type floors and θ_lo; integrate.

## L3.8 Assembly (= [L6] §7)
Unchanged: L3.5–L3.7 give the three events; GROW L4 pathwise argument with L1 (deterministic descent) and [OP]: on
the three events, the LS0 path from any maximiser C ∈ 𝓛 of γ₀ deletes one element of C ∖ S₀ per move, scores S₀ if
ℓ ≥ |C ∖ S₀| − 1 and ends certified at S₀ if ℓ ≥ |C ∖ S₀|; the shipped cap ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀| suffices. Hence
D_n ≤ P(Sand_n^c) + P(NA^c) + P(TL^c) → 0. Posterior input: L1_POST (b) (instead of [L6]'s AR(1)-specific A_X, the
same diagonal argument). M5(0) integrated over the design gives P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E[1 − π(S₀)] + D_n → 0. ∎

## L3.8B Variant LOC-B: block-diagonal designs with growing blocks (small-logarithmic regime)

**Hypotheses.** Setting as L3.0, except (LOC) is replaced by: Σ_n block-diagonal with respect to a deterministic
partition into groups G of size ≤ g_n (no upper spectral bound), λ_min(Σ_n) ≥ c > 0 fixed; each group contains at
most one truth; PTV(a₀) (automatic here with a₀ = cθ_lo: for j ∈ S₀ and any U ∌ j, other truths lie in other,
independent groups, so Cov(W_j, Σθ*_kW_k | W_U) = θ*_jVar(W_j | W_U) and Var(W_j | W_U) ≥ c); and
  (B-χ) s₀(g_n − 1) ≤ (1 − δ₀) log n for a fixed δ₀ ∈ (0, 1); and, if p < 2|Q⁰| + 32s₀ + 1, also p − s₀ ≤ (1 − δ₀) log n.
Relevance set: Q⁰ := ⋃_{j∈S₀} G(j) (|Q⁰ ∖ S₀| ≤ s₀(g_n − 1)), Q := Q⁰ or [p] by the enlargement rule of L3.0.

**Claim LOC-B.** The three events and the conclusions of Theorem LOC hold.

*Proof (delta to L3.2–L3.8).* Independence across groups is preserved under conditioning on any set: for U ⊆ [p] and
v, w in different groups (or v in a group meeting neither w's group nor S₀ ∪ {w}), Cov(W_v, W_w | W_U) = 0 and
Cov(W_v, V | W_U) = 0 when v's group contains no truth. Replace CD(a) by these exact zeros and CD(b) by
Var(W_j | W_U) ≥ c, spectrum of conditional covariance matrices ≥ c (Schur complement ≥ λ_min(Σ_n)); the upper spectral
bound C was used in L3.2–L3.5 only through CD(a) (all other uses are "Var ≤ 1"). (L3.2) Sets of size O(log n) have
sample floor c/2 as before; TV from PTV. (L3.3) Take H_l := G(l) ∪ Q⁰ (size ≤ (s₀ + 1)g_n = O(log n), so
|I_l| = polylog); for l ∉ Q and v ∉ H_l the population covariances of W_v with W_l and with V given W_{U₀} are exactly 0,
and the population residual correlation of W_l and V given U₀ is 0 (l's group is truth-free); the algebraic part is
unchanged. (L3.4) α = 0 exactly (W_l is independent of the truth residuals given U₀), ‖b_j‖ ≤ √15/c, τ² ∈ [c, 1]; m = 0.
(L3.5) unchanged. (L3.6) NA: replaced by GROW L2.3(a): conditionally on X, on the regularity event (G2) holds for the
lattice (|Q ∪ {l}| = O(log n), floor c/2), and |𝒫| = |Q ∖ S₀| ≤ (1 − δ₀) log n by (B-χ) when Q = Q⁰. **Added hypothesis for the enlarged case:** if
Q = [p] (p < 2|Q⁰| + 32s₀ + 1), LOC-B additionally requires p − s₀ ≤ (1 − δ₀) log n; otherwise it is not claimed. L2.3(a) is a statement about the noise given the
design and needs only (G2) and the size bound, so P(NA(𝓛) | X) → 1 uniformly on the regularity event; integrate.
(L3.7), (L3.8) unchanged. ∎

Remark. For bounded g, LOC-B is contained in Theorem LOC (L4_families (e)); its content is growing g_n up to
(1 − δ₀) log n/s₀ + 1. For g_n/log n → ∞ the route is obstructed (L5_VN (V2)); in between, NA would need a new argument
(exchangeable innovations give 2^{g_n} distinct directions, too many for GROW L2.3(b)).

## L3.9 Scope
Not claimed: non-Gaussian rows; d ≥ 2 neighbourhood growth; growing s₀; θ*_min → 0 (BM(c) local alternatives);
PTV failures (masking — GEN/PXN cover bounded masking); delivery. LOC's constants (t₂ from Lemma CT) are explicit
and conservative (numerics/ct_check_out.txt "tightness" lines compare them with the true AR(1) decay rate) [R07-20].
