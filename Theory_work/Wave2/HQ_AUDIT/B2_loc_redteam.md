# HOLDS-WITH-AMENDMENTS

Independent adversarial review of W2-APP, STATEMENT v1.3.1, 2026-11-09.

**Disposition:** the four headline mathematical claims survive this review under their stated sampling assumptions and named proof/implementation inputs. No FATAL or MAJOR finding. One MINOR amendment is needed to synchronise the family map's summary table. No change to POST, LOC/LOC-B, VN/STAR, or ENUM is required by this review. Numerical checks below are falsification attempts, not proofs or production-run validation.

## Findings and exact fixes

### MINOR M1 — the final family-map table still says FAC is pending

**Locations:** `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:167` and `:168`.

Both summary rows retain `per FAC (pending)`, contradicting this file's own qualified FAC-A status at `:149` and the corresponding updated table in `Theory_work/Wave2/W2-APP/REPORT.md:78`. A reader using the summary alone gets an obsolete reported-model frontier. This is an internal status inconsistency; I have not independently audited FAC-A here.

**Exact fixes, confined to the Reported model cells:**

- At L4 `:167`, replace `**per FAC (pending)**` with `FAC-A under the narrowed hypotheses in (g); ENUM when (EXB) holds eventually; otherwise open`.
- At L4 `:168`, replace `per FAC (pending) / LOC if local` with `FAC-A under the narrowed hypotheses in (g3); LOC if local + PTV; ENUM when (EXB) holds eventually; otherwise open`.

No other correctness finding. In particular, none of the attack points below warrants adding a partition-recovery assumption, an upper spectral bound to POST, or a global union bound over all models.

## 1. POST: sparse floors, growing p, and transfer to the joint law

**Audited:** `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:20`–`:69`, against the actual T03-sharp hypotheses in `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:5`–`:13`.

The tail-cutoff argument is conservative but valid. For p >= 2,

    C(p,k)/C(2p-1,k) <= (2/3)^k,
    R_m <= 2(2p)^s0 (2/3)^m.

Thus the displayed m-bar is O(log n) and dominates the actual m-sharp. The extra s0 in k-bar is needed because the eigenvalue hypotheses concern S0 union J, rather than J alone; it is present. If m-bar exceeds K, the zero tail at K handles the truncation.

The potentially dangerous uniformity is handled correctly. On one event controlling every sample correlation entry, every submatrix of size k <= k-bar has error at most k times the maximum entry error. Consequently the required bound is O((log n)^(3/2)/sqrt(n)), simultaneously over all such subsets. There is **no union bound over 2^p sets** in this step, and no assertion that a p-by-p sample Gram matrix has a positive minimum eigenvalue when p > n. Only logarithmic-size submatrices are used. LSF(ii)'s explicit rate makes this error o(psi_n).

Neither concentration of individual Gaussian products nor the energy bound needs lambda-max(Sigma_n). Gaussian products have uniformly controlled tails because individual population variances are one. The signal uses only s0 fixed coordinates, so its energy is bounded by s0^2 theta-hi^2 n regardless of the full spectral norm. A floor for the **correlation** matrix is essential; a raw covariance idiosyncratic floor with unbounded marginal variances is not sufficient. L1 `:71`–`:77` already makes this distinction.

The joint-law claim is stronger than pointwise conditional convergence, but the proof supplies the needed quantifiers. All deterministic sequences selected from the design events satisfy T03-sharp with the same constants and deterministic beta-min envelope. If conditional tightness were not uniform, a subsequence with thresholds tending to infinity could be selected and completed into a deterministic sequence, contradicting T03-sharp. This validates L1 `:58`–`:68`; it is not an interchange of a pointwise limit and a supremum. Under the standardised-signal convention, the conditional noise law depends only on X, as required. The separate raw-slope paragraph correctly uses raw-design sequences when the coefficients depend on sample scales.

