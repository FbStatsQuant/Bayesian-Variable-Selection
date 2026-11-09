# W2-FAC-PK → W2-SIM: simulation request (2026-11-09)

Requester: W2-FAC-PK lead (compound symmetry, p > K = ⌊n/2⌋). Scripts to reuse (all in
`Theory_work/Wave2/W2-FAC-PK/numerics/`, Python 3.13 + numpy/scipy; self-test `pk_selftest.py` → `pk_selftest_out.txt`):
`pk_core.py` (closed-form exact-Gram CS start mode `start_mode_cs` and LS0 path tracer `path_from`), `cs_core.py`,
`n1_scale.py` (template driver), `fac_core.py` + `bvs_core.py` (general exact-Gram / general-design scorer, Schur scans,
start mode, `local_search`). Please write results to `Theory_work/Wave2/W2-SIM/results/FAC-PK/`.

## Theory being tested
* **Theorem NEG (proved, under review):** exact-Gram CS, liminf p/K > 16/15, θ̄ ≠ 0: the start mode has size K and the first
  N_n ≥ n^{1/2−o(1)} LS0 moves are swaps, so LS0 with the merged cap ℓ_n + |S̃₀| never scores S₀ (w.p. → 1).
* **Theorem PATH (proved, under review):** same class, K + 16s₀ + 1 ≤ p ≤ n − 1: the uncapped LS0 path ends at S₀ after
  m* ≤ (1 + δ)K moves, any δ > 0; so the cap ℓ_n + 2|S̃₀| works.
* **Open (frontier, not proved):** (a) the full production method under MR1 on these designs; (b) iid-row CS designs,
  in particular p ≫ n (study regime n = 200, p = 500).

## R1 — large-n closed-form paths (exact Gram), scaling of W and m*/K
Driver: `n1_scale.py` pattern (pk_core.make_cs, cs_partition(p, 16), start_mode_cs, path_from, summarize_moves).
Grid: ρ ∈ {0.2, 0.5, 0.8}; p/n ∈ {0.6, 0.8, 0.99}; n ∈ {2·10⁴, 6·10⁴, 2·10⁵} (larger if feasible; the path costs
O(K·p) numpy work — a sorted-structure implementation would allow 10⁶); truths S₀ = {2, 26, 53, 75}, ϑ = (1.4, 1, 1.8, 1.2)
and mixed (1.4, −1, 1.8, −1.2); 10 seeds each.
Statistics per run: |S̃₀| vs K; lead_swaps W; swaps after first deletion; additions; final_is_S0; m*/K; k_hit − (ℓ_n + |S̃₀|).
**Would change the theory:** any run with final ≠ S₀ at n ≥ 6·10⁴ with |S̃₀| = K (contradicts PATH); m*/K not tending
to 1; W bounded in n (contradicts NEG); any saturated run where MR1 scores S₀ at n ≥ 6·10⁴.

## R2 — production method (full fit) on exact-Gram CS, MR1 vs cap ℓ_n + 2|S̃₀|
Production core `Scripts/SMC_BVS/core` (v3.1 on main). Data: X with centred columns and XᵀX = (n − 1)Σ exactly
(QR of a centred Gaussian n×p matrix times chol(Σ)·√(n−1)), Σ = (1 − ρ)I + ρ11ᵀ, ρ = 0.5, y = Xβ + N(0,1), β as R1 aligned.
Grid: (n, p) ∈ {(600, 570), (2000, 1900), (4000, 3800)}, 10 seeds; for each data set run (i) default (MR1), (ii) a patched
copy with the LS0 cap ℓ_n + 2|S̃₀| (v3_core.cpp:473 `cap_ll = ls0_ell + 2*m.S.size()`; v3_fit.R:44 `ls0_scans <- b$ell + 2*K + 1`).
Statistics: hpm == S₀; hpm_before_ls0 == S₀; LS0 local_limit; LS0 moves; ls0_improved; runtime.
**Would change the reading:** if hpm == S₀ in (i) always, the MR1 failure is a route failure only (SMC/final search still
discover S₀); if hpm ≠ S₀ in (i) but == S₀ in (ii), the cap change is operationally necessary.

## R3 — iid-row CS designs including p ≫ n (frontier)
Rows iid N(0, Σ), Σ CS ρ = 0.5; (n, p) ∈ {(200, 500), (500, 1000), (1000, 2000), (2000, 1500)}; 10 seeds; truths as R1.
General scorer (bvs_core.Problem on the standardised data; start mode via bvs_core.start_mode with
bvs_core.partition(X); LS0 path via bvs_core.local_search with a large cap, recording the move sequence) — or the
production core with LS0 records. Statistics: |S̃₀| vs K; leading swaps; k_hit vs ℓ_n + |S̃₀|; final == S₀.
**Would change the theory:** whether the NEG mechanism (saturated start + swap phase longer than ℓ_n + s₀) persists for
p ≫ n with random rows (only proved for exact Gram).
