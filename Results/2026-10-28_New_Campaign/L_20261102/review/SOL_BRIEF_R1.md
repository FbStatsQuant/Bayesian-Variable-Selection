# Sol review R1: ANALYSIS-L (regime L headline + theory evidence)

Campaign root: `<OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign` (CAMP). Analysis folder: `CAMP\analysis\L_20261102` (AL). HQ D53: at most two full review rounds, so make this one count.

## What Felipe asked (CAMP\CHARTER.md §1, low-p scope; D22)
Q1 Ẑ accuracy vs exact (bias, RMSE, median and 90th-percentile |e|, 0.05·Ẑ lower-bound coverage; per p × scenario × c and pooled); Q2 HPM (% SMC HPM = exact HPM, % exact HPM = truth, % SMC HPM = truth); Q3 PIPs, RB and plain (mean and 90th percentile of the per-fit max |PIP − exact PIP|, % MPM = exact MPM); Q4 exact recovery per scenario /100 and pooled /600 for SMC-BVS (HPM, PIP > 0.5) and exact enumeration (HPM, MPM); benchmarks later (lasso family `ebic1_K37` headline, CV as sensitivity, D35/D42; MCP and ABESS `ebic1_K37`). Plus repeat-seed stability, reconciliation, availability, and theory measures (π₀(S₀), π₀(R_d), scored-set coverage, truth-first phase/mechanism, T37 TD audit d = 1, 2 literal and toward, miss class) summarised per CAMP\THEORY_EXTRACTION_STRATEGY.md.

## What to review
1. `AL\HEADLINE_L.md` (Felipe-facing; must be plain, short, correct, with correct denominators) and `AL\tables\*.csv`.
2. `AL\EVIDENCE_L.md`, `AL\case_theory.csv`, `AL\evidence\*.csv`: are the verdicts (support / contradict / silent) justified by the numbers; any overclaiming.
3. Code and provenance:
   - Scoring pipeline (frozen, reviewed earlier; review only how it is used): `CAMP\code\scoring\run_scoring.R`, `METRICS.md`, `THEORY_MEASURES.md`.
   - `AL\scripts\run_chunks.sh` (24 chunks × 100 cases via `--cases`), `AL\scripts\merge_chunks.R` (re-aggregates with the pipeline's own functions over the full production roster; theory from pass A, everything else from pass B, rep-0 rows asserted identical), `AL\scripts\build_tables.py` (recomputes every cell from case-level CSVs and asserts equality with pipeline H1–H4; adds overall pooled rows and stability/reconciliation/availability), `AL\scripts\build_theory.py` (written by a Sonnet worker), `AL\scripts\render_headline.py` (all headline numbers come from CSVs).
   - Run evidence: `AL\PROGRESS.md`, `AL\logs\`, `AL\work\passA\out_XX.log`, `AL\work\passB\out_XX.log`, `AL\score_final\SCORING_LOG.txt`, `AL\STUDY_CHECK.txt` (local sealed study = staged PROD-L study).
   - Data provenance: OPS PULL/VERIFIED lines for `20261030T1811Z_lowp_{enum20,enum30,smc,smcrep}` in `CAMP\ops\OPS_LOG.md`. Raw data (read only if you need to spot-check): `<PC_NOTS_DATA>\New_Campaign\results\20261030T1811Z_lowp_*` and `...\inputs\lowp_study\`.
4. Specific questions:
   - Is chunking via `--cases` + re-aggregation equivalent to one production `run_scoring.R` pass (roster, denominators, duplicates, registry, in_expected)? Any way a case could be silently dropped or double counted?
   - Stability is computed over primary + 5 extra seeds (6 fits), whereas the brief said "across the 5 extra seeds". Is that acceptable as reported?
   - Q4: SMC `pip05` row comes from the adapter rows; is it the RB MPM? Are the passing-only counts (2 flagged fits) handled and disclosed correctly?
   - EVIDENCE_L T37: is "toward = sufficient, not necessary" a fair reading of td_vs_outcome? Is the T21 section's claim "posterior error is the whole budget" right?
   - Anything in HEADLINE_L that a reader could misread (e.g., "within about 2% of Z in 90% of fits").

## Rules
Read-only except writing your review to `AL\review\SOL_REVIEW_R1.md`. Tooling: absolute paths, no `cd … &&`, no `rm` globs, one simple command per shell call. R is `C:/Program Files/R/R-4.4.1/bin/Rscript.exe`, Python `py -3`. Do not read `AL\tieout\` (independent tie-out in progress) or anything under the session scratchpad.

## Output format (`AL\review\SOL_REVIEW_R1.md`)
Verdict: ACCEPT / ACCEPT WITH FIXES / REJECT. Then numbered findings, each with class (i) blocking defect, (ii) should-fix, (iii) minor/disclosure; file:line or table cell; evidence; suggested fix.
