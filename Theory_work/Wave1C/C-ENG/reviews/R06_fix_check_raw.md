# R06 — check of the R05 fixes (bf093a8..0638af9), Codex gpt-6.1-sol, reasoningEffort high, fresh delegate, read-only.
Verbatim reply, received 2026-11-08 ~23:25 CST.

---

**R05 finding 1 — RESOLVED.**  
`Scripts/SMC_BVS/core/v3_fit.R:146` now copies the flag only when calibration recorded a fallback:

```r
if (!is.null(cf$grid_fallback)) fr$flags$grid_fallback <- cf$grid_fallback
```

Calibration creates that field only when fallback actually fires (`v3_calib.R:183`). Successful no-failure runs therefore omit it. Both `ls0 = FALSE` and `options(v3.grid_fallback = FALSE)` disable fallback at `v3_fit.R:126–127`, preserving flag absence. Repository-wide inspection found no other production consumer requiring `"none"`. The revised regression assertions cover flag absence and flag-name compatibility (`test_ls0.R:286–288`).

**R05 finding 2 — RESOLVED.**  
`Scripts/SMC_BVS/core/v3_run.R:95–99` validates the override before integer conversion: a finite, scalar, whole numeric value in `[0, 1e6]` is required. Unset options use `b$ell`; integer and double representations are accepted, including zero. Validation is skipped when LS0 is disabled.

`cpp/v3_core.cpp:473–476` performs the addition in `long long`, checks against `INT_MAX`, and converts only afterward. Negative base caps are also rejected. The `stop()` inside the `try` block propagates as an R error: the handler at `cpp/v3_core.cpp:483` catches only the distinct `NumericalFailure` type (`cpp/v3_util.h:26`).

Zero retains the intended semantics: `"ell_n"` permits zero moves but still performs a complete scan; the default adds the start-mode size. See `cpp/v3_engine.h:385–412`.

**New findings: none.**

Independent, in-memory R probes passed for unset options, integer/double zero and boundary values, invalid overrides, LS0-disabled validation bypass, and both cap rules. Mocked calibration probes passed for successful construction, disabled fallback, preliminary and rebuild failure, correct complete-grid selection, termination without retries, frozen-hash reconstruction, and resource-stop bypass. I did not rebuild C++ or rerun the full compiled suite; C++ conclusions come from source inspection. No files were edited.

| Requirement | Assessment | Evidence |
|---|---|---|
| **C-GROW MR1** | **MET** under the prescribed default configuration. | Checked cap is `ell_n +` actual start-mode size (`cpp/v3_core.cpp:469–479`); final search retains `o.ell` (`:456`). Complete scans and cap termination remain unchanged (`cpp/v3_engine.h:370–418`). |
| **C-DLV A.2** | **MET** under the stipulated exact-arithmetic assumptions. | Tight-path feasibility and greedy inclusion remain unchanged (`cpp/v3_start.h:229–269`), with the required operation/storage bounds and no uniform reads. Start-mode computation and LS0 remain inside the enclosing runtime measurement and guard (`cpp/v3_core.cpp:468–480`). |
| **C-DLV B / “Exact corrected statement” fallback behavior** | **MET** under its stated premises. | First tier-1 construction failure selects the last successful same-tier construction or completed pilot (`v3_calib.R:114–125`), preserves exported inherited state and tier budgets, and uses ordinary freezing (`:159–190`). Failed prefixes are excluded; numerical/resource stops bypass fallback. Other branches retain flag compatibility. |

The requirement assessments concern the prescribed configuration and stated premises; testing switches intentionally select alternative behavior.

**Verdict: APPROVE.**
