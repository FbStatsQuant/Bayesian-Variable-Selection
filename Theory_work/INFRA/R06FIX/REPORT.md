# INFRA R06 — line-ending-independent hashes + two acceptance-path confirmations — REPORT (implementer, 2026-11-12)

Implementer: Claude Opus 5.5 (claude-personal, effort high). Worktree `C:/Users/felip/BVS-wt/INFRA-R06`, branch
`infra/R06-eol` (HEAD 0d7e94c). **Uncommitted; no git state changed** (HQ commits). Reviewer: Sol (codex gpt-6.1-sol,
high), 2 rounds: `R06FIX_review_sol.md`.

## Update 2026-11-12 (HQ ruling after Sol recheck 2: strict whitelist, fail closed)
- **Decision reader replaced** (`bvsreg.py`: `DECISION_ACCEPT`, `decision_value`, `seat_table`, `_strict_cells`,
  `evidence_raw_text`, `_row_problems`). The decision cell, trimmed of surrounding spaces / tabs and table pipes only,
  must be exactly `ACCEPT` (legacy: exactly `accepted` / `Accepted` / `ACCEPTED`), or `NOT-EXAMINED` (not accepted).
  Anything else is NOT accepted, and a problem names the claim. A row that is incomplete, split (CR, VT, FF, FS/GS/RS,
  NEL, U+2028/9), continued (empty id), has an escaped pipe, a wrong width or a non-empty cell after the decision is
  NOT accepted; a continuation also refuses the previous row's claim. The header must be exact and be followed
  directly by a same-width delimiter row. A header-like line that fails this still counts as a table, but every row
  in it is refused, so a bad header can't fall back to the cell-only rule. Review files are read raw (UTF-8, CRLF/LF
  only), and table problems are attached to the claim they concern. LIFECYCLE §4.1 item 2 updated.
- **(1) Sol recheck 2, 95 cases** (`R06FIX/decision_cases.json`): all 82 non-acceptance cases are read as Sol
  expected (0 acceptance errors). 13 of Sol's positive controls are refused by the whitelist **by design**: #3 `accept`,
  #4 `AcCePt`, #5 `aCcEpTeD`, #7 `**ACCEPT**`, #8 `` `accepted` ``, #9–#14 and #48 (remark forms), #94 (harmless
  remarks column). Every refusal except an exact NOT-EXAMINED names the claim. Sol's five staged variants, plus a
  pipe-less row and an escaped pipe, are REFUSED; plain ACCEPT passes.
- **(4) Sol parser round** (`R06FIX_parser_sol.md`, codex gpt-6.1-sol high): 95/95; 116 new cases, of which 9 were
  read as accepted against the spec, in three MAJOR groups: (i) separators erased by the text-mode file read; (ii)
  delimiter-shaped lines skipped anywhere; (iii) lenient header. **All three fixed after that round:**
  raw review reading; delimiter only directly below the header; exact header, a malformed one refusing its rows.
  The 116 cases (`R06FIX/decision_cases_parser.json`) now read as Sol expected except #110 (a table with no delimiter
  row is refused by design). File-level separator cases (9 characters) and 5 staged variants are refused. **These
  round-4 fixes have not had a Sol round** (HQ ordered one Sol round; it is used).
- **(2) Real tables** (only W3-START has per-claim tables; 84 decisions in 4 council reviews): **49 now read NOT
  accepted**. R1_council_sol and R2_council_sol: all 21 claims each (non-empty `Reason / proof checked` / `Basis`
  column). R1_council_opus: EX, F4, LEAK. R2_council_opus: BR, EX, F1, OVL (cells `accepted with non-blocking
  remarks (…)` / `accepted (…)`). Consequence: W3-START staged acceptance on fresh LF / CRLF clones is now
  **REFUSED** (67 A4 errors, all from the seat tables), where commit 4952705 passed it. Not loosened; per HQ, an
  ACCEPT / NOT-EXAMINED addendum (R2 seats) will fix it.
- **(3)** Suite **169/169 PASS, exit 0**; `check.py --quiet` 406 claims **0 ERROR**. Regression on HEAD: old vs new
  tools give identical findings (401 check, 1,783 acceptance).

## Result (before the update)
- Suite `test_lifecycle.py`: **164/164 PASS, exit 0** (146 before + 18 new R06 results). `check.py --quiet`: 406 claims,
  **0 ERROR** (184 WARN, 217 INFO).
- Sol round 1: 2 MAJOR (F1 CR-variant collision; F2 `ACCEPT=NO` read as acceptance), both fixed. Sol round 2: F1
  RESOLVED; F2 original probes fixed, one remaining MAJOR (R2-F2: negation behind punctuation / in a remark / U+2028
  row split). **R2-F2 fixed by me after the last allowed Sol round, so that fix is not Sol-reviewed** (see §4).

## 1. Manifest hashes (`Theory_work/Wave3/tools/manifest.py`)
- A file is *EOL-normalisable* iff it has no NUL byte and every CR is the first half of a CRLF pair. For such a file
  `freeze` records sha256 of the LF-normalised content; `verify` accepts a recorded hash equal to sha256 of the raw
  bytes, the LF-normalised or the CRLF-ised content. Any other file (NUL = binary; lone CR, e.g. CR CR LF) is hashed
  raw only, on freeze and verify (Sol F1). `bind` only reads the manifest (text mode), unchanged. Documented in the
  module docstring and LIFECYCLE §4.1 "Line endings". No MANIFEST file changed.
