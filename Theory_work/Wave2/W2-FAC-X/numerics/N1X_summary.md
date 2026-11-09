# N1X — iid Gaussian rows, compound symmetry: uncapped LS0 path from [p] (numerics/n1x_iid_cs.py → N1X_raw.jsonl)

Exact iid-row sufficient statistics (Bartlett, numerics/iid_core.py); production move rule (flip + swap neighbourhood,
best strict improvement, exact ties → lexicographically smallest set); start = [p] (the start-mode claim X1 is tested
separately). ρ ∈ {0.3, 0.7}, s0 ∈ {1, 4} (mixed signs), 2 seeds; 121 data sets. (The 'aligned' layout of the first
partial run gives identical paths for the same seed: given (ξ, W, …) the path from [p] does not depend on β — μ is
projected out of every RSS for T ⊇ S0 — so it was dropped.)

δ̂ = max over sampled path sets and kept nulls of |r_j/ĉ − (ξ_j − x̂)| (r_j the signed deletion statistic, (ĉ, x̂) a
least-squares fit) — an empirical proxy for max|δ_j(T)|; "band" = max over sampled steps of the distance from a kept
null inside the hull of the deleted nulls to the nearer hull end; "defect" = number of such kept nulls.

| n | p | A = log p/log n | runs | pure deletion & final S0 | max δ̂ | max δ̂/√(k log p/n) | max band | max defect | max add gain/log n |
|---|---|---|---|---|---|---|---|---|---|
| 1e4 | 16 | 0.30 | 12 | 12 | 0.089 | 1.72 | 0.081 | 1 | −0.408 |
| 1e4 | 63 | 0.45 | 12 | 12 | 0.258 | 1.84 | 0.298 | 8 | −0.378 |
| 1e4 | 251 | 0.60 | 12 | 12 | 0.524 | 2.68 | 0.706 | 65 | −0.339 |
| 1e4 | 1000 | 0.75 | 12 | 12 | 1.055 | 2.75 | 1.387 | 520 | −0.246 |
| 1e5 | 32 | 0.30 | 12 | 12 | 0.037 | 1.48 | 0.025 | 2 | −0.500 |
| 1e5 | 178 | 0.45 | 12 | 12 | 0.122 | 2.87 | 0.150 | 11 | −0.425 |
| 1e5 | 1000 | 0.60 | 12 | 12 | 0.330 | 2.73 | 0.502 | 205 | −0.304 |
| 1e6 | 63 | 0.30 | 12 | 12 | 0.026 | 1.91 | 0.018 | 2 | −0.417 |
| 1e6 | 501 | 0.45 | 12 | 12 | 0.076 | 2.48 | 0.087 | 26 | −0.406 |
| 1e6 | 1000 | 0.50 | 13 | 13 | 0.105 | 3.10 | 0.145 | 69 | −0.338 |

Findings. (1) 121/121 paths are pure null deletions of length p − s0 ending at S0 (no swap, no addition, no tie),
including A = 0.6–0.75 beyond the proved range (evidence that A < 1/2 is a proof-technique limit). (2) The deletion
order is **not** an interval of the sorted ξ's once pβ ≳ 1 (defect up to 520 at n = 1e4, p = 1000), but the defect is
confined to a band whose width is ≈ 1.3–1.5 × δ̂ (X3: w ≤ 4.3β). (3) δ̂ scales like √(k log p/n) with constant ≤ 3.1
(X2: δ ≤ C·H̄·√(p log n/n)). (4) Additions lose by ≥ 0.25 log n everywhere sampled.
