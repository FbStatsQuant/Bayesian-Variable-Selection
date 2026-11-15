# W3-DIST — STATEMENT (candidate statements; v1.0, 2026-11-15; lead: Claude Fable 5.2, Claude Third, high)

## Changelog (every edit tagged against the A1 parity checklist: STRONGER / WEAKER / EQUAL)
- v1.0 (2026-11-15) — first version. Baseline for the tags; nothing to compare against.
- v1.0.1 (2026-11-15, before any review; lead self-check of route step X4) — (i) the range of t in DIST-1, Lemma X and
  Lemma S is M₀ log n ≤ t ≤ n^{1−κ₀} (fixed κ₀ ∈ (0, 1)) instead of t ≤ c₀n: near t ≍ n the dimension cut no longer beats the
  variance-plug-in error. **EQUAL** against A1 (metric, mode, rate, prior unchanged; sequences with ε_n² > n^{−κ₀} are
  covered by monotonicity with exponent c n^{1−κ₀}). (ii) s₀ may be smaller than |supp β*| when a true column is
  constant in the sample; stated explicitly. **EQUAL** (clarification).
- v1.0.2 (2026-11-15, before the blind read; after helper H1 `work/prior_probe/REPORT.md`, unchecked) — (i) stretch item
  S-DIM restated: an exponential-form size tail at s₀ + O(t/log n) without (ND) is **refuted** by duplicate columns (H1 F4);
  what remains open is a *fit tail*. Stretch items are not targets: **EQUAL**. (ii) Lemma V (H1) recorded as the tool for
  step X4(b). **EQUAL**. (iii) Reading of [SL] (11) corrected in ROUTES §1 (it fails with the coded cap). **EQUAL**.

**Status of everything in this file: CANDIDATE (scoping leg; nothing here is proved).** The only pieces with a complete
argument written down are Lemma H (five lines, §3) and the reduction steps of Lemma T (§3); both are *unchecked*.
Statuses of consumed results are verbatim from their files or from `Theory_work/INFRA/registry/claims.tsv`.

Aliases: **[W3P]** = `Theory_work/Wave3/W3-POST/STATEMENT.md` (v1.4); **[P2]** = `Theory_work/Wave3/W3-POST2/STATEMENT.md`
(v1.2.1); **[D]** = `W3-POST2/lemmas/D_hellinger.md`; **[SL]** = Song & Liang (2015), journal pages; **[SAMP]** =
`Theory_work/Wave3/W3-SAMP/STATEMENT.md`; **[CC]** = `W3-SAMP/lemmas/CC_code_check.md`.

## 0. Setting and objects

**Data (RD).** Triangular array. Rows (x_i, y^r_i), i ≤ n, i.i.d.: x_i ~ ν_x, an **arbitrary** law on ℝ^{p_n};
y^r_i = α* + x_iᵀβ* + ε_i with ε_i ~ N(0, σ*²) independent of the design (Gaussian noise, as in [SL] model (1));
σ*² > 0 fixed. **Strict sparsity** ([SL] (4)): |supp β*| = s₀^r fixed. 2 ≤ p_n ≤ n^A, A ≥ 1 fixed, p ≫ n allowed.
True joint density f*(x, y) = ν_x(dx) φ(y; α* + xᵀβ*, σ*²). P* = joint law of the data.

**The exact posterior (prior as coded).** Π(· | D_n) is the exact working-model posterior of (S, θ_S, v) of [W3P] §0
and [D] D0 on the response scale: models S ∈ Ω = {|S| ≤ K}, K = min(p, ⌊n/2⌋), over the retained (non-constant)
columns; prior w(k) = ½/C(2p−1, k) (BB(1, p) capped at K); slab N(0, n v (G_S + I)⁻¹) on sample-standardised columns;
IG(0.01, 0.01) on the standardised response scale (rate b₀s_y² on the response scale). No tuning is added.
θ* = D_xβ* restricted to retained columns, S₀ = supp θ*, s₀ = |S₀| ≤ s₀^r, μ = CX^rβ* (a dropped true column
contributes 0 to μ). s₀ is design-measurable and may take any value in {0, …, s₀^r}; constants below are maxima over
this finite range, and s₀ ≤ K is assumed (true for n ≥ 2s₀^r, p ≥ s₀^r).

