# W3-READER — council round R4 (diff-only re-check), seat `opus` (single seat)

Manifest checked: `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-READER Theory_work/Wave3/W3-READER/reviews/MANIFEST_R4.txt`
printed `verify: OK MANIFEST 8d8bcd6f1519d9b6a0851efebff3b32273072a5c998f844ed6e1000470129ac6`.

Scope: `reviews/R4_diff_R3r3_to_R4.diff` (531 lines; CLAIMS_CARD, DEPS, READER_VERSIONS, REPORT, lemmas/R3, lemmas/R4).
Sources read: the current files; `claims.tsv` at fe05ccec (identical to origin/main 8bec550d for every row cited);
`W3-AUDIT-AX:REP` STATEMENT and `track_A_C/H5_T14_CARD.md` on origin/theory/W3-AUDIT; W3-AUDIT `TRACK_B.md` §S;
`W3-RM2-R/STATEMENT.md:71-93, 144-163` (DLV-0, IDEAL-W⁺, 𝔇); `W3-SAMP/STATEMENT.md:134`; code under
`Scripts/SMC_BVS/core/` (no diff against pin 4676af6); `reviews/R3_council_opus.md`, `R3_council_sol.md`.

## Per-item decisions

| tag | ACCEPT/REJECT | note |
|---|---|---|
| T14-REP (STRONGER) | ACCEPT | Card row 3.1 (`CLAIMS_CARD.md:70`) is the consultant's sentence (H5 card 16, edit 3) word for word. The caps, 𝔇, code lines and p_raw sit in the reader note (`:109-110`) and in Theorems 6 and 7 (`READER_VERSIONS.md:697, 849`). The text keeps both no-overclaim conditions: "Representable inputs still carry the other obligations of IDEAL-W (`2*p-1` in `int` for $p\ge2^{30}$)", and "default configuration (`v3.ls0_ell` unset)". It never says IDEAL-W⁺ = IDEAL-W. Arithmetic re-derived: $n,p_{\mathrm{raw}}\le2^{31}-1$ gives $n+p_{\mathrm{raw}}+1\le2^{32}-1$, so the base cap is at most 32, which is ≤ 10⁶. Also $\lfloor n/2\rfloor\le2^{30}-1$, so the search cap is at most $2^{30}+31<2^{31}-1$. Every representable input is therefore in 𝔇. DLV-0's 𝔇 clause holds "without the lift (DLV's IDEAL-W only) … with all other premises of (D) retained" (`W3-RM2-R/STATEMENT.md:86-89`), so "delivery holds under the remaining conventions (S4), without IDEAL-W⁺" is exact. Code: `v3_run.R:96` (`le > 1e6`), `cpp/v3_core.cpp:474` (`cap_ll > INT_MAX`), `:92` (`int n = X.nrow(), p = X.ncol()`), `cpp/v3_blocks.h:49` (`2 * p - 1`). STRONGER is the right tag: an informal remark becomes the checked `W3-AUDIT-AX:REP@1.0.0` ("PROVED-CHECKED; council R2, MANIFEST 5db04d3a…"), with no premise added or dropped. |
| B2 (GUARD-W wording) | ACCEPT | "returns no estimates; anything else it returns is flagged incomplete and is not covered" matches the code. `v3_fit.R:84` sets `partial_results <- TRUE` on `resource_limit`. `v3_fit.R:85` sets every estimate field to NA through `v3_unavailable_estimates` (`v3_run.R:110-113`). `v3_run.R:142-147` returns the HPM with `hpm_incomplete`, `estimates_available = FALSE` and `partial_results`. Guard sites: `cpp/v3_core.cpp:451, 459, 480, 637, 678`; `v3_calib.R:81, 113, 157`. The new wording is more accurate than "no output", because a guarded run does return a model, flagged incomplete. Citation precision: E6. |
| AUD-S4 | ACCEPT | Matches W3-AUDIT TRACK_B §S "Against core 3": their sampler statements are limits as N → ∞ at fixed data, for every data set; ours hold at the coded budget under design conditions; neither implies the other. The old "prove nothing about its selection output" is gone from row 3.1. Tag EQUAL (it concerns their paper). Precision: E5. |
| R3-O1 | ACCEPT | `READER_VERSIONS.md:1357`: semicolon. |
| R3-O2 | ACCEPT | `lemmas/R4_printed_outputs.md:49`: DLV-0's two C-DLV hypotheses are stated as discharged at main fe05ccec. Registry: `C-DLV:L2-S3@1.0.1` and `C-DLV:P1-Inventory@1.1.1` are each "CODE-CHECKED (second seat, code reading; …)". |
| REQUOTE | REJECT (one quote; see F1) | Every quote that carries a version tag matches `claims.tsv` at fe05ccec (scripted check over the card, READER_VERSIONS, lemma R4 and STATEMENT; the only mismatches were regex false positives). Verified rows: Thm-1@1.0.1; POST2 C/E/A1/A0 @1.0.6 and D@1.1.6; DIST Thm-A/Thm-B/Cor-C/DIST-C/DIST-1/DIST-2/B3 @1.0.1; SAMP C@1.1.5, TR@2.1.5, LT#@2.0.5, D@2.1.5; RM2-R-plus/RM2-F-plus/RM0-plus/DLV-0/Cont-plus @1.0.1; PoolZ and R4 @1.0.1; W1-N1:B and W1-N1:F. Nothing below PROVED-CHECKED is called checked: W1-N1:B/F are quoted as "PROVED under the named premises …" and listed under "What blocks". One untagged quote does not carry its condition (F1). Stale quotes outside the reader statements: E2, E3. |
| B1 | n/a (moot confirmed) | No row's status now carries a C-DLV condition: the RM2-R-plus family @1.0.1 is plain "PROVED-CHECKED; council R3, …". |
| narrative | ACCEPT with E items | The card v1.13 header, the "Status refresh (2676e71f)" bullet and the thm1/thm10 limits follow the requote. Defects: a broken sentence (E1), a resolved item still listed as a blocker (E4), and rewritten history lines (E3). |
| bookkeeping (DEPS) | ACCEPT | I recomputed the sha256 prefixes of CARD (`a2d47c9f135c61fc`), R4 (`fa325f32103d4843`) and R3 (`7aa1218565ecc7b2`); all three match. |

