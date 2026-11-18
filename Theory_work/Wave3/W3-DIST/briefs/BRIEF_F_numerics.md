# Stream F (Claude Sonnet 5.5) — folder `work/F_numerics/` — falsification numerics and citecheck
Read `briefs/COMMON.md` first (you write no proofs). Local CPU only, ≤ 8 workers, set OMP/OPENBLAS threads to 1
before importing numpy, total wall-clock ≤ 60 min. Reuse `Theory_work/Wave3/W3-DIST/work/numerics/common.py` (exact
posterior, enumeration, distances; read `work/numerics/RESULTS.md` first for what exists). Report what the numbers
show, including anything against a statement. Deliver scripts, raw outputs and `RESULTS.md`.
1. **Nested tails (the statement of DIST-1).** p = 12, AR(0.5) Gaussian design, s = 3 strong signals, n ∈ {100, 400}:
   for each of 200 data sets compute Π(n·d² > t | D) **exactly by quadrature or with ≥ 10⁵ draws per data set**, t on a
   grid; report the distribution over data sets of that conditional probability (quantiles 0.5, 0.9, 0.99, max), not
   a pooled tail.
2. **Dangerous collinearity scale.** As experiment N4 of `work/numerics/RESULTS.md`, with 6 null columns =
   x₁ + τ·noise and τ² ∈ {log n/n², 4 log n/n², n⁻¹·⁵}; same statistics plus the law of |S|; n ∈ {100, 400, 1600}.
3. **(A5) violated.** Two true columns nearly equal (correlation 1 − 1/n) with coefficients +B and −B, B ∈ {1, √n, n}:
   report n·d² quantiles and the sample quantities ‖μ‖²/n and ‖θ*‖²/n.
4. **Lemma T.** For p = 50, d ∈ {1, 2, 3}, n ∈ {100, 1000} and three laws (Gaussian, t₂.₁, a law with an atom of mass
   1 − 1/n): search (random restarts + local optimisation over (a, u, c), u d-sparse) for the largest value of
   E_x min{1, (a + uᵀx)²/c} − 2·(sample mean); compare with η²_n(d, δ) of STATEMENT §3 at δ = 0.05.
5. **B2-core.** p = 200, q ∈ {2, 4}, n ∈ {200, 2000}, Gaussian AR(0.9) and independent Rademacher: smallest value over
   q-sparse u and a of [n⁻¹Σ(a + uᵀz_i)²]/[a² + Var(uᵀz)] found by search; frequency of values below ½ over 200 samples.
6. **Lemma V (b) and Lemma S's cutoff.** Re-run the helper's check of the moment bound on singular and duplicated
   designs (see `work/prior_probe/probe_checks.py`); and on the p = 12 enumerations of item 1 report π(|S| > m) against
   the cutoff inequality of Lemma S.
7. **Citecheck.** A script `citecheck.py` that extracts every `file:line` or `file:line-line` pin in
   `Theory_work/Wave3/W3-DIST/STATEMENT.md` and checks that the file exists and the lines exist; output a table and the
   count of MISS.
