# R05FIX — report (implementer, Claude Opus 5.5 high, 2026-11-12)

**Result:** the fix is done, with all five safeguards. Sol's first review found two MAJOR routes around them (B1, B2).
Both are fixed, and Sol's re-check rates both RESOLVED with no new findings. The suite passes 146/146. On main's
registry, no verdict changes. The W3-START staged acceptance now passes in a dry run (21/21). Branch
`infra/R05-ckpt-status` (base main c8a970f), commits bfdb968 + b0c21b0 + this report. Not merged; HQ merges. The live
registry is unchanged.

## Defect
A4 required the frozen manifest to cover each claim's status-source file. Wave 3 status lines live in the ticket's
`CHECKPOINT_<k>.md`, which `manifest.py` excludes by design, so every CHECKPOINT-layout ticket was refused. On
W3-START @ 808ddd1 this gave 21 × A4 errors (reproduced with the old tools).

## Changes (`Theory_work/INFRA/`)
- `tools/bvsreg.py`, new section "checkpoint status sources (INFRA R05)":
  - `own_checkpoint`: the status source counts as exempt only if it is `CHECKPOINT_<k>.md` directly in the claim's
    ticket folder (tickets.tsv `folder`, else the statement's folder) and exists.
  - `manifest_problems`: an exempt checkpoint is dropped from the coverage list; statement and premise files are
    still required.
  - `council_problems`: for an exempt checkpoint, it then runs `checkpoint_problems`:
    - (a) `status_sha256` is recorded and equals the file's current line-wise digest;
    - (b) the checkpoint's claim ids (REGISTRY blocks via ingest's parser, plus rows sourced there) equal each seat's
      accepted ids, read from a `| id | decision |` table;
    - (c) every round cited (`<ROUND>:` / `<ROUND> (<note>):`) in the status line(s) and in the recorded status text
      resolves to exactly one `reviews/<ROUND>_*` file. That file must quote the digest of an internally valid
      `reviews/MANIFEST_*.txt`: well-formed rows that hash to the header; it need not match the current tree. The
      council round `R<k>` resolves to the seat files, which A4 already binds to the acceptance manifest with PASS.
  - New column `status_sha256` (last column). It is part of the acceptance identity (`ACCEPT_FIELDS`). No accept
    events exist on main, so nothing needs migrating.
- `tools/check.py`: new C12-checkpoint check (ERROR when a recorded checkpoint digest no longer matches, so CI fails);
  A4 now gets the registry rows; the docstring is updated.
- `tools/ingest.py` (`new_row`), `registry.py` (`add`, `correct-status`) and `propagate.py` (status changes) record
  `status_sha256`. `registry.py set` cannot set it (it is PROTECTED).
- `LIFECYCLE.md` §4 A4 and §4.1: new paragraph "Checkpoint status source"; the identity field list is updated.

## Tests (`tools/test_lifecycle.py`, block "INFRA R05")
13 new scenarios, all passing:
- **Positive:** staged control passes; ingest records `status_sha256`; the field is not settable.
- **Negative:**
  - an extra claim id;
  - an unresolvable round id;
  - an ambiguous round id (two files);
  - an unbound council seat (verdict for another manifest);
  - an earlier round quoting no digest, or a foreign digest;
  - a corrupted historical manifest (B2);
  - a continued-status citation (B1);
  - a seat that did not accept an id;
  - a seat that accepted an id the checkpoint lacks;
  - a review with no per-claim table;
  - an uncovered status file (LOG.md, a sub-folder CHECKPOINT, another ticket's CHECKPOINT);
  - an uncovered statement file;
  - the checkpoint edited after ingest (C12 + A4);
  - a missing `status_sha256`.

Each refusal is restored and shown clean. Full suite: **146 PASS, 0 FAIL** (my run, and Sol's run in a fresh clone).

## No verdict change
On a clone at main c8a970f, I ran the old tools and then the new ones:
- `check.py --json`: 401 findings, identical.
- `check.py --acceptance <all 406 ids> --json`: 1,783 findings, identical (same 154 claims with errors, all
  pre-existing or legacy).

I repeated this after the B1/B2 fixes: still identical. Sol reproduced it independently.

## W3-START dry run
Setup:
- Clone `theory/W3-START` @ 808ddd1.
- Copy every tracked file byte-for-byte from the read-only worktree `C:/Users/felip/BVS-wt/W3-START` (MANIFEST_R2
  hashed two CRLF inputs there).
- Overlay the new tools.

Then run `ingest.py claims Theory_work/Wave3/W3-START/CHECKPOINT_3.md --staged`.

- **Before** (old tools): exit 1, 21 × A4 coverage errors.
- **After**: exit 0; 427 claims, 0 ERROR; acceptance PASS for all 21 claims.
- **The new checks were exercised:**
  - 21 matching digests;
  - 21 ids per seat;
  - 7 earlier rounds resolved, one file each: LC1-A/B/C, LC2-A/B, BR1, SW1;
  - all 12 historical manifests internally valid.

Sol confirmed this twice. Nothing was written to any live registry.

## Sol (Codex gpt-6.1-sol high) — `R05FIX_review_sol.md`, briefs `BRIEF_sol.md`, `BRIEF_sol_recheck.md`
- **Round 1: BYPASS FOUND.**
  - B1 (MAJOR): a citation carried by a status that continues past its stated line was not scanned.
  - B2 (MAJOR): a header-only or corrupted historical manifest counted as frozen.
  - Safeguards 1, 3 and 4 held in every route tried.
- **Fixes (b0c21b0):** B1 now scans the recorded status text; B2 checks each historical manifest's internal
  integrity.
- **Re-check: SAFEGUARDS HOLD.** B1 and B2 RESOLVED, with 4 extra B2 controls; no new findings.
- **Noted grammar limits, not findings** (documented in LIFECYCLE): a round written in free text, or without a blank
  after its colon, is not a citation; a decision counts as accepted iff it starts with "accepted".

## Scratch (disposable)
- Under `C:/Users/felip/AppData/Local/Temp/`:
  - `r5d/`: W3-START dry-run clone;
  - `r5b/`: main regression clone;
  - `r5_*.json`: regression findings;
  - `r5d_*.txt`: dry-run outputs;
  - Sol: `r5s-*`, `r5sr-*`.
- Suite logs: in my scratchpad (`suite1.log`, `suite2.log`).
