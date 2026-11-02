# A-DRAFT — adversarial novelty and estimator audit

Research date: 2026-11-02. Branch: `theory/A-DRAFT`.

Work in progress. All new mathematical results are candidate results, not locked or adopted.
Status vocabulary: PROVED / PROOF SKETCH / COUNTEREXAMPLE / CONJECTURE / OPEN.

## 1. Novelty audit

OPEN — primary-source audit underway. Song–Liang (2015), Lindsten et al. (2017), and Gutierrez–Guhaniyogi (2022) are absent from `Papers/`; online primary sources are being checked and will be distinguished from repository PDFs.

## 2. Posterior expectations

OPEN — proof will distinguish fixed-data particle limits, actual-budget sample-size limits, and continuous-parameter posterior contraction. Frozen calibration is essential; normalized estimates are not generally unbiased.

## 3. Naive merging

OPEN — the proposed counterexample uses two distinct correlated predictors, a single true signal, and singleton local analyses. Both local inclusions tend to one; the full posterior excludes the proxy. The actual small-p v3 output uses exact enumeration, while a forced SMC component has a separate particle-limit guarantee.
