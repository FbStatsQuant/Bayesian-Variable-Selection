# Independent design review for HQ — 28 October 2026

Read: PROPOSAL.md; BRIEFING.md §§2, 4–5; THEORY_INVENTORY.md; 00_COMMON.md, T01–T36 and THEOREM_MAP.md. This review accepts Felipe's provability premise. No other consultant's answer was consulted; no jobs were run.

## 1. Critique of the selection

The proposed story is strong, but its central implication is incomplete: **T24 repairs an eligible particle; it does not deliver that particle. T26 establishes accuracy when the start already concentrates on the truth; it does not complete the masked-start repair argument.** These are different regimes, not consecutive links in one proof.

I recommend one replacement, keeping eight main-text results:

- **Move T07 to the decision-rule discussion**, with its proof in the supplement. Its distinction between exact-support and Hamming loss matters, but posterior decision theory and cancellation of a common size prior offer little standalone novelty. Moreover, size-prior retuning *can* affect the observed truth-plus-extras errors.
- **Add C37 below**, joining start mass, repair and an explicit discovery budget. This answers the referee's substantive question: where does the repairable particle come from, and what does obtaining and repairing it cost?
- **Keep T26, but label it a favorable-start corollary.** Its evidence/PIP conclusions are valuable, especially because the actual method reports these quantities. Do not advertise them for the masked regime merely because T24 discovers the truth there.
- **Keep T27 as a route-specific lower bound.** It explains why iid start proposals can be insufficient; it is neither a lower bound for the hybrid sampler nor evidence of computational optimality.
- **Keep T12, correcting the proposed shorthand.** The identity is islandwise, $E[\widehat Z_r\widehat{\mathrm{PIP}}_{rj}]=Z\mathrm{PIP}_j$, hence also for the average of these products. It is generally **not** an identity for pooled evidence times the primary, equally pooled PIP.

For **Biometrika's five**, choose **T03, T22, T24, C37, T21**. This preserves the target–start–repair–budget–reported-selection argument. Put T27's contrast in the text with its theorem in the supplement; move T12 and T26 there too. HQ's cut retains two composition results while demoting the start analysis that supplies their substantive content.

## 2. Holes and one new conjecture

The pool contains most necessary *types* of mathematics. The important hole is an explicit, compatible start-to-repair guarantee with finite budgets. Merely assuming eligibility, or increasing unspecified budgets until convergence occurs, does not fill it. C37 offers a small methodology extension that removes the need to prove survival of a repairable particle through the entire tempering/resampling system.

Other candidate directions have lower priority:

- **Weak-signal advantage:** no universal superiority theorem over SuSiE or SSL is justified. Their priors, approximations, optimization and decisions differ. Exact HPM optimality is a posterior-risk statement, not frequentist dominance. Even SMC's HPM–PIP gap may include PIP estimation error. A controlled comparison would need a precisely specified competitor and matched target before blaming approximation.
- **Finite n:** T21 and T24 already provide finite-budget inequalities, but useful numerical constants and a statistical error bound remain necessary. Removing the impossible SE premise alone does not make n = 200 informative.
- **Complexity and lower bounds:** attach T32's arithmetic costs to C37. “Polynomial for fixed sparsity” alone is weak: exhaustive search through supports of bounded size is already polynomial. The gain must be an improved dependence on p or a demonstrated repair-versus-iid separation. Restore **T05 to the supplement**: its sharp threshold and oracle gap honestly delimit the chosen target, although ORTH excludes p > n. Do not claim minimax optimality.
- **PIP calibration:** T23/T26 concern accuracy and eventual 0/1 recovery, not frequentist calibration of intermediate PIPs. That is a separate project. Misspecification robustness is likewise worthwhile but not essential to this paper's stated selection contribution; T04 is not such a robustness theorem.

### C37: Independent start-to-terminal scoring with an explicit budget

**Setting and assumptions.** Retain the exact target, actual block start and terminal hybrid kernel. Add M independent *scoring-only repair tracks*: each starts from an exact π₀ draw and executes h rounds at φ = 1. Their scores update the reported HPM, but do not feed the SMC particles, calibration, evidence or PIP calculations. Use separate random streams and budgets fixed before these tracks run.

On a data event $G_n$ of probability at least $1-\delta_n$, assume deterministic bounds

\[
\pi_0(\mathcal R_d)\ge b_n>0,\qquad
\inf_{x\in\mathcal R_d}K_1(x,S_0)\ge a_n>0,\qquad
\sup_{x\in\mathcal R_d}P_x(\text{one-round first exit})\le\eta_n.
\]

T24 supplies the last two bounds. For the first, T22(i) can supply $b_n$ from a reference $S^\circ\in\mathcal R_d$, using bounds on its aggregation quantities. **That reference need not be S₀**: do not impose start concentration on the truth in the masking regime. All statistical premises must hold jointly for the actual partition.

**Precise statement.** Write $s_n=1-(1-a_n)^h-h\eta_n>0$. Conditional on data in $G_n$, for the potential uninterrupted tracks,

\[
P(S_0\text{ never scored})\le(1-b_ns_n)^M\le e^{-Mb_ns_n}.
\]

