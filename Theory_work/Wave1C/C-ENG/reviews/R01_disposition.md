# R01 disposition (plan review, Codex gpt-6.1-sol high; raw reply `R01_plan_review_raw.md`)

Verdict received: REJECT as written. All seven findings accepted; PLAN.md → v1.1.

| # | sev | finding | disposition |
|---|---|---|---|
| 1 | BLOCKER | LS0 stop keeps the `fit$log_Z` → `log_Zbar0` partial-match hazard; #15 NA fields required by GUARD-W | ACCEPTED. v3.1 mode: shared helper `v3_unavailable_estimates()` sets estimate fields to NA by exact name on every public return without estimates; tests read `fit[["log_Z", exact=TRUE]]` and `fit$log_Z`. PLAN R11(e). |
| 2 | MAJOR | brute-force ĝ oracle contradicts TDP-E contract on real tables (2⁵⁴ example) | ACCEPTED. Oracles separated: lex_min(E) = uncapped enumeration for all tables; brute-force S* only for integer tables; real tables: value and size only; 2⁵⁴ fixture added; bounded claim stated in PLAN §2 and TDP_E.md. |
| 3 | MAJOR | merged-LS0 replay vs O-LS0 export (SPEC:399) missing | ACCEPTED. Test (c2): new core vs `cpp_final_run_ls0` on all p = 30 regression datasets + 3 replay designs at p = 500 (dev generator) if runtime allows, else recorded as an unmet gate. |
| 4 | MAJOR | public `local_limit` hides LS0 cap | ACCEPTED (Q1 answer). `local_limit` = final OR LS0 cap; `final_local_limit`, `ls0_local_limit` for attribution. |
| 5 | MAJOR | weak assertions (centre emission, ell = 0 cap, exact branch bypass) | ACCEPTED. Deterministic fixtures (c3): exact event count on an unscored centre, strict-improvement + ℓ = 0, tie change, endpoint-different HPM, eviction, forced guard stop and forced NumericalFailure; `branch_run == "smc"` asserted. |
| 6 | MINOR | TDP-E hypotheses / invariants; failure instead of empty model | ACCEPTED. Hypotheses added to TDP_E.md; root-feasibility check stops with an error. |
| 7 | MINOR | explicit switch-off branch; narrower equality definition | ACCEPTED. PLAN §4b; equality = all deterministic fields of completed runs, excluding named timing/memory measurements. |

Q2 (E1 on post-LS0 HPM) and Q4 (ℓ = production ℓ) confirmed by the reviewer.