## Findings

### F1 — card row 4.1 quotes `W3-SAMP:LT#` as plain "PROVED-CHECKED" without its condition (F, minor; G4)
`CLAIMS_CARD.md:82`, a line this diff edits (the PoolZ requote): "(`W3-SAMP:LT#` (LT-d), "PROVED-CHECKED")". Since relabel
2676e71f the registry reads `W3-SAMP:LT#@2.0.5` **"PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, MANIFEST
68480a72…, astra=9.1 PASS, opus=8.8 PASS"**. Row 3.6 (`:75`) quotes it in full. Row 4.1 drops the condition, which breaks the
ticket rule "'conditional on …' is carried" (`BRIEF.md:52`). The REQUOTE item says every row was requoted. The condition
is plausibly material here: the code bridge W1-N1:B is what makes the coded `pip_primary` the island mean of T12's frozen
runs, and LT-d is stated for that output (`W3-SAMP/STATEMENT.md:134`). "What blocks" (2) (`:155`) also leaves row 4.1 out.
**Correction:** at `:82`, replace `` (`W3-SAMP:LT#` (LT-d), "PROVED-CHECKED"; `` with
`` (`W3-SAMP:LT#@2.0.5` (LT-d), "PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, …"; ``. In the status
column, replace "proved (LT-d); PoolZ PROVED-CHECKED" with "proved (LT-d; conditional on W1-N1:B, W1-N1:F); PoolZ
PROVED-CHECKED". At `:155`, replace "(rows 3.6, 2.1 body)" with "(rows 3.6, 4.1, 2.1 body)".
The fix is wording only. No reader theorem statement changes.

### Editorial (E) — not counted in the score
- **E1** `READER_VERSIONS.md:180-181`: the requote left a broken sentence. It now reads "…PROVED-CHECKED through
  `SOP:TH09`; the `W3-POST:Thm-1` row keeps its" and then, on a new line, "Thm-1 therefore carries the label above and no open
  condition." Replace the tail of :180 and all of :181 with: "…PROVED-CHECKED through `SOP:TH09`, and `W3-POST:Thm-1@1.0.1`
  now carries the label above and no open condition (relabel, main 2676e71f) [REG-2676]."
- **E2** `lemmas/R4_printed_outputs.md:6-7`: the header still quotes `W3-POST:Thm-1` item 6 as "T03♯: PROVED; SF VERIFIED
  (W2-VT03R); XF VERIFIED (A-REV2)", while :22 of the same file quotes @1.0.1 "PROVED-CHECKED; council C3, …". Requote
  the header to match :22. At :12, the stray "(main 33e1f0f5) [S4-F1]" now follows a [REG-2676] quote. Drop it or write
  "(history: main 33e1f0f5)". `REPORT.md:46` `depends_on` bumps `W3-SAMP:C` to @1.1.5 but leaves `W3-POST:Thm-1@1.0.0`.
  Bump both, or leave the ingest block as history and revert the SAMP bump.
- **E3** History lines rewritten. R2-O10 settled that changelog and update-log lines stay byte-identical as history,
  with corrections made in new lines. This diff instead rewrites old dated lines, and some now misstate the registry at
  their date:
  - `READER_VERSIONS.md:317` (thm2 v0.4) and `:1372` (thm10 v0.8) now say "`W2-APP:POST@1.0.7` conditional on SOP:TH09
    only". At 33e1f0f5 that was @1.0.6; @1.0.7 has always been unconditional "PROVED-CHECKED".
  - `:794` (thm6 v0.5) changes @1.0.6 to @1.0.7. At f526e45b it was @1.0.5, so both values are wrong.
  - `CLAIMS_CARD.md:147` (bullet "Status refresh (main 6cd699dd → 14892123)") says Thm-1 "keeps its label
    'PROVED-CHECKED; council C3, …'". At 14892123 the label was "T03♯: PROVED; …".
  - `CLAIMS_CARD.md:7` (v1.9) drops "3.6" from "rows 1.2, 3.6 carry no open registry condition". That was true at
    v1.9.
  - `CLAIMS_CARD.md:6` (v1.10), `READER_VERSIONS.md:806` (thm6 v0.9) and `:1384` (thm10 v1.1) now quote the B2 wording,
    tag included, as if it had been added at those versions.

  Fix: restore these lines byte-for-byte from fe05ccec. The new facts are already recorded in the v1.13 header, the new
  "Status refresh (2676e71f)" bullet and the FRZ-B log lines.
- **E4** `CLAIMS_CARD.md:155-156`: "What blocks a fully PROVED-CHECKED card" item (3) lists the two C-DLV audits while
  saying they are discharged. Delete (3), or rewrite it as "Resolved since v1.12: the two C-DLV delivery-path audits
  (CODE-CHECKED, main fe05ccec)".
- **E5** AUD-S4 sentence, `READER_VERSIONS.md:1200` and `CLAIMS_CARD.md:63`. In the Theorem 9 context, "ours hold at the
  coded budget under design conditions" omits Corollary 9C's own premise on the run: the returned list must carry
  posterior mass $\ge n^{-cM/2}$. The row states that premise earlier, so nothing is hidden, but the comparison sentence
  is loose. Suggested: "ours hold at the coded budget under design conditions (Corollary 9C also needs the returned list to
  carry posterior mass $\ge n^{-cM/2}$)". The audit also cites supp pp. 9–10 (weighted averages, (13)–(15)), so cite
  "supplement pp. 9–10, 12–13, 16–17" in rows 3.1, 2.1 and thm9.
- **E6** B2 code citation (all eight occurrences). `v3_fit.R:84` only sets `partial_results`. The "no estimates" step is
  `v3_fit.R:85` (and `v3_run.R:147`). Write "(`v3_fit.R:84-85`; `v3_run.R:110-113, 142-147`)".

## Interpretive sentences in changed text (D71)

| location | sentence | verdict |
|---|---|---|
| Card:70; RV:697, 849 | "in the default configuration neither can be reached on any input R can represent …, so this matters only for the $n\to\infty$ form" | SUPPORTED (AX:REP (REP-a), (REP-b); DLV-0 𝔇 clause; representable ⊂ 𝔇 re-derived) |
| RV:697, 849 | "IDEAL-W⁺ is used only by the asymptotic form" | SUPPORTED (`W3-RM2-R/STATEMENT.md:89`: "𝔇 is bounded, so the asymptotic conclusions … are stated under IDEAL-W⁺") |
| Card:70-75; RV:698, 850, 1317, 1323 | guarded run: `resource_limit`, no estimates, the rest flagged incomplete and not covered | SUPPORTED (code above) |
| Card:63, 70; RV:1200 | Song–Liang sampler statements are iteration limits at fixed data; neither implies the other | SUPPORTED (TRACK_B §S core 3; precision E5) |
| Card:70 | "no result at the coded computational budget … known to us" | SUPPORTED as a hedged literature statement (TRACK_B U3) |

## Gates (judged on the diff)

| gate | result | note |
|---|---|---|
| G1 correctness of changed text | PASS | T14-REP arithmetic and code facts re-derived, and the B2 code paths traced. Rewritten history lines (E3) and a broken sentence (E1) are editorial. |
| G3 faithfulness to masters | PASS | T14-REP is exactly AX:REP plus DLV-0's 𝔇 clause, with the consultant's two no-overclaim conditions kept. No change claims more than its master. |
| D71 | PASS | Table above. |
| G4 statuses verbatim | **FAIL** | F1: card row 4.1 drops LT♯'s "conditional on W1-N1:B, W1-N1:F". All version-tagged quotes match. |
| G5 hidden finite-n / scope | PASS | Default configuration and the remaining IDEAL-W obligations are stated. No finite-n claim is added. "So this matters only for the $n\to\infty$ form" is exact. |
| G6 code facts | PASS | `v3_run.R:95-97, 110-113, 142-147`; `v3_fit.R:84-85`; `cpp/v3_core.cpp:92, 473-474`; `cpp/v3_blocks.h:49`, all at pin 4676af6 (no diff). |

Out-of-scope changes: none. Every hunk maps to a tagged item or to bookkeeping.

## Score and fidelity

Score (C, S, F only): **7.9**. The single minor F1 is a one-phrase status completion and needs no re-derivation. Once it
is applied, I would accept the round at about 9.4. Under the brief this failure is wording only: the edits are
otherwise correct, and the R3r3 fallback is not warranted on substance. The reader theorem statements (Theorems 6, 7, 9,
10, the row 3.5 remark, and card rows 2.1, 3.1, 3.2, 3.5, 3.6) are faithful to their masters. F1 concerns the status quote
of a Pillar-4 card row, not the content of any reader statement.

FIDELITY: FAITHFUL

COUNCIL-VERDICT round=R4 manifest=8d8bcd6f1519d9b6a0851efebff3b32273072a5c998f844ed6e1000470129ac6 seat=opus score=7.9 gates=FAIL
