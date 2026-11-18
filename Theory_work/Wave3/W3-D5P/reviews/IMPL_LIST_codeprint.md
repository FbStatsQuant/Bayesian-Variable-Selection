# IMPL-LIST code reading (premise IMPL-LIST, `STATEMENT.md:59-63`) — lead, 2026-11-18

**Scope.** The method commit that adds the list fields, read against SPEC §2, §3, §4, §5, §7 A.1–A.2 (pinned carrier
`sources/SPEC_LIST_PIP_523dda23.md`, unchanged) and HQ's two confirmed SPEC §4 readings; plus a re-check of LIST-CODE's own
code reading (core 4676af6) against the tagged code. Part 1: tag `method-v3.1-listpip` = commit **e9bac478**
(`e9bac47861f1632a6615fecf5b107f6c396b7692`, merge of PR #69). Part 2 (guard hunk): `method-v3.1.1-listpip` = 7100bb3b, §5.
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

## 2b. The single open SPEC item and its effect
**Item.** SPEC §4 row "any other status → the fields are absent (NULL), also when partial results are returned": on a
sampler-branch fit whose **final run did not complete** (`raw$status != "completed"`, `v3_run.R:143`: a runtime-guard stop
or a numerical failure inside the final run), `v3_assemble_final` returns early without `top_store` (`:143-149`), and
`v3_fit.R:176` still calls `v3_list_fields(NULL, …)`: m = 0, so the seven fields are set to NA with
`pip_list_flag = "empty_list"` (`v3_run.R:249`) instead of being absent. Verified independently (code path above;
executable emulation `reviews/impl_list/finalstop.R` → `finalstop_out.txt`).
**Does it break IMPL-LIST as worded?** Yes, for that row only. IMPL-LIST (`STATEMENT.md:59-63`) requires the commit to
compute the fields "as SPEC §2 and §4 prescribe"; on incomplete-final-run fits the §4 row is not followed. The second half,
"changes no other field and no other state", **holds**: the deviation adds new fields only; no legacy field changes
(A/B identity below) and no error or state change occurs (`v3_list_fields(NULL, …)` returns before any computation).
**Is any LIST-R or LIST-CODE clause affected?** No.
- LIST-CODE (i)–(v) read the pinned core's existing fields (C++ unchanged; R lines moved only, §3); the extra fields touch
  neither `status`, `estimates_available`, `hpm`, `top_store` nor `fit$exact`.
- LIST-R (C3)(i)–(iii) are about runs that return output (𝒪 = `estimates_available` TRUE); an incomplete-final-run fit has
  `estimates_available = FALSE` (`v3_run.R:144`), so it is outside every clause. L3 (0.5) uses IMPL-LIST for two facts —
  the post-commit fit returns iff the pinned fit returns, and its existing fields are the pinned ones — both still true on
  those fits (no error is raised; nothing existing changes). L3 Step 1's identification of the printed fields uses SPEC §2
  and the `completed` / `exact` rows of §4 only, which MATCH.
- The NA_DROP premise (§4 below) is about output runs and is unaffected.
**Remedies (HQ's choice).** (a) the guard `if (identical(fit$status, "completed"))` at `v3_fit.R:176` (Engineering's
proposal), new tag `method-v3.1.1-listpip` — then IMPL-LIST as worded is met (part 2 checks the hunk); or (b) narrow the
premise to output runs ("on every run that returns output, computes them as SPEC §2 and §4 prescribe …"), a statement
change needing its own check. HQ chose (a) (manager, 2026-11-18).

## 2c. Inputs consulted (not part of this independent read)
- Engineering's code read `Docs/Experiments/P1M/results/listpip_ab/IMPL_LIST_CODE_READ.md` (main checkout, 2026-11-18):
  same single deviation (its §4 row "DEVIATION (minor)", same cause, same one-line guard); every other row OK — concordant
  with §2 here.
- Legacy-field bit-identity (SPEC §7 A.1–A.2): Engineering's A/B, PR #69 comment
  https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/69#issuecomment-6977156343 (39/39 units identical on tree
  991787ef — 34 PROD-H production + 5 status paths — and 15/15 fast units on the final tree 8ff2d876, same C++ key). Cited,
  not redone; my 10-unit subset (§2, last row) is an independent spot check.

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

