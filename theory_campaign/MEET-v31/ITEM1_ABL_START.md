# MEET-v31 · Item 1 closed: start ablation (ABL-START) read against the agreed rule

Chair record, 2026-11-03, about 23:00 UTC.

## 1. What was run

- **Arms.** Arm A is the production v3 block start. It is bitwise identical to production on p0500_S1_r001_c100 (SYNTH_R2 §0.3). Arm B is singleton factors × the capped size prior. Arm C is the capped prior start. Arm D (backfit) was dropped as v2 evidence only. The kernel B, the neighbour graph and the budgets are the production ones.
- **Designs and seeds.** 12 study designs at p = 500 (S1–S6 × {r001 c100, r002 c050}), one seed each (the study's method seed).
- **Scripts.** ABL-START's own scripts (`origin/theory/ABL-START:theory_campaign/ABL-START/scripts/`). The chair's copy of the summary script only changes the output path (`evidence/item1_scripts/summarise_chair.R`).
- **Compute.** Owls, through `owls_run -j 2`.
- **Run history.**
  1. HQ's ABL-START run produced 9 fits before its jobs were SIGTERMed.
  2. The chair relaunched the remaining fits twice. The first relaunch was killed by the T3 server restart.
  3. The second relaunch used detached jobs.
- **Outputs.**
  - Per-fit table: `evidence/item1_per_fit.csv`.
  - Rule table: `evidence/item1_rule_table.csv`.
  - Rule script: `evidence/item1_scripts/apply_rule.py`, committed in f53d0af before any arm-C or S4/S5 result was read.

**Completion.** 33 of the 36 A–C fits completed, and A, B and C all completed on 9 designs. Three arm-B fits did not complete:
- S4 r001 c100 and S4 r002 c050 were still running after more than 4 h of CPU each. They are left running, and their result is an HQ reporting action.
- S3 r001 c100 was stopped by the chair after 3 h 06 min of CPU. This freed an Owls slot for the summary, since `owls_run` refuses a fourth job.

For comparison, arm A took 10–28 min on the same three designs.

## 2. The agreed rule, applied

The rule is SYNTH_R2 §2 with the R3-6 conventions, accepted by all three seats. Under it, a design is **inconclusive** if any of A, B or C has no complete output, or if the three arms' log Ẑ differ by more than 1 nat (B's R3 convention, implemented in the script).

| | count |
|---|---|
| designs | 12 |
| complete for A, B and C | 9 |
| conclusive | **0** |

All 9 complete designs are inconclusive by the > 1 nat clause. In every case it is **arm C** whose log Ẑ is far from A and B (table below).

**Outcome under the pre-registered rule: Outcome 2. Keep the block start, reframed. The paper makes no depth or speed claim for the block start.** The start is justified as the exactly computable local step that carries the theorems (S1/S2), plus the parallel table stage. The method decision is the same under every outcome: the block start ships (all three seats, R1 to R3). No outcome reopens item 1 (R3-6, all three).

## 3. Descriptive results

These are reported, not decided on. The rule never compared A and B head to head, because the arm-C clause made every design inconclusive. That is a limitation of the rule as written, recorded here.

