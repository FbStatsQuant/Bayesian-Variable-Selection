# PURE check (R7): Opus R6 corrections on NA_DROP v1.5

**All nine corrections were applied exactly as the R6 seat wrote them, nothing else changed, and none of them adds a premise or a claim. One inherited citation slip (WORDING). No QUALIFIER, no GENUINE GAP.**

**How I checked.** I did not use `apply_R6_corrections.py`. My script, `.rc_tmp/pureR7_opus/check.py`, reads the nine Old and New strings directly from `R6_council_opus.md`. It unescapes `` \` `` and `\n`; for S-1 the Old string is the rate line the seat quotes on line 41. It matches the Old strings whitespace-flexibly against `ticket_pre-R6`, inserts the seat's New text verbatim, and byte-compares the result with `ticket`. My scratch is under `.rc_tmp/pureR7_opus/` only. I touched no tracked file and did not modify `main97` or `bt*`.

## Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| a | ACCEPT | Each of the nine Old strings occurs exactly once in pre-R6 and 0 times in the final files. Each New string occurs 0 times in pre-R6 and exactly once in the final files. Locations: C-1 `lemmas/L3_listR.md:33-35`, S-3 `L3:43`, E-2 `L3:44`, C-2 `ERRATA.md:5`, S-4b `REPORT.md:66`, S-1 `REPORT.md:67`, S-4a `STATEMENT.md:24`, S-2 `STATEMENT.md:127`, E-1 `STATEMENT.md:170`. **F is absent:** "follow from (ii) and Step 3 without (D)" matches 0 times in all six files, and "idle" matches 0 times. |
| b | ACCEPT | Replaying pre-R6 plus the nine edits equals the final files **byte for byte** in all six files. CARD.md and READER_DELTA.md are identical to pre-R6, and their manifest hashes are unchanged. No line count moved: STATEMENT 170, REPORT 72, L3 125, ERRATA 7, CARD 23, READER_DELTA 43. All 36 EXT hashes are identical in the pre-R6 and final manifests. The EXT list matches the `#EXTRA` header. All 36 `main97` copies equal `git show 97f9c8c3:<path>`. |
| c | ACCEPT with 1 finding | **No hypothesis or claim is added to LIST-R** (details under "Item (c) in detail" below). S-1 is weaker than the old rate. S-2 equals what L3:116 proves. S-4a/b only scope the claim. C-1 aligns its clause with the clause before it. C-2 mirrors text already in L3. E-1 and E-2 are wording; E-2 is weaker. **S-3 adds two code facts.** They concern fields the proof does not use, and both are true at `main97`. Its citation `cpp/v3_core.cpp:787` is off by one (W-1). |
| d | ACCEPT | I ran `ingest.py convert` (same as `main97`) on a scratch copy of the final ticket. Exit 0, 3 records (LIST-K, LIST-CODE, LIST-R), stderr 0 bytes. `bvsreg.conclusion_level(strength)` for LIST-R gives `reported-model`. The LIST-R statement span is `STATEMENT.md` [100, 128] and the premises are `:29-64`. The (iii) block is still 4 lines (125-128). Line counts: STATEMENT 170, REPORT 72. The `rate` field parses as the S-1 text on a single line. `depends_on` is still the v1.1 list (LIST-K, LIST-CODE, RM2-R-plus, RM0-plus, DLV-0, POST). |
| e | ACCEPT | I built my own scratch repo, `.rc_tmp/pureR7_opus/vt`, the same way the coordinator does: `git init`, the 36 EXT files from `main97`, and the ticket at the same relative path. `main97`'s `manifest.py` (identical to the worktree copy) prints **`verify: OK MANIFEST 9ddef7fd70e2ccca867f44d452e32e028b814a6a98408b9a7cda59d58bc398be`**. As a cross-check, pre-R6 prints `verify: OK MANIFEST 148c9308…`. |
| f | ACCEPT | The status cell of REPORT.md:19 equals the `status:` text of REPORT.md:64 (string test True, 501 characters). `status_source: REPORT.md:19`. The convert's LIST-R status equals the same text. |

## Item (c) in detail

- **S-1 (`REPORT.md:67`): weaker, not stronger.** Write X_n for the error and Y_n := X_n·1_𝒪 for the error set to 0 off the output event. Then Y_n ≤ X_n, so X_n = O_P(r_n) implies Y_n = O_P(r_n), but not the reverse. Y_n is exactly the variable that L3:116 bounds ("X_n := 0 on 𝒪ᶜ").
- **S-2 (`STATEMENT.md:127`): equal.** The joint reading is the L3:116 argument: from {X_n > t} ⊆ 𝒪 ∩ (B₁ ∪ B₂ ∪ B₃)(t), the result P(𝒪 ∩ B(t_n)) → 0 for every t_n follows from Step 2. "No statement conditional on 𝒪" is a disclaimer.
- **S-4a (`STATEMENT.md:24`) and S-4b (`REPORT.md:66`): these describe the claim set, not the method.**
  - "Gains nothing beyond output runs" holds because (iii) gives the tagged method only output-run conclusions, which, as F notes, do not need (D).
  - "Under (D) as without it, these conclusions are on output runs only": every listed conclusion is already stated for "every admissible output run".
