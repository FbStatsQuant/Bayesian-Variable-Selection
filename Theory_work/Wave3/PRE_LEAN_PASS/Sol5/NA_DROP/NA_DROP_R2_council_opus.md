# NA_DROP R2 council review (Opus seat): v1.2 to v1.3, manifest 8fb12543

**Manifest verify:** `python3 Theory_work/Wave3/tools/manifest.py verify …/Sol5/NA_DROP/ticket …/MANIFEST_NADROP13.txt` printed `verify: OK MANIFEST 8fb12543d716f3878e0a23fbd3e36072bc27b59dcf602f1d4918c21e5c067eee` (exit 0). The v1.2 ticket also verifies (`2443df85…`).

**Other checks I ran:**
- **Diff:** I rebuilt the diff from `v1.2_ticket/` and `ticket/` with `diff -u`. It is byte-identical to `NADROP_v1.2_to_v1.3.diff`.
- **Staged files:** the sha256 prefixes and line counts of the 5 files match the brief: c968e071/168, e81a564b/129, a649e9a2/72, 46be3814/23, a3fd959d/45.
- **Claimed edits:** all are present where the grep table says.
- **The three `stop()` lines:** `v3_run.R` lines 251, 253 and 263 hash to `8af9f9b7653c0ef0…` in all three places: `git show 61b0a582:v3_run.R`, `git show 7100bb3b:Scripts/SMC_BVS/core/v3_run.R` and the working tree. There is no core diff between 7100bb3b and HEAD.
- **Converter:** `ingest.py convert` on the staged REPORT gives exit 0 and 3 records. But see F-1: convert passes while the LIST-R conclusion level no longer parses.

**Kinds of finding I hold:** WORDING only (F-1, C-1, C-2, S-1, S-2, E-1 to E-3), plus one mechanical manifest-pin item (G4-1). I found no QUALIFIER and no GENUINE GAP. Every step I checked against the code of record holds.

## Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 (b-1) | ACCEPT | `L3_listR.md:36-45`. All three `stop()` rows of `v3_list_fields` are named, and each reason is correct against the code:<br>(i) **Count mismatch.** `store_to_list` (`cpp/v3_core.cpp:358-362`) fills `M[i]` and `v[i]` in one loop over `s.s`. The sampler store reaches the fit via `:366` → `:510` → `v3_run.R:141,210`; the exact store via `:565`.<br>(ii) **Duplicate model.** Follows from L2 (iii)/(iv), plus injectivity of `to_orig` (C-1).<br>(iii) **Column outside the retained set.** `to_orig` (`:38-42`) writes `D.orig[S[i]]`. `D.orig` is built from the same `orig` that `cpp_context` returns (`cpp/v3_core.cpp:93,105`; `v3_setup.R:7-10`), and that is the `ctx$orig` passed in.<br>The other error paths are base-R ones, not `stop()` rows. None can fire on an output run, but (0.5) does not argue it (C-1). The exact-branch call-site pointer is missing (C-2). |
| 1 (Step 0′) | ACCEPT | `L3_listR.md:51-66`. The list of NA rows is complete against the code: `res("empty_list")` at `:249` and `res("nonfinite_score")` at `:254, :256` are the only NA returns. Absent fields come only from `v3_fit.R:176` (status other than completed) and `v3_run.R:275` (status other than exact). `log_Z_list` is finite (F_max finite, den ∈ [1, m]). (o) is still proved. One attribution is wrong: the two implementation guards are credited to "SPEC §4" (S-1). |
| 2 (b-2) | ACCEPT | `CARD.md:10` ("When p≥2 for all large n, …"), `CARD.md:13` ("for the rate: p≥2 for all large n") and `READER_DELTA.md:30` all match STATEMENT (C3)(ii) "Rate (p ≥ 2 for all large n)" (`STATEMENT.md:119`) and (iii) (`:127`). The REGISTRY rate line `REPORT.md:67` already carried "(p >= 2)". No other rate statement in CARD, READER_DELTA or REPORT lacks the qualifier. |
| 2 (b-3) | ACCEPT | Discharge wording is present at REPORT `:9, :19, :26, :64, :70` and CARD `:10`. It matches `reviews/IMPL_LIST_codeprint.md` §5 ("IMPL-LIST: DISCHARGED at method-v3.1.1-listpip (7100bb3b)") and the registered method field of `W3-D5P:LIST-R`. The v1.3 review status is kept separate ("review of v1.3 pending", `:19, :64`). Wording rider E-3 (CARD), pin rider G4-1. |
| 2 (b-4) | ACCEPT on F-1 | `REPORT.md:66`. (o) is now its own clause, covers all three fields with a finite `log_Z_list`, and matches `STATEMENT.md:104-105`. The data-event sentence no longer carries the non-NA statement. But the edit pushed the level tag `reported-model:` out of first position, so the conclusion level no longer parses (F-1). |
| 3 (pointers) | ACCEPT | STATEMENT changed only line 1 (in place) and appended line 168, so no span shifts. REPORT spans `:100-128`, `:29-64`, `:68-76`, `:80-96`, `:60-64`, `:83-89`, `:100-102` all check out on the v1.3 text. REPORT hunks replace lines 1:1, so `status_source` lines 17/18/19 still hold. No file cites L3 by line number, so the +7 lines in L3 shift nothing. |
| 3 (changelog v1.3) | ACCEPT | `STATEMENT.md:168` lies outside every claim span. The tag "EQUAL (proof completion and derived-text corrections; no statement changes)" is right: the diff touches no text in `:29-64` or `:68-128`. |
| 3 (convert / markers / consistency) | ACCEPT on F-1 | Convert exits 0 with 3 records, and the IMPL-LIST inline definition converts in full (no bars). The LIST-R conclusion level parses as `'(o) every admissible … [na-b4]; reported-model'`, which is not in `CONCLUSION_LEVELS` (F-1). `[NA-b1]` is at L3 `:38, :54` and `[NA-b4]` at REPORT `:66`. Statements of (o) and of the rate now agree across STATEMENT, L3, REPORT, CARD and READER_DELTA. |