**The density attached to a posterior draw.** For (S, θ, v): raw coefficients b_j = θ_j/ŝ_j (ŝ_j = sample SD of column
j), plug-in intercept â = ȳ^r − x̄ᵀb, and
  f_{S,θ,v}(x, y) := ν_x(dx) φ(y; â + xᵀb, v).
(The working model is centred and has no intercept parameter; with a flat-prior intercept the conditional posterior of
the intercept is N(â, v/n) and the statements below are unchanged — Remark R1, candidate.)

**Distance.** d_H²(f, g) := 1 − ∫√(fg) (Hellinger affinity form). [SL]'s d² = ∫(√f − √f*)² = 2 d_H². Since both
densities share the x-marginal, d_H²(f_{S,θ,v}, f*) = E_x H²(N(â + xᵀb, v), N(α* + xᵀβ*, σ*²)) with x ~ ν_x independent
of the data. This is the distance of [SL] Theorems 1–2 (P1), not the in-sample average of [D].

**Sample-level interfaces (X-measurable; design-agnostic; all at a given n).**
- **(E; M)** energy: ‖μ‖² ≤ nM. ([W3P] §2.)
- **(C; M′)** coefficient cost: ‖θ*‖² ≤ nM′. (Very weak: (E) ∧ (F₀) give the far stronger ‖θ*‖² ≤ 1.5M/φ₀² — [P2]
  Implications; (C) is the hypothesis of [W3P] Lemma 1a′ with T = S₀.)
- **(ND; c_D, m)** no degeneracy on average = [P2] (ADG; c_D) on the range 1 ≤ j ≤ min(m, p − s₀):
  C(p − s₀, j)⁻¹ Σ_{J⊆[p]∖S₀, |J|=j} (D_{S₀}/D_{S₀∪J})^{1/2} ≤ [c_D(n + 1)]^{−j/2}.
  Sufficient: [P2] (DG; c_D), or [W3P] (F_w; g₀) with c_D = g₀/(1 + g₀) ([P2] A0, status "PROVED (by this seat,
  unchecked)"). In words: adding j columns to S₀ multiplies the Occam determinant by about n^j on average over J;
  it fails only under near-exact linear dependence (unnormalised Gram eigenvalues of order 1 or less, i.e.
  1 − R² ≲ 1/n). It is **not** an identifiability or beta-min condition and puts no lower bound on signals.
- **(F₀; φ₀)** λ_min(X_{S₀}ᵀX_{S₀}/(n−1)) ≥ φ₀² (only for Theorem DIST-3).
Cutoff: m_n(t) := min{K, s₀ + ⌈(s₀ log(2p) + ((s₀+2)/2) log(n+1) + 3t)/log 2⌉} (a data-free integer of order log n + t).

## 1. Candidate theorems for the exact posterior (target (i); P1–P5)

**Theorem DIST-1 (joint Hellinger contraction, exponential form, sharp rate).** Fix (s₀^r, A, σ*², M, M′, c_D) and κ₀ ∈ (0, 1). There are
constants c ∈ (0, 1], C, M₀, n₀ < ∞ depending only on these such that, in (RD), for every n ≥ n₀ and every
real t with M₀ log n ≤ t ≤ n^{1−κ₀}:
  P*[ Π( d_H(f, f*) > C√(t/n) | D_n ) > e^{−ct} ] ≤ 3e^{−ct} + P*( (E; M)ᶜ ∪ (C; M′)ᶜ ∪ (ND; c_D, m_n(t))ᶜ ).   (1.1)
Equivalently, for every sequence ε_n with C²M₀ log n/n ≤ ε_n² ≤ C²n^{−κ₀} and c₁ := c/C²:
  P*[ Π( d_H(f, f*) > ε_n | D_n ) > e^{−c₁nε_n²} ] ≤ 3e^{−c₁nε_n²} + P*(interfaces fail),
