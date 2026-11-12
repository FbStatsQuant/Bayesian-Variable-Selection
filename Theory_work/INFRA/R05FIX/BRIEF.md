# INFRA tool fix R05 — checkpoint status source — brief (HQ, 2026-11-12)

Implementer: Claude Opus 5.5, effort high, Claude Work. Fresh worktree of main c8a970f; branch
`infra/R05-ckpt-status` (commit only there; HQ merges).

## Defect
The W3-START CP3 acceptance (branch `theory/W3-START` @ 808ddd1) was refused by a tool defect, not by the mathematics:
`Theory_work/INFRA/tools/bvsreg.py`'s coverage rule requires each claim's status-source file to be in the frozen
manifest. Wave 3 tickets write their status lines in their own `CHECKPOINT_<k>.md`, which manifests exclude by design
(a status line written after the council cannot be inside the manifest the council reviewed). Record and decision:
`Theory_work/Wave3/HQ_DECISIONS.md` (last two entries); W3-START `LOG.md` tail and `CHECKPOINT_3.md` §7.1.

## Fix, with ALL of these safeguards
1. Exempt only the ticket's OWN `CHECKPOINT_<k>.md` (same ticket folder), and only as the status source. Statement
   spans and premise files must still be covered by the manifest.
2. Council review files must bind to the acceptance manifest with a PASS verdict (≥ 8.0, gates pass). Earlier review
   rounds bind to their own manifests, not the acceptance one.
3. At ingest, record the checkpoint file's sha256 in the registry row, committed with the ingest. check.py / CI flag
   later edits of that checkpoint.
4. The claim ids in the checkpoint must equal the ids both council seats accepted (no extra, no missing).
5. Check (e) is tool-enforced: each review round id cited in a status line resolves to exactly one existing review
   file, and that file quotes a manifest digest.

## Tests
Positive and negative tests in `test_lifecycle.py`: unbound review, an arbitrary uncovered status file, an uncovered
statement, an extra claim id, an unresolvable or ambiguous round id. Re-run the checks on the already-accepted
tickets / registry and show that no verdict changes. Then run the W3-START staged acceptance as a dry run against
`theory/W3-START` (808ddd1) and report whether it now passes. Change nothing in the live registry.

## Review
When code and tests pass: ONE Codex Sol reviewer (`delegate_task`, provider codex, model gpt-6.1-sol, reasoningEffort
high), blind, with a brief and manifest like R04FIX; it reviews correctness and checks that the safeguards cannot be
bypassed. Fix its findings, with one re-check if any finding is MAJOR or worse. Write
`Theory_work/INFRA/R05FIX/{BRIEF.md, REPORT.md, review files}`.

Rules: Claude helpers only on claudeAgent at effort ≤ high, never claude-personal. Do not touch theorem files or other
tickets.
