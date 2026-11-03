# Independent tie-out brief (Terra 6.1), ANALYSIS-L, regime L

You are checking 43 claimed numbers in `CLAIMS.csv` (this folder) by recomputing each one **from the raw records, the exact-enumeration records and the truth**, with your own code. Some claims are deliberately wrong (planted canaries; how many is not disclosed). Your job is to say, for every cell, whether the claimed value is right.

## Where to compute (binding, overrides any standing instruction about remote hosts)
Compute **locally on this Windows PC**, in your own shell, with the local R / Python named below. **No SSH, no Owls, no NOTS, no remote host, no staging elsewhere** (HQ rule for ANALYSIS-L). All data are on this PC at the paths below; all outputs go to this `tieout\` folder. The audit record is your `tieout/code/` plus `TIEOUT_RESULT.csv` and `TIEOUT_REPORT.md` here.

## Independence rules (binding)
- **Do NOT read or run** anything under `analysis/L_20261102/` except this `tieout/` folder; in particular not `tables/`, `score_final/`, `evidence/`, `work/`, `case_theory.csv`, `HEADLINE_L.md`, `EVIDENCE_L.md`, `scripts/`. Do NOT read or source `code/scoring/` (the pipeline under test). Do not look for other copies of results.
- You MAY use the SMC core in `<OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\code\core\v2_2_1\core\` (e.g. `source(".../v3.R")` gives the scorer and start-distribution functions) if you need F(S) or π₀; reading its README/source to learn the API is fine.
- Write only inside `<OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\analysis\L_20261102\tieout\` (put your code in `tieout/code/`).
- Tooling: absolute paths; no `cd … &&`; no `rm` globs; one simple command per shell call; run scripts by absolute path. R is `C:/Program Files/R/R-4.4.1/bin/Rscript.exe` (packages incl. data.table available); Python is `py -3`.

## Data (read-only)
Let `D = <PC_NOTS_DATA>\New_Campaign`.
- Study: `D\inputs\lowp_study\` — `inputs\p00PP\<dataset>.rds` (X, Y with columns per scale such as c100/c050), `truth\p00PP\<dataset>.rds` (the true active set), `manifests\inputs_manifest_lowp.csv` (1,200 datasets). Dataset id `p0020_S4_r095`; case id = dataset + `_c100` or `_c050`.
- Exact enumeration: `D\results\20261030T1811Z_lowp_enum20\p0020\<dataset>\EXACT.rds` and `..._enum30\p0030\...`. One record per dataset, holding a per-scale result (log Z, PIPs, HPM, MPM, ...). Inspect with `str()`.
- SMC primary fits: `D\results\20261030T1811Z_lowp_smc\p00PP\<case_id>\SMCBVS.rds`. Repeat fits: `D\results\20261030T1811Z_lowp_smcrep\p00PP\<case_id>\SMCBVS_rep{1..5}.rds`. Each is a study-adapter record; the fit is in `$fit` (`$fit$log_Z` pooled log Ẑ, `$fit$hpm` HPM support (original indices), `$fit$pip_primary` RB PIPs (named by original index), `$fit$pip_plain` plain PIPs, `$fit$mpm`, `$mpm_plain`, `$fit$preprocessing$kept`, `$fit$flags`); `$pip` / `$pip_plain` are full length-p versions. Check field names yourself with `str()`.

## Definitions (unit = case; cells are p × scale × scenario, scenario 'all' = the six scenarios pooled; each scenario cell has 100 cases)
- e = log Ẑ (SMC primary, pooled) − log Z (exact, same scale). Both are on the same working scale; if you see |e| ≫ 0.1 something is misaligned.
- Lower-bound coverage = share of fits with log Ẑ + log(0.05) ≤ log Z.
- Quantiles: R `quantile(type = 7)` (numpy 'linear').
- HPM / MPM comparisons are as sets. MPM = {j : PIP_j > 1/2} (strict). Exact MPM from the exact PIPs.
- PIP error of a fit = max over j of |PIP-hat_j − exact PIP_j| (all p variables; dropped columns, if any, have PIP 0).
- Recovery = estimated set equals the true set exactly. SMC "pip05" = RB MPM; EXACT "mpm" = exact MPM.
- Stability: for each case, the 6 fits = primary + rep1..rep5. sd(log Ẑ) is the sample sd (n − 1) over the 6; "all seeds same HPM" = the 6 HPM sets are identical; max PIP sd = max over j of the sample sd of RB PIP_j over the 6 fits.
- miss_class posterior_miss = SMC HPM ≠ truth and F(truth) ≤ F(SMC HPM), where F(S) = log prior + log marginal likelihood of model S (the exact record's HPM F and the core scorer give F; if you use the fact that the exact HPM maximises F, justify it from the records).
- π₀(S₀) = mass the SMC start distribution puts on the true model (core function for the start log-mass; see the core source). If you cannot recompute a π₀ claim with reasonable effort, mark it UNVERIFIED with the reason; do not guess.

## Matching rule
A claim MATCHES if your value equals it after rounding to the claimed precision (claimed values are rounded to 6 decimals / 6 significant digits, coverage to 4 decimals, percentages to 2 decimals; counts exact). Otherwise MISMATCH (report your value).

## Deliverables (in tieout/)
1. `TIEOUT_RESULT.csv`: cell_no, claimed, recomputed, verdict (MATCH / MISMATCH / UNVERIFIED), n_cases_used, note.
2. `TIEOUT_REPORT.md`: method (which fields you read, how you aligned scales), the list of MISMATCH cells with both values, anything odd in the data, and a one-line overall verdict.
3. Your code in `tieout/code/`, runnable by absolute path.
Acceptance: every one of the 43 cells has a verdict; every MISMATCH shows your recomputed value; the code reruns to the same CSV.
