# R6 council review: NA_DROP v1.4 → v1.5 (Opus seat, fresh, effort high)

**Finding kinds held: WORDING (6) and QUALIFIER (1). No GENUINE GAP.** HQ ruling (C) is applied correctly in substance. Seven residues remain, all fixable with the exact texts below, applied as written.

**What I checked myself.**
- **Diff:** I regenerated `diff -ru ticket_pre-v15 ticket`. Ignoring timestamps, it is byte-identical to `NADROP_v1.4_to_v1.5.diff`.
- **Manifest:** `manifest.py verify` returns `verify: OK MANIFEST 148c9308…`. I ran it on my own rebuild in `.rc_tmp/r6opus_vt`, built from `main97` the same way `freeze_on_main.sh` does; I did not touch `bt*`. A raw sha256 check flags 5 files, but all 5 have CRLF line endings, which `verify` accepts by design (INFRA R06).
- **Registry conversion:** `ingest.py convert` exits 0, gives 3 records and an empty stderr. LIST-R's conclusion starts with `reported-model`.
- **Code:** I read `v3_fit.R:73-177`, `v3_run.R:150-279`, `cpp/v3_runtime.h`, `cpp/v3_core.cpp:450-490, 760-790` and `IMPL_LIST_codeprint.md:30-50`, all in `.rc_tmp/main97`.

## Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 | ACCEPT with findings | I grepped all six files for every listed pattern. Every remaining hit is scoped to the pinned core, to output runs, or sits in a historical changelog row (STATEMENT.md:169, v1.4, marked "Withdrawn in v1.5"). The delivery sentence is correctly scoped at L3:27, :42-44, :113-116, :123-124, ERRATA.md:5, CARD.md:10 and READER_DELTA.md:30. **One place still claims beyond output runs:** the registry `rate:` field, REPORT.md:67 (S-1, QUALIFIER). Two sentences are left dangling: STATEMENT.md:24 and REPORT.md:66 (S-4). "O_P on output" is ambiguous in one place: STATEMENT.md:127 (S-2). |
| 2 | ACCEPT | Changed hunks are exactly the claimed list. STATEMENT: lines 1, 24, 125-128, and line 169 equals the old line with only the "**Withdrawn in v1.5** (HQ ruling (C); see the v1.5 row). " prefix inserted (string check True). Line 170 is new. Lines 1-168 otherwise match. CARD: line 10 only. READER_DELTA: old lines 30-31 merged into line 30 (44 → 43 lines; no file cites a READER_DELTA line after 30). ERRATA: line 5. REPORT: lines 4, 19, 64, 66, 69. L3: lines 25, 27, 33-34, 42-49 → 42-44, 118-122 → 113-116, 129-130 → 123-124. The spans `:100-128` and premises `:29-64` keep their extent, and (iii) is still 4 lines. All 46 rows of the claimed-edit grep are where the table says. |
| 3 | ACCEPT with findings | **(iii) is true as proved.** Step 2 (L3:91-102) bounds P(𝒪 ∩ B) by data events, for every run specification, without using (D). So P(𝒪∩B₄) → 0, P(𝒪∩(B₁∪B₂∪B₃)(t)) → 0, and the t_n form all hold. The O_P argument (L3:116) is valid: with X_n := 0 off 𝒪, {X_n > t} = 𝒪 ∩ B_i(t) for each error, the constructed t_n is deterministic, lies in (0,½), and has t_n/r_n = k → ∞. **(iii) is no stronger than (ii) plus Step 2.** For the tagged method, the "Assume (D)" in (iii) is now idle, which is harmless for a WEAKER statement. The DLV-0 sentence in (iii) restates an imported result about the pinned core. "O_P(r_n) on output" must name the reading that was proved (S-2). |
| 4a | ACCEPT with findings | **The causal sentence is true.** On the sampler branch the last guard checks are inside `cpp_final_run` (`v3_core.cpp:459, 480`). On the exact branch the last guard decision is the preflight (`v3_fit.R:115-117`). `finish` (`:79-87`) never calls `check`: `cpp_runtime_report` only reads the clock. The helper runs after all of these, so it cannot affect any guard decision. "For matching guard inputs" is right, because `RuntimeGuard::check` is a function of (elapsed, operation). The "only possible difference" / "can differ only through an allocation" claim is gone (grep: 0 hits outside the changelog). **Two residues of b″-2:** the very next clause, L3:33-34 (C-1), and the ERRATA E1 cell (C-2). |
| 4b | ACCEPT with findings | **Confirmed in the code.** `v3_exact_list_last(finish(fit), e, ctx)` (`v3_fit.R:131`) passes `finish(fit)` as a lazy argument. `:275` reads only `e`; `:276` runs `v3_list_fields`; `:277` reads `fit$pip_primary`, which forces `finish`. So `peak_memory_kb` and `timings$total` are sampled after the helper. **Also sampled after the helper, but not named:** `runtime_guard$elapsed_seconds`. `v3_fit.R:82` calls `cpp_runtime_report`, which returns `g->elapsed()` (`v3_core.cpp:787`). `numerical_routes` reads `ctx` counters that the helper does not touch. **Fields the proof uses:** 𝒪 (`estimates_available`), `status`, `hpm`, `top_store` (sampler branch), `fit$exact` with its store, plus `pip_primary`, `mpm` and `names(pip_primary)` (Step 0′, Step 1 exact branch, `pip_names`). These are covered by "the other existing fields the proof uses", and `finish` writes none of them on an exact output run. **The `IMPL_LIST_codeprint.md:42` citation is under-reconciled:** that row says "fields added after `finish()` (`v3_fit.R:131`…)", which is the textual order, not the evaluation order. Saying it "is read for the fields the proof uses" does not settle that order (S-3). |
| 4c | ACCEPT | Matches the sources. `Sol5b/NA_DROP13_council_sol_R3.md:5-8, 13, 20`: b-1 to b-4 FIXED, b′-1 open, score=8.7 gates=FAIL. `NA_DROP_v14/R5_council_sol.md:14, 32`: b″-1, score=8.4 gates=FAIL (same text as `Sol6/CODEX_gpt-6.2-sol.md`). REPORT.md:19 and :64 carry identical status text, and the convert output's status equals it. CARD.md:10 records both results and says "separate from IMPL-LIST". |
| 5 | ACCEPT with finding | **The (0.6) note asserts no bound.** T_B, T_W and the constants are gone; "no bound … no constants C_W + 1, C_M + 8, and no extension of Lemma R, Corollary R or (D) … is asserted". Its code facts check out: `integer(max(orig))` with orig ⊆ 1..p_raw (`v3_run.R:257`); store capacity 40p+1 on both branches (`v3_ledger.h:78`, `v3_core.cpp:531`); keys from integer indices of ≤10 digits; numeric vectors F, u (length m) and num, pip (length p). Wording slip "K original indices" (E-2). **No new premise:** the assumptions line is unchanged. **depends_on** equals main `claims.tsv` row W3-D5P:LIST-R exactly (LIST-K, LIST-CODE, RM2-R-plus, RM0-plus, DLV-0, POST). |
| 6 | REPORT ONLY | The old clause appears in five reader places outside the ticket (listed under item 6 below). It is the unscoped Cor 6L clause, so (C) contradicts it. |
| 7 | — | All findings are WORDING, except S-1, which is a QUALIFIER. |

