# R06FIX recheck 2 — Sol correctness review

**R2-F2 OPEN (MAJOR).** The four exact round-2 examples are fixed, but the same acceptance boundary still admits conditional or negative parenthetical remarks and decisions split across physical lines, continuation rows, or a remarks column. Five new variants pass real staged carrier ingest with a checked label and zero acceptance errors.

Reviewed branch `infra/R06-eol`, commit `4952705d0e8da9f5be9a589b894ed7fd025f2c9e`. All test runs used my own `git clone --no-hardlinks` under <code>C:/Users/felip/AppData/Local/Temp/r06-recheck2-sol-17b6055a/repo</code>, followed by checkout of `infra/R06-eol`. No implementation or git-state changes in the supplied worktree; only this requested report was written there. No subagents used.

## Findings

1. **Conditional/negative remarks still accept.** [bvsreg.py:1299](C:/Users/felip/BVS-wt/INFRA-R06/Theory_work/INFRA/tools/bvsreg.py:1299)–1323 allows arbitrary balanced parenthetical text unless it matches a limited blacklist. <code>accepted (conditional)</code>, <code>ACCEPT (if lemma B holds)</code>, <code>accepted (decision: NO)</code> and <code>accepted (verdict: NOT)</code> all return true, with no table problem. Negations after punctuation and Unicode variants also evade the blacklist. The closed outer syntax is not a closed disposition grammar.

2. **Physical-line and continuation-row truncation still accept.** [bvsreg.py:1338](C:/Users/felip/BVS-wt/INFRA-R06/Theory_work/INFRA/tools/bvsreg.py:1338)–1356 accepts incomplete pipe rows and ignores empty-id continuation rows. <code>ACCEPT\nNOT-EXAMINED</code> returns true in the decision table although `decision_accepts` on that whole string returns false. Likewise <code>&#124; A &#124; ACCEPT &#124;\n&#124; &#124; NOT-EXAMINED &#124;</code> returns `REV:A=True` with no problem. U+2028/U+2029 within the original single decision cell are now correctly rejected; LF/CRLF still produce this bypass.

3. **Disqualifying remarks columns are ignored.** [bvsreg.py:1290](C:/Users/felip/BVS-wt/INFRA-R06/Theory_work/INFRA/tools/bvsreg.py:1290) splits every pipe and [bvsreg.py:1353](C:/Users/felip/BVS-wt/INFRA-R06/Theory_work/INFRA/tools/bvsreg.py:1353) examines only cell 2. A row with decision ACCEPT and remarks `withdrawn` or `only if proof repaired` is accepted. Neither row-width validation nor a cross-cell ambiguity check prevents this.

