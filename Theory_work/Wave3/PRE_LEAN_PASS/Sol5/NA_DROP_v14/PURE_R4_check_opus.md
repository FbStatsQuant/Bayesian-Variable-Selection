I did not write `Sol5/NA_DROP_v14/PURE_R4_check_opus.md`, because the task said to change nothing. The review is below for the manager to file. All scratch work is in `.rc_tmp/pure_r4_opus/`, and the tracked tree is still clean.

# PURE check: Opus R4 corrections on NA_DROP v1.4 (manifest 906961f6…)

**Verdict: PURE.** I took each finding's Old and New text straight from `R4_council_opus.md`, using a regex over the review itself rather than the staged apply script. I applied them, whitespace-flexibly, to the pre-R4 ticket. The result is byte-identical to the final ticket in all three changed files: `L3_listR.md`, `STATEMENT.md` and `ERRATA.md`. My script is `.rc_tmp/pure_r4_opus/pure.py`.

**What I ran myself:**
- **Manifest verify.** I built my own batch tree at `.rc_tmp/pure_r4_opus/bt`, using the same recipe as `freeze_on_batch.sh` but without touching the shared `.rc_tmp/bt`.
  - Final ticket: `verify: OK MANIFEST 906961f65d79919a89f4de4626ccc5d2144f1a09974397800cc1208ae2b0ba69`.
  - Pre-R4 ticket: `verify: OK MANIFEST 5d06f5c6…62333cb`.
  - The pre-R4 manifest file is byte-identical to `MANIFEST_NADROP14_b330.txt`.
- **ingest convert.** I ran `ingest.py convert` on a scratch copy of the final REPORT.md. It exited 0, wrote 3 records (LIST-K, LIST-CODE, LIST-R) and nothing to stderr. `bvsreg.conclusion_level(strength)` gives `reported-model` for LIST-R and `identity` for LIST-K and LIST-CODE.
- **Unchanged files.** REPORT.md, CARD.md and READER_DELTA.md are byte-identical to the pre-R4 versions (`cmp`).

## Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 | ACCEPT | **F-1, `ERRATA.md:5`.** The Old tail "; optionally: on the exact branch … (`v3_fit.R:115-117`) and `:121-122` creates the list" occurred once in the pre-R4 file and is now deleted. "optionally" and ":121-122" no longer appear anywhere in ERRATA. |
| 2 | ACCEPT | **C-1, `L3_listR.md:49`.** Old occurred once; New is present once and Old is absent. Code facts re-read on the batch tree: `v3_fit.R:131` is `return(v3_exact_list_last(finish(fit), e, ctx))`. In `v3_run.R:274-279`, `fit` is not forced at :275 on the exact branch, `v3_list_fields` runs at :276, and `fit` is first forced at :277. So the qualifier is correct as worded. |
| 3 | ACCEPT | **S-1, `STATEMENT.md:169`.** Old once, New once. "existing IDEAL-W⁺ premise" is gone. `L1_resources.md:95-96` is Lemma R's "R-level copies and the serialised fit … the factor 2" passage, which matches the citation. |
| 4 | ACCEPT | **S-2 correction 1, `L3:49`.** Old once, New once. `L1_resources.md:73` is W̄ := C_W[…] and `:78` is M̄ := 2·C_M[…], so 2(C_M+8)𝔅_M follows. |
| 5 | ACCEPT | **S-2 correction 2, `L3:49`.** Old once, New once. The parenthesis sits where the seat's wording puts it (see W-2, optional). |
| 6 | ACCEPT | **C-2, `L3:49`.** The anchor "holds with the same polynomial allocation formulas." occurred once; the added sentence follows it, once. M_G is not defined in L3 or in RM2-R `STATEMENT.md`; it is defined only in FABLE_ALLOC_CARD §3 (see W-3, optional). |
| 7 | ACCEPT | **S-3, `L3:118`.** Old once, New once. On whether this adds a premise, see item 12. |
| 8 | ACCEPT | **C-4 correction 1, `L3:45`.** Old once, New once. `v3_preprocess.R:112` is `kept <- which(!constant); …`, which matches. |
| 9 | ACCEPT | **C-4 correction 2, `L3:45`.** Old "(`v3_run.R:245-269`)" occurred once; New once. The wrapper `v3_exact_list_last` is at `:274-279`, which matches. |
| 10 | ACCEPT | **C-3, E-1 and S-4 are not applied.** Their distinctive texts appear 0 times in all six ticket files: "guard consultation of the tagged fit is preceded", "applied in L3 (0.5), v1.4", and the S-4 remark text. `ERRATA:5` still has the plain "[applied]". `STATEMENT:35` is unchanged, since lines 1-168 are identical. |
| 11 | ACCEPT | **Nothing else changed.** The line counts are unchanged (169 / 131 / 7). The diff touches only `STATEMENT:169`, `L3:45, 47 (wrapped line of 49's block), 118` and `ERRATA:5`. My independent application reproduces the final files byte for byte, so no edit exists outside the nine applied texts. The 46-line `NADROP_v1.4_pre-R4_to_final.diff` matches this. |
| 12 | ACCEPT | **(b) No new premise.** S-3's "its envelopes dominate the pinned core's, so (0.4) applies" is the seat's text, verbatim. It is an inference from material already in (0.6) and adds no premise. The tagged constants C_W+1 ≥ C_W and C_M+8 ≥ C_M make the tagged envelopes dominate the pinned ones, and C-2 gives M_G + T_M ≥ M_G for the shipped-code envelopes. So a declared allocation that satisfies (D) for the tagged method also satisfies it for the pinned core, and (0.4) (DLV-0 for the core) applies. The C-1, S-1, S-2 and C-2 texts add parentheticals and citations to existing objects (Lemma R, MACH's β/β₀ clause, RM2-R's re-derivation); none adds a hypothesis. The S-1 changelog cell still ends "no new premise", and that is now true under a correct attribution. |
| 13 | ACCEPT | **(c)** ingest convert exits 0 with 3 records, and LIST-R's level is `reported-model`. REPORT.md, CARD.md and READER_DELTA.md are byte-identical to pre-R4. |
| 14 | ACCEPT | **(d)** The LIST-R spans `STATEMENT.md:100-128` and premises `:29-64` are byte-identical (lines 1-168 are identical; the only change is at :169, after every span). |
| 15 | ACCEPT | **(e)** The last cell of ERRATA row E1 equals card §6 (ii)'s "New cell" exactly: same bytes, 874 characters including the quotes. Nothing follows the closing quote before " \|". `E1_new_cell.txt` equals the cell without its quotes. |
| 16 | ACCEPT | **Claimed-edits table** `NADROP14_R4_CLAIMED_EDITS_GREP.txt` (FAILS 0): each claimed edit is at the stated line. They are `ERRATA.md:5` (F-1), `L3_listR.md:45` (C-4), `:49` (C-1, S-2, C-2), `:118` (S-3) and `STATEMENT.md:169` (S-1). The digest matches the brief. |

