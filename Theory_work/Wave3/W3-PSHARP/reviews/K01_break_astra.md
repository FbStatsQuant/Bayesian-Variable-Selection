# K01 blind adversarial break review

Reviewed STATEMENT v1.1 against the permitted definitions, proof routes, assumption map, and numerical sources. No proof files in W3-PSHARP were read. No other reviews or logs were read. I did not change the reviewed sources, commit, or start subagents. The independent code and its output are in `K01_scratch/check.py` and `K01_scratch/check_out.txt`.

**Result:** no numbered mathematical claim broken. Two MAJOR findings concern purported numerical evidence, and one MINOR finding concerns the wording of B. Counts: **FATAL 0; MAJOR 2; MINOR 1; NIT 0.** NOT-BROKEN means the stated claim survived the checks described below, not that an unseen finished proof has been certified.

## 1. Per-claim verdicts

| Claim | Verdict | Work performed |
|---|---|---|
| S | NOT-BROKEN | Re-derived both Schur identities, strict equality condition, positivity, empty/rank-deficient cases; reran 8,064 numerical pairs. |
| A | NOT-BROKEN | Derived both witness arguments, truncation constant, dependence handling, uniformity and conditional transfer. |
| A1 | NOT-BROKEN | Derived odds-to-probability and expectation consequences. |
| A2 | NOT-BROKEN | Derived necessary sparsity conditions and checked existence of growing-support witnesses satisfying E and C. The advertised E2 experiment does not satisfy E: finding F1. |
| A3 | NOT-BROKEN | Checked the hypotheses against the permitted statements of Theorem 1, Corollary 1R, and the expectation theorem. Did not inspect their external proofs. |
| B | NOT-BROKEN | Re-derived the finite sum, its first term and all constants, including s0=0. Wording correction F3. |
| B1 | NOT-BROKEN | Derived deterministic bound and limiting implications. |
| B2 | NOT-BROKEN | Derived the tightness implication for deterministic sparsity sequences. |
| B3 | NOT-BROKEN | Checked the stated witness scope and the rate/consistency obstruction. |
| C.1 | NOT-BROKEN | Derived exact representation, coefficient blowup, reference-cost bounds and checked actual parent hypotheses; independent high-precision minimization. |
| C.2 | NOT-BROKEN | Derived a bound valid for every n >= 200; independently scanned all integers 200 through 20,000. |
| C.3 | NOT-BROKEN | Derived a uniform fit-loss and posterior comparison with explicit constants sufficient for C_b=1200; checked the ridge penalty when x2 is used with a large coefficient. |

## 2. Findings and exact corrections

### F1 — MAJOR — Growing-sparsity numerical experiment violates the energy hypothesis

**Place:** `Theory_work/Wave3/W3-PSHARP/numerics/a_orth.py:140-147`, especially lines 141 and 147; Proposition A's energy condition is `STATEMENT.md:50`.

E2 labels itself a check of Corollary A2, but takes s0=round(n^0.3), an orthogonal design, and theta=1 on every active column. Consequently

    ||mu||^2/n = ((n-1)/n) s0 -> infinity.

There is no fixed M satisfying E. In addition, response scaling then grows with s0, so the omitted fixed-energy restriction is relevant to the proposed normalization argument; this is not merely a cosmetic choice of constants. The independent script reports energies per observation 5.985, 8.994375 and 13.9978125 at the three configured n values.

**Exact correction:** in E2 set the active coefficient argument of `suff_stats` to `1.0/math.sqrt(s0)` and change the printed description accordingly. Then ||mu||^2=(n-1), ||theta||^2=1, all active coefficients remain nonzero, and the experiment is within the corollary. Rerun E2 and replace its output. Alternatively retain the old experiment but explicitly label it outside E, and add an actual within-hypothesis experiment. This does not break A2: the corrected sequence establishes that its assumptions are satisfiable.

### F2 — MAJOR — Boundary lower-bound experiment is promoted to a full necessity conclusion

**Place:** `Theory_work/Wave3/W3-PSHARP/ASSUMPTION_MAP.md:13` and `:14`; compare `numerics/a_boundary.py:6-9`, `:32-33` and `a_boundary_out.txt:1-5` at the snapshot read.

