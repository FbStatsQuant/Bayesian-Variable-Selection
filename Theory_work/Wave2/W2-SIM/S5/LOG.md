# W2-SIM family S5 — LOG

* 2026-11-09 ~10:00 — start. Read W2-SIM briefs COMMON.md, INFRA.md, S5.md; W2-FAC-S5 SIM_REQUEST.md, STATEMENT (v2 LOCKED),
  PLAN, LOG, numerics/bcs_core.py, s3_cc.py, S3_summary.txt; KL_attempt_sol imbalance definition (sign sum over kept nulls).
  Ticket snapshot on NOTS (tickets_20261109T0943) sha256 of bcs_core.py (b6c0fb53…) and s3_cc.py (2886c060…) = local files.
* 10:03 — S5/scripts/s5cc.py = verbatim copy of s3_cc.py loop + added read-only fields (r_bulk/mid/end in units
  H = sqrt(2 log 2p), centre-only versions, band maxima, imbalance I(m) of sign(tau_{j|T\j}) over retained nulls,
  end trace m <= 30). Validation (S5/validation/validate_s5cc.sh -> val_compare.txt): original 12 fields identical in 6/6
  cases (p 500–2000, n 1e4–1e20, S5 and (3,.2,.6)).
* 10:06 — NOTS login node 10.226.96.48 (ssh alias `nots`) unreachable (ping 100% loss); loginx1 10.226.96.46 /
  loginx2 .47 reachable -> using `ssh -o HostName=10.226.96.46 nots` (same cluster/filesystem/Slurm; config untouched).
* 10:08 — pilot s5_pilot01 (job 2633049, scavenge, 5 tasks): s5cc p=1e4 n=1e12/1e20 seed 1, p=2000 seed 1;
  cost probes time_steps.py p=5e4 (2000 steps), p=2e5 (1000 steps).
* 10:12–10:20 — E-S5CC DESIGN.md, task tables (s5cc_small 380, s5cc_big 100), summarise_cc.py (tested on pilot and
  validation outputs); added bulk-proper fields (r over m >= p/10, m >= sqrt p; fixed-m checkpoints) after the pilot showed
  r_bulk attained at m = 30; re-validated (6/6 identical original fields).
* 10:20 — R01 design review launched (Codex gpt-6.1-sol high, async). Large batch held until verdict.
* 10:20–10:38 — E-S5P drivers: scripts/s5p_exact.py (bcs_core path, s1_path rule; candidate swaps every step for
  p <= 5000, else checkpoints) — validated vs ticket s1_path.py 5/5 identical moves/margins (validation/val_s5p_compare.txt);
  scripts/s5p_iid.py (FAC-X iid_core IidData Bartlett with S5 loadings, complete-scan ls0_path) — law validation vs
  explicit rows p=40 n=80, 2000 reps each, 10 KS tests, min p = 0.12 (validation/val_iid_law.txt). Jump statistics in units
  of H for all events and of d_j only when d_j >= H/4; Dout/d_T restricted likewise (ratioR_*).
  Local cost: iid p=1000 n=2000 97 s (O(p^3)) => p = 1e4 (> 24 h) excluded.
