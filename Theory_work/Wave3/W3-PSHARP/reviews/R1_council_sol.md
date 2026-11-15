# R1 blind council review — seat sol

Overall score: **7.6/10.0**. **FAIL for this frozen submission.** The four lemma files and the locked mathematical statement are sound on their stated domains. The report/registry materially broadens Claim B by dropping hypotheses, producing false claims. Two numerical summaries also need qualification.

Scope: the content designated in the brief as manifest `ce522b1f5ea1ec7ae390559678e4e58eb35a38d6248e59bd590148739a0ebb6a`, read only within the brief's allowlist. No other review, disposition, log, checkpoint, or manifest file was read. Prior reviewers' reported verdicts were not independently authenticated against their prohibited review files. No subagents or commits. Scratch and reproducible checks are in `reviews/R1_scratch_sol/`.

## Six gates

- **G1 correctness: PASS.** Re-derived Lemma V by completing the square; both Schur complements and the positive eigenvalue difference in S(1); block inversion in S(2); the prior ratio, gamma domain, exponential inequality and disjoint summation in S(3–4). These arguments cover empty sets and singular designs. For A, checked the exact truncated Gaussian moments, sphere normalization via the two gamma-ratio bounds, density bounds, Chebyshev constants and Lemma R without any assumed independence of kappa and scores. The orthogonal V bound gives the required exponent accuracy. In the spherical case, the identity for Q minus squared ridge-residual norm is correct; the conditional score law is constant in epsilon, giving unconditional iid scores; the rank-based events and both logarithmic restrictions yield the claimed uniform bound. A1's expectation lower bound and A2's necessary conditions follow by monotonicity and deterministic subsequence arguments. For B, the combinatorial product is exact and the fixed-j/Fatou argument gives exp(lambda/2) only under the stated s0/p -> 0 condition. For C, projection/minimization, the common noise event, fit comparison, prior/determinant/count bound and final exponent all check. No counterexample to a locked theorem item was found.
- **G2 hypotheses used = stated: PASS.** Every numbered item of STATEMENT is covered by its proof. The consequences of B are explicitly restricted at STATEMENT.md:98, with the extra critical-scale condition at :101. A3 clearly conditions the upper bounds on parents and retains the extra design-event qualification for the random-design expectation upper bound. C only claims failure for the two-column reference; its bounded-cost k-column alternative is correctly distinguished. The substantive discrepancy is in the report, detailed in M1 below.
- **G3 no hidden assumptions: FAIL.** The proof domains themselves are explicit and sufficient: nonconstant response, p >= 2, feasible supersets, rank-zero and empty-support cases, conditional randomness, common constants and common little-o envelopes. However REPORT.md:41–44, :106 and :149 drop restrictions that are essential to those conclusions. In particular the registry explicitly supplies only s0 <= K-1 as scope. See M1.
- **G4 statuses and citations: FAIL.** Proof statuses are consistently quoted as `PROVED (by this seat, unchecked)`; no parent upper bound is presented as proved here. C's account of the two parent size-tail statements and divergence of their normalized remainders is correct. The permitted external citation ranges support the quoted definitions and statements (32 external token checks passed). But the report and ingestible registry inflate B's proved scope (M1). This is a substantive reporting error, not a proof failure. The full citecheck script was not executed because one check reads TRIAGE.md outside this seat's allowlist; no such external file was read.
- **G5 constants and rates: FAIL.** All constants in the locked claims check: A's 1/sqrt(pi), c(p,s0), the full lower sum, and the critical exp(-lambda/2) limit on its stated domain. C's k=ceil(12 log n), n0=200, C_b=1200 and c1=1/[73(sigma*^2+bbar^2)] are valid. The cutoff envelope at 200 is about 0.18137 and decreases thereafter; p <= n/2 follows from the decreasing linear/log envelope. The entropy envelope is <=12(log n)^2, and 1/42-1/100-1/73 is positive (about 0.000110894). Thus these checks extend analytically beyond the finite numerical sweep. Nevertheless the report's unqualified critical-scale constant is false (M1), so this gate fails for the submission as a whole.
- **G6 coded target and numerics: FAIL.** The mathematical target agrees with the permitted C++ lines: K, nu, prior, determinant ratio and Q. The numerical formulas compute that real-arithmetic target; the structured C formulas correctly avoid cancellation. Fresh validation passed for orthogonal DP versus brute force, spherical one-step ratios, C's float64 and 60-digit comparisons, 8,064 S identities and 55,740 B cases. The fresh B minimum was 1.040315 (different seed), with equality in the explicit superset equality cases. The spherical and boundary experiments correctly compute only one-step odds; C correctly labels its reduced-k experiment in the proof file. Two report summaries obscure the actual numerical scope (m1–m2).

## Findings and exact corrections

### M1 — MAJOR: Claim B loses essential sparsity hypotheses in the report and registry

