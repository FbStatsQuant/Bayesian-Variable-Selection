# BRIEF K2 — lemma line check (blind first read), seat: Sol (codex gpt-6.1-sol, reasoningEffort high)

You are an independent line-by-line checker of one proof file. Your job is to find errors and gaps: check every step,
every cited input (open the cited file and lines), every constant and threshold. Do not praise.
Repository root = your working directory. Read-only except the one output file. No git changes. No subagents.
Do not read any file under a `reviews/` folder (except this brief and, for G.5's last paragraph only,
`Theory_work/Wave3/W3-MISR/reviews/L01_statement_lock_sol.md` finding 1, which the proof cites as the source of an
example), nor LOG/PLAN/CHECKPOINT/REPORT files, nor `Theory_work/Wave3/API_AUDIT/`.

## Proof to check
`Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md` — Corollary G(a), G(b), Corollary H (with the "reference law"
paragraph), Remarks SNR, P, U — against the statement `Theory_work/Wave3/W3-MISR/STATEMENT.md` (v1.2) §5–§7 (and §0–§4
for definitions). It uses Lemma R′ and Theorem MIS-R of `Theory_work/Wave3/W3-MISR/lemmas/R_reduction.md` and
`M_misr.md`; take those two files as given (another reviewer checks them), but tell us if G uses them for something
they do not state.

## Inputs you may (and should) open
- `Theory_work/Wave3/W3-POST/STATEMENT.md`; `Theory_work/Wave3/W3-POST2/STATEMENT.md`;
  `Theory_work/Wave3/W3-POST2/lemmas/{A_occam,B_tail_approx,C_expectation,D_hellinger,E_visibility}.md`.
- `Theory_work/Wave1C/C-MIS/STATEMENT.md`; `Theory_work/Wave1C/C-MIS/lemmas/{L1_reduction,L2_gaussian,L4_theoremF,L6_null}.md`.
- Older locked proofs under `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/` if a definition is needed.
The W3-POST2 and C-MIS claims are inputs: do not re-audit their proofs; do check that they are used exactly as stated
(hypotheses, regimes, constants' dependence, which quantities their conclusions are about).

## Questions
1. G.1: is the Gaussian-conditioning step valid at a single n with σ² ≥ 0 and n-dependent (m, Σ, β)? Is W_n really
   independent of σ(X^r_𝒞) with law N_N(0, I)? Is κ_n measurable; non-constant columns a.s.?
2. G.2: go through steps 1–5 against C-MIS `L2_gaussian.md` lines 88-105. Do the unchanged steps really not involve
   the response variance? Are the two changed steps right? Constants (φ₀² = c_pop/(8C₀), M = 2M₀ + 1, g₀ = 1, c_D = ½)?
   Is membership in 𝒦^λ_n complete (every defining condition, including s(κ_n) = s, (SZ), (F₀), (OS) with its onset)?
   Is P(𝒜_nᶜ) = O(1/n) and hence E δ_n = O(r_n)? Is the stated hypothesis list of STATEMENT §5(b) sufficient
   (anything used but not assumed: β^𝒞 ≠ 0, p_𝒞 ≥ s, k_n ≤ p_𝒞)?
3. G.3: is the transfer of W3-POST2 Claim D exact — the sets B_n, B̃_n and the bijection; the regime R1 for the
   unit-noise array; the constants C_H and 1 + C_H/4; the Hellinger invariance; D(a)'s hypothesis δ_n → 0 and its
   four-part bad set with the √(v_n/n) threshold and zero-padding? Is every sentence of the "reference law" paragraph
   correct (the variance of (Cy^r)_i; the KL statement and its restriction)?
4. G.4: for each listed claim (W3-POST Theorem 1 items 1–6; W3-POST2 A1, B, C, D, E), is its conclusion really a
   function of objects that are invariant / equivariant in the way used, and are its hypotheses mapped correctly
   (in particular Claim B's reference cost and the random-design clauses with a design-measurable variance)?
5. G.5: check the three transfers (C-MIS Theorem MIS (i); (ii), (ii′); Theorem F with Corollaries F(a), F(b)) against
   C-MIS STATEMENT lines 52-78 and 122-146 and `L4_theoremF.md`: is the scaled problem a legitimate instance of the
   C-MIS model in each case (which of its objects are allowed to be zero or design-dependent)? Is every
   variance-dependent hypothesis in the table, and is each row right? Is the final example (unnormalised BM-∞ fails)
   proved — the total-variation step and the use of C-MIS Lemma Z?
6. G.6: is the uniqueness argument complete (same law, different classes, the maxima of constants)?
7. Does every clause of STATEMENT §5–§7 have a proof here, and does any proof prove less than, or something different
   from, the clause as stated? Is any status line at the top of the file wrong about what it is conditional on?

## Output
Write `Theory_work/Wave3/W3-MISR/reviews/K2_G_check_sol.md`: per item (Cor G(a), G(b), Cor H(a), H(b), reference law,
Remark SNR, Remark P: MIS(i) / MIS(ii),(ii′) / Theorem F / example, Remark U) a verdict VERIFIED /
VERIFIED-WITH-AMENDMENTS / GAP / FALSE; findings numbered and graded FATAL / MAJOR / MINOR / NIT with file:line
evidence and the required change. Final message: the per-item verdicts in one line and the counts per grade.
