PURE check of `Sol3/Sol3-S3a-1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/s3a1/`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. `git apply --check` passes. On a scratch copy (`.rc_tmp/s3a1/patched.md`) the line count stays at 97. A character-level word-diff shows the only change is inside line 3's parenthetical: "conditions" becomes "the list", and "historical; the active conditions, at `CorGb-plus@1.0.3`, are W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P: " is inserted before "STATEMENT §5". The patch has exactly one removed line and one added line, both in PROOF.md.
2. The new text matches the card exactly. I pulled the replacement string out of row S3a-1, column (c), programmatically, and it appears verbatim in patched line 3, followed by the closing ".".
3. The new statement is correct. In `claims.tsv`, the row `W3-MISR-R:CorGb-plus` has version 1.0.3 and status "PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6df…, sol=10.0 PASS, opus=9.6 PASS". Its changelog cell says "was … W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P", which is the list the new header calls historical. `W3-D2/STATEMENT.md` §5 (line 79 on), lines 81-82, records `CorGb-plus@1.0.3` with the same three conditions.
4. The bold seat status ("PROVED (by this seat, unchecked), conditional on W3-POST2:C, …, C-MIS:Prop-P") is unchanged. The new wording doesn't contradict it: it says that list was carried from version 1.0.1 and marks it as historical.
5. No recorded claim span is touched. The patch changes only PROOF.md, so STATEMENT.md lines 29-48 (§1) and 50-58 (§2) are unchanged.
