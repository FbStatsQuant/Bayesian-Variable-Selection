# Brief — Sol read of X1, X3, X5 (v1.1): statement lock + line check + re-check of the LC2 repairs
# (Codex gpt-6.1-sol, high)

Manager 11-16: one Sol read serves as the lock, the line check and the re-check of the repairs. Read only; write no
files; change no git state; start no sub-agents. Workspace: `/home/fb31/BVS-wt/W3-AUDIT`.

**Part A — blind (do this first, before opening any review file).** Read
`Theory_work/Wave3/W3-AUDIT/track_A_X/{X1_T12,X3_L1A,X5_POOLZ}/{STATEMENT,PROOF}.md` and the sources they cite:
T12 `Docs/Theory/proofs/T12_T8_frozen_run_identities/{STATEMENT.md,PROOF_v6.tex}`; `Theory_work/Wave1/W1-N1/{STATEMENT.md,lemmas/L1_bridge.md}`;
`Theory_work/Wave3/W3-SAMP/{STATEMENT.md,lemmas/CC_code_check.md}`; `Theory_work/Wave3/W3-POST/{STATEMENT.md,lemmas/L1a_size_tail.md}`;
`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`; `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`;
the sibling statements `Theory_work/Wave3/W3-AUDIT/track_A/{T1_GW,T5_CAL,T6_START,T7_KER}/STATEMENT.md` (inputs, not under
review); for X5 the claim in the worktree `/home/fb31/BVS-wt/W3-READER`, file `Theory_work/Wave3/W3-READER/STATEMENT.md`
lines 12–37; the code `Scripts/SMC_BVS/core/` (pin 4676af6 = HEAD). Do not open LOG, INDEX, CHECKPOINT or CHECK files.
For each item: (1) **lock** — right target (X1: T12 (i.a)–(i.c), (ii), (R1)–(R3) for the code of record; X3: a line check
of W3-POST:Lemma-1a′; X5: a line check of W3-READER:PoolZ), faithful to sources, hypotheses explicit, nothing claimed
beyond the proof: LOCK / LOCK WITH CHANGES / DO NOT LOCK; (2) **line check** — every step, every citation: VERIFIED /
VERIFIED WITH AMENDMENTS / NOT VERIFIED.

**Part B — re-check (after Part A).** Read `Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/LC2_reply_opus.md` (an earlier
Claude line check of v1.0) and the STATEMENT changelogs; for each LC2 finding say RESOLVED / NOT RESOLVED in v1.1, and
whether any repair broke something.

Reply (final message, plain markdown): Part A verdicts per item; Part B table; numbered findings tagged C / S / F / E with
file:line and the fix. Last line: `X-SOL-VERDICT: X1 lock=<…>, check=<…>; X3 lock=<…>, check=<…>; X5 lock=<…>, check=<…>`.
