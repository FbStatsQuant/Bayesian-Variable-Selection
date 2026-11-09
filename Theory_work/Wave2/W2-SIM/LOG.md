# W2-SIM — LOG (lead)

* 2026-11-09 09:15–09:43 — read PROTOCOL (Wave2/1C/1), W2-FAC-B REPORT/MR, W2-FAC-PK/PKA/S5/X/XA STATEMENTs, LOC2 REPORT;
  requests received: FAC-PK SIM_REQUEST (R1–R3) + addendum to R2; FAC-S5 SIM_REQUEST (CC scaling); FAC-PKA SIM_REQUEST (P1–P3).
* 09:43 — NOTS workspace created (/home/fb31/projects/BVS/theory_w2, /scratch/fb31/theory_w2). Code deployed:
  code/main_11dc9b7 (git archive of main 11dc9b73416dacb9f159846d39902d4b57b49a57; core = v3.1 merge 4676af6, no diff in
  Scripts/SMC_BVS/core between 4676af6 and 11dc9b7) + code/tickets_20261109T0943 (snapshot of untracked ticket numerics).
  sha256 lists on NOTS. Env: nots/env_sim.sh (production env.sh + SciPy-bundle/2025.07). Runner: nots/run_table.sh,
  nots/submit_table.sh (manifests with sha256 of frozen scripts/tasks).
* 09:46 — smoke01 (job 2632784): task 1 failed by my test-design error (p = 60 < max S₀ index 76; guard added);
  core compiled (.cpp_cache READY 09:46). Task 2 (excs n=100 p=80, dbl) running > 12 min.
* 10:00 — family leads launched via delegate_task (Opus 5.5 high): S5 (claude-personal, 25 slots), PK (Claude Work, 25),
  PKA (Claude Work, 25; independence from PK enforced in brief), X (claude-personal, 30), LOC (claude-personal, 20).
  Lead keeps 25 slots for production-core fits (FAC-PK R2 + addendum, FAC-PKA P3). Briefs: briefs/*.md.
* 10:02 — FAC-X request (numerics/SIM_REQUEST.md: A iid CS paths n≤1e6; B loadings; C optional production) forwarded to family X (steer), output results/FAC-X/.
* 10:58 — loginx3 (10.226.96.48) unreachable from ~10:30; ~/.ssh/config Host nots HostName → nots.rice.edu (backup ~/.ssh/config.bak_w2sim_20261109); works. smoke01 task 2 (excs n=100 p=80, dbl) TIMEOUT at 50 min (scavenge).
