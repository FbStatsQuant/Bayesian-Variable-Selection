# Brief: Codex fidelity read of D2 "What we prove" (Writing Department, 2026-11-16)

You are an independent reviewer. Read one document, a section of a statistics paper that states consistency results, and
check it against its sources for **fidelity**. Report findings only; do not edit any file except your report.

## The document
- PDF: `Docs/Writing/results/what_we_prove.pdf`; LaTeX: `Docs/Writing/results/sections/*.tex` (macros in
  `Docs/Writing/shared/smcbvs.sty`). Paths are relative to the worktree root `/home/fb31/BVS-wt/WRITING`.
- Scratch files go in `/home/fb31/BVS-wt/WRITING/.rc_tmp/` only. Do not set TMPDIR. Do not write anywhere else.

## Sources (the document may not go beyond them)
1. Reader versions of the theorems: `/tmp/claude-71711/-home-fb31-BVS-wt-WRITING/8e3086be-1ddb-4604-89b5-5313e2023f22/scratchpad/src/READER_VERSIONS.md`
   (= `git show origin/theory/W3-READER:Theory_work/Wave3/W3-READER/READER_VERSIONS.md`, commit 7eb818e6). Theorem k of that file
   maps to D2 as follows: 1 → Thm 3.1; 1′ → Thm 3.4; 2 → Thm 3.9; 3 → Thm 3.13; 4 → Thm 3.18 (check); 9 → Thm 4.2 + Prop 4.3;
   9B → Thm 4.6; 9C → Cor 4.7; 5 → Thm 5.2; 6 → Thm 5.7; 7 → Thm 5.12; 8 → Thm 5.16; 8′ → Thm 5.17; 10 → Thm 5.19.
   (Check the numbers in the PDF; they may have moved by one or two.)
2. Headline card: `.../scratchpad/src/CLAIMS_CARD.md` (same commit).
3. Registry: `Theory_work/INFRA/registry/claims.tsv` (on this worktree, = main f8a6c2da), column `status`.
4. Status ledger and HQ rulings: `Docs/Writing/results/STATUS_LEDGER.md` (section "Flags for HQ — answered").
5. Song & Liang (2015), the published paper:
   `/home/fb31/Bayesian-Variable-Selection/Papers/Core_bibliography/32_2015_Song_Liang_A_split_and_merge_Bayesian_variable_selection_approach_for_ultrahigh_dimensional_regression.pdf`
   (journal page = PDF page + 946). An earlier check of the card's Song–Liang lines is
   `git show origin/theory/W3-READER:Theory_work/Wave3/W3-READER/reviews/SL_PDF_CHECK_card.md`.
6. Code-fact claims in §2 (data, prior, posterior, the method's objects) are checked against
   `Scripts/SMC_BVS/core/` (pins in `.../scratchpad/src/CODE_FACTS.md`).

## What was changed on purpose (do not report these as drift, but do report if one changes meaning)
- **Labels and order.** Assumptions are relabelled: global named ones such as (GL), (DIM), (SP), (BC), (EF), (NC),
  (BM), (GR), (FS$_\beta$), (FS$_\theta$), (EF$_\Sigma$), (V), (NL); conventions (C1)–(C3) for the reader versions'
  (S3)–(S5); and numbered local Assumptions with items. Statements are reordered into lead-in, in words, assumptions,
  theorem, status, remarks.
- **Symbols renamed** (presentation only): working coefficients $\theta_S$; prior normaliser $\bar w_K$; $\mathrm{SS}_S$
  for $Q_S$; constants $C_1$, $C_2$, $C_3$, $c_\star$, $c_{\mathrm{id}}$, $c_{\mathcal C}$, $M_{\mathcal C}$, $M_\mu$,
  $M_\theta$, $M_1$, $\underline\theta$, $\varphi_{\mathrm b}$, $C_L$, $\kappa_H$, $b_H$ (for $\rho$), $\omega_n$ (for
  $M_n$), $d_n$ (for $\nu_n$), $\delta_Q$, $k_n$ (the screening budget $q_n$); $\mathcal H_l$; $\mathcal D_n$; $\zeta_j$
  (for $z_j$); $\varrho$ for correlations in examples.
- **Status notes** are plain-words labels of the registry strings, following HQ's rulings H1–H4 in the ledger.
- **Song–Liang text.** Card row 1.1 was rewritten as full sentences (Remark "Comparison with Song and Liang" after
  Thm 3.4). HQ allows this only with **exactly the same claims**. Rows 1.2, 1.4 and 3.1 and the Theorem 9 comparison are
  near-verbatim, with only cross-references renumbered.

## What to check
- **A. Statements.** For every theorem, proposition, corollary and remark: are the hypotheses and conclusions the same as
  in the reader version? Report any added, dropped, strengthened or weakened hypothesis or conclusion, any changed
  quantifier or constant dependence, and any sentence that claims more than the source.
- **B. Statuses.** Each shaded status note against `claims.tsv` and the HQ rulings. Report any note that claims more
  than its registry status: a condition not carried, "checked" where the registry says less, or a reader-form bridge
  not marked as pending.
- **C. Song–Liang.** Each sentence that mentions Song and Liang (Remarks after Thms 3.4, 3.9, 3.17, 5.7; §4.5; Table 2)
  against (i) the card line or reader-version text it comes from and (ii) the PDF (theorem, condition, equation and
  page numbers). Report any new comparison, and any claim made stronger or weaker.
- **D. Numbers.** Every number (certification counts, 2,400 / 2,394 / 376 / 71 / 61 of 122 / …, $n\gtrsim1{,}450$,
  $2.1\times10^9$, $4.3\times10^9$, $2^{10^6}$, island spreads 0.09 / 0.76–1.15 / 79% / $5\times10^{-4}$, 24/24 and 10/10)
  against the card and the reader versions.
- **E. Setup.** §2's description of the data, the prior, the posterior and the method's objects against the code facts.

## Report
Write `Docs/Writing/reviews/D2_codex_fidelity.md`: a findings table (id, location, what the document says, what the
source says with file:line, severity C = changes a claim / S = scope or status / F = wording that could mislead /
E = editorial), then one line: `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL`. Findings only, no rewrite.
Effort high.
