# Family X — iid rows, general loadings, k ≥ 2 factors, real-data-like covariances (informs W2-FAC-X, W2-FAC-XA, W2-FAC-K2)
Family tag: `X` (RUN_ID prefix `x_`). Concurrency allotment: **30** tasks. Folder `W2-SIM/X/`.

Read: `Theory_work/Wave2/W2-FAC-X/` (STATEMENT.md v3 locked, PLAN.md, LOG.md, numerics/: iid_core.py, n1x_iid_cs.py,
n2x_loadings.py, n3x_softgap.py, n5x_start.py, N1X/N2X summaries, T2/), `W2-FAC-XA/` (STATEMENT.md, PLAN.md, LOG.md,
numerics/N1/N2 scripts + summaries), `W2-FAC-K2/` if it exists, `W2-FAC-B/REPORT.md` §5(c),(d), `W2-FAC-A/REPORT.md`,
`W2-APP/REPORT.md` and `W2-APP/data_diag/` (riboflavin, FRED-MD/QD diagnostics: eigenvalues, blocks; data files).

## Questions (state the claim each informs)
1. **iid-row CS beyond the proof's range** (FAC-X Theorem FAC-CS-iid assumes limsup log p/log n < 1/2; FAC-XA seeks
   a < 1/4 first): uncapped LS0 path from the start mode, n increasing (up to 1e6–1e8 via the exact sufficient-statistic
   simulation of iid_core, validated), log p/log n ∈ {0.3, 0.5, 0.75, 0.9} and p ≤ n/2: pure deletion? ends at S₀? band
   width vs ϖ_n = √(p log n / n)·H̄ scaling; gap-invariant violations (kept nulls inside (a_T, b_T); deleted nulls outside
   the 4.3ϖ band — FAC-X (C2)(iii)); centre trajectory x_T; worst addition margin in units of log n.
2. **one factor, unequal loadings** (FAC-X T2, FAC-XA C2): exact Gram (p ≤ n − 1) and iid rows; loadings from a finite set
   and from a continuous interval in (0, 1); n increasing, p ≤ n/2; same path statistics, plus whether the start mode is
   the near-full model S* and whether XA's visibility constant c₀ (min |c(U, j)|) is bounded away from 0 for the designs used.
3. **k = 2, 3 factors** (W2-FAC-K2; multi-class exchangeable first, then generic loadings): start mode, path, S₀ reached.
4. **real-data-like covariances**: Σ = the sample correlation of riboflavin (p = 4088, n = 71) and FRED-MD/QD (from
   data_diag) or a shrunk/regularised version (state it), with iid Gaussian rows at increasing n and p ≤ n/2 (subsample
   columns if needed; state how): start-mode size, path, S₀ reached; which regime (local / factor / mixed) the path looks like.
5. **does the production method recover S₀** (questions 1–4 at moderate n, e.g. n ∈ {500, 2000, 8000}, p ≤ n/2):
   copy `W2-SIM/scripts/prod_fit.R` into your scripts dir (record sha256), add the designs you need (do not change the
   fit call or recorded fields), run v3_fit with an allocation large enough for the preflight (record preflight estimates),
   10 seeds per cell. Record HPM = S₀ rate, hpm_before_ls0 = S₀, LS0 moves vs cap, first scoring scan. Pilot one fit per
   cell first and report runtimes; drop cells that cannot finish within 24 h (state exactly which).
Prioritise 1 → 2 → 5 → 3 → 4 unless a running ticket asks otherwise (check their LOG.md for open numerics questions).
