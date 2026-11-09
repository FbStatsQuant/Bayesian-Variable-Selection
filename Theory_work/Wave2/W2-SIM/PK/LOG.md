# W2-SIM family PK — LOG

* 2026-11-09 10:00 — launched (brief briefs/PK.md). Read COMMON, INFRA, PK brief, Wave2 PROTOCOL, W2-FAC-PK STATEMENT/PLAN/
  SIM_REQUEST, pk_core/cs_core/bvs_core/fac_core/n1_scale/n3_robust/pk_selftest, W2-FAC-B REPORT §5.
  Ticket module sha256 (local repo) == NOTS snapshot tickets_20261109T0943.
* 10:05–10:12 — scripts: pk_common.py, r3_iid.py (general scorer, iid rows CS/S5), r1_cs.py (pk_core closed form),
  s5_exact.py (fac_core.ExactGram), validate_general.py, validate_s5_partition.py. Local pilots (Windows, Python 3.13, numpy 2.3.0):
  R3 cs0.5 n=200 p=500 aligned (start 100 = K, W = 5, MR1 scores; 12 s); R1 rho=.5 n=2e4 p/n=.99 (start 37 s, path 47 s;
  W = 429, k_hit 10424 > cap 10016); S5 exact n=600 p=480 mixed (start size 6!, 2 moves).
* 10:13 — validate_general (local): 28/28 small iid cases identical path of sets fac_core.ls0_path vs bvs_core.local_search
  (max |F diff| 1.1e-11). -> results/FAC-PK/validation/.
* 10:14 — NOTS login IP 10.226.96.48 unreachable (timeout); using notsx.crc.rice.edu (other login node), same cluster.
  Uploaded scripts to sim/pk/scripts; submitted pk_pilot01 (job 2633080, 14 tasks, commons, 12 h, 12G).
* 10:16–10:21 — pilot results (EXP=PILOT seeds): validate_general on NOTS 28/28; R3 cs (2000,1500) aligned: start 1000 = K,
  W = 27, k_hit 1024 > MR1 cap 1012 (131 s); (1000,2000): W = 58, MR1 miss; (400,4000): W = 27, MR1 miss (partition 214 s);
  (200,2000): W = 9, MR1 scores; (500,1000) mixed: start 96 < K, MR1 scores. iid paths show isolated swaps after the first
  deletion (not seen in exact Gram). S5 exact (2000,1980) aligned: start 1000 = K, W = 85, MR1 miss. R1 rho=.8 n=6e4 mixed
  59 s. validate_s5_partition: closed form (floor(B/5) groups per block) WRONG for B = 14 & p mod 5 != 0 (3/27);
  fixed to next-fit packing of group sizes (spot-checked locally on the 3 failing cases + 3 others; B = 16 unaffected).
* 10:22 — DESIGN.md v1 (extended grid: R3 280, R1 540, S5 iid 280, S5 exact 180 runs). Design review R01 delegated
  (Codex gpt-6.1-sol high).
* 10:28–10:38 — pilot slow tasks: R1 n=2e5 rho=.5 p/n=.99 aligned: 12.5 min, 1.3 GB, W = 1338, MR1 miss; rho=.2 p/n=.6 mixed
  16.8 min, W = 574; S5 exact (4000,3960) aligned 21.5 min, start 2000 = K, W = 113, MR1 miss. S5 iid (800,8000) > 26 min.
* 10:40 — design review R01 returned GO-WITH-FIXES (6 findings, all accepted; reviews/PK_R01_design.md, PK_R01_disposition.md).
  Fixes: pk_common.trace_general (executed moves, censoring flag, NaN guards, direct re-scoring checkpoints, margins),
  path_record; R1 ties/arrival/limit/NaN; validators exit 1 on disagreement; s5_partition = next-fit packing; summarize.py v2
  (task-table reconciliation, conflicts/missing/provenance, event vs run counts, n-trend slopes). DESIGN.md v2.
  Genuine near-ties found (R1 pilot n=6000: margin 7e-12 between two swap-out nulls) — recorded, not a bug.
* 10:41 — scripts_v2 uploaded (sim/pk/scripts_v2). pk_val01 (job 2634167, scavenge): validate_general 28/28 rc 0.
* 10:43 — production: pk_r3_01 (job 2634250, 280 tasks, commons 12 h, 6G, throttle 15); pk_r1_01 (job 2634251, 540 tasks,
  commons 2 h, 3G, throttle 10). S5 arrays wait for validate_s5_partition (pk_val01 task 2) and free slots.
* 10:47 — pk_val01 task 2: validate_s5_partition 27/27 rc 0 (revised next-fit closed form). Both validations ->
  results/FAC-PK/validation/pk_val01/ (+ manifest).
* 10:55 — submitted pk_s5ex_01 (job 2634683, 180 tasks, commons 4 h, 4G, throttle 15, after R3 job) and pk_s5iid_01
  (job 2634684, 280 tasks, commons 8 h, 8G, throttle 10, after R1 job) — keeps the family at <= 25 concurrent tasks.
  Note: the lead's run_table appends ends.jsonl concurrently; one empty line seen in pk_r3_01 ends.jsonl (harmless;
  summaries reconcile against raw files, not ends.jsonl).
