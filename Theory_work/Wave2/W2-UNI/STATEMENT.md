# W2-UNI — STATEMENT (design-agnostic main consistency theorem)

Ticket W2-UNI, Theory Wave 2. Lead: Claude Opus 5.5 (Claude Personal). Status of this file: **v1.1.4 — LOCKED** (2026-11-09; v1.1.1 = R04-1 editorial split of (i′); v1.1.2 = R05a sweep fixes
[R05a-1, 2, 5]: PLR scope stated explicitly, LS0 move count qualified by its event, FAC-L containment restricted to the
fixed-beta-min subclass; v1.1.3 = R05b-4 wording in §6; v1.1.4 = council C1 NIT-3, status wording in (i′); no UNI-0/UNI-1 hypothesis or conclusion changed)
after statement-lock review R01 (Codex gpt-6.1-sol high, LOCK-WITH-CHANGES; all eight required changes applied, see
`reviews/R01_disposition.md`; change markers [R01-#]). Protocol: `Theory_work/Wave2/PROTOCOL.md` (extends Wave1C and
Wave1 protocols). All results are asymptotic (n → ∞); finite-n behaviour is out of scope and never listed as a limitation.

**Felipe's requirement (binding).** The theorems are stated under general, mild assumptions on X; design families
(S1–S6, AR, CS, …) are examples only. This file states (A1)–(A3) and the theorems first; family results appear only in
the corollary table (§5).

Abbreviations. APP = `Theory_work/Wave2/W2-APP/`; LOC2 = `Theory_work/Wave2/W2-LOC2/`; FACA = `Theory_work/Wave2/W2-FAC-A/`;
FACB = `Theory_work/Wave2/W2-FAC-B/`; GROW = `Theory_work/Wave1C/C-GROW/`; GEN = `Theory_work/Wave1/W1-GEN/`;
FIN = `Theory_work/Wave1C/FINAL/sections/`. Method = production core v3.1 as merged on main at 4676af6 (LS0 from the
start mode with move cap ℓ_n + |S̃₀|; tie-aware start-mode DP; tier-1 calibration fallback). **No method change is
requested.**

## 1. Setting (as LOC2 STATEMENT §1 and FACA STATEMENT §1)

* **Design.** Either (R) *random design*: raw rows iid N(m_n, Σ_n), Σ_n unit-diagonal (WLOG by scale invariance;
  m_n arbitrary), X = centred, sample-standardised raw design; or (E) *approximate-Gram fixed design*: X centred and
  standardised with R̂ := XᵀX/(n − 1) satisfying ‖R̂ − Σ_n‖_op ≤ δ_n (δ_n = 0: exact Gram, p ≤ n − 1).
  p = p_n ≤ n^A, A ≥ 1 fixed.
* **Response.** Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of the raw design, σ² > 0 fixed; S₀ := supp θ*; response
  scaled inside the score (FIN s1).
* **Method and premises.** D0 score, capped BB(1, p) prior, K_n := min(p, ⌊n/2⌋), Ω = {|S| ≤ K_n}, block tables, start
  γ₀, start mode S̃₀, LS0 cap ℓ_n + |S̃₀|; implementation premises EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete scans,
  IND-T and the c₄ search when R′ > 4, "the emitted LS0 centre is some maximiser of γ₀" (named, not proved). Delivery
  claims use the premises and allocation of FACA L7 (Proposition F-FAC; CAL not assumed). Partition: any X-measurable
  partition with blocks of size ≤ 16 (in particular the coded one).
* **Events** (GROW L1, L3, L4; FACA §1): Sand_n(Q) := {S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω}; for
  𝓛 := {T : S₀ ⊆ T ⊆ Q}: NA(𝓛), TL(𝓛); D_n, 𝒪 (output), Ŝ⁺ (reported HPM), U_n as in GROW L4 / FIN s5.

## 2. General assumptions

Fixed constants: A, c, C, C₀, d₀, K, a, s₀, θ_lo, θ_hi, a₀, γ̄, κ̄ (independent of n); population objects may vary with n.

**(A1) Rows and dimension.** Setting (R) (or (E) where stated); p ≤ n^A.
* **(A1-post, random-design posterior)** [R01-1]. Let j₀ = ⌈(2A + 1)s₀⌉ + 1,
  m̄_n = ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n]/log(3/2)⌉, and k̄_n = min{p, s₀ + max(j₀, m̄_n)}. For fixed
  φ > 0, require λ_min(Σ_{n,S}) ≥ φ² whenever |S| ≤ min(p, s₀ + j₀), and λ_min(Σ_{n,S}) ≥ ψ_n whenever |S| ≤ k̄_n, where
  ψ_n√n/(log n)^{3/2} → ∞. No upper spectral bound is imposed. These are the sufficient LSF conditions of APP L1_POST;
  they are not asserted necessary. (Sufficient: λ_min(Σ_n) ≥ c.)

