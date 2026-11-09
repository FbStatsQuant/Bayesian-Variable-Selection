# R03 — Cross-family key-lemma check: L3–L6

Reviewer: Codex gpt-6.1-sol, xhigh. Date: 2026-11-09.
Target: W2-UNI `STATEMENT.md` v1.1, Theorem UNI-1 and R3/R4/R5.

| File | Verdict |
|---|---|
| `lemmas/L3_ULOC.md` | **VERIFIED-WITH-AMENDMENTS** |
| `lemmas/L4_k1.md` | **VERIFIED-WITH-AMENDMENTS** |
| `lemmas/L5_delivery.md` | **VERIFIED-WITH-AMENDMENTS** |
| `lemmas/L6_frontier.md` | **VERIFIED-WITH-AMENDMENTS**; OBS-k itself **VERIFIED** |

Findings: **0 FATAL, 1 MAJOR, 5 MINOR**. The MAJOR finding is a missing case in the stated interface to TL, with a direct repair on the existing event. I found no counterexample to U-LOC, UNI-1, F-UNI or OBS-k under the stipulated inputs. No strengthening of the locked theorem hypotheses is required by these findings.

Scope: I took exactly the uniform regression bound, conditional-variance floor, uniform localisation with deterministic epsilon(r) tending to zero, and variance comparison specified in the review brief as given. I did not certify their proofs in L1_metric. I compared the listed FACA L1–L5/L7, FACA STATEMENT, and LOC2 L7. Source status qualifications remain inherited; this review does not independently re-certify the underlying operational/machine results or the separately reviewed metric toolkit. All objections below concern asymptotic statements or proof interfaces.

## L3_ULOC.md — VERIFIED-WITH-AMENDMENTS

The mathematics of (a)–(d) checks out. Findings 1–3 concern the final interface, its rate description, and the numerical evidence cited at the top.

**1. MAJOR — The final corollary omits the empty conditioning set needed by TL.**

Locations: L3 lines 108–115; L4 lines 28–31 and 53–55. Consumer: FACA `lemmas/L3_NA_TL.md:64`–`:71`.

Both versions of Corollary U-LOC quantify only over nonempty T. FACA's TL proof sets B = T minus {i} and invokes the uniform envelope for Z_(B,i) and, for a swap, Z_(B,l). The permitted case s0 = 1 and T = S0 has B empty. Consequently L4 cannot literally substitute the stated corollary into the whole TL proof. This case persists along asymptotic sequences; it is not a finite-n objection. NA itself has no such problem because its conditioning sets contain the nonempty S0.

**Exact fix:** extend both corollaries to all T, defining the entire size-dependent factor summand as zero when T is empty, without evaluating its logarithm there. No additional event, hypothesis or failure probability is needed. On the existing E_U, (b) and (c) already give

    max_l |Z^Sigma_(empty,l)|
      <= sqrt(2 log p) + eta_n + kappa'_bd sqrt(2 log log n)
      <= sqrt(2 log p) + epsilon^U_n.

Apply the same U(d) perturbation bound to these empty-set innovations. The conditional simultaneous probability remains at least 1 - 5/log n. In L4 explicitly use the resulting all-T event. For FACA L3.2 use, for example,

    Zbar_n = sqrt(2 log p) + kappabar sqrt(2 log(e gammabar p))
             + epsilon^U_n + L_psi delta_n sqrt(5(p+1) log log n),

which is O(sqrt(log n)) and covers both empty and nonempty B. With this repair, the TL substitution is valid.

**2. MINOR — “remainder of the same order” is stronger than what the supplied toolkit establishes.**

Location: L3 lines 124–127.

The required conclusion is epsilon^U_n = o(sqrt(log n)), and the proof correctly establishes it. It does not establish equality of orders with FACA's O((log p)^(1/4) + sqrt(log log n)) population remainder. Here the reference entropy contributes up to O((log log n)^d0), and the assumptions supplied for this review specify only epsilon(r) -> 0, not a rate that would put the atom term in FACA's finer order. The transfer does not need that finer order.

**Exact fix:** replace “with an o(sqrt(log n)) remainder of the same order” by “with a deterministic o(sqrt(log n)) remainder, which is the only remainder property used in FACA L3.1.” Do not introduce a new metric-toolkit requirement just to preserve this wording.

**3. MINOR — The cited “exact c_G” enumeration skips the full set.**

Locations: L3 lines 3–5; L4 lines 64–65; supporting script `numerics/n3b_exhaustive.py:53`–`:60` and `:116`–`:118`.