**Item-1 verdict:** `(b-1) (0.5) COMPLETE AND CORRECT` (with WORDING riders C-1 and C-2; no missing `stop()` row, no wrong reason).

## Findings

**F-1 [F, WORDING, must be applied before freeze] `REPORT.md:66`: LIST-R conclusion level unparsable.**
- **What breaks:** `bvsreg.conclusion_level` (`Theory_work/INFRA/tools/bvsreg.py:946-947`) takes the text before the first `:`. The v1.3 line gives `'(o) every admissible output run, … [na-b4]; reported-model'`; v1.2 gave `'reported-model'`.
- **Consequences:**
  - `check.py:358-360` raises a WARN S1-schema "conclusion level … unknown".
  - `ingest.py:459-461` raises a PROBLEM when the conclusion goes through strength ingest.
  - `compare()` loses the level axis.
- **Why the converter didn't catch it:** `ingest.py convert` does not check the level, which is why it exits 0.
- **Fix:** replace
  `conclusion: (o) every admissible output run, on either branch and for every data set, prints pip_list, mpm_list and a finite log_Z_list [NA-b4]; reported-model: on Theorem 6's data event`
  with
  `conclusion: reported-model: (o) every admissible output run, on either branch and for every data set, prints pip_list, mpm_list and a finite log_Z_list [NA-b4]; on Theorem 6's data event`
  and leave the rest of the line unchanged. Apply as written.
- **Tested** on a scratch copy (`.rc_tmp/r2opus/fixtest/`): convert exits 0 with 3 records, and the levels are identity, identity, reported-model.

**C-1 [C, WORDING] `L3_listR.md:36-45`: (0.5) asserts "can end the fit with an error only through the three `stop()` rows" but does not exclude base-R errors.**
The claim holds; I checked each base-R error path. Two changes:
- At `:41-42`, replace "hold distinct models (L2 (iii), (iv));" with:
  "hold distinct models (L2 (iii), (iv)), and `to_orig` is injective (`D.orig` strictly increasing, `v3_setup.R:8`), so their comma-joined keys are distinct;"
- After "assigns a position in 1..p to every stored column." insert:
  "No other line of `v3_list_fields`, `v3_add_list_fields` or `v3_exact_list_last` (`v3_run.R:245-279`) can raise an error on an output run: `integer(max(orig))` needs p ≥ 1, which holds since p = 0 returns `no_predictors` before branching (`v3_preprocess.R:114`, `v3_fit.R:99-102`); `names(pip) <- pip_names` (and `setNames` in `res`) needs length(`pip_names`) = p, which holds since `pip_names` is `names(fit$pip_primary)`, of length p by `v3_run.R:161-162` (sampler), or `names(e$pip)`, of length p by `cpp/v3_core.cpp:558` and `v3_exact.R:9` (exact); the remaining operations (`vapply` of `paste`, `exp`, `log`, indexing within 1..m) raise no error."

Apply as written.

**C-2 [C, WORDING] `L3_listR.md:44-45`: call-site pointers for (iii).**
- The exact-branch call is `v3_run.R:276`, reached through `v3_exact_list_last` from `v3_fit.R:131`; it is not cited.
- `v3_run.R:220` never runs inside `v3_fit`, because `v3_fit.R:162` passes `list_fields = FALSE`.
- **Fix:** replace "(`ctx$orig`, built from `pre$kept` at `v3_fit.R:118` and passed at `:176`; `v3_run.R:160, 220`)" with:
  "(`ctx$orig`, built from `pre$kept` at `v3_fit.R:118`; passed at `:176` on the sampler branch and, on the exact branch, at `v3_run.R:276` through `v3_exact_list_last` (`v3_fit.R:131`); `v3_run.R:160, 220` is the same vector in a standalone `v3_final_run`, which `v3_fit` calls with `list_fields = FALSE`, `v3_fit.R:162`)".

