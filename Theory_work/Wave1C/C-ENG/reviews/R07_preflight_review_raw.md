# R07 — review of the preflight delta 8a27652..ef33f91 (`Scripts/SMC_BVS/core/v3_fit.R`), Codex gpt-6.1-sol, reasoningEffort
high, fresh delegate, read-only. Verbatim reply, received 2026-11-09 ~00:10 CST.

---

1. **MAJOR — Archive allowance undercounts stored data and conversion peak.** `Scripts/SMC_BVS/core/v3_fit.R:42`

   > `comp <- c(comp, ls0_archive = 2 * ls0_scans * (4 * K + 64))`

   The two factors represent path and scanned-centre models, but do not cover their simultaneous C++ and R representations. `LocalArchive` also retains scores, `scan_complete`, `scan_size`, centre/returned models, and vector capacities. `local_to_list(A0, D)` allocates R copies while `A0` remains alive (`v3_core.cpp:478`).

   **Failure scenario:** With `K = 100`, `ell = 11`, the allowance is **103,936 bytes**. An independently constructed R archive with 111 path entries and 112 scanned centres, each of size K, occupies **107,400 bytes already**, excluding the live C++ archive. The term has the required asymptotic order, but its constant is inadequate as an archive memory bound.

   **Fix:** Charge C++ storage and capacity growth, R model/list headers and payloads, all parallel vectors, and centre/returned models at the conversion peak. Validate the allowance against representative constructed archives; the existing test merely checks the proposed formula.

2. **MAJOR — The new SMC benchmark runs before an already-certain memory rejection.** `Scripts/SMC_BVS/core/v3_fit.R:41`

   > `ls0_s <- time_fun(K); ls0_seconds <- 2 * ls0_requests * ls0_s`

   This executes before `bytes` and `exceeds` are evaluated. Through `v3_time_scores`, it creates a timing context and performs 200 size-K scores. The shipped SMC preflight could reject immediately without either operation.

   **Failure scenario:** For `n = 20000`, `p = 10000`, `K = 10000`, and 8 GiB, the estimate is approximately **227 GiB**, yet a stub confirms the timing function is still invoked. The real benchmark builds a 10,000-column context, including its dense Gram matrix, then attempts expensive scores. A predictable `resource_limit` return can become prolonged computation or allocation failure.

   **Fix:** Evaluate the memory estimate, including the archive term, before invoking the benchmark. Return the memory rejection without timing when it already exceeds allocation.

The remaining checks passed inspection and deterministic probes:

- The scan bound includes the final complete scan. The request bound also covers centre emission: fewer than the maximum scans leave at least one scan’s slack; attaining the maximum requires a size-K start, whose first scan skips additions and supplies the necessary slack.
- Both initial and escalation preflights include the LS0 time comparison in `exceeds`.
- Both compatibility switches preserve the shipped preflight construction. Controlled comparisons against `8a27652` were identical for both branches and tiers.
- Timing-context sizing preserves K: `min(p, max(64, K)) >= K`; neither `p < 64` nor small n introduces a size mismatch. The exact branch remains unchanged.
- Size-K timing with factor 2 is a plausible operational heuristic, but the supplied tests do not establish that it covers cache/store overhead or numerical fallback costs. It should not be interpreted as a rigorous runtime bound.
- Additional refusals caused by the new archive/time gates are intended. The benchmark-before-rejection failure above is an unintended regression.

**Verdict: REJECT.**

## Disposition (C-ENG)
- #1 ACCEPTED. Allowance = (2 scans + 4)(12K + 256) + 96 scans + 4(8W + 4K + 96) bytes (C++ vectors with capacity growth +
  R copies + list slots for path, scanned centres, centre, returned; parallel vectors both copies; scan particles).
  Validated in `tests/test_preflight.R` against a constructed worst-case archive (R copy measured with `object.size`, built
  exactly like `local_to_list`, plus an upper estimate of the live C++ archive) for (K, p) = (30, 30), (100, 500),
  (100, 1000), (1000, 2000): all covered (`numerics/out_test_preflight.txt`).
- #2 ACCEPTED. The memory estimate (with the archive term) is evaluated first; the size-K timing runs only if it fits
  (`ls0_worst_case$timed`); spy test: 228 GiB > 8 GiB case returns with 0 benchmark calls.
- Timing heuristic: documented in code and REPORT as an operational estimate, not a rigorous runtime bound.
