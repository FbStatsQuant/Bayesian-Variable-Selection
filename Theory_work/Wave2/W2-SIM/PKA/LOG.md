# W2-SIM family PKA — LOG (lead: Claude Opus 5.5)

* 2026-11-09 ~10:02 — read COMMON.md, INFRA.md, briefs/PKA.md, Wave2 PROTOCOL; W2-FAC-PKA STATEMENT/PLAN/LOG/CHECKPOINT/
  GENERAL_ASSUMPTIONS/SINGLETON_TARGET/REPORT, lemmas L0–L2, numerics n1–n4, SIM_REQUEST; R02 adapter findings (F2 empty
  model crash, F3 assert replacements, F5 split truth-in/out tags); FAC-B cs_core/bvs_core/fac_core. Independence rule
  observed (no FAC-PK material opened).
* 10:04 — NOTS: workspace listing; snapshot sha256 of n1 (7512ea90…) and n3 match local at that time; FAC-B cs_core
  matches; bvs_core/fac_core archive bytes differ only by CRLF (content identical modulo \r; checked by diff).
* 10:05 — PKA updated n1_exact_grid.py after the snapshot (now 13983c75…: replace_once asserts + dtype=bool fix);
  a new ticket snapshot `tickets_<ts>_pka` will be uploaded and cited.
* 10:06–10:20 — wrote PKA/scripts/pka_lib.py (imports + validated replacements: partition, start DP), validate.py,
  p1_run.py, p2_run.py. Local validation: V1 partition equal on all 33 cases; V2 start DP bit-identical on 72 cases;
  V3 reference run_path = dense fac_core.ls0_path on 120 cases (40 size-K starts, 343 swaps, 0 ties); V4 singleton
  start = source DP. (Local = Windows, Python 3.12.4, numpy 1.26.4; the record run is on NOTS.)
* 10:20 — local timing: P1 c=.98 n=800/1600/3200: 4/5/10 s per seed; P2 full n=1e4 ≈ 30 s; P2 early n=1e5 ≈ 200 s.
* 10:14–now — NOTS unreachable (ssh timeout to 10.226.96.48 and notsx 10.226.96.47; PC on Rice network 168.5.x).
  Local pilot started (P1 ρ=.5 n ≤ 3200 20 seeds; P2 n=1000 full 20 seeds) labelled LOCAL, for the design review
  only; the record runs will be on NOTS.
* 10:25 — DESIGN.md v1, make_tasks.py, summarise.py written.
* 10:36 — local pilot complete (300 seeds; no tracebacks): results/FAC-PKA/pilot_local/ (+ summary/). Codex
  gpt-6.1-sol (high) design review R01 launched (async) with DESIGN.md + scripts + local pilot. NOTS still unreachable;
  monitor armed. Plan: on NOTS return, run val + pilot (small) while the review runs; large batches only after R01.
