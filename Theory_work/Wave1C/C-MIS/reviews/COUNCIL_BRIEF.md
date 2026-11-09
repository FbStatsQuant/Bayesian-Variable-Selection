# C-MIS — council brief (round 1)

You are one of two independent council seats for ticket C-MIS (Theory Wave 1C). Score the finished proof package; you are
briefed to **break** it, not to confirm it. Repo root: `C:\Users\felip\Bayesian-Variable-Selection`. Read-only except your
single output file; no git commands.

**Package (read all):** `Theory_work/Wave1C/C-MIS/STATEMENT.md` (target, v1.1 locked + logged edits);
`Theory_work/Wave1C/C-MIS/lemmas/00_MAIN.md` (proof map, hypothesis-to-step table), `L1_reduction.md`, `L2_gaussian.md`,
`L3_hpm.md`, `L4_theoremF.md`, `L5_frontier.md`, `L6_null.md`; `numerics/SUMMARY.md` (falsification evidence only, never a
proof); `reviews/CITECHECK.txt` (citation check output).

**Sources to check against:** `Theory_work/State_of_Project/sections/04_theory.tex` (TH09 card ~761–822; M5 card ~464–540),
`02_method.tex:84-135`; T03♯ proof `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/A-REV5/sources/W1-T03R/PROOF.md`;
`Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex`; `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`;
`Docs/Theory/theorems/00_COMMON.md`; T38 part (0) `.../A-REV5/sources/W4-T38FULL/T38_PROOF.md:34-46`; Theorem GEN
`Theory_work/Wave1/W1-GEN/` (STATEMENT.md, REPORT.md, lemmas/L5_assembly.md, lemmas/L6_instances.md); Song & Liang (2015)
PDF `C:\Users\felip\.t3\userdata\attachments\647bfd65-83bc-403a-b3b0-0a8352044e7f-588fe83a-5cbe-4a20-8055-1cfbd7c9c936-pdf.pdf` §2.3 (p. 957).

**Context.** The project wants Song–Liang (2015) Theorem 4 / Corollary 2 analogs (misspecified candidate sets) for SMC-BVS's
exact posterior, p ≤ n^A, fixed sparsity. Do not read this ticket's LOG.md or other reviews; judge the package as it stands.

**Gates (each PASS / FAIL with reasons):**
1. Correctness of every step (reduction, de-randomisation, Gaussian conditioning, every changed step of the T03♯ re-run,
   Lemma T, Lemma Z, corollaries, examples).
2. Hypotheses used = hypotheses stated (incl. the candidate-only rerun, fixed σ_𝒞², s₀^𝒞 ≥ 1, envelopes, GEN premises).
3. No hidden assumptions.
4. Cited lemmas have adequate status (statuses copied verbatim, nothing upgraded; inputs' own premises carried).
5. Constants / rates / thresholds tracked (δ_n^𝒞, E_n^𝒞, c₀ unchanged, m^T_n, O_P rates, no expectation rate inferred).
6. Fidelity to the method as coded (shipped score, IG(0.01, 0.01) with response-dependent rate, BB(1, p_𝒞) weights, cap K,
   candidate standardisation, reported HPM over the scored set).
Also judge: no overclaim relative to Song–Liang; frontier honestly stated.

**Output:** gate verdicts, numbered findings (fatal / major / minor) with file:line and exact fix, and an **uncapped 0–10
score**. Pass = both seats ≥ 8.0 with all gates PASS.