- Real data: on LF and CRLF clones, the new tool gives **exactly the same difference list** for all 28 branch manifests
  (START 12, RM2 12, PSHARP 2, MISR 2) as the old raw-byte tool on the original frozen worktrees (Sol confirmed, 56/56).
  The old tool on the clones disagrees with the frozen-tree result on at least one clone for every manifest (up to 59
differences; MISR's CRLF clone happens to match its all-CRLF frozen tree). Current council manifests verify clean on both: START R2,
  PSHARP R2, MISR R2, RM2 PC1. The others still fail on the clones as they do on the frozen trees: the reviewed content
  changed after those rounds (e.g. RM2 R1's 7 post-council edits); that is not an EOL effect.
- W3-START `ingest.py claims CHECKPOINT_3.md --staged` on **fresh** LF and CRLF clones (no byte copy from the frozen
  worktree): **PASS, 21 claims, 0 ERROR** with R06 tools; REFUSED (21 A4) with pre-R06 tools.

## 2. Registry fingerprints (`sha256`, `tex_sha256`, `status_sha256`, `fp2`)
No code change needed. Every site reads files in text mode / `git show` + `splitlines()` and joins with LF
(`text_hash`, `_digest`), so they were line-ending-independent since their introduction. No raw-byte value exists to
migrate (no `accept` event in `events.log`; C12 shows every recorded `status_sha256` equals the line-wise digest).
Test: all 406 claims' (recomputed sha256, status_sha256, fp2 stamp) tuples are identical on an LF and a CRLF clone
(Sol reproduced; artifact / row / alias mutations still change the stamp). Documented in LIFECYCLE "Line endings".

## 3. Acceptance paths (`Theory_work/INFRA/tools/bvsreg.py`, LIFECYCLE §4.1)
(a) **Addendum seat tables.** These failed before the fix: `ACCEPT` was not read as acceptance, because only decisions
starting with `accepted` counted. A NOT-EXAMINED id kept in the checkpoint without a checked label also refused the
whole checkpoint. Now:
- Tables are read anywhere in the review, so a dated addendum after the verdict line counts. A body/addendum
  contradiction is not accepted.
- A second `COUNCIL-VERDICT` line (same or another digest) refuses A4 and `bind`. This code is unchanged; it is now
  tested for addenda.
- Decision reader: superseded by the strict whitelist (see the update at the top). The closed grammar described
  in earlier rounds was replaced.
- Safeguard 4 now requires each seat to accept every checkpoint id with a checked label, and every id a seat accepted
  to be in the checkpoint. A NOT-EXAMINED id may stay in the checkpoint only without a checked label.

(b) **Carrier files.** `ingest.py claims <carrier>` (JSONL, or REGISTRY-block `.md` with `Theory_work/` or relative
paths) works from outside the manifest (`reviews/`, the repo root). Statement, premise and status-source coverage is
unchanged; the carrier itself is never a coverage input. Note: a carrier placed directly in the ticket folder would be
`ADDED` and break `verify`, so put it in `reviews/` or outside the ticket.

New guard (`seat_table_problems`): if ANY seat's review has a per-claim table, a checked claim whose status source is
not its own checkpoint must be accepted in a table of EVERY seat's review. This closes "carrier + status line borrowed
from a covered file" for a NOT-EXAMINED id. Councils with no table keep the cell-only rule.

Regression on HEAD: old vs new tools give identical `check.py --json` findings (401) and identical
`check.py --acceptance <all 406 ids> --json` findings (1,783).

## 4. Open for HQ
- **The round-4 parser fixes have not had a Sol round** (regressions are in the suite). HQ may accept this, or order
  one more narrow Sol run of `BRIEF_sol_parser.md`.
- W3-START needs ACCEPT / NOT-EXAMINED addenda (both R2 seats) before `--record`. Addendum tables must be exactly
  `| id | decision |`, then `|---|---|`, then rows `| <id> | ACCEPT |` or `| <id> | NOT-EXAMINED |`, with no other
  columns, a blank line before and after, and remarks outside the table.
- Every malformed table problem without a claim id (e.g. a broken header) refuses all of that seat's claims: fail
  closed.
- The clone test (`R06 every MANIFEST_*.txt …`) reads the local refs theory/W3-{START,PSHARP,MISR,RM2} (or
  origin/…). An absent branch is allowed only if HEAD carries its ticket folder (merged). It adds ~1–2 min to the
  suite. The count grew from 52 to 56 checks during this run as ticket branches moved, so the test is not pinned to
  commits.

## Files
`Theory_work/Wave3/tools/manifest.py`; `Theory_work/INFRA/tools/bvsreg.py`; `Theory_work/INFRA/tools/test_lifecycle.py`
(block "INFRA R06" at the end); `Theory_work/INFRA/LIFECYCLE.md` (§4.1); `Theory_work/INFRA/R06FIX/{decision_cases.json, decision_cases_parser.json, BRIEF_sol_parser.md, R06FIX_parser_sol.md, R06FIX_recheck2_sol.md, BRIEF_sol.md,
BRIEF_sol_recheck.md, R06FIX_review_sol.md, REPORT.md}`. Scratch: `C:/Users/felip/AppData/Local/Temp/claude/
b6670484aa90e31a/67fe9880-b706-4152-ab57-f9faa4db5efd/scratchpad` (survey / dry-run scripts and logs). Sol's scratch:
`C:/Users/felip/AppData/Local/Temp/r6s-7812`, `C:/Users/felip/AppData/Local/Temp/r6s2-112`.
