# W3-READER — council round R5 (diff-only re-check of the R4 fixes), seat `opus` (single seat)

Manifest checked: `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-READER Theory_work/Wave3/W3-READER/reviews/MANIFEST_R5.txt`
printed `verify: OK MANIFEST 9f1104743b12c1358bc5b2bbb8266c7bac345fe81f4d6bf213f25b052b80df52`.

Scope: `reviews/R5_diff_R4_to_R5.diff` (244 lines). I regenerated it as `git diff b4123f62 7405a463 -- <ticket>`, with
reviews/ and LOG.md excluded, and the result is byte-identical (`cmp`). Between 7405a463 and HEAD 1cb14acb the ticket has no
change outside reviews/ and LOG.md.

Sources read:
- the current files;
- `claims.tsv` (last changed at fe05ccec; every row cited below was read there);
- `CLAIMS_CARD.md` and `READER_VERSIONS.md` at fe05ccec, for the history check;
- `W3-DIST/STATEMENT.md:217-238` (Cor-C);
- origin/theory/W3-AUDIT `TRACK_B.md:244-245, 388-390, 418, 429`;
- `Scripts/SMC_BVS/core/v3_fit.R:80-86` and `v3_run.R:108-148` (no diff against pin 4676af6);
- my R4 review and the R4 brief.

Scratch: `reviews/R5_scratch_opus/` (regenerated diff and copies of the fe05ccec, R4 and R5 files).

## Per-finding decisions

| R4 finding | ACCEPT/REJECT | note |
|---|---|---|
| F1 (G4) row 4.1 LT♯ quote | ACCEPT | `CLAIMS_CARD.md:82` now reads `W3-SAMP:LT#@2.0.5` (LT-d), "PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, …". This matches the registry status ("… council R1, MANIFEST 68480a72…, astra=9.1 PASS, opus=8.8 PASS"), shortened with "…" in the same way as the other card quotes. The status cell reads "proved (LT-d; conditional on W1-N1:B, W1-N1:F); PoolZ PROVED-CHECKED". PoolZ@1.0.1 is plain "PROVED-CHECKED; council R3, …" in the registry, so it correctly carries no condition. "What blocks" (2) at `:155` now names "rows 3.6, 4.1, 2.1 body". Fixed as I specified. |
| E1 broken sentence (thm1 master block) | ACCEPT | `READER_VERSIONS.md:180` is one sentence that ends "…`W3-POST:Thm-1@1.0.1` now carries the label above and no open condition (relabel, main 2676e71f)." "The label above" is the :179 quote, which matches the registry. Thm-1@1.0.1 is plain "PROVED-CHECKED; council C3, …", so "no open condition" is true. Small style point (E-c): "; and". |
| E2 stale quotes (R4 header, R4:12, REPORT:46) | ACCEPT | `lemmas/R4_printed_outputs.md:5` quotes Thm-1@1.0.1 "PROVED-CHECKED; council C3, MANIFEST 420c1cb0…, astra=8.8 PASS, opus=8.7 PASS", matching the registry and :22. The stray "(main 33e1f0f5)" is gone from :10. `REPORT.md:46` now depends on `W3-POST:Thm-1@1.0.1`. The same header edit also dropped ", T03♯ discharged" after the POST@1.0.7 quote. That part of the header requote is true and redundant, it changes no claim, and I count it inside E2. The unchanged tail of the same line still has a stale R1 quote (E-b). |
| E3 history lines restored | ACCEPT | Scripted check against fe05ccec. In both files, every history line (card `v1.N =` changelog lines and the "Status refresh" bullets; READER_VERSIONS update-log items `- v…`, `- FRZ…`, `- R…`, `- S…`, `- R2-ED…`) is byte-identical to fe05ccec. The only additions are the v1.13 header, the new "Status refresh (2676e71f)" bullet and the FRZ-B lines. I also diffed every continuation line: the only changes are in current-status text (thm1/thm6/thm9 master paragraphs and limits, all from R4), not in log entries. The six lines I named in R4 are each restored: card v1.9 (with "rows 1.2, 3.6"), card v1.10, the 14892123 bullet (with the "T03♯: PROVED; …" label), thm2 v0.4 (@1.0.6), thm6 v0.5 (@1.0.6), thm6 v0.9, thm10 v0.8 (@1.0.6) and thm10 v1.1. The restored lines keep their original text, errors included (for example thm6 v0.5 still says @1.0.6 where it should be @1.0.5). That is correct under R2-O10: corrections go in new lines. |
| E4 "What blocks" item (3) | ACCEPT | `CLAIMS_CARD.md:155` now says "The two delivery-path code-reading audits of rows 3.1–3.2 are discharged (main fe05ccec)." Registry: `C-DLV:L2-S3@1.0.1` and `C-DLV:P1-Inventory@1.1.1` are each "CODE-CHECKED …". |
| E5 AUD-S4 (Cor 9C premise; pp. 9–10) | ACCEPT | The new parenthesis "(and, for Corollary 9C, given that the returned list carries posterior mass at least $n^{-cM/2}$)" matches the Cor-C master (`W3-DIST/STATEMENT.md:228-229`: "every completed run … with π(𝒯) ≥ n^{−cM/2}"). The page citation "supplement pp. 9–10, 12–13, 16–17" matches TRACK_B `:244-245, 388, 418, 429`. Both are applied at card rows 2.1 and 3.1 and at Theorem 9 (3) (`READER_VERSIONS.md:1199`). Placement nit in row 3.1: E-a. |
| E6 B2 code citation | ACCEPT | All 8 current occurrences (4 in the card, 4 in READER_VERSIONS) now read "(`v3_fit.R:84-85`; `v3_run.R:110-113, 142-147`)". The code agrees. `v3_fit.R:84` sets `partial_results <- TRUE` on `resource_limit`. `:85` calls `v3_unavailable_estimates` when `estimates_available` is not TRUE. `v3_run.R:110-113` is that function (estimate fields set to NA, `estimates_available <- FALSE`). `v3_run.R:142-147` gives the HPM, `hpm_incomplete`, `partial_results`, and `v3_unavailable_estimates` at :147. The only remaining `v3_fit.R:84` without a range is in the thm6 v0.9 history line (`:805`), which is correctly unchanged. |
| out-of-table changes | none | Every hunk maps to F1 or E1–E6, or to DEPS bookkeeping. In DEPS, `checked_by` was relabelled, and I recomputed shas: CARD `5b43ee74c8801745`, R4 `e67dd737a0e5407e` and R2 `6f70b56635abab50` all match the files. R2 OK = sha equals checked_sha. |