## 5. Part 2 — the guard hunk at `method-v3.1.1-listpip` = main **7100bb3b** (`7100bb3b5a341aed5cbcd3b03fa5851a6345f0dd`, PR #80)
`git diff method-v3.1-listpip method-v3.1.1-listpip -- Scripts/SMC_BVS/core/`: **one file, one line** (`v3_fit.R`, 1+/1−):
```
-  v3_add_list_fields(fit, v3_list_fields(fit$top_store, ctx$orig, names(fit$pip_primary)))
+  if (identical(fit$status, "completed")) v3_add_list_fields(fit, v3_list_fields(fit$top_store, ctx$orig, names(fit$pip_primary))) else fit
```
(`v3_fit.R:176`; the other tag-diff files are outside the core: tests, `Lean/BRIEF.md`, Wave3 HQ notes.)
- **Incomplete final run → fields absent (SPEC §4).** On a sampler fit whose final run did not complete, `fit$status` is not
  "completed" (it is copied from the final run, `v3_fit.R:171`), so `:176` returns `fit` unchanged: no list field is added.
  Executed: `reviews/impl_list/finalstop.R` on the tagged core → `reviews/impl_list/finalstop_out_v3.1.1.txt`: "status:
  resource_limit … list fields present: (none)". The open item of §2 / §2b is **closed**.
- **Completed branch untouched.** For `fit$status == "completed"` the line evaluates exactly the former call (same arguments,
  same function); `finish()` and everything above `:176` are unchanged (one-line diff).
- **Exact branch untouched.** It returns at `v3_fit.R:131` (`v3_exact_list_last(finish(fit), e, ctx)`) before `:176`; no line
  of it changed.
- **Nothing else changed** in `Scripts/SMC_BVS/core/` (diff stat: 1 file); `v3_run.R` and all of `cpp/` identical to
  e9bac478, so §1–§4 (field lines, SPEC verdicts, LIST-CODE re-check, NA premise) carry over unchanged.
- **Tests at the tag.** `tests/list_pip_units.R`: **all 155 checks passed** (`reviews/impl_list/list_pip_units_out_v3.1.1.txt`),
  including the new final-run-stop and INV-SCORE-BITS checks.
- **INV-SCORE-BITS (Engineering, cited).** `Docs/Experiments/P1M/results/listpip_ab/IMPL_LIST_CODE_READ.md` §"INV-SCORE-BITS"
  (manager-verified 2026-11-18; trace `SCORE_PATH_TRACE.md`): every score offered to the top and leader stores for a model
  S is the binary64 value `D.logprior[|S|] + Scorer::score(S).logm`, one deterministic function of the sorted S; hence a model
  never reaches a store with two values, the store's (value, S) dedup is exact dedup by model, and the list-PIP duplicate
  `stop()` (`v3_run.R:253`) is unreachable by construction, also in binary64. Test: the `identical()` recomputation in
  `tests/list_pip_units.R` "INV-SCORE-BITS" (PR #80). This complements L2 D2 / L3 (0.5), which exclude duplicates under EX-A.
- **For the recording.** With IMPL-LIST discharged, LIST-R carries no open premise ("conditional on IMPL-LIST" is dropped;
  status plain PROVED-CHECKED), method pin `method-v3.1.1-listpip` (7100bb3b). The T6 F3 wording fix of L3 (0.5) — name all
  three `stop()` rows of `v3_list_fields` (store/score length mismatch `v3_run.R:251`, duplicate model `:253`, column outside
  the retained set `:263`), each unreachable on an output run — belongs to the later NA_DROP round, not v1.1 (manager,
  2026-11-18).

## 6. SUPERSEDED (route b′ not taken) — SPEC §4 amended to match the tagged code
*Record only.* HQ's latest decision is route (a) (manager, 2026-11-18): Engineering adds the guard, HQ tags
`method-v3.1.1-listpip`; no SPEC carrier change, no STATEMENT edit (`STATEMENT.md:11` and `:57` stay true once the guard makes
the fields absent), no NA_DROP Step 0′ rewording. The text below is kept as the record of the route not taken.

*Conflict to resolve first.* The manager's earlier message "HQ CHANGED COURSE … decision (a): guard + new tag
`method-v3.1.1-listpip`; SPEC stays as is" states that it supersedes a crossed "SPEC §4 amended" message. The message asking
for this section announces "SPEC §4 is amended … no code change, no re-tag". The two routes are exclusive; **which one
stands is HQ's** — this section answers the (b′) questions so either can proceed.

**(1) Every claim is about output runs only — where each clause restricts itself** (`STATEMENT.md`, v1.1.2 in MANIFEST_R3r):
| clause | restriction | where |
|---|---|---|
| LIST-K (C1) (a)–(e) | deterministic; about a list 𝒯 ⊆ Ω containing S₀ — no run, no field | `STATEMENT.md:67-75` |
| LIST-CODE (C2) (i) | "On the sampler branch, `fit$status == "completed"` iff … 𝒪. On such a run …" | `:82-86` |
| LIST-CODE (C2) (ii), (iii) | "On a completed run" | `:87`, `:89` |
| LIST-CODE (C2) (iv) | "On status `exact`" | `:91` |
| LIST-CODE (C2) (v) | "on a completed run …; on an exact-branch run" | `:94-95` |
| LIST-R (C3) (i) | "every admissible run that returns output" | `:103` |
| LIST-R (C3) (ii) | the error events are "of an output run" and every bound is on 𝒪 ∩ B (`P(𝒪 ∩ …)`); the t_n display "every admissible run that returns output" | `:109`, `:113-114`, `:119` |
| LIST-R (C3) (iii) | under (D) "every admissible run returns output (DLV-0)" | `:122` |
| Corollary 6L (reader) | "A run that produces output returns …"; "every run that produces output" | `READER_DELTA.md:13`, `:21` |
| Card row 3.1L | "every run that produces output" | `CARD.md:10` |
An incomplete-final-run fit has `estimates_available = FALSE` (`v3_run.R:144` at the tag), i.e. lies in 𝒪ᶜ: **no clause
uses SPEC §4's incomplete-run case**; LIST-CODE does not mention the list fields at all. Unaffected: LIST-K, LIST-CODE (i)–(v),
LIST-R (i)–(iii), Corollary 6L. The proofs: L3 (0.5) uses only "the commit raises no error except the duplicate row" and
"no existing field changes" — both true at the tag also on incomplete fits (§2b).

**(2) What must change so that IMPL-LIST refers to the amended SPEC.**
- **Carrier.** A CORRECTION-ONLY update of the pinned carrier: a new file `sources/SPEC_LIST_PIP_<amended commit>.md`
  (byte-identical copy of the amended SPEC at its commit, with the same one-line carrier header), and the old carrier
  `sources/SPEC_LIST_PIP_523dda23.md` kept or removed by HQ's choice (kept is safer for the record); `STATEMENT.md:11`
  ("SPEC := … @ theory/W3-AUDIT 523dda23") must then name the amended commit — **a wording change in STATEMENT itself**
  (a pointer; EQUAL if the amendment touches only the incomplete-run row).
- **STATEMENT §1, `STATEMENT.md:57`** — "Other statuses: the fields are absent (SPEC §4); no claim." — becomes false under
  the amended §4 for incomplete-final-run fits. **Wording change in STATEMENT itself, flagged:** e.g. "Other statuses: the
  fields are absent, or — on a fit whose final run did not complete — present as NA with `pip_list_flag = "empty_list"`
  (SPEC §4 as amended); no claim." Tag EQUAL (a description of the code's non-output behaviour, outside every claim span;
  no clause uses it) — to be confirmed by the check.