which is [SL] (15) with an explicit remainder. Consequences:
- (a) **[SL] (15)-form** holds whenever P*(interfaces fail) ≤ e^{−c₁nε_n²}. At the best rate ε_n² = C²M₀ log n / n the
  right side is n^{−cM₀}: a polynomial, so polynomial-probability control of the design events is enough.
- (b) **[SL] (16)-form**: if P*(interfaces fail) → 0 then lim P*[Π(d_H > ε_n | D_n) > e^{−c₁nε_n²}] = 0.
- (c) **Rate (P3)**: ε_n² ≍ M₀ log n / n with M₀ of order s₀(A + 1), i.e. of order s₀ log p / n when p = n^A. No beta-min,
  no eigenvalue floor on any set, no identifiability condition ([SL] Condition 3 is not used).
- (d) **No condition on ν_x enters the passage from the sample to the population distance** (Lemma T is
  distribution-free); the law of x matters only through the probability of the three interfaces.
- (e) **Posterior predictive.** For the posterior-mean density f̄ := ∫ f dΠ(f | D_n): on the event in (1.1),
  d_H²(f̄, f*) ≤ C²t/n + e^{−ct} (convexity of d_H² in its first argument).

**Theorem DIST-2 (no design condition beyond energy; slower rate).** Fix (s₀, A, σ*², M, M′). There are c, C, M₀, n₀
such that for n ≥ n₀ and M₀ log n ≤ t ≤ n^{1−κ₀}:
  P*[ Π( d_H(f, f*) > C√(t log(p ∨ n)/n) | D_n ) > e^{−ct} ] ≤ 3e^{−ct} + P*( (E; M)ᶜ ∪ (C; M′)ᶜ ).   (1.2)
Best rate ε_n² ≍ s₀ log n · log p / n; in [SL]'s form the exponent is c nε_n²/log(p ∨ n), not c nε_n² (P2 exponent:
short by the factor log p; P3: short of [SL] by a logarithm — see CHECKPOINT parity table). No condition at all on the
dependence among predictors; (ND) is not assumed.

**Theorem DIST-3 (parametric rate under selection consistency; in probability).** In (RD), suppose there are events on
which (E; M), (F₀; φ₀) hold with common constants and with probability → 1, δ_n = 1 − π(S₀) → 0 in P*-probability
(e.g. under [W3P] Theorem 1, [P2] Claim A1 or Claim E with their beta-min conditions), and the fixed-support transfer
**(TR₀; C_T)**: P*( E_x(a + uᵀx)² ≤ C_T · n⁻¹Σ_i(a + uᵀx_i)² for all a ∈ ℝ and all u supported on supp β* ) → 1
(a comparison of the population and sample second-moment matrices of (1, x_{supp β*}); it holds with any C_T > 1 for a
fixed law of x_{supp β*} with finite second moments, by the law of large numbers, degenerate directions included).
Then for every M_n → ∞:
  Π( d_H(f, f*) > M_n/√n | D_n ) → 0 in P*-probability.
(No exponential inner threshold is possible at this rate: Π(S ⊋ S₀ | D_n) ≥ order n^{−1/2} by [W3P] Proposition LB,
and one-extra-variable models sit at distance of order √(log n/n).)

**Stretch statements (not targets of the first proof leg; listed so the route is on record).**
- **S-APX (approximate sparsity, [SL] (3)/(8), P4 stretch).** Replace S₀ by a reference pair (T, ϑ), |T| = t₀ fixed,
  with cost B_T(ϑ) ≤ B ([P2] Claim B) and bias ‖μ − X_Tϑ‖² ≤ nΔ_n². Candidate: (1.1)/(1.2) hold with ε² replaced by
  ε² + C·Δ_n². ([SL] (8) asks Δ(r_n) ≺ ε_n, the same order.)
- **S-EXP (exponential p).** Candidate: (1.1) with log n replaced by log(p ∨ n) for log p = o(n); constants no longer
  through A. Not attempted in the first leg.
