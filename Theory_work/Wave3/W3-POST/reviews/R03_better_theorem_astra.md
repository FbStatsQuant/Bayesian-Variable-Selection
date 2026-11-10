# R03 — Better-theorem proposals for W3-POST

Fresh research review; 2026-11-09. Scope: stronger statements and bounded proof extensions, not a correctness review. All proposals retain the coded capped BB(1,p) prior, ridge score, standardisation and IG(0.01,0.01). Statements below are asymptotic and use interfaces on the design and signal. Examples are diagnostics, not design-family assumptions in the proposed main theorem. “Low risk” means a short derivation remains to be written, not that the statement is already proved.

References: P1 and P3 are the locked PROOF_v3.tex and PROOF_v2.tex named in STATEMENT.md; C1–C10 refer to W1-T03R/PROOF.md §6; POST refers to W2-APP/lemmas/L1_POST.md. I read these sources and the new size-tail proof. No external literature is needed for the proposals below.

## Recommended order by value for cost

1. Replace the logarithmic-size eigenvalue floor by a determinant-ratio interface (§2A); combine with a signal-visibility interface instead of the bounded-size normalised floor (§2B).
2. Strengthen Lemma 1a′ to bounded penalised approximation and retain the exact reference determinant (§6A).
3. Broaden the random-design bridge to sub-Gaussian coordinates; for Gaussian rows dramatically weaken the population floor by using relative, rather than entrywise additive, covariance concentration (§4A).
4. Add expectation rates and explicit uniformity over designs (§6B). These have direct consequences for error probabilities.
5. Reduce the beta-min constant without changing the proof architecture (§1B).
6. Extend beyond polynomial p, initially with an honest stronger beta-min condition (§3).
7. Allow slowly growing sparsity (§4B).

Do not advertise specificity without beta-min under AF alone: §5 gives a positive-floor counterexample mechanism. Do not advertise log p = o(n) or arbitrary non-Gaussian noise from this proof chain.

## 1. Beta-min: order, constants, and the attainable improvement

### A. Sharp orthogonal benchmark

Let s0 be fixed and consider a true coordinate orthogonal to the other columns, with N = n−1 and lambda_j = N theta_j²/sigma² = O(log n). The odds for retaining it against deleting it have expansion

    log[ell(S0)/ell(S0\{j})]
      = (sqrt(lambda_j) + Z_j)²/2 − log(2p/s0) − (log n)/2 + O_P(1),

with Z_j standard normal; changing 2p/s0 to the exact prior ratio only changes the bounded term. Response standardisation and the fixed IG hyperparameters do not alter these leading logarithmic terms. For polynomial p the residual-variance Taylor remainder is negligible here.

Consequently, if log p / log n → a, the sharp leading constant for retaining a fixed true coordinate is

    n theta_min²/(sigma² log n) > 2a + 1,

with a fixed positive margin. Below 2a+1, the deletion odds diverge. At equality, the Gaussian cross term is of order sqrt(log n), so equality is not a consistency condition. More generally the transition is around 2 log p + log n, with a diverging margin on the square-root noncentrality scale.

For the stated RATE delta_n = O_P(sqrt(log n/n)), the deletion contribution requires the stronger leading constant c > 2a+2. Indeed its size is n^{a+1/2−c/2+o_P(1)}. Consistency and the advertised rate have different signal thresholds. Orthogonal arrays have p ≤ n−1; this is a sharp benchmark there, not a claimed orthogonal construction at p ≫ n. A coordinate orthogonal to a large null dictionary still gives the same necessary deletion comparison in the overcomplete regime.

**Improved statement:** distinguish consistency beta-min from rate beta-min; present 2 log p + log n as the method's unavoidable deletion threshold. No uniform o(sqrt(log n/n)) beta-min theorem is possible for this prior, even for fixed p.

**Changed step:** expand P3 eq:score for a one-coordinate deletion instead of using lem:signalgain. To obtain a complete orthogonal posterior theorem, also control the null additions using the existing truncated-moment summation.

