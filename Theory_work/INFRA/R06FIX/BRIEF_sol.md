# R06FIX — independent correctness review (Sol) — brief

Context: this is a software-correctness review of a research-project bookkeeping tool (a Python registry of
mathematical claims and the checks that decide when a claim counts as reviewed). No security testing is involved.

You are an independent correctness reviewer (Codex GPT-6.1 Sol, effort high). The change is UNCOMMITTED in the worktree
`C:/Users/felip/BVS-wt/INFRA-R06` (branch `infra/R06-eol`, HEAD 0d7e94c = main 849dfb5 + the brief). **Read that
worktree only; change no git state anywhere** (no commit, checkout, stash, worktree add, branch) and do not touch any
other checkout's working files, any live registry, scheduled task or hold file. Start no subagents. The only file you
write outside your scratch clones is your output, given below.

## What changed and why
1. `Theory_work/Wave3/tools/manifest.py`: council manifests hashed raw bytes; frozen trees had mixed LF/CRLF files and
   git stores LF blobs, so on any uniform checkout `verify` failed although content was identical. Now `freeze` records
   the sha256 of LF-normalised content (CRLF -> LF); `verify` accepts a recorded hash equal to the sha256 of the raw
   bytes, the LF-normalised or the CRLF-ised content; a file containing a NUL byte is hashed raw only. No existing
   MANIFEST file changes.
2. Registry fingerprints (`sha256`, `status_sha256`, `fp2`) were already computed from files read line-wise (text mode,
   `splitlines`); the implementer claims no code change is needed and no raw-byte value exists (check this).
3. `Theory_work/INFRA/tools/bvsreg.py`, acceptance paths HQ relies on next (HQ decision "acceptance audit dispositions",
   `Theory_work/Wave3/HQ_DECISIONS.md`, 2026-11-12 ~09:30 CT):
   (a) per-claim seat tables appended to a council review as a dated addendum after its `COUNCIL-VERDICT` line, values
   `ACCEPT` / `NOT-EXAMINED` (before: only decisions starting with `accepted` counted). A NOT-EXAMINED id must not get a
   checked label; it may stay in the ticket's own `CHECKPOINT_<k>.md` only without a checked label (R05 safeguard 4 now
   compares the checkpoint's CHECKED-labelled ids with each seat's accepted ids; accepted ids must still be in the
   checkpoint). The verdict line stays binding; a second verdict line is refused (unchanged code).
   (b) new `seat_table_problems`: a claim whose status source is not its own checkpoint, in a council where ANY seat's
   review has a per-claim table, must be accepted in a table of EVERY seat's review (closes the carrier route below).
   (c) `ingest.py claims <carrier>` with a carrier file outside the frozen manifest (JSONL or REGISTRY-block `.md`);
   coverage still requires the statement / premise / status-source files to be in the manifest (unchanged code).
Docs: `Theory_work/INFRA/LIFECYCLE.md` §4.1 (items "Ids = what both seats accepted", "Seat tables by addendum; carrier
files", "Line endings"). Diff: `git -C C:/Users/felip/BVS-wt/INFRA-R06 diff` (read-only). Tests: block "INFRA R06" at
the end of `Theory_work/INFRA/tools/test_lifecycle.py`. Implementer's notes: `Theory_work/INFRA/R06FIX/REPORT.md` if
present (may be a draft).

## Do
1. Work only in disposable clones under a short temp path, e.g.
   `git -c core.longpaths=true clone --shared -q -c core.longpaths=true C:/Users/felip/BVS-wt/INFRA-R06
   C:/Users/felip/AppData/Local/Temp/r6s-<random>`, then copy the worktree's changed files (`git -C <worktree> diff
   --name-only`, plus untracked files under `Theory_work/INFRA/R06FIX/`) over the clone. For EOL probes use
   `git -c core.autocrlf=false|true clone ...` (and `checkout --force`; in Git Bash set `MSYS_NO_PATHCONV=1` for
   sparse-checkout patterns).
2. **Bypass analysis (main task).** Try to:
   - make a CHANGED file verify (any content change beyond a uniform CRLF<->LF conversion: lone CR, a CR moved,
     binary/NUL files, UTF-16, BOM, trailing newline, collisions between the three accepted variants, a manifest row
     whose recorded hash matches the variant of a different file, ADDED/REMOVED handling, `#EXTRA` directories);
   - make a stale accept record stay current, or make `sha256` / `status_sha256` / `fp2` differ between an LF and a
     CRLF clone (or between a frozen mixed tree and a clone);
   - make the addendum route accept something the council did not: NOT-EXAMINED or missing ids with a checked label
     (checkpoint or carrier), a decision string that should not count as ACCEPT, contradictory body/addendum rows,
     a second or rescored `COUNCIL-VERDICT` line in an addendum, tables in one seat only, local vs full ids, aliases;
   - make the carrier route accept something the council did not: statement / premise outside the manifest, the carrier
     itself as statement, status lines borrowed from a covered file for an id no seat accepted, `.md` carrier relative
     path resolution, a carrier in the ticket folder (would it break `verify`?).
   Report each route with severity (CRITICAL / MAJOR / MINOR), a reproduction (commands, exit codes, output) and a fix
   direction. Do not report intended fail-closed strictness as a defect unless it breaks a documented HQ workflow.
3. **Regression / real data.** Spot-check the implementer's evidence: (i) on HEAD, old vs new tools give identical
   `check.py --quiet --json` findings (401) and identical `check.py --acceptance <all 406 ids> --json` findings
   (1,783); (ii) on LF and CRLF clones, every `reviews/MANIFEST_*.txt` of theory/W3-START, W3-PSHARP, W3-MISR, W3-RM2
   gives with the new tool the same difference list as the OLD tool gives on the frozen worktrees
   (`C:/Users/felip/BVS-wt/W3-START`, `C:/Users/felip/BVS-wt/W3-RM2`,
   `C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-d4be6581-880c6173f796fa3a` (PSHARP),
   `C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-c2aa11df-8fc28a209b389288` (MISR) — READ ONLY);
   (iii) `ingest.py claims Theory_work/Wave3/W3-START/CHECKPOINT_3.md --staged` on fresh LF and CRLF clones of
   theory/W3-START with the new tools overlaid: exit 0, acceptance PASS for 21 claims (pre-R06 tools: REFUSED).
4. Run the full suite once in a fresh clone with the changes and no other probes in it:
   `python -B Theory_work/INFRA/tools/test_lifecycle.py` (expected all PASS; ~10+ minutes; wait for it).

## Output
`C:/Users/felip/BVS-wt/INFRA-R06/Theory_work/INFRA/R06FIX/R06FIX_review_sol.md` (the only file you write in that
worktree): overall verdict line first (HOLDS / HOLDS WITH MINOR FINDINGS / BYPASS FOUND); a table item (1 hashes,
2 fingerprints, 3a addendum, 3b seat tables, 3c carrier) -> verdict with evidence; findings (or "none found"), each with
severity, reproduction and fix direction; regression results; the suite result; scratch paths used. Keep it factual
and compact. End your run with a ≤ 5-line summary.
