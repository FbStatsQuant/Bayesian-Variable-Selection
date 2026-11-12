ACCEPTANCE ERRORS FOUND

Tested commit `4952705d0e8da9f5be9a589b894ed7fd025f2c9e` plus the supplied working changes, Python `Python 3.15.2`. Source worktree read only; no source Git mutations or subagents. Only this report was written there.

95 supplied cases: **95/95 match `expected`**, zero mismatches; no missing claim-specific refusal messages (excluding the known NOT-EXAMINED reading). New direct parser cases: **116**, **9 acceptance mismatches**, **0 false negatives**. An additional 15 staged variants include nine file-reading failures that direct string tests correctly reject.

## Findings

1. **MAJOR — review loading erases forbidden separators before validation.** `bvsreg.py:531,544,1195`: `open(...).read().splitlines()` (including universal newline translation for CR) and subsequent LF joining lose CR, VT, FF, FS/GS/RS, NEL, U+2028 and U+2029. Exact reproducer: `H + "| A | ACCEPT |" + s + " \n"`, with each of those nine characters substituted for `s`. Direct `seat_table` refuses A with a named problem; `seat_table(evidence_text(path), ticket)` accepts A without a problem. Both seats then permit staged checked acceptance, exit 0. The space after `s` ensures CR is lone content, never a legitimate CRLF. **Fix direction:** give review parsing a raw, non-universal-newline read that normalizes CRLF pairs only and splits on LF only; preserve all other separators for row validation. Apply to working-file and pinned-file evidence. Pinned implementation was inspected; custom pinned fixtures were not committed or tested.

2. **MAJOR — separator-shaped lines bypass complete-row validation.** `bvsreg.py:1357` skips `_SEP_ROW` matches anywhere in the table, before width/completeness checks. Exact reproducers: `H + "| A | ACCEPT |\n" + tail + "\n"`, where `tail` is `"---"` or `"---|---"`. Both leave A accepted without any problem, though the lines are incomplete. The bare `---` is an incomplete line that must also invalidate preceding A. The bare variant passes staged A4, exit 0. Complete wrong-width rows are a separate diagnostic issue: they do not, on their own, invalidate preceding A under the continuation rule. **Fix direction:** recognize the actual header delimiter at the appropriate position with matching cell count; validate subsequent lines rather than skipping every hyphen-shaped line. Preserve/invalidate the previous id when a line may continue it.

3. **MAJOR — header recognition exceeds the stated literal aliases.** `bvsreg.py:1288,1293,1350`: `_cells` removes repeated boundary pipes and broad Unicode whitespace, and `_plain` removes emphasis/backticks and collapses whitespace. Seven nonliteral headers in the table below are recognized as `id/claim id` plus `decision`; A is accepted although the specified first/second literal cells are absent or the header has an extra empty cell. Double leading/trailing pipes also hide a header/data width mismatch. Double-pipe and emphasized headers pass staged A4, exit 0. **Fix direction:** parse header boundaries once, preserve empty cells, and match the stated aliases case-insensitively without unrequested Markdown or Unicode rewriting. Under the documented legacy carrier fallback, completely absent tables retain cell-only acceptance; header rejection alone therefore does not change that separate fallback policy.

**MINOR - missing malformed-row diagnostics:** `H + "| A | ACCEPT |\n|---|\n"` and the three-cell `|---|---|---|` variant are silently skipped: no problem is emitted for their missing/wrong-width/unknown decision. A may remain accepted here because the row itself is complete; this is a diagnostic finding, not counted as an A-reading mismatch. Validate delimiter width and position before skipping. **False negatives:** none observed in these probes. Plain NOT-EXAMINED is refused for a checked claim with a clear A4 message naming the claim. Valid ACCEPT / NOT-EXAMINED dated addenda, both duplicate orders, and local/full-id equivalence are covered below and by the suite.

## New direct inputs

Every row tests `bool(seat_decisions(text, "REV")[0].get("REV:A", False))`. `H` denotes exactly `"| id | decision |\n|---|---|\n"`; `H +` means concatenate the displayed JSON string. Escape sequences identify exact code points. A = accepted, N = not accepted. Literal header aliases are interpreted as written in the brief; tables are scanned anywhere because the specification gives no fence exclusion. Normal CRLF remains valid. ID emphasis is a compatibility control, separate from the strict decision-cell whitelist.

