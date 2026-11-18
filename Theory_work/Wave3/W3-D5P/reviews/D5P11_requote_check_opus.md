# W3-D5P v1.1: READER card / READER_VERSIONS requote check. PART 1: status quotes (Opus one-shot, recorder-requested; NOT a council seat)

Reviewer: Claude Opus 5.5 (one-shot subagent, read-only), task D5P v1.1, 2026-11-18, dry run on main 83a633db. Subject: CLAIMS_CARD.md:71 (row 3.1L) and READER_VERSIONS.md:1432-1433 (§11.2): "pending recording" replaced by the recorded statuses of
W3-D5P:LIST-R, LIST-K, LIST-CODE (@1.0.0). Registry read: the dry clone after the recording. The reviewer's report follows verbatim. Recorder's remark: that report was written on the first dry run, whose two new prose sentences were the recorder's; HQ then ordered two other sentences verbatim (card :71, READER_VERSIONS :1433), which are checked in Part 2 below. The status-quote parts are unchanged between the two runs.

REQUOTE-VERDICT: PURE

The edit is a faithful requote. Every pin and status quote matches the registry. No statement, hypothesis or conclusion text of Corollary 6L changed, and both line counts are unchanged. There is one citation-location imprecision (item 7) and one attribution that is not literally in D120 (section C). Neither claims more than the sources support.

Scope: the diff is byte-identical to `git diff -U0` in the clone. Changed lines: CLAIMS_CARD.md:71, READER_VERSIONS.md:1432 and :1433. Card :71: the closing bold sentence of the statement cell ("Pending recording: not presented as a software statement until IMPL-LIST lands." -> "Recorded (see the status column); IMPL-LIST is discharged; presenting 6L as a software statement is HQ's card decision.") and the master part of the status cell. RV :1432: heading suffix only. RV :1433: first sentence and master status part. Corollary 6L's body (RV :1435-1441, Remark :1443) and the "Inputs:" parts are not in the diff.

