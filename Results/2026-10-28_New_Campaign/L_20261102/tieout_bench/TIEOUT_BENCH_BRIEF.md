# Independent numbers-only tie-out (benchmark rows, pass C): brief

You are checking the claimed numbers in `CLAIMS_BENCH.csv` (this folder) by recomputing each one from the **raw records and the truth**, with your own code. Some claims are deliberately wrong (planted canaries; how many is not disclosed). For every cell, say whether the claim is right.

## Where to compute (binding; overrides any standing instruction about remote hosts)
Compute **locally on this Windows PC**: R `C:/Program Files/R/R-4.4.1/bin/Rscript.exe` (data.table and leaps are available) or `py -3`. **No SSH, no Owls, no NOTS, no remote staging.**

## Independence rules (binding)
- **Do NOT read** anything under `<OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\analysis\L_20261102\` except this `tieout_bench\` folder. In particular, not `tables\`, `score_final*\`, `work\`, `abess_check\`, `scripts\`, `HEADLINE_L.md`, `EVIDENCE_L.md` or `tieout\`.
- **Do NOT read or source** `…\I_2026-10-28_New_Campaign\code\scoring\` (the scorer under test).
- Write only inside this `tieout_bench\` folder, with your code in `tieout_bench\code\`.
- Tooling: absolute paths; no `cd … &&`; no `rm` globs; one simple command per shell call; run scripts by absolute path.

## Data (read-only)
`D = <PC_NOTS_DATA>\New_Campaign`.
- **Study.** `D\inputs\lowp_study\inputs\p00PP\<dataset>.rds` holds X and Y; Y has one column per scale (`c100`, `c050`). The truth is at `D\inputs\lowp_study\truth\p00PP\<dataset>.rds`; its active set is the true support. The manifest is `D\inputs\lowp_study\manifests\inputs_manifest_lowp.csv` (1,200 datasets: p ∈ {20, 30}, scenarios S1–S6, replicates 1–100). Case id = dataset id + `_c100` or `_c050`.
- **Benchmarks.** `D\results\20261102T2309Z_lowp_benchres\p00PP\<case_id>\<M>.rds`, for M in F1 F2 F3 F4 F5 A1 A2 A3. Each record has `$rows`, a data.frame with one row per rule: `rule_id`, `role`, `status` ("ok" or a failure), and `support` (semicolon-separated original column indices; "" is the empty set). Inspect it with `str()`.
- **SMC primary fits.** `D\results\20261030T1811Z_lowp_smc\p00PP\<case_id>\SMCBVS.rds`. The record's `$pip_plain` is the length-p plain PIP vector; inspect it with `str()`.

## Definitions
- **Recovery** of a (method, rule) in a case: that rule's row has status "ok" and its support equals the true active set exactly, as sets. A missing row, a status other than "ok", or a missing record counts as not recovered.
- **Cells.** A cell is p × scale × scenario (100 cases). Scenario "all" pools the six scenarios of that p × scale (600 cases).
- **SMC `mpm_plain`:** the set {j : plain PIP_j > 1/2} (strict) of the SMC primary fit, compared with the truth.
- **ABESS size cells** (F5, rule `ebic1_K37`). For each case:
  - take X as stored (its columns are already centred) and yc = Y[, scale] − mean(Y[, scale]);
  - let S be the support of the `ebic1_K37` row, and k = |S|;
  - RSS(S) is the residual sum of squares of the no-intercept least-squares fit of yc on X[, S];
  - RSS*_k is the minimum of RSS over **all** supports of size k (exact best subset with no intercept, e.g. `leaps::regsubsets(..., intercept = FALSE, method = "exhaustive")` or full enumeration).

  The case counts if RSS(S) − RSS*_k > 1e-8 · max(1, RSS*_k). The claimed number is the count of such cases among the 600 in the cell.

## Matching rule
All claims are integer counts. MATCH if your count equals the claim exactly; otherwise MISMATCH, and report your value.

## Deliverables (in `tieout_bench\`)
1. `TIEOUT_RESULT.csv`: cell_no, claimed, recomputed, verdict (MATCH / MISMATCH / UNVERIFIED), n_cases_used, note.
2. `TIEOUT_REPORT.md`: method (the fields you read), every MISMATCH with both values, anything odd in the data, and a one-line verdict.
3. Your code in `code\`, runnable by absolute path.

**Acceptance:** every cell has a verdict, and the code reruns to the same CSV.
