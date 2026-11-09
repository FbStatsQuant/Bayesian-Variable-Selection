# R05 — review of the HQ wave-2 diff 95be87e..bf093a8 (C-GROW MR1, C-DLV A.2, C-DLV B + HQ_AUDIT precision), Codex
gpt-6.1-sol, reasoningEffort high, fresh delegate, read-only. Verbatim reply, received 2026-11-08 ~23:14 CST.

---

1. **MINOR — No-failure fits acquire a new flag, violating output compatibility.**  
   `Scripts/SMC_BVS/core/v3_fit.R:145`:
   ```r
   if (isTRUE(ls0)) fr$flags$grid_fallback <- cf$grid_fallback %||% "none"
   ```
   **Failure scenario:** Any successful SMC fit with LS0 enabled and no grid failure now returns `flags$grid_fallback = "none"`, whereas the baseline omits that field. This also happens with `options(v3.grid_fallback = FALSE)`. Consequently, flag names, serialized outputs, and exact comparisons change outside the former `schedule_limit` event.

   **Fix:** Add the fit flag only when calibration actually recorded a fallback:
   ```r
   if (!is.null(cf$grid_fallback))
     fr$flags$grid_fallback <- cf$grid_fallback
   ```

2. **MINOR — The new cap addition can overflow through the existing testing override.**  
   `Scripts/SMC_BVS/core/cpp/v3_core.cpp:473`:
   ```cpp
   int ls0_cap = o.ls0_ell + (o.ls0_cap_plus_mode ? (int)m.S.size() : 0);
   ```
   `Scripts/SMC_BVS/core/v3_run.R:95`:
   ```r
   ro$ls0_ell <- as.integer(getOption("v3.ls0_ell", b$ell))
   ```
   **Failure scenario:** `options(v3.ls0_ell = .Machine$integer.max)` reaches C++ unchanged. A nonempty start mode then causes signed integer overflow, which is undefined behavior. With ordinary wrapping, the resulting negative cap makes `A.moves >= ell` immediately true at the first improving scan. This addition introduces a failure for an override previously representable as an `int`.

   **Fix:** Validate the override and perform checked addition in a wider integer type before converting to the local-search parameter type. Reject unrepresentable caps explicitly. The production default is safe under the current integer dimension bounds; this finding concerns the exposed testing override.

**Requirement assessments**

- **1. C-GROW MR1 — NOT MET across all accepted settings**, because of finding 2. The default implementation otherwise correctly uses the size of the actual start mode, adds it once, and leaves the final local search at `o.ell`. The `"ell_n"` switch removes the size increment. Existing scan, tie, provenance, and uniform behavior remains unchanged.

- **2. C-DLV A.2 — MET under the reference’s exact-arithmetic assumptions.** `mode_tie_dp` greedily selects the lexicographically smallest member of the tight-path tie set; under EX-A this is the reference maximizer. Its feasibility work satisfies the requested operation bound. Importantly, `arg` stores each block code at most once across its size lists, so its total storage is `O(Σ_b 2^{|C_b|})`, not a list of global maximizing models. Together with `M`, `reach`, masks, and size tables, storage satisfies `O(Σ_b 2^{|C_b|} + J(K+1))`.

  The preceding enumeration retains only the current choices, recursion stack, current model, and best model. Its fixed one-million-leaf cap also keeps its work within the requested asymptotic envelope. Neither path reads uniforms; the elapsed start-mode computation is included in the enclosing LS0 guard check. Binary64 guarantees remain limited to lex-minimum of the coded tie set, as the proof note explicitly acknowledges.

- **3. C-DLV B / HQ precision — NOT MET strictly**, because finding 1 changes no-failure output flags. The fallback control flow itself meets the requirement: a failed rebuild leaves `g` holding the last successful same-tier construction; preliminary failure selects the completed same-tier pilot. Failed prefixes are not frozen, and construction failure ends the tier without retries.

  In-memory R probes confirmed preliminary failure, rebuild failure, forced completed pilot, partial pilot, numerical failure, and blocked escalation behavior, including ordinary frozen-hash reconstruction. Tier budgets and inherited state are preserved. Numerical/resource stops bypass fallback. `ls0 = FALSE` disables the new fallback and flag insertion.

  The existing harness **can intentionally change behavior** on former `schedule_limit` cases: both cited acceptance checks still pass, but `worker.R:103` now enters its calibrated-final branch. Baseline comparisons needing the old failure behavior should explicitly disable fallback.

The requested main-checkout `TDP_E.md` was absent; I reviewed the copy in this worktree. No files were edited.

**Verdict: APPROVE-WITH-FIXES.**

## Disposition (C-ENG)
- #1 ACCEPTED, fixed in 0638af9: `flags$grid_fallback` is set only when the fallback fired; test `wave2` now asserts no
  flag (and the v3 flag set plus the four LS0 flags) on no-failure runs.
- #2 ACCEPTED, fixed in 0638af9: `v3.ls0_ell` validated in R (whole number in [0, 1e6]); C++ computes the cap in 64-bit and
  stops if it exceeds INT_MAX; test `wave2` checks that `.Machine$integer.max` is rejected.
- Harness note: re-run of the existing harness on the final code (B3/C3) records whether any seed hits the former
  schedule_limit branch (REPORT §3d).
