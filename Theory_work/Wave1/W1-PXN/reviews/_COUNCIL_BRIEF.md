# Council brief (W1-PXN) — read fully

You are one of two independent council reviewers for theory ticket W1-PXN, repo C:\Users\felip\Bayesian-Variable-Selection.
Read-only except for your ONE output file. No git state changes. No subagents. Do NOT read Theory_work/Wave1/W1-PXN/reviews/
(other than this brief), LOG.md or PLAN.md: judge independently from the mathematics and the sources.

## Material
- Theorem (locked): Theory_work/Wave1/W1-PXN/STATEMENT.md (§2 = the theorem; §5 = post-review changes, which take precedence).
- Definitive proof map: Theory_work/Wave1/W1-PXN/FINAL_PROOF.md (says which text proves each step, in which order, on which events).
- Candidate proof text it cites: Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md, as amended by
  Theory_work/Wave1/W1-PXN/lemmas/ERRATA.md (E-1..E-22).
- Replacement lemma files: Theory_work/Wave1/W1-PXN/lemmas/{CR_corr_tails, P8_T03sharp, L_strict_localmax, LS_P6_repair,
  R_branch_repair, B_ii_domain}.md; assessment only: lemmas/I8_lean_readiness.md.
- Numerical falsification evidence (diagnostic only): Theory_work/Wave1/W1-PXN/numerics/SUMMARY.md and numerics/n8/SUMMARY.md.
- Sources for dependencies: T22 deterministic aggregation (…/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md);
  T03-sharp (…/branch_snapshots/W6-FIXREV2/STATEMENTS.md:19-60); W7-PART (…/branch_snapshots/W7-PART/PROOF.md §§0-3);
  operational premises (…/branch_snapshots/W6-FIXREV1/T38_STATEMENT.md:28-80); Lemma RO (…/branch_snapshots/W2-BOOK/PROOF.md:75-95);
  registry statuses Theory_work/Old_Projects/New_BVS_Headquarters/ID_REGISTRY.md (rows TH116, TH123, T03-sharp, TH148, TH162, TH163);
  method: Docs/Methodology/METHODOLOGY_v3.md §§3, 6.10 and Scripts/SMC_BVS/core/ (cpp/v3_blocks.h, v3_start.h, v3_engine.h, v3_core.cpp, v3_preprocess.R).
  (… = Theory_work/Old_Projects/New_BVS_Headquarters)

## What to judge
Whether the theorem of STATEMENT.md §2 — in particular the headline (P) + (C): on LH-iid with SIZE, p ≤ n^A for any fixed
A ≥ 1 (A > 1 allowed), v3 + LS0 under the operational premises, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 — is proved by the material, at a
standard you would accept for a refereed statistics paper's supplement.

## Gates (each PASS / FAIL with one-line reason)
G1 correctness of every step; G2 hypotheses used = hypotheses stated; G3 no hidden assumptions; G4 cited lemmas have adequate
status (say which status you rely on for each); G5 constants/rates tracked (incl. dependence on A); G6 fidelity to the method
as coded (what is and is not claimed about the production code).

## Output (write to the file named in your task; return the same content as your final message)
First lines: "GATES: G1 …, G2 …, G3 …, G4 …, G5 …, G6 …" and "SCORE: x.x / 10" (uncapped, one decimal). Then numbered issues,
each with severity (BLOCKING / MAJOR / MINOR), path:line evidence and the fix you require. Then a one-paragraph overall reading.
Pass requires all gates PASS and score ≥ 8.0; be calibrated, not generous.
