# L5 — Frontier: what is not covered and why

Status (per claim): Lemma O1 — R03 VERIFIED-WITH-AMENDMENTS (applied); Lemma O2 — R03 VERIFIED-WITH-AMENDMENTS (its
original consequence paragraph was GAP/FALSE and was replaced); §6 Examples E2, E3 — added after R04, R05 VERIFIED;
§§3–5 remarks/conjectures, not claims. Sweep R06 fixes applied. Council pending.

## §1 A nonzero residual outside the unrestricted candidate span requires rank X_𝒞 < N

**Lemma O1.** If rank X_{c,𝒞} = N, then every full mean μ_c ∈ ℝ^N lies in the *unrestricted* span col X_{c,𝒞}: any
representation μ_c = X_{c,𝒞}θ + r with X_{c,𝒞}ᵀr = 0 has r = 0. *Proof.* col X_{c,𝒞} = ℝ^N and r ⊥ ℝ^N. ∎
(p_𝒞 ≥ n alone does not imply rank N.) Consequence. For a full-rank candidate design there is no residual outside the
unrestricted span, but μ_c may still have no *feasible* (|S| ≤ K ≈ n/2) or *sparse* representation: there
"the candidate set misses a true variable" means a question of sparse/capped representability (approximate sparsity),
outside T03♯ (exact s₀-sparse truth). EP with r = 0 and a sparse θ^𝒞 is of course possible (then it is the
well-specified case). GR (Theorem MIS) restores a *well-specified* conditional Gaussian candidate regression for any
p_𝒞; it is *sparse* only under the separately assumed projection-sparsity (fixed s₀^𝒞) — Gaussianity alone does not give
it (e.g. independent standard Gaussian candidates and an omitted variable equal to their sum plus independent noise: every
candidate has a nonzero projected coefficient).

## §2 Why T02(i♯) (the size tail) does not port to EP

What survives: the numerator identity E_true[m^c_b(S)/f_true] = 1 holds for every fixed rate b and every positive true
density ([P1] lem:num), misspecified or not. What fails is the denominator lower bound (Lemma den′), which was proved for
the true model with a pure-noise residual. Lemma O2 below is an obstruction to *that denominator strategy* only (the candidate densities can inflate their scalar
variance to ≈ σ² + Δ_n but cannot represent the orthogonal mean r); it says
nothing against posterior consistency under EP.

T02(i♯) (T03R §2, `PROOF.md:74-99`) bounds π(|S| > m | y) by a ratio whose numerator has E₀[I_{b₋}(E_m)/f₀(y_c)] =
ϖ(E_m) ([P1] `lem:num`; an identity valid under **any** true density f₀) and whose denominator is a lower bound on
m^c_{b₊}(S₀)/f₀(y_c) ≥ (n+1)^{−s₀/2}c_IG σ*² n^{−1/2}e^{−Λ_n} (Lemma den′, `PROOF.md:89-91`), proved for the
true model S₀ and the true variance.

**Lemma O2 (the denominator is exponentially small under EP).** Assume EP, G, rank X_{c,𝒞} =: d_n with d_n/N → 0,
and Δ_n ≥ Δ₀ > 0. Then for every rate b′ > 0 and every S ⊆ 𝒞, with f₀ = N_N(μ_c, σ²I),
  log[m^c_{b′}(S)(y_c)/f₀(y_c)] ≤ −(N/2)·log(1 + Δ_n/σ²)·(1 + o_P(1)),
