# RC1 disposition (lead) — reconciliation review by Codex gpt-6.1-sol (high)

Review: `RC1_reconciliation_sol.md`, manifest 94c0349e10ddd9354fe9317803559f78d8d05f1682bf8e5d2d10e3f1a863c735
(STATEMENT v1.1; a copy of the reviewed text is kept as `STATEMENT_v1.1_as_reviewed_by_RC1.md` for the diff check).
Verdict: **LOCK WITH CHANGES**. Per finding: R1, R2, R3, R5, R6, O1–O4 RESOLVED; R4 PARTIALLY RESOLVED (one
remaining MAJOR, record only: dependency edges and a status condition in the registry block); one new MINOR defect
N1 (a stale exponent equality in §6). No CRITICAL; "no new mathematical defect found in the revised width constants,
regression domain, toolkit premises or example exponent choices".

Both items are accepted and applied → `STATEMENT.md` **v1.2 LOCKED** (markers [RC1-#]).

| item | required | action in v1.2 |
|---|---|---|
| R4 (MAJOR, record) | add to RM2-F's `depends_on`: W3-RM2:W-suff, W3-RM2:W-conv; to RM2-R's: W3-RM2:D-to-W, W3-RM2:W-conv, W3-RM:B9; give W-suff the edge C-GROW:L2.3@proof and D-to-W the edges W2-LOC2:NA-R@proof, W3-RM:D-loc@proof; carry "conditional on W3-RM:B9@1.0.0 for (P10) unless re-proved" in RM2-R's status and disclose it in §5 | all added verbatim, with one deviation: the edge to W3-RM:B9 is written `@hyp`, not `@stmt`, because B9's status is "PROVED (by this seat, unchecked)" and the registry template allows a premise below PROVED-CHECKED only as an `@hyp` edge with the condition in the status (`Theory_work/INFRA/templates/ASSUMPTION_MAP.md:51-52`). §5 now lists W3-RM:B9@1.0.0 among the conditional inputs, C-GROW:L2.3@1.0.0 ("PROVED-CHECKED") among the re-run engines and W3-RM:D-loc@1.0.0 among the templates |
| N1 (MINOR) | §6: replace "ρ > 1/(4α), b = 1/(2α)" by "b > 1/(2α) and ρ > ρ* > 1/(4α), choosing both enlargements with strict slack as in (C5)" | replaced verbatim |

No hypothesis of (C1)/(C2), no claim (C3)–(C5) and no bridge statement (P0)–(P10) differs between v1.1 and v1.2;
the diff consists of the header, the two §5 lines, the §6 phrase and the registry block. Per PROTOCOL rule 15 an
independent Sol reviewer checks the diff (round RC2) and attests whether it is record/editorial only.
