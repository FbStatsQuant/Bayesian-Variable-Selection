# COUNCIL BRIEF — round 2 (TH-SONG-ASSUMPTIONS)

You are one seat of a three-seat review council (Opus, Neon, Sol); the seats work independently. Effort: high.
Mission: the Theory Department has defined target theorems for the SMC-BVS v3.1.1 posterior, mapped one-to-one to Song &
Liang (2015, JRSS-B 77(5)), and conjectured assumptions for them. **No proofs are claimed.** Your job is to judge whether
each assumption is (1) **defensible** — exact verified citation and/or S1/S2 simulation evidence, and an honest statement
of what is and is not supported — and (2) **relevant/sufficient** — the proof-path sketch plausibly uses it, it is not
stronger than needed (anti-stringency), and with the other assumptions it plausibly suffices for the target.

## Round 2 specifics
- The package is now **v1.2** (commit named in your dispatch message). It revises v1.1 after round 1.
- Read first: `COUNCIL_RECORD.md` (the Round 1 triage: every blocker, substantive point and nitpick with its disposition),
  then your own seat's round-1 review `council/R1_<SEAT>.md`. You may read the other seats' R1 files too.
- New evidence: `SIMULATION_DATA_ANALYSIS.md` §E9 (conditional-width Monte Carlo), `scripts/e9_width_mc.py`,
  `tables/e9_width_s1.tsv`. You may re-run or extend it if useful (single thread: `export OMP_NUM_THREADS=1
  OPENBLAS_NUM_THREADS=1`, run under `nice -n 10`, ≤ 10 CPU-min, output only under `.rc_tmp/`).
- Your tasks: (a) for each R1 blocker (B-1 … B-5 in COUNCIL_RECORD), say **resolved / not resolved** with a reason;
  (b) re-score every assumption on D and R; (c) list any new or remaining SUBSTANTIVE/BLOCKER points, including any error
  introduced by the revision; (d) nitpicks separately. Declined nitpicks carry a one-line reason in COUNCIL_RECORD; do not
  re-raise them as substantive unless you think the classification is wrong (then say why).
- A-DIM′ and A-BS′ are evaluated weaker alternatives (a labelled high-risk conjecture and a "recorded, not adopted" form).
  Score them as such: R measures whether their stated status and the reasons for it are correct, not whether they are
  already proved.

## Rules
- Read-only review. Write ONLY your review file (path below). Do not edit any other file; do not delete files; do not
  commit; do not spawn subagents. Scratch only under `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/` (never /tmp, never outside
  the worktree). Do not read or write under `/home/fb31/Bayesian-Variable-Selection/_local/engineering/`.
- Package (folder `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/song_assumptions/`): `THEOREM_DEFINITIONS.md`,
  `ASSUMPTIONS_AND_PROOF_PATHS.md`, `SIMULATION_DATA_ANALYSIS.md`, `OWNER_DEFENSIBILITY_DOSSIER.md`. Background you may
  consult: `advisors/ASTRA_R1.md`, `advisors/FABLE_R1.md`, `advisors/ASTRA_R2.md` (if present), `PRECEDENTS_NEW.md`
  (read its "Task Lead errata" first), `../writing_answers/PRECEDENTS_2026-11-17.md`, `council/S1_SL_CITATION_CHECK.md`,
  `tables/`. Song & Liang text: `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/song/papers/32.txt` (main) and `32b.txt`
  (supplement); rendered pages in `.rc_tmp/song/papers/img/`; PDFs alongside. Manuscript sections (our delivered
  statements): `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/song/ms/*.tex`.
- Spot-check at least 5 citations against the paper texts/PDFs in `.rc_tmp/song/papers/` and at least 5 numbers against
  `tables/`.

## What to score
For EACH assumption — A-GL, A-SPARSE, A-DIM, A-DIM′ (conjecture), A-SUBG, A-NEC, A-BS/A-BS′, A-MARGIN-H, A-MARGIN-U,
A-MIS(iii), A-MOM — give two scores 0–10:
- **D (defensibility)**: citations exact and correctly characterised; evidence correctly reported; limitations admitted.
- **R (relevance/sufficiency)**: used where claimed in the proof path; not stronger than needed; with the others,
  plausibly sufficient for the stated target (TD, TD′, TD-as, TS-a, TS-b + converse, TM-a0, TM-a, TM-b; MARGIN\* is now an open refinement, not a target).
Also give one overall score for the package (0–10) and say whether the 1-to-1 SL map (THEOREM_DEFINITIONS §2–§3) is
complete and correct.

## Classify every criticism
- **SUBSTANTIVE** — a wrong statement, a mis-cited or mischaracterised source, an assumption that is insufficient for its
  target or provably stronger than needed, a proof-path step that fails, a number that disagrees with the tables, an
  over-claim of status. Give the exact location and a concrete fix.
- **BLOCKER** — a substantive flaw that makes the package not deliverable until fixed.
- **NITPICK** — wording, formatting, ordering, style, optional extra content, extra examples. Nitpicks must NOT lower
  scores; list them separately.

## Output
Write `council/R2_<SEAT>.md` (SEAT = OPUS, NEON or SOL; ≤ 250 lines) with: (1) score table (assumption × D, R, one-line
reason); (2) overall score; (3) blocker-resolution table for B-1 … B-5, then the new/remaining SUBSTANTIVE/BLOCKER list, numbered, each with location + fix; (4) NITPICK list; (5) the
citations and numbers you spot-checked and the result. Then reply with a ≤ 15-line summary (scores, blocker status, any new blockers).
