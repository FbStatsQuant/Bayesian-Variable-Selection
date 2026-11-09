# C-MIS — STATEMENT (target statement)

Ticket C-MIS, Theory Wave 1C. Lead: Claude Opus 5.5.
Status of this file: **v1.2** — v1.1 LOCKED (2026-11-08 ~21:58 CST) after statement-lock review R01 (Codex gpt-6.1-sol
high, LOCK-WITH-CHANGES, seven required changes, all applied; `reviews/R01_statement_lock_sol.md`, disposition
`reviews/R01_disposition.md`); v1.2 = v1.1 plus the wording/scope corrections and additions required by R02–R08 (Lemma T /
Cor F(b), Lemma Z, Examples E1–E3, Corollary N, centring qualification of the SL identification, 𝓜 notation), each logged
in LOG.md and in the review dispositions. No hypothesis of a locked claim was weakened; additions are flagged in REPORT.md.

Abbreviations. SoP = `Theory_work/State_of_Project/sections/`; NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`;
T03R = `NBH/branch_snapshots/A-REV5/sources/W1-T03R/PROOF.md` (the T03♯ proof); [P3] =
`Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex`; [P1] = `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`;
GEN = `Theory_work/Wave1/W1-GEN/`; SL = Song & Liang (2015), JRSS-B 77(5), §2.3 (printed p. 957): Theorem 4, Corollary 2, eq. (19).

## 0. Target and relation to Song–Liang

**What SL prove (§2.3, p. 957).** Within SL's full Gaussian linear model (iid random design, no intercept), for a candidate
subset s of fixed size satisfying their Condition 4, under their normal/inverse-gamma parameter-prior setting and with a
model prior positive on every model of s: **Theorem 4** — posterior consistency of the *densities* around the KL minimiser f₀ within the
candidate class (eq. (18), a.s.); **Corollary 2** — if x_s has no exact multicollinearity, π(s̃ ⊂ ξ | D_n^s) → 1 in
probability, where s̃ = supp β₀, β₀ := argmin E(β_sᵀx_s − β*ᵀx)² (their projection; eq. (19) writes it as Σ_s⁻¹cov(x_s, y),
which agrees with the minimiser for centred predictors): **support inclusion (screening)**, not concentration
on the single model s̃.

**What this ticket targets.** A *stronger, method-specific* conclusion under *stronger* hypotheses: exact-model
concentration π_𝒞(S₀^𝒞 | y) → 1 with rate O_P(√(log n/n)) for the shipped prior, with p_𝒞 ≤ n^A:
* **Theorem MIS (main).** Under a Gaussian-residual condition (GR) on the omitted contribution, the candidate-only problem
  is *exactly* a well-specified Gaussian linear model with truth β^𝒞 and noise σ² + τ²; T03♯ (TH09) transfers.
  For jointly Gaussian rows β^𝒞 is the population regression slope *with an intercept*, Σ_𝒞𝒞⁻¹cov(x_𝒞, y); after
  population centring (m = 0) it equals SL's β₀ and S₀^𝒞 = SL's s̃ (for non-centred predictors without an intercept SL's
  minimiser uses second moments and can differ — sweep R06 item 1). The no-beta-min inclusion clause is the counterpart of
  SL's Corollary 2. No density-contraction analog of SL's Theorem 4 is claimed.
* **Theorem F (separate fixed-design target).** Under exact sparse projection (EP) of the full mean on the candidate span,
  T03♯'s proof is re-run with explicitly changed steps; the size-tail step is replaced by a hypothesis TAIL^𝒞, discharged
  for bounded p_𝒞 (Corollary F(a)) and under a large-omitted-residual condition (Corollary F(b), Lemma T).

## 1. Setting

* **D0 (method).** The method is **re-run on the candidate data** (X^r_𝒞, y^r) only — not obtained by conditioning the
  full-p posterior on S ⊆ 𝒞. It standardises the candidate columns and y and uses the shipped g = n ridge score m(S),
  IG(a₀, b₀), a₀ = b₀ = 0.01, ν = a₀ + n/2, BB(1, p_𝒞) size weights w(k) = ½/C(2p_𝒞 − 1, k), p_𝒞 := |𝒞|, cap
  K = min(p_𝒞, ⌊n/2⌋), Ω_𝒞 = {S ⊆ 𝒞 : |S| ≤ K} (SoP `02_method.tex:84-106`). π_𝒞(· | y) is the exact posterior on Ω_𝒞;
  S†_𝒞, MPM_𝒞, PIP_j as in `Docs/Theory/theorems/00_COMMON.md` §1 with [p] replaced by 𝒞. **Valid inputs:** candidate
  columns and y^r non-constant (`00_COMMON.md:9`); y^r is non-constant a.s. under every model below; non-constant
  candidate columns are assumed for fixed designs, hold a.s. under jointly Gaussian rows, and are part of 𝒜_n in MIS (ii).
* **True model.** X^r = [X^r_𝒞, X^r_𝓜] (𝓜 = omitted ("missing") columns; the symbol 𝒪 is reserved for M5's
  output-available event); y^r = α1 + X^r_𝒞β_𝒞 + ω + ε, ω := X^r_𝓜β_𝓜;
  **ε ~ N_n(0, σ²I_n) independent of X^r_𝒞** (in the random-design statements: conditionally on X^r_𝒞,
  ε ~ N_n(0, σ²I)), σ² > 0 fixed. S₀ := supp β. Misspecification: S₀ ⊄ 𝒞.
* X_𝒞 = CX^r_𝒞D_x⁻¹ (D_x = candidate raw sample SDs); N := n − 1; r_n := √(log n/n); U (n × N), UᵀU = I, UUᵀ = C.

## 2. Theorem MIS (Gaussian-residual omitted part)

**(GR).** Conditionally on X^r_𝒞 (for a fixed candidate design: unconditionally), ω = a1 + X^r_𝒞γ + ξ with
ξ ~ N_n(0, τ²I_n), (a, γ) measurable functions of X^r_𝒞, τ² ≥ 0 fixed; conditionally on X^r_𝒞, ξ and ε are independent
and ε ~ N_n(0, σ²I). The method's uniforms are independent of (X^r, ε, ξ).
**Definitions.** β^𝒞 := β_𝒞 + γ; **S₀^𝒞 := supp β^𝒞**; s₀^𝒞 := |S₀^𝒞|; σ_𝒞² := σ² + τ²; θ^𝒞 := D_xβ^𝒞; μ^𝒞 := X_𝒞θ^𝒞.
Then y^r = (α + a)1 + X^r_𝒞β^𝒞 + ε′, ε′ := ε + ξ, and ε′ | X^r_𝒞 ~ N_n(0, σ_𝒞²I) (so ε′ is independent of X^r_𝒞).
**(H-MIS)** = the T03♯ hypotheses (SoP `04_theory.tex:774-782`) for the candidate problem, i.e. with
(p, S₀, s₀, θ*, μ, σ*²) := (p_𝒞, S₀^𝒞, s₀^𝒞, θ^𝒞, μ^𝒞, σ_𝒞²), eigenvalue conditions on subsets of 𝒞, and in particular
**s₀^𝒞 ≥ 1 fixed** (the empty-support case is excluded; not claimed), p_𝒞 ≤ n^A, ‖μ^𝒞‖² ≤ Mn, λ_min(R̂_{S₀^𝒞}) ≥ φ₀²,
SE_λ(j₀), SE_w(m♯_n; g₀), and BM-∞ or BM(c > c₀) **with σ_𝒞²**.

**Theorem MIS.**
(i) *Fixed candidate design.* For a deterministic array (X^r_𝒞)_n with GR and (H-MIS): 1 − π_𝒞(S₀^𝒞 | y) = O_P(r_n);
  max_j|PIP_j − 1{j ∈ S₀^𝒞}| ≤ 1 − π_𝒞(S₀^𝒞 | y) (every data set, s₀^𝒞 ≤ K); P(MPM_𝒞 ≠ S₀^𝒞) → 0;
  P(S†_𝒞 ≠ S₀^𝒞) ≤ 2E[1 − π_𝒞(S₀^𝒞 | y)] → 0 (no expectation rate is claimed); without beta-min, for fixed c > c₀,
  π_𝒞(S ⊉ J_n^𝒞(c) | y) = O_P(r_n), J_n^𝒞(c) := {j ∈ S₀^𝒞 : θ^𝒞_j² ≥ cσ_𝒞² log n/(nφ₀²)}.
  Consequences: a candidate j ∈ S₀^𝒞 ∖ S₀ (null in the full model, carrying omitted signal) has PIP_j → 1; a true
  candidate with β_j + γ_j = 0 (cancellation) has PIP_j → 0. **Corollary N (L1):** every T ≠ S₀^𝒞 has
  π_𝒞(T | y) ≤ 1 − π_𝒞(S₀^𝒞 | y); in particular π_𝒞(S₀ ∩ 𝒞 | y) → 0 when S₀ ∩ 𝒞 ≠ S₀^𝒞, and the (a.s. dense when
  τ² > 0 and the centred candidate matrix has full column rank) sample-projection support gets vanishing mass.
(ii) *Random candidate design, envelope form.* X^r_𝒞 random, GR conditionally, fixed constants (A, s, M, φ₀, g₀, σ_𝒞²)
  and a fixed c > c₀ or a deterministic M_n → ∞, and measurable sets 𝒜_n with P(X^r_𝒞 ∈ 𝒜_n) → 1 such that every
  x ∈ 𝒜_n satisfies, at that n, the finite-n inequalities of (H-MIS) with these constants, s₀^𝒞(x) = s ≥ 1, and
  BM(c) (resp. θ^𝒞_min(x)²nφ₀²/(σ_𝒞² log n) ≥ M_n). Then every deterministic sequence x_n ∈ 𝒜_n is a T03♯ array,
  and the conclusions of (i) hold under the joint law (diagonal argument for tightness, Lemma DR). (ii′): dropping the
  beta-min requirement from 𝒜_n, the inclusion clause π_𝒞(S ⊉ J_n^𝒞(c) | y) = O_P(r_n) holds under the joint law.
(iii) *Jointly Gaussian rows.* Convention: 𝓜 := S₀ ∖ 𝒞 (the **active** omitted columns; inactive omitted columns are
  marginalised out, which can create precision-graph edges — R04 finding 1). Rows (x^r_{𝒞,i}, x^r_{𝓜,i}) iid N(m, Σ)
  (m, Σ may depend on n), Σ_𝒞𝒞 ≻ 0, independent of ε. Then **at each n** the GR decomposition holds with
  γ = Σ_𝒞𝒞⁻¹Σ_𝒞𝓜β_𝓜, a = m_𝓜ᵀβ_𝓜 − m_𝒞ᵀγ, τ² = β_𝓜ᵀ(Σ_𝓜𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁻¹Σ_𝒞𝓜)β_𝓜; β^𝒞 = Σ_𝒞𝒞⁻¹cov(x_𝒞, y) (slope with an
  intercept); for centred rows (m = 0) this is SL's β₀ and S₀^𝒞 = SL's s̃ (Proposition P(a)–(b)). **GR as used by Theorem MIS additionally requires τ_n² ≡ τ² fixed in n**
  (Gaussianity alone gives a possibly n-dependent τ_n²; e.g. an independent omitted column of variance n² gives
  τ_n² = n²); MIS (i)–(ii) is applied only under this fixed-variance requirement. If Σ ≻ 0, Θ = Σ⁻¹: γ = −Θ_𝒞𝓜Θ_𝓜𝓜⁻¹β_𝓜, τ² = β_𝓜ᵀΘ_𝓜𝓜⁻¹β_𝓜 (P(c)).
  **One active omitted variable k (β_k ≠ 0), Θ the precision of the marginal vector (x_𝒞, x_k):** γ_j = −β_kΘ_jk/Θ_kk, so a candidate j that is null in the full model is
  in S₀^𝒞 iff Θ_jk ≠ 0 (nonzero partial correlation with x_k given the other candidates), whatever its marginal
  correlation; a true candidate j leaves S₀^𝒞 iff β_j = β_kΘ_jk/Θ_kk (cancellation) (P(d)). With several omitted
  variables, contributions can cancel; only supp γ ⊆ {j : Θ_jk ≠ 0 for some k ∈ 𝓜} is claimed. Membership in S₀^𝒞 gives
  selection only together with (H-MIS), in particular beta-min.
  **Design hypotheses with probability → 1 (Lemma GD).** (a) p_𝒞 fixed, m, Σ, β fixed in n, Σ_𝒞𝒞 ≻ 0, β^𝒞 ≠ 0: (ii)
  applies; here J_n^𝒞(c) = S₀^𝒞 eventually, so the inclusion clause recovers, in the jointly Gaussian special case,
  SL's Corollary 2 conclusion (π(S₀^𝒞 ⊆ S) → 1; S₀^𝒞 = s̃ for m = 0, its intercept-adjusted analogue otherwise) — in general triangular arrays the no-beta-min clause screens only J_n^𝒞(c). (b) *(optional, conditional)* growing p_𝒞 ≤ n^A under stated population restricted-eigenvalue, variance,
  projected-energy and projected beta-min assumptions; projection sparsity (fixed s) is **assumed**, never inferred from
  Gaussianity (one omitted variable can have a growing number of graph neighbours, e.g. a one-factor design).

**Example E1 (analytic target separation; L2).** x₁, x₂, x₃, z iid N(0,1), 𝒞 = {1,2,3}, omitted x_k = −x₁ + x₂ + z,
y = x₁ + x_k + ε. Full truth {1, k}; S₀ ∩ 𝒞 = {1}; β^𝒞 = (0,1,0), S₀^𝒞 = {2}; σ_𝒞² = σ² + 1. By GD(a), π_𝒞({2} | y) → 1:
candidate 2 is a proxy, the true candidate 1 is cancelled, and both π_𝒞({1} | y) and the posterior mass of the
(almost surely dense) sample-projection support {1,2,3} tend to 0.
**Null projection (Lemma Z, L6).** If s₀^𝒞 = 0 (β^𝒞 = β_𝒞 + γ = 0: the candidate coefficients and the projected omitted
contribution cancel coordinatewise, so the aggregate candidate regression slope vanishes; this may result from cancellation and does
not require independence of individual omitted predictors; under EP:
P_𝒞μ_c = 0) and p_𝒞 is bounded with λ_min(X_𝒞ᵀX_𝒞) ≥ g₀ eventually: 1 − π_𝒞(∅ | y) = O_P(n^{−1/2})
(fixed design under GR; also under EP with θ^𝒞 = 0). The general growing-p null case is not claimed.

## 3. Reported HPM (M5(0)) and the never-scored term

**Corollary H.** At every n, for any candidate design and any law of the data supported on valid inputs, for any
T ∈ Ω_𝒞 (deterministic or a measurable function of the candidate design), with D_n(T) := P(𝒪̄ ∩ {T ∉ 𝒮̄⁺}) (potential-run
notation and premises of M5(0)): P(𝒪 ∩ {Ŝ⁺ ≠ T}) ≤ 2E[1 − π_𝒞(T | y)] + D_n(T). With T = S₀^𝒞, D_n^𝒞 := D_n(S₀^𝒞), the
first term → 0 under Theorem MIS or Theorem F. (Input: T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))".)
No discovery or delivery claim.
**Corollary D.** Under GR with a fixed candidate design, method v3.1 + LS0 with GEN's premises (LS0 as specified; not in
production code — GEN REPORT flag 4), and GEN's (H0)–(H2)
(GEN `STATEMENT.md` v2.3 §2; (H0) includes **BM-∞**) — or (H0), (H2) with S* = S₀^𝒞 — for the candidate problem with
σ² := σ_𝒞² **everywhere in GEN** (v_T, leakage exponents, NL, VIS, BM) and μ := μ^𝒞 (so GEN's Δ_T is the residual energy
of μ^𝒞; τ² is not added again), on the actual candidate-only partition: D_n^𝒞 → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀^𝒞}) → 0, and
liminf P(𝒪 ∩ {Ŝ⁺ = S₀^𝒞}) = 1 − limsup P(U_n). Random candidate designs: GEN (C4) with all GEN envelope conditions and
measurable candidate coefficients/certificates. **Optional:** an explicit proxy instance on GEN's W family (Corollary D′).

## 4. Theorem F (fixed design, exact sparse projection)

Everything deterministic except ε. **Coordinates:** contrast coordinates throughout: μ_c := UᵀX^rβ (full mean),
X_{c,𝒞} := UᵀX_𝒞, e := Uᵀε ~ N_N(0, σ²I), y_c = μ_c + e.
**(EP).** There are S₀^𝒞 ⊆ 𝒞 and θ^𝒞 with supp θ^𝒞 = S₀^𝒞 such that r := μ_c − X_{c,𝒞}θ^𝒞 satisfies X_{c,𝒞}ᵀr = 0.
(The projected mean P_𝒞μ_c = X_{c,𝒞}θ^𝒞 is the fixed-design least-squares/KL mean target; S₀^𝒞 is its sparse
coefficient support, distinguished by the hypotheses below, not by KL alone: SE_λ(j₀) makes θ^𝒞 the unique
representation of P_𝒞μ_c among coefficient vectors with support T, |T ∖ S₀^𝒞| ≤ j₀.) Δ_n := ‖r‖²/N, σ²_{𝒞,n} := σ² + Δ_n ∈ [σ², σ² + 2M].
**Hypotheses.** s₀^𝒞 ≥ 1 fixed, p_𝒞 ≤ n^A, s₀^𝒞 ≤ K eventually; G; R^𝒞: ‖μ_c‖² ≤ Mn, λ_min(R̂_{S₀^𝒞}) ≥ φ₀²;
SE_λ(j₀) and SE_w(m_n; g₀) anchored at S₀^𝒞 on subsets of 𝒞, for a deterministic cutoff m_n with
s₀^𝒞 ≤ m_n ≤ min(K, C log n) (default m_n = m♯_n); BM^𝒞: BM-∞ (θ^𝒞²_min nφ₀²/log n → ∞) or BM(c), c > c₀, with
σ²_{𝒞,n}: θ^𝒞²_min ≥ cσ²_{𝒞,n} log n/(nφ₀²); **TAIL^𝒞(m_n):** π_𝒞(|S| > m_n | y) = O_P(r_n).
**Theorem F.** Then 1 − π_𝒞(S₀^𝒞 | y) = O_P(r_n), and the deterministic consequences hold for S₀^𝒞
(max_j|PIP_j − 1{j ∈ S₀^𝒞}| ≤ 1 − π_𝒞(S₀^𝒞 | y); P(MPM_𝒞 ≠ S₀^𝒞) → 0; P(S†_𝒞 ≠ S₀^𝒞) ≤ 2E[1 − π_𝒞(S₀^𝒞 | y)] → 0 —
T03R conclusions (ii)–(iii)); without beta-min
(keeping TAIL^𝒞), π_𝒞(S ⊉ J_n^{𝒞,F}(c) | y) = O_P(r_n) with J_n^{𝒞,F}(c) := {j ∈ S₀^𝒞 : θ^𝒞_j² ≥ cσ²_{𝒞,n} log n/(nφ₀²)}.
**Corollary F(a).** p_𝒞 bounded ⇒ m♯_n = K eventually ⇒ TAIL^𝒞(m♯_n) holds; F holds without TAIL^𝒞.
**Corollary F(b)** (added in v1.1). If d_n := rank X_{c,𝒞} and, for a fixed κ ∈ (0,1),
(TL) σ²/(Δ_n + σ²(1 − d_n/N)) ≤ (3/4)(1 − κ) eventually, then TAIL^𝒞 holds at m^T_n := s₀^𝒞 + ⌈C_{κ,s,A} log n⌉
(Lemma T, no eigenvalue condition beyond S₀^𝒞), so F holds with m_n := min(K, max(m♯_n, m^T_n)) without TAIL^𝒞.
**Changed steps** (lemmas/L4): new event (G5) on rᵀe; lem:ongood(b) with δ_n^𝒞 := δ_n + 2 log n/N, propagated through
(C4)'s υ_n, (C5)'s ε_n and q_n, and (C8); lem:ongood(c) with E_n^𝒞 := 2b + ‖r + e‖² + (2/(n+1))‖y_c‖²
≤ Nσ²_{𝒞,n}(1 + δ''^𝒞_n); lem:SvsSp second inequality and lem:signalgain with σ²_{𝒞,n}; lem:signal / Δ_S with μ^𝒞
(not μ_c); [P3]'s P_{S′}μ = μ step replaced by (P_{S′} − P_S)r = 0; Step 0 → TAIL^𝒞. The actual response-dependent IG
rate b = b₀‖y_c‖²/N is kept (it is common to all models); no raw-likelihood substitution.

## 5. Frontier (characterised; claims only where proved)
* **Unrestricted span vs capped feasibility.** If rank X_{c,𝒞} = N then r = 0 for every μ_c (no residual outside the
  unrestricted candidate span) — but μ_c may still have no feasible (|S| ≤ K) or sparse representation; p_𝒞 ≥ n alone
  does not imply full rank. So for full-rank candidate designs "misspecification" is a question of sparse/capped
  representability, outside T03♯.
* **Why T02(i♯) does not port.** The numerator identity E_true[m^c_b(S)/f_true] = 1 survives misspecification (any fixed
  rate b, any positive true density); what fails is the denominator lower bound (Lemma den′), proved for the pure-noise
  residual. For the full contrast experiment, the candidate densities can inflate their scalar variance to ≈ σ² + Δ_n but cannot represent the
  orthogonal mean r, which costs a likelihood/KL loss of order N:
  log[m^c_b(S)/f₀] ≤ −(N/2)log(1 + Δ_n/σ²)(1 + o_P(1)) uniformly in S ⊆ 𝒞 when Δ_n ≥ Δ₀ > 0 and d_n/N → 0 (Lemma O2).
  This is an obstruction to that denominator strategy only, not a failure of posterior consistency. Reduced-experiment
  variants (loss ≍ d_n[log(v/σ²) + σ²/v − 1]/2 in the candidate span) are conjectural.
* **Random-design EP.** Random-design versions of Theorem F / Lemma T / Lemma Z are not claimed; the Lemma DR route would
  need EP and (TL) on design envelopes.
* **Open window.** EP with growing p_𝒞 and 0 < Δ_n < σ²(1/3 + d_n/N) (roughly): TAIL^𝒞 not proved.
* **Outside GR:** nothing is claimed here (numerics N5 exploratory only). Within SL's full Gaussian linear model, for a
  fixed candidate set satisfying Condition 4 and their stated normal/inverse-gamma prior setting, their Theorem 4 gives
  density consistency; with their additional no-exact-multicollinearity condition, Corollary 2 gives inclusion. Some
  non-Gaussian or heteroscedastic omitted contributions induced by random omitted predictors fall within that setting.
  Example E2 (L5 §6) shows that Gaussian marginals of the omitted part do not suffice for our transfer.

## 6. Statuses
Targets until checked. Cited inputs keep verbatim statuses: T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)";
T01–T03 "PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY"; T38-(0) as above; Theorem GEN "PROVED-CHECKED"
(Wave 1) with its premises (e4; N3 "OPEN" as a general invariant). All convergence claims are asymptotic, with thresholds
depending on the stated constants and envelope/onset sequences. TH09's approximately two-million illustration
(SoP `04_theory.tex:811`) is not a universal threshold and is not transferred to the new results.