## Findings

No C, S or F finding.

### Editorial (E) — not counted in the score
- **E-a** `CLAIMS_CARD.md:70` (row 3.1, Buys column). The E5 parenthesis "(and, for Corollary 9C, given that the returned
  list carries posterior mass at least $n^{-cM/2}$)" was pasted into the Theorem 6 row. That row's comparison concerns
  Theorem 6 and never mentions Corollary 9C, so the clause is a non sequitur there. It is true and claims nothing, but it is
  out of place. My R4 E5 asked for the premise only in the Theorem 9 context and for the page citation in all three
  places. Fix: delete the parenthesis from row 3.1 and keep it in row 2.1 and in Theorem 9 (3).
- **E-b** `lemmas/R4_printed_outputs.md:5` (on a line changed by E2, but the text itself is unchanged). The line still says
  "this ticket's bridges R1 (B2.1, B6.1) "PROVED (by this seat, unchecked)"". That quotes `lemmas/R1_set_sizes.md:3`,
  but the registry has `W3-READER:R1@1.0.1` as "PROVED-CHECKED; council R3, MANIFEST 7aebdf2e…, sol=9.5 PASS, opus=9.4
  PASS". It understates the status and overclaims nothing, so it does not trip G4's no-overclaim purpose. Fix: "this
  ticket's bridges R1 (B2.1, B6.1), `W3-READER:R1@1.0.1` "PROVED-CHECKED; council R3, …"". I missed this in R4. The local
  file headers of R1–R3, the PoolZ STATEMENT header and REPORT ingest status lines are bookkeeping for the recorder.
- **E-c** `READER_VERSIONS.md:180`: "…through `SOP:TH09`; and `W3-POST:Thm-1@1.0.1` now carries…". Use "…through
  `SOP:TH09`, and `W3-POST:Thm-1@1.0.1` now carries…" (or drop "and").

## Interpretive sentences in changed text (D71)

| location | sentence | verdict |
|---|---|---|
| Card:63, 70; RV:1199 | "ours hold at the coded budget under design conditions (and, for Corollary 9C, given that the returned list carries posterior mass at least $n^{-cM/2}$); neither implies the other" | SUPPORTED (Cor-C master; TRACK_B U3, §S core 3). Placement in row 3.1: E-a. |
| Card:155 | "The two delivery-path code-reading audits of rows 3.1–3.2 are discharged (main fe05ccec)" | SUPPORTED (registry CODE-CHECKED rows) |
| RV:180 | "`W3-POST:Thm-1@1.0.1` now carries the label above and no open condition" | SUPPORTED (registry) |
| Card:70-75; RV:697, 849, 1316, 1322 | guarded run: `resource_limit`, no estimates, the rest flagged incomplete and not covered (citation now 84-85 / 142-147) | SUPPORTED (code above) |

## Gates (judged on the diff)

| gate | result | note |
|---|---|---|
| G1 correctness of changed text | PASS | Each changed sentence was checked against the registry, the master or the code. History lines were checked byte-for-byte against fe05ccec. |
| G3 faithfulness | PASS | No change claims more than its master. E5 adds a premise and F1 adds a condition, so both make the text weaker or more exact. |
| D71 | PASS | Table above. |
| G4 statuses verbatim | PASS | LT#@2.0.5, Thm-1@1.0.1 (card, RV:179-180, lemma R4 :5 and :22), PoolZ@1.0.1, C-DLV audits and REPORT `depends_on` all match `claims.tsv`. The stale R1 quote (E-b) is pre-existing, understates the status and asserts no condition away. |
| G5 hidden scope | PASS | The Cor 9C premise is now explicit in the comparison. No finite-n or scope claim was added. |
| G6 code facts | PASS | `v3_fit.R:84-85`; `v3_run.R:110-113, 142-147` at pin 4676af6 (no diff in `Scripts/SMC_BVS/core/`). |

Out-of-scope changes: none.

## Score and fidelity

Score (C, S, F only): **9.6**. All of R4's findings, F1 and E1–E6, are applied correctly and completely. The R4 gate
failure, G4 (F1), is closed exactly as specified, and the history restore is byte-exact. What remains is three editorial
nits (E-a, E-b, E-c). None of them affects a reader statement, a status gate or fidelity. The reader theorem statements and
card rows touched by this diff stay faithful to their masters.

FIDELITY: FAITHFUL

COUNCIL-VERDICT round=R5 manifest=9f1104743b12c1358bc5b2bbb8266c7bac345fe81f4d6bf213f25b052b80df52 seat=opus score=9.6 gates=PASS
