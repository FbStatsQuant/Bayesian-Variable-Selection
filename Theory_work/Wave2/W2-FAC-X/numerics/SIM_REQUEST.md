# W2-FAC-X → W2-SIM request (2026-11-09)

Requester: W2-FAC-X (Theorem FAC-CS-iid: iid Gaussian rows, compound symmetry, proved route needs
limsup log p/log n < 1/2; Target 2: general one-factor loadings). Not blocking; results inform the frontier section.

## Scripts to reuse (all in Theory_work/Wave2/W2-FAC-X/numerics/)
* iid_core.py — exact iid-row sufficient statistics (X'X, X'y, y'y) at any n via Bartlett (no n×p matrix), general
  loadings Λ (p×k), `IidData(Lam, beta, n, rng)`; `ls0_path(P, start, S0)` = exact production LS0 move rule, uncapped,
  O(k(p−k)) per scan. Self-test: iid_selftest.py.
* n1x_iid_cs.py (CS paths from [p]; records pure deletion, final == S0, band defect, empirical δ̂), n2x_loadings.py
  (heterogeneous loadings), n5x_start.py (start mode with the production partition, bvs_core.py).
Production core runs (Scripts/SMC_BVS/core/, main 4676af6) are welcome for item C.

## A. Frontier beyond the proof range (iid CS rows) — highest priority
Design: rows iid N(0, (1−ρ)I + ρ11ᵀ), ρ ∈ {0.3, 0.7}; s0 = 4, coefficients (1.4, −1.0, 1.8, −1.2), σ = 1.
Grid: n ∈ {1e4, 1e5, 1e6}; p with log p/log n ∈ {0.5, 0.6, 0.7, 0.8, 0.9} and p ≤ n/2 (cap p at what is feasible,
ideally ≥ 5000); 20 seeds per cell. Start: the production start mode (n5x_start.py logic) if feasible, else [p].
Statistics per run: (1) uncapped LS0 path pure null deletion? (2) ends at S0? (3) number of moves vs MR1 cap
ℓ_n + |S̃₀|; (4) max over steps of the best addition gain / log n; (5) hull defect and band width (as n1x).
**What would change the theory:** at fixed A ∈ [0.5, 1), a failure rate of (1)/(2) that does not decrease with n
(or grows), or additions with gain > 0, would show the A < 1/2 limit is not only a proof-technique limit. A failure
rate → 0 with n supports the conjecture that consistency holds for every A < 1 (current N1X: 121/121 paths fine up to
A = 0.75 at n ≤ 1e6, p ≤ 1000).

## B. Target 2: fixed-dispersion one-factor loadings (iid rows)
Loadings: two-class λ ∈ {0.3, 0.9} and {0.5, 0.95} (alternating), and λ_j ~ U[0.2, 0.9] (fixed per j); same truths;
n ∈ {1e5, 1e6}, p ∈ {500, 2000, 5000}, 20 seeds. Same statistics (1)–(4). Also record whether the deleted null is the
argmin of the variable-centre statistic |ξ_j − ℓ_jX_T| (see n2x_loadings.py, rank_var).
**What would change the theory:** any failure of (1)/(2) not vanishing in n would indicate a genuine obstruction for
heterogeneous loadings (currently 64/64 fine at p ≤ 400).

## C. End-to-end (optional)
Production core on iid CS rows at (n, p) = (2e4, 2000), (5e4, 5000), 20 seeds: P(Ŝ⁺ = S0), LS0 scored S0, fallback use.

Please write results to Theory_work/Wave2/W2-SIM/results/ (a summary .md per item, raw .jsonl).
