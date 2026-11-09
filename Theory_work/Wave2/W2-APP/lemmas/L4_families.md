# L4 — Family map: which design families satisfy which hypotheses (v2)

Status: each entry is either **cited** (status verbatim from its source) or **derived here** from L1_POST, L2_CT,
L3_LOC (incl. LOC-B), L5_VN — derived entries: **PROVED (by this seat, unchecked)**. Check record: R05 (Codex
gpt-6.1-sol high, `reviews/R05_L4_check_sol.md`): v1 FALSE as written (6 MAJOR, 3 MINOR: overstatements and missing
hypotheses, no FATAL); all nine repairs applied in this v2 [R05-#]; re-checked by sweep R07 (findings #2, #3, #18 applied [R07-#]). Council r1: Sol issue 1 (enumeration override, new
lemmas/L6_ENUM.md) and issue 2 / Opus issue 2 (polynomial-tail qualifier) applied [C1-#]. **ENUM override (v2, council r2):**
every row's reported-model status is 'covered' — by exact enumeration + POST (L6_ENUM) — on every sequence for which
the coded exact-branch inequality (EXB) holds eventually (sufficient: 2^{p_n} ≤ 4np_n, e.g. fixed p, p_n ≤ c log n with
c < 1/log 2); the 'unproved' / 'route-obstructed' statuses below refer only to sequences on which (EXB) fails
infinitely often. Mid-point R06 (Sol xhigh): CONTINUE; its three map corrections are in v2 (issues
1, 3 were already fixed by R05; issue 2 added) [R06-#].
Setting: STATEMENT §1 (iid Gaussian rows, unit-diagonal Σ_n = population correlation, p ≤ n^A, fixed s₀ and
|θ*_j| ∈ [θ_lo, θ_hi] on the **sample-standardised** scale, σ² fixed). Every entry separates **(Σ)** covariance-class
membership ("Σ ∈ LOC" etc.), **(θ)** signal conditions that must be ADDED (never claimed to hold), and **(T)** the
theorem that then applies. "Covered" always means: under the stated (θ) conditions and the implementation premises of
STATEMENT §1; no delivery (P(𝒪) → 1) claim anywhere. All results asymptotic.

Abbreviations: POST = L1_POST (posterior level, T03♯ under the joint law); LOC = Theorem LOC (L3_LOC; shipped LS0
cap ℓ_n + |S̃₀|); LOC-B = L3_LOC §L3.8B; VN = L5_VN (route obstruction); GEN, GROW, PXN, MIS as in FIN.
**Study sequence** [R05-7]: the asymptotic sequences of GEN (C5)(d) / GROW (C5)(c): groups of 5 consecutive indices,
p_n = 5G_n → ∞, p_n ≤ n^A, s₀ = 14 at one of the generator's two fixed high-p layouts (step 7 / step 13; positions and
the 14-entry pattern β^pat as in `Scripts/Data_generators/gen_dev_data.R`), signal c·β^pat on standardised columns
with a fixed c > 0, σ² = 1, iid N(0, Σ_s) rows. Not the p = 30 layout, not shrinking c, not the finite n = 200 runs.

## Auxiliary facts proved here

**F1 (Toeplitz spectrum).** Let γ(h) = ∫_{−π}^{π}e^{ihλ}f(λ)dλ for an integrable spectral density f ≥ 0 and
Σ_jk = γ(j − k)/γ(0). (i) If f ≥ m > 0 a.e., every principal submatrix of Σ (any finite index set) has λ_min ≥
2πm/γ(0). (ii) If also f ≤ M a.e., λ_max ≤ 2πM/γ(0). *Proof.* For v supported on a finite J ⊂ ℤ,
vᵀΓ_Jv = Σ_{j,k∈J}v_jv_kγ(j − k) = ∫|Σ_{j∈J}v_je^{ijλ}|²f(λ)dλ, and ∫_{−π}^{π}|Σv_je^{ijλ}|²dλ = 2π‖v‖² (orthogonality);
bound f below/above. ∎ No summability or upper bound is needed for (i) [R05-9]; e.g. long-memory covariances with an
integrable density bounded below a.e. satisfy (i). For sequences, m/γ(0) must be uniform in n.

**F2 (bounded block-diagonal with a spectral floor ⇒ LOC).** If Σ is block-diagonal with blocks of size ≤ g (fixed)
and each block has spectrum in a common [c, C] with c > 0 fixed [R05-5], order the blocks consecutively by π; then Σ
is banded with bandwidth g − 1, so Σ ∈ LOC(c, C, e^{g−1}, 1) (L2_CT §L2.3(i)/(iii)). (For unit diagonal and bounded g,
C ≤ g automatically; the floor c must be assumed: size-2 blocks with ρ_n = 1 − n⁻² have λ_min = n⁻².) Equicorrelated
block of size g, correlation ρ: eigenvalues 1 − ρ (mult. g − 1) and 1 + (g − 1)ρ; so ρ in a fixed compact subset of
(−1/(g − 1), 1) gives fixed [c, C].

**F3 (PTV sufficient conditions).** (i) ≤ one truth per independent component (block-diagonal): for j ∈ S₀ and any
U ∌ j, Cov(W_j, Σ_kθ*_kW_k | W_U) = θ*_jVar(W_j | W_U) (other truths are independent of (W_j, W_{U∩G(j)}), and
conditioning on independent components does not change this), so PTV(cθ_lo) with c = λ_min(Σ). (ii) Separation in
LOC: if |θ*_j|c − K₂Σ_{k∈S₀∖{j}}|θ*_k|e^{−t₂d(j,k)} ≥ a₀ for every j ∈ S₀, then PTV(a₀), because
Cov(W_j, Σ_kθ*_kW_k | W_U) = θ*_jVar(W_j | W_U) + Σ_{k∉U∪{j}}θ*_kCov(W_j, W_k | W_U) (terms with k ∈ U vanish) and
Lemma CD; in particular if min_{j≠k∈S₀}d(j, k) ≥ D* := t₂⁻¹log(2s₀θ_hiK₂/(cθ_lo)) then a₀ = cθ_lo/2.
(iii) AR(1): GROW's separation (6.0) gives PTV with a₀ = (θ_lo/2)(1 − ρ²)/(1 + ρ²) (GROW L6.2, TV paragraph).
(iv) **PTV can fail** with two truths in one block: block {1, 2}, ρ = ½, θ* = (1, −2): the matrix product Σ·θ* = (0, −1.5)ᵀ, so
Cov(W₁, W₁ − 2W₂) = 0 at U = ∅. Such configurations have Σ ∈ LOC but fail PTV, so Theorem LOC does not apply
[R05-8]; GEN/PXN cover specific masked families under their own hypotheses — no general claim here.

**F4 (MIS projected support, bounded block-diagonal).** Under MIS (iii)'s own model (rows iid N(m, Σ) jointly
Gaussian, RAW-scale linear model with fixed raw slopes, candidate set 𝒞, omitted active set ℳ := S₀ ∖ 𝒞) with Σ
block-diagonal (groups G): γ = Σ_{𝒞𝒞}⁻¹Σ_{𝒞ℳ}β_ℳ is supported in 𝒞 ∩ ⋃_{k∈ℳ}G(k). *Proof.* Σ_{𝒞𝒞} is block-diagonal
along the groups, so is its inverse; Σ_{𝒞k} is supported on 𝒞 ∩ G(k). ∎ Hence |S₀^𝒞| ≤ s₀ max_G|G|. This gives
bounded support SIZE only; a fixed positive support cardinality, projected beta-min, fixed τ² and (H-MIS) are NOT
implied (cancellation possible).

