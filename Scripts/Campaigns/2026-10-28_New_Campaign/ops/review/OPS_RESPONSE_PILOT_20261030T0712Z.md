# OPS response to Sol review of the LOWP pilot 20261030T0712Z and the PROD-L sizing (2026-10-30)

Review: `SOL_REVIEW_PILOT_20261030T0712Z.md`. Verdicts: (A) pilot accepted **YES WITH CAVEATS**; (B) sizing **ACCEPT WITH FIXES**. No blocking finding.

| # | Finding | Disposition |
|---|---|---|
| 1 | Clean-up acceptance (§10.7) not independently evidenced | **Fixed.** `ops/evidence/ops4_pilot_20261030T0712Z_cleanup.txt` holds the dry-run and `--yes` transcripts copied verbatim from the session (`CLEANUP VERIFIED`, residue search `(none)`, guard OK, exit 0), plus a **retrospective** read-only check at 08:09:22Z (no jobs, no `*20261030T0712Z*` residue at depth 3 in campaign home or scratch, runs/logs/results empty, guard OK at 9.42 GiB). Recommendation for future bundles (LOWP/CONF): add an operational-closure receipt and verdict to the acceptance summary. The historical summary is unchanged. |
| 2 | 8-thread cost used a false 10 s start-up | **Fixed** in sizing §2–§3: the false derivation is removed; 46.7 CPU-h (single-dataset baseline 35.05 s) and 56.7 (42.5 s with an explicit 7.45 s allowance) are shown; the matched saving is ≈ 11 %; 16 threads stays the supported design. |
| 3 | Delay allowance is a scenario, not a rate | **Fixed:** labelled a scenario; Sol's sensitivity cases added (primary 21.6, repeats 19.1 CPU-h); production should log per-fit and per-task wall and CPU. |
| 4 | Conservative arithmetic | **Fixed:** formulas stated for every column; recomputed (SMC 15.9 / 16.2; subtotal 110.0; total 150.6). The summarizer's generic projection is marked as superseded for production sizing. |
| 5 | Per-fit 4 h guard vs batch deadline | **Recorded as a bundle requirement** in sizing §4 (do not start a fit without enough remaining scheduler time; commit units; completion inventory; explicit resubmission). This is for the PROD-L bundle authors (LOWP/CONF via HQ), not an OPS setting. |
| 6 | Combined concurrency and truth-lock coordination | **Fixed** in sizing §4: benchmarks serialized after the SMC/repeat lane; combined ceiling stated (PROD-L ≤ 132 alone, ≤ 68 with PROD-H; proposed H+L ≤ 192 charged CPUs, for HQ to agree); one shared stage before a single truth lock, with the unlock depending on every consumer. |
| 7 | Disk units and repeat sizes | **Fixed:** GiB/KiB labels; repeats sized from repeat records (1.005 GiB); total 3.49 GiB, plan 4 GiB plus reserve; home margin conditional on one shared stage and a fresh guard. |
| 8 | Requested vs allocated ceiling | **Fixed** in sizing §1: 311 requested CPU-h ↔ 472.7 allocated CPU-h; whole-core explanation described as consistent with the topology, not as proof of billing policy. |