A. Checks (all MATCH unless stated):
1-4. `W3-D5P:LIST-R@1.0.0`, `LIST-K@1.0.0` "PROVED-CHECKED; council R4, …" and `LIST-CODE@1.0.0` "CODE-CHECKED (code reading at core 4676af6); council R4, …" equal the registry statuses up to the abbreviated council digest (MANIFEST bb35f65d…, sol=9.5 PASS, opus=9.6 PASS); LIST-R has no "conditional on"; A:IMPL-LIST is still listed in LIST-R's assumptions but assumptions.tsv marks it DISCHARGED (HQ ruling (i)) and the LIST-R notes say "plain PROVED-CHECKED".
5. Tag `method-v3.1.1-listpip` = 7100bb3b5a341aed5cbcd3b03fa5851a6345f0dd (merge of PR #80), an ancestor of HEAD 83a633db: MATCH.
6. IMPL_LIST_codeprint.md:199 (the file's last line) reads exactly `IMPL-LIST: DISCHARGED at method-v3.1.1-listpip (7100bb3b)`: MATCH on wording.
7. MISMATCH, literal location only: that line sits after §6 "SUPERSEDED (route b′ not taken)" (:141-199), not at the end of §5; §5 (:110 to about :139) contains the discharge reasoning and the recording instruction ("With IMPL-LIST discharged, LIST-R carries no open premise … status plain PROVED-CHECKED, method pin `method-v3.1.1-listpip` (7100bb3b)"). The registry cites "§5" too.
8-11. Inputs unchanged and true: W3-RM2-R:RM2-R-plus, RM0-plus, DLV-0 @1.0.1 "PROVED-CHECKED; council R3, …"; W2-APP:POST@1.0.7 "PROVED-CHECKED".
12-13. Line counts unchanged: CLAIMS_CARD.md 181, READER_VERSIONS.md 1458. 14. Corollary 6L text unchanged.

B. Nearby sentences still saying "pending recording" (version-log text, historical): CLAIMS_CARD.md:2 (v1.14 header) and READER_VERSIONS.md:810 (update log v1.0). Nothing in row 3.1L or §11.2 still says "conditional on IMPL-LIST" or "not in the registry".

C. The two new sentences: "Recorded" and "IMPL-LIST is discharged" are supported by the registry and the codeprint; "presenting 6L as a software statement is HQ's card decision" defers rather than claims. No decision in Dept/DECISIONS.md says "HQ's card decision": D120 (DECISIONS.md:463) says "Cor 6L: not presented as a software statement until IMPL-LIST lands (before the Lean freeze)"; read literally D120's gate is now met. The RV parenthesis attributing the gate to D120 is a mild misattribution. No contradiction with the registry or nearby text; no overclaim.

D. Residual concerns: (1) LIST-R's `assumptions` still lists A:IMPL-LIST ("unconditional" rests on assumptions.tsv marking it DISCHARGED). (2) LIST-CODE's status pins "code reading at core 4676af6" (re-pin to the tag is a later step): the row mixes a 4676af6 pin with a 7100bb3b discharge. (3) the "§5" locator is imprecise (item 7). (4) the "HQ's card decision" wording needs HQ's confirmation or a D-number other than D120. (5) the run log says "5 line replacements" (in-line substitutions) while the diff shows 3 changed lines: cosmetic.


# PART 2: HQ's two ordered sentences (Opus one-shot, read-only, 2026-11-18, second Opus reviewer)

Subject: CLAIMS_CARD.md:71 and READER_VERSIONS.md:1432-1433 as edited by the recorder (main 13be759b). HQ's text, verbatim: card :71 "Recorded (see the status column); IMPL-LIST is discharged at method-v3.1.1-listpip; presented as a statement about the frozen software once the code re-pin to that tag is recorded." (inside the existing bold markup); READER_VERSIONS :1433 "Presented as a software statement once the code re-pin to method-v3.1.1-listpip is recorded." Reviewer's report, verbatim:

REQUOTE-VERDICT: PURE

(a) MATCH. CLAIMS_CARD.md line 71, statement cell: HQ's sentence (1) appears exactly once, wrapped in `**…**`, ending the statement cell after a single space in the place of the old bold sentence. READER_VERSIONS.md line 1433 starts with HQ's sentence (2) exactly, followed directly by " Source:" as the old sentence was.
(b) MATCH. Line counts unchanged: CLAIMS_CARD.md 181, READER_VERSIONS.md 1458; a line-level diff shows only the hunks at :71 and :1432-1433.
(c) MATCH. Only three lines changed. CLAIMS_CARD.md:71 (5 cells in both versions): cells id, gain, class identical; statement cell: only sentence (1) changed; status cell: the status-quote replacement ("pending recording … conditional on IMPL-LIST until Engineering's method commit is code-read" became the LIST-R@1.0.0 / LIST-K@1.0.0 / LIST-CODE@1.0.0 quotes), " Inputs:" onward identical. READER_VERSIONS.md:1432: heading suffix "— pending recording" -> "— recorded (W3-D5P)". :1433: first sentence = sentence (2); " Source:" up to "Master" identical; the Master part is the status-quote replacement (label "Master:" -> "Master, recorded:"), byte-identical to the new card status cell; " Inputs:" onward identical.
(d) MATCH. Corollary 6L's text is unchanged: the card statement cell up to "…needs the raw-scale bridge (open)." and READER_VERSIONS §11.2 lines :1434-1444 (statement, display, Remark :1443); §11.3 and everything after unchanged.
(e) MATCH. The old card sentence appears 0 times in line 71 of the new file; the old READER_VERSIONS sentence appears 0 times in line 1433. A search of the whole files for "until IMPL-LIST lands" finds only CLAIMS_CARD.md:2.
Residual concern (reviewer): CLAIMS_CARD.md line 2 (v1.14 version header, unchanged) still reads "new row 3.1L (Corollary 6L, pending recording, not a software statement until IMPL-LIST lands; …)"; outside this edit's scope, historical version-log text; HQ may want it re-quoted in a later edit.