## The map (Σ / θ / T)

**(a) iid / isotropic, Σ = I.**
(Σ) LSF with φ = 1; Σ ∈ LOC with any fixed (K, a). (θ) PTV automatic, a₀ = θ_lo (F3(i), components of size 1).
(T) POST: holds. LOC: covered. GEN: the study sequence's S1 is covered by GEN (C5)(d) (cited: GEN "PROVED-CHECKED";
SEL "VERIFIED-WITH-AMENDMENTS"), production cap ℓ_n. MIS (raw-slope model): γ = 0, S₀^𝒞 = S₀ ∩ 𝒞,
τ² = Σ_{k∈ℳ}β_k²Var(W^r_k).

**(b) General Σ with spectrum in [c, C] (bounded condition number) — the key general statement.**
(Σ) LSF with φ² = ψ_n = c: **POST holds for every such Σ, any p ≤ n^A** (only λ_min ≥ c is used).
Reported model: bounded spectrum alone does **not** suffice for any current route: STAR (L5_VN (V1): spectrum
{½, 1, 3/2}, m_n = ⌊n^{1/3}⌋ leaves; append independent coordinates for p ≫ n) has every maximiser of γ₀ containing
≥ min(K − 1, m_n − 15) nulls w.p. → 1, which obstructs the GEN and GROW/LOC routes (necessary for these routes; the
method's behaviour there is not determined). If in addition **Σ ∈ LOC(c, C, K, a)** — exponential decay along some
bijection π (unknown to the method) — and (θ) PTV holds, **(T) Theorem LOC applies** (any coded partition; no
partition condition). Reading: a general sufficient condition is "bounded spectrum + exponential locality along some
ordering + PTV"; no necessity is claimed [R05-8].

**(c) AR(1) and stationary Toeplitz.**
AR(1), fixed 0 < |ρ| < 1: (Σ) spectrum [(1 − |ρ|)/(1 + |ρ|), (1 + |ρ|)/(1 − |ρ|)], Σ ∈ LOC(·, ·, 1, log(1/|ρ|)).
(θ) separation (6.0) or PTV. (T) POST; GROW (C5)(c) under (6.0) (cited: C-GROW "PROVED-CHECKED"; covers asymptotic
extensions of the study's S2 layouts, every c > 0); LOC under PTV. GEN: the study sequence's S2 is outside GEN's
sufficient class (GEN L6 (d) "Not covered", cited) — a statement about that sequence only, not about every AR(1)
regime [R05-7]. MIS: Prop. P(d) (cited, C-MIS "PROVED-CHECKED") [R05-3]: with exactly ONE active omitted variable k
(nonzero raw slope), a candidate that is null in the full model is a proxy iff Θ_jk ≠ 0 for Θ the precision of the
MARGINAL vector (W_𝒞, W_k); for AR(1) these are the nearest retained coordinates on either side of k (when present),
not necessarily k ± 1. With several active omissions only support containment holds and contributions can cancel
(AR(1), ρ = ½, 𝒞 = {2}, ℳ = {1, 3}, β = (1, −1): γ₂ = ½ − ½ = 0).
Stationary Toeplitz with |γ(h)/γ(0)| ≤ K′ϱ^h (ϱ < 1 fixed; same normalisation as L2_CT §L2.3(iv)) and spectral density in [m, M], m > 0, uniformly in n
(e.g. causal invertible ARMA with fixed parameters — standard, not re-proved; the two properties are the hypotheses of
this entry): (Σ) F1 + L2_CT §L2.3(iv) ⇒ Σ ∈ LOC with uniform constants. (θ) PTV. (T) POST; LOC.
Polynomially decaying γ or long memory, with f ≥ m > 0 a.e. (F1(i)): **POST holds**. Non-membership in LOC [R07-18]
for the two-sided polynomial family |γ(h)/γ(0)| ≥ c′h^{−β} for ALL h ≥ 1 (fixed c′, β > 0; this includes long-memory
tails h^{2d−1}), p → ∞: take j = ⌈p/2⌉; for every m ≤ p/2 − 1 at least m indices k have |Σ_jk| ≥ c′m^{−β}. If
|Σ_jk| ≤ Ke^{−a|π(j)−π(k)|} for some bijection π, then |Σ_jk| ≥ ε forces |π(j) − π(k)| ≤ a⁻¹log(K/ε), so at most
2a⁻¹log(K/ε) + 1 indices qualify; with ε = c′m^{−β} this is O(log m) < m for m large — contradiction for p large. The
precision alternative (LOC-Θ) is excluded too, since by L2_CT Lemma CD(c) it implies (LOC-Σ) with changed constants.
(T) reported model: **unproved** — neither covered nor shown obstructed.

**(d) Banded / finite-range dependence.** Σ banded with FIXED bandwidth b (e.g. MA(q), q = b) or Σ⁻¹ banded with fixed
b (Gaussian Markov random field on a line, e.g. causal AR(b)), spectrum in a fixed [c, C] (for MA(q): invertible,
f ≥ m > 0 via F1). (Σ) LOC by L2_CT §L2.3(i)/(ii). (θ) PTV (e.g. truths ≥ D* apart, F3(ii)). (T) POST; LOC.
Growing bandwidth b_n → ∞: bandedness alone then gives no fixed LOC constants; such sequences are covered by LOC
if uniform exponential decay and spectral bounds still hold (R05-2 example: a single far entry
e^{−(p−1)}/4), otherwise **not classified here** [R05-2]. MIS: general banded precision NOT settled (marginalising
excluded nulls can create fill-in, R01 item 9); no claim.

**(e) Block-diagonal with blocks of bounded size g (any fixed g, incl. g > 16) and a uniform spectral floor**
[R05-5]. (Σ) F2 ⇒ Σ ∈ LOC. (θ) ≤ one truth per block ⇒ PTV automatic (F3(i)); several truths per block ⇒ PTV is a
genuine condition and can fail (F3(iv)). (T) POST; LOC (shipped cap; no partition condition). **Study S1, S3, S4, S6**
(the study sequence: groups of 5, one truth per group, within-ρ ∈ {0, 0.7, 0.85, 0.4…0.9}, between 0; eigenvalue
envelopes [1,1], [0.3,3.8], [0.15,4.4], [0.1,4.6] — R05 recomputation): covered by GEN (C5)(d) via (C4) with the
production cap ℓ_n (cited: GEN "PROVED-CHECKED"; SEL "VERIFIED-WITH-AMENDMENTS"), and also by LOC with the shipped
cap (F2, F3(i): standardised-signal convention, which is the generator's).
**LH-iid (masked pairs; PXN)** [R05-6]: a separate, cited RAW-SLOPE model (FIN `s5_hpm.tex` §PXN: raw rows, truth
θ_{j_a} = β_i, θ_{j_b} = −ψ_iβ_i on the raw scale with exact population masking; independent components are the linked
pair units of size ≤ 2g, not the g-groups). PTV fails at the masked b-hubs by design, so Theorem LOC does not apply;
Theorem PXN (cited, "PROVED-CHECKED") covers it under all LH-iid hypotheses incl. SIZE (9 ≤ g ≤ 16 asymptotically).
No standardised-signal version of the masking is claimed. MIS: F4.
**Role of make_blocks.** LOC/LOC-B/VN: none — any X-measurable partition with blocks ≤ 16 (the method's B ≤ 16).
GEN (C5)(d)/SEL: uses that, on the concentration event, every actual block is a union of whole groups (proved there
for within-correlation ≥ 0.4 > between = 0; S1: any partition) — containment of whole groups, not equality.
PXN: partition recovery P(blocks ≠ groups) → 0 under SIZE (Theorem PXN (R)).

**(f) Equicorrelated blocks of growing size g_n → ∞, fixed ρ ∈ (0, 1), ≤ one truth per block.**
(Σ) λ_min = 1 − ρ (LSF holds), λ_max = 1 + (g_n − 1)ρ → ∞; not in LOC with fixed constants (Σ_jk = ρ at distance up to
g_n − 1 in any ordering of a block). (θ) PTV automatic (F3(i)). (T) POST holds. LOC-B: covered under ALL its
hypotheses [R05-4]: s₀(g_n − 1) ≤ (1 − δ₀) log n AND, when the enlargement rule gives Q = [p] (p < 2|Q⁰| + 32s₀ + 1),
p − s₀ ≤ (1 − δ₀) log n. VN (V2) ⇒ GEN route obstructed as soon as g_n → ∞; GROW/LOC sandwich obstructed when
g_n/log n → ∞. **Unproved**: every case where either LOC-B bound fails but g_n/log n does not diverge (NA would need a
new direction count). (Within-block covariance with uniform exponential decay and spectral bounds: (d).)

**(g) Equicorrelation / factor models (pervasive correlation)** [R05-1] — three separate sub-rows.
(g1) **Fixed positive equicorrelation** Σ = (1 − ρ)I + ρ11ᵀ, fixed ρ ∈ (0, 1): (Σ) LSF with φ² = 1 − ρ ⇒ **POST
holds** (λ_max ≍ p irrelevant); Σ ∉ LOC for any fixed constants once p → ∞ (Σ_jk = ρ for all pairs). (T) reported
model: VN (V3) — if |Σ_kθ*_k| ≥ θ̄₀ > 0, every maximiser of γ₀ contains ≥ min(K − s₀, p − 16s₀) nulls, obstructing GEN
if p → ∞ and GROW/LOC if p/log n → ∞ (R04-1: for p ≍ √(log n) GROW still applies with Q = [p]). Σ_kθ*_k = 0: no claim.
(g2) **Varying equicorrelation** ρ_n with 1 − ρ_n bounded below: POST holds; VN only after verifying VNF
quantitatively (ρ_n = 1/n gives squared visible correlations of order n⁻² — VN does not apply); no general claim.
(g3) **Factor models** with a fixed floor of the population CORRELATION matrix (raw BBᵀ + D, D ⪰ dI, bounded raw
variances suffices; a raw idiosyncratic floor alone does not — R02-1): POST holds. Locality depends on the loadings:
geometrically decaying loadings can give Σ ∈ LOC (R05-1 example b_j = 2^{−j}: spectrum ⊂ [¾, 4/3], Theorem LOC applies
under PTV). One-factor with |b_l| ≥ b₀ on a null set 𝒩_n and |b_{S₀}ᵀθ*| ≥ β₀ (all V4 floors): GEN obstructed if
|𝒩_n| → ∞, GROW/LOC if min(K, |𝒩_n|)/log n → ∞. Cancellation — including WEIGHTED factor cancellation
b_{S₀}ᵀθ* = 0 with Σ_kθ*_k ≠ 0 (R06-2: θ* = (1, 1), b = (½, −½) on S₀, b_l = ½ on nulls, Ψ = ¾I: every null has zero partial
correlation with the response) — weak exposure, multi-factor: **no claim**.
Study S5 (0.3 common, 0.7 within groups of 5): Σ_S5 = 0.3·11ᵀ + 0.4H + 0.3I has correlation floor 0.3, so **POST holds**
for the study sequence's S5 (R06); GEN's sufficient class excludes the study sequence (GEN L6 (d), cited);
GROW frontier (C-GROW (C6), "Frontier (with evidence, not proved)"). Reported model on pervasive designs:
**W2-FAC-A "PROVED-CHECKED" (for its narrowed, flagged target: Theorem FAC-L — one global factor + bounded-size local blocks, class 𝔉(γ̄, ψ₀, κ̄), limsup log p/log n < α₀(κ̄) = 1/(2κ̄(κ̄+2)), = 1/6 for every block compound symmetry incl. CS and S5; iid-row version (L5) under (TV-pop); CS instances need (GC-CS), which fails at a = 1/2; W2-FAC-A/REPORT.md:20-24, :29-53)**; outside that class open; W2-FAC-B provisional at sync time [C3-Sol-1].
MIS: Prop. P remark (cited): a one-factor design can make s₀^𝒞 grow (outside MIS); cancellation can also remove proxies.

## Summary table

Columns: (Σ) class / POST / reported-model route and status. "under PTV" = (θ) added; all reported-model entries are
also under the implementation premises; none is a delivery claim.

| Family | POST (T03♯, joint law) | GEN | GROW | LOC / LOC-B | Reported model | Files |
|---|---|---|---|---|---|---|
| (a) iid | holds | study S1 (cited) | — | LOC (PTV automatic) | covered | L1, L3, GEN (C5)(d) |
| (b) spectrum ⊂ [c,C] | **holds** | not implied; STAR obstructs | not implied; STAR obstructs | Σ ∈ LOC ⇒ Theorem LOC under PTV | covered under exp. locality + PTV; route-obstructed for STAR | L1, L3, L5 (V1) |
| (c) AR(1), fixed 0<\|ρ\|<1 | holds | study S2 outside GEN class (cited) | (C5)(c) under (6.0) (cited) | LOC under PTV | covered under (6.0)/PTV | GROW L6, L3 |
| (c) Toeplitz, exp. decay, f∈[m,M] | holds | — | — | LOC under PTV | covered under PTV | F1, L2.3(iv), L3 |
| (c) Toeplitz, two-sided polynomial tail (uniform lower bound c′h^{−β}), f≥m, p→∞ | holds | — | — | Σ ∉ LOC (counting argument); polynomial upper envelope alone: not excluded | **unproved** (unless (EXB) eventually: ENUM) | F1, L1, L6 |
| (d) banded Σ or Σ⁻¹, fixed bandwidth, spectral bounds | holds | — | — | LOC under PTV | covered under PTV | L2.3, L3 |
| (e) bounded blocks (any g), spectral floor | holds | study S1/S3/S4/S6 (cited); LH-iid raw-slope: PXN (cited) | — | LOC under PTV (automatic if ≤1 truth/block) | covered under PTV; masked LH-iid via PXN | F2, F3, L3 |
| (f) growing equicorr. blocks, fixed ρ, ≤1 truth per block | holds | obstructed if g_n→∞ (VN) | sandwich obstructed if g_n/log n→∞ | LOC-B if s₀(g_n−1) ≤ (1−δ₀)log n and post-enlargement bound | covered (LOC-B); **unproved** otherwise unless g_n/log n→∞ (route-obstructed) | L3.8B, L5 (V2) |
| (g1) fixed equicorrelation | holds | obstructed if \|Σ_kθ*_k\| ≥ θ̄₀ > 0, p→∞ (VN) | obstructed if \|Σ_kθ*_k\| ≥ θ̄₀ > 0, p/log n→∞ | Σ ∉ LOC once p→∞ | **per FAC (pending)** | L5 (V3) |
| (g3) factor, correlation floor | holds | obstructed under V4 floors, \|𝒩\|→∞ | obstructed under V4 floors, min(K,\|𝒩\|)/log n→∞ | depends on loadings (can be LOC) | per FAC (pending) / LOC if local | L5 (V4), L3 |

"Obstructed" = the route's own conclusion (bounded start mode / O(log n) sandwich) is false w.p. → 1 — a statement
about the proof route, **not** about the method.
