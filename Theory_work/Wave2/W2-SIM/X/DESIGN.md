# W2-SIM family X — DESIGN (v2, 2026-11-09; v1 reviewed by X_R01 SOUND-WITH-CHANGES, all changes applied — reviews/X_R01_disposition.md)

Lead: family-X lead (Claude Opus 5.5). Scope: brief `briefs/X.md`, re-prioritised by the W2-SIM lead at 10:02 to the
W2-FAC-X request `Theory_work/Wave2/W2-FAC-X/numerics/SIM_REQUEST.md` (items A, B, C), then the rest of the brief.

## Code provenance
* Scorer and path: `iid_core.py` (`IidData`, `PathState`, `ls0_path`) and `bvs_core.py` (`partition_from_corr`,
  `block_size`, `start_mode`) of W2-FAC-X, imported **unchanged** from the deployed ticket snapshot
  `/home/fb31/projects/BVS/theory_w2/code/tickets_20261109T0943/Theory_work/Wave2/W2-FAC-X/numerics/`
  (sha256 iid_core d410eaa9…f521f24, bvs_core e8283f56…e603; identical to the repo working-tree files at 10:05, checked).
  `iid_core` is validated by the ticket (`iid_selftest_out.txt`: incremental gains = direct closed-form scan to ≤ 4.4e-8,
  n ≤ 1e7; Bartlett law check). Every record carries the sha256 of x_paths.py / iid_core.py / bvs_core.py.
* Driver: `X/scripts/x_paths.py` (data draw + seeds, optional production start mode, `ls0_path`, diagnostics by replaying
  the returned move list — the diagnostics cannot affect the path). Grid: `X/scripts/gen_grid.py`.
* NOTS: environment `sim/env_sim.sh` (Python 3.13.5, numpy 2.3.2, scipy 1.16.1, 1 thread). Submission:
  `X/nots/submit_table_x.sh` = `sim/submit_table.sh` with RUN_DIR moved to `/scratch/fb31/theory_w2/fam_X/runs/` (NOTS
  home quota was full at 10:13; diff in LOG). Manifests (sha256 of frozen scripts and tasks) are written there.