- **S-FIT (sharp rate with no design condition; was S-DIM).** Without (ND), the posterior size has a geometric tail
  of ratio ≈ ½ and no better (duplicate columns: [T03R] Proposition D; H1 check C4), so a size cut at s₀ + O(t/log n)
  with mass e^{−ct} is **false** in general. But near-duplicate columns fit almost no extra noise, so the Hellinger
  statement of DIST-1 may still hold without (ND) through a *fit tail* (effective dimension eᵀM_Se instead of |S|).
  Numerics N4 are consistent with this (ASSUMPTION_MAP §3). If true, DIST-2's logarithm disappears and (ND) drops out of
  DIST-1. OPEN; see ROUTES §5. H1 derived (unchecked) the design-free superset bound
  Σ_{|J|=j} π(S₀∪J)/π(S₀) ≤ poly(j)(√(1+η)/2)^j · O_P(1) (its Lemma V); non-supersets are open.

## 2. Candidate theorem for the method as coded (target (ii); P6)

**Code facts (pins; core = commit 4676af6, unchanged at cef2c32).** On a completed run the fit returns
`hpm` (`Scripts/SMC_BVS/core/v3_run.R:142`), `pip_r` and `pip_primary` (`:159-162`), `mpm` (`:163`), `log_Z` (`:154`),
and `top_store` = the ledger's top store (`:210`; `cpp/v3_core.cpp:358-366`): the 40p + 1 best-scored distinct models
offered to the final-run ledger (`cpp/v3_ledger.h:43-56, 78`) with their exact scores F(S) = log ϖ(S) + log m(S)
([CC] CC2, status "CODE-CHECKED"). **The run returns no particles, no draws of (β, σ²) and no predictive
distribution.** So "the distribution the coded SMC returns" has to be defined as a function of the returned output;
three canonical choices, each computable from the output and the data in closed form ([D] D0):
- **Store BMA.** 𝒯 := `top_store` models; π_𝒯(S) := e^{F(S)}/Σ_{S′∈𝒯} e^{F(S′)}; Π̂^𝒯 := Σ_{S∈𝒯} π_𝒯(S) Π(· | S, D_n).
  Under EX-A (exact arithmetic) Π̂^𝒯 = Π(· | S ∈ 𝒯, D_n). This is the object of C-PACK SL2 (store-restricted PIPs).
- **HPM plug-in.** Π̂^H := Π(· | S = Ŝ, D_n), Ŝ = `hpm`.
- **MPM plug-in.** Π̂^M := Π(· | S = MPM, D_n), MPM from `pip_primary` (defined when |MPM| ≤ K).
`pip_primary` itself is a vector of marginal probabilities, not a distribution on models; its consistency is the
selection-level statement of [SAMP] (Theorems LT♯, C, TR) and is not restated here.

**Theorem DIST-C (coded output; jointly with output; conditional as labelled).** In the setting and on the event of
Theorem DIST-1 (or DIST-2, with its rate), write B_n := {d_H(f, f*) > C√(t/n)}.
- (C-i) **Store BMA, deterministic transfer.** For every data set, Π̂^𝒯(B_n) ≤ Π(B_n | D_n)/π(𝒯). Hence
  P*( {completed} ∩ {π(𝒯) ≥ η} ∩ {Π̂^𝒯(B_n) > η⁻¹e^{−ct}} ) ≤ 3e^{−ct} + P*(interfaces fail), for every η ∈ (0, 1],
  and on that event the store-BMA predictive density f̄^𝒯 satisfies d_H²(f̄^𝒯, f*) ≤ C²t/n + η⁻¹e^{−ct}.
- (C-ii) **When does the store hold the mass?** (α) With selection: on {completed} ∩ {S₀ ∈ 𝓜} ∩ {δ_n < ½}, S₀ ∈ 𝒯 and
  π(𝒯) ≥ ½ (the top store keeps the best-scored model — SOP:TH04 M4(c), status "N13: PROVED (PC1 claim 5)"; EX-A).
  P*({completed} ∩ {S₀ ∉ 𝓜}) → 0 is supplied by the existing delivery results under their own premises: [SAMP]
  Theorem D (D-iv) (P-MAP/P-CONC and P-OVL), W3-RM2:RM2-F / RM2-R, W3-START / START2 (statuses in the consumes table).
  (β) Without beta-min: π(𝒯) ≥ η is a **premise (P-STORE)** about the run; the output does not certify it in general
  ([SAMP] LT-f: the top store is a strict subset of Ω). Nothing is claimed about P-STORE here.