**Risk:** low for the benchmark and lower obstruction; medium for a sharp full posterior theorem. **False alternative:** replacing the rate by o(sqrt(log n/n)) uniformly is false by the deletion odds above. A universal sharp constant depending only on phi0 cannot be read off this benchmark: replacement-model geometry also matters.

### B. A concrete smaller sufficient constant under the current assumptions

Keep C_* and j0 as presently defined. A bounded-work replacement for c0 is

    c_new = (sqrt(C_*) + sqrt(2(A+1)))².

Conjectured improved theorem: all rate conclusions of Theorem 1 hold for any fixed c > c_new. One may use min(c0,c_new) to guarantee the statement only enlarges the admitted class. In the present parameter range this meaningfully reduces the existing conservative constant.

**Proof sketch / changed steps:** In C7 and C10, retain a = |S0\S| and Delta_S ≥ a c sigma² log n. Keep

    V_S ≥ sigma² log n (sqrt(a c) − sqrt(C_*))²
        ≥ a sigma² log n (sqrt(c) − sqrt(C_*))².

In P3 lem:SvsSp retain its FIRST displayed inequality. At V of logarithmic size its exponent is (1−o(1))V/(2sigma²), rather than V/(8sigma²); larger V only strengthens this monotone bound. Retain the prior/determinant penalty a(A+1/2)log n + O(a). The strict inequality c > c_new then makes kappa_n = O(n^{−1/2−eta}) for some eta > 0. C8 needs only o(r_n), not the existing n^{−2}. All other terms remain as before.

**Risk:** low–medium. **False instead?** No counterexample to this sufficient constant identified. It is not sharp: C_* is of order A j0, hence roughly A²s0. Reaching O(A) uniformly would require replacing the maximum over all small underfits in C8 by a weighted testing/summation argument. That is plausible, but I do not nominate an exact O(A) constant under AF as a bounded-work theorem. The easy constant improvement should not be sold as resolving that question.

## 2. Floor set sizes and masking

### A. Replace SE_w by the quantity actually used

**Improved statement:** retain the other hypotheses but replace F_w by

    DG(c_D): D_(S0∪J)/D_S0 ≥ [c_D(n+1)]^{|J|}
             for 1 ≤ |J| ≤ m♯_n,

where c_D > 0 is fixed. Then all conclusions of Theorem 1 still hold. DG is a geometric-mean condition on the coded determinant ratio, not on det(G) alone. A sufficient spectral version uses the product of f(lambda_i), f(x)=((n+1)x+1)/(x+1), of the |J| smallest eigenvalues of G_(S0∪J). Raw det(G) can be inflated by large eigenvalues and is not the appropriate substitute.

**Changed steps:** C4 uses DG directly for the determinant penalty. C5 replaces 1+1/g0 by c_D^{-1}. No lower eigenvalue of the large superset is used in its smoother upper bound: the floor on S0 suffices. If the union is singular, its projection increment has rank d ≤ j. Replace the truncated random variable exp(chi²/2)1{chi²≤tau_j} by exp(min(chi²,tau_j)/2). This is increasing and admits stochastic domination by rank j. Its expectation is bounded by (C tau_j/j)^{j/2}; the additional endpoint tail has the same or smaller order. Thus neither exact rank j nor full rank is essential. C2/G3 uses rank domination, and C8 is unchanged.

DG follows from F_w with c_D=g0/(1+g0), but permits individual eigenvalues to deteriorate with j. It can even permit some rank loss at logarithmic j if the determinant product still clears the threshold. Small sets remain controlled by F_lambda in this first version.

**Risk:** low. **False instead?** No; this is essentially the unused route identified in T03R §7, with the rank issue explicitly removed. Removing BOTH determinant control and all replacement complexity control is not justified. The current bounded-size floor alone does not automatically imply DG at logarithmic sizes.

### B. Replace the normalised small-set floor by signal visibility

**Improved statement:** retain E, the normalised floor on S0 itself, and F_w. Replace F_lambda on other unions by

    VIS(phi): ||(I−P_S)mu||² ≥ N phi² ||theta*_(S0\S)||²