uniformly in S ⊆ 𝒞 and b′ (the o_P(1) term does not depend on S or b′).
*Proof.* m^c_{b′}(S) is a mixture over (β, v) of N_N(X_{c,S}β, vI) densities (ridge slab N(0, nv(G_S + I)⁻¹) on β given v, and IG(a₀ + ½, b′) = IG(0.51, b′) on v in the contrast experiment;
[P1] §"Integral representation", `PROOF_v3.tex:52-56,340-342`; SoP `02_method.tex:127-130`), so it is at most sup_{β, v>0} N_N(y_c; X_{c,S}β, vI) = (2πv̂_S)^{−N/2}e^{−N/2},
v̂_S := ‖(I − P_S)y_c‖²/N. Let V := col X_{c,𝒞}. Since P_V ⪰ P_S and (I − P_V)μ^𝒞 = 0, r ∈ V^⊥:
N v̂_S ≥ ‖(I − P_V)y_c‖² = ‖r + (I − P_V)e‖² = ‖r‖² + 2rᵀe + ‖(I − P_V)e‖².
‖(I − P_V)e‖²/σ² ~ χ²_{N−d_n}, rᵀe ~ N(0, σ²‖r‖²); so v̂_S ≥ Δ_n + σ²(1 − d_n/N) − O_P(√(1/N)) − O_P(√(Δ_n/N))
= σ²_{𝒞,n}(1 − o_P(1)) uniformly in S. And f₀(y_c) = (2πσ²)^{−N/2}exp(−‖e‖²/(2σ²)) with ‖e‖²/σ² = N + O_P(√N).
Hence log(m/f₀) ≤ −(N/2)log(v̂_S/σ²) + (‖e‖²/σ² − N)/2 ≤ −(N/2)log(σ²_{𝒞,n}/σ²) + o_P(N), and
log(σ²_{𝒞,n}/σ²) = log(1 + Δ_n/σ²) ≥ log(1 + Δ₀/σ²) > 0. ∎
**Consequence for the technique (replaced after R03; the earlier draft's posterior bound and its "vacuous for every
m ≤ K" claim were a GAP and FALSE respectively).** O2 rules out the polynomial lower bound with a tight exponent used by
den′ in the full experiment. For Δ_n bounded away from zero, a method using only the numerator's mean and a single S₀
denominator incurs an exponential denominator loss. At a nonempty logarithmic cutoff m = O(log n), T03R E1(c) gives
log R_m = −o(n), so the prior factor cannot compensate for that loss. This obstructs that particular route to TAIL^𝒞 at
logarithmic cutoffs. It does not establish an upper bound on posterior tail mass, nor a sharp necessary cutoff for
arbitrary m (R03 exhibits a duplicate-column design where the same route does work at m = K − 1). TAIL^𝒞 for growing
p_𝒞 is discharged here by a different route — Lemma T / Corollary F(b) under (TL) — and for bounded p_𝒞 by
Corollary F(a); the window below (TL) remains open.

## §3 Repair routes (conjectures, not attempted to completion)
(a) **Sufficiency reduction.** π_𝒞(· | y) depends on y_c only through (P_V y_c, ‖(I − P_V)y_c‖²). Performing the T02(i♯)
change of measure in the reduced experiment replaces the e^{−cN} loss by e^{−c d_n} (variance mismatch σ² vs σ²_{𝒞,n} in
d_n directions; the 1-dimensional residual statistic costs O(1) after matching means). This would give TAIL^𝒞 when
d_n = O(log n). Not proved.
(b) **Large-Δ direct sums — SUPERSEDED by Lemma T (L4.9), which proves a stronger version of this route (no eigenvalue
condition beyond S₀^𝒞, threshold (TL)).** Original remark: When Δ_n ≥ (1 + ε)σ², the superset exponent (n/2)σ²χ²_j/(2b + Q) is ≤ tχ²_j with
t < ½ uniformly over sizes up to K (because 2b + Q^c_S ≥ ‖r‖² + 2rᵀe), so E e^{tχ²_j} = (1 − 2t)^{−j/2} without
truncation and the superset sum over all sizes ≤ K converges under SE_w(K; g₀); with (C6)(a) this would give TAIL^𝒞.
Not proved (the uniform control of 2b + Q over all S ⊆ 𝒞 of size ≤ K is the step to write).

## §4 Outside GR: non-Gaussian or heteroscedastic omitted residual
SL Theorem 4 covers a fixed-size candidate set under a general random design via the KL projection (SL §2.3). For our
prior and p_𝒞 ≤ n^A nothing is claimed. Numerics N5 (ω = x₀² − 1 and ω = x₀x₁ − 0.3 with Gaussian candidates, whose
linear projections on x_𝒞 vanish) show substantial finite-sample posterior mass on {3, 4} in these runs (median
π = 0.962 / 0.966 at n = 6400; mean PIP of a non-target candidate up to 0.13) — exploratory evidence consistent with a
possible KL-projection extension; no convergence or rate conclusion follows.

## §5 Fixed design without exact projection
If P_𝒞μ is not exactly sparse but is "sparse plus small", the residual signal leaks into extra candidates with
noncentral χ² terms; a GEN-type leakage condition (NL_η / NL_avg, GEN `STATEMENT.md` §2 (H2c)) would be the natural
hypothesis. Not attempted.

## §6 Boundary examples: why GR and EP cannot simply be deleted (from R04; R05 VERIFIED)

**Example E2 (Gaussian marginals are not enough for GR).** n even ≥ 4; deterministic centred orthogonal raw candidate
columns x₁, x₂ with ‖x_j‖² = n and x₂ᵢ = ±1 (balanced); Z ~ N(0, 1) independent of ε ~ N_n(0, I); omitted column
x_k := Z x₂; y^r = x₁ + x_k + ε. The omitted contribution ω = Zx₂ has E[ω] = 0, Gaussian marginals with identical
variance 1, but covariance x₂x₂ᵀ (rank one), so GR fails. A "mean-only" projection prescription (E[ω | X_𝒞] = 0) would
target {1}. Conditionally on Z = z ≠ 0, the candidate problem is a G-model (fixed design, σ² = 1) with raw coefficients
(1, z); standardisation rescales them by √(n/N); the T03♯ hypotheses hold (orthogonal design, p_𝒞 = 2, fixed nonzero
coefficients ⇒ BM-∞), so π_𝒞({1, 2} | y) → 1 in probability given Z = z. Since P(Z = 0) = 0, integrating over z
(dominated convergence for the bounded conditional probabilities) gives π_𝒞({1} | y) → 0 in probability under the joint
law. So the covariance/independence content of GR matters: a common random omitted slope defeats the transfer.
(Not an iid-row counterexample to Song–Liang; it violates their iid-row setting.)

**Example E3 (dropping EP for a fixed sparse target).** Fixed orthogonal candidates x₁, x₂ (X_𝒞ᵀX_𝒞 = N·I),
μ_c = bx₁ + cx₂ + r with b, c ≠ 0 fixed and r ⊥ span X_𝒞, ‖r‖² ≤ MN. If one names the fixed target {1} (i.e. treats cx₂
as part of a non-orthogonal "remainder" bx₁-residual r′ := cx₂ + r, which violates EP for the target {1}), the posterior
does not concentrate on {1}: EP holds for the target {1, 2} with θ^𝒞 = (b, c), and Corollary F(a) (p_𝒞 = 2; BM-∞ since
b, c are fixed; SE trivially) gives π_𝒞({1, 2} | y) → 1, hence π_𝒞({1} | y) → 0. So the orthogonality in EP is what
identifies the target; it cannot be dropped for a pre-named target.
(Neither example shows that GR or EP is necessary for *every* consistency theorem; they show the present transfer and
proof cannot be generalised by deleting those hypotheses.)