- (C-iii) **HPM plug-in.** Let 𝔅_n := {S ∈ Ω : Π(B_n | S, D_n) > e^{−ct/2}}. On the event of DIST-1,
  π(𝔅_n) ≤ e^{−ct/2}; so if the final-run ledger contains a model S′ with π(S′) > e^{−ct/2} (**premise P-HIT**; implied
  by S₀ ∈ 𝓜 when δ_n < ½), then Ŝ ∉ 𝔅_n and Π̂^H(B_n) ≤ e^{−ct/2}. With selection ((α) above), Ŝ = S₀ and
  Π̂^H = Π(· | S₀, D_n), which contracts at the parametric rate of DIST-3.
- (C-iv) **MPM plug-in.** On {MPM = S₀} (probability statements: [SAMP] LT-e, C-v, TR-d, under their premises),
  Π̂^M = Π(· | S₀, D_n); parametric rate as in DIST-3.
- **Honest label.** (C-i) and the first sentence of (C-iii) are deterministic and need no sampler premise. Everything
  that says the store or the ledger contains enough is conditional on a delivery premise (discovery of S₀, P-STORE or
  P-HIT) and is stated jointly with the output event; P(completed) → 1 is neither assumed nor claimed. Floating-point
  fidelity is EX-A. No statement is made about a particle approximation, because none is returned.

## 3. Key lemmas (stated precisely; ids as in DEPS.md)

**Lemma H (Hellinger reduction; deterministic).** For every (S, θ, v), with Δ(x) := (â + xᵀb) − (α* + xᵀβ*):
  d_H²(f_{S,θ,v}, f*) ≤ (v/σ*² − 1)² + E_x[min{1, Δ(x)²/(4σ*²)}].
*Proof.* Pointwise in x, [D] Lemma D0's computation gives H² = 1 − A·B(x) ≤ (1 − A) + (1 − B(x)), 1 − A ≤ (v/σ*² − 1)²,
and 1 − B(x) = 1 − exp(−Δ(x)²/(4(v + σ*²))) ≤ min{1, Δ(x)²/(4σ*²)}. Integrate over ν_x. ∎ (unchecked)
In-sample: Δ_i := Δ(x_i) = ε̄ + (μ̂ − μ)_i, so n⁻¹Σ_iΔ_i² = ε̄² + ‖μ̂ − μ‖²/n (μ̂ − μ ⊥ 1), μ̂ = X_Sθ.

**Lemma T (distribution-free sample-to-population transfer on sparse directions).** Let x₁, …, x_n be i.i.d. from any
law on ℝ^p, 1 ≤ d ≤ p, δ ∈ (0, 1). With probability ≥ 1 − δ, simultaneously for all a ∈ ℝ, c > 0 and u ∈ ℝ^p with
|supp u| ≤ d:
  E_x[min{1, (a + uᵀx)²/c}] ≤ 2·n⁻¹Σ_i min{1, (a + uᵀx_i)²/c} + η²_n(d, δ),
  η²_n(d, δ) := (4/n)[d log(ep/d) + 2(d + 1) log(4en/(d + 1)) + log(4/δ)].
No moment, tail, small-ball or eigenvalue condition. *Route:* the level sets {x : |a + uᵀx| > s} are unions of two
half-spaces of a d-dimensional coordinate subspace; apply the Vapnik–Chervonenkis relative deviation inequality
(sup_A (P(A) − P_n(A))/√P(A) ≤ η w.p. ≥ 1 − 4 S(2n) e^{−nη²/4}; Anthony & Shawe-Taylor 1993 — to be cite-checked) to
that class, integrate over the level t ∈ (0, 1) with Cauchy–Schwarz to get Pg − P_ng ≤ η√(Pg), and solve. (unchecked)

