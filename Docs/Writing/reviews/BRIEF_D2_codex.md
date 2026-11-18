# Brief: Codex fidelity read of D2 "What we prove" (Writing Department, 2026-11-16)

You are an independent reviewer. Read one document, a section of a statistics paper that states consistency results, and
check it against its sources for **fidelity**. Report findings only; do not edit any file except your report.

## The document
- PDF: `Docs/Writing/results/what_we_prove.pdf`; LaTeX: `Docs/Writing/results/sections/*.tex` (macros in
  `Docs/Writing/shared/smcbvs.sty`). Paths are relative to the worktree root `/home/fb31/BVS-wt/WRITING`.
- Scratch files go in `/home/fb31/BVS-wt/WRITING/.rc_tmp/` only. Do not set TMPDIR. Do not write anywhere else.

## Sources (the document may not go beyond them)
1. Reader versions of the theorems: `.rc_tmp/d2_sources/READER_VERSIONS.md`
   (= `git show origin/theory/W3-READER:Theory_work/Wave3/W3-READER/READER_VERSIONS.md`, commit 7eb818e6). Theorem k of that file
   maps to D2 as follows: 1 → Thm 3.1; 1′ → Thm 3.4; 2 → Thm 3.9; 3 → Thm 3.13; 4 → Thm 3.18; 9 → Thm 4.2 + Prop 4.3;
   9B → Thm 4.6; 9C → Cor 4.7; 5 → Thm 5.2; 6 → Thm 5.7; 7 → Thm 5.12; 8 → Thm 5.16; 8′ → Thm 5.17; 10 → Thm 5.19; row 2.2 → Remark 4.9; row 3.5 → Remark 5.22.
   The status ledger is Appendix D of the PDF (Appendix C is "Explicit constants").
2. Headline card: `.rc_tmp/d2_sources/CLAIMS_CARD.md` (same commit).
3. Registry: `Theory_work/INFRA/registry/claims.tsv` (on this worktree, = main f8a6c2da), column `status`.
4. Status ledger and HQ rulings: `Docs/Writing/results/STATUS_LEDGER.md` (section "Flags for HQ — answered").
5. Song & Liang (2015), the published paper:
   `.rc_tmp/d2_sources/SongLiang2015.pdf` (journal page = PDF page + 946; read it with `pdftotext -layout`). An earlier
   check of the card's Song–Liang lines is `.rc_tmp/d2_sources/SL_PDF_CHECK_card.md`.
6. Code-fact claims in §2 (data, prior, posterior, the method's objects) are checked against
   `Scripts/SMC_BVS/core/` (pins in `.rc_tmp/d2_sources/CODE_FACTS.md`).

## What was changed on purpose (do not report these as drift, but do report if one changes meaning)
- **Labels and order.** Assumptions are relabelled: global named ones such as (GL), (DIM), (SP), (BC), (EF), (NC),
  (BM), (GR), (FS$_\beta$), (FS$_\theta$), (EF$_\Sigma$), (V), (NL); conventions (C1)–(C3) for the reader versions'
  (S3)–(S5); and numbered local Assumptions with items. Statements are reordered into lead-in, in words, assumptions,
  theorem, status, remarks.
- **Symbols renamed** (presentation only): working coefficients $\theta_S$; prior normaliser $\bar w_K$; $\mathrm{SS}_S$
  for $Q_S$; constants $C_1$, $C_2$, $C_3$, $c_\star$, $c_{\mathrm{id}}$, $c_{\mathcal C}$, $M_{\mathcal C}$, $M_\mu$,
  $M_\theta$, $M_1$, $\underline\theta$, $\varphi_{\mathrm b}$, $C_L$, $\kappa_H$, $b_H$ (for $\rho$), $\omega_n$ (for
  $M_n$), $d_n$ (for $\nu_n$), $\delta_Q$, $k_n$ (the screening budget $q_n$); $\mathcal H_l$; $\mathcal D_n$; $\zeta_j$
  (for $z_j$); $\varrho$ for correlations in examples; $c_{\mathrm H}$ (for Theorem 9's $c$); $r^\circ_n$ (the locality
  rate in (NL), Theorem 5's $r_n$); $\mathcal E_{\mathrm{cal}}$ (Theorem 10's event $\mathcal A$); $s_{\mathcal C}$, $m_{\mathcal C}$,
  $\beta^*_{\mathcal C}$, $\beta^*_{\mathcal M}$ in Theorem 4 and its Example; $x^{(i)}$ for the $i$-th observation in §4;
  $C_H$ (for $C'_H$).
- **Status notes** are plain-words labels of the registry strings, following HQ's rulings H1–H4 in the ledger.
- **Song–Liang text.** Card row 1.1 was rewritten as full sentences (Remark "Comparison with Song and Liang" after
  Thm 3.4). HQ allows this only with **exactly the same claims**. Rows 1.2, 1.4 and 3.1 and the Theorem 9 comparison are
  near-verbatim, with only cross-references renumbered.

## Content added since the reader versions (check each against the cited source)
- §2.6 "The sampler" paragraph, the calibration success/fallback definition, valid inputs and seed, and "completed run"
  (sampler status only): against the code facts (`.rc_tmp/d2_sources/CODE_FACTS.md`) and Theorem 10's scope note.
- The sentence after Theorem 3.1 on the factor 4: the source is READER_VERSIONS bridge B1.5
  (`P(HPM≠S0) ≤ 2Eδ_n`, the same for the MPM).
- Remark 3.5(iii): $T\subseteq[p]\setminus S_0$ (source: `Theory_work/Wave3/W3-POST2/STATEMENT.md:30-33`); "(NC) implies it
  for all large n" (READER_VERSIONS bridge B1.7, `W3-POST2:A0`).
- The definition of the noiseless gain before Theorem 5.17 and its identity with $\mathrm{SS}^\mu$: source
  `Theory_work/Wave3/W3-SCR/STATEMENT.md:51-55` (check that their $Q_S$ is the $\mathrm{SS}_S$ of D2's (7)).
- "(EF$_\Sigma$) implies Assumption 5.1" before Theorem 5.19: READER_VERSIONS bridge B6.1.
- Remark 5.20(ii): $\rho_n/\sqrt{\log n/n}=e^{C_3\sqrt{\log n}}/\sqrt{\log n}$ (arithmetic).
- §1 "How the results depend on each other": each edge against the masters' "conditional on" lists and bridges.
- Appendix C: $c_1$ copied from `W3-POST2/STATEMENT.md:130` ($C_A$ at :22); $c_0$ from `W3-POST/STATEMENT.md:75`.
- Example 5.5 (visibility and leakage with three predictors): new arithmetic and inference; check both.

## What to check
- **A. Statements.** For every theorem, proposition, corollary and remark: are the hypotheses and conclusions the same as
  in the reader version? Report any added, dropped, strengthened or weakened hypothesis or conclusion, any changed
  quantifier or constant dependence, and any sentence that claims more than the source.
- **B. Statuses.** Each shaded status note against `claims.tsv` and the HQ rulings. Report any note that claims more
  than its registry status: a condition not carried, "checked" where the registry says less, or a reader-form bridge
  not marked as pending.
- **C. Song–Liang.** Each sentence that mentions Song and Liang (Remarks 3.8, 3.11, 3.22 and 5.10; §4.5; §1 and Table 2)
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