The map says “FAILED-REMOVAL in kind” and that “the log factor disappears in probability,” citing a script which only computes L1, the sum of one-step superset odds. Even proving L1=O_P(n^-1/2) would not prove that delta or all posterior odds lack the sqrt(log p) factor: L1 is a LOWER bound, and all other model sizes and non-supersets are omitted. The script properly calls its argument a heuristic; the map overstates it. The output snapshot had only one completed positive-correlation configuration, so it also did not establish a limiting trend for that arm. Additional rows would not fix the direction-of-inequality problem.

**Exact correction:** replace the necessity cell with: “Evidence that the one-step proof mechanism need not retain the logarithmic enhancement under dependent null columns; the script computes only one-step odds. Failure of Proposition A's full posterior conclusion without the witness condition is not established here.” Do not classify the condition as FAILED-REMOVAL for the full posterior until there is an upper bound controlling the remaining models, or a separate valid counterexample. Apply the same qualification to row 14's “as above.” This issue does not affect the actual witness theorem A.

### F3 — MINOR — “Equivalently” discards the higher-order terms of B

**Place:** `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:93-94`.

The full odds bound is equivalent to pi(S0)<=1/(1+O_lb). The displayed bound sqrt(n)/(sqrt(n)+c) is only its j=1 consequence (and is equivalent to the weaker odds>=c/sqrt(n) inequality). Generally the higher-j terms are strictly positive.

**Exact correction:** replace “equivalently pi(S0) <= sqrt(n)/(sqrt(n)+c(p,s0))” with “equivalently pi(S0) <= 1/(1+O_lb_n), and in particular pi(S0) <= sqrt(n)/(sqrt(n)+c(p,s0)).” Both current inequalities are true; this is not a counterexample to B.

## 3. Adversarial derivations: S and A

### S: determinants, fit, and degeneracy

Both G+I and H are positive definite even for a rank-deficient S. Their new diagonal entries are n and n^2, respectively, giving exactly the two Schur complements stated in S. For every eigenvalue lambda>=0,

    (n+1)^2/((n+1)lambda+1) - n/(lambda+1)
      = ((n+1)lambda+n^2+n+1)/(((n+1)lambda+1)(lambda+1)) > 0.

Thus s<=n*den, with equality exactly when g=0, equivalent to orthogonality to the whole column space. This also handles S empty. Iteration gives the determinant inequality for every disjoint J as an algebraic statement, even when the union leaves Omega; posterior comparisons use only feasible unions.

The block inverse gives the stated squared residual score times n/s. The minimum-penalized-squares representation of Q proves positivity and monotonicity independently of cancellation-prone matrix subtraction. Since 2b0>0, gamma<1. Prior ratios and summation then give S.3-S.4 without further assumptions. No sign reversal or lost factor of n was found.

### A: orthogonal witness and dependence on V

Write u_j=x_j/sqrt(n-1). Null scores u_j'epsilon/sigma are independent standard Gaussians. The unscaled variational bound is

    V=s_y^2(2b0+Q0) <= ||C epsilon||^2 + M+M' + 2b0 s_y^2.

Uniformly under E, s_y^2=O_P(1), so V/(n sigma^2)<=1+O_P(n^-1/2). The precise multiplier is 2nu(n-1)sigma^2/(nV), as in PLAN. Since N<=n-1, its possible downward error times log N vanishes. **Independence of this multiplier and the scores is not needed:** intersect its high-probability lower-bound event with the truncated empirical-sum event. This handles the dependence explicitly rather than pretending the denominator is independent.

For tau=2log N and Z~N(0,1),

    E[exp(Z^2/2) 1{Z^2<=tau}] = sqrt(2tau/pi).

The second moment is at most exp(tau/2)*sqrt(2tau/pi). Hence the relative variance of the sample mean tends to zero; the multiplier error changes each truncated term by at most exp(-o_P(1)). Multiplying by S's prior factor and n^-1/2 gives exactly Lambda, including its factor 2 and pi. The n-1, nu=n/2+0.01, and studentization terms contribute only the vanishing multiplier correction.

### A: spherical witness

Condition on (X0,theta,epsilon). The nonzero ridge residual direction is then fixed. Rotational invariance in the (n-1)-dimensional centered space gives iid scores

    zeta_j=(n-1)<omega_j,rho/||rho||>^2
       ~ (n-1) Beta(1/2,(n-2)/2).

The conditional distribution is constant in the conditioning variables, so the scores are also independent of those variables. Centering reduces the ambient dimension by one; the stated beta parameter is correct. Columns outside the truth and witness block do not enter these pairwise odds. They may affect the posterior normalization, but cannot invalidate the lower bound from the selected ratios.

