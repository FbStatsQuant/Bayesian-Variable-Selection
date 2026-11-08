MIDPOINT VERDICT: CONTINUE

References: T = Theory_work/Wave1/W1-PXN/STATEMENT.md; P = Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md; L = Theory_work/Wave1/W1-PXN/lemmas/; NBH = Theory_work/Old_Projects/New_BVS_Headquarters/.

1. [No substantive blocker: (P), including A > 1.] T03-sharp has the needed fixed-design conclusion and explicitly allows p <= n^A (NBH/branch_snapshots/W6-FIXREV2/STATEMENTS.md:19-35,51-57). L/P8_T03sharp.md:27-54 supplies a deterministic O(log n) cutoff, simultaneous sparse eigenvalue control, beta-min, and a valid sequence-selection de-randomisation argument. L/CR_corr_tails.md:32-39 supplies the required correlation event. None requires p <= n or a polynomial lower bound on p. Accepting the cited theorem as a dependency, its application is adequate.

2. [No substantive blocker: (R), but explicit constant unresolved.] L/CR_corr_tails.md:17-30 gives a valid elementary pair tail; :41-51 combines it with deterministic partition recovery to obtain summability and eventual p^{-C}. This bypasses Hotelling/W7 Corollary B entirely. It does NOT establish T:53's sharper constant/exponent. T:94-97 expressly permits this fallback, so resolving D2 this way does not require changing the headline.

3. [No substantive blocker: (S), (E).] P:246-268 uses unconditional fixed-group Beta laws, truncated moments and locked T22(i); recovery is intersected afterwards (P:104-115). P:280-284 correctly obtains the masked limiting law using locked T22(ii) and the joint masked-column limit. The unique-mode argument proves eligibility without a DP tie invariant (L/LS_P6_repair.md:38-42). The unused invalid large-set domain of B(ii) is properly restricted in L/B_ii_domain.md:8-13. I see no additional statistical gap here.

4. [No substantive blocker: (T), (K).] With the checked lattice margins, L/L_strict_localmax.md:10-30 supplies the missing uniform addition bound, including its additive o(1) remainder for each fixed A. L/LS_P6_repair.md:14-35 correctly distinguishes scoring, arrival and certification, imposes the eventual move-cap/feasibility conditions, and repairs both score counts. Laurent-Massart is used within its stated chi-square range; the Lemma E corrections are recorded at L/ERRATA.md:8-12.

5. [No substantive blocker: reported HPM / (C).] Finding S0 alone would not suffice. P:443-446 instead uses posterior mass > 1/2 to ensure that S0 beats every scored competitor. The repaired closure inclusion (L/LS_P6_repair.md:44-50) connects actual and potential scored sets under the expressly assumed GUARD/OP-LS0 premises. Thus the result concerns the reported HPM of the specified v3 + LS0 method, while making no delivery guarantee (T:28-45,67-71). It does not establish a production implementation bridge.

6. [Minor: onset and stale quantitative wording.] T:51 writes n0(A,C,rho,psi-bar), but SIZE is only eventual, with a sequence-dependent n1 (T:19). The recovery onset must also require n >= n1. Moreover T:84's displayed cutoff estimate should be reconciled with the corrected, slightly larger bound actually proved in L/P8_T03sharp.md:29-35. Neither issue obstructs (P) + (C) for fixed A.

Required before final verification:
- Resolve D2 explicitly: retain only (R') unless the sharper Hotelling constant is independently justified; propagate that choice to T:52-54,83.
- Qualify the recovery onset by SIZE's onset, and synchronise the displayed cutoff bound with the repaired proof.
- Present a single final proof using the enlarged design event, all ERRATA replacements, and the eventual conditions ell_n >= c and s0 <= K. Keep exact arithmetic and GUARD/OP-LS0 as hypotheses.

No counterexample or fatal remaining gap identified. This is a midpoint recommendation to finish verification, not a final verification certificate.

---
## Disposition (W1-PXN lead, 2026-11-08)
CONTINUE. Required items: (i) D2: the mid-point reviewer saw only proof files; the sharper Corollary-B constant was
independently justified by item reviewer R14 (Hotelling density, Lemma 2 steps 1–6, t*, I*, constant), with the display
split of lemmas/R_branch_repair.md §1; (R′) is kept as the independent cruder route. STATEMENT keeps (R-b) as VERIFIED (R14)
and (R-c) summability. (ii) SIZE onset n₁ added to (R); STATEMENT §3 cutoff synchronised with P8♯ step 1. (iii) A single
consolidated final proof is written as FINAL_PROOF.md before the exhaustive sweep.
