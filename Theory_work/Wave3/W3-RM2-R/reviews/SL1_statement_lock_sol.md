# SL1 — statement lock, W3-RM2-R (Sol: codex gpt-6.1-sol, reasoningEffort high; fresh, blind; brief BRIEF_SL1_sol.md). Reviewed STATEMENT v0.1 (the v0.1.1 record edit landed during the review). Reply verbatim below.

**1. Verdict: DO NOT LOCK.**

The constant-level statistical changes are viable. The delivery claim needs corrections to its domain and treatment of explicit code guards; T2(c) and one dependency edge also need repair.

**2. Findings**

1. **[S] The input definition omits `length(y) = n`.**  
   [STATEMENT:73–75](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:73) defines a finite, nonconstant response vector without specifying its length. Consequently, the universal delivery claims at lines 116–127 include, literally, `X = matrix(c(0,1,2), ncol=1)` and `y = c(0,1)`. The pinned [preprocessing check](/home/fb31/BVS-wt/W3-RM2-R/Scripts/SMC_BVS/core/v3_preprocess.R:104) rejects this input. I reproduced that rejection using only the R preprocessing function.

   **Fix:** require \(y^r\in\mathbb R^n\), and explicitly require scalar seed and allocation fields matching the public validators.

2. **[F] IDEAL-W does not, as stated, exclude every explicit LS0 validation exit.**  
   [STATEMENT:125–132](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:125) promises delivery for every valid input; [PLAN:14](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/PLAN.md:14) treats size-related exits as excluded by IDEAL-W. However, [v3_run.R:95–97](/home/fb31/BVS-wt/W3-RM2-R/Scripts/SMC_BVS/core/v3_run.R:95) explicitly rejects `ls0_ell > 1e6`. This comparison is not an arithmetic overflow. The imported IDEAL-W premise removes arithmetic overflow, not comparisons against literal limits.

   On an unbounded-size interpretation, the default \(\ell_n=\lceil\log_2(n+p+1)\rceil\) eventually exceeds \(10^6\). For example, idealised \(n=p=2^{10^6}\) enters the SMC branch and has \(\ell_n=10^6+2\). The option validator then stops the fit regardless of allocation. I separately reproduced the validator’s rejection with a small in-memory settings object.

   The explicit [C++ cap-range guard](/home/fb31/BVS-wt/W3-RM2-R/Scripts/SMC_BVS/core/cpp/v3_core.cpp:473) also needs a stated interpretation under the unbounded-word machine.

   **Fix:** explicitly specify which representability/validation guards the idealisation lifts, or restrict the delivery theorem to a supported domain and reconcile that restriction with its asymptotic uses. A fixed bound \(\ell_n\le10^6\) alone cannot support an unrestricted \(n\to\infty\) conclusion. The present exit classification is incomplete.

