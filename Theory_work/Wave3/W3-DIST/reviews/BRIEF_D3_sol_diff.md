# W3-DIST — diff check D3 (re-check of the amendments made after D1 and D2) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent checker, new to this ticket. Repo clone `/home/fb31/Bayesian-Variable-Selection`; ticket folder
`Theory_work/Wave3/W3-DIST/` (paths below are relative to it). **Read-only except your one output file
`reviews/D3_sol_diff.md`.** Run no git command that changes state; start no agents; no cluster jobs; any computation small
and `nice`. Any temporary file goes under `/home/fb31/SMC_Theory_Department/tmp/20261116-W3-DIST-D3/` (never `/tmp`); remove
it when done. This is a short task: about sixty changed lines, given as an exact diff in `reviews/DIFFS_D3.patch`
(three blocks). The files change no further while you work; if a hash below does not match, say so and stop.

Two diff checks raised the findings behind these edits: `reviews/D1_sol_diff.md` (D1-01 … D1-04) and
`reviews/D2_sol_NEC_diff.md` (D2-01). Read those findings, the patch, and as much of the surrounding text as you need.
Decide, hunk by hunk, whether the amendment resolves its finding and whether the amended text is correct as it now reads.

1. **D1-01** — `work/D_output/P6_DISTC.md`, amendment A-10 (finiteness of the marginal likelihood m(S)). Check the corrected
   argument against the locked identification it cites: [P1] =
   `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`
   (`thm:T01i`): the N-dimensional contrast likelihood, the inverse-gamma shape 0.51 and rate 0.01·s_y², the moment
   E[v^{−N/2}], the factor between m(S) and the contrast marginal likelihood. Is the bound right and is anything still
   mixed up? Does any other line of the file depend on the old form?
2. **D1-02** — `STATEMENT.md`, Theorem DIST-C (C-i): the event of the predictive sentence is now written out. Does (C-i)
   as it now reads match what `work/D_output/P6_DISTC.md` §6 (C-i) proves? **Tag to confirm or contest:** the changelog
   row 1.4.8 says **EQUAL on TC8**, where TC8 (`TARGET.md` §5) reads "(C-0) and the deterministic parts of (C-i), (C-iii);
   every delivery statement jointly with {completed} and under its named premise". Answer CONFIRMED or CONTESTED with the
   reason; if contested, say whether you read the change as WEAKER on TC8.
3. **D1-03, D1-04** — `STATEMENT.md`, changelog rows of v1.4 for Corollary C, the Remarks of §1R and the bridges: the tags
   were split. For each of the three rows: is every part now tagged in the right direction (STRONGER / WEAKER / EQUAL),
   is the described content accurate, and is the range change of the last bridge bullet (D1-03) recorded? The Corollary C
   row records a go from HQ for the STRONGER part; that is a record of a decision, not for you to verify. Do verify
   the mathematics it refers to: **Corollary C's conclusion that, when a completed run scored the true model and its
   posterior probability exceeds ½, the true model is the model the method reports as most probable** (`STATEMENT.md` §1R,
   Corollary C; proof `work/D_output/COR_C.md` C2 and `work/D_output/P6_DISTC.md` Corollary R1; code
   `Scripts/SMC_BVS/core/v3_run.R:142` and the store in `Scripts/SMC_BVS/core/cpp/v3_ledger.h`). This conclusion was added at
   v1.4; check it line by line, including ties, the exact-arithmetic convention and what "reports" means in the code.
4. The "check" column of the changelog rows 1.4 … 1.4.7 now quotes D1's verdicts. Spot-check five rows against
   `reviews/D1_sol_diff.md` (among them 1.4.7 and the DIST-C row).
5. **D2-01** — `lemmas/NEC.md` §8(d): the numerical remark was reworded with the reviewer's text. Resolved? Anything
   still asserted about the full posterior that the restricted calculation does not give?
6. Does the patch contain any change that answers none of D1-01 … D1-04, D2-01 (apart from version lines)? Does any
   hunk alter a theorem, a lemma, a constant or a proof step other than as described?

Hashes (sha256, first 16 hex) at launch: `STATEMENT.md` 1662ba905918bb90; `work/D_output/P6_DISTC.md` 0b0b1556cfba806b;
`lemmas/NEC.md` 48cb55be4d967f3e; `work/D_output/COR_C.md` 55d8b14f968de040.

Output (`reviews/D3_sol_diff.md`): first line `D3 diff check — STATEMENT.md <16 hex>; work/D_output/P6_DISTC.md <16 hex>;
lemmas/NEC.md <16 hex>; work/D_output/COR_C.md <16 hex>`. Findings with id (D3-xx), severity (CRITICAL / MAJOR / MINOR / NIT),
place, the error in full, minimal repair. Verdict lines: items 1–6, each RESOLVED / NOT RESOLVED (items 1, 2, 5),
CONFIRMED / CONTESTED (the tags of items 2, 3), VERIFIED / NOT VERIFIED (the Corollary C conclusion of item 3); then one
line per file as it now stands (`work/D_output/P6_DISTC.md`: Lemma P6, Theorem DIST-C; `lemmas/NEC.md`; `STATEMENT.md`
DIST-C (C-i); Corollary C): VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Final line: overall verdict. Do not soften
findings; say exactly what you could not check.