## Findings

**C-1 · WORDING (b″-2 residue) · `lemmas/L3_listR.md:33-34`.**
The parenthesis says no comparison of separate executions is claimed. The next clause then makes one, keyed only on input and uniforms. That is false whenever the measured times differ, because a guard can stop one execution and not the other.
- Replace: `— on every input and every\nrealisation of the run's uniforms the post-commit fit and the pinned fit execute the same computation (not the same measured times) up to the new\nfields,`
- With: `— on every input, every\nrealisation of the run's uniforms and matching guard inputs, the post-commit fit and the pinned fit execute the same computation up to the new\nfields (the measured times themselves are not claimed equal),`

Apply as written.

**C-2 · WORDING (b″-2 residue) · `ERRATA.md:5`, E1 proposed-fix cell.**
- Replace: `"so every guard decision of the tagged fit is that of the pinned fit [applied in L3 (0.5)], and`
- With: `"so the new computation, which comes after the last guard consultation, cannot affect any guard decision; for matching guard inputs every guard decision of the tagged fit is that of the pinned fit [applied in L3 (0.5)], and`

Apply as written.

**S-1 · QUALIFIER (ruling (C) not applied to the registry rate) · `REPORT.md:67`.**
`rate: O_P(sqrt(log n / n)) for the two PIP errors and |log_Z_list - log Z| (p >= 2)` has no "on output". Main's v1.1 rate had none either, but it was then covered by "under (D) without 'on output'". Under (C) the rate is proved only with each error set to 0 off 𝒪 (L3:116).
- Replace with: `rate: O_P(sqrt(log n / n)) on output runs (each error set to 0 off the output event) for the two PIP errors and |log_Z_list - log Z| (p >= 2)`

This is single-line and free text; the convert parse is unaffected. Apply as written, then re-run `ingest.py convert`.

**S-2 · WORDING (reading of "O_P on output") · `STATEMENT.md:127`.**
For the tagged method P(𝒪) is no longer controlled, so the conditional reading P(X_n > M r_n | 𝒪) is not proved. The joint reading, as in L3:116, is.
- Replace: `i.e. the two PIP errors and the evidence error are O_P(r_n) on output.`
- With: `i.e. the two PIP errors and the evidence error, each set to 0 off 𝒪, are O_P(r_n) ("on output"; no statement conditional on 𝒪).`

This stays on line 127, so the span and the 4-line extent are unchanged. It is EQUAL to the v1.5 intent. Apply as written.

