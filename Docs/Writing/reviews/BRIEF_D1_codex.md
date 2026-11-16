# Brief: Codex fidelity read of D1 "The SMC-BVS method, as coded" (Writing Department, 2026-11-16)

You are an independent reviewer. Read one document, the methodology section of a statistics paper, and check it against
the shipped code and its sources for **fidelity**. Report findings only; do not edit any file except your report.
Paths are relative to the worktree root `/home/fb31/BVS-wt/WRITING`. Scratch goes in `.rc_tmp/` only. Do not set TMPDIR.

## The document
`Docs/Writing/methodology/smc_bvs_method.pdf` (LaTeX: `smc_bvs_method.tex`; macros `Docs/Writing/shared/smcbvs.sty`).

## Authorities, in order
1. **The code:** `Scripts/SMC_BVS/core/` (R: `v3_*.R`; C++: `cpp/*.h`, `cpp/v3_core.cpp`). The code wins over every
   other source. In the parameter table (Section 6), code locations are relative to this folder.
2. Code facts with pins: `.rc_tmp/d1_sources/CODE_FACTS.md` (a map; verify in the code).
3. Example 4.1 and Figure 2: `.rc_tmp/d1_sources/METHOD_INTUITION.md` and the computation behind them,
   `.rc_tmp/d1_sources/toy_example.py` and `toy_example_out.txt`.
4. Appendix A (the 10⁶ engine): `.rc_tmp/d1_sources/ENGINEERING_SPEC.md` §0-v2.2 (a draft spec; the appendix must present
   it as a different engine, not the method).
5. Appendix D (source–code disagreements): `Theory_work/State_of_Project/sections/02_method.tex`,
   `Docs/Methodology/METHODOLOGY_v3.md`, `Scripts/SMC_BVS/core/README.md`.
6. Cross-references to the companion part ("Theory" column; Remark 5.22; conventions (C1)–(C3)):
   `Docs/Writing/results/what_we_prove.pdf`. Check that each cited theorem or convention really uses the parameter.

## Already done (do not redo; report only if something is still wrong)
An Opus clarity read (`Docs/Writing/advisor/CLARITY_D1_opus.md`, disposition `CLARITY_D1_disposition.md`) and an Opus code check (`Docs/Writing/reviews/D1_code_check_opus.md`, disposition `D1_code_check_disposition.md`) has
checked every table row and procedural statement, and its findings are applied.

## Specified after a clarity read (new content; check each against the code)
- The grid rule, which refines the pilot temperatures (`cpp/v3_calib.h:60-98`), and the rebuild and convergence rules (`v3_calib.R:44-130`).
- The calibration control flow in Algorithm 1: a failed step 3 skips the rebuild loop; tier-1 triggers are only recorded; an unconverged grid is used as it is; the fallback; "a grid always exists" with the fallback on.
- The three stores and "the best model found so far" (`cpp/v3_ledger.h:66-80`).
- The block partition (`cpp/v3_blocks.h:110-141`).
- The exact sampler's backward split (`cpp/v3_start.h:136-176`).
- The non-negative form of SS_S (`cpp/v3_score.h:145-160`).
- The lists of outputs and stops in Section 5.7, including the exact case.

## What to check
- **A. Formulas.** Every formula in Sections 1–5 against the code: the prior, the marginal likelihood and $C_n$, the log
  score, the start law and its recursion, the discrepancy and the identity after (11), the path (12), the four moves and
  their acceptance probabilities, the island's evidence estimate, $\rho_V$, the pooled estimates.
- **B. Procedure.** Algorithm 1 and Sections 5.1–5.7: every procedural statement, including the new paragraph "The check
  before the run" (its formula and the threshold arithmetic at $n=200$, $p=10^4$), the trigger timing, the move-cap
  semantics, what a stop returns, and the diagnostics list.
- **C. Table.** Each row of Table 1: value; pin; code name; example value at $n=200$, $p=10^4$ (recompute); and whether the
  Theory entry is right.
- **D. Numbers.** Every number in Example 4.1, Figure 2 (the weights are ratios of the two rows of the example's table) and
  the text, against the sources above.
- **E. Appendices.** Appendix A against the spec; Appendix D, each item against its cited lines.
- **F. Overclaims.** Any sentence that claims more than the code or the sources support, or that a theorem says something
  it does not.

## Report
Write `Docs/Writing/reviews/D1_codex_fidelity.md`: a findings table with columns id, location, what the document says,
what the code or source says (file:line), and severity (C = wrong fact, S = misleading scope or omission, F = wording that
could mislead, E = editorial). End with one line: `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL`. Findings only. Effort
high.