for every underfit S of size ≤ m♯_n with |S\S0| ≤ j0. Use phi in BM. This is strictly weaker as a condition on (X,theta*): it controls only masking of the actual missing signal. A signal-independent version asks for the corresponding residual Gram lower bound on missing truth coefficients, not on null-only directions.

**Changed steps:** C7/lem:signal becomes the VIS assumption. In C3 and C6(b), F_w supplies a lower bound g0 for the relevant nonzero eigenvalues, so

    0 ≤ nP_T/(n+1) − M_T ≤ C/n · P_T.

The correction on ||y_c||²=O(n) is now O(1), instead of o(1). Likewise Q_S ≤ RSS_S + O(||y_c||²/n). This changes rho_n to a bounded constant, and E_n by O(1), harmless against log n signal gaps. Rank domination handles the noise projection bounds. C4–C5 still use the normalised floor on S0 and F_w.

One can combine this with DG, but then explicitly retain an O(1/n) smoother-defect bound on the small comparison unions used by C3/C6. DG alone should not silently substitute for this bound.

**Risk:** medium, a short rewrite of the ridge-comparison lemmas. **False instead?** No counterexample with these interfaces. The claim that normalised conditioning is required in null-only directions is too strong. Conversely, removing VIS as well is false: an almost duplicate of a truth column can make its label unidentifiable.

### C. Can F_w be deleted entirely given F_lambda(j0)?

I do not nominate this as proved or as a low-cost theorem. Small-set restricted floors do not imply conditioning at logarithmic size: collections can have a linear dependence whose minimal support exceeds j0. But this observation alone is NOT a posterior inconsistency counterexample. Such a dependence can also carry substantial prior and determinant penalties. Proving deletion of F_w would require a new rank/entropy counting argument for dependent supersets and their underfits. **Risk: high; truth unresolved here.** DG and VIS are the defensible deliverables.

## 3. Beyond polynomial dimension

**Concrete conservative improved statement:** let s0 stay fixed and L_n=log(2p)+log n. Permit L_n=o(n^{1/3}). Keep E, the normalised anchored floor through j_n, and the unnormalised floor through m♯_n, where m♯_n=O(L_n). Choose j_n large enough that

    p^{s0} n^{s0/2} (j_n+2)^{s0} [C sqrt(L_n/n)]^{j_n+1}
        = o(sqrt(L_n/n)).

This is a deterministic explicit interface; for example a sufficiently large constant multiple of

    [s0 log(2p)+(s0+2)log n] / log(n/L_n)

works. Assume n phi0² theta_min²/sigma² ≥ C_B(j_n L_n + log n), with sufficiently large fixed C_B depending on s0. Then propose

    1−pi(S0) = O_P(sqrt(L_n/n)).

This contains the polynomial range and also log p=log n times arbitrary fixed polylog factors. It allows much larger p, but honestly pays a stronger signal condition than sqrt(log p/n) when j_n diverges.

**Changed steps:** C1 and C9 give m♯=O(L_n) without using p≤n^A. Replace all C_A log n thresholds in P3 G2/G3 by C L_n. Then delta_n=O(sqrt(log n/n)+m♯L_n/n), and epsilon_n=O(L_n sqrt(log n/n)+m♯L_n²/n)=o(1) under L_n=o(n^{1/3}). C5 gives q_n=O(sqrt(L_n/n)). Keep the j_n dependence in K_(s0,j_n)=O((j_n+2)^{s0}), and impose the displayed tail condition in C8. G4 costs O(j_n log p+log n), so C10 requires the stated stronger beta-min. The size-tail remains O_P(n^{−1/2}).

**Risk:** medium. **False instead?** No obstruction to this conservative extension identified. The statement “replace log n by log p everywhere and retain beta-min sqrt(log p/n)” does NOT follow: the moving G4 union bound costs j_n log p. Getting that sharper signal scale needs a new weighted-underfit argument. Log p=o(n) also exceeds the current epsilon_n calculation; it is not a bounded bookkeeping extension. For log p comparable to n, even a one-coordinate unknown-variance likelihood gain is no longer its quadratic local approximation. I do not claim impossibility for all log p=o(n), only that this chain does not establish it cheaply.