**S-3 · WORDING (b″-3 completeness) · `lemmas/L3_listR.md:43`.**
- Replace: `so \`peak_memory_kb\` and \`timings$total\`, which \`finish\` samples, are measured after the helper; the proof does not use them, and the conformance citation \`reviews/IMPL_LIST_codeprint.md:42\` is read for the fields and state the proof uses)`
- With: `so \`peak_memory_kb\`, \`timings$total\` and \`runtime_guard$elapsed_seconds\` (\`v3_fit.R:80-82\`; \`cpp/v3_core.cpp:787\`), which \`finish\` samples, are measured after the helper; the proof does not use them, and the conformance citation \`reviews/IMPL_LIST_codeprint.md:42\` ("fields added after \`finish()\`", \`v3_fit.R:131\`: textual order; in evaluation order \`finish\` runs after \`v3_list_fields\` on the exact branch) is read only for the fields and state the proof uses)`

Apply as written.

**S-4 · WORDING (dangling delivery sentence) · `STATEMENT.md:24` and `REPORT.md:66`.**
Both sentences say "under the delivery premises / under (D), on output runs …" and then state no conclusion.
- STATEMENT.md:24
  - Replace: `under the delivery premises, on output runs of the method with the list fields (allocation/delivery of the list fields is not claimed for the tagged method beyond output runs)`
  - With: `with the delivery premises, the method with the list fields gains nothing beyond output runs (allocation/delivery of the list fields is not claimed for the tagged method beyond output runs)`
- REPORT.md:66
  - Replace: `; under (D), on output runs only: allocation/delivery`
  - With: `; under (D) as without it, these conclusions are on output runs only for the method with the list fields: allocation/delivery`

Apply as written.

**E-1 · WORDING · `STATEMENT.md:170`.**
- Replace: `the delivery conclusion "without 'on output'" is kept only on output runs for the method with the list fields`
- With: `the delivery conclusion is scoped to output runs for the method with the list fields (the form without 'on output' is withdrawn)`

Apply as written.

**E-2 · WORDING · `lemmas/L3_listR.md:44`.**
- Replace: `(K original indices of at most D ≤ 10 decimal digits each)`
- With: `(each of at most K original indices of at most D ≤ 10 decimal digits)`

Apply as written.

**F (note, no change requested).** For the tagged method, (iii)'s conclusions follow from (ii) and Step 3 without (D). The "Assume (D)" in (iii) only frames the imported pinned-core sentence (DLV-0). This is consistent with the WEAKER tag and with "no new premise".

## Item 6: outside the ticket (report only; no edits requested to frozen files)

The old clause still appears in two frozen reader files on main:
- `.rc_tmp/main97/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:71`: "…$O_P(\sqrt{\log n/n})$ on output; without "on output" under the delivery conventions (S4)."
- `.rc_tmp/main97/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:1441`: "…on output, and without "on output" under the delivery conventions (S4)."

The same clause is in the D5Pa v3 staged readers:
- `Sol5/D5Pa_v3_m97/staged_reader/CLAIMS_CARD.md:71`
- `Sol5/D5Pa_v3_m97/staged_reader/READER_VERSIONS.md:1441`

The D5Pa v3 ticket files also still carry the v1.1 text: `ticket/CARD.md:10`, `READER_DELTA.md:30`, `STATEMENT.md:123` ("without "on output": P(B₄) → 0"), `REPORT.md:66` and `TARGET.md:7`.

**Verdict on these:** each is a claim about Cor 6L's list fields, which only the tagged method (`method-v3.1.1-listpip`) prints. So it is exactly the claim (C) withdraws. All need the (C) scoping at the A re-pin. D5Pa v3 also edits W3-D5P/CARD.md:10, REPORT.md:66 and STATEMENT, so whichever of the two lands second must carry the (C) text, or the old clause comes back.

## Gates
- **G1 correctness: PASS.** The weakened (iii) is proved by Step 2 and Step 3. The b″-2 and b″-3 code facts hold. C-1 and C-2 are wording residues; the argument needs only the matching-guard-input reading, which holds.
- **G3 faithfulness and scope: PASS, conditional on S-1, S-2 and S-4 applied as written.** The one claim beyond output runs (REPORT.md:67) is a QUALIFIER fix.
- **G4 statuses and pins: PASS.** b″-4 quotes are verified against both review files. `verify` OK on 148c9308. depends_on equals the v1.1 list.
- **G5 registration form: PASS.** Convert exit 0, 3 records, empty stderr, `reported-model`. The S-1 text keeps the single-line form.

**Score: 8.7.** The (C) scoping is correct and complete in the claim span and the proof, the edits are exactly the claimed ones, and the manifest and statuses are clean. Points off for the registry rate left unscoped and for b″-2 residues in two places.

COUNCIL-VERDICT round=R6 manifest=148c9308f186bf9035697f46656479039a29c6ca1d5f9ac106cd845c52926aae seat=opus score=8.7 gates=PASS