3. **[F] T2(c) is stated under a stronger start event than the requested target.**  
   [STATEMENT:59–63](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:59) and [103–112](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:103) require **every** maximiser of \(\gamma_0\) to belong to \(\mathcal L'\). The [BRIEF’s target T2(c)](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/BRIEF.md:28) concerns the interval below the **coded** start \(\widetilde S_0\). These events can differ when start-law maximisers tie.

   **Fix:** state (a′) on
   \[
   \{\widetilde S_0\in\mathcal L'\}\cap NA(\mathcal L')\cap TL(\mathcal L').
   \]
   Down-closure then keeps \([S_0,\widetilde S_0]\) inside \(\mathcal L'\). Use this start event in the associated error bound; retain the all-maximiser event as a sufficient condition. This requires no additional proof machinery.

4. **[F] The DLV-0 ⇒ Proposition F edge does not preserve the parent premises as written.**  
   [STATEMENT:189](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:189) justifies the implication by “every input ⇒ almost every input.” That addresses the data-law restriction, but DLV-0 also changes the method’s LS0 cap and requires allocation envelopes re-derived for that cap and the current preflight. The [parent delivery setup](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave1C/C-DLV/STATEMENT.md:10) uses the earlier cap and allocation specification.

   **Fix:** qualify the edge as recovery of the parent *delivery conclusion under (D)*, rather than an unqualified implication to the registered parent theorem; alternatively, prove a parameterised delivery lemma covering both cap/allocation specifications. The statistical containment rows do not have this problem.

5. **[E] Two DLV premise pointers are stale or incomplete.**  
   [STATEMENT:66](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:66) cites DLV lines 21–39, but TDP-IMPL’s cost/storage requirements continue through line 42. Line 75 cites DLV lines 40–41 for declared inputs; those conditions are now at [DLV:43–44](/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave1C/C-DLV/STATEMENT.md:43).

   **Fix:** update those ranges to 21–42 and 43–44, respectively. This is editorial.

**3. Per-point answers**

1. **(V♭): passes.** On the parent block-noise event, \(z_n/\sqrt{\log n}\le\sqrt{2A}+o(1)\). Step 2(a) therefore has score margin
   \[
   \left[\frac{(\sqrt{M_V}-\sigma\sqrt{2A})^2}{2C_R}-A-\tfrac12\right]\log n-o(\log n)>0.
   \]
   The stated \(M_V>M_V^0\) suffices. The ladder and junk-exclusion steps do not otherwise consume visibility; neither do the lattice or posterior bridges.

2. **(BM-W⁺): passes.** The first inequality gives the truth square at least \(\sigma^2\lambda_n/4\). Identity (4.1) then gives the planned RSS bound. Substitution into the score comparison yields exactly
   \[
   c_{\mathrm{TL}}>8(A+1)+4(2A+1)C_R/\sigma^2.
   \]
   This also makes the RSS difference positive. Both `(BM-W) ⇒ (BM-W⁺)` and `(BM-Q♭) ⇒ (BM-W⁺)` follow from the displayed bounds; the sufficient constants are conservative.

3. **(T1-F♭): passes.** BM(c) is explicitly an alternative hypothesis of SOP:TH09 itself, and its conclusion includes \(1-\pi(S_0)=O_P(\sqrt{\log n/n})\). Boundedness converts convergence in probability into [POST]; Markov then gives [MODE]. No remaining Form F bridge needs BM-∞ separately once visibility and truth removal are supplied by their new hypotheses.

4. **RM0-plus: the proof extensions pass, subject to finding 3.** L1.1 uses NA at the current set \(C\) and at \(C\setminus\{e\}\), and TL at \(C\); all belong to the down-closed family. RM-0(b) uses \(\pi(S_0)>1/2\) only to obtain strict global F-maximality. The almost-sure input-validity assertion is correct for Setting F with nonconstant raw columns and for Setting R: unit marginal variances suffice for nonconstant Gaussian columns, and the response is conditionally nonconstant almost surely.

5. **DLV-0: not yet established as stated.** The fallback argument works: tier-0 construction failure sets a trigger and forces escalation unless its preflight stops; tier 1 records the last successful construction or the pilot schedule. Both satisfy `v3_check_grid`, so the `e == 1` fallback removes `schedule_limit`. Nonconstant retained columns exclude `no_predictors`; EX-A excludes scorer failure. The enlarged LS0 count, archive size and measured preflight charge remain polynomial, so re-auditing resources requires no new mathematics. Findings 1–2 nevertheless leave uncovered exits.

6. **Ex-Proxy-d: passes.** The residual formula in PLAN gives the stated upper bound uniformly over proxy subsets; outside columns do not affect the residual. Since \(r(q-1)\to0\), \(d_n=O(1)\). Part (b)’s BM-Q equivalence follows from \(q+\log n\sim n^b\). In part (c), the factor two compensates for \(\phi_0^2=1/2\); moreover \(c_{\mathrm{TL}}^0>8\), so κ₀ also covers the first additive-width inequality.

7. **Dependencies: the statistical rows pass; the DLV row needs qualification.** The hypothesis weakenings and retained conclusions justify the RM0, RM2-F/R, sandwich, TL and fixed-signal proxy implications. Cont-plus composes with the parent containment claims. The DLV edge needs the cap/allocation distinction in finding 4. The registry retains the stated substantive conditions on SOP:TH09 and W2-APP:POST.

8. **Targets: substantially covered, with two unresolved qualifications.** T4’s three signal changes and the decaying-signal witness are present. T2(b) is faithfully implemented. T2(a) remains blocked by the delivery-domain/code-guard issues, and T2(c) needs the coded-start formulation in finding 3. The optional quantile and equicorrelation work, and the named Form R open item, are disposed of consistently with the brief.
