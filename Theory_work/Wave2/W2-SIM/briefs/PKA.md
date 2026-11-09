# Family PKA — compound symmetry with p > K (informs W2-FAC-PKA; kept independent of W2-FAC-PK)
Family tag: `PKA` (RUN_ID prefix `pka_`). Concurrency allotment: **25** tasks. Folder `W2-SIM/PKA/`.
**Independence rule (from the ticket):** do not read, use or relay anything from `Theory_work/Wave2/W2-FAC-PK/`,
`W2-SIM/PK/` or `W2-SIM/results/FAC-PK/`. Use only W2-FAC-PKA and W2-FAC-B material.

Read: `Theory_work/Wave2/W2-FAC-PKA/` (STATEMENT.md, PLAN.md, LOG.md, CHECKPOINT.md, lemmas/, numerics/
n1_exact_grid.py, n2_checks.py) and the explicit request **`W2-FAC-PKA/numerics/SIM_REQUEST.md` — follow it exactly**
(Priority 1 and Priority 2; **Priority 3 (production core, population CS p ≥ n) is run by the W2-SIM lead**, not you).
FAC-B scorers: `W2-FAC-B/numerics/cs_core.py, fac_core.py, bvs_core.py`. Output: `W2-SIM/results/FAC-PKA/`
(P1/, P2/) with configuration, code revision (commit 11dc9b7 + ticket snapshot sha256), raw per-seed data and
interpretation.

Key points of the request (the file governs): P1 — exact-Gram CS, p = ⌊c n⌋, c ∈ {.6, .85, .98}, n = 800, 1600, 3200,
6400 then 12800/25600 as practical; ρ = .5 primary, .2/.8 sensitivity; truths (2, 26, 53, 75), coefficients
.5·(1.4, 1, 1.8, 1.2), σ = 1; start = actual capped block DP (not [p], not oracle); save the partition (label the
baseline partition tie-tolerance difference from production); 20 pilot seeds then up to 100, prioritising n-growth;
optimised partition/DP replacements only after validation on small cases (same blocks, scores, mode); per-seed move
records, first SCORING scan (not merely arrival), all cap outcomes for a = ℓ + |start| and a′ = ℓ + 2|start| from one
uncapped path's scan prefix, maximum centre magnitude, first-deletion index, end-of-swap index, swap reappearance.
P2 — singleton blocks (explicitly non-production), s₀ = 1, θ₀ = 1, n up to 1e5–1e6 if O(p) CS scans allow, 20 seeds;
initial swaps / log n, early centre drift, residual Q; plus s₀ = 2, θ = (1, −.1). Do not combine P2 with production-
partition outcomes.
