# W3-DIST helper brief — NUMERICS HARNESS — Claude Sonnet 5.5, Claude Third, effort high

You are a helper of ticket W3-DIST (lead: Claude Fable 5.2). Repo clone `/home/fb31/Bayesian-Variable-Selection`.
**Write only under `Theory_work/Wave3/W3-DIST/work/numerics/`.** Run no git command. Start no agents. Local CPU only
(≤ 8 cores, total wall-clock ≤ 45 min; no NOTS, no cluster, no R/C++ build — Python with numpy/scipy only).
Deliver: scripts, raw outputs (`*_out.txt` or `.csv`), and `RESULTS.md` with tables and a 10-line reading. Report what
the numbers show, including anything that contradicts the lead's predictions. Fixed seeds; every table reproducible.

## The exact posterior (coded target; `Theory_work/Wave3/W3-POST/STATEMENT.md` §0)
Raw data (X^r, y^r), n rows. Drop constant columns. X = centred columns scaled so that ‖x_j‖² = n − 1;
s_y² = ‖Cy^r‖²/(n − 1); y = Cy^r/s_y. K = min(p, ⌊n/2⌋). For a model S (|S| ≤ K): G_S = X_SᵀX_S, H_S = (n+1)G_S + I,
z_S = X_Sᵀy, Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, D_S = det H_S / det(G_S + I), ν = 0.01 + n/2, b₀ = 0.01,
log π(S) = const + log w(|S|) − ½ log D_S − ν log(2b₀ + Q_S), w(k) = ½ / C(2p − 1, k).
Given S: σ² | S, y ~ InvGamma(shape ν, rate b₀ + Q_S/2); β_S | σ², S, y ~ N(n H_S⁻¹ z_S, n σ² H_S⁻¹) (standardised
scale). Back-transform: v = s_y² σ²; raw coefficients b_j = s_y β_j / sd_j (sd_j the sample SD used in the scaling);
predictive law of a new response at a new raw row x: N(ȳ^r + Σ_{j∈S} (x_j − x̄_j) b_j, v). Truth: N(α* + xᵀβ*, σ*²).
Sanity check the conjugate formulas once against brute-force quadrature at n = 8, p = 3.

## Distances
H²(N(a, v), N(b, w)) = 1 − (2√(vw)/(v + w))^{1/2} exp(−(a − b)²/(4(v + w))).
**Joint Hellinger** (the target): d²(f, f*) = E_x H²(N(m_f(x), v), N(m*(x), σ*²)) over a fresh x from the design law
(Monte Carlo, ≥ 20 000 fresh rows, common across posterior draws). (Song–Liang's d² is twice this.)
**In-sample**: h̄² = n⁻¹ Σ_i H²(·) at the n design rows; also the truncated in-sample mean-part
t̄ = n⁻¹ Σ_i min(1, Δ_i²/(4σ*²)), Δ_i = fitted minus true mean at row i.
Posterior mass Π(d² > ε² | D): draw ≥ 4000 (S, β, σ²) from the exact posterior (models by enumeration, see below).

## Model enumeration
- p ≤ 14: all models with |S| ≤ K (exact).
- p ≫ n (p = 4n and p = n^{1.5} capped at 600): **restricted** posterior on a declared family: all models of size ≤ 2
  over the full p, plus all subsets of size ≤ 5 of a pool U = S₀ ∪ {12 columns with the largest |corr| with y} ∪
  {4 random columns}. Label these results "restricted family" everywhere.

## Experiments (R = 40 replications each unless too slow; n ∈ {50, 100, 200, 400, 800} for p ≤ 14; n ∈ {50, 100, 200} for p ≫ n)
- **N1 rate, sub-Gaussian.** Rows N(0, Σ), Σ = AR(0.5); s₀ = 3, β* = (1, −1, 1) on the first three, σ* = 1.
  Report per n: posterior median, 0.9 and 0.99 quantiles of n·d² and of n·d²/log n (averaged over replications), and the
  tail curve M ↦ mean over replications of log Π(d² > M log n / n | D) for M ∈ {1, 2, 4, 8, 16}.
- **N2 heavy tails / second moments only.** Same with (a) iid t₂.₅ coordinates scaled to unit variance, (b) symmetric
  Pareto tail index 2.1, (c) "spike" columns: x_j = 0 w.p. 1 − 2/n, ±√(n/2) otherwise (many columns will be constant
  in-sample and dropped; a true column may be dropped — report how often, and d² in those cases).
- **N3 no beta-min.** N1 with β* = (1, c√(log n/n), c√(log n/n)), c = 0.7.
- **N4 collinearity boundary (the assumption the sharp rate uses).** N1 with p = 12 where 6 null columns are
  x₁ + τ·(independent noise), τ² ∈ {n⁻², n⁻¹, log n / n, 1}. Report the same statistics plus the posterior law of |S|.
  Lead's prediction: the Hellinger rate is essentially unaffected even when selection fails.
- **N5 approximate sparsity.** N1 with β*_j = j⁻² for all j ≤ p (p = 12), rescaled so Var(xᵀβ*) = 3.
- **N6 transfer check.** For every posterior draw in N1 and N2 record ρ = d²_mean / (2 t̄ + log n / n), where d²_mean is
  the mean part E_x min(1, Δ(x)²/(4σ*²)) at a fresh x; report max and 0.999 quantile of ρ per design. (A distribution-free
  inequality predicts ρ bounded by a constant, for every design law, heavy tails included.)
- **N7 p ≫ n.** N1 and N2(a) on the restricted family.

## RESULTS.md
One table per experiment; a final table "does n·d²/log n stay bounded? does n·d² stay bounded (with strong signals)?
does log Π(d² > M log n/n) decrease linearly in M with slope ≈ −c log n?" with yes/no/unclear and the numbers.