Set P=(n+1)X0 H0^-1 X0'. Direct algebra gives

    Q0-||rho||^2 = y'P[(n+1)^-1 I+I-P]y.

The first part is <=(n-1)/(n+1). For the second, use unscaled y=mu+Cepsilon and the PSD inequality for the sum of two vectors. Spectrally,

    mu'P(I-P)mu <= ||theta||^2/(n+1),
    epsilon'P(I-P)epsilon <= ||Proj_col(X0) epsilon||^2/4.

This proves the O_P(1+s0) bound with C and no eigenvalue floor. The part of epsilon perpendicular to col(X0), of dimension at least n-1-s0, also gives Q0 bounded below by a positive constant times n in probability, after scaling, uniformly since s0<=K-1 and E bounds s_y^2. Therefore the exponent multiplier is at least 1-O_P((1+s0)/n).

On zeta<=2log N the spherical-to-normal density ratio is exp(O((log N)^2/n)); normalization contributes only O(1/n). The two little-o hypotheses in the statement are precisely sufficient for this density error and the multiplier error. They allow polynomial p of any fixed degree, as well as some larger p. They constrain N, not necessarily p when the witness block is smaller.

All estimates above have constants controlled by the fixed energy/coefficient/noise bounds. In the spherical case common little-o envelopes are needed, as explicitly stated. The lower envelope N>=N_under ensures the empirical-sum concentration is uniform. Conditioning on random (X0,theta) with the same envelopes and adding the probability of the exceptional event proves the transfer, provided the conditional hypotheses (including the noise/null-block laws) really hold.

### A1, A2 and A3

A1 uses Lambda->0, guaranteed by either witness restriction for fixed s0 and all nulls. The map x/(1+x) then transfers the odds bound to delta; a fixed-epsilon high-probability lower bound also gives the liminf expectation claim without uniform integrability. A2 does **not** require Lambda->0: its valid delta bound is (1-o_P(1))*Lambda/[1+(1-o_P(1))*Lambda]. Consistency forces Lambda->0. If delta=O_P(r_n), then delta->0 and odds=O_P(r_n), so the necessary O(1) sparsity result follows when log p is comparable to log n. No improper linearization is needed in the large-Lambda regime.

Growing supports compatible with E and C exist: orthogonal truth coefficients 1/sqrt(s0) suffice, with p=n-1 and s0=o(p), for example s0=round(n^0.3). This also identifies the precise repair to F1.

For A3(i), all Gram submatrices are (n-1)I, so both floors hold, E holds for fixed s0 and fixed coefficients, and beta-min diverges. The truncation p=n-1 at a=1 preserves log p~log n. For (ii), Sigma=I satisfies both population floor conditions in the stated Corollary 1R, and conditioning on the truth block leaves independent Gaussian null columns. Fixed raw coefficients yield bounded standardized coefficients on the stated high-probability event. The expectation assertion explicitly retains the extra O(r_n) design-event requirement; it does not incorrectly infer an expectation rate from O_P alone.

## 4. B and C

### B: exact combinatorics and consequences

For j additions, multiplying the prior ratio by C(p-s0,j) gives exactly

    C(s0+j,j) product_{i=0}^{j-1} (p-s0-i)/(2p-1-s0-i).

Every fit factor is >=1 and every determinant factor is >=n^-j/2. The j=1 term is c/sqrt(n). If s0<=p/2 the fraction in c is >=1/3. Also c>=1 for s0>=1 follows equivalently from (s0-1)(p-s0-1)>=0; c(p,0)=p/(2p-1)>1/2. The ratio c/(s0+1) tends to 1/2 under s0/p->0. Empty truth is therefore covered correctly.

“Surely” in B1 is justified by a pointwise data bound. B2 follows because its deterministic floor must be O(rho_n) whenever delta=O_P(rho_n), rho_n->0; rearrangement gives s0+1=O(sqrt(n)rho_n). These are deterministic support-size sequences; random sizes would require probabilistic versions of the size conditions. B3's growing target s0=o(log n/log log n) lies in the small-Lambda range at log p comparable to log n. More generally the consistency obstruction follows directly from A2, and the scale sqrt(n) obstruction from B1. No claim of sufficiency follows from these necessary conditions.

### C.1: existence, exact representation, and ridge cost

