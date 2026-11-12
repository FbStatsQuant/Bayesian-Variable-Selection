# BRIEF K1 — lemma line check (blind first read), seat: Sol (codex gpt-6.1-sol, reasoningEffort high)

You are an independent line-by-line checker of two proof files. Your job is to find errors and gaps: check every
step, every cited input (open the cited file and lines), every constant and threshold. Do not praise.
Repository root = your working directory. Read-only except the one output file. No git changes. No subagents.
Do not read any file under a `reviews/` folder (except this brief), nor LOG/PLAN/CHECKPOINT/REPORT files, nor
`Theory_work/Wave3/API_AUDIT/`.

## Proofs to check
- `Theory_work/Wave3/W3-MISR/lemmas/R_reduction.md` — Lemma R′ (a), (a′), (a″), (b), (c) and the translation table R.6.
- `Theory_work/Wave3/W3-MISR/lemmas/M_misr.md` — Theorem MIS-R (i) with its consequences and the stability clause,
  (i′) (a)–(d), (ii) (a)–(c).
against the statement `Theory_work/Wave3/W3-MISR/STATEMENT.md` (v1.2) §0–§4.

## Inputs you may (and should) open
- `Theory_work/Wave3/W3-POST/STATEMENT.md`; `Theory_work/Wave3/W3-POST2/STATEMENT.md`;
  `Theory_work/Wave3/W3-POST2/lemmas/{A_occam,C_expectation,D_hellinger,E_visibility}.md`.
- `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md` ([T03R]) and
  `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex` ([P3]),
  `…/T01_T02_contrast_dimension/PROOF_v3.tex` ([P1]).
- Code: `Scripts/SMC_BVS/core/` (for R.3); `Theory_work/Wave3/W3-MISR/numerics/N0_code_invariance.R`, `N0_out.txt`.
The W3-POST2 claims (A1, C, D, E) are **declared hypotheses** of this ticket: do not re-audit their proofs for
correctness; do check that this ticket uses them exactly as they are stated or as their proof files literally give
(hypotheses, "at that n", thresholds, constants' dependence).

## Questions
1. R.1–R.2: is each identity right (C1 = 0, s_{y′} = |c|s_y, evenness of the two quadratic forms, the image map for
   the parameter posterior, why c > 0 there)? Are (R1)–(R3) correct, including the non-constancy of Uu?
2. R.3: does the table describe the code correctly, line by line? Is the "occurs nowhere else" claim true (search)?
3. R.4: is the equality in law argued completely (measurability of Φ, Ψ; the a.s. non-zero contrast vector; the
   identification of the unit-noise model with model G of W3-POST)? Is "the same for every law satisfying GR^c" proved?
4. R.5 (part (c)): is π a function of T = zzᵀ/‖z‖² as claimed (the formula for Q_S; positivity; measurability)? Is
   the total-variation inequality applied correctly? Is the example right? Is the restriction to the model-space
   posterior justified?
5. R.6: check every row against the cited source lines. Anything in the W3-POST2 hypotheses (regime R1, p ≥ 2, A ≥ 1,
   s₀ ≥ 1, s₀ ≤ K, "for all large n" vs "at that n") that is not covered by (SZ) and the class definitions?
6. M.1: does W3-POST2 Claim C, as stated (STATEMENT lines 85-94; C_expectation.md lines 8-15), give exactly the claim?
   Constants' dependence; the 𝒦^λ_n case; consequences (1a)–(2c) and item 3; the stability clause (is the indicator of
   {HPM ≠ S₀} a function of the posterior? what is assumed about ties?).
7. M.2: check inputs (I1)–(I6) against their sources: is each really a bound at a single n under exactly the named
   hypotheses, with a threshold depending only on the listed constants? Then check (a), (b), (c), (d) line by line:
   the set inclusions, the counting "at most 2^{s₀} − 1", the ranges of the sums (j ≤ min(m♯_n, p − s₀)), the use of
   (I5) per model under a coordinate margin, e^{ρ_n} ≤ 2, the arithmetic that turns each term into ≤ const·r_n, the
   claim that (a) uses only the first (OS) inequality, the inclusion {|S| ≥ s + j₀} ⊆ Ω∖𝒩 in (d), and (c)'s constant.
8. M.3: Borel measurability of g_n and of the classes; the freezing step; "δ_n = g_n(κ_n, W_n) a.s."; the event
   {κ_n ∈ 𝒦_n} ∈ 𝓕_n; (b) slices; (c) the limsup argument. Any hidden assumption (p random? U fixed? regular
   conditional laws?) not in the statement?
9. Does every clause of STATEMENT §1–§4 have a proof here, and does any proof prove less than, or something different
   from, the clause as stated?

## Output
Write `Theory_work/Wave3/W3-MISR/reviews/K1_RM_check_sol.md`: per item (R′(a), (a′), (a″), (b), (c), R.6, MIS(i),
(i′)(a), (b), (c), (d), (ii)(a), (b), (c)) a verdict VERIFIED / VERIFIED-WITH-AMENDMENTS / GAP / FALSE; findings
numbered and graded FATAL / MAJOR / MINOR / NIT with file:line evidence and the required change. Final message: the
per-item verdicts in one line and the counts per grade.
