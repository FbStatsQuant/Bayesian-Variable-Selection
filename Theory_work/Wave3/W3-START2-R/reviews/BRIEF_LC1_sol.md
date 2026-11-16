# BRIEF LC1 — line check, W3-START2-R: R1_VIS, R2_NEC; plus the statement-change check of the SL1 changelog rows
# (Sol, gpt-6.1-sol, high; fresh agent)

You are an independent line checker. You have not seen this ticket before. Read only the files listed; do **not** read
`LOG.md`, any `CHECKPOINT_*.md`, or anything under `reviews/` except this brief and the two files named in Part B.
**Do not edit, create or delete any file; change no git state.** Return your review as your final message (the lead
saves it verbatim to `reviews/LC1_line_check_sol.md`).

Repository root: `/home/fb31/BVS-wt/W3-START2-R`. Ticket folder: `Theory_work/Wave3/W3-START2-R/` (here "T/").

## Part A — line check
- Target statement (locked): `T/STATEMENT.md` v1.5 — (D3) and its relation paragraph (§2); [VIS-c], [VIS-m], [START-F],
  [F4], [NEC-b], [NEC] (§3.1); the supersession rows for these claims (§5).
- **Under check:** `T/lemmas/R1_VIS.md`, `T/lemmas/R2_NEC.md`.
- Consumed (read the cited lines; these parent files were checked before and are not under review, but every citation
  into them is): BASE = `Theory_work/Wave3/W3-START/` — `STATEMENT.md`, `lemmas/L1_AGG_FLOOR.md`, `lemmas/L2_TK.md`,
  `lemmas/L3_LEAK.md`, `lemmas/L4_VIS.md`, `lemmas/L5_ASM_STARTF.md`, `lemmas/L6_COROLLARIES.md`, `lemmas/L7_NEC.md`;
  PARENT = `Theory_work/Wave3/W3-START2/` — `STATEMENT.md`, `lemmas/P1_LEADING.md`, `lemmas/P3_NEC.md`.
What to check: every step correct; every citation says what is claimed; constants and thresholds depend only on what is
said (uniformity of (T1⁺⁺)(d)); quantifiers right; each file proves exactly its STATEMENT clauses, with no unstated
hypothesis. Try to break in particular: the exact price π_n(d, a; Q) in the copy of BASE L4.1 (both signs, log(p/c_Q) < 0
allowed); the copy of L4.2 with log(2p) kept; that only the visibility thresholds change in START-F⁺⁺ (via BASE L6.0);
the pointwise level and both drifting clauses of NEC-b⁺⁺ (large gains in (i) with no upper bound on the gain); the
pigeonhole for (N2⁺⁺); the example in R2.6; F4⁺⁺'s explicit bound (C_A, n_F); each "old premise ⇒ new premise" step.

## Part B — statement-change check (PROTOCOL_v4 §4.2)
Read `T/reviews/SL1_statement_lock_sol.md` (the lock review) and `T/reviews/SL1_disposition.md`, and the changelog
table at the foot of `T/STATEMENT.md`. For each changelog row of version 1.5: is the change made as described, is the
tag (STRONGER / EQUAL) right, and does any dependent clause break? In particular the STRONGER row: VIS-c⁺⁺, VIS-m⁺⁺ and
NEC-b⁺⁺ now take [TK] (quantitative form, BASE `STATEMENT.md:187-191`) in place of (E), (GF-16) — do R1/R2 prove them
under that hypothesis?

## Output format
- Per file: `| file | verdict |` (PASS / PASS WITH FIXES / FAIL); per changelog row: `| row | confirmed tag | OK? |`.
- Findings, numbered, each tagged **C** (step wrong or unproved), **S** (claims more than proved / unstated hypothesis),
  **F** (unfaithful to STATEMENT or a cited source/line) or **E** (editorial), with file:line, what fails, a fix.
- Final line: `LC1-VERDICT: PASS | PASS WITH FIXES | FAIL`.
