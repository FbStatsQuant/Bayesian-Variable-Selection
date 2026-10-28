# Exact best subset with BIC (methodology benchmark 3)

**Sources.** Hocking & Leslie (1967), *Selection of the best subset in regression analysis*, Technometrics 9(4):531–540
(Sec. 2: the bounding property "the RSS of a subset bounds the RSS of all its sub-subsets", the staged search).
Furnival & Wilson (1974), *Regressions by leaps and bounds*, Technometrics 16(4):499–511 (Sec. 3: the
simultaneous regression/bound tree traversal implemented in `leaps`). Schwarz (1978), *Estimating the dimension of a
model*, Ann. Statist. 6(2):461–464 (the ½ k log n penalty). Methodology, Section "Benchmark methods", item 3.

**Protocol (frozen).** `leaps::regsubsets(method = "exhaustive", intercept = FALSE, nvmax = p = 30, nbest = 1,
really.big = TRUE)` returns, for every size k = 1..30, the support with minimum RSS; the empty model is added with
RSS = y'y. Then `BIC(k) = n log(RSS_k / n) + k log n` is minimised over k = 0..30 (ties to the smaller k). The primary
selection is that support; `beta` is its ordinary-least-squares refit without intercept. No size cap is applied
(`kmax_used = 30`, `full_search = TRUE` recorded), so the methodology's clause on capped searches is void. The true
support size is never used. `seed` and `foldid` are recorded and unused: the method is deterministic.

**Verification inside every fit** (all recorded in `diagnostics$checks`; `converged = FALSE` if any fails):
the RSS of every returned support is recomputed by QR and must agree with leaps' value to 1e-8 relative; sizes 1..6 are
re-solved by an independent exact enumeration of all choose(30, k) supports (`bs_rankone_size_k`, rank-one updates on
X'X); every returned support passes a single-swap optimality check; the RSS path is non-increasing; leaps emitted no
warning or linear-dependence flag. Ties (probability zero under the continuous design) are counted and reported.

**Sensitivities (reported, not benchmarks).** `EBIC_0.5` and `EBIC_1`: `BIC(k) + 2γ log choose(p, k)` on the same path.

**Tests** (`tests.R`): leaps path equals a pure-R brute force at p = 12 (RSS and supports), the rank-one enumeration
equals brute force, the BIC formula and argmin, OLS refit, consistency checks, EBIC sensitivities, empty-model
eligibility, a noise-only response, determinism, invalid inputs.

**Lineage.** `Others/1_Latest_work_cycle1_and_next/heterogeneous_1v1/scripts/benchmarks/best_subset.R` (kmax = 12 with
extension, EBIC and size-oracle rows), reduced here to the methodology's single BIC rule with an uncapped search.
Cost at p = 30: about 7 s per dataset including the verification passes (laptop measurement, S1 r001).