**Result:** POST holds as stated, conditional on the cited fixed-design T03-sharp theorem. This audit checks its applicability and transfer, not a new proof of T03-sharp itself. A fixed positive sparse floor is sufficient; the actual LSF(ii) statement also allows a shrinking logarithmic-size floor at its specified rate.

## 2. LOC: partition selection, the constant 15, and the sandwich

**Audited:** `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:25`–`:96`, including the inherited argument in `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:169`–`:389`.

The partition does enter the start law and the proof through block-table optimality. What is unnecessary is an additional hypothesis about *which* columns the partition groups together. The uniform statements range over all l and all U of size at most 15. Therefore they apply to U equal to the selected part of any block, even when the partition is chosen from X. The score toolkit covers every subset of size at most 16 before a random block is used. Its number of sets is polynomial in n because the exponent 16 is fixed.

PTV has exactly the right quantifier for the truth-addition step: U may include other truths, and only j itself is excluded (`L3_LOC.md:28`). It does not merely quantify over null conditioning sets. When an absent truth j is added to a block of size at most 16, its current conditioning set has at most 15 members. Cancellation after conditioning on more than 15 variables is irrelevant to this step. Later, TL protects truths in the entire logarithmic-size lattice using Gram floors and beta-min, not PTV on that larger lattice.

The inherited sandwich argument does not silently assume that a maximiser is small. Its global size ladder first bounds *every* maximiser by 2(q+16s0), including maximisers at the cardinality cap. The ladder uses per-block removal and counts of large far-null statistics. Only then are missing truths added, with feasibility supplied by the enlargement rule. Finally the far-null tail makes deletion of every selected l outside Q profitable. See inherited L6 `:329`–`:388`. All conditioning sets used in these block-table increments still have size at most 15.

For the selection-removal step, exponential conditional covariance decay makes a variable outside the deterministic neighbourhood essentially irrelevant to both the candidate l and the response signal. The neighbourhood includes both l and the truths, not merely l. This is necessary to bound both vectors in the recursive partial-correlation formula. The stated H_l has that property (`L3_LOC.md:75`–`:83`). Its size is O(log n) under any permitted ordering, so the reference sets number only polylogarithmically per l. The spherical-tail conditioning is also legitimate: condition on W_(U0 union S0) and the noise, which fixes the response including its sample-scale signal coefficients. The candidate's population innovation remains independent. The proof does not condition on the common concentration event and then falsely retain a spherical law.

**Result:** no hidden partition-containment or recovery assumption found. The constant 15 is tied to the algorithmic block cap 16, not to the size of a population covariance component. Population blocks of any fixed size, including sizes larger than 16, are therefore allowed. If the method's block cap were increased to B, this proof would need PTV through B-1, together with the corresponding bounded-size uniform estimates.

### A sharpness control for 15 (not a counterexample to the stated theorem)

Let Z1,...,Z16,E0,E1 be independent standard normals and define

    Wj = (E0 + (1/4) sum Zi)/sqrt(2),
    Wk = (-E0 + E1 + (1/4) sum Zi)/sqrt(3),
    theta_j = sqrt(2), theta_k = sqrt(3).

These 18 variables form a fixed, positive-definite correlation matrix with minimum eigenvalue 0.087129071. They constitute one bounded population component, hence a LOC design after consecutive ordering. The signal is E1 + (1/2) sum Zi. Conditioning on u nulls without the other truth gives

    Cov(Wj, signal | u nulls) = (16-u)/(8 sqrt(2)).

Checking both truths and the cases with the other truth conditioned upon gives minimum absolute covariance 0.088388348 over **all** U of size at most 15, using exchangeability. Yet conditioning on all 16 nulls makes the covariance for truth j exactly zero (computed residual -2.22e-16). Thus the 15-variable premise cannot simply be carried unchanged to a 17-column method block. It does suffice for the current 16-column cap. This control also shows why a population component larger than 16 does not itself violate the stated theorem.

