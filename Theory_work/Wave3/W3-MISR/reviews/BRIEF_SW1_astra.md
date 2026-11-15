# BRIEF SW1 — exhaustive sweep (blind first read), seat: Astra (codex gpt-6-astra, reasoningEffort high)

You are an independent sweep reviewer of a finished proof package. An exhaustive sweep reads **every line** of the
package once, looking for any defect of any size: a wrong or unjustified step, a statement that the proof does not
prove (or proves differently), an undefined or inconsistently used symbol, a wrong citation or line reference, a
constant or threshold whose dependence is misstated, a number in the text that does not match the numerical outputs,
an overclaim, a missing non-claim, an inconsistency between files. Do not praise. Be token-efficient: targeted reads.
Repository root = your working directory. Read-only except the one output file. No git state changes. No subagents.
Do **not** read: any file under a `reviews/` folder (of this or any ticket) other than this brief and
`Theory_work/Wave3/W3-MISR/reviews/CITECHECK.txt`; any `LOG.md`, `PLAN.md`, `CHECKPOINT_*.md`; anything under
`Theory_work/Wave3/API_AUDIT/`.

The content is frozen as `MANIFEST d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d` (the package
files are unchanged since commit 2f360ed; `git diff --stat 2f360ed -- Theory_work/Wave3/W3-MISR ':!Theory_work/Wave3/W3-MISR/reviews' ':!Theory_work/Wave3/W3-MISR/LOG.md' ':!Theory_work/Wave3/W3-MISR/CHECKPOINT_*.md'`
must print nothing — run it, read-only, and quote the digest in your review).

## Package (sweep all of it)
`Theory_work/Wave3/W3-MISR/`: `STATEMENT.md` (v1.2), `lemmas/R_reduction.md`, `lemmas/M_misr.md`,
`lemmas/G_corollaries.md`, `ASSUMPTION_MAP.md`, `REPORT.md` (§1, §3–§7 only: do not read its §2 "Review trail"),
`numerics/` (scripts and outputs), `citecheck.py`.

## Sources (open what a line cites)
`Theory_work/Wave3/W3-POST/STATEMENT.md`; `Theory_work/Wave3/W3-POST2/STATEMENT.md` and
`Theory_work/Wave3/W3-POST2/lemmas/{A_occam,B_tail_approx,C_expectation,D_hellinger,E_visibility}.md` (these W3-POST2
claims are declared hypotheses of the ticket: check that they are used as stated, do not re-audit them);
`Theory_work/Wave1C/C-MIS/STATEMENT.md`, `Theory_work/Wave1C/C-MIS/lemmas/{L1_reduction,L2_gaussian,L4_theoremF,L5_frontier,L6_null}.md`;
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md` and
`…/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/{T03_A2_selection_consistency/PROOF_v2.tex,T01_T02_contrast_dimension/PROOF_v3.tex}`;
code `Scripts/SMC_BVS/core/{v3_preprocess.R,v3_fit.R,v3_setup.R,cpp/v3_score.h,cpp/v3_core.cpp}`.

## Sweep checklist (go through each; report everything you find)
1. Statement ↔ proof: every clause of STATEMENT §1–§7 has a proof that proves exactly that clause.
2. Every step of the three lemma files (algebra, set inclusions, counting, expectations on events, measurability,
   the conditioning argument, the scaling maps, the Theorem F table, the counterexample).
3. Every citation `file:line` / "[X] lines a-b": does the cited place say what is claimed?
4. Notation and definitions: each symbol defined once and used consistently across the four main files.
5. Constants and thresholds: what each depends on; every "for n ≥ …"; every numerical constant.
6. Numerics: every number quoted in STATEMENT, ASSUMPTION_MAP, REPORT against the output files; every description
   of what a script does against the script.
7. Statuses: each "conditional on …" complete for what the proof uses; inherited statuses quoted as they are.
8. Claims about the literature and about version 1 (C-MIS); the "Not claimed" list; the registry blocks of REPORT §7
   (line ranges, ids, dependencies) against the files.
9. Anything substantive: a clause that is false, unproved, vacuous, or weaker/stronger than it reads.

## Output
Write `Theory_work/Wave3/W3-MISR/reviews/SW1_sweep_astra.md`: the digest you reviewed; findings numbered and graded
FATAL / MAJOR / MINOR / NIT, each with file:line evidence and the exact fix; for each finding say whether fixing it
is **editorial** (wording, bookkeeping, a description) or **substantive** (changes a statement, a proof step, a
premise or a code pin). End with one line `SWEEP-VERDICT: CLEAN | EDITORIAL-ONLY | SUBSTANTIVE` and the counts per
grade. Final chat message: that line and the counts.
