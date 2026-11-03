# Sol narrow check: pass C benchmark rows only (HQ D92; D53 class (i) check)

AL = `<OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\analysis\L_20261102`. Your earlier reviews (`AL\review\SOL_REVIEW_R1.md`, `SOL_REVIEW_R2.md`) accepted everything except the benchmark rows, which had not landed. This is a **narrow** check of the new rows only. Report class (i) defects (wrong numbers, wrong rule, a denominator error, a broken process); list anything else briefly as (ii)/(iii). Do not re-review the accepted SMC/exact material.

## What changed (pass C)
- **Data.** `<PC_NOTS_DATA>\New_Campaign\results\20261102T2309Z_lowp_benchres` (PROD_L_BENCH rev 2; acceptance report `…\NOTS Data\New_Campaign\runs\20261102T2309Z_lowp_bench\accept\ACCEPT_BENCH.md`; PULL VERIFIED line in `CAMP\ops\OPS_LOG.md`, 2026-11-03T12:45Z; CAMP = `…\02_Experiments\I_2026-10-28_New_Campaign`).
- **Scoring.** `AL\scripts\run_chunks.sh … passC 0` with all five roots, then `AL\scripts\merge_chunks.R` (with the R1 own-chunk filter) into `AL\score_final_bench\`, theory from pass A. Run logs: `AL\logs\passC.log`, `AL\work\passC\out_XX.log`. All non-benchmark CSVs are byte-identical to `AL\score_final\`; `case_selection.csv` and `H4_recovery.csv` differ only by the benchmark rows and dtype formatting.
- **Tables.** `AL\scripts\build_tables.py` → `AL\tables\Q4_recovery.csv`, with a new SMC `mpm_plain` row taken from the accuracy table and cross-checked so the RB MPM equals `pip05`. The pre-benchmark snapshot is `AL\tables_prebench\`.
- **Headline.** `AL\scripts\render_headline.py` → `AL\HEADLINE_L.md`. Short answer 4 and the Q4 section changed; the plain MPM rows were added to the SMC per-scenario table. Diff against `AL\work\HEADLINE_L_prebench.md`.
- **Evidence.** `AL\scripts\render_bench_evidence.py` → the `<!-- BENCH:BEGIN -->…<!-- BENCH:END -->` section appended to `AL\EVIDENCE_L.md` (diff against `AL\work\EVIDENCE_L_prebench.md`).
- **ABESS D54.3 exact size-k check.** `AL\scripts\abess_size_check.R` and `abess_summary.py` → `AL\abess_check\` (`ABESS_CHECK.md`, `abess_size_check.csv`, `abess_size_summary.csv`, `ABESS_LINE.txt`). Is the method right: centred X and yc, no intercept, leaps exhaustive, RSS tolerance, ties allowed? Are the alignment checks adequate?
- **Tie-out.** `AL\tieout_bench\` (brief, 25 claims, Terra's result and report, `CANARY_KEY.json`, `TIEOUT_VERDICT.md`).
- **Tests.** `AL\review\TEST_PASSC_RENDER.txt` (renderer pending/partial/complete consistency).

## Specific questions
1. Are the headline rules right per HQ D92/D35/D42/D17: F1–F3 `ebic1_K37` headline with `cv_min` as sensitivity; F4/F5 `ebic1_K37`; A1 `pip05`, A2 `ssl_final`, A3 `ci95`? Is the p ≤ 30 LA-4 overlay applied as the registry derives it?
2. Denominators: 600 per p × c and 100 per scenario, with failed or not-run results as non-recoveries.
3. Are the flags (SSL above the exact-posterior HPM in 3 cells; lasso/EN CV near 0) reported without overinterpretation?

## Rules and output
Read-only, except your review at `AL\review\SOL_REVIEW_PASSC.md`. Work locally; no SSH or remote host. Tooling: absolute paths, no `cd … &&`, no `rm` globs, one simple command per shell call.

Format: verdict (ACCEPT / ACCEPT WITH FIXES / REJECT), then the class (i) findings, then a brief list of (ii)/(iii).
