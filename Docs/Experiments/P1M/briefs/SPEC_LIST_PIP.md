<!-- copy of /home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/SPEC_LIST_PIP.md at theory/W3-AUDIT 523dda23 (HQ order 11-17); the original is binding -->
# SPEC — list-renormalised PIPs and their median model (audit Fable, 2026-11-17; for HQ → Engineering, core v3 and engine v4)

Owner-approved method companion to #5′. **Nothing existing changes:** `pip_primary` (the equal-weight island mean) and
`mpm` stay the primary outputs; the new fields are additional, are computed after everything else, read no random
numbers and alter no state. Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (core last changed at 72785fe).

## 1. The list
𝒯 := the returned top store, `fit$top_store` (`v3_run.R:210`, from `led$top`, `:170`), as exported by `store_to_list`
(`cpp/v3_core.cpp:358-362`): `models` (a list of integer vectors of **original** column indices, `to_orig`), `value`
(the scores F(S) = log ϖ(S) + log m(S), one per model), `capacity` = 40p + 1 (`cpp/v3_ledger.h:78`), `full`. The store
holds distinct models, best first under the HPM order (`cpp/v3_ledger.h:32-56`). Let m = length(models), F_i = value[i].

## 2. Definition
For every retained column j (the names of `pip_primary`, `v3_run.R:160-162`), with F_max := max_i F_i and
u_i := exp(F_i − F_max):

    pip_list[j] := ( Σ_{i : j ∈ models[i]} u_i ) / ( Σ_{i=1}^{m} u_i ),
    mpm_list    := { j : pip_list[j] > 0.5 }   (strict, the rule of `mpm`, `v3_run.R:163`; increasing original indices),
    log_Z_list  := F_max + log( Σ_{i=1}^{m} u_i ).

In words: the posterior over models renormalised to the returned list, its inclusion probabilities, their median
model, and the log of the list's total unnormalised weight (on the scale of the printed `log_Z`).

## 3. Numerical rules
- Log-sum-exp as written: subtract F_max before exponentiating; never exponentiate F_i itself.
- Both sums run over the store **from the last entry to the first** (smallest weights first), in double precision, no
  compensated summation. The result is then deterministic within an implementation.
- Core v3 and engine v4 may differ in the last bits of `exp`; they must agree to 1e−12 in `pip_list` and `log_Z_list`.
- Clamp nothing. By construction 0 ≤ pip_list[j] ≤ 1 up to rounding; a value outside [−1e−12, 1 + 1e−12] is a bug.

## 4. Cases
| Case | Rule |
|---|---|
| Status `completed` (sampler branch) | compute the three fields from `top_store` |
| Status `exact` (enumeration branch, `v3_fit.R:122-127`) | `pip_list := pip_primary`, `mpm_list := mpm` (already exact), `log_Z_list` from the store if it is returned, else NA; `pip_list_source = "exact"` |
| Any other status (`resource_limit`, `invalid_input`, `no_predictors`, `y_constant`, `numerical_failure`, calibration failure; `v3_fit.R:84-158`) | the fields are absent (NULL), also when partial results are returned |
| Single model in the list | `pip_list` is its indicator; `mpm_list` is that model; `log_Z_list` = its score |
| The empty model in the list | it contributes to the denominator only |
| Exact tie, pip_list[j] = 0.5 | j is not in `mpm_list` (strict rule) |
| A column in no listed model / in every listed model | pip_list[j] = 0 / = 1 exactly |
| Empty list (m = 0) on a completed run | must not occur; set the fields to NA, `pip_list_flag = "empty_list"`, and fail the test suite |
| Duplicate models in the list | must not occur (the store is a set); detect and stop with an error, do not merge |
| A non-finite score | −Inf entries get weight 0; NaN or +Inf: fields NA, `pip_list_flag = "nonfinite_score"` |

## 5. Field names
`pip_list` (named numeric vector, same names and order as `pip_primary`), `mpm_list` (integer vector, as `mpm`),
`log_Z_list` (numeric), `list_size` (= m), `list_full` (= `top_store$full`), `pip_list_source` ("store" or "exact"),
`pip_list_flag` (NULL when clean).

## 6. Relation to #5′
These are the quantities #5′ is about. In exact arithmetic `pip_list[j]` = π(j ∈ S | S ∈ 𝒯, y) and
`log_Z_list` = log Z + log π(𝒯 | y). If the list contains S₀, then for every data set
max_j |pip_list[j] − 1{j ∈ S₀}| ≤ 1 − π(S₀ | y), `mpm_list` = S₀ whenever 1 − π(S₀ | y) < ½, and
log Z + log π(S₀ | y) ≤ `log_Z_list` ≤ log Z. #5′ will supply "the list contains S₀" on the designs inside Theorem 6.
The fields say nothing by themselves about how much posterior mass the list holds; `log_Z − log_Z_list` is a rough,
uncertified indication (the printed `log_Z` is an estimate).

## 7. Acceptance tests for Engineering
**A. Nothing existing moves (golden tests).**
1. On the production-hash set (the 24 + 10 cases already used for the engine comparison) and on one fit per status path
   of §4: every existing field of the fit is `identical()` before and after the change — `hpm`, its score and
   provenance, `pip_r`, `pip_primary`, `mpm`, `log_Z` and per-island values, `top_store` (models, value, capacity,
   full), both leader stores, near ties, flags, local-search and LS0 records, score counts, grid. Timings excluded.
2. The fit with the new fields removed serialises to the same hash as the old fit.
3. Same seed, two runs: the new fields are `identical()`.

**B. The new fields, by hand.**
4. Store {1}, {1, 2}, {3} with scores c + log 0.5, c + log 0.3, c + log 0.2: `pip_list` = (0.8, 0.3, 0.2) on columns
   1, 2, 3; `mpm_list` = {1}; `log_Z_list` = c. Run with c = 0, c = 1000 and c = −1000: same `pip_list` to 1e−12.
5. One model {2, 5}: `pip_list` is 1 on columns 2 and 5 and 0 elsewhere; `mpm_list` = {2, 5}.
6. Store ∅ and {1} with equal scores: pip_list[1] = 0.5; `mpm_list` is empty.
7. Two models whose scores differ by 800: no NaN, no Inf; `pip_list` equals the indicator of the better model to 1e−12.
8. A design with a constant raw column (dropped): names of `pip_list` equal names of `pip_primary`.
9. A small problem on the enumeration branch whose store holds every model: the formula of §2 applied to the store
   equals the exact PIPs to 1e−10.
10. Invariants on every golden case: 0 ≤ `pip_list` ≤ 1; with S* the first listed model and w* its renormalised weight,
    max_j |pip_list[j] − 1{j ∈ S*}| ≤ 1 − w* + 1e−12; permuting the store changes `pip_list` by at most 1e−12.
11. A `resource_limit` fit and a failed calibration: the new fields are absent.
12. Core v3 against engine v4 on the golden set: `pip_list` and `log_Z_list` within 1e−12; `mpm_list` identical unless
    some pip_list[j] is within 1e−9 of 0.5 (report those cases).