At n>=200, k+2<=floor(n/2), so K=p and the k+1 orthogonal centered vectors exist. The normalization of x2 is exact. The displayed theta cancels the x1 component and produces b*u/sqrt(k). Its norm squared is b^2/(eta^2 k)*(1+c^-2), so the stated weaker lower bound and divergence of ||theta||^2/n follow from the signal lower bound. L1a_size_tail.md:10-19 has no hidden fixed-truth-size or eigenvalue assumption; T is deterministic, feasible, and exactly represents mu. Its coefficient restriction really is the missing hypothesis. The truth support T' growing with n does not violate that lemma.

For a model S, let d be the number of missing T' columns. If the x2 coefficient is v, projection onto those missing orthogonal coordinates gives the deterministic lower bound

    ||mu-X_S vartheta||^2 + ||vartheta||^2/n
      >= (n-1)d (b/sqrt(k)+c eta v)^2 + v^2/n.

Its minimum over v is

    [(n-1)d b^2/k] / [1+n(n-1)d c^2 eta^2].

This also bounds models without x2 by allowing an extra free variable. The denominator is <2 for d<=k and n>=200. This argument retains the enormous coefficient penalty: using x2 with a huge coefficient does not provide a cheap fit.

For T, d=k, yielding min B_T>=b^2(n-1)/2; taking vartheta=0 gives the upper bound b^2(n-1). For T', exact fit gives B=b^2. Independent 70-digit minimization gives min B_T/(b^2(n-1)) equal to 0.9992046264 at n=200 and 0.999999999917 at n=10^6. The numerical values are supplementary; the inequality above establishes the bound for the whole sequence.

### C.2: finite-n cutoffs

For p=k+2, the first q ratio is p/(2p-1)<=2/3 and each subsequent ratio is <=1/2. Thus R_m<=4p^2 2^-m is a valid loose envelope. With p<=12log n+3 and m=floor(k/2)>=6log n-1/2,

    n^2 R_m <= 4 sqrt(2) (12log n+3)^2 n^(2-6log 2) < 1

at n=200. Its logarithmic derivative is 24/(12log n+3)+2-6log 2<0 thereafter. This proves the finite-n bound, not merely an asymptotic version. Since t=2, the cutoff threshold is exactly n^-2.

The cancellation-free Schur expressions in c_counter.py give D_T<=4n on this domain (indeed it is close to n), so A_m<=2/n<=n^-1/2. The independent integer scan finds max n^2 R_m=0.0005192843124421544 at n=225; the maximum need not occur at 200 because of the ceiling/floor steps.

### C.3: uniform noisy fit gap and constants

Let A0=sigma^2+bbar^2 and let P_X project onto the full design span, of rank k+1. For |S|<=floor(k/2), d>=k/2, and the preceding deterministic loss is at least b^2(n-1)/4. Splitting off the noise perpendicular to the full span and applying ||a+e||^2>=||a||^2/2-||e||^2 gives simultaneously for all such S

    s_y^2 Q_S >= ||Cepsilon||^2 - 2||P_X epsilon||^2 + b^2(n-1)/8.

The reference T' obeys s_y^2 Q_T'<=||Cepsilon||^2+b^2. Since ||P_X epsilon||^2=O_P(log n) and nb^2>=1200 A0 log^2 n, the gap is at least nb^2/10 with probability tending to one, uniformly in S. Also

    s_y^2(2b0+Q_S) <= (1+2b0/(n-1)) ||mu+Cepsilon||^2 <= 2n A0