4. **Additional conservative/formatting mismatches.** Harmless <code>accepted (proof verified; no blocking issues)</code> and <code>accepted (no blocking issues)</code> are rejected by the `blocking`/initial-negation blacklist. These are false negatives rather than acceptance bypasses. `_plain` deletes all stars/backticks, including unmatched/interior markers: <code>ac`cept</code> and <code>ac**cept</code> become ACCEPT. Those malformed strings are conservatively expected false; the major verdict does not depend on their formatting interpretation.

Fix direction: use a genuinely constrained decision/remark grammar that excludes conditions and hedges, validate complete Markdown rows, and reject dispositions whose meaning continues into another row or disqualifying remark. Keep benign remarks distinguishable from contradictory decisions. Add the staged variants below as regressions.

## Parser input/output matrix

Each decision string is inserted verbatim into `| A | <decision> |` after `| id | decision |` and its separator. `Expected` follows the requested acceptance semantics plus the documented fail-closed punctuation convention (`Accepted.` may refuse). Balanced Markdown emphasis/code around the whole positive token and harmless parenthetical remarks are positive controls; unmatched/interior markup is expected to refuse. `Actual` is `seat_decisions(text, "REV")[0].get("REV:A", False)`. `Cell` additionally shows `decision_accepts` before table parsing. JSON escapes show exact separators/escaping. Structural cases have their full text below.

95 cases: 26 mismatches (24 false positives, 2 false negatives). No mismatched case generated a parser problem.

| # | Group | Input | Expected | Actual | Cell | Result |
|---|---|---|---|---|---|---|
| 1 | positive | <code>ACCEPT</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 2 | positive | <code>accepted</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 3 | positive | <code>accept</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 4 | positive | <code>AcCePt</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 5 | positive | <code>aCcEpTeD</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 6 | positive | <code> ACCEPT </code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 7 | positive | <code>**ACCEPT**</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 8 | positive | <code>`accepted`</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 9 | positive | <code>accepted (F-1 verified)</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 10 | positive | <code>accepted with non-blocking remarks</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 11 | positive | <code>accepted with non-blocking remarks (F-1 verified)</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 12 | positive | <code>accepted (proof verified; no blocking issues)</code> | ACCEPT | NOT ACCEPTED | NOT ACCEPTED | **MISMATCH** |
| 13 | positive | <code>accepted (all checks pass)</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 14 | positive | <code>accepted (checked (details verified))</code> | ACCEPT | ACCEPT | ACCEPT | OK |
| 15 | prior F2 / R2-F2 | <code>ACCEPT=NO</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 16 | prior F2 / R2-F2 | <code>ACCEPT/NOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 17 | prior F2 / R2-F2 | <code>accepted, no</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 18 | prior F2 / R2-F2 | <code>ACCEPT not</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 19 | prior F2 / R2-F2 | <code>accepted (not accepted)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 20 | prior F2 / R2-F2 | <code>ACCEPT : NO</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 21 | prior F2 / R2-F2 | <code>accepted with remarks; withdrawn</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 22 | prior F2 / R2-F2 | <code>ACCEPT\u2028NOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 23 | punctuation / negative / strict grammar | <code>NOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 24 | punctuation / negative / strict grammar | <code>not-examined</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 25 | punctuation / negative / strict grammar | <code>NoT-ExAmInEd</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 26 | punctuation / negative / strict grammar | <code>NO</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 27 | punctuation / negative / strict grammar | <code>NOT</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 28 | punctuation / negative / strict grammar | <code>rejected</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 29 | punctuation / negative / strict grammar | <code>not accepted</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 30 | punctuation / negative / strict grammar | <code>acceptable</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 31 | punctuation / negative / strict grammar | <code>accepted-ish</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 32 | punctuation / negative / strict grammar | <code>ACCEPT.</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 33 | punctuation / negative / strict grammar | <code>ACCEPT!</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 34 | punctuation / negative / strict grammar | <code>accepted unconditionally</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 35 | punctuation / negative / strict grammar | <code>ACCEPT:</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 36 | punctuation / negative / strict grammar | <code>accepted; withdrawn</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 37 | punctuation / negative / strict grammar | <code>ACCEPT (NO)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 38 | punctuation / negative / strict grammar | <code>ACCEPT (NOT)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 39 | punctuation / negative / strict grammar | <code>ACCEPT ((not accepted))</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 40 | punctuation / negative / strict grammar | <code>accepted (later rejected)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 41 | punctuation / negative / strict grammar | <code>accepted (pending review)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 42 | punctuation / negative / strict grammar | <code>accepted (withdrawn)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 43 | punctuation / negative / strict grammar | <code>accepted (blocking gap)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 44 | punctuation / negative / strict grammar | <code>accepted (not-examined)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 45 | punctuation / negative / strict grammar | <code>accepted (status: not accepted)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 46 | punctuation / negative / strict grammar | <code>accepted (retracted)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 47 | punctuation / negative / strict grammar | <code>accepted (failed proof)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 48 | punctuation / negative / strict grammar | <code>accepted (no blocking issues)</code> | ACCEPT | NOT ACCEPTED | NOT ACCEPTED | **MISMATCH** |
| 49 | hedged / disposition in remark | <code>accepted (conditional)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 50 | hedged / disposition in remark | <code>ACCEPT (if lemma B holds)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 51 | hedged / disposition in remark | <code>accepted (only if revised)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 52 | hedged / disposition in remark | <code>accepted (subject to verification)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 53 | hedged / disposition in remark | <code>accepted (probably)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 54 | hedged / disposition in remark | <code>accepted (tentative)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 55 | hedged / disposition in remark | <code>accepted (unless a counterexample appears)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 56 | hedged / disposition in remark | <code>accepted (decision: NO)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 57 | hedged / disposition in remark | <code>accepted (verdict: NOT)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 58 | hedged / disposition in remark | <code>accepted (status: NOT-EXAMINED)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 59 | hedged / disposition in remark | <code>accepted (status: not: accepted)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 60 | hedged / disposition in remark | <code>accepted (status: not/accepted)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 61 | hedged / disposition in remark | <code>accepted (status: **NOT**-EXAMINED)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 62 | hedged / disposition in remark | <code>accepted (status: rejected)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 63 | hedged / disposition in remark | <code>accepted (decision: no, proof incomplete)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 64 | Unicode remark / whitespace | <code>accepted (proof\u2028not accepted)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 65 | Unicode remark / whitespace | <code>accepted (proof\u2029not accepted)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 66 | Unicode remark / whitespace | <code>ACCEPT\u00a0NOT</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 67 | Unicode remark / whitespace | <code>ACCEPT\u2003NOT</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 68 | Unicode remark / whitespace | <code>accepted (status: NOT\u2011EXAMINED)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 69 | Unicode remark / whitespace | <code>accepted (status: NOT\u2028EXAMINED)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 70 | separator | <code>ACCEPT\u2028NOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 71 | separator | <code>ACCEPT\u2029NOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 72 | separator | <code>ACCEPT\u0085NOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 73 | separator | <code>ACCEPT\rNOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 74 | separator | <code>ACCEPT\nNOT-EXAMINED</code> | NOT ACCEPTED | ACCEPT | NOT ACCEPTED | **MISMATCH** |
| 75 | separator | <code>ACCEPT\r\nNOT-EXAMINED</code> | NOT ACCEPTED | ACCEPT | NOT ACCEPTED | **MISMATCH** |
| 76 | separator | <code>ACCEPT\u000bNOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 77 | separator | <code>ACCEPT\fNOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 78 | markdown | <code>\\*ACCEPT\\*</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 79 | markdown | <code>\\`ACCEPT\\`</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 80 | markdown | <code>ACCEPT\\&#124;NOT-EXAMINED</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 81 | markdown | <code>accepted (status: \\*not accepted\\*)</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 82 | markdown | <code>ac`cept</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 83 | markdown | <code>ac**cept</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 84 | markdown | <code>**ACCEPT** (conditional)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 85 | markdown | <code>__ACCEPT__</code> | NOT ACCEPTED | NOT ACCEPTED | NOT ACCEPTED | OK |
| 86 | markdown | <code>accepted (status: NOT_EXAMINED)</code> | NOT ACCEPTED | ACCEPT | ACCEPT | **MISMATCH** |
| 87 | table structure | <code>third column negative remark</code> | NOT ACCEPTED | ACCEPT | — | **MISMATCH** |
| 88 | table structure | <code>third column conditional remark</code> | NOT ACCEPTED | ACCEPT | — | **MISMATCH** |
| 89 | table structure | <code>continuation row negative</code> | NOT ACCEPTED | ACCEPT | — | **MISMATCH** |
| 90 | table structure | <code>continuation row conditional</code> | NOT ACCEPTED | ACCEPT | — | **MISMATCH** |
| 91 | table structure | <code>incomplete physical row</code> | NOT ACCEPTED | ACCEPT | — | **MISMATCH** |
| 92 | table structure | <code>duplicate contradictory row</code> | NOT ACCEPTED | NOT ACCEPTED | — | OK |
| 93 | table structure | <code>duplicate reverse order</code> | NOT ACCEPTED | NOT ACCEPTED | — | OK |
| 94 | table structure | <code>third column harmless remark</code> | ACCEPT | ACCEPT | — | OK |
| 95 | table structure | <code>CRLF positive</code> | ACCEPT | ACCEPT | — | OK |

