# R04 — review of the post-R03 deltas (C-PACK MR2 guard in v3_start.h, 9b9d234..36c0cfe; harness edits in
Scripts/SMC_BVS/tests), Codex gpt-6.1-sol, reasoningEffort high, fresh delegate, read-only. Verbatim reply, received
2026-11-08 ~22:58 CST.

---

No actionable findings (BLOCKER/MAJOR/MINOR/NIT).

1. **MR2 satisfied — `Scripts/SMC_BVS/core/cpp/v3_start.h:272`.**  
   `if (tie_dp && cap < 2) throw std::invalid_argument(...)` enforces the required minimum whenever the fallback is enabled. With cap ≥ 2, a unique maximiser finishes enumeration at count 1 without triggering the fallback. Disabling `tie_dp` preserves the previous path.

2. **MR1 satisfied — `Scripts/SMC_BVS/core/cpp/v3_core.cpp:467–471`.**  
   `start_mode(st, 1000000, o.ls0_tie_dp)` uses the run’s setup-owned `Start`; `E.local_search(m.S, ..., true, ..., PH_LS0)` starts from its returned set and emits the centre. In `v3_engine.h:383`, `eval(C, ME_LOCAL, emit_centre)` records that score through the shared ledger, including on a cache hit.

3. **Exception behavior acceptable — `Scripts/SMC_BVS/core/cpp/v3_core.cpp:477`.**  
   The sole production caller supplies literal cap `1000000`, so the new throw cannot fire through current production inputs. Hypothetically, `std::invalid_argument` would bypass the `NumericalFailure` handler and propagate through Rcpp as an R error; no structured failure fit would be assembled. That is acceptable for this unreachable programming-contract violation.

4. **Harness changes preserve the relevant checks — `Scripts/SMC_BVS/tests/changed_units.R:5`; `v2_runtime_units.R:121–135`.**  
   The formal-name assertion remains exact, adding only `ls0`. `no_ls0()` removes the row only after checking every entry equals zero; a successful LS0 centre emission increments the logical counter even when cached, so it cannot silently pass. All remaining counters retain exact comparison.

   `unavailable()` rejects every finite scalar and every longer estimate vector. Exact-name indexing prevents partial matching to `log_Zbar0`. Accepting `NULL` preserves the existing v3 behavior; scalar NA accommodates v3.1. This assertion does not independently enforce the entirety of row #15—field presence and every estimate field—but that is an existing coverage boundary, not a regression introduced by these edits.

Read-only static review; the harness was not executed.

**Verdict: APPROVE.**
