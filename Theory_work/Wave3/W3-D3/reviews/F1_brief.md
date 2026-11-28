# W3-D3 — F1 form check brief (Opus 5.5 high, new agent; saved before launch 2026-11-17)

Form check (PROTOCOL_v4 §7, FORM-ONLY re-freeze) for ticket W3-D3, worktree /home/fb31/BVS-wt/W3-D3 (read-only for you except
your reply file). Do not read LOG.md, CHECKPOINT files or dispositions. No git state changes.

**Context.** Council diff round R2 passed on `reviews/MANIFEST_R2.txt` (MANIFEST f559960469015b9c993e17cc82b3955ceee2890db189b8ae23e2aa2f1f4840a6;
seat review `reviews/R2_council_opus.md`, 9.3, gates=PASS; bind `reviews/R2_bind.txt`: OK). In the R2 tree five DEPS rows
(S:B3w, S:ExSG, P:B3w, P:ExSG, R:registry) were STALE although the R2 seat re-verified them in full (its §(b)). The lead has now
marked those rows as checked by the R2 review (`deps_hand.py`), changing only `DEPS.tsv`, and re-froze as
`reviews/MANIFEST_R2f.txt` (MANIFEST c52866ef738795c479b2853ec386d193df7069698fe4e6a20d8a4f66e567a5d3).

**Tasks.** (1) Run `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-D3 Theory_work/Wave3/W3-D3/reviews/MANIFEST_R2f.txt`
and compare the per-file rows of MANIFEST_R2 and MANIFEST_R2f: is DEPS.tsv the only changed file? (2) Read
`reviews/F1_form_diff.txt`: does the diff only set checked_sha/checked_by/state for those five rows, with checked_sha equal to
the current sha and the sha column unchanged? Recompute the five span hashes with deps_hand.py's rule (in memory or a scratch
copy under /home/fb31/BVS-wt/W3-D3/.rc_tmp/, deleted after) and confirm. (3) Confirm from `reviews/R2_council_opus.md` §(b) that
the R2 seat re-checked exactly those five rows in full.

**Reply.** Write `Theory_work/Wave3/W3-D3/reviews/F1_formcheck_opus.md` with one line `F1-VERDICT: FORM-ONLY` or
`F1-VERDICT: NOT FORM-ONLY` and your reasons (a few lines). Then end.
