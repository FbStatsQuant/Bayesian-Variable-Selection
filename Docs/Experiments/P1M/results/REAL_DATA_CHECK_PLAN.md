# REAL_DATA_CHECK_PLAN: riboflavin on the frozen core (input to the run brief; Sonnet planner, 2026-11-18, read-only checks, nothing run or installed)

Scope (owner): RUN riboflavin (hdi `data(riboflavin)`, n = 71, p = 4,088) on `method-v3.1.1-listpip`, on Owls. Background: BRIEFING §451 "real data: supplement only; one dataset, with Astra's stability check"; `W2-APP/EMPIRICAL.md:9` "the project has no real data set"; no SMC-BVS fit on the riboflavin y exists in the repo.

## 1. Where riboflavin is used in the repo (design only, never a fit of y)
- Data file (tracked, public repo): `Theory_work/Wave2/W2-APP/data_diag/downloads/hdi/hdi/data/riboflavin.RData`, md5 `2ea5489eabefbaa5ff1fe91d28b2b509` (re-checked today), object `riboflavin` with `$x` (71 x 4,088, class AsIs, double, column names AADK_at…, no NA) and `$y` (71, range −9.97…−5.67, no NA). Loads without `hdi` (`load()`, then `unclass(x)`). Provenance: `…/data_diag/data/PROVENANCE.txt` (hdi 0.1-10 CRAN-Archive tarball md5 `e7cf1f703e575b5ac3acfdef79b2aa84`; hdi was archived 2026-07-10).
- Design diagnostics and the one plug-in on the real y (5-step OMP; labelled "not verification"): `Theory_work/Wave2/W2-APP/data_diag/{diag_riboflavin.R,out_riboflavin*.txt,SUMMARY.md §2}`; the partition our core computes on this X: **B = 8, 683 blocks, 99.5% of strong pairs split across blocks** (`out_riboflavin.txt` (e)). Check: the new fit must report the same 683 blocks (a real "matches earlier numbers" test).
- Semi-synthetic use (real X, planted truth): `Theory_work/Wave2/W2-SIM/X/` (x_R1, `data/riboflavin_L.csv`); W3-AUDIT track C used the factor `riboflavin_L.csv` (`NOTS_HYGIENE_INVENTORY.md` H17). Theory's verdict: a riboflavin-like pervasive-factor design is outside the proved scope (`Theory_work/Wave3/HQ_DECISIONS.md:691`), so report the fit descriptively, no theorem claim.

## 2. Is `hdi` on Owls?
`Rscript -e 'requireNamespace("hdi")'` → **FALSE** (R 4.6.0, user lib `~/R/x86_64-redhat-linux-gnu-library/4.6`). Not installed, per instruction. Not needed: use the tracked RData above. `digest` and `Rcpp` (needed by the core) are installed; `glmnet` is not.

## 3. Calling the frozen core
- The local checkout's `Scripts/SMC_BVS/core` is OLDER than the tag (tag is on `origin/main`, not in the local `main`): extract the tag, do not use the working tree. `git archive method-v3.1.1-listpip Scripts/SMC_BVS/core | tar -x -C <scratch dir>` (as the rerun2400 bundle did), then verify the tree against `source_manifest.json`.
- Entry (`core/v3_fit.R:73`, pattern of `tests/list_pip_ab/ab_run.R` at the tag): `source("<dir>/Scripts/SMC_BVS/core/v3.R")` (compiles C++ into a `.cpp_cache` inside that dir; needs gcc, Rcpp, digest), then
  `fit <- v3_fit(X, y, seed, allocation = list(mem_gb = M, hours = H))`; `ls0` stays at its default TRUE (the frozen method). `X = unclass(riboflavin$x)`, `y = riboflavin$y`; seed an integer in [1, 2^31 − 1]. `saveRDS(fit, …)`. No other arguments exist.
- Allocation is the only free choice and it is an admission test plus a hard stop: the preflight charges the LS0 worst case, and on Owls at p = 1000 it already tripped the PROD-H allocation (A/B reran those units with `hours = 48`, `LIST_PIP.md`). At p = 4,088 expect the charge to be larger (STUDY_RERUN_PLAN §5 scaled ≈ 94 h at n = 200; less at n = 71; UNMEASURED). Use `mem_gb = 4`, `hours = 120` for the first attempt; a `resource_limit` returned in seconds means the projection exceeds `hours` (read the record, raise `hours`; do not change any other setting).
- Branch: exact branch needs ΣC(p,k≤35) ≤ (5·H0 + 4·N0)·p: impossible at p = 4,088, so SMC. K = min(p, ⌊n/2⌋) = 35.
- Outputs to read: `status`, `log_Z`, `log_Z_r`, `hpm`, `hpm_F`, `pip_primary` (named by gene), `pip_r`, `mpm`, `diag` (escalated, grid_unconverged, cut_group, local_certified), `peak_memory_kb`, `runtime_s`; list fields `pip_list`, `mpm_list`, `log_Z_list`, `list_size`, `list_full`, `pip_list_source`, `pip_list_flag` (README at the tag, lines 64–68).