## 4. Growing sparsity and non-Gaussian extensions

### A. Random-design bridge

**Improved interface statement:** any random design law for which E, BM and the chosen deterministic interfaces hold with probability tending to one inherits the fixed-design conclusion, uniformly with common constants. The main theorem need not name a row distribution.

Two concrete stronger sufficient bridges:

1. Independent rows with centred, unit-variance coordinates having uniformly bounded sub-Gaussian norms satisfy the existing POST entrywise event. Coordinates within a row may be dependent. With the same LSF thresholds as POST, all its conclusions follow. Change only POST step (2): products are sub-exponential, apply Bernstein plus a union bound, also controlling sample means and variances. Steps (3)–(5) are unchanged. **Risk: low. False instead?** No, with the uniform norm and independence assumptions stated; merely finite variance is insufficient for this union-bound bridge.

2. For Gaussian rows, replace POST LSF(ii)'s condition psi_n sqrt(n)/(log n)^{3/2}→infinity by n psi_n≥C for a sufficiently large fixed C. Require floors only on the anchored unions actually used. For each such support T, whiten its population covariance and use the lower singular-value bound for its centred Gaussian sample matrix. A net/chi-square proof gives simultaneous relative covariance control when k log p=o(n), where k=O(log n) here. Thus sample covariance ≥(1−o(1))Sigma_T, and uniform diagonal concentration transfers this to sample correlations. Choose C so the unnormalised sample floor exceeds g0. No global population upper eigenvalue bound is needed. Change POST steps (2)–(3); other steps survive. **Risk: low–medium. False instead?** No for Gaussian rows; for general coordinatewise sub-Gaussian rows the whitened sub-Gaussian norm need not be uniform as psi_n→0, so do not extend this stronger bridge without that additional assumption.

These are bridge propositions to the design-interface theorem, not new main theorems restricted to a named design family.

### B. Slowly growing s0

**Conservative improved statement:** for p≤n^A, allow s=s_n→infinity with s=o(log n/log log n), fixed energy and floor constants, j_n=ceil((2A+3)s)+2, and F_w through the exact cutoff m♯=O(s log n). Assume

    n phi0² theta_min²/sigma² ≥ C_A' s log n

with a sufficiently large fixed C_A'. Then propose delta_n=O_P((s+1)sqrt(log n/n)), hence exact posterior selection. This is deliberately modest; it is a bounded-work growing-sparsity theorem, not a claim of an optimal range.

**Changed steps:** use L1a′ for the growing reference size; its coefficient-cost bound is uniform under the truth floor and E. In C5 retain the exact binomial prior bound and use

    sum_(j≥1) binom(s+j,j) q^j = (1−q)^{−s−1}−1 = O(sq)

when sq→0. Do not use K_(s,0) as an unexplained constant. Track 2^s, K_(s,j_n), and all floor ranges in C8. Their logs are O(s log(s+1)); the extra margin in j_n absorbs them since log s=o(log n). G4 has C_*=O_A(s), so the stated beta-min handles C10 and the factor 2^s. The residual expansion requires s log³n/n→0, satisfied by the nominated regime.

**Risk:** medium. **False instead?** No counterexample identified under these assumptions. Keeping fixed nonzero coefficients, a uniform truth floor and E while s→infinity is impossible: E bounds ||theta*||². A growing-sparsity extension must allow shrinking coefficients. Keeping the original rate independent of s is also not a reasonable generic promise: the prior's one-addition multiplicity is proportional to s+1.

### C. Replacing Gaussian noise

I do not recommend an unrestricted “sub-Gaussian noise” theorem with the same score and constants. P1 lem:num uses the true density, and P3 lem:chi(b) uses the critical truncated exponential moment, not just a concentration inequality. Both need replacement.

