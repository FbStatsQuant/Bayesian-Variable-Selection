# Family PK — compound symmetry and S5 with p > K = ⌊n/2⌋ (informs W2-FAC-PK)
Family tag: `PK` (RUN_ID prefix `pk_`). Concurrency allotment: **25** tasks. Folder `W2-SIM/PK/`.
Do not read or use anything under `W2-SIM/PKA/` or `W2-SIM/results/FAC-PKA/` (parallel ticket; kept independent).

Read: `Theory_work/Wave2/W2-FAC-PK/` (STATEMENT.md, PLAN.md, LOG.md, lemmas/, numerics/: pk_core.py, cs_core.py,
fac_core.py, bvs_core.py, n1_scale.py, n2_diag.py, n3_robust.py, pk_selftest*), and the explicit request
`W2-FAC-PK/numerics/SIM_REQUEST.md` (R1, R2, R3). `W2-FAC-B/REPORT.md` §5(a), METHOD_REQUIREMENTS.md.
**R2 (production core full fits) is run by the W2-SIM lead, not by you.** You run R1 and R3 and task item 1's
remaining parts. Output: `W2-SIM/results/FAC-PK/` (subfolders R1/, R3/, S5PK/).

## R1 (explicit request) — large-n closed-form exact-Gram CS LS0 paths
As SIM_REQUEST.md: ρ ∈ {0.2, 0.5, 0.8}; p/n ∈ {0.6, 0.8, 0.99}; n ∈ {2e4, 6e4, 2e5} (larger if a validated faster
path allows); truths S₀ = {2, 26, 53, 75}, ϑ = (1.4, 1, 1.8, 1.2) and mixed (1.4, −1, 1.8, −1.2); 10 seeds. Per run:
|S̃₀| vs K; lead swaps W; swaps after first deletion; additions; final == S₀; m*/K; k_hit − (ℓ_n + |S̃₀|). Theory-changing
outcomes listed in the request (final ≠ S₀ at n ≥ 6e4 with |S̃₀| = K; m*/K not → 1; W bounded; MR1 scoring S₀ in a
saturated run at n ≥ 6e4). Time n = 2e4 first; the path is O(K·p) numpy work — if 2e5 is infeasible within 24 h per
task, write a validated sorted-structure path (agreement with pk_core.path_from on ≥ 20 small cases, saved).

## R3 (explicit request) — iid-row CS incl. p ≫ n (frontier of NEG)
Rows iid N(0, Σ), Σ CS ρ = 0.5, (n, p) ∈ {(200, 500), (500, 1000), (1000, 2000), (2000, 1500)}, 10 seeds, truths as
R1 (aligned). General scorer: bvs_core.Problem on the standardised data, start mode bvs_core.start_mode with
bvs_core.partition(X), LS0 path via bvs_core.local_search with a large cap, recording every move. Statistics: |S̃₀| vs K;
leading swaps; first scan whose neighbourhood contains S₀ (scoring) vs arrival; k_hit vs ℓ_n + |S̃₀| and ℓ_n + 2|S̃₀|;
final == S₀. Add p/n ∈ {2.5, 5, 10} at n = 200 and 400 if feasible (task item 1).

## S5PK (task item 1 remainder)
Same statistics for S5 (groups of 5, ρ_b = 0.3, ρ_w = 0.7) with p > K: exact Gram (p ≤ n − 1, p/n ∈ {0.6, 0.8, 0.99},
fac_core general exact-Gram scorer or a validated block-CS closed form; n as large as feasible) and iid rows
(p/n ∈ {1, 2.5, 5, 10}, n = 200, 400, 800 as feasible). Does the NEG mechanism (saturated start + swap phase longer
than ℓ_n + s₀) appear for S5 too? Does the uncapped path end at S₀?
