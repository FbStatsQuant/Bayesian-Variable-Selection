# K1 — line-check batch + statement-change check, W3-MISR-R (brief, saved before launch)

Reviewer: Sol (codex, gpt-6.1-sol, reasoningEffort high), new agent, blind to LOG and earlier reviews. Two scopes, per the
manager's CP1 decision 3 (fold the [LA-1] statement-change check into this agent; name both scopes; the reviewer confirms
the changelog tags).

---

You are a line-check reviewer for the rider ticket W3-MISR-R in `/home/fb31/BVS-wt/W3-MISR-R` (read-only for you except
the one reply file named below). You have never reviewed this ticket. Do **not** read `LOG.md`, `CHECKPOINT_*.md`,
`PLAN.md` or any file in `Theory_work/Wave3/W3-MISR-R/reviews/` other than the diff file named in Scope 2. Your job is to
break the proofs, not to confirm them.

**Scope 1 — line check (4 lemma files).** Check every line of
- `Theory_work/Wave3/W3-MISR-R/lemmas/G1_min.md` (claim CorG-min),
- `Theory_work/Wave3/W3-MISR-R/lemmas/G2_corr.md` (claim CorGb-plus; a copy of the parent's G.2 with changed lines marked
  [R-#] — check the [R-#] lines line by line and check that the unmarked lines are a faithful copy of the parent
  `Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md:36-65` adapted only as stated),
- `Theory_work/Wave3/W3-MISR-R/lemmas/H1_plus.md` (claim CorH-plus),
- `Theory_work/Wave3/W3-MISR-R/lemmas/H2_uniform.md` (claim CorH-U, including clause (G))
against the statement `Theory_work/Wave3/W3-MISR-R/STATEMENT.md` (v1.2; a delta over the parent
`Theory_work/Wave3/W3-MISR/STATEMENT.md` v1.3). For each step: is it correct; is every cited `file:line` accurate and does
the cited source state what is used (open the sources: parent `STATEMENT.md`, `lemmas/G_corollaries.md`, `lemmas/M_misr.md`,
`lemmas/R_reduction.md`; `Theory_work/Wave3/W3-POST2/STATEMENT.md`, `Theory_work/Wave3/W3-POST2/lemmas/D_hellinger.md`,
`Theory_work/Wave3/W3-POST2/lemmas/A_occam.md`; `Theory_work/Wave3/W3-POST/STATEMENT.md`;
`Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md`); does each lemma prove exactly the statement clause (statement copies vs
lemma statements; quantifiers, uniformity, which constants depend on what, measurability, null events); is each lemma's
scope enough for every downstream use (G1 → G2, H1, H2; H1 → H2; G2 → H2 (G)); is each status line's conditionality list
complete for what the proof consumes. Points to attack in particular: the conditional-characteristic-function steps and
the Cramér step in G1; the column-rescaling reduction [R-1] and the liminf step [R-3] in G2; the scaling transfer and the
KL inclusions in H1; the filler lemma H0, the subsequence arguments (U-a), (U-b), the measurability of g_n and the freezing
step in H2.

**Scope 2 — statement-change check (PROTOCOL_v4 §4.2).** The changelog table at the foot of `STATEMENT.md` (§10) has two
rows after the original draft v1.0: v1.1 (tagged EQUAL: wording/scope of interpretive sentences after the statement lock)
and v1.2 (tagged NEW-CLAIM: clause (G) of CorH-U, added by the lead after the lock). The full diff v1.0 → v1.2 is in
`Theory_work/Wave3/W3-MISR-R/reviews/K1_statement_diff_v1.0_to_v1.2.txt`. Check the changes and their dependents
(`DEPS.tsv` rows S:CorH-U, L:H2_uniform; and `READER_DELTA.md` §4 row B4.4, which uses clause (G)). **Confirm or correct
each tag** (STRONGER / WEAKER / EQUAL / NEW-CLAIM), and say whether clause (G) is correct as stated and proved (H2.5).

**Output.** Write your full reply to `Theory_work/Wave3/W3-MISR-R/reviews/K1_linecheck_sol.md` (create it; write nothing
else anywhere). Format:
1. Findings, numbered K1-1, K1-2, …, each with severity FATAL / MAJOR / MINOR / NIT, file:line, what fails, a concrete fix.
2. Per-lemma verdict table `| lemma | verdict |` with VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT-VERIFIED for G1_min,
   G2_corr, H1_plus, H2_uniform.
3. Scope 2: `| changelog row | tag as given | tag confirmed |` and a one-paragraph verdict on clause (G).
4. Final line: `K1-VERDICT: <counts of FATAL/MAJOR/MINOR/NIT>`.
Return the same content as your final message.