Structural-case texts:

- third column negative remark: <code>&#124; id &#124; decision &#124; remarks &#124;\n&#124;---&#124;---&#124;---&#124;\n&#124; A &#124; ACCEPT &#124; withdrawn &#124;\n</code>
- third column conditional remark: <code>&#124; id &#124; decision &#124; remarks &#124;\n&#124;---&#124;---&#124;---&#124;\n&#124; A &#124; ACCEPT &#124; only if proof repaired &#124;\n</code>
- continuation row negative: <code>&#124; id &#124; decision &#124;\n&#124;---&#124;---&#124;\n&#124; A &#124; ACCEPT &#124;\n&#124; &#124; NOT-EXAMINED &#124;\n</code>
- continuation row conditional: <code>&#124; id &#124; decision &#124;\n&#124;---&#124;---&#124;\n&#124; A &#124; ACCEPT &#124;\n&#124; &#124; only if proof repaired &#124;\n</code>
- incomplete physical row: <code>&#124; id &#124; decision &#124;\n&#124;---&#124;---&#124;\n&#124; A &#124; ACCEPT\nNOT-EXAMINED &#124;\n</code>
- duplicate contradictory row: <code>&#124; id &#124; decision &#124;\n&#124;---&#124;---&#124;\n&#124; A &#124; ACCEPT &#124;\n&#124; A &#124; NOT-EXAMINED &#124;\n</code>
- duplicate reverse order: <code>&#124; id &#124; decision &#124;\n&#124;---&#124;---&#124;\n&#124; A &#124; NOT-EXAMINED &#124;\n&#124; A &#124; ACCEPT &#124;\n</code>
- third column harmless remark: <code>&#124; id &#124; decision &#124; remarks &#124;\n&#124;---&#124;---&#124;---&#124;\n&#124; A &#124; ACCEPT &#124; proof verified &#124;\n</code>
- CRLF positive: <code>&#124; id &#124; decision &#124;\r\n&#124;---&#124;---&#124;\r\n&#124; A &#124; ACCEPT &#124;\r\n</code>

## A4 carrier integration

