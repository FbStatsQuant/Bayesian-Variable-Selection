# Pre-check P4 — stream B: Lemma H, Lemma T, Theorem DIST-3
Read `Theory_work/Wave3/W3-DIST/briefs/PRECHECK_COMMON.md` first. Output file: `Theory_work/Wave3/W3-DIST/reviews/P4_opus_precheck_B.md`.
Proof files: `Theory_work/Wave3/W3-DIST/work/B_transfer/H.md`, `T.md`, `DIST3.md` (statements: STATEMENT §3 Lemma H,
Lemma T; §1 Theorem DIST-3 with its (TR₀), (L₀), notes (i)–(iii)). Also readable: the check scripts in that folder and
`Theory_work/Wave3/W3-POST2/lemmas/D_hellinger.md` (D0, D1, for comparison only).
Comparison material for Lemma T (independent attempts, unchecked): `Theory_work/Wave3/W3-DIST/work/api_attempts/dist1/T-a-1.md`,
`T-b-1.md`, `T-c-1.md`.
Specific duties. (1) T.md proves a one-sided inequality P(∃A: P(A) > 2P_n(A) + η²) ≤ 2S(2n)e^{−nη²/4} for nη² ≥ 25 by a
ghost sample with Cantelli's bound and random swaps with Hoeffding: recompute every constant of that argument (the
author says the Cantelli step has little slack: 0.284 against 1/4); check the symmetrisation step by step, the
conditioning, the union over the traces on 2n points, and the measurability reduction. (2) Check the growth-function
bound for unions of two affine half-spaces on at most d of P coordinates and the claim that the stated η²_n(d, δ) always
gives nη² > 36. (3) Check the layer-cake step from sets to the truncated quadratic loss, simultaneously in (a, u, c).
(4) Compare with T-a-1 and T-c-1, which claim the same statement through the classical ratio-type inequality with
cited external facts: do the three derivations agree on the final statement and constants; which external facts
would need a citation check; is the self-contained route of T.md preferable? (5) DIST3.md: the fixed-design step, the
integration over the design, the constant c = 1, the dependence of n₀, and the three requested wording clarifications.