**Lemma X (in-sample exponential core; fixed design; the key new lemma).** Fixed design, noise G, R1 sizes. Under
(E; M), (C; M′), (ND; c_D, m_n(t)): there are c, C, M₀, n₀ (depending on (s₀, A, σ*², M, M′, c_D, κ₀) only) such that for
n ≥ n₀ and M₀ log n ≤ t ≤ n^{1−κ₀}:
  P_ε[ Π( ‖μ̂ − μ‖² > Cσ*²t  or  |v/σ*² − 1| > C√(t/n) | y ) > e^{−ct} ] ≤ 2e^{−ct}.
Structure: (X1) a noise event of probability ≥ 1 − e^{−ct}; (X2) on it, every "good" model (|S| ≤ d_t := s₀ + ⌈C′t/log n⌉ — of order t/log n, since log(n/t) ≥ κ₀ log n —,
ridge loss L_S ≤ C″σ*²t) has conditional posterior mass ≤ e^{−ct} outside the ball; (X3) small models with large ridge
loss have total mass ≤ e^{−ct}·π(S₀); (X4) models with |S| > d_t have total mass ≤ e^{−ct} with probability ≥ 1 − e^{−ct}
(supersets by truncated Occam moments under (ND); other large models through their union with S₀; sizes above m_n(t)
by Lemma S). Tool for X4(b): **Lemma V** of `work/prior_probe/REPORT.md` §3 (helper-derived, unchecked): for S ⊇ S₀ and
η > 0, Q_{S₀} − Q_S ≤ eᵀD′e + (1 + 2/η)ρ′ and E[(D_{S₀}/D_S)^{1/2} exp(eᵀD′e/(2σ*²))] ≤ (1 + η)^{s₀+|J|/2}, with no floor.

**Lemma X′ (the same without (ND)).** Under (E; M), (C; M′) only, the conclusion of Lemma X holds with ‖μ̂ − μ‖² >
Cσ*²t log(p ∨ n) in place of ‖μ̂ − μ‖² > Cσ*²t (steps X1–X3 with d_t replaced by m_n(t); X4 is Lemma S alone).

**Lemma S (design-free size tail with an exponential tail).** Fixed design, G, (E; M), (C; M′), p ≥ 2, s₀ ≤ K. For
n ≥ n₀ and log n ≤ t ≤ n^{1−κ₀}:  P_ε[ π(|S| > m_n(t)) > e^{−t} ] ≤ 2e^{−t}.
(Strengthens the tail of [W3P] Lemma 1a′, whose failure probability is of order 1/log L; same cutoff order.)

**Lemma P6 (deterministic).** For every data set, every 𝒯 ⊆ Ω with π(𝒯) > 0 and every measurable B:
Π(B | S ∈ 𝒯, D_n) ≤ Π(B | D_n)/π(𝒯); and for 𝔅 := {S : Π(B | S, D_n) > a}: π(𝔅) ≤ Π(B | D_n)/a.

**Bridges (examples; candidates; not part of the theorems).**
- **B1.** If Var(xᵀβ*) ≤ M/2 and Σ_j Var(x_j)β*_j² ≤ M′/2 with uniformly integrable squares (or a fixed law), then
  P*((E; M) ∩ (C; M′)) → 1; if xᵀβ* and the true coordinates are sub-Gaussian with constant K_x, the failure
  probability is ≤ e^{−c(K_x)n}. ([SL] Condition 1 implies the second, Condition 2 the first up to uniform integrability.)
- **B2.** (ND) from population quantities: if every (m_n(t) + s₀)-sparse sub-vector of x has a covariance with
  condition number ≤ c n and satisfies a small-ball bound, and max_j ŝ_j²/Var(x_j) is controlled, then (F_w; g₀), hence
  (ND), holds with probability ≥ 1 − e^{−cn} − (tail term). For Gaussian rows this is implied by W3-POST Corollary 1R
  (LSF). The candidate improves 1R's requirement ψ_n√n/(log n)^{3/2} → ∞ to ψ_n ≳ 1/n. To be stated exactly in the
  proof leg.

## 4. Consumes table (claim id, recorded status, exact statement used)

