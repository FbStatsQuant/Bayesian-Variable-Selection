# SENIOR REVIEW BRIEF: Completeness, Generality & Naturalness (TH-SONG-ASSUMPTIONS, Stage 1)

You are one of two fresh, independent **senior judges**: Fable 5.2 and Astra 6.2. The owner ordered this review after Council R2 was accepted as PASSED.

The package defines the **target theorems** and conjectures **defensible assumptions** for our SMC-BVS paper. The paper uses a coded g-prior with g = n, a unit ridge, a BB(1, b) size prior and an IG σ² prior. The package also maps Song & Liang (2015) (SL) one-to-one onto our setting. It contains **no proofs and no Lean**: it gives statements, proof paths, citations and S1/S2 simulation evidence.

## Read (in full)
Folder: `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/song_assumptions/`
- `THEOREM_DEFINITIONS.md`: targets TD, TD-as, TS-a, TS-b, TM-a0, TM-a, TM-b and the SL map.
- `ASSUMPTIONS_AND_PROOF_PATHS.md`: each assumption, its defence and its weaker alternatives, plus the proof paths.
- `OWNER_DEFENSIBILITY_DOSSIER.md`: the owner's Q&A, one section per assumption.
- `SIMULATION_DATA_ANALYSIS.md`: the S1/S2 evidence (E1–E9b).
- Optional context: `COUNCIL_RECORD.md` (prior rounds). The staged sources are under `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/song/`: `papers/32.txt` is the SL main paper, `papers/32b.txt` the SL supplement, and `ms/` the delivered manuscript TeX.

## Two questions (owner mandate)
1. **Completeness.** Did we miss anything important? Consider:
   - a hidden technical requirement;
   - a gap in a proof path (an unstated step, quantifier, event or uniformity);
   - a missing assumption a referee would expect;
   - a key SL 2015 counterpart that is absent or mis-mapped.
2. **Generality & naturalness (OWNER TOP PRIORITY).**
   - Every assumption must be stated in a **general, design-agnostic** form for the high-dimensional linear-regression BVS problem with our priors.
   - No assumption may assume AR(1), a Toeplitz design, a specific ρ, s0 = 10, the S1/S2 coefficient patterns or S1/S2 constants. Nothing may look reverse-engineered from our simulations.
   - Benchmark: SL 2015's conditions read as general, natural BVS assumptions even where the method struggles. Sparse-eigenvalue lower bounds, sub-Gaussian designs, beta-min/margin conditions and dimension growth rates are the right genre.
   - S1/S2 belong **only** in the verification and reasonableness evidence.
   - For each assumption (A-GL, A-SPARSE, A-DIM, A-DIM′, A-SUBG, A-NEC, A-BS, A-BS′, A-MARGIN-H, A-MARGIN-U, A-MIS(iii), A-MOM), judge whether its **statement** is general and natural.
   - Flag any constant, quantity or phrasing that feels artificial or S1/S2-tied. Examples might be:
     - a design-dependent width w_Dm(X) that reads as engineered;
     - a constant C defined only through a proof step;
     - a margin that is hard to interpret;
     - a window that only makes sense for our priors.
   - For each flagged item, either propose a **clean general re-expression** (a standard-feeling form) or propose **dropping it** in favour of a cleaner general replacement with a clear proof path. State what the replacement costs: strength, proof risk, and whether S1/S2 still satisfy it.
   - Judge the **assumption set as a whole**: is it cohesive, minimal and natural for our paper? Is it defensible by literature and/or simulation realism?

## Rules
- Read-only. Write ONLY `council/SENIOR_<SEAT>.md`, where SEAT = FABLE or ASTRA, at most 200 lines. Never delete files. Do not commit. Do not spawn subagents.
- Scratch only under `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/`: never /tmp, never outside the worktree. Never read or write under `/home/fb31/Bayesian-Variable-Selection/_local/engineering/`. No cluster jobs.
- For any Python or R, set `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` and run under `nice -n 10`.
- No stylistic nitpicks. Each finding must be substantive: missing, wrong, too narrow, or unnatural.

## Output (`council/SENIOR_<SEAT>.md`)
1. **Completeness findings.** For each: ID (C-1, …), location, what is missing, why it matters, and a proposed fix. Severity: BLOCKER, SUBSTANTIVE or MINOR.
2. **Generality/naturalness table**, one row per assumption: natural as stated? (yes / needs re-expression / replace); the S1/S2-specific or artificial element, if any; your proposed general statement (exact wording where you can); the cost of the change.
3. **Assumption set as a whole:** cohesion and redundancy, the SL benchmark comparison, and what a referee would object to first.
4. **Top 5 changes**, ranked by priority.
5. Scores 0–10: completeness, generality/naturalness, and overall readiness for the owner's assumption-by-assumption Q&A.

Then reply with a summary of at most 12 lines.