## 3. Conditional decay and the non-Markov NA argument

**Audited:** `Theory_work/Wave2/W2-APP/lemmas/L2_CT.md:9`–`:59` and `lemmas/L3_LOC.md:98`–`:148`.

The CT conjugation bound works on inherited integer positions. After conditioning on U, the complement retains its original positions; it is not compressed into consecutive indices. At most two coordinates remain at each integer distance, so both Schur-test sums retain the same bound. Applying CT first to Sigma and then to the appropriate principal precision submatrix proves the claimed conditional decay uniformly in U. The second application uses the spectral lower bound 1/C, which is available for LOC. POST does not depend on this argument.

For NA, write g = C e_(T intersect B_l) and h = (I-P_T)g. The identity relating h to the sample residual of x_l is exact because the population regression on T intersect B_l lies in span(X_T). This does not require a Markov property. The omitted population prediction variance is bounded by a geometric tail of squared conditional covariances, yielding O((log n)^(-2)) with the stated growing radius.

The two separate counts are appropriate:

- The reference noise statistics number p times 2^O(log log n), so their squared maximum is bounded by 2 log p + O(log log n).
- The intermediate union over (T,l) has size at most p 2^|Q| = n^O(1). These are lattice sets inside deterministic Q, **not all subsets of [p]**.