**Places:** `REPORT.md:40`, `REPORT.md:41`, `REPORT.md:43`, `REPORT.md:106`, `REPORT.md:149`. Compare the correct `STATEMENT.md:98` and `STATEMENT.md:101` and `lemmas/B_sparsity.md`'s Consequences section.

The report states the critical-scale cap exp(-lambda/2) without s0/p -> 0. Its registry repeats this and states the necessary s0/rate conditions with scope only 0 <= s0 <= K-1. The text also says that beyond s0 comparable to sqrt(n), consistency fails on every design, without the p/2 restriction.

These are false as written, not merely unsupported. Take orthogonal standardized columns and standardized y = sum_{j in S0} x_j/sqrt(s0). For a model containing t signal columns and u null columns,

    D_S = n^(t+u),
    Q_S = (n-1)/n + [(n-1)^2/n] (s0-t)/s0.

All models missing a signal have negligible total odds when s0 is comparable to sqrt(n): their fit penalty dominates the exp(O(s0 log n)) prior/determinant/count factor. Supersets have fit factor one.

1. With p=s0+1 and s0=floor(sqrt(n))-1, there is one strict superset and its odds are exactly n^(-1/2). Consequently pi(S0) -> 1, although s0/sqrt(n) -> 1. Grouped exact enumeration gives pi(S0)=0.9900990099 at (n,p,s0)=(10000,100,99) and 0.9990009990 at (1000000,1000,999). Also delta=O(n^(-1/2))=O(r_n), contradicting the unrestricted registry's necessary s0=O(sqrt(log n)).
2. Even retaining s0 <= p/2 is insufficient for the reported critical constant: set p=2s0 and s0/sqrt(n) -> lambda. The superset odds tend to exp(lambda/3)-1, and pi(S0) -> exp(-lambda/3), exceeding exp(-lambda/2). For lambda=1 the exact values are 0.7132154480 at n=10000 and 0.7161995961 at n=1000000, approaching exp(-1/3). The sum limit follows from the fixed-j limit and domination by the negative-binomial series with ratio factor s0/(3s0-1).

**Exact correction:** introduce the consequences at REPORT.md:40 with `For sequences with s0 <= min(K-1,p/2):`; add `and s0/p -> 0` to the critical-scale sentence at :41. At :106, qualify the every-design obstruction by `with s0 <= min(K-1,p/2)`. At :149, retain the broad scope only for the exact O_lb inequality; explicitly attach `s0 <= p/2` to the consistency and rate necessities, and attach `s0/p -> 0` to the critical limit. Replace the unconditional registry rate `(s0+1)/(2 sqrt n)` by `c(p,s0)/sqrt n`, noting the former as its asymptotic value when s0/p -> 0. Likewise qualify the arrow at :40 by s0/p -> 0. No change to the locked theorem or its proofs is needed.

### m1 — MINOR: orthogonal numerical summary omits the model-size truncation

**Place:** `REPORT.md:81` (continuing :82–85).

The report describes the DP outputs as odds delta/(1-delta). The large fixed-s0 runs omit sizes above s0+60, while the growing-s0 runs use s0+80. The script and A_log_factor.md's final remark disclose this accurately, but the report itself does not. Finite comparisons showing tiny differences do not establish that every reported row equals the full odds.

**Exact correction:** describe these as `odds summed over |S| <= min(K,s0+60) (s0+80 for E2), a lower bound on full odds before quadrature error`; retain the exact-formula/quadrature and finite validation qualifications. Refer to these restricted odds in the following ratios.

### m2 — MINOR: counterexample summary omits b=3 qualification

**Place:** `REPORT.md:97`.

`pi(|S| > cutoff) = 1.000 for n >= 100 on the counterexample arm` is not true of all displayed rows: c_counter_out.txt also reports median 0.9489 at n=400,b=1 and 0.4656 at n=1600,b=0.5. Even on the b=3 rows, 1.000 is rounded numerical output. The C proof file's final paragraph correctly qualifies this as a median at b=3.

**Exact correction:** replace the sentence fragment with `For b=3, the median pi(|S| > cutoff) rounds to 1.000 for n >= 100; the control tail is <=3.2e-13 in every recorded seed.`

## Verification record and disposition

`R1_scratch_sol/checks.py` and `checks_out.txt` contain the fresh numerical checks and grouped counterexamples; `citations.py` checks permitted external ranges only. The reported frozen output numbers were compared with the permitted output files. Long Monte Carlo suites were inspected rather than repeated in full; no numerical result was used as a substitute for an asymptotic proof. Claim C's finite enumeration is correctly treated as a mechanism check, not a verification of its large constant hypotheses.

Counts: **0 FATAL, 1 MAJOR, 2 MINOR, 0 NIT**. Correct M1 before acceptance; the core mathematical results need no identified repair.

COUNCIL-VERDICT round=R1 manifest=ce522b1f5ea1ec7ae390559678e4e58eb35a38d6248e59bd590148739a0ebb6a seat=sol score=7.6 gates=FAIL