The script builds all_sets using range(p), and its separate block-CS c_G loop uses range(1,p). Both omit T = [p]. This is harmless for add-statistic pairs, since no l is then available, but c_G is an infimum over every nonempty T, including [p]. The enumeration therefore does not generally certify the advertised exact c_G. This is an enumeration-domain error, not an objection to using small numerical probes for an asymptotic theorem.

For an explicit witness with singleton groups, take lambda = (1/2,1/2) and

    Psi = (3/4) [[1,1/2],[1/2,1]].

Then Sigma = lambda lambda^T + Psi is a correlation matrix. The two singleton ratios are 1/3, whereas s_[2]/2 = 2/9. Omitting the full set changes the answer. This does not show the recorded random-design values are wrong; it shows their claimed exact coverage is incomplete.

**Exact fix:** enumerate range(p+1) when constructing the sets used for c_G, and range(1,p+1) in the separate CS c_G loop. The innovation loops may keep excluding the full set or simply have no available l there. Re-run the output and retain/update the cited values accordingly. The analytic proof of c_G and the CS normalisation is unaffected. I have not edited the numerical script.

### Requested attacks on (a), (c), (d)

**(a): independence is valid for general positive definite Psi.** The residual e = zeta_l - beta_T^T zeta_T satisfies Cov(e,zeta_T) = 0 and Cov(e,xi0) = 0. Joint Gaussianity makes it independent of (xi0,zeta_T), hence of W_T. The orthogonal complement K_T minus H_T has dimension one; omega_T has variance 1+s_T and is orthogonal to every gamma_j, j in T. Its coefficient against gamma_l is lambda-tilde_(l|T)/sqrt(1+s_T). These observations prove exactly the displayed decomposition without block structure. No independence between the families indexed by different T is asserted or needed.

**(b): the deterministic bound is valid.** The exact denominator produces kappa'_(l,T) times |xi0 - sqrt(s_T) F_T|/(1+s_T). Using sqrt(s_T)/(1+s_T) <= 1/sqrt(s_T) for nonempty T gives the bound. Positivity of s_T follows from A2-1. The empty-set summand must be interpreted separately rather than as zero times an undefined F_empty/sqrt(s_empty), as already done in the proof.

**(c): the reference/atom count and uniformity are valid.** Each pair (T,l) selects one existing reference A = T intersect B(l,r_n). The error is bounded deterministically by ||Delta||_1 max_v |zeta_v| on the single p-atom event. Thus the simultaneous event covers all T without a union over those T. There are at most p times 2^N_n references and p atoms. The absolute Gaussian tail bound used in the text is valid; independence of references or atoms is unnecessary. Unit diagonal of Sigma ensures Var(zeta_v) <= 1.

The variance ratio is at most 1+C epsilon_n^2/c. Since N_n = O((log log n)^(2d0)) = o(log n), epsilon_n -> 0, and log p <= A log n, every term in the displayed eta_n is o(sqrt(log n)). This remains true for bounded p and for varying population matrices with the same constants. No quantitative decay rate for epsilon is needed.

**(d): the exponential union is present, explicit and correctly paid for.** Choosing h groups and a nonempty subset of each gives at most binom(G,h)(2^gammabar-1)^h sets. F_T is marginally standard normal for every such T. The total failure bound is

    sum_(h=1)^G |T_h| exp(-x_h)
       <= [1/(2 log n)] sum_(h=1)^infinity 1/(h+1)^2
       = (pi^2/6 - 1)/(2 log n).

No independence across T is required. The inequalities for x_h/h, h >= |T|/gammabar, and G <= p give exactly the stated varrho_n. Multiplying c_G^(-1/2) by kappa' gives kappa; thus c_G may tend to zero without entering the final remainder separately. The uniform bound on kappa' comes from RB_M, bounded loadings and the conditional-variance floor.

**FACA normalisation is reproduced exactly.** For its group partition, block diagonality gives s_T = sum_g s_(T intersect g), so c_G >= c_min; a subset in a single group attaining c_min gives the reverse inequality. Likewise the suprema defining kappa' coincide. Hence kappa_UNI = kappa_FACA, not merely <=. For the block-CS representation with b = rho_w-rho_b > 0, d = 1-rho_w > 0 and u conditioning coordinates in l's group,

    c_G = rho_b/(d+b),
    lambda-tilde^2/(psi c_G)
       = d(d+b)/[(d+ub)(d+(u+1)b)] <= 1,