| # | Input | Spec | Actual | Result |
|---|---|---|---|---|
| 1 | H + `"| A | ACCEPT |\n"` | A | A | OK |
| 2 | H + `"| A | accepted |\n"` | A | A | OK |
| 3 | H + `"| A | Accepted |\n"` | A | A | OK |
| 4 | H + `"| A | ACCEPTED |\n"` | A | A | OK |
| 5 | H + `"| A |  ACCEPT  |\n"` | A | A | OK |
| 6 | H + `"| A | \tACCEPT\t |\n"` | A | A | OK |
| 7 | H + `"| A | accept |\n"` | N | N | OK |
| 8 | H + `"| A | Accept |\n"` | N | N | OK |
| 9 | H + `"| A | aCcEpT |\n"` | N | N | OK |
| 10 | H + `"| A | aCcEpTeD |\n"` | N | N | OK |
| 11 | H + `"| A | NOT-EXAMINED |\n"` | N | N | OK |
| 12 | H + `"| A | **ACCEPT** |\n"` | N | N | OK |
| 13 | H + `"| A | _ACCEPT_ |\n"` | N | N | OK |
| 14 | H + `"| A | `ACCEPT` |\n"` | N | N | OK |
| 15 | H + `"| A | <b>ACCEPT</b> |\n"` | N | N | OK |
| 16 | H + `"| A | ACCEPT<!-- --> |\n"` | N | N | OK |
| 17 | H + `"| A | &#65;CCEPT |\n"` | N | N | OK |
| 18 | H + `"| A | ACCEPT&nbsp; |\n"` | N | N | OK |
| 19 | H + `"| A | ACCEPT\\ |\n"` | N | N | OK |
| 20 | H + `"| A | \\ACCEPT |\n"` | N | N | OK |
| 21 | H + `"| A | \uff21\uff23\uff23\uff25\uff30\uff34 |\n"` | N | N | OK |
| 22 | H + `"| A | \u0410CCEPT |\n"` | N | N | OK |
| 23 | H + `"| A | ACCEPT\u0301 |\n"` | N | N | OK |
| 24 | H + `"| A | \ufeffACCEPT |\n"` | N | N | OK |
| 25 | H + `"| A | ACCEPT\u200b |\n"` | N | N | OK |
| 26 | H + `"| A | ACCEPT\u200d |\n"` | N | N | OK |
| 27 | H + `"| A | \u00a0ACCEPT |\n"` | N | N | OK |
| 28 | H + `"| A | ACCEPT\u00a0 |\n"` | N | N | OK |
| 29 | H + `"| A | \u2003ACCEPT |\n"` | N | N | OK |
| 30 | H + `"| A | ACCEPT\u202f |\n"` | N | N | OK |
| 31 | H + `"| A | ACCEPT\u2060 |\n"` | N | N | OK |
| 32 | H + `"| A | ACCEPT\u0000 |\n"` | N | N | OK |
| 33 | H + `"| A | ACCEPT. |\n"` | N | N | OK |
| 34 | H + `"| A | ACCEPT (yes) |\n"` | N | N | OK |
| 35 | H + `"| A | ACCEPT \\| NOT-EXAMINED |\n"` | N | N | OK |
| 36 | H + `"| A | ACCEPT\r |\n"` | N | N | OK |
| 37 | H + `"| A | ACCEPT |\r\n"` | A | A | OK |
| 38 | H + `"| A | ACCEPT |\n\r\n| B | ACCEPT |\n"` | A | A | OK |
| 39 | H + `"| A | ACCEPT\u000b |\n"` | N | N | OK |
| 40 | H + `"| A | ACCEPT |\u000b\n"` | N | N | OK |
| 41 | H + `"| A | ACCEPT |\n\u000b\n| B | ACCEPT |\n"` | N | N | OK |
| 42 | H + `"| A | ACCEPT\f |\n"` | N | N | OK |
| 43 | H + `"| A | ACCEPT |\f\n"` | N | N | OK |
| 44 | H + `"| A | ACCEPT |\n\f\n| B | ACCEPT |\n"` | N | N | OK |
| 45 | H + `"| A | ACCEPT\u001c |\n"` | N | N | OK |
| 46 | H + `"| A | ACCEPT |\u001c\n"` | N | N | OK |
| 47 | H + `"| A | ACCEPT |\n\u001c\n| B | ACCEPT |\n"` | N | N | OK |
| 48 | H + `"| A | ACCEPT\u001d |\n"` | N | N | OK |
| 49 | H + `"| A | ACCEPT |\u001d\n"` | N | N | OK |
| 50 | H + `"| A | ACCEPT |\n\u001d\n| B | ACCEPT |\n"` | N | N | OK |
| 51 | H + `"| A | ACCEPT\u001e |\n"` | N | N | OK |
| 52 | H + `"| A | ACCEPT |\u001e\n"` | N | N | OK |
| 53 | H + `"| A | ACCEPT |\n\u001e\n| B | ACCEPT |\n"` | N | N | OK |
| 54 | H + `"| A | ACCEPT\u0085 |\n"` | N | N | OK |
| 55 | H + `"| A | ACCEPT |\u0085\n"` | N | N | OK |
| 56 | H + `"| A | ACCEPT |\n\u0085\n| B | ACCEPT |\n"` | N | N | OK |
| 57 | H + `"| A | ACCEPT\u2028 |\n"` | N | N | OK |
| 58 | H + `"| A | ACCEPT |\u2028\n"` | N | N | OK |
| 59 | H + `"| A | ACCEPT |\n\u2028\n| B | ACCEPT |\n"` | N | N | OK |
| 60 | H + `"| A | ACCEPT\u2029 |\n"` | N | N | OK |
| 61 | H + `"| A | ACCEPT |\u2029\n"` | N | N | OK |
| 62 | H + `"| A | ACCEPT |\n\u2029\n| B | ACCEPT |\n"` | N | N | OK |
| 63 | `"| ID | DECISION |\n|---|---|\n| A | ACCEPT |\n"` | A | A | OK |
| 64 | `"| claim | disposition |\n|---|---|\n| A | ACCEPT |\n"` | A | A | OK |
| 65 | `"| Claim Id | Decision |\n|---|---|\n| A | ACCEPT |\n"` | A | A | OK |
| 66 | `"| **id** | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | A | mismatch |
| 67 | `"| id | `decision` |\n|---|---|\n| A | ACCEPT |\n"` | N | A | mismatch |
| 68 | `"|| id | decision ||\n|---|---|\n| A | ACCEPT |\n"` | N | A | mismatch |
| 69 | `"| \u00a0id | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | A | mismatch |
| 70 | `"| claim\tid | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | A | mismatch |
| 71 | H + `"| A | ACCEPT |\nA | NOT-EXAMINED |\n"` | N | N | OK |
| 72 | H + `"| A | ACCEPT |\n| A | ACCEPT\n"` | N | N | OK |
| 73 | H + `"| A | ACCEPT |\n| | NOT-EXAMINED |\n"` | N | N | OK |
| 74 | H + `"| A | ACCEPT |\n| A | ACCEPT ||\n"` | N | N | OK |
| 75 | H + `"| A | ACCEPT |\n|| A | ACCEPT |\n"` | N | N | OK |
| 76 | H + `"| A | ACCEPT |\n| A | ACCEPT | remarks |\n"` | N | N | OK |
| 77 | H + `"| A | ACCEPT |\n| A | ACCEPT \\| |\n"` | N | N | OK |
| 78 | H + `"| A | ACCEPT |\nparagraph\n"` | N | N | OK |
| 79 | H + `"| A | ACCEPT |\n---\n"` | N | A | mismatch |
| 80 | H + `"| A | ACCEPT |\n|---|\n"` | A | A | OK |
| 81 | H + `"| A | ACCEPT |\n---|---\n"` | N | A | mismatch |
| 82 | H + `"| A | ACCEPT |\n|---|---|---|\n"` | A | A | OK |
| 83 | H + `"| A | ACCEPT |\n|:---|---:|\n"` | A | A | OK |
| 84 | H + `"| A | ACCEPT |\n\n| A | NOT-EXAMINED |\n"` | A | A | OK |
| 85 | H + `"| A | ACCEPT |\n \n| A | NOT-EXAMINED |\n"` | A | A | OK |
| 86 | H + `"| A | ACCEPT |\n\t\n| A | NOT-EXAMINED |\n"` | A | A | OK |
| 87 | H + `"| A | ACCEPT |\n \t \n| A | NOT-EXAMINED |\n"` | A | A | OK |
| 88 | H + `"| A | ACCEPT |\n| A | NOT-EXAMINED |\n"` | N | N | OK |
| 89 | H + `"| A | ACCEPT |\n| REV:A | NOT-EXAMINED |\n"` | N | N | OK |
| 90 | H + `"| A | ACCEPT |\n\n## Addendum 2026-11-12\n\n| id | decision |\n|---|---|\n| A | NOT-EXAMINED |\n"` | N | N | OK |
| 91 | H + `"| A | NOT-EXAMINED |\n| A | ACCEPT |\n"` | N | N | OK |
| 92 | H + `"| A | NOT-EXAMINED |\n| REV:A | ACCEPT |\n"` | N | N | OK |
| 93 | H + `"| A | NOT-EXAMINED |\n\n## Addendum 2026-11-12\n\n| id | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | N | OK |
| 94 | H + `"| A | ACCEPT |\n| A | ACCEPT |\n"` | A | A | OK |
| 95 | H + `"| A | ACCEPT |\n| REV:A | ACCEPT |\n"` | A | A | OK |
| 96 | H + `"| A | ACCEPT |\n\n## Addendum 2026-11-12\n\n| id | decision |\n|---|---|\n| A | ACCEPT |\n"` | A | A | OK |
| 97 | H + `"| A | accepted |\n| A | ACCEPT |\n"` | A | A | OK |
| 98 | H + `"| A | accepted |\n| REV:A | ACCEPT |\n"` | A | A | OK |
| 99 | H + `"| A | accepted |\n\n## Addendum 2026-11-12\n\n| id | decision |\n|---|---|\n| A | ACCEPT |\n"` | A | A | OK |
| 100 | H + `"| A | garbage |\n| A | ACCEPT |\n"` | N | N | OK |
| 101 | H + `"| A | garbage |\n| REV:A | ACCEPT |\n"` | N | N | OK |
| 102 | H + `"| A | garbage |\n\n## Addendum 2026-11-12\n\n| id | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | N | OK |
| 103 | H + `"| REV:A | ACCEPT |\n"` | A | A | OK |
| 104 | H + `"| **A** | ACCEPT |\n"` | A | A | OK |
| 105 | H + `"| `A` | ACCEPT |\n"` | A | A | OK |
| 106 | `"> | id | decision |\n> |---|---|\n> | A | ACCEPT |\n"` | N | N | OK |
| 107 | `"```markdown\n| id | decision |\n|---|---|\n| A | ACCEPT |\n\n```\n"` | A | A | OK |
| 108 | `"```markdown\n| id | decision |\n|---|---|\n| A | ACCEPT |\n```\n"` | N | N | OK |
| 109 | `"id | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | N | OK |
| 110 | `"| id | decision |\n| A | ACCEPT |\n"` | A | A | OK |
| 111 | `"| id | decision |\r\n|---|---|\r\n| A | ACCEPT |\r\n"` | A | A | OK |
| 112 | `"| id | decision | remarks |\n|---|---|---|\n| A | ACCEPT | \t |\n"` | A | A | OK |
| 113 | `"|| id | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | A | mismatch |
| 114 | `"| id | decision ||\n|---|---|\n| A | ACCEPT |\n"` | N | A | mismatch |
| 115 | `"| \u0456d | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | N | OK |
| 116 | `"\ufeff| id | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | N | OK |

## Staged ingest and caller checks

Independent R06T fixture in the probe clone: STATEMENT.md line 1 is `Lemma A. A holds.`; REPORT.md line 2 is `PROVED-CHECKED`; both are covered by `reviews/MANIFEST_R1.txt`. Each seat file contains exactly one matching `COUNCIL-VERDICT round=R1 manifest=<digest> seat=<sol/opus> score=<8.6/8.4> gates=PASS` line and the tested table. The council cell references both seats. `reviews/CARRIER_R1.jsonl` holds one checked lemma A, with `premises: []`, statement span `[1,1]`, and status source `Theory_work/WaveT/R06T/REPORT.md:2`.

Command, from the probe clone:

```powershell
python -B Theory_work/INFRA/tools/ingest.py claims Theory_work/WaveT/R06T/reviews/CARRIER_R1.jsonl --staged
```

| Variant / exact table | Spec | Direct A | Loaded A | Python exit | Acceptance |
|---|---|---|---|---|---|
| plain_ACCEPT: H + `"| A | ACCEPT |\n"` | A | A | A | 0 | PASS |
| bare_separator: H + `"| A | ACCEPT |\n---\n"` | N | A | A | 0 | PASS |
| wrong_width_separator: H + `"| A | ACCEPT |\n|---|---|---|\n"` | A | A | A | 0 | PASS |
| double_pipe_header: `"|| id | decision ||\n|---|---|\n| A | ACCEPT |\n"` | N | A | A | 0 | PASS |
| emphasis_header: `"| **id** | decision |\n|---|---|\n| A | ACCEPT |\n"` | N | A | A | 0 | PASS |
| NOT_EXAMINED: H + `"| A | NOT-EXAMINED |\n"` | N | N | N | 1 | REFUSED |
| row_separator_0xd: H + `"| A | ACCEPT |\r \n"` | N | N | A | 0 | PASS |
| row_separator_0xb: H + `"| A | ACCEPT |\u000b \n"` | N | N | A | 0 | PASS |
| row_separator_0xc: H + `"| A | ACCEPT |\f \n"` | N | N | A | 0 | PASS |
| row_separator_0x1c: H + `"| A | ACCEPT |\u001c \n"` | N | N | A | 0 | PASS |
| row_separator_0x1d: H + `"| A | ACCEPT |\u001d \n"` | N | N | A | 0 | PASS |
| row_separator_0x1e: H + `"| A | ACCEPT |\u001e \n"` | N | N | A | 0 | PASS |
| row_separator_0x85: H + `"| A | ACCEPT |\u0085 \n"` | N | N | A | 0 | PASS |
| row_separator_0x2028: H + `"| A | ACCEPT |\u2028 \n"` | N | N | A | 0 | PASS |
| row_separator_0x2029: H + `"| A | ACCEPT |\u2029 \n"` | N | N | A | 0 | PASS |

All 14 PASS runs report `407 claims; 0 ERROR` and `acceptance (R06T:A): PASS; 0 acceptance ERROR`. NOT-EXAMINED reports exit 1, REFUSED, and for each seat: `claim R06T:A is not accepted (decision is not ACCEPT, or its row is unreadable / contradictory): a checked label needs each seat's ACCEPT`. No staged run applied registry changes.