| consumed | recorded status (verbatim) | used for | exact content used |
|---|---|---|---|
| W3-POST2:D (v1.1.0; D.D(a) 1.0.0, D.D(b) 1.2.0) | registry: "PROVED (by this seat, unchecked)"; council-passed C1 (8.6/8.6), acceptance pending | DIST-3; Lemma H; template for X2 | Lemma D0 (pointwise Hellinger bound); D1(a)–(d) (conditional moments, no floor); D(a) |
| W3-POST2:A0, A1 (1.0.0) | "PROVED (by this seat, unchecked)" | (ND) interface; X4 | (F_w) ⇒ (DG) ⇒ (ADG); truncated Occam weights a_J (to be re-derived with t-scaled truncation) |
| W3-POST2:B (1.0.0) | "PROVED (by this seat, unchecked)" | Lemma S (starting point); S-APX | size tail with approximate reference and exact determinant |
| W3-POST2:E (1.0.0) | "PROVED (by this seat, unchecked)" | X3 (template) | Lemma E1(b): likelihood-ratio bound for models with large ridge loss, (E), (F₀) only |
| W3-POST:Lemma-1a′ (1.0.0) | "PROVED (by this seat, unchecked)" | Lemma S (to be strengthened) | design-free size tail (weak tail in L) |
| W3-POST:Thm-1 (1.0.0), item 6 | "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" | DIST-3 (δ_n → 0; random-design interface form) | items 1, 6 |
| W3-POST:Prop-LB (1.0.0) | "PROVED (by this seat, unchecked)" | remark in DIST-3 | 1 − π(S₀) ≥ 1/(1 + √(n+1)) |
| W3-POST:Cor-1R (1.0.0) | "PROVED (by this seat, unchecked)" | example for B2 | Gaussian rows + LSF ⇒ (F_λ), (F_w) events |
| T04 (`Docs/Theory/proofs/T04_A3_contraction/`) | "proved (Opus 5.5 lead; reviewed by 2 independent Opus 5.5 xhigh, CP + CW); not adopted"; **not in the registry** | route guide only for Lemma X′ | master-theorem structure; **not consumed as a premise** (PROTOCOL rule 11: not an ACTIVE registry claim) |
| C-PACK SL0/SL2 (`Wave1C/C-PACK/lemmas/I4_SL_corollaries.md`) | "PROVED (by this seat, unchecked)", R34-checked; council C1 passed | DIST-C framing | SL0(ii) (TV identity), SL2 (store-restricted object) |
| SOP:TH04 (1.0.0) M4(b), M4(c) | "MZ-P3 … AUTHOR-ONLY"; M4(c): "N13: PROVED (PC1 claim 5)" | DIST-C (C-ii)(α) | retention: S₀ ∈ 𝓜 and δ < ½ ⇒ S₀ ∈ 𝒯 |
| W3-SAMP:CC (1.1.1) | "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" | code facts | CC2 (ledger, HPM), CC3 (PIPs, MPM, log Z) |
| W3-SAMP:D (2.1.1), LT♯ (2.0.1), C (1.1.1), TR (2.1.1) | "PROVED-CHECKED" | DIST-C (C-ii)–(C-iv) discovery / MPM premises | D-iv; LT-e; C-v; TR-d |
| W3-RM2:RM2-F, RM2-R (1.0.0) | "PROVED-CHECKED, conditional on SOP:TH09" / "… conditional on W2-APP:POST" | DIST-C (C-ii)(α) | reported-model consistency (S₀ ∈ 𝓜 jointly with output) |
| W3-START / START2 (1.0.0) | "PROVED-CHECKED" | DIST-C premises (P-OVL / start mass) | OVL, START-R (as premises of [SAMP] D) |
| SOP:TH09 (1.0.0), W2-APP:POST (1.0.1), W1-PXN (P) | "T03♯: PROVED; SF VERIFIED …"; "PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied"; "XF VERIFIED" | DIST-3 instances | δ_n = O_P(√(log n/n)) |
Rule 11: every consumed premise below PROVED-CHECKED is carried as an explicit hypothesis into the status text of the
result that uses it ("conditional on …"). Theorems DIST-1, DIST-2 and Lemmas H, T, X, X′, S, P6 are planned
**self-contained** (they re-derive what they need from the closed forms of [P1] `thm:T01i`, `lem:spec`), so their only
consumed premise is the identification of the coded posterior with the contrast model (locked T01).