with equality at u=0. Therefore kappa=1 and alpha0=1/6, with the original groups. Changing the partition can change this normalisation; no partition-invariant equality is being certified.

The sample coupling is also valid: its reconstruction of independent xi0 and zeta has the stated Gaussian covariance, and U(d) needs only the global lower spectral bound and correlation diagonals. It introduces no block assumption or upper bound on ||Sigma||. The original-space inequality event has the claimed conditional probability by containment of the enlarged-space event.

## L4_k1.md — VERIFIED-WITH-AMENDMENTS

The reduction works after finding 1. Finding 6 below also applies to its frontier remark.

I found no additional structural use of block-diagonal Psi in the general-theorem parts of FACA L2–L5/L7. The inventory is correct when “only place” means the only essential use of block structure itself: the other consequences of membership in F are separately supplied in the inventory. This is not a claim about FACA's family-specific L5.2/L5.3 calculations, which are not imported into UNI-1.

* **FACA L2:** it needs energy, the floor on actual method blocks, Gaussian noise, TV, polynomial dimension and K=p. Its polynomial block-family union is conditional on X. No idiosyncratic group partition is used. The method's blocks need not match the metric or G.
* **FACA L3.0:** the determinant/ridge expansions and response-noise event use the global sample Gram floor and p=o(n), not block structure or a bounded upper spectral norm.
* **FACA L3.1:** after reducing to the innovation envelope, it uses only sqrt(2P)+kappabar sqrt(2x_k)+o(sqrt(log n)). In particular,

      max_(0<=s<=1) [(1+kappabar s)^2-s^2]
          = kappabar(kappabar+2),   kappabar >= 1.

  This yields exactly alpha0 = 1/[2 kappabar(kappabar+2)]. The strict growth gap absorbs the squared remainder uniformly in k. No FACA-specific remainder rate or block-energy independence is subsequently used.
* **FACA L3.2:** it needs the all-conditioning-set O(sqrt(log n)) envelope, the Gram floor and beta-min. Finding 1 supplies the missing interface case. The truth coefficient bounds in UNI imply BM-infinity uniformly even if the bounded coefficients vary with n.
* **FACA L4:** the posterior input uses H0, supplied by fixed sparsity, bounded coefficients and the sample Gram floor. The deterministic descent lemma needs only S0 subset Q and |Q|<=K. With Q=[p], feasibility follows eventually from the strict exponent condition; the merged cap suffices.
* **FACA L5.0:** all new remainders have common deterministic bounds from the fixed locality constants, A and n. Neither c_G itself nor a lower bound on individual loadings enters the final common envelope. Thus its uniformity argument survives c_G -> 0.
* **FACA L5.1:** entrywise Gaussian correlation concentration is structure-free. The resulting error obeys delta_n sqrt(p log log n) = O(p^(3/2) sqrt(log n log log n/n)) -> 0 under the stated exponent. TV-pop transfers on bounded-size V using only the spectral floor, bounded coefficients and the same simultaneous entrywise error. Even the family of all size-at-most-16 blocks creates no unaccounted union: the Gram event already controls every entry, and the Lipschitz constant is uniform. Conditional convergence is upgraded using common envelopes and the every-sequence argument, rather than pointwise conditioning alone.
* **FACA L7:** validity and allocation are separate inputs; its statistical step uses the scoring event and posterior expectation. No factor geometry is consumed there.

Consequently L3/L4 need no metric-toolkit statement beyond the inputs stipulated in this review. Finding 2 removes wording that could misleadingly suggest a stronger rate requirement.

## L5_delivery.md — VERIFIED-WITH-AMENDMENTS

The abstract reduction R4 is correct, conditional on its explicitly retained delivery premises and inputs (V), (S), (P). The exact start mode belongs to the feasible lattice on Sand; NA and TL keep the complete-scan descent there until S0 is scored, within the merged cap. Therefore P(K_n^c)->0 follows from the joint event (S), not from D_n->0. On output and K_n and posterior mass above 1/2, the reported maximiser must be S0. Markov's inequality gives exactly the stated bound 2 E[1-pi(S0)] + P(K_n^c). The input and no-output reductions match FACA L7 and LOC2 L7. The UNI-1 instance inherits finding 1 until repaired.

**4. MINOR — Positive population covariance does not exclude sample collinearity at unrestricted dimension.**

Location: L5 line 24.

The parenthesis “lambda_min > 0 excludes exact collinearity a.s.” is unnecessary and, if it means full column rank, false in this abstract proposition. For instance, under p_n=n^2 and Sigma_n=I, the centred sample rank is at most n-1 at every n. The validity and scorer arguments do not require full column rank. Nonconstant columns follow from their positive marginal variances, and ridge terms make the score well-defined even on rank-deficient subsets.