with probability tending to one. Hence the likelihood-factor ratio m(S)/m(T'), apart from determinants, is at most exp(-nb^2/(40A0)), using log(1-x)<=-x and nu>=n/2.

D_T'=n^k and D_S>=1. Every prior ratio is bounded by C(2p-1,k), and there are at most 2^p models. Their combined logarithmic overhead is at most

    (k/2)log n + log C(2p-1,k) + p log 2
      = (6+o(1))log^2 n <= 7log^2 n

eventually. Since 7/1200<1/80, the resulting posterior sum is bounded by exp(-nb^2/(80A0)) eventually on the high-probability event. Thus even c1=1/(80A0) is available with these loose bounds. This verifies that 1200 is sufficient, including shrinking b_n, without hiding a union bound over exponentially many noisy projections.

The cutoff conclusions and divergence of both normalized tail variables follow because the relevant deterministic normalizations vanish while the actual tail tends to one. This contradicts the fixed-cost/coefficient-free proposed versions, not the actual parent lemmas. For any envelope B_n/log^2 n->infinity, one can choose nb_n^2 proportional to A0 log^2 n eventually, keeping b_n<=bbar and min B_T<=B_n. Thus the final “cannot be weakened” assertion has the required existential counterexample for each such envelope.

## 5. Numerical audit and limits

- The orthogonal sufficient-statistic reduction is exact in law. The Gamma identity and elementary-symmetric recursion are correct. The computed integral is numerical quadrature over a finite interval; large runs additionally omit sizes above s0+60. The source's lines 13-14 and 37-40 disclose both limitations. “Exact” should be understood as an exact target/formula evaluated numerically, not a certified error enclosure. Omission of positive terms gives a mathematical lower bound before quadrature error; floating-point output is not a rigorous lower-bound certificate. I found no substantive discrepancy in the checks. Independent V1's worst relative discrepancy was 1.50e-13.
- The supplied V2 output compares all sizes and increased truncation/quadrature, with discrepancies up to 2.2e-11. It is useful validation at those draws, not a global truncation-error theorem. Small medians below 1 and nonmonotone empirical probabilities do not refute an asymptotic high-probability lower bound with slow logarithmic concentration. The orthogonal output was still partial when read; no unprinted E2 results were assumed.
- The spherical reduction uses an orthonormal basis of span(X0,rho), dimension s0+1 almost surely for its Gaussian truth-block experiments. Its remaining chi-square degrees of freedom n-2-s0 are correct. R0 compares independent samples, not identical coupled draws, so it is a distributional diagnostic only. Independently rerunning V1 gave maximum relative discrepancy 1.5e-13. The reduction does not purport to handle every rank-deficient deterministic truth block in A; the mathematical proof does.
- The structured C enumeration includes every subset in the configured small-k problems, handles the cap through zero weights, and uses the correct Schur complements. The stable “11” formulas retain the small residual terms which direct subtraction would lose. My rerun gave 2.3e-13 error for the float comparison and 1.4e-15 for the 60-digit comparison. The posterior simulations use k=16..22, not ceil(12log n), and do not satisfy the theorem's large signal constant; the source explicitly discloses the k change. They demonstrate the mechanism, not a finite-n verification of every theorem hypothesis. C's separate cutoff calculation does use the stated k.
- The supplied B output distinguishes equality for superset odds from equality for all odds when s0>0; this distinction is correct. My independent F1 rerun covered 8,064 pairs with determinant-formula error 8.9e-13 and fit error 1.6e-14, including degenerate designs. The supplied F2 reports 55,740 cases and no violation; I read its enumeration logic and output but did not rerun F2.
- F1 and F2 above are the two substantive evidence defects. The rest of the numerical validation supports the formulas within its stated finite scope and does not replace their proofs.

## 6. PROPOSAL: stronger records at comparable cost

### PROPOSAL P1 — Exponential cap from B at the critical sparsity scale

Assume s0/sqrt(n)->lambda in (0,infinity), s0/p->0, and the same feasibility conditions. Then, deterministically and uniformly in design/data,

    limsup pi(S0) <= exp(-lambda/2).

For every fixed j, B's jth summand tends to (lambda/2)^j/j!. Since K-s0->infinity, keep the first J terms, pass to the limit, then let J->infinity. This gives liminf O_lb>=exp(lambda/2)-1. No exchange of infinite sums and limits, nor an upper bound on O_lb, is required. This strictly improves the first-term critical-scale cap 1/(1+lambda/2), and much more strongly the stated 1/(1+lambda/3). It is already latent in B's finite sum and costs only this paragraph to state and prove. The existing table is consistent with it.

### PROPOSAL P2 — Replace spherical support-size restriction by truth-block rank

In W-sph replace (s0+1)log N=o(n) by (rank(X0)+1)log N=o(n), retaining the other hypotheses, including s0+1<=K, E and C. The proof in section 3 gives Q0-||rho||^2=O_P(1+rank(X0)), because the noise term is bounded by a chi-square variable of that rank, and the signal term is bounded directly by C. The perpendicular-noise lower bound is also at least as strong. The conditional sphere law and all prior factors remain unchanged. Uniformity requires a common rank-based little-o envelope.

This is strictly wider: a large truth support of repeated columns with appropriately small nonzero coefficients can have fixed rank and bounded energy/coefficient norm. Such designs are permitted by A even though they are not examples for the upper-bound theorem A3. The proposed improvement does not claim concentration on those nonidentifiable supports; it strengthens only the lower-bound witness class.