With $m=p+B+2$, each track uses at most $1+2mh$ score evaluations. An indefinitely continued sequence of tracks therefore has expected score count until the first truth score at most

\[
C_{\rm setup}+\frac{1+2mh}{b_ns_n}.
\]

The first truth score is an analysis stopping time, not an implementable stopping rule. The implemented bank uses fixed M. Choose $h=\lceil\log(4)/a_n\rceil$, require $h\eta_n\le1/4$, and take $M=\lceil2b_n^{-1}\log(1/\epsilon_n)\rceil$. Then the miss probability is at most ε_n. T21 yields

\[
P(\text{no usable output or wrong HPM})
\le P(U)+2E_0[1-\pi(S_0)]+\delta_n+\epsilon_n.
\]

If $b_n\ge n^{-r}$, $a_n\ge n^{-s}$, and $\eta_n=o(a_n)$, expected discovery costs $C_{\rm setup}+O(pn^{r+s})$ score evaluations. Arithmetic cost additionally includes T32's per-score and start-sampling costs.

**Why plausible / proof route.** Condition on entering the basin, apply T24's survival-and-repair bound, multiply independent track failure probabilities, then sum a geometric tail. Use T22's normalized reference bound and T32 for the remaining inputs. The substantive proof work is a compatible statistical family, ideally one satisfying T27 where direct iid discovery is expensive but $b_n,a_n$ stay bounded below.

**Main risk.** The probability calculation is elementary; without that family and useful constants this is only bookkeeping. T24's factorial entrance constant may make the guarantee impractical. The tracks are a genuine algorithm extension, requiring separately labelled validation; the existing 2,400 fits did not run them. If they explain essentially all selection gains, the paper must also address what tempering contributes.

**Paper placement.** Immediately after T24 and before T21; no claim of PIP/evidence accuracy from these tracks. This is the only new conjecture I recommend.

## 3. Restatement notes for the eight selected results

Common convention: use a triangular array with fixed s₀ (e.g. 14), $p_n\le n^A$, and B ≤ 16. This does not cover a growing-sparsity generator $s_0=\lfloor\sqrt n\rfloor$. Distinguish the uninterrupted process from output availability; never condition identities on observed completion.

- **T03.** Retain Ω with cap K_n; restrict SE to the comparison unions actually used, bounded by $\min\{p_n,\min(K_n,m_n)+s_0\}$, and recheck cap-boundary comparisons. First use BM-∞ with $M_n\log n/n\to0$; then sharpen constants. Neither a feasible SE condition nor an $O_P$ posterior rate supplies a useful finite-n frequentist error rate.
- **T22.** Prove EXP and visibility/leakage bounds for the actual X-dependent partition. Require $2^{B_n}\sqrt{\log n}\,n^{-\kappa}\to0$ for truth concentration; for C37 use the deterministic reference bound instead. Normalized mass, response scaling and uniform score remainders are the failure points.
- **T27.** State a two-sided sequential law with a controlled reciprocal random multiplier and normalized reference mass. Recompute discovery from $Q_n p_n^{-c}n^{-c/2}$, where c counts masked additions, whenever budgets change; the published exponent is budget-specific. Initial marginal cancellation alone does not establish sequential cancellation.
- **T24.** Require $h_na_n\to\infty$ and $h_n\eta_n\to0$ for a single long track; PIP claims additionally need prefix stability and population occupancy. For C37 short restarted tracks, use its explicit h_n/M_n choices. Derive LK/EXIT/GAIN jointly; internal swaps, multiple-extra deletions and the factorial constant remain dangerous.
- **C37.** Use predetermined h_n, M_n, fresh streams and independent tracks, with $b_n,a_n,\eta_n$ justified on one event. Budget sequences must use declared bounds, not the unknown truth. Keep scoring-only information separate from SMC estimation; include setup, sampling and operational failures.
- **T21.** Retain P(U), nonlaunch and scoring-failure terms; insert C37's explicit bound or a separately verified original-method route. No independence between statistical and computational failures is needed. “Scored” must include rejected proposals; discovering truth cannot cure a posterior ranking error.
- **T26.** Keep the no-switch regime explicit: require $(T_n+1)\Delta_n\to0$ and $(L_n+4)\rho_{*,n}\to0$. Polylogarithmic budgets suffice only when those deficits decay polynomially; prove schedule/resource availability separately. Remove secondary PIPs. Increasing N_n alone does not repair these premises or establish masked-regime evidence accuracy.
- **T12.** Freeze calibration, grid, budgets and escalation before final randomness. Arbitrary finite n-indexed budgets preserve the ideal islandwise identities; state the averaged-product identity correctly. Remove the obsolete secondary estimator and exclude completion/flag conditioning. Floating-point evidence needs separate validation.

## 4. Verdict

**ENDORSE WITH CHANGES.** Final main-text eight: **T03, T22, T27, T24, C37, T21, T26, T12**. Biometrika five: **T03, T22, T24, C37, T21**. T07 becomes a decision-rule remark; T05 returns in the supplement. The proof campaign should prioritize compatible start-and-repair assumptions, not merely prove each conditional statement separately.
