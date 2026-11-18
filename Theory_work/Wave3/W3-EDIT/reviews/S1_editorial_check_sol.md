# S1 editorial-only diff check — Sol, high

Reviewed the regenerated `git diff 1478808 HEAD -- . ':(exclude)Theory_work/Wave3/W3-EDIT'`: 17 files, 30 hunks. It is byte-identical to `reviews/S1_diff.patch`. Checked all 29 ledger rows whose route is exactly `IN-PLACE`, their motivating findings, and the relevant source statements, code and stored numerical output. Report transcription corrections are classified as editorial where they reproduce an existing master statement without altering its hypotheses, conclusion or proof. No mathematical claim or proof is revised by this batch.

Paths in the table are relative to `Theory_work/`.

| ledger id | file:line | EDITORIAL / CHANGES-MATH / INCORRECT | one-line reason |
|---|---|---|---|
| C6-01 | Wave1C/C-MIS/STATEMENT.md:59 | EDITORIAL | The current T03♯ hypotheses and conclusion occupy SoP 04_theory.tex:780–788; only the citation moves. |
| C6-02 | Wave1C/C-MIS/STATEMENT.md:174 | EDITORIAL | The approximately two-million onset illustration is now at 04_theory.tex:817. |
| C6-03 | Wave1C/C-MIS/lemmas/L1_reduction.md:10 | EDITORIAL | 04_theory.tex:782–788 contains the cited cutoff, eigenvalue, signal and conclusion text. |
| C6-04 | Wave1C/C-MIS/lemmas/L1_reduction.md:16 | EDITORIAL | 04_theory.tex:782–785 contains the same hypotheses formerly cited at 776–779. |
| C6-05 | Wave1C/C-MIS/lemmas/L1_reduction.md:45 | EDITORIAL | Fixed s₀ ≥ 1 is explicitly at 04_theory.tex:781. |
| C6-06 | Wave1C/C-MIS/lemmas/L1_reduction.md:62 | EDITORIAL | The onset illustration is at 04_theory.tex:817; its non-universal reading is unchanged. |
| C6-07 | Wave1C/C-MIS/lemmas/L3_hpm.md:6 | EDITORIAL | The quoted T38-(0) status occurs verbatim at 04_theory.tex:469. |
| C6-08 | Wave1C/C-MIS/numerics/citecheck.py:20–25 | EDITORIAL | Its six updated ranges mirror the corrected citations; all 34 checks pass. |
| C6-09 | Wave1C/C-MIS/reviews/CITECHECK.txt:5–10 | EDITORIAL | The refreshed record exactly matches the checker's current stdout, including ALL OK. |
| C6-10 | Wave2/W2-FAC-X/reviews/citecheck.py:9 | EDITORIAL | The added Wave2 prefix resolves the existing FAC-A/FAC-B report citations without altering a proof. |
| C6-11 | Wave2/W2-FAC-X/reviews/CITECHECK.txt:1–18 | EDITORIAL | The generated portion exactly matches current stdout, ok=7 miss=0; the status-string appendix is unchanged. |
| E7-01 | State_of_Project/sections/02_method.tex:452 | EDITORIAL | Both v3_run.R versions use rowMeans(P), threshold at >0.5 and log-sum-exp minus log(R); the methodology quotation is untouched. |
| I3-E1 | Wave3/W3-PSHARP/REPORT.md:39 | EDITORIAL | Restores the feasible summation limit already present in STATEMENT.md:94 and B_sparsity.md:8. |
| I3-E2 | Wave3/W3-PSHARP/PLAN.md:28–29 | EDITORIAL | Correctly describes the delivered restricted-size odds, quadrature and transformed lower bound; matches Sol N2. |
| I3-E4 | Wave3/W3-PSHARP/REPORT.md:9 | EDITORIAL | Correctly distinguishes deterministic S/B from asymptotic A/C, as the source statements already do. |
| I3-E5 | Wave3/W3-PSHARP/REPORT.md:47 | EDITORIAL | Labels the existing p=s₀+1 possibility remark as an unproved heuristic, exactly as requested. |
| I3-E6 | Wave3/W3-PSHARP/REPORT.md:111 | EDITORIAL | Distinguishes the witness lower bound from the two-sided rate on Remark A3's two sequences, citing the parent upper bounds. |
| I3-E8 | Wave3/W3-PSHARP/REPORT.md:89 | EDITORIAL | The quoted maximum agrees with the rounded V2(i) output, a_orth_out.txt:17–19 (maximum 3.5e−13). |
| I3-E9 | Wave3/W3-PSHARP/REPORT.md:8,74,175 | EDITORIAL | All four replacements point to the actual R2 council record at CHECKPOINT_3.md:3–9. |
| I4-F5 | Wave3/W3-MISR/numerics/N5_energy_obstruction.py:5 | EDITORIAL | The companion [P3] STATEMENT.md:21 gives 4C_*≈160.953<192 at s₀=2,A=1; the executable code is unchanged. |
| I4-S1 | Wave3/W3-MISR/ASSUMPTION_MAP.md:17,41,54; REPORT.md:76 | INCORRECT | The requested qualifications are inserted, but the edited row still ends with the categorical “weakenable, not removable”; see S1. |
| I4-S2 | Wave3/W3-MISR/numerics/N5_energy_obstruction.py:9–10 | EDITORIAL | Removes the false 200>c₁ comparison; c₁(2,1)≈258.905 and the controls remain explicitly unverified. |
| I4-X1 | Wave3/W3-MISR/ASSUMPTION_MAP.md:27 | EDITORIAL | The formula matches PSHARP Corollary A1:71–73 on its witness domain; its R2 checked status and the open T12 target are supported. |
| I5-E1 | Wave3/W3-START2/REPORT.md:23 | EDITORIAL | Copies the exact-order conditions η′=0 and κ_V>½ already stated in F2⁺, STATEMENT.md:115–117. |
| I5-E2 | Wave3/W3-START2/REPORT.md:89 | EDITORIAL | Distinguishes the leading contribution from full odds and cites the existing remainder conditions of P1.6(v):140–141. |
| I5-E6 | Wave3/W3-START2/REPORT.md:28 | EDITORIAL | Reproduces the fixed-c margin of STATEMENT.md:157–159 rather than an insufficient pointwise strict inequality. |
| I1-M17 | Wave2/W2-APP/lemmas/L4_families.md:144–145 | EDITORIAL | The cancellation example has zero conditional correlation for truth-free conditioning sets; the “no claim” classification is unchanged. |
| I1-M45 | Wave1/W1-N3/lemmas/LFP_floating_point.md:63 | EDITORIAL | Both example instances use cap=10⁶, equal to the default; the prose is correct, although the ledger's explanatory note is wrong (E1). |
| I1-M47 | Wave1/W1-PXN/lemmas/CR_corr_tails.md:46 | EDITORIAL | Adds a pointer to the already-existing strict-global-margin argument at R_branch_repair.md:20–26 and ERRATA E-17; no new proof argument is inserted. |

