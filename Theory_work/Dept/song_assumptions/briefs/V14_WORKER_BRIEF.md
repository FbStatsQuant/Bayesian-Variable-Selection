# Worker brief: v1.4 edits to OWNER_DEFENSIBILITY_DOSSIER.md and SIMULATION_DATA_ANALYSIS.md

Folder: `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/song_assumptions/`.

**Canonical source.** `council/V14_CHANGESPEC.md` holds the converged text and is the authority. Carry its statements **verbatim in substance**. Do not invent new mathematics. If the spec does not settle something, leave the current text and list it in your reply.

**Scope.** Edit ONLY the two files `OWNER_DEFENSIBILITY_DOSSIER.md` and `SIMULATION_DATA_ANALYSIS.md`. The Lead is editing `THEOREM_DEFINITIONS.md` and `ASSUMPTIONS_AND_PROOF_PATHS.md` in parallel, so do not touch those.

**Style.** Keep the existing structure and the house style:
- short numbered items;
- plain English;
- exact citations as already given;
- Unicode maths as in the files.

Prefer the Edit tool for targeted edits, and keep the files' lengths about the same. Set the header version to **v1.4 (senior review: completeness, generality and naturalness; see COUNCIL_RECORD.md and council/V14_CHANGESPEC.md)**.

## OWNER_DEFENSIBILITY_DOSSIER.md
1. **Score card (top table).** Change the A-MARGIN-U row to the population form, and the A-MARGIN-H row to the diverging ratio. Add rows for A-SPARSE-C and TM-a0-inc. Remove S1 numbers that describe the *assumption* itself; numbers in the "holds on our data" column may stay.
2. **New short section near the top: "Assumption blocks"**, giving the four blocks of spec §3.
3. **A-SUBG item 1 and A-NEC item 1.**
   - Windows: use the spec §2 wording, i.e. size ≤ k_n; for fixed level, every fixed c·log n; q_n(M_n) for varying M.
   - A-NEC: state it as n·φ_min(k_n) ≥ c_ψ, "may vanish but no faster than the ridge scale", with the 1 − n^{−2} example.
4. **A-NEC item 3 (Standard?).** Fix the R3 leftover:
   - Split NH14 and SBJ into separate bullets. NH14 expressly allows exact dependence via its nonzero convention, and its p_n^{−κ} floor can be below c_ψ/n at large p. SBJ (8) indexes its nonzero-eigenvalue quantity through min(n, |k|); do NOT say SBJ allows duplicates.
   - SL (26) has a vanishing lower threshold and a growing upper threshold, with Cor S1 choosing such a pair.
   - Add the SL Condition 3 Gaussian sufficient form (spec §3).
5. **A-BS item 3.** Add SL (3), p. 950, as A-BS's direct counterpart (spec §3). **A-BS′:** use the spec §2 wording (recorded pair; open target; the A-NEC energy bound).
6. **A-DIM item 5.** A-DIM′ is "log p = o(√n)" as the conjecture's regime, and the product form is the proof budget.
7. **A-MARGIN-H item 1.** Use the diverging ratio "for every fixed k", plus the fixed-level remark. Say that TS-a is per predictor first, then joint.
8. **A-MARGIN-U, the central section. Rewrite items 1, 2, 4, 5 and 6 to the population form of spec §1.**
   - Item 1 (Assumed): give (U1), (U2a), (U2b), ā, m̄_d, Q_n as an accounting device, and the three special cases. Plain-English first, then the exact form.
   - Item 2 (Why needed): explain Lemma W in plain words:
     - the leakage share controls how far the added nulls can move the residual direction;
     - per base, a simultaneous Gaussian bound;
     - the refined design-conditional form is a parallel sufficient condition, not implied.
   - Item 4 (Holds on our data?), using spec §1 "Evidence":
     - U2a min ratio = exact κ_n, 2.505–2.771 at SNR 2, checked over inside proxies;
     - the AR(1) leakage decay;
     - the fallback fails at SNR 2 and holds at SNR 3;
     - E9/E9b are diagnostics of the refined form only: selected D, four designs, zero slack. Exact minima: SNR 2 min 2.386 (C = 121, a sensitivity setting) and 2.489 (no credit).
   - Remove the "C ≈ 121 implied" claim (spec §2, credit constant).
   - **Remove** the line ~191 wording "On ordinary correlated designs" (R3 leftover). Say instead "on S1's AR(1) designs (estimated)" or move it to the evidence.
   - Item 5 (Weaker forms): the corollaries C-i and C-ii, and the weaker variant remark (proxies pay their own price).
   - Item 6 (Referees): add "How do I construct Q_n?", answered by "accounting device", and "Why this width?", answered by the leakage form and the worked cases.
