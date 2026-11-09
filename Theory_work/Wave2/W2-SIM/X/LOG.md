# W2-SIM family X — LOG

* 2026-11-09 10:00 — start. Read COMMON.md, INFRA.md, briefs/X.md, Wave2 PROTOCOL, FAC-X (STATEMENT v3, PLAN, LOG,
  CHECKPOINT, numerics: iid_core, n1x, n2x, n5x, N1X/N2X summaries), FAC-XA (STATEMENT, PLAN, LOG, N1/N2/N5 summaries),
  FAC-B REPORT §5, APP data_diag (riboflavin, FRED-MD/QD). No W2-FAC-K2 folder exists yet.
* 10:02 — W2-SIM lead steer: FAC-X SIM_REQUEST (items A, B, C) = priority 1; results to results/FAC-X/.
* 10:05 — deployed ticket snapshot tickets_20261109T0943: sha256 of iid_core.py, bvs_core.py, n1x, n2x, n5x identical
  to the repo working tree → no new snapshot needed; x_paths.py imports them unchanged via $TICKETS.
* 10:08 — x_paths.py written (driver + replay diagnostics with the exact reference centre). Local smoke (scratchpad):
  n = 1e4, p = 200, ρ = 0.3: production start mode has 125/200 and 129/200 variables (≠ [p] ∖ N₀; ~half of every block
  kept), paths from it are pure deletions ending at S₀. Theory-relevant (C1 at finite n, A = 0.58): kept seeds 0, 1 of
  cell (A, ρ 0.3, n 1e4, p 200) — recomputed in the main grid.
* 10:09–10:13 — `ssh nots` (HostName 10.226.96.48 = loginx?) timed out; nots.rice.edu works → all NOTS commands use
  `-o HostName=nots.rice.edu` (ssh config untouched). NOTS home quota full (10076M/10240M; usage in ~/.vscode-server,
  ~/.codex, not ours): `mkdir runs/x_pilot01` failed (an empty /scratch/fb31/theory_w2/x_pilot01 was created by the
  failed submit and removed; RUN_ID x_pilot01 never ran). Workaround: X/nots/submit_table_x.sh = sim/submit_table.sh
  with RUN_DIR → /scratch/fb31/theory_w2/fam_X/runs/RUN_ID (only change). Scripts/configs in /scratch/fb31/theory_w2/fam_X/.
  **For the W2-SIM lead: home quota is full; other families' submits will fail the same way.**
* 10:15 — pilot x_pilot02 (job 2633071, 7 tasks, seed 900). Timings: [p]-path 13 s at p = 1000, ~100 s at p = 2000
  (cubic), start mode 6 s / 31 s. Pilot event (kept): A cell ρ 0.3, n 1e4, p 1000, seed 900: start mode 565/1000; path
  from it has 2 null swaps and a positive addition gain (+0.028 log n) at a visited set; ends at S₀. Path from [p]: pure.
* 10:21 — design review X_R01 (Codex gpt-6.1-sol high) launched (DESIGN.md + scripts + pilot).
* 10:22 — item C production pilots: x_Cpilot_a (job 2633122; iidcs n 2e4 p 2000 ρ .3 rep 1 mr1 hours 22) and
  x_Cpilot_b (job 2633123; n 5e4 p 5000). prod_fit.R copied to X/scripts_prod (sha256 a32a764d…bfe87e7071ebdf = lead's).
* 10:25 — Q4 data: scripts/make_real_lambda.R → data/<name>_L.csv: Σ_δ = 0.9 R + 0.1 I = LLᵀ + 0.1 I exactly (k = rank R:
  riboflavin 70, fred_md 99, fred_qd 170). Q3/Q4 driver scripts/x_paths_k.py (same ticket modules; no 1-factor
  diagnostics). Local smoke: k3glob, fred_md, riboflavin(p 200) all pure deletion to S₀.
* 10:29 — pilot x_pilot_k01 (job 2633379, 4 tasks, seed 900): k2glob, k3gen, riboflavin p 4088, fred_qd.
  fred_qd n 1e3: start mode 40/170, both paths pure deletion → S₀.
* 10:30 — x_Cpilot_a (job 2633122): status resource_limit after 423 s: preflight LS0 worst case 7.6e9 s
  (2016 scans, 1.88 s/score, est 11.0 GB) vs allocation 22 h → item C at (2e4, 2000) infeasible by the method's own
  preflight. x_Cpilot_b (5e4, 5000) left to finish (expected the same).
* 10:31 — x_Q5pilot01 (job 2633620, 8 tasks, rep 900): production iidcs ρ .5 at (500; 50, 100, 250), (2000; 100, 300,
  1000), (8000; 100, 300) to map the feasible frontier for brief Q5.
* 10:38 — X_R01 received: SOUND-WITH-CHANGES (5 MAJOR, 5 MINOR). Saved verbatim reviews/X_R01_design.md; all applied
  (reviews/X_R01_disposition.md): x_paths.py v2 (b099783a…), x_paths_k.py (49a9bb22…), summarize.py v2 (6525ba45…),
  gen_grid.py v2 (f7919561…). DESIGN.md v2.
* 10:40 — batch 1 submitted: x_A1 (job 2634090, 118 tasks, throttle 12), x_B1 (job 2634114, 42 tasks, throttle 6),
  x_BS1 (job 2634116, 8 tasks, throttle 2). Pilot timing: [p]-path 894 s at p = 4000 (x_pilot02 task 4).
  x_Q5pilot01 task 1 (p 50) failed rc 1: prod_fit.R requires p ≥ 76 (S₀ index 76) — design error of this pilot, not
  a method failure; task 6 (n 2000, p 1000): resource_limit after 36 s (preflight).
