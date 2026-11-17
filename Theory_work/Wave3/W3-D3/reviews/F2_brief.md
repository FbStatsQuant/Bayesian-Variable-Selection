# W3-D3 — F2 form check brief (Opus 5.5 high, new agent; saved before launch 2026-11-17)

Form check (PROTOCOL_v4 §7, FORM-ONLY re-freeze) for ticket W3-D3, worktree /home/fb31/BVS-wt/W3-D3 (read-only for you except
your reply file). Do not read LOG.md, CHECKPOINT files or dispositions. No git state changes.

**Context.** The council passed on `reviews/MANIFEST_R2f.txt` (MANIFEST c52866ef738795c479b2853ec386d193df7069698fe4e6a20d8a4f66e567a5d3;
carrier `reviews/R2f_record_opus.md`, seat review `reviews/R2_council_opus.md`, 9.3, gates PASS). A binding HQ decision (H5 card 17)
then changed the class-1 anchoring wording: **the class-1 anchor of (A4) is Narisetty–He (2014, Lemma 6.1) only**; "implies
Song and Liang's Condition 1" is dropped *as an anchor* everywhere and may stay only as a separate factual remark ("it also
implies Song–Liang's Condition 1 for centred rows"). The lead edited STATEMENT §5 (outside the registered claim spans §§1–3),
REPORT §2 and the §3 card text, READER_DELTA's class paragraph, TARGET's class cell, PLAN (a supersession note), STATEMENT's
header and changelog (row 1.4), and re-hashed DEPS (S:class, which covers §5, now names this review as its check). Re-frozen as
`reviews/MANIFEST_R2g.txt` (MANIFEST c41a5b3485d712770989cc3c82a621fe8f5690f976bb8bb0378a188efa40665f). The diff:
`reviews/F2_form_diff.txt`.

**Tasks.** (1) `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-D3 Theory_work/Wave3/W3-D3/reviews/MANIFEST_R2g.txt`;
compare MANIFEST_R2f and MANIFEST_R2g: which files changed, and are the external inputs and every lemma/numerics file unchanged?
(2) Read the whole diff. Confirm: no change inside the registered claim spans (STATEMENT §§1–3) or in `lemmas/`; the REPORT §6
registry blocks unchanged in content; every mathematical relation stated is unchanged and still true (NH14's rows as the case
Σ = I for centred rows; (A4) ⇒ Song–Liang Condition 1 for z = x − m_n); the new wording makes NH14 the only anchor and presents
the Song–Liang implication only as a separate factual remark, with the centring qualifier, in every place it appears (STATEMENT §5,
REPORT §2 and §3, READER_DELTA, TARGET, PLAN). Search the frozen ticket for any remaining sentence that presents Song–Liang's
Condition 1 as a class-1 anchor. (3) DEPS: recompute the S:class span hash with deps_hand.py's rule (in memory) and confirm its
row; confirm the other nine rows are unchanged in sha and still OK. (4) Confirm the changelog row 1.4 tag (EQUAL, outside spans).

**Reply.** Write `Theory_work/Wave3/W3-D3/reviews/F2_formcheck_opus.md` with one line `F2-VERDICT: FORM-ONLY` or
`F2-VERDICT: NOT FORM-ONLY` and your reasons (a few lines; list any remaining anchor sentence by file:line). Then end.
