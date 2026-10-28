# Bayesian Variable Selection

Local-to-global Bayesian variable selection (SMC-BVS).

## Layout

| Folder | Contents |
|---|---|
| `Scripts/SMC_BVS/` | SMC-BVS v3 (BB(1,p) size prior, HPM selection), version v2.1 |
| `Scripts/SMC_BVS/core/` | Method core: R driver files (`v3.R` entry, `v3_fit.R`, preprocessing, setup, calibration, final run, exact branch) and C++ engine in `cpp/` |
| `Scripts/SMC_BVS/study/` | `adapter.R` and `run_case.R`: run one dataset through the method |
| `Scripts/Benchmarks/<method>/` | Code of each benchmark's final production run (n = 200 study): Lasso, ElasticNet, AdaptiveLasso, MCP_SCAD, ABESS, SuSiE, SSL, Horseshoe |
| `Papers/` | Reference papers |
| `Others/` | Miscellaneous |

Usage of the core:

```r
source("Scripts/SMC_BVS/core/v3.R")
fit <- v3_fit(X, y, seed, allocation = list(mem_gb = 8, hours = 24))
```

Data and simulation outputs are not stored in this repository.