- **C-1 (`L3:33-35`): weaker.** It adds the restriction "matching guard inputs" to an internal comparison sentence. The clause just before it, already in v1.5, has the same phrase "for matching guard inputs", and R6 G1 accepted this reading. It is not a premise of LIST-R. "(The measured times themselves are not claimed equal)" is a disclaimer.
- **C-2 (`ERRATA.md:5`): not new.** The added clause repeats the existing L3:33 sentence ("so the new computation, which comes after the last guard consultation, cannot affect any guard decision"). ERRATA is not a claim file.
- **S-3 (`L3:43`): new code facts, both true.**
  - The first fact, that `finish` samples `runtime_guard$elapsed_seconds`, holds. The citation `v3_fit.R:80-82` is correct: 80 is `peak_memory_kb`, 81 is `timings$total`, and 82 calls `cpp_runtime_report`.
  - The second fact, the evaluation order on the exact branch, holds. In `v3_run.R:276`, `lf <- v3_list_fields(...)` runs before line 277 first touches `fit` (`fit$pip_primary` and the `fit` argument of `v3_add_list_fields`), and that touch forces the lazy `finish(fit)` from `v3_fit.R:131`.
  - The quote `IMPL_LIST_codeprint.md:42` matches "fields added after `finish()` (`v3_fit.R:131`, …)".
  - **But `g->elapsed()` is on `v3_core.cpp:789`, and the `return List::create(` that contains it opens at :788. Line 787 is the closing `}` of the records loop.** The other `v3_core.cpp` citations in L3 (358, 366, 459, 480, 558, 565) all match `main97`, so this is a slip in the R6 seat's text, applied verbatim.
- **E-2 (`L3:44`): weaker** ("at most K"), inside the "not a claim" note. **E-1 (`STATEMENT.md:170`):** a descriptive changelog edit.

## Findings

**W-1 · WORDING (inherited citation slip, not a PURE violation) · `lemmas/L3_listR.md:43`.**
- Replace: `` (`v3_fit.R:80-82`; `cpp/v3_core.cpp:787`) ``
- With: `` (`v3_fit.R:80-82`; `cpp/v3_core.cpp:788-789`) ``

The fact it cites is true; only the line is off. It can be folded in at the next touch of the ticket or at the A re-pin.

**A-1 · advisory, no change requested now · `STATEMENT.md:170`.** The v1.5 changelog row lists "(C3)(iii) and the registry conclusion" as changed. After S-1, the registry `rate` changed too (WEAKER, so the row's tag is still right). Suggested text for a later touch:
- Replace: `(C3)(iii) and the registry conclusion:`
- With: `(C3)(iii) and the registry conclusion and rate:`

**A-2 · advisory, no change requested now · `CARD.md:15` and `READER_DELTA.md:30`.** Both still say "O_P(√(log n/n)) … on output". STATEMENT.md:127 now defines "on output" as the joint reading, so these are consistent with that defined term. If the reader texts are touched at the re-pin, they could carry the same "(each error set to 0 off the output event)" gloss.

## Gates

- **G1 correctness: PASS.** The edits are the seat's texts verbatim. The weakened sentences (C-1, S-1) are implied by what Step 2, Step 3 and L3:116 prove. The S-3 code facts are true.
- **G3 faithfulness and scope: PASS.** No premise or claim is added. S-1 closes the R6 QUALIFIER. S-2 and S-4 scope the claim, they do not extend it.
- **G4 statuses and pins: PASS.** Verify is OK on 9ddef7fd (and on 148c9308 for pre-R6). Status :19 equals :64. EXT hashes are unchanged. W-1 is a line-citation slip on a field the proof does not use.
- **G5 registration form: PASS.** Convert exit 0, 3 records, empty stderr, `reported-model`, spans and line counts unchanged.

**Score: 9.5.** The PURE conditions hold exactly: byte-for-byte replay, the edits and only the edits, no added premise. Points off only for the inherited off-by-one citation in S-3 and the changelog row not naming the rate.

I did not write `PURE_R6_check_opus.md`, because this seat was told to change no file; this message is the verbatim text for the coordinator to save.

COUNCIL-VERDICT round=R7 manifest=9ddef7fd70e2ccca867f44d452e32e028b814a6a98408b9a7cda59d58bc398be seat=opus score=9.5 gates=PASS
