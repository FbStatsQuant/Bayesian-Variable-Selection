# R05FIX — independent correctness review (Sol) — brief

Context: this is a software-correctness review of a research-project bookkeeping tool (a Python registry of
mathematical claims and the checks that decide when a claim counts as reviewed). No security testing is involved.

You are an independent correctness reviewer (Codex GPT-6.1 Sol, effort high). The change is committed on branch
`infra/R05-ckpt-status` of the repository `C:/Users/felip/Bayesian-Variable-Selection` (head given in your task
message; base main c8a970f). **Change no git state in any existing checkout or worktree** and do not touch the main
checkout's working files, any live registry, scheduled task or hold file. Start no subagents. The only file you write
outside your scratch clones is your output, given below.

## What changed and why
Acceptance (`check.py --acceptance`, check A4) required the frozen council manifest to cover each claim's statement,
premise AND status-source files. Wave 3 tickets write per-claim status lines in their own `CHECKPOINT_<k>.md`, which
`Theory_work/Wave3/tools/manifest.py` never covers by design, so every such ticket was refused. The fix exempts the
ticket's own checkpoint as status source, under five safeguards that are the subject of this review:
1. Only the ticket's OWN `CHECKPOINT_<k>.md` (directly in the ticket folder), and only as status source; statement and
   premise files must still be covered.
2. Council review files bind to the acceptance manifest with a PASS verdict (≥ 8.0, gates PASS); earlier review rounds
   bind to their own manifests.
3. At ingest the checkpoint's content digest is recorded in the row (`status_sha256`, committed with the ingest);
   `check.py` (CI) flags any later edit (check C12-checkpoint) and acceptance refuses.
4. The claim ids of the checkpoint equal the ids each council seat accepted (no extra, no missing).
5. Each review round id cited in a status line resolves to exactly one existing review file, which quotes a frozen
   manifest digest.
Read the rule as documented in `Theory_work/INFRA/LIFECYCLE.md` §4.1 "Checkpoint status source" and the `check.py`
docstring (A4, C12). Code: `git diff c8a970f <head> -- Theory_work/INFRA` — mainly `tools/bvsreg.py`
(section "checkpoint status sources (INFRA R05)", `manifest_problems`, `council_problems`, `ACCEPT_FIELDS`, the new
`status_sha256` column), `tools/check.py` (C12, A4 call), `tools/ingest.py` (`new_row`), `tools/registry.py`,
`tools/propagate.py`; tests in `tools/test_lifecycle.py`, block "INFRA R05".

## Do
1. Work only in disposable clones under a short temp path (long paths fail on Windows), e.g.
   `git -c core.longpaths=true clone --no-hardlinks --quiet -c core.longpaths=true --branch infra/R05-ckpt-status
   C:/Users/felip/Bayesian-Variable-Selection C:/Users/felip/AppData/Local/Temp/r5s-<random>`.
2. **Bypass analysis (main task).** For each safeguard 1–5, try to obtain an acceptance PASS (`check.py --quiet
   --acceptance <ids>` exit 0, or `ingest.py claims <CHECKPOINT>.md --staged` reporting acceptance PASS) for a claim
   that violates it: e.g. a status source that is not the ticket's own checkpoint (other folder, sub-folder, other
   ticket, case or path tricks, `..`, tickets.tsv `folder` edits), an uncovered statement or premise, a council seat
   not bound to the acceptance manifest, an earlier round's review quoting no / a foreign digest, an edit of the
   checkpoint after ingest that neither C12 nor acceptance notices, a way to set or refresh `status_sha256` other
   than ingest / status-change tools, checkpoint ids ≠ a seat's accepted ids (table parsing, local vs full ids,
   duplicated or contradictory rows, multiple tables, aliases), a cited round id that is unresolved or ambiguous yet
   accepted, a round citation the grammar silently misses in a way that matters. Report each route with severity
   (CRITICAL / MAJOR / MINOR), a reproduction (commands, exit codes, relevant output) and a fix direction. Do not
   report intended fail-closed strictness as a defect unless it breaks a documented workflow; you may note limits of
   the citation grammar as MINOR/NOTE with reasoning.
3. **Regression.** Check that claims whose status source is NOT a checkpoint behave exactly as before (coverage still
   required; no verdict change). The implementer's evidence: on main c8a970f, old vs new tools give identical
   `check.py --json` findings (401) and identical `check.py --acceptance <all 406 ids> --json` findings (1,783).
   Reproduce or spot-check this.
4. **W3-START dry run.** Reproduce: clone `theory/W3-START` (808ddd1); copy every tracked file byte-for-byte from the
   worktree `C:/Users/felip/BVS-wt/W3-START` (read only! its two CRLF inputs are what MANIFEST_R2 hashed; a fresh
   checkout does not verify) over the clone; overlay `Theory_work/INFRA/tools/*.py` from the R05 branch; run
   `python -B Theory_work/INFRA/tools/ingest.py claims Theory_work/Wave3/W3-START/CHECKPOINT_3.md --staged`.
   Implementer's result: exit 0, 0 ERROR, acceptance PASS for all 21 claims (old tools: 21 × A4 coverage refusals).
   Confirm, and confirm the new checks were actually exercised (not vacuous) on that data.
5. Run the full suite once in a fresh clone of the branch with no other probes in it:
   `python -B Theory_work/INFRA/tools/test_lifecycle.py` (expected all PASS; it takes ~10 minutes; wait for it).

## Output
`C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-2e671d0e-a49ad4d4306276ae/Theory_work/INFRA/R05FIX/R05FIX_review_sol.md`
(the only file you write in that worktree; it is uncommitted there): overall verdict line first (SAFEGUARDS HOLD /
HOLD WITH MINOR FINDINGS / BYPASS FOUND); a table safeguard 1–5 → verdict with evidence; findings (or "none found"),
each with severity, reproduction and fix direction; regression and dry-run results; the suite result; scratch paths
used. Keep it factual and compact. End your run with a ≤ 5-line summary.