- **IMPL-LIST text (`STATEMENT.md:59-63`)** needs no change: "as SPEC §2 and §4 prescribe" then reads against the amended
  SPEC through the SPEC pointer.
- **Elsewhere:** the NA_DROP draft's L3 Step 0′ (not frozen) lists the §4 rows and says other statuses are "absent; not an
  output run" (`reviews/post_cp3/NA_DROP/L3_listR_v1.2_draft.md:46-47`) — reword to "absent or NA-flagged; not an output
  run". REPORT, CARD, READER_DELTA, L1–L3 as frozen do not mention the other-status row.
- **Process.** The above as one CORRECTION-ONLY change (carrier + `STATEMENT.md:11`, `:57`), re-freeze (R3r → new manifest),
  and one Opus check that (i) the carrier is byte-identical to the amended SPEC, (ii) the amendment touches only the
  incomplete-run row (else every changed SPEC row must be re-read here), (iii) no clause or proof step uses that row, (iv)
  the two STATEMENT edits are EQUAL. The council seats (Opus R4, Sol R3S) are on MANIFEST_R3r; the recorder carries them as
  for R3r2.

**(3) NA_DROP premise with the amendment folded in.** On every **output** run, `log_Z_list` is provably non-NA under EX-A
against the tagged code: SPEC §4 (amended) sets the fields NA only on (α) incomplete-final-run fits — not output runs
(`estimates_available = FALSE`); (β) an empty list — impossible on output runs (LIST-CODE (iii), (iv)); (γ) a NaN / +Inf
score, or all scores −Inf (HQ reading (2), `v3_run.R:256`) — impossible on output runs: every store value is a finite
F(S) (Lemma S.2, LIST-CODE A5), so in particular not all are −Inf; and the exact branch computes `log_Z_list` from
`fit$exact$top` (reading (1)). Hence non-NA on every output run, in particular on Theorem 6's data event and on the delivery
event. NA_DROP's (o) is unchanged in substance; only Step 0′'s description of the other-status row changes (above).

IMPL-LIST: DISCHARGED at method-v3.1.1-listpip (7100bb3b)