## Findings

**S1 — S (strength): incomplete assurance correction in I4-S1.** `Theory_work/Wave3/W3-MISR/ASSUMPTION_MAP.md:17` still concludes **“weakenable, not removable”**. This is an inherited phrase retained on the edited line, not a newly introduced theorem error. Nevertheless, it continues to present non-removability categorically after the same row has correctly qualified the evidence as finite-sample observations and an analytic sketch. The motivating Sol finding (`reviews/R2_council_sol.md:31`) explicitly disallows promoting that evidence to a checked asymptotic obstruction; `STATEMENT.md:260–264` also says it is not a checked proof. N5_out.txt:14–19 supports deterioration over the sampled n, not a proved limit. Thus the row does not fully implement the finding's assurance correction.

Exact fix: on ASSUMPTION_MAP.md:17 replace `— **weakenable, not removable**` with `— **numerical evidence compatible with weakening; non-removability suggested, not proved**`. This retains the intended evidence reading without changing any theorem. No source edit was made in this review.

**E1 — E (editorial record): inaccurate cap rationale in the ledger.** `Theory_work/Wave3/W3-EDIT/LEDGER.tsv:86` (row I1-M45; locate by id if the ledger shifts) ends its after-column rationale with `[fp_example.py sets no cap]`. In fact `Theory_work/Wave1/W1-N3/numerics/fp_example.py:10,22` explicitly supplies `10**6` to both `Inst` constructors. This equals the default in `numerics/n3lib.py:21`, so the actual edited lemma text is correct and no mathematical change is needed. Exact fix: replace that bracketed note with `[fp_example.py explicitly sets cap=10**6, equal to the default]`.

## Coverage and verification

Every IN-PLACE row has its corresponding edit, and every changed hunk is accounted for by an IN-PLACE row. No orphan edit or missing IN-PLACE edit was found. The non-IN-PLACE routes were not counted as requested edits. The applied text otherwise matches the ledger's after-columns and motivating findings, with the E1 rationale exception above.

Both citation scripts were inspected for side effects and rerun with Python bytecode writing disabled, capturing output in memory: C-MIS gives 34 OK / ALL OK; FAC-X gives ok=7 miss=0. Their generated records match byte for byte, and FAC-X's hand-appended status-string section is preserved. Checked the re-pointed SoP ranges directly; checked the pooling code in both cited versions; checked the numerical-plan truncation and transforms against a_orth.py and the quoted validation error against a_orth_out.txt; checked the N5 constants against the pinned [P3] companion statement and POST2's c₁ formula. The PSHARP:A status is PROVED-CHECKED / council R2 in `Theory_work/INFRA/registry/claims.tsv:409`; the every-p expectation extension is a named open T12 item in HQ_NOW.md. `git diff --check` reports no whitespace errors.

The verdict fails solely for the remaining S1 assurance overclaim. The count `incorrect=1` denotes the incomplete I4-S1 row; `changes_math=0` records that no mathematical claim or proof was changed. Only this reply file was written; no commit, push or git-state change was performed.

EDITORIAL-CHECK verdict=FAIL rows=29 changes_math=0 incorrect=1
