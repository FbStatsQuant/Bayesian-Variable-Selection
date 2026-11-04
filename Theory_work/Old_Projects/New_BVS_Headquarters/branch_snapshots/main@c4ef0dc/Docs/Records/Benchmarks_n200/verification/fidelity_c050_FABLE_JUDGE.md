# Fable 5.1 ruling on the fidelity findings (2026-10-21; Fable call 1 of this task)

Input: FABLE_DOSSIER.md and the eight REPORT.md files. Reply as returned:

## Rulings

**Q1. EBIC size rule.** **(b)**: K = ⌊n/log n⌋ = 37 as the primary bound for every EBIC rule (F1–F5, all γ), cap 100 kept as secondary; additionally register F4 `λ ≥ 0.05·λmax` and F5 `sic_smax` as S0 rows. Reason: Chen & Chen's Theorem 1 is stated for bounded model size, so some K is required, and K must be truth-free, the same for every method, and invariant to c; the 0.05·λmax endpoint fails the last test (it admits 59–68 variables at c = 0.5, F4 §5), and SIC's s_max = 17–19 sits so close to the true 14 that it would look tailored, so (c) belongs as sensitivity, not headline. K = n/log n is a function of n alone and is the standard screening-size bound (attributed to Fan & Lv by the F4 auditor from memory; unverified in these files). It is principled, not arbitrary, and it is inert for F1–F3 at c = 1 (max EBIC size 31), so uniformity costs nothing. Pre-declare: K formula; its application to all five methods and all γ; cap 100 as S0; the two author-tuning S0 rows; redefinition of `ebic_at_largest` to count k > K (F4 M1); the production scorer, not a derived script, as the authoritative code path, with equality verified on c = 1. c = 1 label: re-headline with K37 marked "post hoc (chosen from size diagnostics after c = 1)", with the original cap-100 row kept directly beneath and never deleted.

**Q2. cv_min vs cv_1se.** Keep **cv_min** as the registered primary. Reason: it is Tibshirani's own rule and was pre-declared; switching now with knowledge that cv_min gives 0/600 would be outcome-informed even though generous to the benchmarks; both the 1996 and JSS 2010 recommendations are real author recommendations, so neither is unprincipled. Pre-declare: every headline table shows cv_min, cv_1se and ebic1 (K37) side by side with equal prominence; T5 footnotes the thresh = 1e-16 inflation or adds a default-settings timing row. c = 1: unchanged.

**Q3. F2 α grid.** **Keep and disclose.** Reason: α = 0.9 at the CV minimum corresponds to λ₂ ≈ 0.01, which is already a point in Zou & Hastie's own grid; CV error is monotone toward α → 1, so extending to .99 just produces a near-lasso that F1 already represents, at ~600 CPU-h for 2–14 fewer variables. The 100% edge rate is a pre-declared diagnostic, so disclosure is honest, not concealment. Pre-declare: grid frozen; `alpha_edge` and α* distribution reported per cell; the m3 restriction (EBIC candidates from the α* path only) stated. c = 1: unchanged.

**Q4. A1 refine.** **Register `SuSiE-refine` as an extra arm at both scales.** Reason: it is the authors' shipped remedy for exactly the regime c = 0.5 creates; running it at c = 1 preserves pairing; choice between fits by ELBO is outcome-free; the asymmetry with F5 (not polished) is principled because polishing is not ABESS whereas refine is SuSiE. Pre-declare: default A1 stays primary; refine is S1, reported beside, never substituted; ELBO gain and ΔPIP tabulated; `L_saturated` renamed "all L effects active". c = 1 label: "arm added after c = 1 results were seen; fit selection by ELBO".

**Q5. A2.** **Agree.** Frozen settings; SSL-RS reported at c = 0.5 as "SSL with the Ray–Szabó ladder (variance/ladder sensitivity)". Pre-declare that label plus σ_L and support-settling point by cell. c = 1: unchanged.

**Q6. A3.** **D-c050-1 is sound.** Add: run the 12 dev datasets at c = 0.5 with the production budget, diagnostics only, applying O10 per p and per scenario, with a second-chain Jaccard; any budget change applies to both scales with c = 1 rerun. c = 1 label: flag fractions by scenario; state that `ci95` is bayesreg's own printed indicator and that `km2` is unsourced.

**Q7. Stop or rerun c = 1?** **No rerun of any existing arm.** Needed: derived rows (F4 0.05·λmax, F5 sic_smax, K37 for all EBIC rules) from saved c = 1 fits; refine at c = 1 as an additive arm; the pending bit-identical reproductions for A3 and F1–F5. See hypotheses below for what the audits missed.

**Q8. Auditor probes.** **They do not compromise the decisions.** Own generator, own seeds, no study data; the recommended rules are either functions of n alone or the authors' shipped option with ELBO-based choice, so the probe TP counts cannot have steered a free parameter. Pre-declare: the registration notes that probes existed; probe TP counts are never cited as evidence in the paper.

## (i) Before c = 0.5 production, in order

1. Write and timestamp the pre-registration containing every rule above; c = 0.5 pilots remain diagnostics-only until it exists.
2. Complete the bit-identical c = 1 reproduction through the new code for A3 and F1–F5.
3. Implement K37 in the production scorer, fix the F4 flag, derive the F4/F5 author-tuning rows at c = 1 from saved fits, and confirm the derived K37 rows equal the scorer's rows.
4. A3 c = 0.5 dev diagnostic pilot (per-scenario O10, second-chain Jaccard).
5. Run the 12-dataset c = 0.5 diagnostic pilot for A3 and F1–F5 (only A1 and A2 are done); check F1–F3 `npasses` headroom against c = 1 maxima.
6. Register SuSiE-refine, re-measure `--time`, launch the c = 1 refine arm (may run concurrently with c = 0.5 production, as it is additive).

## (ii) Hypotheses the audits may have missed

- H1: The cap of 100 "equals the SMC k_max". If benchmarks now get K = 37 while SMC-BVS keeps a support bound of 100, a referee will ask about the asymmetry. Pre-declare why an EBIC candidate bound and a prior support bound differ, or apply the same bound to both.
- H2: The F4 artefact (OLS refit on near-saturated supports) can appear in the F1–F3 EBIC rows at c = 0.5, because the lasso path reaches larger supports relative to noise; it was inert at c = 1 only because sizes stayed ≤ 31. The uniform K37 rule is the protection; do not exempt F1–F3.
- H3: A3's `ci95` is a marginal 95% rule and will under-select at β_min = 0.4 by construction; A1's `bfdr10` has a structural ⌊k/9⌋ extra. Both will shift at c = 0.5 for rule reasons, not method reasons; captions must say so or SMC-BVS will look better than it is.
- H4: Two code paths (production scorer vs `derive_ebic1_K37.R`) for the same rule is a reproducibility risk; item 3 above addresses it.
- H5: No audit checked whether the c = 0.5 λ grids' deep end causes `maxit`/`jerr` failures in S5 for F2 (slowest arm); a single failure fails all four rules.

## (iii) Overall

**Proceed**, conditional on items 1–3 being complete before any c = 0.5 scored output exists. The c = 1 study stands; the only blocking defect (F4 B1) is a selection-rule bound fixable from saved fits, and every other finding is labelling, disclosure, or an additive arm.
