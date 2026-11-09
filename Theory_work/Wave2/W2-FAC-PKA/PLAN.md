# Plan

1. Read Wave2, Wave1C and Wave1 protocols; FAC-B statement, L1–L5, report and source numerics; APP VN; CAP and production cap implementation.
2. Obtain fresh Claude Personal Opus 5.5 high statement lock before proof work.
3. Numerics first: reuse source scorers read-only without creating bytecode outside this folder. Fixed-ratio exact-Gram grid 1/2<p/n<1; detect infeasible exact-Gram inputs explicitly. Separate population-factor experiments for p/n>1 and growing. At most 20 seeds per experiment. Store scripts, configuration and outputs.
4. Develop one lemma per file, falsify numerically, then obtain fresh cross-family Claude review before downstream use. Prioritize rank frontier, saturated start and swap dynamics. Do not silently replace start-mode selection by an arbitrary size-K set.
5. At key lemma write CHECKPOINT; fresh Claude midpoint gets only statement and proof files; obey CONTINUE/REDIRECT/STOP, stopping and reporting on the latter two.
6. If continuing, exhaustive Claude sweep, fix findings, citation-check script and saved output, council with fresh Claude Opus high and Codex gpt-6.1-sol xhigh; both >=8 and all six gates in one round, maximum three rounds.
7. REPORT with precise clause status, verbatim reviews and evidence, METHOD_REQUIREMENTS and outstanding frontier. Writes only here; no git state changes; no contact with parallel ticket.

## R01 supplement

Key lemma: T2 path bound. CHECKPOINT at that lemma or about three hours, whichever first. Three reviewed failed proof attempts -> STUCK; counterexample to locked target -> stop/report; midpoint REDIRECT/STOP -> stop/report.

Initial n=200,400,800, p/n=.6,.85, two seeds; add .51,.98 boundary diagnostics. Closed-form block tables and scans use cs_core formulas, adapted to actual capped-DP start; self-test against dense fac_core for small cases. Population allocation and retained-null signed means must be compared; truth-in swaps separately counted. Larger grids require scalable allocation, not dense DP extrapolation. Iid p>=n experiments use separate generation/scoring. Numerical trends do not decide limits.

Use python -B and disable imported bytecode. Scientific interpreter C:/Users/felip/anaconda3/python.exe; default Python315 lacks NumPy.
