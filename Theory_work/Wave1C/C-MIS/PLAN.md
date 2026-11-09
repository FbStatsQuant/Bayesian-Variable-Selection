# C-MIS — PLAN

Deadline: checkpoint 01:30 CST, final report 04:30 CST (2026-11-09).

## Route
1. **L1 (reduction, Theorem MIS (i)).** Under GR, (X^r_𝒞, y^r) has exactly the law of a G-model with design X^r_𝒞,
   coefficients β^𝒞, noise σ_𝒞². The method and π_𝒞 are functions of (X^r_𝒞, y^r) only. T03♯ (TH09) applies with
   (S₀, θ*, σ*²) := (S₀^𝒞, θ^𝒞, σ_𝒞²). Points to check: T03♯'s hypotheses use only (X, θ*, σ*²) — not the generating
   mechanism; standardisation uses candidate columns; intercept absorbed by contrasts.
2. **L2 (Theorem MIS (ii)).** De-randomisation with an O_P (uniform tightness) diagonal argument, extending GEN L5.3
   (which handles probabilities → 0) to tightness.
3. **L3 (Proposition P, Theorem MIS (iii)).** Gaussian conditioning; block-inverse identity; graph-neighbour support.
   Lemma GD(a): |𝒞| fixed ⇒ (H-MIS) holds w.p. → 1 (sample correlation → population; m♯ = K). GD(b) growing p:
   attempt via a Gaussian smallest-singular-value bound + union bound, else leave as hypothesis.
4. **L4 (Corollaries H, D).** Read the T38-(0) proof to confirm it uses no property of S₀ beyond feasibility and no
   property of the data law; then substitute S₀^𝒞. Corollary D: GEN applies conditionally on X_𝒞 under GR; build the
   proxy instance on a GEN instance (check GEN L6 for which instance tolerates a generic fixed σ²).
5. **L5 (Theorem F).** Go through T03R (C1)–(C10) and [P3] with y_c = μ^𝒞 + r + e, r ⊥ col(X_𝒞): write every changed
   step in full (ongood(b),(c), new event G5, SvsSp, signalgain, Step 1 constant), cite unchanged ones; Step 0 ← TAIL^𝒞;
   Corollary F (bounded p_𝒞).
6. **L6 (frontier).** Rank-N vacuity of EP; the T02(i♯) change-of-measure obstruction (explicit KL computation);
   non-GR probe numerics.

## Numerics (falsification, local, Python 3.13 + numpy; exact enumeration, p_𝒞 ≤ 12, ≤ 20 seeds)
* N1: jointly Gaussian design, one omitted variable with several graph neighbours among candidates; check
  π(S₀^𝒞) → 1 vs n; compare with naive S₀ ∩ 𝒞 and with the support of the *sample* projection.
* N2: chain design (candidate correlated with k only through another candidate): marginal correlation without
  being a neighbour ⇒ not selected (tests Prop P).
* N3: fixed design EP (r ⊥ col(X_𝒞) exactly, deterministic): π(S₀^𝒞) → 1; dilution: signals near the σ²-threshold but
  below the σ²_{𝒞,n}-threshold.
* N4: cancellation (β_j + γ_j = 0) ⇒ PIP_j → 0; small γ_j ⇒ shows the beta-min margin on β^𝒞.
* N5: non-GR probe (ω = x₁² − 1, heteroscedastic) — exploratory only.
* N6: Corollary D proxy instance at small scale (exact posterior; method run not attempted unless time).

## Reviews (per protocol)
Statement lock (Codex gpt-6.1-sol high) → lemma checks (Sol high; xhigh for L5, the key technical lemma) →
mid-point (Sol xhigh, fresh) → exhaustive sweep (Sol high) → council (Sol xhigh + Opus high). CITECHECK script before the council.

## Fallbacks
If L5 fails: keep Theorem MIS + Corollaries; Theorem F only for bounded p_𝒞 (classical argument). If GD(b) fails:
hypothesis. If the GEN instance cannot be checked: Corollary D conditional on GEN's hypotheses (no instance).