Fresh ticket `RECHECK2`: covered `STATEMENT.md` and checked status in `REPORT.md`, frozen manifest, two distinct reviews each with one valid verdict and the same per-claim decision. JSONL carrier lives in excluded `reviews/`. Each row below ran `python -B Theory_work/INFRA/tools/ingest.py claims Theory_work/WaveT/RECHECK2/reviews/carrier.jsonl --staged`. No monkeypatches.

| Variant | Exit | Actual A4 result |
|---|---|---|
| positive | 0 |   acceptance (RECHECK2:A): PASS; 0 acceptance ERROR |
| not_examined | 1 |   acceptance (RECHECK2:A): REFUSED; 3 acceptance ERROR |
| conditional | 0 |   acceptance (RECHECK2:A): PASS; 0 acceptance ERROR |
| no_in_remark | 0 |   acceptance (RECHECK2:A): PASS; 0 acceptance ERROR |
| line_split | 0 |   acceptance (RECHECK2:A): PASS; 0 acceptance ERROR |
| continuation | 0 |   acceptance (RECHECK2:A): PASS; 0 acceptance ERROR |
| negative_remarks_column | 0 |   acceptance (RECHECK2:A): PASS; 0 acceptance ERROR |
| R2F2_original | 1 |   acceptance (RECHECK2:A): REFUSED; 3 acceptance ERROR |

The five passing negative/ambiguous variants are `conditional`, `no_in_remark`, `line_split`, `continuation`, and `negative_remarks_column`. Ordinary ACCEPT passes; standalone NOT-EXAMINED and the original `accepted (not accepted)` refuse. Exact review texts are retained in `integration.py`; per-run outputs are `ingest_<variant>.log` in the scratch directory.

## Verdict and NOT-EXAMINED safeguards

`manifest_tool().verdict_problems(text, digest, 1, "sol", "8.6")`:

| Verdict input | Expected | Actual | Diagnostic |
|---|---|---|---|
| one | allow | allow |  |
| identical duplicate | reject | reject | 2 COUNCIL-VERDICT lines for MANIFEST aaaaaaaaaaaa... (exactly one) |
| rescored duplicate | reject | reject | 2 COUNCIL-VERDICT lines for MANIFEST aaaaaaaaaaaa... (exactly one) |
| other digest | reject | reject | contradictory COUNCIL-VERDICT line for another manifest bbbbbbbbbbbb... (R1, seat sol, gates=PASS): a council review file gives one verdict, on one manifest |
| malformed second | reject | reject | malformed COUNCIL-VERDICT line &#x27;COUNCIL-VERDICT invalid&#x27; (expected exactly: COUNCIL-VERDICT round=R&lt;k&gt; manifest=&lt;64-hex&gt; seat=&lt;seat&gt; score=&lt;x.y&gt; gates=PASS&#124;FAIL) |

**Second COUNCIL-VERDICT line: rejected**, whether identical, rescored, another digest, or malformed. The lifecycle suite also exercises A4 and `manifest.py bind` for second verdicts.

**Standalone NOT-EXAMINED: no checked acceptance.** Plain and mixed-case cells all return false. A real two-seat carrier attempt with `PROVED-CHECKED` refuses (exit 1); the direct carrier guard also reports that both seats did not accept. However, the stronger claim that NOT-EXAMINED can *never* coexist with a successful checked acceptance is false: the LF/continuation examples above hide it while accepting A. Unicode nonbreaking hyphen U+2011 inside a later parenthetical disposition also evades the blacklist.

## Lifecycle suite

Ran `python -B Theory_work/INFRA/tools/test_lifecycle.py` **once** in the clone: **164 PASS, 0 FAIL; Python exit 0**. Exit captured directly from `subprocess.run().returncode`. Existing tests cover standalone NOT-EXAMINED checked-label refusal on checkpoint and carrier paths, unchecked retention, duplicate verdicts, and the original R2-F2 examples. Their passing result does not cover the bypasses above.

- R06 clones: 56 (manifest, commit) checks on 5 refs (HEAD, theory/W3-MISR, theory/W3-PSHARP, theory/W3-RM2, theory/W3-START); missing refs: none

## Evidence and isolation

Scratch directory: <code>C:/Users/felip/AppData/Local/Temp/r06-recheck2-sol-17b6055a</code>. `probes.py`, `cases.json`, `verdicts.json`, `guard.json`, `integration.py`, `ingest_results.json`, `ingest_*.log`, `suite.log`, and `suite.exit` retain the exact tests/results. Reproduce probes from `repo/` with `python -B ../probes.py`; the table reader and carrier guard used the unmodified parser.

The parser, lifecycle suite, and manifest tool in the clone byte-match the supplied worktree. Review fixes were not made.