## Findings

All are **WORDING**, optional, and do not affect PURE. Each applies only if HQ wants an R5 touch; otherwise none is needed.

- **W-1 (WORDING), `L3_listR.md:49`, C-1 text.** "the bounds below do not depend on this order" sits after T_M ≤ 16·𝔅_M and T_W ≤ 𝔅_W, which are stated earlier, so "below" covers only Lemma R's constants.
  - Possible replacement: "and the bounds below do not depend on this order" → "and the bounds of this paragraph do not depend on this order".
- **W-2 (WORDING), `L3_listR.md:49`, S-2 correction 2.** The literal placement gives "the brackets (the first with factor 16) 𝔅_M, 𝔅_W of C-DLV Lemma R". The parenthesis separates "brackets" from their names.
  - Possible replacement: "the right sides are sums of terms of the brackets (the first with factor 16) 𝔅_M, 𝔅_W of C-DLV Lemma R at (n, p_raw)" → "the right sides are sums of terms of the brackets 𝔅_M, 𝔅_W of C-DLV Lemma R at (n, p_raw) (the first with factor 16)".
- **W-3 (WORDING), `L3_listR.md:49`, C-2 text.** M_G appears in L3 only here. It is defined in neither the cited `W3-RM2-R/STATEMENT.md:76-79` nor `L1_resources.md`; its definition is in FABLE_ALLOC_CARD §3.
  - Possible replacement: "whose word bound M_G ≥ M̄" → "whose word bound M_G = M̄ + C·K(K+1) ≥ M̄ (`PRE_LEAN_PASS/Sol5/FABLE_ALLOC_CARD.md` §3)".

There is no QUALIFIER finding and no GENUINE GAP.

## Gates

- **G1 correctness: PASS.** The texts add no step, and the code facts behind C-1, C-4 and S-2 check out on the batch tree.
- **G3 faithfulness and scope: PASS.** All nine texts are applied verbatim and nothing else changed. C-3, E-1 and S-4 are absent.
- **G4 statuses and pins: PASS.** REPORT is byte-identical, the level is `reported-model`, and the digest verifies OK on the batch tree.
- **G5 registration form: PASS.** Convert gives 3 records with an empty stderr. The LIST-R spans and premises are unchanged.

**Score: 9.3.** The application is exactly PURE; the three optional wording notes concern the seat's own phrasing, not the application.

COUNCIL-VERDICT round=R4 manifest=906961f65d79919a89f4de4626ccc5d2144f1a09974397800cc1208ae2b0ba69 seat=opus score=9.3 gates=PASS