**Exact fix:** replace the parenthesis by “Var = Sigma_jj = 1 > 0”; delete the collinearity clause. Optionally spell out the inherited score facts H_S positive definite, G_S+I positive definite and Q_S >= y^T y/(n+1)>0. No change to (V) or any theorem conclusion is needed.

## L6_frontier.md — VERIFIED-WITH-AMENDMENTS

**OBS-k itself is VERIFIED.** One may take the row bound L>0 without loss, including when all rows vanish. The sphere has a finite cover of the specified diameter, uniformly in n. Selecting perpendicular u_j and applying the pigeonhole principle yields a set of exactly m rows with all projections onto one unit vector at most eta. Since Psi_TT^(-1) <= c^(-1) I, its information matrix has Rayleigh quotient at most m eta^2/c. The infimum is nonnegative and eventually at most eta^2/c for every eta>0, which proves its convergence to zero. No upper spectral bound or locality assumption is used. The theorem's fixed-m scope agrees with the locked statement.

The remainder is labelled a plan, but two assertions in its explanatory prose should be narrowed.

**5. MINOR — OBS-k does not prove the asserted obstruction for smallest nonzero eigenvalues, or rarity of weak sets.**

Locations: L6 lines 18–20 and 34.

OBS-k concerns lambda_min including zeros. For example, with k=2, every row equal to a fixed nonzero multiple of e1 and Psi=I, every S_T has a zero eigenvalue, but its sole nonzero eigenvalue divided by |T| is a fixed positive constant. Thus the lemma cannot justify the adjacent claim about smallest nonzero eigenvalues. Nor are weak-direction sets necessarily few: with half the rows proportional to e1 and half to e2 there are 2^(p/2)-1 nonempty subsets of the first half with an exactly zero second direction, even though the full information matrix has full rank. The orientation of the residual loading against those directions also matters in the actual factor contribution.

**Exact fix:** retain the stated obstruction to a uniform full-rank lower bound on all subsets of size at least a fixed m. Replace the last sentence of the Scope paragraph by: “OBS-k alone gives neither a bound on nonzero eigenvalues nor an entropy bound for weak subsets. A k-factor extension must control the factor contribution without assuming this impossible uniform full-rank floor; possible approaches include bounds sensitive to directions and residual loadings, stratification of sets when justified, or a path argument.” Replace “weak directions on few sets” in the plan table by “control of weak directions without a uniform full-rank subset floor.”

**6. MINOR — SHARP does not establish necessity of a path route at every kappa-dependent alpha0.**

Locations: L4 lines 65–66; L6 lines 26–27.

FACA SHARP is an exact-CS impossibility for full-lattice NA beyond 1/6. It does not show that the sufficient alpha0(kappabar) is sharp for general representations, nor that a path argument is the only possible replacement. A simple illustration is exact CS with kappa=1 but a permissible loose bound kappabar=2: alpha0(2)=1/16. At log p/log n=1/10, the existing kappa=1 theorem still proves full-lattice NA, although this exponent is beyond alpha0(2). No path is required there.

**Exact fix:** replace both general necessity assertions by: “For exact CS, SHARP rules out full-lattice NA beyond 1/6; covering those exponents requires replacing that route, for example by a path argument. Necessity of alpha0(kappabar) for other representations has not been established.” This preserves the intended plan and its family-specific evidence without asserting an unproved general sharpness result.

## Independent numerical falsification

I ran Python 3.13 with -B, numpy, seed 9303, entirely in memory. For p=8 and three idiosyncratic designs (AR correlation, a path-precision correlation, and size-2 block correlation), I enumerated all 2^p subsets, including the full set for c_G/counts, and every available l. There were 3,072 innovation pairs. I checked the decomposition, the analytic covariance between Xi and W, the deterministic bound (b), and the exact localisation variance identity for radii 0,1,2. I also checked the exact count binom(4,h)3^h for size-2 groups. These are algebra/numerical falsification checks, not probability estimates or substitutes for the asymptotic proof.

Recorded output:

```text
exhaustive pairs=3072; max_decomposition_error=1.499e-15; max_abs_Cov_Xi_W=2.946e-16; max_variance_identity_error=2.220e-16; positive_bound_excess=0.000e+00
group-count equality verified: C(4,h)*3^h for every h=1,...,4 (three designs).
full-set omission witness: singleton c_G=0.333333333333; full-set s_T/|T|=0.222222222222
```

