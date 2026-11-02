# Low-p benchmark adaptations

LA-1 through LA-3 are technically accepted by Sol's review; the review did not establish the separate D3 commitment.

- **LA-1:** F1–F5 use the feasible EBIC/BIC size bound `min(100,p)`. This restates the original feasible set.
- **LA-2:** F5 uses sizes `0..min(100,p)`; larger sizes are impossible.
- **LA-3:** A1 requests `L=min(50,p)`, matching the effective capacity of the pinned implementation. Report requested L=50 and effective L=p; `L_saturated` means all available effects active (possible weak-effect over-fitting).
- **LA-4 (LOWP manager decision):** Implement PREREG R1 for both scales from the saved primary fit without refitting. Use `K=min(floor(n/log(n)),p)=p` here. K37 and cap rows have identical values by construction because p≤30<37<100, but their identities and roles remain distinct. Keep cap rows secondary; F1–F3 retain `cv_min` primary and K37 companions S0. F4 and F5 use `ebic1_K37` primary; F4 also emits S0 `ebic1_lam005`, and F5 S0 `sic_smax` over sizes 0 through `min(p,floor(n/(log(p)*log(log(n)))))`. No S1 arms. Derived rows are labelled pre-registered at c050 and post hoc at c100. The reason is to honor the preregistered registry and the LOWP manager's explicit ruling even when the candidate sets coincide.

`selected_k_gt_K37` records PREREG's additional size diagnostic; it cannot be true at these p values. The inherited `ebic_at_largest` code continues to identify the largest valid candidate (including a full p-variable model); it does not imply an artificial restriction. F3 uses the exact production expression `10^seq(3,-6,length.out=61)`. The F3 ridge pilot, A2 Beta(1,p) and ladder, and A3 production budget are unchanged. Fit timing starts before wrapper invocation; packages are checked and loaded before timing, unlike the earlier LOWP runner. Comparisons with historical timing must account for package loading and runtime environment.