## 4. Expected runtime and memory (EXTRAPOLATED; no measurement at n = 71, p = 4,088)
- Measured basis (v3.1 on NOTS SPR, n = 200, 1 core): PROD-H new side mean 723 s (p = 500), 1,807 s (p = 1,000), max 4,874 s; peak RSS ≤ 393 MB (`rerun2400/verdict/per_fit.csv`). Power law p500→p1000 ≈ p^1.6 gives ≈ 5 h at p = 4,088 if no escalation.
- W3-SCALE v3-core runs at p = 5k (n not verified here): 12.2 h (profile fit, `NOTS_FACTS.md`) and 15.5 h (B3, 1.22 GB RSS); escalation certain at p ≥ 5k, E2 fires at 5k, `grid_unconverged` only at ≥ 10k (`REQUESTS.md` R6). p = 4,088 sits just below that boundary.
- **Planning figure: 1 core, ≈ 5–25 h per fit (central ≈ 10 h), unloaded NOTS-equivalent; Owls was load ≈ 31 today and ran ≈ 1.2–1.5× slower than NOTS, so ≈ 7–35 h.** Memory ≈ 0.5–1.3 GB (Gram p² doubles = 134 MB); request 4 GB. Three seeds in parallel = 3 cores (≤ 16 allowed), `nice -n 19`, detached, wall = the slowest.
- Cross-machine caution: Owls is R 4.6.0, the campaign NOTS builds R 4.5.2 / GCC 14.3; bit-identity with NOTS is not claimed. Seed-to-seed and rerun-on-Owls checks are valid.

## 5. Published comparison sources (VERIFIED by web search 2026-11-18; no gene list is quoted here)
- Bühlmann, P., Kalisch, M. and Meier, L. (2014), High-dimensional statistics with a view toward applications in biology, Annu. Rev. Stat. Appl. 1, 255–278: introduces the data (provided by DSM; response = log riboflavin production rate of B. subtilis, 4,088 gene-expression predictors, n = 71) — [stat.ethz.ch preprint](https://stat.ethz.ch/Manuscripts/buhlmann/paper-AnnRev.pdf).
- Meinshausen, N. and Bühlmann, P. (2010), Stability selection, J. R. Stat. Soc. B 72(4), 417–473, doi:10.1111/j.1467-9868.2010.00740.x — the stability-selection method the stability check can follow.
- Dezeure, R., Bühlmann, P., Meier, L. and Meinshausen, N. (2015), High-dimensional inference: confidence intervals, p-values and R-software hdi, Statist. Sci. 30(4), 533–558, doi:10.1214/15-STS527 — the package that ships the data; has the multi-split and lasso-projection analyses of it — [arXiv:1408.4026](https://arxiv.org/abs/1408.4026).
- NOT verified (a search snippet only; fetch before citing): Javanmard and Montanari (2014) reanalysis of the same data. The run agent must read the selected genes and thresholds from these papers; I did not.
- In-repo plug-in for orientation only: OMP picks XHLA_at, YXLG_at, YOAB_at, ARGF_at, YHDZ_at (`out_riboflavin.txt` (f)); it is not a published number.

## 6. What "check" should mean (pre-register before the run)
1. Runs clean: `status` completed (not `resource_limit`/`invalid_input`), finite `log_Z`, no NA in the legacy or list fields; record the `diag` flags as found.
2. Sane outputs: 683 blocks; PIPs in [0, 1]; |HPM| ≤ 35; `mpm` and `mpm_list` read against `pip_primary`/`pip_list`; list fields present, `list_full`/`list_size` recorded.
3. Reproducible: 3–5 method seeds on the same data (HPM, MPM, max|ΔPIP|, sd of `log_Z_r`); same seed twice on Owls bit-identical.
4. Literature: report the overlap with the published analyses qualitatively; no published SMC-BVS number exists to match.
Output: `Docs/Experiments/P1M/results/REAL_DATA_CHECK.md`; records under `~/SMC_Engineering_Department/records/realdata/`.
