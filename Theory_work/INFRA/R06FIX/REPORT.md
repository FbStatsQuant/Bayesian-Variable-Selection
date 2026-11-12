# INFRA R06 — line-ending-independent hashes + two acceptance-path confirmations — REPORT (implementer, 2026-11-12)

Implementer: Claude Opus 5.5 (claude-personal, effort high). Worktree `C:/Users/felip/BVS-wt/INFRA-R06`, branch
`infra/R06-eol` (HEAD 0d7e94c). **Uncommitted; no git state changed** (HQ commits). Reviewer: Sol (codex gpt-6.1-sol,
high), 2 rounds: `R06FIX_review_sol.md`.

## Result
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
- Closed decision grammar (`decision_accepts`): `accept` / `accepted` / `accepted with non-blocking remarks`, plus at
  most one balanced parenthetical remark that carries no disposition phrase. All 84 real decision cells on the four
  branches read the same as under the R05 parser (0 differences).
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
- **R2-F2 fix is not Sol-reviewed.** It has regressions in the suite: the parser on Sol's 4 strings plus more, and a
  staged checkpoint-path refusal of `accepted (not accepted)`. The real tables are unchanged (0/84 differences). HQ may
  accept this, or order one narrow Sol check of `decision_accepts`.
- The grammar is fail-closed: a seat writing e.g. `Accepted.` or `accepted unconditionally` is NOT accepted. Addendum
  briefs should prescribe exactly `ACCEPT` / `NOT-EXAMINED`.
- The clone test (`R06 every MANIFEST_*.txt …`) reads the local refs theory/W3-{START,PSHARP,MISR,RM2} (or
  origin/…). An absent branch is allowed only if HEAD carries its ticket folder (merged). It adds ~1–2 min to the
  suite. The count grew from 52 to 56 checks during this run as ticket branches moved, so the test is not pinned to
  commits.

## Files
`Theory_work/Wave3/tools/manifest.py`; `Theory_work/INFRA/tools/bvsreg.py`; `Theory_work/INFRA/tools/test_lifecycle.py`
(block "INFRA R06" at the end); `Theory_work/INFRA/LIFECYCLE.md` (§4.1); `Theory_work/INFRA/R06FIX/{BRIEF_sol.md,
BRIEF_sol_recheck.md, R06FIX_review_sol.md, REPORT.md}`. Scratch: `C:/Users/felip/AppData/Local/Temp/claude/
b6670484aa90e31a/67fe9880-b706-4152-ab57-f9faa4db5efd/scratchpad` (survey / dry-run scripts and logs). Sol's scratch:
`C:/Users/felip/AppData/Local/Temp/r6s-7812`, `C:/Users/felip/AppData/Local/Temp/r6s2-112`.