Also called both `seat_table_problems` and `checkpoint_problems` directly for all 15 tables, using a checked checkpoint row with the current `status_sha256` and both seat paths. Both returned no problems for the 14 PASS variants; NOT-EXAMINED returned two named seat problems each. Thus the checkpoint comparison in part (b) shares the acceptance failures. These direct caller probes do not constitute a second full staged checkpoint integration run.

## Full suite

Fresh, separate suite clone, with supplied changes copied over and no probes added: `python -B Theory_work/INFRA/tools/test_lifecycle.py` run **once**. Python process exit captured directly via `$LASTEXITCODE`: **0**. Results: **166 PASS**, **0 FAIL**. stderr: retained in suite.stderr.txt; it includes the transaction-failure test's `REGISTRY LOCKED ... .TXN_FAILED (run bvsreg.py recover)` diagnostic. The final suite still reports all PASS and exit 0.

## Scratch and preservation

Probe clone: `C:\Users\felip\AppData\Local\Temp\r6s-904e4b/probe`; suite clone: `C:\Users\felip\AppData\Local\Temp\r6s-904e4b/suite`. Scripts: `C:\Users\felip\AppData\Local\Temp\r6s-904e4b/probe_parser.py`, `C:\Users\felip\AppData\Local\Temp\r6s-904e4b/staged_parser.py`. Exact case/results JSON: `C:\Users\felip\AppData\Local\Temp\r6s-904e4b/probes.json`, `staged.json`, `callers.json`. Suite stdout, stderr and directly captured exit: `C:\Users\felip\AppData\Local\Temp\r6s-904e4b/suite.stdout.txt`, `suite.stderr.txt`, `suite.exit.txt`. All retained for inspection. The staged fixture can be rebuilt with `python -B "C:\Users\felip\AppData\Local\Temp\r6s-904e4b\staged_parser.py"`; it writes only the probe clone.

The three supplied modified tracked files still match the copied suite inputs byte for byte. No fixes were made.