A bounded-work candidate is asymptotically Gaussian noise in total variation on the centred contrast vector: if its law is at TV distance o(1) from N(0,sigma²I), every O_P conclusion transfers unchanged. This is mathematically stronger but practically limited. **Risk: low; no counterexample with this TV premise.** For general independent non-Gaussian noise, a useful theorem requires uniform projection moderate deviations and a replacement size-tail argument. **Risk: high.** Finite variance alone is not enough: with high-leverage columns and heavy-tailed errors, isolated extreme observations can create large spurious score gains. No claim here that Gaussianity itself is necessary.

## 5. Specificity without beta-min

### A. AF alone: a counterexample mechanism even with a fixed positive floor

Take three centred, standardised columns with x1,x2 orthogonal and

    x3 = r(x1+x2)/sqrt(2) + sqrt(1−r²)u,

where u has the same norm and is orthogonal to x1,x2. Let S0={1,2}, theta1=theta2=b sqrt(log n/n), sigma²=1. Put r²=0.9. The three-column normalised Gram has minimum eigenvalue 1−r>0.

First take p=3 and L=1/2; alternatively embed the block in a polynomial-size null dictionary with log p/log n→a and put L=a+1/2. Choose b²=1.5L. To leading order in log n, log posterior weight relative to the empty model equals explained signal energy divided by 2, minus L per selected coordinate:

    {1} or {2}:       b²/2 − L = −0.25L;
    {1,2}:           b² − 2L = −0.5L;
    {3}:             r²b² − L = 0.35L.

The fitted signal fraction for {1,3} or {2,3} is 1/(2−r²), giving score coefficient b²/(2−r²)−2L < 0. The full triple also loses. All gaps are order log n and stochastic fluctuations are order sqrt(log n). Thus for p=3, pi({3})→1 and PIP_3→1, although both AF floors hold. This finite-dictionary construction alone disproves the universal specificity claim in R1.

For p≫n the same block can be embedded with the remaining columns in its orthogonal complement, choosing a deterministic dictionary with uniform floors on O(log n) supports; probabilistic constructions establish existence for any fixed polynomial p. The null-addition sums are controlled by the same truncated-moment calculation. Completing this embedding is additional work, not needed for the R1 counterexample. The phenomenon is compression of several weak signals by one proxy, not a nearly singular Gram matrix.

**Risk:** low for the p=3 asymptotic counterexample; medium for the overcomplete embedding. **Verdict:** specificity under AF without beta-min is false.

### B. A sufficient interface under which specificity is recoverable

**Improved statement:** under the existing floors, E, fixed s0 and Gaussian noise, impose the block-orthogonality interface X_(S0)^T X_(S0^c)=0. Without any beta-min, propose

    pi(S\S0 != empty) = O_P(r_n),

which implies max_null PIP→0 and is stronger than merely ruling out strict supersets of S0.

**Changed steps:** partition models by T=S∩S0 and compare T∪J to T, rather than to S0. Block orthogonality makes determinant ratios and smoother increments for J independent of T, and the increment contains pure noise. Residual signal from omitted truths only raises the denominator; the existing good-event residual lower bound remains valid. Apply C4–C5 uniformly over the at most 2^{s0} subsets T, and divide by the sum of all truth-subset weights. Large models use L1a′. Small T inherit the truth floor. **Risk: medium. False instead?** No counterexample under this interface; relaxing it to nonzero leakage needs a quantitative score-gain condition that excludes the proxy example above.

## 6. Other stronger conclusions

### A. Lemma 1a′ with approximate references and the exact determinant

**Improved statement:** let a deterministic reference T∈Omega satisfy, for some theta,

    ||mu−X_T theta||² + (||X_T theta||²+||theta||²)/n ≤ B,

with B fixed, and retain ||mu||²≤nM. Exact representation is unnecessary. Define

    A_(T,m) = [sum_(k>m) q_k / w(|T|)] sqrt(D_T) sqrt(n).

