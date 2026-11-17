# W3-D2 — L1 statement lock brief (Sol, fresh, blind first read; saved before launch 2026-11-17)

You are the statement-lock reviewer (PROTOCOL_v4 §3 step 1, Tier B) for ticket W3-D2 in the git worktree
/home/fb31/BVS-wt/W3-D2 (read-only for you except your reply file). Do not read LOG.md. No TMPDIR, no writes outside the
worktree; scratch only in /home/fb31/BVS-wt/W3-D2/.rc_tmp/ (delete it at the end). Do not run git commands that change state.

**Target.** Derive Theorem 2 (claims card row 1.2: posterior concentration on a random Gaussian design) from the
omitted-variables master `W3-MISR-R:CorGb-plus@1.0.1`, so that its eigenvalue floor is asked on smaller sets
(3(A+1)(s₀+1) log n instead of 5(A+1)(s₀+1) log n), with conclusions in expectation.

**Read (all paths relative to the worktree root):**
1. `Theory_work/Wave3/W3-D2/STATEMENT.md` (the object to lock), `PLAN.md`, `PROOF.md` (the proof route; you may check it,
   but your job is the statement), `TARGET.md`.
2. The master: `Theory_work/Wave3/W3-MISR-R/STATEMENT.md` §1–§3 (lines 1-108) and its proof
   `Theory_work/Wave3/W3-MISR-R/lemmas/G2_corr.md`; definitions it uses in `Theory_work/Wave3/W3-MISR/STATEMENT.md` §0 (lines 17-66)
   and `Theory_work/Wave3/W3-POST/STATEMENT.md` §0 (lines 16-39).
3. The floor arithmetic: `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md` (B1.3, B4.1).
4. The recorded row 1.2: `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` lines 257-320 (Theorem 2), lines 26-30
   ((S1), (S2)), and `Theory_work/Wave3/W3-READER/NOTATION.md` §1; card row `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:55`.
Registry rows (do not open the registry; quoted): `W3-MISR-R:CorGb-plus@1.0.1` "PROVED-CHECKED, conditional on W3-POST2:C,
W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6df…, sol=10.0 PASS, opus=9.6 PASS";
`W3-READER:R1@1.0.2` "PROVED-CHECKED; council R3, MANIFEST 7aebdf2e…, sol=9.5 PASS, opus=9.4 PASS";
`W3-POST2:C@1.0.6` "PROVED-CHECKED, conditional on W3-POST:Prop-LB, W2-APP:POST"; `W3-POST:Prop-LB@1.0.0` "PROVED (by this seat, unchecked)".

**Questions.** Try to break the statement.
- Is every hypothesis of CorGb-plus implied by (A1)–(A3) of Theorem 2X in the setting of STATEMENT §0, including the
  q = 0 instance (no omitted columns, degenerate (OV) with a = γ = τ² = 0)? Is any hypothesis used but not stated?
- Are the four displays of Theorem 2X and its explicit form (C, n*, b_n) faithful to what CorGb-plus plus the
  deterministic facts of §3 give? Quantifiers and dependence of constants right?
- Corollary 2X: are the recorded Theorem 2 hypotheses quoted faithfully, and do they imply (A1)–(A3)? Is the model's
  (α*, β*) deterministic in the recorded setting (as the corollary uses)?
- STATEMENT §7: is the tag STRONGER against the recorded row-1.2 reader statement right? Is the status/vanishing-floor
  caveat complete and correctly worded? List any other way in which the new form is weaker.
- List every interpretive sentence ("hence …", "this means …", readings) inside the claimed spans (§1, §2) and give each a
  verdict (RIDER_RULES: such sentences must be moved out or checked).
- Readability (PROGRAM.md "Readability"): is the Theorem 2X statement a clean reader statement (numbered primitive
  assumptions, ≤ 3–4 displays, no internal ids)?

**Reply.** Write your reply to `Theory_work/Wave3/W3-D2/reviews/L1_statement_lock_sol.md`: verdict line
`LOCK` / `LOCK-WITH-AMENDMENTS` / `NO-LOCK`; findings numbered L1-1, L1-2, …, each tagged C (correctness), S (strength:
claims more than proved or uses an unstated hypothesis), F (faithfulness) or E (editorial), with the line and the fix;
answers to the questions above. Then end.
