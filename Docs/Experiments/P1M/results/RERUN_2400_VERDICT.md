# RERUN_2400 verdict: v2.2.1 vs frozen v3.1 on a subset of the p ≫ n 2,400-fit study (2026-11-18)

**NO REGRESSION.** HQ accepted it 2026-11-18. It is a sign-off condition for the method freeze, together with IMPL-LIST.

- **Design** (plan: `../RERUN_2400_PLAN.md`, manager decision): PROD-H, n = 200, p ∈ {500, 1000} × S1–S6 × c ∈ {1, 0.5} × r ∈ {1, 25, 50, 75, 100} plus the known stop `p0500_S5_r088_c100`. That is 121 datasets×scales, each fitted by OLD = v2.2.1 (its own tree and study layer, manifest-verified) and NEW = v3.1 (core tree 8ff2d876 = tag `method-v3.1-listpip`, e9bac478). Original seeds and allocations; both sides of a pair ran in one task on the same NOTS SPR node.
- **Run:** rr2400_20261118T0636Z; precompile 2773942, arrays 2773943 (p1000, 30 tasks) + 2773944 (p500, 31 tasks), ≤ 40 at once; 00:36 → 03:50 CST; **86.3 elapsed core-h** (172.6 billed) of the 120 cap.

| check | result | band |
|---|---|---|
| legacy fields identical() on both-completed pairs (log_Z, log_Z_r, hpm, hpm_F, pip_primary, pip_r, status) | **120/120**, 0 differences | identical |
| X/y SHA-256 match | 121/121 | match |
| completed → stopped | **0** (the known stop stopped on both: 6,300 / 6,299 s) | 0 |
| LS0 HPM gains (disclosed) | 0 | — |
| runtime median ratio new/old per p × c | 0.985 / 0.972 (p500 c100/c050), 0.961 / 0.975 (p1000); worst cell 1.02 | ≤ 1.25 |
| pooled paired-median ratio per p | 0.975 (p500), 0.978 (p1000) | ≤ 1.10 |
| peak RSS ratio | 1.00–1.06 (max 393 MB) | ≤ 1.2 |

**Not affected by v3.1.1:** the coming guard (`v3_fit.R:176`, list fields only on completed final runs) changes only stopped fits' list fields, which this comparison never reads.

**Files:** `../rerun2400/verdict/{verdict.md, verdict.csv, verdict_pooled_p.csv, per_fit.csv}`; the full records (406 MB, 242 checksum files, 0 bad) are on Owls at `~/SMC_Engineering_Department/records/rerun2400/rr2400_20261118T0636Z/`; the run log is `../rerun2400/RUN_LOG.md`.
