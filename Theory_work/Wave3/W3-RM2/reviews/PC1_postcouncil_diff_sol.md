MANIFEST d2b379495d8b9408c20aad7417a723390a128e187f4d408e2e2186e4d91b5de0

## Verify / bind outputs

Run from `C:/Users/felip/BVS-wt/W3-RM2`:

`python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2 Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1.txt`

```text
CHANGED ASSUMPTION_MAP.md
CHANGED REPORT.md
CHANGED SHARPNESS.md
CHANGED STATEMENT.md
CHANGED lemmas/L2_width.md
CHANGED lemmas/L3_assemblyF.md
CHANGED numerics/RESULTS.md
verify: 7 difference(s) vs MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a
```

Exit 1 is the expected difference result. Exactly the seven authorized texts changed; every other R1 manifest entry, including the external inputs and code pins, is unchanged. No missing file or other difference was reported.

`python Theory_work/Wave3/tools/manifest.py bind Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1.txt Theory_work/Wave3/W3-RM2/reviews/C_R1_council_astra.md Theory_work/Wave3/W3-RM2/reviews/C_R1_council_opus.md`

```text
bind: OK, 2 review(s) give a PASS verdict (>= 8.0) on MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a
council cell: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

Exit 0. Also ran the same verify command against `reviews/MANIFEST_PC1.txt`:

```text
verify: OK MANIFEST d2b379495d8b9408c20aad7417a723390a128e187f4d408e2e2186e4d91b5de0
```

Exit 0. Independently SHA-256 hashed all seven saved council texts (the snapshot directory uses flat basenames) against their corresponding R1 rows:

| Text | Snapshot SHA-256 | Result |
|---|---|---|
| STATEMENT.md | 86478dc78041fcb87600fdd8872f24d14f4b6a7c683b4535ca6cd1565d6a08e2 | MATCH |
| REPORT.md | 429898c17b4ab61d893be1c864b83c5b337556d9c1a8932825a19635ba8c8780 | MATCH |
| SHARPNESS.md | 971f809f8210fa5b012462e9494ddd6b091aaff3be2e190f5f6093059fe939d5 | MATCH |
| ASSUMPTION_MAP.md | 7fc7a2b4ad04bb38353de7d620ac7bee18c0451c5eae12583712fd4ca4431ac1 | MATCH |
| lemmas/L2_width.md | a4f59502eb292b5cdbe4df404d35790e062f08de30993590bcee0c7861f1352a | MATCH |
| lemmas/L3_assemblyF.md | 2a65ad0fcdd6b70d07a853c531abef81181fc73d143fa95c2444bb1f1e0352ee | MATCH |
| numerics/RESULTS.md | 112d441a97d59b12ec8d766573740952ab987f4d604ae8bdc07643dc1c03fef1 | MATCH |

## Hunks: all seven files

Compared every pair with GNU `diff --strip-trailing-cr -u` (Git's bundled executable; plain `diff` was not on PATH). These are all 12 unified-diff hunks, with old/new coordinates. Classification: (a) a correction expressly required by a council finding; (b) record/editorial; (c) substantive. Neither seat required a change for the council pass. F1 alone is expressly REQUIRED before registry ingest by Opus; its pointer corrections are marked (a) in that limited sense. The other applied recommendations are (b), even when responding faithfully to a finding.

### STATEMENT.md

1. `@@ -253,7 +253,7 @@` ? **(b), F5.** Replaces the P9 row's ?median?mean? description with a probability-? ? event plus lower-tail concentration about the mean of a Lipschitz functional; adds [C1-F5]. Faithfully describes the unchanged proof in L5:100?106: probability at least ? below ?s?_n, versus probability at most exp(?2) below E??2. No P9 hypothesis or conclusion changes.
2. `@@ -304,7 +304,7 @@` ? **(b), F10.** Adds `@1.0.0` to Lemma-BC and [C1-F10]. This harmonizes an already identified input with the version already recorded in the frozen REPORT example registry entries; it changes no dependency or code pin.

### REPORT.md

1. `@@ -33,9 +33,10 @@` ? **(b), council result.** Replaces the future council placeholder with R1 PASSED, Astra 9.5, Opus 8.8, all six gates PASS, no finding required for council pass. Keeps HQ audit pending and preserves the unchecked claim statuses. Faithful to both council reviews; Opus's separate before-ingest F1 requirement is resolved below.
2. `@@ -99,11 +100,12 @@` ? **(b), F2 and review-trail records.** Moves the interrupting dispositions line below the table, completes its listed disposition families, adds the RC6 record consistently with C1_disposition, and replaces the future council placeholder with the R1 result. The table is contiguous. The numerical scores and gate verdicts are faithful. The separate RC6 review was not opened, as required by the read restrictions.
3. `@@ -117,7 +119,8 @@` ? **(b), F7.** Narrows ?one line of each proof? to the junk-exclusion payment in each sandwich proof, and explicitly records Form R's additional b < ? uses in L5 (S2) and P9a Step 4. No budget is changed.
4. `@@ -154,12 +157,13 @@` ? **mixed (a)/(b), F1 and council records.** The RM2-F status_source becomes REPORT.md:73, its current own row: faithful (a) before-ingest correction. The introductory explanation that correct/council now record R1 while lit/necessity/better remain PENDING is (b). No status upgrade occurs.
5. `@@ -167,70 +171,70 @@` ? **mixed (a)/(b), F1, F3, F7 and council records.** The other 17 status_source pointers are corrected to their own current rows: faithful (a) before-ingest corrections. In each headline theorem, correct becomes PASS with the two R1 reviews, better remains PENDING but now names BT2_disposition.md, and council becomes the full bound R1 cell: (b), faithful to the final-statement review pointer correction and the council result. The RM2-R sharpness evidence adds L5 (S2) and P9a Step 4: (b), faithful F7. Assumptions, consumed claims, dependency identities, conclusions and statuses are unchanged.

### SHARPNESS.md

1. `@@ -9,7 +9,8 @@` ? **(b), F7.** Qualifies the single junk-exclusion payment as a sandwich-proof description and adds the two further Form R uses. The existing beta and epsilon budgets remain identical. L5:20?23 and :82?85 explicitly support the added wording.

### ASSUMPTION_MAP.md

1. `@@ -24,14 +24,14 @@` ? **(b), F4 and F5 (two changed rows within one hunk).** Replaces the nonexistent ladder (3.3) reference with L1 (2.2)?(2.3) and Step 2(b), exactly the correction identified by Opus. Replaces the P9 ?median?mean? description with the probability-? ?/lower-tail-mean description, supported by L5:100?106. These changes repair references/descriptions, not the mapping's mathematical conditions. L1 itself was not opened under this brief's read restrictions.

### lemmas/L2_width.md

1. `@@ -4,7 +4,7 @@` ? **(b), F6.** Header now says written for v1.3 and unchanged for Form F in v1.4, with [C1-F6]. Proof and lemma statements are byte-unchanged outside the header replacement.

### lemmas/L3_assemblyF.md

1. `@@ -4,7 +4,7 @@` ? **(b), F6.** Same header clarification, with [C1-F6]. Assembly, hypotheses and containment argument are unchanged.

### numerics/RESULTS.md

1. `@@ -1,5 +1,10 @@` ? **(b), A2.** Adds the final-count opening note, labels sections 1?3 as the historical 207-run snapshot superseded by ?4, and retains the validated LS0 re-implementation/start-mode/nominal-classification qualifications. This changes the presentation of existing results, not numerical data or conclusions. Independently checked counts below.

No hunk is (c). All nine applied corrections listed in C1_disposition are accounted for. F8 and F9 remain untouched because L4 and L1 are unchanged in the R1 verification; F11's C1 parenthetical and L3 proof are also unchanged in the seven-pair diffs. They remain non-required NITs, not newly introduced changes.

## Registry-block checks

All 18 status_source targets are in REPORT ?3 and point to their own clause rows (SAND/TL superscript notation versus registry hyphen notation denotes the same claim):

| Registry claim (W3-RM2:) | REPORT.md line | Own row |
|---|---:|---|
| RM2-F | 73 | (C1) RM2-F |
| RM2-R | 79 | (C2) RM2-R |
| Toolkit-b | 67 | (P0) Toolkit-b |
| SAND-F-b | 68 | (P1) SAND-F^b |
| TL-F-b | 72 | (P2) TL-F^b |
| NA-W | 69 | (C3)(a) NA-W |
| W-conv | 70 | (C3)(b) W-conv |
| W-suff | 71 | (C3)(c) W-suff |
| Cont-F | 74 | (C4) Cont-F |
| SAND-R-b | 75 | (P7) SAND-R^b |
| F-to-R | 76 | (P8) F-to-R |
| D-to-W | 77 | (P9) D-to-W |
| POST-R | 78 | (P10) POST-R |
| Cont-R | 80 | (C4) Cont-R |
| Ex-PolyR | 81 | (C5) E2 Ex-PolyR |
| Ex-PolyF | 82 | (C5) E3 Ex-PolyF |
| Ex-Proxy | 83 | (C5) E4 Ex-Proxy |
| Ex-Equi | 84 | (C5) E5 Ex-Equi |

The current targets are one line later than the council's suggested numbers because REPORT ?1 gained one line; using the council's old absolute numbers verbatim would now be wrong. The applied recomputation is faithful.

Both `council:` values (REPORT:175 and :187) were programmatically compared for exact equality with the full `council cell:` value emitted by bind: both match. Every PASS/PENDING filename exists, checked individually relative to the ticket root: reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, ASSUMPTION_MAP.md, SHARPNESS.md, reviews/BT2_disposition.md. BT2_disposition was checked for existence only, not read.

REPORT ?1:36?39 and ?4:107 agree with both reviews: Astra score 9.5, Opus score 8.8, G1?G6 individually PASS for each seat, matching both COUNCIL-VERDICT lines. ?No REQUIRED finding? is accurate for council pass; Opus separately required F1 before ingest, and all its pointer corrections are now resolved. Claims remain ?PROVED (by this seat, unchecked)?; HQ audit and headline-strength decisions remain pending.

## Opening numerical note

Parsed all 26 summary.csv cells and summed the numerator/denominator of `end_S0`: 204/208. Exactly one cell has a numerator below its denominator: type B4, eta=1, n=1600, b=0.375, `end_S0=2/6`, hence four failures among six. This exactly matches the added note. All other cells total 202/202. No new numerical run or mathematical inference was introduced.

ATTESTATION: editorial/record only ? the package stands as passed by council round R1

Remaining required change: none for this post-council diff check; F1's before-ingest requirement is satisfied. HQ acceptance and the explicitly pending strength decisions are outside this attestation.

## Checks performed / not checked

Performed both manifest verifications, seven saved-text SHA-256 checks, all seven CR-normalized unified diffs (12 hunks), finding/disposition reconciliation, all 18 own-row pointer checks, exact equality of both council cells with bind, all registry PASS/PENDING filename-existence checks, score and six-gate comparison with both council reviews, the restricted L5 wording checks, and summary.csv count aggregation.

This is a change-scope review, not a fresh proof review. Did not rerun simulations, re-prove unchanged results, validate external inputs beyond manifest identity, inspect implementation contents, read L1/L4 contents, inspect BT2's contents, or make an HQ acceptance decision. No LOG.md, CHECKPOINT file, or unlisted review was read. Only the brief's permitted inputs were inspected (plus directory names to locate the flat council snapshots); the prescribed manifest commands performed the requested hash checks. No subagents were started, no effort setting above high was used, and no git command or git-state change was made. This review is the sole file written.
