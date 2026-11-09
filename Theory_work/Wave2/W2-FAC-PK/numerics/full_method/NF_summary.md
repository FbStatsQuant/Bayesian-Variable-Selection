# NF summary (production SMC-BVS v3.1, LS0 on) — INCOMPLETE: no fit finished

Core: copy of `Scripts/SMC_BVS/core` (no `.cpp_cache`) in the session scratchpad `core_copy`; nothing under `Scripts/` touched.
Driver: `nf_run.R` (one fit per process, args `n p rep [hours]`), `nf_driver.sh` (1200 s `timeout` per fit).
Data: exact-Gram CS design, rho 0.5, checked max|X'X/(n-1) - Sigma| ~ 2e-15 and column means ~ 3e-16 (n=600, p=450, reps 1–2).

| attempt | allocation | (n,p) | reps run | outcome |
|---|---|---|---|---|
| 1 | hours = 2 (ticket value), mem 8 GB | (600,450) | 1, 2, 3 | all `status = "resource_limit"` after 5–7 s, raised by the production **preflight** (`fit$preflight$exceeds = TRUE`); no SMC ran. File: `NF_raw_attempt1_hours2_preflight_resource_limit.jsonl` |
| 2 | hours = 1000 (guard lifted) | (600,450) | 1 | killed by the 1200 s wall-clock timeout (rc 124), no output. Rep 2 was started and then killed by me when I stopped the grid (no record). File: `NF_raw.jsonl` |

Grid stopped after the first timeout, as instructed (fits too slow). (600,570), (1200,1100), (2000,1900) were not run.

Counts per (n,p) (hpm==S0 / hpm_before_ls0==S0 / LS0 local_limit): none available — 0 completed fits at every (n,p).

Preflight at (600,450), rep 1 (hours=2): est_bytes 3.83e8 (memory fine); `preflight$ls0_worst_case`: scans 312, requests 15,935,400,
model_size_timed K = 300, seconds_per_score 0.0166, bookkeeping_factor 2, est_seconds 527,480 (~146.5 h) > 2 h → exceeds.
budgets: ell_n = 11, so the LS0 cap = 11 + |start mode| (K = 300 gives the 312 scans).
