# R03 — code review of the diff f16ce15..9b9d234 (Codex gpt-6.1-sol, reasoningEffort high), verbatim reply

Reviewer: fresh delegate_task (Codex, gpt-6.1-sol, high), read-only, briefed to find defects in
`git diff f16ce15 9b9d234 -- Scripts/SMC_BVS/core Scripts/SMC_BVS/study/adapter.R` against SPEC rows #6, #8-#10, #15, #26,
L1, PLAN.md, lemmas/TDP_E.md, W1-N3. Received 2026-11-08 ~22:17 CST.

---

No actionable findings.

Reviewed the specified diff against METHOD_v3.1_FINAL rows #6, #8–10, #15, #26 and L1, the implementation plan, TDP_E, and W1-N3.

- The tie DP preserves the enumeration’s tie set and selects its lexicographic minimum. Bounds, `j = 0`, K restrictions, block-position masks, interleaved blocks, and refresh after rejected inclusion appear correct. With `tie_dp = false`, the original arithmetic and enumeration order are preserved.
- LS0 runs after the final local-search guard checkpoint, uses the existing ledger/cache, emits its centre, and consumes no randomness. I found no change to the preceding sampler computation.
- `PH_LS0` is appended without shifting existing indices. Serialization retains the old matrix layout when disabled; I found no incompatible positional consumer in the requested directories.
- E3 uses the pre-LS0 HPM. Certification checks the returned HPM against each certified search endpoint. Completed move caps retain estimates; guard stops and numerical failures suppress them.
- The exact-name NA helper prevents `fit$log_Z` from partially matching `log_Zbar0`. The adapter preserves valid scalar estimates and empty supports while recognizing unavailable markers.

Independent, in-memory R checks passed for NA handling, adapter behavior, E3 isolation, endpoint certification, completed LS0 caps, and stopped-run assembly.

Validation limit: I did not rebuild Rcpp or independently rerun the compiled regression/replay suites. The C++ conclusions and disabled-switch compatibility assessment are based on source review.

**Overall verdict: APPROVE.**