**(A2) Approximate factor structure with a local idiosyncratic part.** Σ_n = Λ_nΛ_nᵀ + Ψ_n with a fixed number k ≥ 0 of
factors (Λ_n ∈ ℝ^{p×k}; λ_max(Σ_n) ≍ p allowed) and Ψ_n ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a):

> **Definition (metric locality, LOC_M).** A symmetric matrix Ψ on [p] is in 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) if its spectrum
> lies in [c, C] (0 < c ≤ C), and there is a pseudometric δ on [p] with **polynomial growth**
> N_δ(r) := max_i |{k : δ(i, k) ≤ r}| ≤ C₀(1 + r)^{d₀} for all r ≥ 0, such that either (Σ-branch)
> |Ψ_jk| ≤ K e^{−a δ(j,k)} (j ≠ k) or (Θ-branch) |(Ψ⁻¹)_jk| ≤ K e^{−a δ(j,k)} (j ≠ k).

The pseudometric is arbitrary (n-dependent; unrelated to the method's partition or to any ordering); only its growth
function enters. Examples: index distance on a line (d₀ = 1); Euclidean distance between separated sites in ℝ^d (d₀ = d);
graph distance on a graph of polynomial growth; distance 0 within / p between blocks of size ≤ γ̄ (C₀ = γ̄, d₀ = 1).

For **k = 1** write Λ = λ ∈ ℝ^p and, for T ⊆ [p], l ∉ T:
  ψ_{l|T} := Ψ_ll − Ψ_{lT}Ψ_TT⁻¹Ψ_{Tl},  λ̃_{l|T} := λ_l − Ψ_{lT}Ψ_TT⁻¹λ_T,  s_T := λ_TᵀΨ_TT⁻¹λ_T.
* **(A2-1, subset exposure ratio)** [R01-5]. For a partition 𝒢_n into groups of size at most γ̄ (any partition, unrelated to
  Ψ and to the method's blocks), define c_{𝒢,n} = inf_{∅≠T⊆[p]} s_T/h_𝒢(T), h_𝒢(T) := #{g ∈ 𝒢 : g ∩ T ≠ ∅}, and
  κ′_n := sup_{T, l∉T} |λ̃_{l|T}|/√ψ_{l|T}. Require c_{𝒢,n} > 0 at each n and κ_n = κ′_n/√c_{𝒢,n} ≤ κ̄ for a fixed κ̄ ≥ 1.
  A uniform positive lower bound on c_{𝒢,n} is sufficient but is not required. For singleton groups, a uniform lower bound
  on every |λ_j| is one sufficient way to obtain that stronger condition.
  In the unit-diagonal representation Σ = λλᵀ + Ψ, |λ_j| ≤ 1 and ψ_{l|T} ≥ c; RB_M therefore implies κ′ ≤ (1 + L₀)/√c
  uniformly in n. Finiteness is automatic under the complete representation assumptions, not under LOC_M without a loading
  bound. This is a representation-dependent sufficient ratio condition for the full-lattice route. It is not asserted
  necessary for consistency. The stronger condition c_{𝒢,n} ≥ c₁ > 0 would force every loading to be uniformly bounded
  away from zero by singleton tests; that stronger condition is not imposed here. Neither condition should be identified
  without qualification with average factor pervasiveness.
* Growth exponent α₀(κ̄) := 1/(2κ̄(κ̄ + 2)) (FACA's formula; α₀(1) = 1/6).

**(A3) Signal.** s₀ = |S₀| ≥ 1 fixed; |θ*_j| ∈ [θ_lo, θ_hi] on S₀ (fixed beta-min θ_lo > 0); non-masking **PTV(a₀)**:
for every j ∈ S₀ and U ⊆ [p] ∖ {j} with |U| ≤ 15, |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀ (W a population row;
APP `lemmas/L3_LOC.md:28`). PTV is not used for (i); for (iii) it is one sufficient visibility condition (see (iii)).

**Mildness (justified in REPORT §6; not a claim).** (A1) is the Gaussian-row, polynomial-dimension setting of
Song–Liang-type results with a sparse eigenvalue floor (cf. sparse Riesz / restricted eigenvalue conditions); (A2) is an
approximate factor model in the sense of Fan–Liao–Mincheva (2013) / Fan–Ke–Wang (2020), with the idiosyncratic sparsity
replaced by **additional sufficient structure** — exponential decay along an arbitrary geometry of polynomial growth —
and, for k = 1, a bounded subset-exposure ratio [R01 optional]; (A3) is fixed sparsity, beta-min and "no masking by ≤ 15
conditioning variables" (automatic when truths sit in mutually independent groups).

## 3. Claims

**(i) Theorem UNI-P (posterior)** [R01-1]. Under design (R), (A1-post), polynomial dimension, fixed sparsity and the
signal bounds of (A3), without PTV, the joint-law posterior rate is 1 − π(S₀) = O_P(√(log n/n)), with the SL1 corollaries
in APP L1_POST(b). This is APP L1_POST(b), independent of any factor representation. Fixed exact-Gram designs are covered
separately under APP L1_POST(c). Approximate fixed Grams require verification of the T03♯ sample-design hypotheses and are
not covered by population LSF alone.

**(i′) Theorem PLR (general reported-model engine; LOC2 L5: "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS, inside W2-LOC2 "PROVED-CHECKED" [C1-B NIT-3])** [R01 optional]. Stated as the
principal abstract theorem [R04-1]. [R05a-2] Under setting (R) (random rows; this is not an (E)-design theorem), fixed
s₀, the coefficient bounds of (A3) (fixed beta-min θ_lo > 0, θ_hi) without PTV, and the method premises of §1, let Σ_n be
any population correlation sequence with a deterministic relevance set Q (|Q| ≤ (log n)^κ, feasibility
dichotomy, floor (N1)) such that P(Sand_n(Q)) → 1 and Lemma NA-R's (R1)–(R3) hold: (C-i) P(NA(𝓛)) → 1, P(TL(𝓛)) → 1 and
D_n → 0; (C-ii) **if additionally (A1-post)/LSF holds**, 1 − π(S₀) = O_P(√(log n/n)) and P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0
(output-intersected reported-model consistency); unconditional delivery P(Ŝ⁺ = S₀) → 1 only with F-UNI's premises (R4).
UNI-0 is the verification of these hypotheses under (A2, k = 0); LSF holds there (and in UNI-1) through λ_min(Σ_n) ≥ c, so
neither concrete theorem needs an extra assumption.

**(ii) Theorem UNI-0 (reported model, k = 0).** (R), Σ_n ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) (unit diagonal), (A3) with PTV, any
p ≤ n^A. Relevance set [R01-8]: with the conditional-decay constants (K₂, t₂) of CD_M, let
d_n = ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉ and Q⁰ = {l : min_{j∈S₀} δ(l, j) ≤ d_n}. Set Q = Q⁰ if p ≥ 2|Q⁰| + 32s₀ + 1,
and Q = [p] otherwise. Then |Q| = O((log n)^{d₀}); eventually Q = [p] or K_n ≥ 2|Q| + 32s₀ + 1. Conclusions, with the
shipped cap ℓ_n + |S̃₀|: P(Sand_n(Q)) → 1, P(NA(𝓛)) → 1, P(TL(𝓛)) → 1, D_n → 0, 1 − π(S₀) = O_P(√(log n/n)),
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1); and under the delivery premises/allocation,
P(no output) = 0 and **P(Ŝ⁺ = S₀) → 1**. The extra conditions beyond "Σ local" are exactly PTV and polynomial growth; no
condition on the partition or on the ordering.

**(iii) Theorem UNI-1 (reported model, k = 1, local Ψ).** Σ_n = λλᵀ + Ψ_n unit-diagonal with Ψ_n ∈ 𝓛𝓞𝓒, (A2-1),
**limsup log p/log n < α₀(κ̄)**, and [R01-2]: assume the fixed-sparsity and coefficient bounds of (A3). Under (R), assume
TV-pop of FACA STATEMENT §3 for a deterministic family 𝔅_n covering every realised method block on a design event of
probability tending to one. All-subset PTV(a₀) is a sufficient partition-free condition, obtained by taking 𝔅_n to be all
subsets of size at most 16. Under (E), assume δ_n√(p log log n) → 0 and TV on the actual blocks, as defined in FACA
STATEMENT §3. PTV is not additionally required for (E).
The strict exponent condition implies p = o(n), so K_n = p eventually and the full lattice is feasible. Under (R),
entrywise Gaussian correlation concentration gives ‖R̂ − Σ‖_op = O_P(p√(log n/n)); multiplication by √(p log log n) tends
to zero under this exponent condition, as in FACA L5.1. No separate p ≤ K_n assumption or upper bound on λ_max(Σ) is needed
[R01-5].
Conclusions: P(Sand_n([p])) → 1, P(NA(𝓛)) → 1 and P(TL(𝓛)) → 1 on the full lattice 𝓛 = [S₀, [p]], D_n → 0,
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and with the delivery premises P(Ŝ⁺ = S₀) → 1. [R05a-5] On Sand_n([p]) ∩ NA(𝓛) ∩ TL(𝓛) (an event
of probability tending to one), the prescribed deterministic LS0, viewed as uninterrupted on these data, reaches S₀ after
exactly |S̃₀ ∖ S₀| deletion moves, within the merged cap ℓ_n + |S̃₀|; a delivered SMC run executes that search, and the
exact-enumeration branch scores S₀ directly.
Containment [R01-2, R05a-1]: the structural class includes every FACA representation with bounded idiosyncratic blocks;
for its group partition, c_𝒢 = c_min and κ_UNI = κ_FACA, so the exponent is unchanged. UNI-1 contains the
fixed-positive-beta-min subclass of FAC-L, with the same structural representation, κ, exponent, and TV/TV-pop
qualifications. FAC-L's fixed-design BM-∞ relaxation (vanishing signals with nθ*²_min/log n → ∞) remains a separate
imported result. The extension beyond bounded idiosyncratic blocks is a new target requiring U-LOC.

**(iii′) k ≥ 2 and k = 1 beyond α₀ — strongest current statement + absorption plan.** Not claimed as theorems. The report
gives: (a) **Lemma OBS-k** [R01-7]: fix k ≥ 2 and a positive integer m independent of n. If p_n → ∞, the loading rows are
uniformly bounded, and Ψ_n ⪰ cI for fixed c > 0, then inf_{m≤|T|≤p_n} λ_min(Λ_TᵀΨ_TT⁻¹Λ_T)/|T| → 0. This obstructs an
extension requiring uniform positive information on every subset of size at least that fixed m. It does not obstruct
assumptions imposed only on sufficiently large subsets, other proofs for k ≥ 2, or consistency itself. (b) The
family-specific results beyond (iii) (FACB: exact CS, every p ≤ n/2) as clearly-marked partial versions. (c) A plan stating,
for each parallel ticket (FAC-S5/S5F, FAC-X/XA, FAC-K2, FAC-PK/PKA), which general hypothesis its result would discharge.

## 4. Reduction lemmas (new mathematics; each with falsification numerics and a cross-family check)

* **R1 Metric toolkit.** CT_M, CD_M, RB_M, TAIL_M and LOCL. [R01-4] All shell sums begin at m = 0, with shell counts
  bounded by C₀(m + 2)^{d₀}. For matrices with spectrum in [c, C], use Var(ζ_l | ζ_T) ≤ C, not ≤ 1, and hence
  (B⁻¹)_ll ≥ 1/C in the regression formula. Constants in RB_M, TAIL_M and LOCL may depend on C. Prove the bounds uniformly
  for principal submatrices and conditional covariances. In the correlation factor setting Ψ_jj ≤ 1 is available as an
  additional simplification.
  **LOCL:** establish constants B, t > 0 such that |β_T^Ψ(l)_v| ≤ B exp(−tδ(l, v)) uniformly in T, l, v, and a uniform ℓ¹
  regression bound L₀. For U = T ∩ B(l, r), V = T ∖ U, show β_U − β_{T,U} = Ψ_UU⁻¹Ψ_UVβ_{T,V}, whence
  ‖β_T − β̄_U‖₁ ≤ (1 + L₀′)‖β_{T,V}‖₁ ≤ ε(r), with ε(r) → 0 explicit (L₀′ the ℓ¹→ℓ¹ constant of Ψ_UU⁻¹Ψ_UV). Empty index
  sets have zero coefficient vectors.
* **R2 k = 0 engine inputs.** (A2, k = 0) + (A3) ⇒ the hypotheses of Theorem PLR: P(Sand_n) → 1 with Q of (ii)
  (selection removal, spherical tail, size ladder), (N0)–(N1), (R1)–(R3) of Lemma NA-R, TL inputs. (Delta to LOC2 L4 Part A
  with packing replaced by the growth function.)
* **R3 k = 1 engine inputs (key lemma U-LOC).** For Σ = λλᵀ + Ψ with Ψ ∈ 𝓛𝓞𝓒 and (A2-1):
  (a) exact Pythagorean decomposition of the add statistic along the residual factor direction for general Ψ (FACA U(a)
  with U replaced by T in ψ, λ̃, Ξ);
  (b) [R01-4] for U = T ∩ B(l, r_n), control the local standard normals (ζ_l − β_Uᵀζ_U)/√ψ_{l|U} over at most
  p·2^{C₀(1+r_n)^{d₀}} references. Use TAIL_M to compare ψ_{l|U}/ψ_{l|T} = 1 + o(1) uniformly, and use LOCL with coordinate
  atoms to bound |(β_T − β̄_U)ᵀζ| ≤ ε(r_n) max_j |ζ_j|. With r_n = ⌈(log log n)²⌉, log(reference count) ≤ log p + o(log n),
  max_j |ζ_j| = O_P(√(log p + log log n)), and the resulting uniform idiosyncratic envelope is √(2 log p) + o(√log n);
  (c) [R01-3] for G = |𝒢|, b = 2^{γ̄} − 1 and 1 ≤ h ≤ G, the number of nonempty T with h_𝒢(T) = h is at most C(G, h)b^h.
  Put x_h = log C(G, h) + h log b + 2 log(h + 1) + log log n + log 2. With probability at least 1 − 1/log n,
  simultaneously for all nonempty T, |F_T| ≤ √(2x_{h_𝒢(T)}), where F_T = λ_TᵀΨ_TT⁻¹ζ_T/√s_T is marginally N(0, 1).
  Therefore |λ_TᵀΨ_TT⁻¹ζ_T|/s_T ≤ √(2x_h/(c_𝒢h)). In particular this is at most c_𝒢^{−1/2}[√(2 log(eγ̄p/|T|)) +
  O(1 + √log log n)], uniformly over nonempty T. Constants depend only on γ̄. The empty set is handled separately using
  s_∅ = 0 and W_∅ = ξ₀;
  (d) transfer to (E)/(R) by FACA U(d); hence NA and TL on the full lattice for limsup log p/log n < α₀(κ̄); sandwich with
  Q = [p] from TV / TV-pop.
* **R4 Delivery** [R01-8]. For a deterministic Q ⊇ S₀, let 𝓛 = {T : S₀ ⊆ T ⊆ Q} ⊆ Ω. Assume
  P(Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛)) → 1 and E[1 − π(S₀)] → 0. Under the exact start-mode, complete-scan LS0, cap,
  input-validity, machine and allocation premises of FACA L7, the deterministic LS0 scores S₀ with probability tending to
  one and the delivered reported model satisfies P(Ŝ⁺ = S₀) → 1. Derive this through the LS0-scoring event, not from
  D_n → 0 alone. Check input validity separately in each design setting.
* **R5 Lemma OBS-k** (iii′)(a).

## 5. Corollary table [R01-6] (exact checks in `lemmas/C_corollaries.md`)

| Existing result and source status | Relation to UNI | Exact qualifications |
|---|---|---|
| APP POST (inside APP PROVED-CHECKED) | UNI-P under (R) | Exact LSF cutoffs, fixed signal bounds; fixed exact Grams use POST(c). |
| APP LOC; GROW AR(1); GEN study S1/S3/S4/S6 (source reports PROVED-CHECKED) | UNI-0 for the specified random-design instances | Ordering/block pseudometric and fixed spectral bounds; retain the source's PTV or verify it. For study bounded-block layouts, verify at most one truth per independent group, giving PTV(cθ_lo). This does not import every masked-truth theorem of GEN. |
| LOC2 LOC-d (PROVED-CHECKED) | UNI-0 | Separated Euclidean sites give polynomial growth; source spectrum and PTV assumptions retained. |
| LOC2 LOC-BF (PROVED-CHECKED) | Additional PLR instance | Uses the reference/atom construction of LOC2 L4 Part B; no membership of growing groups in fixed-constant LOC_M is asserted. |
| LOC2 polynomial decay α > 17/2 (PROVED-CHECKED) | Separate extension of the engine | Uses LOC2 L6's polynomial-size re-run of the toolkit, NA and assembly; not Theorem PLR directly, whose relevance sets are polylogarithmic. |
| FACA FAC-L (PROVED-CHECKED) | UNI-1 for its fixed-positive-beta-min subclass [R05a-1] | Bounded idiosyncratic blocks give LOC_M, c_𝒢 = c_min and κ_UNI = κ_FACA; retain AG, growth, and actual-block TV or covering-family TV-pop. S5 inherits its certified family of unions of whole groups. FAC-L's fixed-design BM-∞ relaxation (vanishing signals) is a separate imported result, not an instance of UNI-1. |
| FACB FAC-CS (PROVED-CHECKED) | Overlapping special case below 1/6, otherwise separate | Fixed exact-Gram CS, including column signs, with FACB's signal and method assumptions and p ≤ n/2. The actual-block-TV subclass below 1/6 is an instance of UNI-1(E). Masked truths under FS′ remain a separate result; they are not instances of a visibility theorem even below 1/6. |
| APP ENUM (inside APP PROVED-CHECKED) | Separate enumeration override | Require the coded EXB inequality eventually, EX-A, and posterior consistency. LSF alone does not activate enumeration. It gives output-intersected selection consistency, not an independent delivery theorem. |

## 6. Not claimed
Non-Gaussian rows; growing s₀; θ_lo → 0 for the reported model; visibility failures (masking) except where a cited family
result covers them (PXN, FACB (FS′)); k ≥ 2; k = 1 with limsup log p/log n ≥ α₀(κ̄) in general; [R01-5] representations
with c_{𝒢,n} = 0 or without a uniform bound on κ_n (vanishing common loading scale is not itself excluded when c_{𝒢,n} > 0
and κ_n stays bounded); Ψ outside LOC_M, e.g. with only polynomial decay or super-polynomial growth [R05b-4] (polynomial
decay on a line: LOC2 L6, α > 17/2); fixed-domain (infill) asymptotics; p > K_n in (iii); approximate fixed Grams for (i).