Reproduction source follows in this review so that no additional file is created:

```python
import itertools, math
import numpy as np
rng=np.random.default_rng(9303)
p=8
max_dec=max_cov=max_var=max_excess=0.0
pairs=0
for kind in range(3):
    lam=rng.uniform(.15,.7,p)*rng.choice([-1,1],p)
    q=np.arange(p)
    if kind==0:
        R=.65**np.abs(q[:,None]-q[None,:])
    elif kind==1:
        Q=np.eye(p)+np.diag(np.full(p-1,-.4),1)+np.diag(np.full(p-1,-.4),-1)
        R=np.linalg.inv(Q); z=np.sqrt(np.diag(R)); R=R/z[:,None]/z[None,:]
    else:
        H=np.equal.outer(q//2,q//2).astype(float)
        R=.6*np.eye(p)+.4*H
    D=np.sqrt(1-lam**2); P=D[:,None]*R*D[None,:]; S=P+np.outer(lam,lam)
    J=np.zeros((p+1,p+1)); J[0,0]=1; J[1:,1:]=P
    noise=np.r_[rng.normal(),rng.multivariate_normal(np.zeros(p),P)]
    kp=0; rec=[]; cg=math.inf
    groups=[list(range(a,min(a+2,p))) for a in range(0,p,2)]
    counts=[0]*(len(groups)+1)
    for mask in range(1<<p):
        T=[j for j in range(p) if mask>>j&1]
        h=sum(any(j in T for j in g) for g in groups)
        if T:
            a=np.linalg.solve(P[np.ix_(T,T)],lam[T]); st=lam[T]@a
            cg=min(cg,st/h); counts[h]+=1
        else: a=np.zeros(0); st=0
        w=np.zeros(p+1); w[0]=1; w[np.array(T,dtype=int)+1]=-a; w/=np.sqrt(1+st)
        F=(a@noise[np.array(T,dtype=int)+1])/np.sqrt(st) if T else 0
        for l in range(p):
            if l in T: continue
            b=np.linalg.solve(P[np.ix_(T,T)],P[T,l]) if T else np.zeros(0)
            v=P[l,l]-P[l,T]@b; lt=lam[l]-b@lam[T]; kp=max(kp,abs(lt)/np.sqrt(v))
            e=np.zeros(p+1); e[l+1]=1; e[np.array(T,dtype=int)+1]=-b; e/=np.sqrt(v)
            max_cov=max(max_cov,abs(e@J@w))
            bs=np.linalg.solve(S[np.ix_(T,T)],S[T,l]) if T else np.zeros(0)
            gamma=lam*noise[0]+noise[1:]
            Z=(gamma[l]-bs@gamma[T])/np.sqrt(S[l,l]-S[l,T]@bs)
            dec=(np.sqrt(v)*(e@noise)+lt/np.sqrt(1+st)*(w@noise))/np.sqrt(v+lt*lt/(1+st))
            max_dec=max(max_dec,abs(Z-dec)); rec.append((Z,e@noise,F,st))
            for r in [0,1,2]:
                A=[j for j in T if abs(j-l)<=r]
                bA=np.linalg.solve(P[np.ix_(A,A)],P[A,l]) if A else np.zeros(0)
                d=np.zeros(p); d[T]=b; d[A]-=bA
                vA=P[l,l]-P[l,A]@bA
                max_var=max(max_var,abs(vA-v-d@P@d))
            pairs+=1
    for Z,Xi,F,st in rec:
        bound=abs(Xi)+kp*abs(noise[0])+(kp*abs(F)/np.sqrt(st) if st else 0)
        max_excess=max(max_excess,abs(Z)-bound)
    assert all(counts[h]==math.comb(4,h)*3**h for h in range(1,5))
print(f'exhaustive pairs={pairs}; max_decomposition_error={max_dec:.3e}; max_abs_Cov_Xi_W={max_cov:.3e}; max_variance_identity_error={max_var:.3e}; positive_bound_excess={max_excess:.3e}')
print('group-count equality verified: C(4,h)*3^h for every h=1,...,4 (three designs).')
P=.75*np.array([[1.,.5],[.5,1.]]); lam=np.full(2,.5)
print(f'full-set omission witness: singleton c_G={lam[0]**2/P[0,0]:.12f}; full-set s_T/|T|={lam@np.linalg.solve(P,lam)/2:.12f}')
```

Only this review file was written. No proof, statement, numerical source or output file was edited; no git command was run.