9. **New section "Worked cases".** Place it after A-MARGIN-U. Give the four closed forms of spec §3 (orthogonal, AR(1), block, equicorrelation / one factor), each with its conditioning set, plus the reading: where small Q_n exists and where the interpolated form operates. The dossier previously promised these.
10. **A-MIS(iii) item 1.** Use the primitive form (spec §2), conditional on each admissible C, with the candidate-set rule (fixed before the analysis sample, or chosen on independent data). Add a new short **A-SPARSE-C** section in the same 6-item format: holds under local dependence (AR(1) neighbours), fails under pervasive factors, relaxation TD-A.
11. **A-MOM.** Second moments suffice for inclusion (TM-a0-inc, the SL Cor 2 counterpart); score moments are needed only for exclusion.
12. **Known weak points.** Replace items 3, 5 and 7 and add the spec §5 list:
    - MARGIN\* is now superseded by the population form;
    - the TS-b obligations now include the base-indexed step 3 and the k > m̄_d step;
    - mixed-rival evidence;
    - no necessity result for (U2b);
    - the Gaussian-linear TM tier;
    - TD′.
13. **Engine decision.** Add one line where the dossier discusses Engineering changes (or in "Questions about what we removed"): spec §4.
14. **No S1/S2 number inside any "Assumed." item.**

## SIMULATION_DATA_ANALYSIS.md
1. **Lead synthesis and the summary table.** E9/E9b are diagnostics of the *refined design-conditional form* only:
   - E9b's 3 D per (cell, d, m) are selected examples, chosen by population residual;
   - four designs at zero slack establish no 1 − o(1) event;
   - C = 121 is a sensitivity setting, not an implied constant.

   Add the **U2a check** (spec §1 Evidence; script `.rc_tmp/lead_v14/u2a_check.py`, which the Lead ran): the minimum over D and up to 2 inside proxies equals the exact κ_n. Quote, at SNR 1/2/3:

   | cell | SNR 1 | SNR 2 | SNR 3 |
   |---|---|---|---|
   | (500,500) | 0.653 | 2.613 | 5.878 |
   | (500,5000) | 0.693 | 2.771 | 6.234 |
   | (1000,500) | 0.626 | 2.505 | 5.635 |
   | (1000,5000) | 0.670 | 2.679 | 6.028 |

   The binding D retain x_10. Also add the AR(1) leakage-decay numbers.
2. **E9b section.** It was rerun with the raw-centred mean μ, as in harness/generate.R. The v1 table with the coded mean is kept as `tables/e9b_width_ext_s1_v1_codedmu.tsv`. d = 1 is identical, and d = 2, 3 change by ≤ 0.0015. Quote **exact minima** (never round a minimum upward), from `tables/e9b_width_ext_s1.tsv`:

   | SNR | d | C = 1 | C = 121 | no credit |
   |---|---|---|---|---|
   | 2 | 1 | 3.2896 | 2.3862 | 2.4889 |
   | 2 | 2 | 4.2658 | 3.6228 | 3.6867 |
   | 2 | 3 | 4.2987 | 3.8030 | 3.7921 |
   | 3 | 1 | 6.7098 | 5.8065 | 5.9091 |
   | 3 | 2 | 9.1027 | 8.4597 | 8.5237 |
   | 3 | 3 | 9.8397 | 9.3440 | 9.3332 |

   Width range 0.142–0.426. Re-check every E9b number in the file against the TSV.
3. **E2 reading (~line 178).** "The residual-variance/radius² ratio is ≥ 1 in 9/136 settings (max 1.74)." Do not compare the ratio to ε_n² again.
4. **E7 (and the synthesis/summary rows citing it).** E7 is a predictive-summary diagnostic: across-replicate quantiles of a predictive distance at posterior-mean coefficients, with a different radius. It does not measure within-data posterior mass. The E7 selected-MPM variance ratio illustrates variance inflation for a fitted subset and does not verify a prespecified-candidate theorem. Likewise, E1's MPM recovery and restricted κ do not test exact posterior mass or all active mixed classes. Put these qualifications in the summary table too.
5. **Files list.** Add `tables/e9b_width_ext_s1_v1_codedmu.tsv` (superseded) and the two `.rc_tmp/lead_v14/` scripts.

## Rules
- Write only the two files above. Never delete files. Do not commit. Do not spawn subagents.
- No /tmp scratch; use only `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/`.
- Never read or write under `/home/fb31/Bayesian-Variable-Selection/_local/engineering/`.
- For any Python, `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` and run under `nice -n 10`.

Reply (≤ 12 lines): what you changed per numbered item, and anything you left because the spec did not settle it.
