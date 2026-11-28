# SENIOR SIGN-OFF BRIEF (TH-SONG-ASSUMPTIONS, Stage 2 — the single Final Council pass)

You are one of the two **senior judges** (Fable 5.2, Astra 6.2) of the owner-ordered Completeness, Generality & Naturalness Review. Your Stage 1 report is `council/SENIOR_<SEAT>.md`. The Proposers (Task Lead Opus 5.5 plus the original drafting advisors Fable 5.2 and Astra 6.2) have answered it, and the Lead has applied the result as **v1.4**. This is the **one concise sign-off pass**. The owner capped the discussion at one round, so there is no further round unless the Manager approves one.

## Read
Folder: `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/song_assumptions/`
1. Your own Stage 1 report, `council/SENIOR_<SEAT>.md`, and the other judge's, for context.
2. `council/SENIOR_PROPOSAL_LEAD.md` (the Lead proposal) and `advisors/SENIOR_RESPONSE_FABLE.md`, `advisors/SENIOR_RESPONSE_ASTRA.md` (the advisors' replies).
3. **`council/V14_CHANGESPEC.md`**: the converged canonical text. This is the main object you are signing off.
4. **`council/V14_DIFF.diff`**: the v1.3 → v1.4 diff of the four package files (THEOREM_DEFINITIONS, ASSUMPTIONS_AND_PROOF_PATHS, OWNER_DEFENSIBILITY_DOSSIER, SIMULATION_DATA_ANALYSIS). Open the full files wherever the diff needs context.

## Questions (answer briefly)
1. **Resolution.** For each of your Stage 1 findings (C-x IDs and table rows), mark it RESOLVED, PARTLY or NOT RESOLVED, in one line each.
2. **Correctness of the new statements.** Is anything mathematically wrong in A-MARGIN-U (population form: U1/U2a/U2b, ā, m̄_d, Q_n, special cases, C-i/C-ii), in Lemma W, or in the other changed statements (A-MARGIN-H, windows k_n, A-NEC, A-DIM′, A-BS′, A-MIS(iii) primitive form, A-SPARSE-C, TM-a0-inc, converse, sieve)? Name the location and the fix.
3. **Generality (owner top priority).** Does any **statement** still contain an AR(1)/S1/S2-specific element or a simulation constant? S1/S2 may appear only in evidence items.
4. **Faithfulness.** Is there anywhere the package files contradict V14_CHANGESPEC, or where the v1.4 edits leave a v1.3 claim that is now false (for example "C ≈ 121 implied", "every m ≤ J active", "margin holds there", upward-rounded minima)?
5. **Verdict:** SIGN-OFF, or SIGN-OFF WITH FIXES (list them, each a one-line edit), or NOT SIGNED (a blocker only). Then give scores 0–10 for completeness, generality/naturalness and readiness for the owner's assumption-by-assumption Q&A.

## Rules
- Read-only, except for writing ONLY `council/SIGNOFF_<SEAT>.md` (SEAT = FABLE or ASTRA), at most 80 lines. Never delete files. Do not commit. Do not spawn subagents.
- Scratch only under `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/`: never /tmp, never outside the worktree. Never read or write under `/home/fb31/Bayesian-Variable-Selection/_local/engineering/`. No cluster jobs.
- For any Python or R: `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` and run under `nice -n 10`.
- Substantive points only: no stylistic nitpicks and no new scope. This is a sign-off, not a new review.

Reply with a summary of at most 8 lines: the verdict, the scores, and any fixes.