| design | log Ẑ A / B / C | island SD A / B / C | T A / B / C | rebuilds A / B / C | tier A / B / C | seconds A / B / C |
|---|---|---|---|---|---|---|
| S1 r001 c100 | −69.59 / −69.55 / −82.88 | 0.07 / 0.06 / 5.16 | 26 / 25 / 33 | 2 / 3 / 3 | 0 / 0 / 1 | 568 / 610 / 2,635 |
| S1 r002 c050 | −206.42 / −206.41 / −209.71 | 0.02 / 0.04 / 0.94 | 35 / 36 / 37 | 2 / 3 / 3 | 0 / 0 / 1 | 756 / 858 / 3,150 |
| S2 r001 c100 | −85.02 / −85.00 / −96.34 | 0.06 / 0.03 / 0.45 | 31 / 33 / 32 | 4 / 4 / 3 | 0 / 0 / 1 | 810 / 1,053 / 2,856 |
| S2 r002 c050 | −228.52 / −228.64 / −232.64 | 0.08 / 0.10 / 0.31 | 30 / 31 / 28 | 2 / 3 / 3 | 0 / 0 / 1 | 556 / 672 / 1,967 |
| S3 r001 c100 | −72.13 / — / −79.76 | 0.02 / — / 0.94 | 28 / — / 33 | 3 / — / 3 | 0 / — / 1 | 594 / > 11,000 (stopped) / 2,973 |
| S3 r002 c050 | −188.49 / −188.51 / −191.18 | 0.09 / 0.04 / 1.04 | 28 / 33 / 30 | 5 / 7 / 2 | 0 / 0 / 0 | 898 / 1,542 / 754 |
| S4 r001 c100 | −65.80 / — / −75.47 | 0.07 / — / 2.68 | 33 / — / 32 | 8 / — / 3 | 0 / — / 1 | 1,696 / > 14,000 (running) / 2,930 |
| S4 r002 c050 | −193.10 / — / −193.16 | 0.06 / — / 0.47 | 32 / — / 33 | 5 / — / 3 | 0 / — / 1 | 1,115 / > 14,000 (running) / 3,244 |
| S5 r001 c100 | −105.36 / −105.52 / −112.07 | 0.17 / 0.11 / 0.46 | 35 / 43 / 31 | 5 / 5 / 3 | 0 / 0 / 1 | 1,072 / 1,603 / 3,031 |
| S5 r002 c050 | −225.81 / −226.05 / −229.51 | 0.72 / 0.06 / 1.11 | 35 / 34 / 30 | 7 / 7 / 2 | 0 / 0 / 0 | 1,178 / 1,127 / 770 |
| S6 r001 c100 | −85.44 / −85.51 / −92.43 | 0.10 / 0.03 / 0.80 | 34 / 57 / 32 | 3 / 4 / 3 | 0 / 0 / 1 | 825 / 3,796 / 3,227 |
| S6 r002 c050 | −187.01 / −187.05 / −189.58 | 0.09 / 0.02 / 0.62 | 30 / 40 / 29 | 4 / 8 / 2 | 0 / 0 / 0 | 922 / 2,979 / 740 |

All 33 completed fits returned the best-known mode as the HPM (`hpm_eq_best` TRUE in 33/33). As agreed, HPM counts do not discriminate the arms.

**Prior start (C) vs block start (A).**
- Arm C's log Ẑ is below arm A's on 12/12 designs, by 0.06 to 13.3 nats. The gap exceeds 2.5 nats on 11/12.
- Arm C's island spread is 1.5 to 74 times arm A's (median about 8×).
- Arm C escalated to tier 1 (4× budgets) on 9/12 designs; arm A escalated on none.
- Arm C's wall time is larger on 9/12 designs. On the 3 designs where C stayed at tier 0, it was faster but still 2.6 to 3.7 nats low.

Because Ẑ is unbiased, a low log Ẑ with large island spread is the masked-crossing underestimation mechanism (E1/E2, PC1 claim 4). Read descriptively, arm C is clearly worse on objective 1 (evidence accuracy) at equal declared budgets.

**Singleton start (B) vs block start (A).** On the 9 designs where both finished:
- log Ẑ agrees within 0.02–0.24 nats.
- T_A ≤ T_B on 7/9, rebuilds_A ≤ rebuilds_B on 9/9, and arm A's wall time is shorter on 8/9.
- On the 3 designs where B did not finish in 3–4 h, A took 10–28 min.

Read descriptively, B matches A on accuracy and costs more, sometimes much more. These numbers come from 12 designs with one seed each. They are exploratory and are **not** the pre-registered test.

## 4. What the paper may claim, and what would license more

- **Under the rule (Outcome 2):** the block start is kept as the theorem-bearing local step. The paper makes no depth or speed claim for it from this meeting. The ablation table may be printed as exploratory (12 designs × 1 seed, arm-B fits incomplete on 3 designs).
- **To claim** "the block start lowers cost versus singleton factors at equal accuracy" or "the prior start underestimates the evidence at equal budgets", a confirmatory paired test is needed. It would compare A vs B and A vs C on ≤ 20 seeds with the reference fixed in advance: for example, a long stacked arm-A run, or exact enumeration on a reduced design, rather than the leave-one-arm-out pool that arm C contaminates. That test is an optional **HQ action**. It is **not an open method question**, because the method decision (keep the block start) is the same whatever it shows.