## Data model (exact; ticket iid_core)
Raw rows iid N(0, Σ), Σ = ΛΛᵀ + diag(1 − λ_j²) (one factor), y = Xβ + ε, σ = 1, s0 = 4 truths at
idx = linspace(2, p − 3, 4) with raw β = (1.4, −1.0, 1.8, −1.2) (the request's coefficients; same layout as n1x). The
method centres and standardises; the sufficient statistics (XᵀX, Xᵀy, yᵀy) are simulated exactly at any n via the
Bartlett decomposition of the (1 + k + p)-dimensional Wishart (no n × p matrix). CS: λ_j = √ρ.

Seeds: `numpy.random.SeedSequence([20261109, item, round(1000ρ), n, p, load, mode, seed])`, recorded per run
(`seed_entropy`); distinct across cells and items; seeds 0–19 main, 900 pilot.

## Item A — iid CS frontier (informs W2-FAC-X Theorem FAC-CS-iid (C1), (C2); W2-FAC-XA C1)
Claim informed: FAC-X proves (C1) start mode = S* = [p] ∖ N₀ and (C2) pure-deletion path from S*(N) to S₀ with a
band-controlled hole of width 4.3ϖ_n, ϖ_n = C₀H̄√(p log n/n) + n^{−1/3}, for limsup log p/log n < 1/2 (STATEMENT v3,
"PROVED (by this seat, unchecked)" lemmas; review status per FAC-X LOG). The request asks whether A < 1/2 is a
technique limit.
Grid: A = log p/log n ∈ {0.3 (control, inside the proved range), 0.5, 0.6, 0.7, 0.75, 0.8, 0.9};
n ∈ {1e3, 3e3, 1e4, 3e4, 1e5, 3e5, 1e6, 1e7, 1e8}; p = min(round(n^A), n/2), 10 ≤ p ≤ 4500 in batch 1 (larger p in a
batch 2 with fewer seeds, see below); ρ ∈ {0.3, 0.7}; 20 seeds. Per data set two uncapped paths:
(i) from the production start mode S̃₀ (block DP on the production partition, ticket bvs_core), (ii) from [p] (= S*(∅),
the (C2) object with N = ∅).
Recorded per path: move types (pure null deletion?), final == S₀, moves vs MR1 cap ℓ_n + |start|, arrival move,
max addition gain / log n over visited sets, max truth-move gain, max (best null swap − best null deletion), ties,
replay diagnostics in the ξ frame with the **exact** reference centre x_T = (Σ_{T}ξ − ϱ)/(k + κ) (κ = N/(ℓ²φ²),
ϱ = Nη/(ℓφ²), from the Bartlett coordinates; FAC-X §3): excursion of deleted nulls outside (a_T, b_T) (= the (C2)(iii)
band statistic), hull defect, approximate-argmin excess |ξ_j − x_T| − min_kept|ξ_l − x_T| (the (C2)(i) statistic) and
rank, |x_T| trajectory; all distances also / w0 := H̄√(p log n/n) (ϖ without C₀ and the floor). Start mode: size, ==
[p] ∖ N₀ ((C1)), partially selected blocks, log γ0(mode) − log γ0([p] ∖ N₀).
**Theory-changing outcomes:** at fixed A ≥ 0.5, a rate of non-pure-deletion or of final ≠ S₀ (from [p], or from S̃₀)
that does not decrease in n, or additions with positive gain at visited sets from [p]; or excursion/w0 growing with n at
fixed A (the ϖ scaling would be wrong). For (C1): start ≠ [p] ∖ N₀ at a rate not decreasing in n at A = 0.3.

## Item B — fixed-dispersion one-factor loadings, iid rows (informs FAC-X Target 2 (T2/X7), FAC-XA C2)
Loadings: two03_09 (λ alternating 0.3/0.9), two05_095 (0.5/0.95), unif02_09 (λ_j ~ U[0.2, 0.9], fixed per p, n2x
convention). n ∈ {1e5, 1e6}, p ∈ {500, 2000, 5000}, 20 seeds; paths from [p] (and from the production start mode for
p ≤ 2000). Extra statistics: rank of the deleted null in the variable-centre reference statistic
s_j(T) = (ξ_j − ℓ_jX_T)/√(1 − ℓ_j²/(‖ℓ_T‖² + κ′)), X_T = (ℓ_Tᵀξ_T − ϱ′)/(‖ℓ_T‖² + κ′), κ′ = N/φ², ϱ′ = Nη/φ² (exact
whitened reduction, derivation in x_paths.py header; n2x used κ′ ≈ 1), excursion in the s frame overall and per
loading class, common-centre rank (comparison).
**Theory-changing outcomes:** failures of pure deletion / S₀ not vanishing in n; per-class excursion/w0 growing in n.

## Item C — production core end-to-end (optional)
`prod_fit.R` (W2-SIM lead; copied, sha256 recorded) design iidcs at (n, p) = (2e4, 2000), (5e4, 5000): one pilot fit
each first; the lead's own probes (excs n = 200, p = 190) were still running after 17 min, so these cells may be
infeasible; dropped cells will be stated with the measured runtime.

## Statistics (v2)
Units: (cell, seed, path_from), expected set reconstructed from the task tables (missing units listed; cells marked
incomplete). Per cell: k/m and Wilson 95% intervals (both ends) for pure deletion, final = S₀, S₀ scored within the MR1
cap, positive addition gain at a visited set, numerically ok, C1 (mode paths). Band statistics: median / max, raw,
/w0 and /(w0 + n^{−1/3}). Trend at fixed A_target (per ρ and path_from): failures by n; exact-conditional
Cochran–Armitage permutation test in log10 n when ≥ 1 failure; otherwise pooled Wilson upper bound. Detectable effect:
0/20 per cell ⇒ rate ≤ 0.161 (95% Wilson); pooling the n-cells of one A_target (60–180 units) ⇒ ≤ 0.02–0.06. These are
finite-sample statements; a non-detected decline is not evidence of an asymptotic obstruction, and a positive trend
would be evidence, not a proof. No pooling across ρ.
Numerical validity: every run validates incremental gains against a fresh recomputation at the refresh boundaries and
at the endpoint (X_R01 item 5); runs with numerically_ok = False are reported separately as inconclusive.
Scope labels: path from [p] = (C2) with N = ∅; path from S̃₀ = the method's actual LS0 start; oracle path from S*(N₀)
when N₀ ≠ ∅ = (C2) with N = N₀ independently of (C1). The simultaneous-over-N claim is not tested. Item B conclusions
are conditional on the loading arrays and the coefficient/class pairing; sensitivity set x_BS1 (coef=rev, lseed 1, 2).

## Batches
1. x_pilot02 (7 tasks, seed 900): timing (p = 1000: 13 s per [p]-path, 6 s start mode; p = 2000: 133 s).
2. x_A1 (job 2634090; 118 tasks, item A, p ≤ 4500, ~138 CPU-h predicted), x_B1 (job 2634114; 42 tasks), x_BS1 (job
   2634116; 8 tasks), submitted 10:40 after X_R01.
3. x_A2: p ∈ (4500, ~11000] (A = 0.5 at n = 1e8, 0.7 at 3e5, 0.75 at 1e5, 0.8 at 1e5, 0.9 at 3e4), 10 seeds, start
   mode + [p] on seeds 0–2, [p] only on 3–9 (~630 CPU-h predicted: will be trimmed to fit the allotment).
4. x_K1 (brief Q3: k2blk, k2glob, k3glob, k2gen, k3gen; 7 (n, p) pairs; 20 seeds) and x_R1 (brief Q4: riboflavin,
   FRED-MD, FRED-QD shrunk correlations δ = 0.1; n 1e3–1e8, p ≤ n/2, column subsets 200/1000/full), x_paths_k.py.
5. Production core (brief Q5 / item C): x_Q5pilot01 maps the feasible frontier via the method's own preflight.