The noise projection bound uses P_T <= P_Q for all lattice T; it does not pay a separate noise tail for every T. Combining the projection estimates in L3 `:138`–`:145` gives

    max |Z_(T,l) - Zref_(l,T')|
      = O(log n/sqrt(n) + 1/sqrt(log n)) = o_P(1).

The resulting squared-statistic excess is at most O(log log n)+O(1) beyond 2 log p, safely below the threshold's additional log n minus O(log log n). There is ample asymptotic slack, even if the CT constants give an extremely late onset.

**Independent non-Markov check:** for the MA(1)-type correlation matrix with diagonal 1 and adjacent entries 0.4, p=12, n=2048, Q={1,...,7}, S0={1}, I checked all 512 lattice/candidate pairs. At an intentionally fixed reference radius 1, the exact projection identity had maximum error 5.77e-15, but max |Z-Zref| was 0.514108 and the largest omitted population prediction variance was 0.075294. Thus radius one does not provide an exact innovation reduction for this non-Markov example. The submitted proof uses a growing radius and bounds that error; it does not make the failed fixed-radius assertion.

For the same population covariance, I also checked all 4096 conditioning sets via (Theta_VV)^(-1). The minimum conditional variance was 0.600183143, above the population spectral floor 0.223246546. The largest off-diagonal conditional-covariance/CD-bound ratio was 0.112565696. No violation was found.

## 4. LOC-B and claimed family membership

**Audited:** `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:169`–`:197`; `lemmas/L4_families.md:28`–`:47`, `:78`–`:130`.

LOC-B really does avoid an upper spectral bound: cross-component conditional covariances vanish exactly, the individual conditional variances are at most one, and inverse bounds use the fixed lower floor. The logarithmic-size score toolkit requires lower Gram bounds and energy, not a uniform upper norm of the growing population block. The spherical mean term is zero for a null outside the truth-containing components.

The enlarged-Q requirement is essential and is present in v1.3.1. GROW L2.3(a) charges |Q minus S0| degrees of freedom. A bound only on the original truth-containing blocks would not suffice after Q is enlarged to [p]. The additional p-s0 bound is stated in the lemma, statement, family entry and report. No repair is outstanding on this point.

Membership claims also survive, with their existing qualifications:

- Fixed-bandwidth covariance has exponential off-diagonal bounds with fixed K; fixed-bandwidth precision uses its spectral norm bound 1/c. The inverse/conditional-decay lemma supplies what is then needed.
- For a fixed causal invertible finite-order ARMA model with positive innovation variance, stable AR roots give exponentially decaying impulse coefficients (polynomial factors from repeated roots can be absorbed by a slightly slower exponential); invertibility excludes MA zeros on the unit circle. The rational spectral density is continuous and strictly positive on that circle, giving fixed upper and lower bounds. Thus the **qualified** ARMA example in L4 `:88`–`:90` is valid. An arbitrary sequence of near-unit-root or near-noninvertible ARMA parameters is not covered by that fixed-constant claim.
- Bounded population blocks can be ordered consecutively. Their bandwidth may exceed 15 without increasing the method's conditioning-set size.
- Growing equicorrelated blocks have a fixed lower floor but unbounded upper norm and cannot be placed in LOC with uniform constants. They are covered by LOC-B only with its stated post-enlargement small-logarithmic bound. No unjustified claim of LOC membership was found.

## 5. VN and STAR

**Audited:** `Theory_work/Wave2/W2-APP/lemmas/L5_VN.md:14`–`:72`.

F16 supplies all bounded-dimensional inverse and conditional-variance bounds needed to transfer the population visible-null floor to sample partial correlations. The sample error is O(sqrt(log n/n)); the condition n kappa_n/log n -> infinity makes this o(sqrt(kappa_n)). The proof compares correlations before squaring, so it does not mistakenly require kappa_n to dominate sqrt(log n/n).

For a nonsaturated maximiser, any omitted visible null in a truth-free method block has an improving addition. Its prior cost is at most log(2p); its table gain is at least n kappa_n/4 minus (1/2)log(n+1) and a bounded remainder. Blocks that touch a truth can protect at most 15s0 nulls. Saturation is handled by the alternative |S-tilde|=K. This proves the displayed minimum bound without a union over maximisers.

For STAR, the perturbation has only two nonzero eigenvalues, +/-r sqrt(m), giving total spectrum {1/2,1,3/2} at r=1/(2 sqrt(m)). Leaves are mutually uncorrelated. Conditioning on other leaves or independent padding therefore leaves Cov(W_l,W_1|U)=r and Var(W_l|U)=1. The stated lower bound theta^2/[4m(theta^2+sigma^2)] for squared partial correlation is valid. With m=floor(n^(1/3)), it meets the visibility rate and K is eventually much larger than m. The lower count is consequently m-15, uniformly over allowed method partitions. Padding to polynomial p much larger than n does not change the calculation.

Nonmembership in LOC is also justified: m leaf correlations of size 1/(2 sqrt(m)) require m positions within O(log m) of the hub under any exponential covariance bound. This is impossible on a line. The precision alternative is excluded by CD(c), since it would imply exponential covariance decay. PTV holds for the single truth by the spectral floor. Thus STAR isolates locality rather than a bad condition number or a masked truth.

**Independent finite-sample attempt:** seed 220911, n=32768, m=32, p=65, theta=2, sigma=1; generate independent leaves/padding and construct the hub as r times the sum of leaves plus sqrt(3/4) times an independent standard normal. After centring/scaling, I sampled 1000 leaf/conditioning-set pairs with U excluding the truth and |U|<=15. Using the actual D0 marginal-score formula, every add gain remained positive even after subtracting log(2p): minimum 67.511902. This is an independent score calculation, not a production DP/LS0 run or a proof about all finite-sample subsets.

VN proves route obstructions, not failure of the method. The shipped LS0 cap permits deletion of a large start model; VN does not rule out such a path. The report preserves this distinction.

## 6. ENUM versus the implementation

**Audited:** `Theory_work/Wave2/W2-APP/lemmas/L6_ENUM.md:7`–`:31`, against:

- `Scripts/SMC_BVS/core/v3_preprocess.R:19`–`:32`: K, N0, H0 and call to the count routine.
- `Scripts/SMC_BVS/core/cpp/v3_core.cpp:72`–`:84`: exact binomial recurrence, sum from k=0 through K, strict rejection only when the sum exceeds (5H0+4N0)p.
- `Scripts/SMC_BVS/core/cpp/v3_core.cpp:537`–`:556`: recursive visit of every feasible subset, including the empty set, with no duplicate-component pruning.
- `Scripts/SMC_BVS/core/cpp/v3_util.h:121`–`:125`: strict F, then smaller size, then lexicographic tie order.
- `Scripts/SMC_BVS/core/v3_fit.R:120`–`:131`: exact branch returns before LS0; estimates are available only on completed exact enumeration.

The inequality in v1.3.1 is the coded decision, including its non-strict equality boundary. The sufficient inequality 2^p <= 4np is not presented as an equivalence to that decision. Gaussian nonconstant columns suffice to preserve p in preprocessing; duplicate diagnostics do not remove columns from the enumerated space.

Under EX-A, posterior mass greater than 1/2 gives a unique F maximiser, so tie handling cannot change the conclusion. On complete enumeration S0 is necessarily scored. Resource or numerical failures without estimates are outside O, and POST therefore implies the stated joint-with-output error probability without an LS0 argument. This does not prove delivery or conditional-on-output consistency.

**Independent arithmetic check:** Python arbitrary-precision integers, n in {3,...,100,128,256,512,1000,1024,4096,32768,10^6,10^9}, p=1,...,300. I compared the production recurrence and early rejection with a full sum of exact binomial coefficients: 32,100 cases, zero mismatches. All 1,179 cases satisfying 2^p <= 4np also selected enumeration. For n=1000, p=17 passes and p=18 fails (262144 > 226080); for n=32768, p=21 passes and p=22 fails (4194304 > 3621794). This tests an independent port of the decision arithmetic; the compiled production routine was inspected, not executed.

## Reproduction notes and limits

Checks ran in memory using R 4.6.1 and Python 3.15.2 with standard libraries/base R; no simulation files, code edits, compiled artifacts, or git operations were produced. Only this audit is written. The numerical calculations can be reproduced from the recipes above; the exact-branch check is:

```python
from math import comb
ns = list(range(3, 101)) + [128, 256, 512, 1000, 1024, 4096,
                           32768, 10**6, 10**9]
checked = sufficient = 0
for n in ns:
    for p in range(1, 301):
        N = max(2500, n, p)
        H = (512*N + 2499)//2500
        threshold = (5*H + 4*N)*p
        K = min(p, n//2)
        term, total = 1, 0
        for k in range(K + 1):
            if k:
                term = term*(p-k+1)//k
            total += term
            if total > threshold:
                break
        exact_branch = total <= threshold
        assert exact_branch == (sum(comb(p, k) for k in range(K+1))
                                <= threshold)
        if 2**p <= 4*n*p:
            assert exact_branch
            sufficient += 1
        checked += 1
print(checked, sufficient)  # 32100 1179
```

For the MA(1) check, use R seed 220912 and W = G chol(Sigma), where G has iid standard normal entries, then centre columns and draw independent standard normal epsilon. Enumerate T={1} union A for every A subset {2,...,7}, and every l outside T. With T'=T intersect {v:|v-l|<=1}, calculate g=W_l-W_T' Sigma_T'T'^(-1) Sigma_T'l and compare (I-P_T)g with (I-P_T)W_l, and their normalised noise inner products. The reported CT/CD check exhausts all U via solve(solve(Sigma)[V,V]), with constants computed exactly from L2_CT using the finite matrix's extreme eigenvalues, a=1 and K=exp(1). The deliberately small radius in this test is not substituted into Theorem LOC.

Remaining boundaries are already explicit in the submission: fixed s0 and coefficient floors; iid Gaussian rows; fixed locality constants and one-dimensional neighbourhood growth; named exact-arithmetic/operational premises; no delivery guarantee. The verdict does not extend to changing block caps, general non-Gaussian designs, unqualified ARMA sequences, or an unconditional guarantee that a finite-resource fit returns an estimate.
