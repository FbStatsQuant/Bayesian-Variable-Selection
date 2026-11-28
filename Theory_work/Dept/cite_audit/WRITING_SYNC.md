# CITE-AUDIT → Writing sync instructions (Section 3)

For: Theory Manager → Writing Manager (Lead 1 / Lead 3). Source: `CITE_AUDIT.md` fixes W1–W9.

- Base: `writing/main` **2682a942** (this already includes the owner terminology ruling commit; the audit itself read 3445496d).
- Patch: [`WRITING_SYNC.patch`](WRITING_SYNC.patch), unified diff for `Docs/Writing/paper_smcbvs/sections/03_theory.tex` and `Docs/Writing/paper_smcbvs/refs.bib`.
  Apply from the repo root with `git apply Theory_work/Dept/cite_audit/WRITING_SYNC.patch` (or `patch -p1`).
- Tested: applied to a clean export of 2682a942 and built with `latexmk -pdf`. Result: exit 0, 0 LaTeX warnings, 0 BibTeX warnings, 45 pp. Both new bib entries resolve.

| fix | anchor text in 03_theory.tex | change |
|---|---|---|
| W1 | "which leads to slower rates" | slower rates attributed to SongLiang2015 only (SBJ state no rates) |
| W2 | "Fixed floors on sparse eigenvalues" | BRT09 / NH14 floors may vanish slowly (1/log n, p^{-κ}); a fixed floor is the special case |
| W3 | "(Condition~4.4) ask the residual signal of every model" | NH14 4.4 is over models with fewer than a fixed multiple of s₀ predictors |
| W4 | "ask its ratio to $\log p$" | Luo–Chen ratio is to $\sz\log p$ |
| W5 | `\citep{Wainwright2009,FletcherRanganGoyal2009}` | → `WainwrightIT2009` (Information-theoretic limits, IEEE TIT 55(12)); the old key = Lasso paper, now unused in Sec. 3 |
| W6 | "their discussion states the converse" | converse is for true predictors among the candidates |
| W7 | "stated there for Gaussian data with omitted predictors" | Gaussian linear model (Gaussian errors, predictors with finite second moments) |
| W8 | "studied by \citet{RossellRubio2018} and \citet{Rossell2022}" | RR18 = misspecified error law, Bayes factors consistent at slower rates; KL-optimal concentration = Rossell 2022 |
| W9 | "By Cram\'er's decomposition theorem" | add `\citep{Cramer1936}` + new refs.bib entry (HQ request) |

New refs.bib entries: `WainwrightIT2009` (DOI 10.1109/TIT.2009.2032816) and `Cramer1936` (DOI 10.1007/BF01180430).
Volume, issue and pages were checked against Crossref and the PDF first pages.