Apply as written.

**S-1 [S, WORDING] `L3_listR.md:53-54`: the stop rows are attributed to SPEC §4.**
SPEC §4 (@523dda23) has only the duplicate-model row. Count mismatch and out-of-set column are implementation guards. Two replacements:
- "SPEC §4 makes a field NA (or absent) only in these rows:" becomes "SPEC §4, as implemented by `v3_list_fields` and `v3_exact_list_last` (`v3_run.R:245-279`), makes a field NA (or absent) or stops only in these rows:".
- "a count mismatch, a duplicate model or a column outside the retained set (the three `stop()` rows," becomes "a duplicate model (SPEC §4) and the implementation's two guards, a count mismatch and a column outside the retained set (the three `stop()` rows,".

Apply as written.

**S-2 [S, WORDING] `L3_listR.md:29`: stale "pending" wording.**
(0.5) still says "the method after the pending commit that adds the fields", while the same paragraph cites lines of that commit and b-3 now records the discharge.
- **Fix:** replace "LIST-R is about the method after the pending commit that adds the fields." with "LIST-R is about the method with the fields, `method-v3.1.1-listpip` (7100bb3b; IMPL-LIST discharged there, `reviews/IMPL_LIST_codeprint.md` §5)."
- **Leave unchanged:** `STATEMENT.md:16, :60, :62` ("method commit, pending", "to be discharged"). That text sits in the locked premise span `:29-64`, and editing it would be a statement change. The status belongs in REPORT/CARD, as staged.

Apply as written.

**E-1 [E, WORDING] `L3_listR.md:37`: "byte-identical" is true but vacuous.**
`git rev-parse 7100bb3b:Scripts/SMC_BVS/core` = 61b0a582, so the "core tree" and the tag are the same object.
- **Fix:** replace "these three lines are byte-identical at the core tree 61b0a582 and at `method-v3.1.1-listpip`, 7100bb3b" with "at `method-v3.1.1-listpip`, 7100bb3b, whose core tree is 61b0a582; `v3_run.R` is unchanged from e9bac478".

Apply as written.

**E-2 [E, WORDING] `READER_DELTA.md:8-9`: stale clause.**
"until that commit exists the text below speaks of 'quantities computed from the returned list'" is out of date, and line 15 already says "The method prints".
- **Fix:** replace with "the method companion exists at `method-v3.1.1-listpip` (7100bb3b)."

Apply as written.

**E-3 [E, WORDING] `CARD.md:10`: ambiguous review status.**
"is reviewed separately (NA_check_opus; Sol-5 (b))" can be read as "has been reviewed".
- **Fix:** replace with "is under separate review (v1.2: NA_check_opus; Sol-5 (b) R1 FAIL, points b-1 to b-4 applied in v1.3; review of v1.3 pending)".

Apply as written.

**G4-1 [S, mechanical pin; apply as written] manifest `#EXTRA` list.**
- **Problem:** the new IMPL-LIST status (REPORT `:19, :26, :64, :70`; CARD `:10`) rests on `Theory_work/Wave3/W3-D5P/reviews/IMPL_LIST_codeprint.md`. That file is not among the 32 `#EXTRA` inputs, and `manifest.py` skips `reviews/` (`SKIP_DIRS`, `manifest.py:50`).
- **Fix:** at the re-freeze, add `#EXTRA Theory_work/Wave3/W3-D5P/reviews/IMPL_LIST_codeprint.md` (sha256 `72a2d781cfe7e3d786fb6640f6109d5a4f22b87cdcf5ec73d84017c61eae6fb2`; on main since df1f5872).

Optional and not a finding: `[NA-b2]` and `[NA-b3]` markers are not placed at the CARD and READER_DELTA edits.

## Gates
- **G1 correctness: PASS.** (0.5) and Step 0′ hold against the code of record. C-1 and C-2 are wording completions.
- **G3 faithfulness and scope: PASS** on S-1, S-2, E-1 to E-3 as written. (o) and the rate are consistent across the five files. No claim text changed, so the EQUAL tag is right.
- **G4 statuses and pins: PASS** on G4-1 as written. IMPL-LIST discharge is correctly stated, and there is no claim that v1.3 is reviewed.
- **G5 registration form: PASS** on F-1 as written. As staged, the LIST-R conclusion level is unparsable; with F-1 applied, convert gives exit 0, 3 records and level reported-model.

Under the HQ rule, `gates=PASS` holds because every finding is WORDING (or a mechanical pin) to be applied as written. F-1 is mandatory before the next freeze.

## Scores
- C (correctness): 9.1
- S (scope / faithfulness): 9.0
- F (form / registration): 8.4
- Overall: 8.8

COUNCIL-VERDICT round=R2 manifest=8fb12543d716f3878e0a23fbd3e36072bc27b59dcf602f1d4918c21e5c067eee seat=opus score=8.8 gates=PASS
