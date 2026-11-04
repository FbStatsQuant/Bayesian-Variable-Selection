# W7-SEP working notes

Branch `theory/W7-SEP` from `claude/theory-w7-sep-fq36cn` @ 6f93ea3 (= theory/campaign Wave-7 specs).

## Inputs read
PROTOCOL, THEORY_PRIORITIES, tasks/W7-SEP; W1-EXP REPORT (LH, Thms 3-6), W3-PXN REPORT (LH-iid P1-P8),
W4-T38FULL T38_STATEMENT + T38_PROOF §3 (Lemma LS-score, Lemma M, Thm b1, Prop LH-LAT, masking on LH),
W1-T37R REPORT (Thm A, TD', PGD, C3), W3-VT37R REPORT, F-DRAFT NEW_TARGETS (Thm W, W''), O-WSTAB PROOF head,
W4-SHARE REPORT (Prop M), O-BGIBBS REPORT (Thm BG1, Prop LH), DROPPED R-T20(i), METHODOLOGY §6.2-6.10, 00_COMMON budgets.

## Early finding (drives the plan)
The task's clause (a) says start-only methods *with the production local search* fail unless the greedy basin of S0
contains the start mode. On LH (exact Gram) and LH-iid this exception is exactly what happens:
S~0 = S° w.p. -> 1 and LS from S° scores S0 in c moves (T38(b1-LH), W3-PXN P5-P6). So (a) with local search is
FALSE on the task's own family. Plan: prove more — a greedy-universality proposition (Prop GU): under exact Gram,
SE, fixed signals and a finite relevant structure, the production LS from *every* relevant centre scores and
certifies S0. Hence no fixed-signal family of this kind separates "start + LS" from v3.

What *does* separate: iid start sampling and one-shot importance correction (sampling-only start methods).
Threshold budget Q* = p^c n^{c/2} (two-sided, from the T27 law) vs v3's polynomial ceiling O((n+p) p log^2 n);
separation iff c(a + 1/2) > a + max(1, a), i.e. iff c >= 2 (p = n^a). Super-polynomial only if c_n -> infinity.

## Plan
1. SEPARATION.md: statement + proofs of (a-iid), (a-IS = b), (a-LS negative: Prop GU), (c) citation.
2. scripts: exact LH computations at p <= 20 (c = 2, 3): pi0(S0), pi(S0), iid hit probs vs Q, IS rel. variance,
   LS from S~0, from iid draws, and from every centre (exhaustive) to test Prop GU.
3. REPORT.md.
