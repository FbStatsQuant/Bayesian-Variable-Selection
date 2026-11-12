# W3-MISR — STATEMENT (v1.0, 2026-11-11; lead: Claude Fable 5.2, claudeAgent, high)

Ticket W3-MISR (T1 of `Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md`): C-MIS v2, the misspecified-subset theorem
without fixed variances. Status of this file: **v1.0, targets — nothing below is proved or checked yet**. Each claim
gets its own status in its proof file (`lemmas/`). Inherited statuses are quoted verbatim in §8.

**Aliases.** [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md` (v1.4); [POST2] = `Theory_work/Wave3/W3-POST2/STATEMENT.md`
(v1.2.1) with its proof files `Theory_work/Wave3/W3-POST2/lemmas/{A_occam,C_expectation,D_hellinger,E_visibility}.md`;
[MIS1] = `Theory_work/Wave1C/C-MIS/STATEMENT.md` (v1.2) with `Theory_work/Wave1C/C-MIS/lemmas/{L1_reduction,L2_gaussian}.md`;
SL = Song & Liang (2015), JRSS-B 77(5), §2.3, Theorem 4 and Corollary 2 (as described in [MIS1] §0).
Code = `Scripts/SMC_BVS/core/` at commit 16a7f85 (last change to that folder: 72785fe).

## 0. Setting and notation

* **Method on the candidates (D0, as [MIS1] §1).** 𝒞 is the candidate set. The method is re-run on (x, y^r), where x is
  the n × p raw candidate design (n ≥ 3) and y^r the raw response; constant columns are dropped by the code, so
  throughout x has p ≥ 1 non-constant columns. π_𝒞(· | x, y^r) is the coded target of [W3P] §0 (lines 16-29) computed
  from (x, y^r): X = CxD_x⁻¹ (standardised columns, D_x the raw sample SDs), y = Cy^r/s_y, Ω = {S ⊆ [p] : |S| ≤ K},
  K = min(p, ⌊n/2⌋), prior w(k) = ½/C(2p − 1, k), score m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν}. It is defined when y^r is
  non-constant. PIP_j, HPM (any tie rule), MPM, ξ_q are the exact-posterior outputs of [W3P] §0. All statements are
  about this real-arithmetic target, not about the sampler or floating point.
* **Contrasts.** N := n − 1; U is n × N with UᵀU = I_N, UUᵀ = C (centring); r_n := √(log n/n).
* **Configuration.** κ = (x, β, v): x as above, β ∈ ℝ^p, v ∈ (0, ∞). Derived objects: S₀(κ) := supp β,
  s(κ) := |S₀(κ)|, θ(κ) := D_xβ, μ(κ) := Cxβ = Xθ(κ), μ_c := Uᵀμ(κ); for S ⊆ [p], M_S and
  L_S(κ) := μ_cᵀ(I − M_S)μ_c as in [POST2] (lines 17, 40-41); j₀ := ⌈(2A + 1)s⌉ + 1; m♯_n as in [W3P] (lines 36-39)
  with (p, s₀) := (p, s); 𝔉(κ) := {S ∈ Ω : S₀(κ) ⊄ S, |S∖S₀(κ)| ≤ j₀}.
* **(GR^c) contrast-law Gaussian residual.** A law of y^r (x fixed) satisfies GR^c at κ = (x, β, v) if
    Uᵀ(y^r − xβ) ~ N_N(0, v·I_N).
  Nothing else is assumed about y^r: the intercept may be random and dependent on everything, and no decomposition of
  the residual into "noise" and "omitted part" is needed. [MIS1]'s GR (line 54-58) implies GR^c with β = β^𝒞 = β_𝒞 + γ
  and v = σ² + τ², for any σ², τ² ≥ 0 with σ² + τ² > 0. β need not be unique when the centred design has deficient
  column rank; every statement is about a chosen representation satisfying the stated hypotheses.
  Under GR^c, y^r is non-constant almost surely.

**Hypotheses at a given n, in signal-to-noise form** (constants A ≥ 1, M ≥ 0, 0 < φ₀ ≤ 1, C_OS < ∞, c):
- **(SZ)** 2 ≤ p ≤ n^A and 1 ≤ s(κ) ≤ K.
- **(E^σ; M)** ‖μ(κ)‖² ≤ n·M·v.
- **(F₀; φ₀)** λ_min(X_{S₀}ᵀX_{S₀}/(n − 1)) ≥ φ₀², S₀ = S₀(κ).
- **(OS; C_OS)** the superset Occam-sum condition of [POST2] (lines 29-36) at this n, anchored at S₀(κ). (Design-only.
  Implied by (F_w; g₀), (DG), (ADG): [POST2] line 46.)
- **(ID^{M,σ}; c)** L_S(κ) ≥ c·v·log n for every S ∈ 𝔉(κ). Coordinate form **(ID^{M,σ}_j; c)**, j ∈ S₀(κ): the same
  for every S ∈ 𝔉(κ) with j ∉ S.
- **(F_λ; φ₀)** of [W3P] (lines 68-70) anchored at S₀(κ); **(BM^σ; c)** min_{j∈S₀(κ)} θ_j(κ)² ≥ c·v·log n/(nφ₀²).

These are exactly the hypotheses (E), (F₀), (OS), (ID^M; c), (F_λ), BM(c) of [POST2]/[W3P] for the **unit-noise
model**: design x, coefficient β/√v, σ*² = 1, energy constant M. (OS), (F₀), (F_λ) do not involve (β, v) beyond S₀(κ).

**Classes.** For s ≥ 1: 𝒦⁰_n(s, A, M, φ₀, C_OS) := {κ : s(κ) = s, (SZ), (E^σ; M), (F₀; φ₀), (OS; C_OS)};
𝒦_n(s, A, M, φ₀, C_OS, c) := 𝒦⁰_n ∩ {(ID^{M,σ}; c)}; 𝒦^λ_n(s, A, M, φ₀, C_OS, c) := 𝒦⁰_n ∩ {(F_λ; φ₀), (BM^σ; c)}.
**Constants.** c₁(s, A) as in [POST2] line 130; c₀(s, A) as in [W3P] lines 74-75 (it depends on (s, A) only). "The
constants of [POST2] Claim C at σ*² = 1" means its (n₀, C) for (s₀, A, σ*², M, φ₀, c, C_OS) = (s, A, 1, M, φ₀, c, C_OS).
**Laws.** For a configuration κ, P_κ denotes any law of y^r satisfying GR^c at κ, and E_κ its expectation. By Lemma
R′(b) the law of π_𝒞(· | x, y^r) is the same for all of them.

## 1. Lemma R′ (scale invariance; contrast-law reduction)

**(a) Invariance (deterministic).** For every x, every non-constant y^r, every a ∈ ℝ and c ≠ 0:
  π_𝒞(· | x, a1 + c·y^r) = π_𝒞(· | x, y^r) on Ω,
hence the same for PIP, the set of posterior modes, MPM and ξ_q. (The standardised response changes only by the sign
of c, and the score depends on it through yᵀy and z_SᵀH_S⁻¹z_S. The locked T03 statement, conclusion (v), records only
that the beta-min inequalities are unchanged by a rescaling; (a) is the invariance of the posterior itself.)
**(a′) Equivariance of the parameter posterior.** Let Π(· | x, y^r) be the joint posterior of (S, θ_S, v) on the
original response scale of [POST2] Claim D (lines 101-103: the working posterior of (S, β_S, σ²) mapped by
(θ, v) = (s_yβ, s_y²σ²)). For c > 0, a ∈ ℝ: Π(· | x, a1 + c·y^r) is the image of Π(· | x, y^r) under (S, θ, v) ↦ (S, cθ, c²v).
**(a″) Code path.** In the code the scorer receives only the standardised response, and the IG rate b₀ = 0.01 is a
constant on that scale; the raw scale s_y is stored for reporting and enters no score: `v3_preprocess.R:37-68`
(`v3_standardise`: centre, divide by the sample SD), `:123-127` (`y = sy$z`; `s_y` stored), `v3_fit.R:97, 118`
(`pre <- v3_preprocess(X, y)`; `v3_context(pre$X, pre$y, …)`), `cpp/v3_score.h:14` (`b0 = 0.01`), `:55-60`
(`z = Xᵀy`, `yty`, `logm0` from the standardised y), `:217-223` (`Q = yty − n·quad`, `logm = logCn − ½(ldH − ldA) − ν log(2b0 + Q)`).
So the code's target is the invariant π_𝒞 of (a); in floating point the outputs agree up to rounding (numerics N0).
**(b) Reduction.** Let x be fixed and let the law of y^r satisfy GR^c at κ = (x, β, v). Then the law of
π_𝒞(· | x, y^r) (a random probability on Ω) equals its law under the **unit-noise G-model** ỹ = xβ/√v + ε̃,
ε̃ ~ N_n(0, I_n); in that model S₀ = S₀(κ), θ* = θ(κ)/√v, μ = μ(κ)/√v. The same holds for the law of the image of
Π(· | x, y^r) under (S, θ, v′) ↦ (S, θ/√v, v′/v).

## 2. Theorem MIS-R (i): fixed candidate design, uniform expectation rate

Fix s ≥ 1, A ≥ 1, M, φ₀, C_OS and c > c₁(s, A). Let (n₀, C) be the constants of [POST2] Claim C (case iii) at σ*² = 1.
Then for every n ≥ n₀:
  **sup_{κ ∈ 𝒦_n(s, A, M, φ₀, C_OS, c)} E_κ[1 − π_𝒞(S₀(κ) | x, y^r)] ≤ C·r_n.**
The same holds on 𝒦^λ_n(s, A, M, φ₀, C_OS, c) for c > c₀(s, A), with the constants of case (ii).
The constants do not depend on v: the residual variance may be any positive number at each n (fixed, → 0, → ∞).
Consequences, for the same n and κ, with δ := 1 − π_𝒞(S₀(κ) | x, y^r):
1. max_j |PIP_j − 1{j ∈ S₀(κ)}| ≤ δ and sup_{T ≠ S₀(κ)} π_𝒞(T) ≤ δ for every data set; so both have E_κ ≤ C r_n.
2. P_κ(HPM ≠ S₀(κ)) ≤ 2C r_n; P_κ(MPM ≠ S₀(κ)) ≤ 2C r_n; P_κ(ξ_q ≠ S₀(κ)) ≤ C r_n/min(q, 1 − q) for q ∈ (0, 1).
3. (Proxies and cancellations, as [MIS1] lines 69-72.) Under [MIS1]'s GR with β = β_𝒞 + γ: a candidate that is null
   in the full model but has γ_j ≠ 0 is in S₀(κ) and has E_κ(1 − PIP_j) ≤ C r_n; a true candidate with β_𝒞,j + γ_j = 0
   has E_κ PIP_j ≤ C r_n; if S₀^{full} ∩ 𝒞 ≠ S₀(κ) then E_κ π_𝒞(S₀^{full} ∩ 𝒞) ≤ C r_n.

## 3. Theorem MIS-R (i′): without the margin (same uniform form)

Fix s ≥ 1, A ≥ 1, M, φ₀, C_OS and c > c₁(s, A). There are n₀′, C′ depending only on (s, A, M, φ₀, C_OS, c) such that
for every n ≥ n₀′ and every κ ∈ 𝒦⁰_n(s, A, M, φ₀, C_OS):
(a) **No strict-superset mass.** E_κ π_𝒞(S ⊋ S₀(κ)) ≤ C′ r_n.
(b) **Strong coordinates.** For every j ∈ S₀(κ) with (ID^{M,σ}_j; c): E_κ π_𝒞(S ∌ j) ≤ C′ r_n. Hence, with
    J^M_n(κ; c) := {j ∈ S₀(κ) : (ID^{M,σ}_j; c) holds}: E_κ π_𝒞(S ⊉ J^M_n(κ; c)) ≤ s·C′ r_n.
(c) **Beta-min form.** If also (F_λ; φ₀), then J^M_n(κ; c) ⊇ {j ∈ S₀(κ) : θ_j(κ)² ≥ c″·v·log n/(nφ₀²)} for every
    c″ ≥ c·n/(n − 1); so the right-hand set is included with the bound of (b). (This is the counterpart of SL's
    Corollary 2 and of [MIS1]'s inclusion clause, in expectation, relative to v.)

## 4. Theorem MIS-R (ii): random designs and design-dependent variance (conditional form)

Let (Ω*, 𝒢*, P) carry, at each n, a σ-field 𝓕_n ⊆ 𝒢*, an 𝓕_n-measurable **random configuration**
κ_n = (X^r_𝒞, β^𝒞, σ²_𝒞) (so the candidate coefficient and the residual variance may depend on the design and on
anything else in 𝓕_n), and a response y^r such that
  **(GR^c | 𝓕_n)** W_n := Uᵀ(y^r − X^r_𝒞β^𝒞)/σ_𝒞 is independent of 𝓕_n and W_n ~ N_N(0, I_N).
(Default: 𝓕_n = σ(X^r_𝒞); then β^𝒞 = β^𝒞(x), σ²_𝒞 = σ²_𝒞(x) are measurable functions of the design, and GR^c | 𝓕_n
says: given X^r_𝒞 = x, the contrast residual is N_N(0, σ²_𝒞(x) I). The residual may be heteroscedastic across designs.)
Write δ_n := 1 − π_𝒞(S₀(κ_n) | X^r_𝒞, y^r). With (n₀, C) as in §2 and (n₀′, C′) as in §3:
(a) **Conditional and uniform.** For n ≥ n₀: E[δ_n | 𝓕_n] ≤ C r_n almost surely on {κ_n ∈ 𝒦_n(s, A, M, φ₀, C_OS, c)}.
    Hence for any event 𝒜_n ∈ 𝓕_n contained in that event: E[δ_n 1_{𝒜_n}] ≤ C r_n P(𝒜_n) and
    E δ_n ≤ C r_n + P(𝒜_nᶜ); likewise P(HPM ≠ S₀(κ_n)) ≤ 2C r_n + P(𝒜_nᶜ), and the same for MPM, ξ_q, PIPs as in §2.
    The same with 𝒦^λ_n; and the bounds of §3 hold conditionally on {κ_n ∈ 𝒦⁰_n(…)} in the same way.
(b) **Slices in s.** If on 𝒜_n the size s(κ_n) takes values in {1, …, s̄} and κ_n ∈ 𝒦_n(s(κ_n), A, M, φ₀, C_OS, c)
    with c > max_{s ≤ s̄} c₁(s, A), then (a) holds with n₀ := max_{s≤s̄} n₀(s), C := max_{s≤s̄} C(s).
(c) **Tight constants.** Suppose that for every η > 0 there are constants (s̄, A, M, φ₀, C_OS, c)_η as in (b) and
    events 𝒜^η_n ∈ 𝓕_n as in (b) with limsup_n P((𝒜^η_n)ᶜ) ≤ η. Then δ_n = O_P(r_n) under P, and
    P(HPM ≠ S₀(κ_n)) → 0, P(MPM ≠ S₀(κ_n)) → 0, max_j|PIP_j − 1{j ∈ S₀(κ_n)}| = O_P(r_n).
    (Fixed constants with P(𝒜_n) → 1 — the form of [MIS1] (ii) — are the special case of one family for all η.)

## 5. Corollary G (example: jointly Gaussian rows; no fixed-variance requirement)

Rows (x^r_{𝒞,i}, x^r_{𝓜,i}), i ≤ n, iid N(m, Σ) with Σ_𝒞𝒞 ≻ 0, 𝓜 the omitted active columns; y^r = α1 + X^r_𝒞β_𝒞 +
X^r_𝓜β_𝓜 + ε with ε ~ N_n(0, σ²I) independent of X^r, σ² ≥ 0. Everything (m, Σ, β, σ², p) may depend on n.
(a) With β^𝒞 := β_𝒞 + Σ_𝒞𝒞⁻¹Σ_𝒞𝓜β_𝓜, τ² := β_𝓜ᵀ(Σ_𝓜𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁻¹Σ_𝒞𝓜)β_𝓜 and σ²_𝒞 := σ² + τ²: if σ²_𝒞 > 0 then
    (GR^c | σ(X^r_𝒞)) holds at each n with the deterministic (β^𝒞, σ²_𝒞). So §4 applies with no condition on how
    σ², τ² vary with n; [MIS1]'s requirement "τ_n² ≡ τ² fixed" (its lines 83-85) is not needed. (Example there: an
    independent omitted column of variance n² gives τ_n² = n²; the theorem then applies exactly when the hypotheses hold
    relative to σ²_𝒞 = σ² + n².)
(b) (Growing p_𝒞 ≤ n^A, sufficient population conditions.) Assume s := |supp β^𝒞| ≥ 1 fixed, λ_min(Σ_TT) ≥ c_pop > 0
    for T ⊆ 𝒞 with |T| ≤ s + max(j₀, m♯_n), max_j Σ_jj ≤ C₀, β^𝒞ᵀΣ_𝒞𝒞β^𝒞 ≤ M₀σ²_𝒞, and
    n·min_{j∈supp β^𝒞} Σ_jj(β^𝒞_j)²/(σ²_𝒞 log n) → ∞. Then E δ_n = O(r_n), so P(HPM ≠ supp β^𝒞) = O(r_n).
With centred rows (m = 0), supp β^𝒞 is SL's s̃ ([MIS1] Proposition P(b)).

## 6. Corollary H (density contraction around the projected law — the analog of SL's Theorem 4)

Fixed designs; a sequence of configurations κ_n ∈ 𝒦⁰_n(s, A, M, φ₀, C_OS) for all large n, laws P_{κ_n}. For the
parameter posterior Π of R′(a′), the fitted centred mean μ̂ := X_Sθ and
  h̄_n² := n⁻¹ Σ_i H²(N(μ̂_i, v′), N(μ_i(κ_n), v_n))   ((S, θ, v′) ~ Π; H² the squared Hellinger distance of [POST2] line 105):
(b) (no margin, no beta-min) there is C_H depending only on (s, A) such that, for every M_n → ∞,
    Π(‖μ̂ − μ(κ_n)‖² > C_H v_n log n or |v′/v_n − 1| > M_n n^{−1/2} | x, y^r) → 0 in probability; hence
    Π(h̄_n² > (1 + C_H/4) log n/n | x, y^r) → 0 in probability.
(a) (with the margin) if moreover κ_n ∈ 𝒦_n(…, c), c > c₁(s, A) (or 𝒦^λ_n, c > c₀(s, A)): for every M_n → ∞,
    Π(‖μ̂ − μ(κ_n)‖² > M_n v_n or |v′/v_n − 1| > M_n n^{−1/2} or S ≠ S₀(κ_n) or ‖θ − θ(κ_n)‖ > M_n √(v_n/n) | x, y^r) → 0
    in probability; hence Π(h̄_n > M_n n^{−1/2} | x, y^r) → 0 in probability.
Under [MIS1]'s GR the reference N(μ_i(κ), v) is the (centred) conditional law of y_i given the candidates, i.e. the
Kullback–Leibler projection of the full model on the candidate class. Differences from SL's Theorem 4: in-sample
average distance, convergence in probability, the shipped prior, p_𝒞 ≤ n^A with s fixed; a rate is given.

## 7. Remarks (each is a one-step consequence of Lemma R′)

**Remark SNR (the well-specified theorems hold with n-dependent σ*²).** Take 𝒞 = [p]. [W3P] Theorem 1 (items 1–6) and
[POST2] Claims A1, B, C, D, E hold when σ*² = σ*²_n > 0 varies with n in any way (and, in the random-design items, is a
measurable function of the design), provided every hypothesis is read in signal-to-noise form — (E): ‖μ‖² ≤ nMσ*²_n;
Claim B's reference cost: B_T(ϑ) ≤ Bσ*²_n; beta-min, (ID), (ID^M) are already relative to σ*² — and every constant
is evaluated at σ*² = 1; Claim D's thresholds become ‖μ̂ − μ‖² > C_Hσ*²_n log n, resp. > M_nσ*²_n, and
‖θ − θ*‖ > M_nσ*_n n^{−1/2}.
**Remark P ([MIS1] in signal-to-noise form).** [MIS1] Theorem MIS (i), (ii), (ii′) hold with σ²_𝒞 replaced by any
σ²_{𝒞,n} > 0 (in (ii): any measurable σ²_𝒞(x) > 0), with ‖μ^𝒞‖² ≤ Mnσ²_𝒞 in place of ‖μ^𝒞‖² ≤ Mn. [MIS1] Theorem F
holds with σ² = σ²_n > 0 arbitrary and ‖μ_c‖² ≤ Mnσ²_n in place of ‖μ_c‖² ≤ Mn (so σ²_{𝒞,n}/σ²_n ∈ [1, 1 + 2M]).
**Remark U (uniqueness of the target).** If two representations (β, v), (β′, v′) of the same law at the same x both
lie in 𝒦_n (or 𝒦^λ_n) with the same constants and n ≥ n₀ is so large that C r_n < ½, then supp β = supp β′.

## 8. Inputs (registry id @ version; state ACTIVE on base main 16a7f85) and their verbatim statuses

- W3-POST2:C@1.0.0, W3-POST2:E@1.0.0, W3-POST2:A1@1.0.0, W3-POST2:D@1.1.0, W3-POST2:B@1.0.0 — registry status
  "PROVED (by this seat, unchecked)"; council C1 passed (registry `council` field); `Theory_work/Wave3/HQ_DECISIONS.md:48-49`
  records PROVED-CHECKED labels. Under PROTOCOL rule 11 they are used here as **declared hypotheses**: every status of
  §§2–7 reads "conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:D" (as applicable) until HQ's acceptance
  record exists.
- W3-POST:Thm-1@1.0.0 (Remark SNR only) — "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)".
- C-MIS:Prop-P@1.0.0, C-MIS:GD(b)@1.0.0 (Corollary G), C-MIS:Thm-MIS(i)@1.0.0, C-MIS:Thm-MIS(ii)@1.0.0,
  C-MIS:Thm-F@1.0.0 (Remark P) — council R07/R08 PASS (registry).

## 9. Relation to [MIS1] and non-claims

**Implies.** §2 (on 𝒦^λ_n) + §4 ⇒ the main clauses of C-MIS:Thm-MIS(i), (ii) (rate, PIPs, MPM, HPM) under their
hypotheses: (F_w; g₀) implies (OS) for large n ([POST2] line 46), BM-∞ implies (BM^σ; c) eventually, and a fixed σ²_𝒞
is a special case. Their inclusion clause is recovered by §3(c) for c > c₁(s, A), and for [MIS1]'s range c > c₀(s, A)
by Remark P.
**New relative to [MIS1].** (1) no fixed variance: any σ²_{𝒞,n} > 0, design-measurable in the random case;
(2) GR only on the contrast law; (3) hypotheses (OS), (ID^M) instead of (F_w), (F_λ), beta-min; (4) expectation rate,
uniform over a configuration class, so rates for HPM/MPM/PIPs; (5) random designs by conditioning: conditional and
uniform conclusion, slices in s, tight constants, any σ-field 𝓕_n; (6) no-margin clauses in expectation; (7) a
density-contraction corollary; (8) Gaussian rows with n-dependent parameters.
**Not claimed.** Non-Gaussian or non-scalar contrast residuals (Example E2 of [MIS1] `L5_frontier.md:80-88` shows the
target changes under a common random slope unless it is put in 𝓕_n); s(κ) = 0; growing s; p > n^A; anything about
the sampler or the reported HPM beyond [MIS1] Corollary H (whose first term now has the rate 2C r_n); an out-of-sample
(integrated) Hellinger statement; sharp constants (c₁, c₀ are proof artefacts).

## 10. Assumption ids (for the registry block)
A:MISR-GRC (new; GR^c: contrast-law Gaussian residual with scalar covariance; implied by A:GR; implies the
A:GAUSS-NOISE interface for the unit-noise model through Lemma R′(b), the bridge); A:MISR-ESNR (new; (E^σ; M));
A:MISR-IDM-SNR (new; (ID^{M,σ}; c), = A:POST2-IDM for the unit-noise model); A:POST2-F0; A:POST2-OS; A:POST2-FLAMBDA
and A:BETAMIN (relative form) for 𝒦^λ_n; A:FIXED-S0; A:P-POLY; A:IID-GAUSS-ROWS (Corollary G only).
