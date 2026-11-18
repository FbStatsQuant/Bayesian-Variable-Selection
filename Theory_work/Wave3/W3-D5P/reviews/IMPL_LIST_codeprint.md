# IMPL-LIST code reading (premise IMPL-LIST, `STATEMENT.md:59-63`) — lead, 2026-11-18

**Scope.** The method commit that adds the list fields, read against SPEC §2, §3, §4, §5, §7 A.1–A.2 (pinned carrier
`sources/SPEC_LIST_PIP_523dda23.md`, unchanged) and HQ's two confirmed SPEC §4 readings; plus a re-check of LIST-CODE's own
code reading (core 4676af6) against the tagged code. Part 1: tag `method-v3.1-listpip` = commit **e9bac478**
(`e9bac47861f1632a6615fecf5b107f6c396b7692`, merge of PR #69). Part 2 (guard hunk, `method-v3.1.1-listpip`): pending.
Scratch only under `.rc_tmp/`; evidence copied to `reviews/impl_list/`.

**What changed in the core.** `git diff 4676af6 e9bac478 -- Scripts/SMC_BVS/core`: `README.md` (+8), `v3_fit.R` (+6/−3),
`v3_run.R` (+53/−3). **No C++ file changed** (`cpp/` identical), so every C++ fact of LIST-CODE stands as read. Commits:
4b08bb88, 99aa0998, 8bd779be.

## 1. Where each field is computed (tag e9bac478)
| field | sampler branch (status `completed`) | exact branch (status `exact`) |
|---|---|---|
| all | `v3_fit.R:176` `v3_add_list_fields(fit, v3_list_fields(fit$top_store, ctx$orig, names(fit$pip_primary)))`, after `fit <- finish(fit)` (`:173`) | `v3_fit.R:131` `return(v3_exact_list_last(finish(fit), e, ctx))`; `v3_run.R:274-279` |
| `pip_list` | `v3_run.R:257-265`: `u <- exp(F − Fmax)`, loop `for (i in m:1L)` adds u_i to `den` and to `num[j]` for j ∈ S_i (`:260-264`), `pip <- num/den`, named `pip_names` (`:265`) | `fit$pip_primary` (`v3_run.R:277`) |
| `mpm_list` | `as.integer(orig[pip > 0.5])` (`v3_run.R:266`) | `fit$mpm` (`:277`) |
| `log_Z_list` | `Fmax + log(den)` (`v3_run.R:266`) | from `v3_list_fields(e$top, …)` (`:276-277`) |
| `list_size`, `list_full` | `m`, `isTRUE(top$full)` (`v3_run.R:266-267`) | from the same call on `e$top` (`:277`) |
| `pip_list_source` | `"store"` (`:267`) | `"exact"` (`:278`) |
| `pip_list_flag` | `NULL` when clean (`:267`), so absent (`v3_add_list_fields` skips NULL, `:269`); `"empty_list"` (`:249`), `"nonfinite_score"` (`:254`, `:256`) | `lf$pip_list_flag` (`:278`) |
The direct-caller path `v3_assemble_final(…, list_fields = TRUE)` (`v3_run.R:119`, `:219-220`) is not used by `v3_fit`, which
passes `list_fields = FALSE` (`v3_fit.R:162`).

## 2. Verdict per SPEC item
| SPEC item | verdict | evidence |
|---|---|---|
| §1 the list = `fit$top_store` (sampler), models in original indices, values F | MATCH | input `fit$top_store` (`v3_fit.R:176`); `lut` maps original → retained (`v3_run.R:257`) |
| §2 `pip_list[j]` = Σ_{j∈S} u / Σ u, u = exp(F − F_max) | MATCH | `v3_run.R:255-265` |
| §2 `mpm_list` = {j : pip_list[j] > 0.5}, strict, increasing original indices | MATCH | `:266`; `orig` = `pre$kept` is increasing |
| §2 `log_Z_list` = F_max + log Σ u | MATCH | `:266` |
| §3 subtract F_max before exp; sums from last entry to first, plain double, no compensation; no clamping | MATCH | `:258-264` (explicit loop `m:1L`; comment `:236-238` on R's long-double `sum()`); no clamp |
| §4 status `completed` → from `top_store` | MATCH | `v3_fit.R:176` |
| §4 status `exact` → `pip_list` = `pip_primary`, `mpm_list` = `mpm`, `log_Z_list` from the store, source "exact" (**HQ reading (1)**: store = `fit$exact$top`; `list_size`/`list_full` describe it) | MATCH | `v3_run.R:274-279` uses `e$top` (= `fit$exact$top`, `v3_fit.R:122`) |
| §4 **any other status → fields absent (NULL), also when partial results are returned** | **DEVIATION (open item)** | sampler branch, final run not completed (`resource_limit` from the runtime guard in the final run, or `numerical_failure` in the final run): `v3_fit.R:176` still runs; `fit$top_store` is NULL there (set only on the completed path, `v3_run.R:210`; early return `:143-149`), so `v3_list_fields(NULL, …)` returns all seven fields NA with `pip_list_flag = "empty_list"`, `list_size = 0` (`v3_run.R:249`). Demonstrated: `reviews/impl_list/finalstop.R` (final-run status forced to `resource_limit` through a wrapper of `cpp_final_run`) → `reviews/impl_list/finalstop_out.txt`: "status: resource_limit … list fields present: pip_list, …, pip_list_flag; pip_list_flag: empty_list". Other non-output statuses are correct: preprocessing failures, preflight `resource_limit`, setup failure and calibration stops return before `:176` (`v3_fit.R:89`, `:102`, `:117`, `:137`, `:159`), and a non-`exact` enumeration leaves the fit unchanged (`v3_run.R:275`); the tagged unit test checks these (`tests/list_pip_units.R:152-160`) but has no final-run stop. **Fix (HQ decision (a)):** a guard so the fields are absent unless the final run completed; new tag `method-v3.1.1-listpip`. |
| §4 single model; empty model in the list; tie at 0.5; column in no / every model (0 / 1 exactly) | MATCH | `:262` (empty model adds to `den` only); strict `> 0.5`; a column in every model adds the same terms in the same order as `den` → exactly 1 |
| §4 empty list on a completed run → NA + `"empty_list"` (must not occur) | MATCH | `:249`; cannot occur (LIST-CODE (iii)) |
| §4 duplicate models → stop with an error | MATCH | `:253` (checked before the non-finite flags at `:254`, `:256`) |
| §4 −Inf weight 0; NaN or +Inf → NA + `"nonfinite_score"`; **HQ reading (2)**: all −Inf → NA + `"nonfinite_score"` | MATCH | `:254`, `:256`; exp(−Inf) = 0 at `:258` |
| §5 names: `pip_list` named and ordered as `pip_primary`; `mpm_list` integer; `pip_list_flag` NULL when clean | MATCH | `pip_names = names(fit$pip_primary)` (`v3_fit.R:176`); `as.integer` (`:266`); NULL skipped (`:269`) |
| §7 A.1–A.2 nothing existing moves; fields added last; no random numbers, no state | MATCH (on the runs checked) | code: additions only; fields added after `finish()` (`v3_fit.R:131`, `:173-176`); no RNG call in `v3_list_fields`; no global assignment. Executed: old core 4676af6 vs tagged core on 10 units (5 supplementary, 5 status paths) with Engineering's comparator `tests/list_pip_ab/ab_run.R`: `identical=TRUE fp_equal=TRUE names_order=TRUE attrs=TRUE elem_attrs=TRUE new_last=TRUE` for all 10 (`reviews/impl_list/ab_subset_log_new.txt`). Tagged unit suite `tests/list_pip_units.R`: **all 124 checks passed** (`reviews/impl_list/list_pip_units_out.txt`). The 24 PROD-H cases were not run here (Engineering's confirmation covers them). |
*Observation (not an open item; unreachable under EX-A).* On the exact branch a non-finite store score would set
`log_Z_list` NA and the flag while `pip_list`/`mpm_list` stay the exact PIPs/MPM (`v3_run.R:277-278`). Under EX-A every
store value is a finite F(S) (Lemma S.2), so this row never fires on an output run.

## 3. LIST-CODE re-check against the tagged code (what it reads, moved or changed)
- **C++** (`cpp/*.h`, `cpp/v3_core.cpp`): unchanged; every C++ citation of L2 (A1–A5, B2–B4, C, D1–D3, E) stands.
- **R, changed or moved lines cited in L2 / L3** (content still supports the step unless stated):
  - `v3_run.R:223-229` (L2 notation, `v3_final_run`) → now **`v3_run.R:225-231`** (+2 lines: signature gains `list_fields`, `:225`).
  - L3 (0.5) / R3 review cite `v3_run.R:227` (`cpp_final_run` call) → now **`v3_run.R:229`**.
  - `v3_run.R:119` signature of `v3_assemble_final` gains `list_fields = TRUE` (L2 does not cite the signature line).
  - `v3_fit.R:131` (L3 Step 1 cites `:130-131` "returns with `estimates_available` FALSE"): now
    `return(v3_exact_list_last(finish(fit), e, ctx))` — still returns; the added fields do not touch `status` or
    `estimates_available`.
  - `v3_fit.R:162` (L2 notation, L3 (0.5)): now passes `list_fields = FALSE`; same call, same role.
  - `v3_fit.R:173` (L2 B1 "after the final run at `v3_fit.R:173`"): now `fit <- finish(fit)`; the fit is returned at
    **`v3_fit.R:176`** with the list fields added. B1's equivalence `status == "completed"` ⇔ `estimates_available`
    is unaffected (the new fields touch neither).
  - Unchanged and still exact: `v3_run.R:88-103, 110-114, 121, 141-149, 160-162, 210, 218`; `v3_fit.R:78-89, 99-102,
    106, 117-122, 125-129, 171`.
- Conclusion: LIST-CODE (i)–(v) hold for the tagged code; two R citations moved by two lines (above). L3 (0.5)'s guard
  sentence holds: the list fields are computed after the last guard consultation (`v3_fit.R:131`, `:176`, both after
  `finish()`), and the computation raises no error on an output run (duplicates and out-of-set columns are excluded by
  L2 (iii)/(iv)).

## 4. NA_DROP premise: is `log_Z_list` provably non-NA on Theorem 6's event / the delivery event?
Against the tagged code, **yes on every output run** under EX-A (hence on Theorem 6's data event and on the delivery
event): sampler branch — `v3_list_fields(fit$top_store, …)` returns NA only for an empty store (`:249`; impossible, the store
holds the HPM-order maximum of a nonempty offered set, LIST-CODE (iii)), a NaN/+Inf score or all −Inf (`:254`, `:256`;
impossible, every store value is a finite F(S), Lemma S.2); exact branch — the same function on `e$top` (`:276`), same
argument with LIST-CODE (iv). The incomplete-run deviation of §2 concerns non-output runs only and does not affect this;
after the guard (part 2) those fields are absent there. This is the premise NA_DROP v1.2 needs; recording v1.2 (STRONGER)
still needs seats on a new manifest (manager, 2026-11-18).

## 5. Part 2 — the guard hunk (`git diff method-v3.1-listpip method-v3.1.1-listpip -- Scripts/SMC_BVS/core/`)
Pending: the new commit.

IMPL-LIST: NOT DISCHARGED (one open SPEC §4 item: on fits whose final run did not complete the list fields are present — NA, flag "empty_list" — instead of absent; HQ decision (a): guard, new tag method-v3.1.1-listpip)