Then pi(|S|>m)=O_P(A_(T,m)), uniformly over all such references and designs, for arbitrary p and |T|≤K. In particular any deterministic cutoff with A_(T,m)≤exp(−omega_n) has tail O_P(exp(−omega_n)). Choose the best admissible deterministic reference if several exist. This improves both the reference class and the (n+1)^{|T|/2} normalisation.

**Changed step:** in L1a′'s variational bound put r=mu−X_T theta. Then

    Q_T^c ≤ ||e||² + 2e^T r + B.

Use B+2|e^T r| as the nonnegative excess. Since ||r||²≤B, this excess has uniformly bounded moments and exponential moments. P1 lem:den's integral argument still works. Retain sqrt(D_T) rather than replacing it by (n+1)^{|T|/2}. P1 lem:num and T03R's exact prior tail are unchanged. Choosing references uses only (X,mu), never the response/noise.

**Risk:** low. **False instead?** No. Allowing an unbounded approximation/penalty cost while keeping the same normalisation is not justified; an exponential cost factor would generally enter. A rank-r reference has D_T≤(n+1)^r, which gives a useful effective-rank refinement automatically.

### B. Expectation rates with the present cutoff

**Improved statement:** under Theorem 1's existing hypotheses and beta-min, for every fixed 0<q<1,

    E[1−pi(S0)] = O(n^{−q/2}).

Consequently HPM and MPM error probabilities, and expected maximum PIP error, obey the same rate. The statement is uniform over designs with common constants and a common strict beta-min margin.

**Changed steps:** in L1a′ use the truth floor and E to obtain a uniform bounded coefficient cost. Its denominator variable Lambda has E exp(t Lambda)=O(1) for every fixed t, for all sufficiently large n: this follows directly from the chi-square MGF and the bounded deterministic cost. On the scale event, write tail ≤ min(1,a e^Lambda Z), with a=O(n^{−1/2}) and E Z=1. Holder gives

    E min(1,a e^Lambda Z)
      ≤ a^q (E exp(q Lambda/(1−q)))^{1−q} (E Z)^q
      = O(n^{−q/2}).

Add the O(1/n) scale-event failure. C5 and C8 already provide expectation bounds for the truncated small-model contributions; the good-event complement costs O(1/n). These terms are O(r_n)+O(n^{−1}polylog(n)) and hence smaller than n^{−q/2}. No independence between Z and Lambda is assumed.

**Risk:** low. **False instead?** No identified obstruction. E delta=O(r_n) is a worthwhile further target but does not follow from tightness or this Holder argument; I do not claim it here.

### C. Predictive/Hellinger and uniformity

**Improved statement:** under the existing fixed-s0 theorem, the posterior contracts for the in-sample mean at the oracle n^{−1/2} scale: for every M_n→infinity,

    Pi(||X beta−mu||/sqrt(n) > M_n/sqrt(n) | data) → 0

in probability, with coefficients and variance interpreted on the original centred-response scale. Analogously the average squared Hellinger distance between the fitted one-observation Gaussian laws and the true laws contracts at order 1/n, with a diverging multiplier. This is an in-sample average, not joint n-observation Hellinger convergence or unrestricted out-of-sample prediction.

**Changed step:** after model selection, condition on S0 and compute the conjugate Gaussian/IG posterior. The truth floor and bounded energy give O_P(1) total fitted-mean squared error and variance estimation error O_P(n^{−1/2}). Bound the full posterior bad-event probability by delta_n plus the conditional-on-S0 probability. Undo response scaling and account for the contrast-space variance convention. A posterior expected unbounded loss is NOT implied merely by small wrong-model mass.

**Risk:** medium, mostly parameter-scale bookkeeping. **False instead?** Out-of-sample prediction uniformly over unconstrained new covariates, or Hellinger convergence of the full n-fold experiment at this scale, would be false without additional qualifications.

Finally, explicitly state uniform O_P bounds over the admissible (X,theta*) class with common constants and strict c>c0, or a common divergent BM envelope. POST step (5) already explains the sequential-to-uniform argument. This costs almost nothing, makes the random-design bridge transparent, and avoids an unjustified uniform claim over arbitrarily slow divergent BM sequences.
