VERIFIED-WITH-AMENDMENTS

No FATAL or MAJOR defect found. The identities and stated bounds are valid under the factor-class assumptions in STATEMENT.md. The amendments below clarify domains, constants, and probability-space bookkeeping; they do not change the bound or its asymptotic order. Line references refer to the files as read for this review.

1. Location: lemmas/L1_uniform_add.md:68 and STATEMENT.md:65–68, 108 — representation and κ′ notation.

   Problem: the parenthetical “κ(Σ)” incorrectly suggests that κ is intrinsic to Σ, although the locked statement explicitly makes it representation-dependent. Also, the lemma defines κ′ as the actual maximum, whereas STATEMENT (L1) defines κ′ := κ̄√c_min. Those quantities need not be equal when κ < κ̄. The statement's larger coefficient is valid, but the common notation obscures the inequality being used.

   Severity: MINOR.

   Exact fix: write κ = κ(λ, Ψ, 𝒢), κ′_* := max_{l,U}|λ̃_{l|U}|/√ψ_{l|U} = κ√c_min, and κ′_bd := κ̄√c_min. Use κ′_* in U(b)–U(c), and either coefficient, explicitly identified, in Corollary U. In STATEMENT (L1), use κ′_bd. Since κ ≤ κ̄, κ′_* ≤ κ′_bd. No larger probability allowance is needed.

2. Location: lemmas/L1_uniform_add.md:115, 123–126 — the promised explicit Lipschitz constant.

   Problem: “C₁(ψ₀) explicit below” is not fulfilled: C₂ and C₃ are introduced only as unnamed bounds. Their existence is proved, but the requested numerical constant is not supplied.

   Severity: MINOR.

   Exact fix: put m := 3ψ₀/4 and B := m^(−1/2), and take

       C₂ := (1+B)(3+B²)/(2m^(3/2)),
       C₃ := (1+B)/√m,
       L_ψ := C₂ + 2C₃/ψ₀.

   Indeed, ‖c_R−c_Σ‖ ≤ δ(1+B)/m, |v_R−v_Σ| ≤ δ(1+B²), and both Schur complements are ≥ m. The two terms in the displayed bound for ‖a_R−a_Σ‖ are therefore bounded by δ(1+B)/m^(3/2) and δ(1+B)(1+B²)/(2m^(3/2)), respectively. These constants depend only on ψ₀.

3. Location: lemmas/L1_uniform_add.md:6–17, 35, 87–93, 137 and STATEMENT.md:104, 108 — covariance domain and empty sets.

   Problem: Z^M is initially defined only for globally positive definite M, but L1.0 explicitly allows a possibly singular R̂ provided its relevant principal block and residual are nonsingular. The right-hand side of (0.1) thus slightly exceeds the declared notation's domain. The empty-set phrase “terms … read as 0” is also too broad literally: W_∅ is ξ₀, not zero, and ψ_{l|∅} is Ψ_ll. Multiplying an undefined log(p/|T|) by an indicator also needs the intended piecewise convention.

   Severity: MINOR.

   Exact fix: extend Z^M to positive semidefinite M whenever M_TT ≻ 0 and v_M > 0. State that only products/sums over empty index sets vanish; explicitly set c_∅ = 0, s_∅ = 0, W_∅ = ξ₀, ψ_{l|∅} = Ψ_ll, λ̃_{l|∅} = λ_l, and Ξ_{l,∅} = ζ_l/√Ψ_ll. Define the entire size-dependent summand as zero when T = ∅, without evaluating its logarithm. Under the small-δ condition used in Corollary U, R̂ is already globally positive definite, so no downstream inverse is missing.

4. Location: lemmas/L1_uniform_add.md:23–24, 60–63, 101–106 — description of the union bound.

   Problem: the literal assertion that no union over the 2^p sets T is taken is misleading. U(c)(iii) unions over all nonempty subsets of the factor groups; when every group is a singleton this is exactly 2^p−1 subsets, in bijection with nonempty T. This does not invalidate the estimate: its cardinality-dependent threshold absorbs the combinatorial count.

   Severity: MINOR.

   Exact fix: replace the assertion by: “We avoid a direct union bound over the innovation normals indexed by (T,l). We union over the local innovation pairs (l,U), and over subsets of factor groups with thresholds depending on the number of groups.” The variables W_T still have up to 2^p indices; their simultaneous control comes from U(b), not from a polynomial count of those directions.

5. Location: lemmas/L1_uniform_add.md:134–141 — specify the original-space event in the coupling proof.

   Problem: the latent good event supplied by U(c) lives on an enlarged probability space. It should not itself be called an event measurable only in (X,ε). The coupling is nevertheless legitimate: it implies a lower bound for the original-space event that all the displayed inequalities hold.

   Severity: MINOR (formalization; no invalid probability transfer found).

   Exact fix: define B_n(X,ε) to be the event that the Corollary U inequality holds for every admissible (T,l), using the chosen representation's deterministic constants. For each fixed good X, put γ = Σ_n^(1/2)R̂^(−1/2)g. With b := Σ_n^(−1)λ and an additional independent V ~ N(0,1), set

       ξ₀ := bᵀγ + √(1−λᵀΣ_n^(−1)λ) V,
       ζ := γ−λξ₀.

   The square root is strictly positive because Ψ ≻ 0. Given X, these are jointly Gaussian with Var(ξ₀)=1, Cov(ζ)=Ψ and Cov(ξ₀,ζ)=0. They realize γ = λξ₀+ζ exactly while preserving the original marginal law of (X,ε). If A_n is the intersection of the latent U(c) good event and the norm good event, then A_n ⊆ B_n and

       P(B_n | X) = P_enlarged(B_n | X)
                  ≥ P_enlarged(A_n | X) ≥ 1−4/log n.

   Take E_n := B_n. This argument permits probabilities of original-data events; it makes no assertion that the latent good event itself belongs to the original sigma-field. For random designs, apply the argument conditionally on X on the design event where the Gram bound holds, and then integrate over X. The noise/design independence specified in STATEMENT.md:47–49 is essential and is present.

The remaining line-by-line checks are as follows.

L1.0, lines 14–21: correct. The unnormalized residual inner product is σ√(n−1)(g_l−R̂_lT R̂_TT^(−1)g_T), and its squared norm is (n−1)v_R̂. Division cancels both factors exactly, with no extra n/(n−1) or response-standardization factor. Given X, Gaussian noise gives g ~ N(0,R̂); centering replaces ε by Cε without changing Xᵀε. This is a statement about the noise add direction defined here, not a claim that a general signal-plus-noise response has zero conditional innovation mean.

U(a), lines 28–58: correct, including arbitrary signs, vanishing individual loadings, and T = ∅. The covariance of the vector (ξ₀,ζ_T) is diag(1,Ψ_TT), so its coordinates are linearly independent in L² and dim 𝓚_T = |T|+1. The covariance of γ_T is Σ_TT ≻ 0, giving dim 𝓗_T = |T|. Because 𝓗_T ⊆ 𝓚_T, the orthogonal complement has dimension one; no generic-position or nonzero-loading assumption is needed for this assertion.

Block diagonality makes ζ_l orthogonal to ζ_{T\U}, and also makes those outside coordinates orthogonal to ζ_U. Thus projection onto all ζ_T really does reduce to projection onto ζ_U. The first residual has variance ψ_{l|U}>0 and is orthogonal to all of 𝓚_T. For ω_T = ξ₀−λ_TᵀΨ_TT^(−1)ζ_T, Cov(ω_T,γ_j)=0 for every j∈T, while Var(ω_T)=1+s_T>0. Consequently W_T is the unit direction in 𝓚_T ⊖ 𝓗_T, and

    E[γ_l W_T] = (λ_l−λ_TᵀΨ_TT^(−1)Ψ_Tl)/√(1+s_T)
               = λ̃_{l|U}/√(1+s_T).

The second equality uses both the support of Ψ_Tl and the block structure of Ψ_TT^(−1). Orthogonality gives the claimed innovation variance. Since Ξ_{l,U} and W_T are jointly Gaussian linear forms, their zero covariance proves their independence for each fixed pair (T,l). Independence across different pairs is neither asserted nor required.

U(b), lines 67–80: correct. Replacing √(α²+β²) by α gives the stated upper bound, and inserting W_T supplies precisely (1+s_T)^(−1), rather than (1+s_T)^(−1/2). Cauchy–Schwarz applies in the positive definite Ψ_{T_gT_g}^(−1) metric. The variational identity for q_V is exact; extending a coefficient vector by zeros proves q_V≤Q_g for every realization, despite negative within-group correlations. Summing across hit groups gives √s_T√ΣQ_g. Each nonempty group contributes at least c_min, so s_T≥c_min h_T>0 and √s_T/(1+s_T)≤1/√s_T≤1/√(c_min h_T). Hence the last coefficient is κ′_*/√c_min = κ, exactly as needed. The empty-T case is handled before division by s_T or h_T.

No uniform positive lower bound on c_min is secretly needed. In fact, the same variational monotonicity, with λ in place of ζ, gives c_min = min_j λ_j²/Ψ_jj. Thus finite-p nonzero loadings ensure c_min>0, while c_min may tend to zero with n. In the correlation factor class, Ψ_jj≥ψ₀ and λ_j²=1−Ψ_jj imply c_min≤(1−ψ₀)/ψ₀≤1/ψ₀. Therefore κ′_*≤κ′_bd≤κ̄/√ψ₀ uniformly, which verifies the stated dependence of constants.

U(c), lines 84–108: correct with fixed γ̄, as imposed by (AG). The exact count of indexed local normals is Σ_g |g|2^(|g|−1)≤p2^(γ̄−1). No independence of these normals is used. The Mills bound 2Φ(−t)≤√(2/π)e^(−t²/2)/t applies for t>0; the subsequent comparison to e^(−t²/2) needs t²≥2/π. At n=16, 2 log log n≈2.03956 already exceeds 2/π, so both uses meet that condition even at p=1. The replacement of the local threshold by the larger displayed threshold is harmless.

For any fixed h-group subset, the sum of Q_g is χ²_D with D=Σ_g|g|≤hγ̄. Independence here follows from block-diagonal Gaussian ζ. The Laurent–Massart threshold D+2√(Dx)+2x is increasing in D, so replacing D by hγ̄ makes the failure event smaller. With x_h=log binom(G,h)+2log(h+1)+log log n, the union bound over group subsets cancels binom(G,h) exactly. Summation over h costs at most (π²/6−1)/log n < 1/log n. Together with the two Gaussian events this gives ≤3/log n.

After division by h, log binom(G,h)/h≤log(eG/h) gives precisely a_h, with all coefficients correct. For integer h≥1, h+1≤2^h implies r_h≤2log2+log log n. Also h_T≥|T|/γ̄ and G≤p give log(eG/h_T)≤log(eγ̄p/|T|), and log(eG/h_T)≤log(eγ̄p) bounds the remainder inside the nested root. Splitting √(a+b)≤√a+√b gives the displayed ϱ_n.

More explicitly, let ℓ=log log n and b=2log2+ℓ. Then

    ϱ_n ≤ √(2b)+√γ̄+√2 γ̄^(1/4)[log(eγ̄p)+b]^(1/4)
         ≤ C(γ̄)[(log p)^(1/4)+ℓ^(1/2)],  n≥16.

The last step uses ℓ≥1 to absorb constants and ℓ^(1/4). This also covers fixed or bounded p, including p=1. The order assertion is not uniform over a growing γ̄; the contextual assumption that γ̄ is fixed is therefore material.

U(d), lines 112–130: correct. Weyl's inequality gives λ_min(R)≥3ψ₀/4. For b_M=e_l−ι_Tc_M, the minimization formula gives v_M=b_MᵀMb_M≥λ_min(M) because ‖b_M‖²=1+‖c_M‖²≥1. The correlation normalization yields c_MᵀM_TTc_M=M_ll−v_M≤1, so the coefficient norms depend only on the lower eigenvalue. The identity for c_R−c_Σ has the correct sign and bounds only submatrices of R−Σ. Comparing the two quadratic minima proves the stated Schur-complement difference bound; the reciprocal-square-root denominator is exact.

The square-root perturbation inequality holds for positive definite symmetric matrices without a commutativity assumption. To see this directly, set D=A^(1/2)−B^(1/2). Then A^(1/2)D+DB^(1/2)=A−B, whence

    D = ∫₀^∞ exp(−tA^(1/2))(A−B)exp(−tB^(1/2)) dt.

Taking operator norms gives the stated denominator √λ_min(A)+√λ_min(B). Both minima are bounded below here. The identity x−γ=(R^(1/2)−Σ^(1/2))R^(−1/2)x is exact in the stated multiplication order, and the resulting coefficient is at most 2δ/ψ₀. Thus no factor ‖Σ‖_op, √‖Σ‖_op, or p is hidden in L_ψ.

The weighted Laurent–Massart form used for ‖x‖ is also correct: diagonalizing R with eigenvalues d_i≥0 gives the threshold tr R+2√(tr(R²)u)+2‖R‖_op u. For completeness, the centered quadratic-form log-mgf is at most t²Σ_i d_i²/(1−2t max_i d_i), for 0<t<(2 max_i d_i)^(−1); Chernoff's inequality yields exactly that threshold. Since R is a correlation matrix, tr R=p, tr(R²)≤‖R‖_op tr R≤p². For u≥1, p+2p√u+2pu≤5pu≤5(p+1)u. This remains valid for a pervasive factor with ‖R‖_op of order p.

Corollary U, lines 134–143: the enlargement in finding 5 is valid conditionally on X and supplies the claimed original-space event. There is no requirement that the latent factor itself be an original-data observable. At n≥16, u=log log n≥1, and e^(−u)=1/log n, giving the fourth failure allowance. (AG) implies δ_n→0 and eventually δ_n≤ψ₀/4, and p+1≤2p for p≥1 makes the final perturbation remainder tend to zero. The exact-Gram case can retain the sharper 1−3/log n probability without paying for a norm event.

Hidden-assumption check: all inverses in U(a)–U(c) exist because Ψ≻0 and Σ≻0; all inverses in U(d) and Corollary U exist by the lower eigenvalue bound. Approximate full-Gram closeness with δ≤ψ₀/4 itself forces R̂≻0 and therefore p≤n−1 for centered X, just as exact-Gram closeness does; there is no valid p≥n exception. The factor partition 𝒢 is unrelated to the algorithmic blocks C_b, and the proof never identifies them. All innovation claims require l∉T; T=[p] contributes no pair. A nonempty partition implies p≥1 and γ̄≥1. U(a) permits zero loadings, while U(b)–U(c) explicitly exclude them via c_min>0. No p→∞ assumption is needed for this lemma.

Numerical checks

I read the author's FU_out.txt and FU5_out.txt. They report identity errors 8.882e−15 and 2.89e−15 and zero deterministic-bound violations in 53,003 and 39,895 cases, respectively. I did not rerun their writing entry points, because this task permits writing only this review file. Their perturbation experiments are sampled checks, not a proof of dimension-independent constants.

I ran the following additional script from the repository root through `py -3.13 -`. It imports the author's pure helper functions, disables bytecode writes, and writes no files. It checks the final U(b) bound with the global κ and κ′, not just the intermediate bound returned by the helper. The perturbation row norm maximizes the discrepancy over all unit x for each sampled (T,l), and the matrices R and Σ need not commute. The last loop deliberately includes some group-count/size combinations that cannot be realized by a partition; proving the deterministic inequality on this larger set is harmless.

```python
import sys, math, itertools
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, "Theory_work/Wave2/W2-FAC-A/numerics")
from fu_check import innov, decomp, kappa_cmin
rng = np.random.default_rng(90211)
pairs = err = violations = cov_err = 0
# Exhaustive subsets; unequal groups, mixed signs, tiny loading, and p=1.
for sizes in ([1], [1, 2, 3], [2, 2, 2]):
    p = sum(sizes)
    groups = []
    start = 0
    for size in sizes:
        groups.append(list(range(start, start + size)))
        start += size
    gid = np.empty(p, dtype=int)
    lam = rng.uniform(.05, .8, p) * rng.choice([-1, 1], p)
    if p > 1:
        lam[0] = 1e-7
    Psi = np.zeros((p, p))
    for i, g in enumerate(groups):
        gid[g] = i
        A = rng.normal(size=(len(g), len(g)))
        Psi[np.ix_(g, g)] = A @ A.T + .2 * np.eye(len(g))
    d = np.sqrt(lam**2 + np.diag(Psi))
    lam, Psi = lam/d, Psi/np.outer(d, d)
    Sig = Psi + np.outer(lam, lam)
    kap, cm, kp = kappa_cmin(lam, Psi, groups)
    assert abs(kap * math.sqrt(cm) - kp) < 1e-12
    for rep in range(6):
        xi = rng.normal()
        zeta = np.linalg.cholesky(Psi) @ rng.normal(size=p)
        gamma = lam * xi + zeta
        Q = [zeta[g] @ np.linalg.solve(Psi[np.ix_(g, g)], zeta[g])
             for g in groups]
        for mask in range(1 << p):
            T = [j for j in range(p) if mask >> j & 1]
            s = lam[T] @ np.linalg.solve(Psi[np.ix_(T,T)], lam[T]) if T else 0.
            hit = sorted(set(gid[T]))
            for l in set(range(p)) - set(T):
                z = innov(Sig, gamma, T, l)
                zd, _, Xi = decomp(lam, Psi, gid, groups, xi, zeta, T, l)
                bound = abs(Xi) + kp*abs(xi)/(1+s)
                if hit:
                    bound += kap*math.sqrt(sum(Q[g] for g in hit)/len(hit))
                err = max(err, abs(z-zd))
                violations += int(abs(z) > bound + 1e-10)
                pairs += 1
    # Exact covariance of the constructive posterior coupling.
    b = np.linalg.solve(Sig, lam)
    v = 1 - lam @ b
    A = np.zeros((p+1, p+1))
    A[0, :p], A[0, p] = b, math.sqrt(v)
    A[1:, :p] = np.eye(p) - np.outer(lam, b)
    A[1:, p] = -lam*math.sqrt(v)
    base = np.zeros((p+1, p+1))
    base[:p, :p], base[p, p] = Sig, 1
    target = np.zeros_like(base)
    target[0, 0], target[1:, 1:] = 1, Psi
    cov_err = max(cov_err, np.max(np.abs(A @ base @ A.T - target)))
print(f"exhaustive U(a)/final U(b): pairs={pairs}, max_identity_error={err:.3e}, violations={violations}")
print(f"posterior coupling covariance max_error={cov_err:.3e}")
# L1.0 with centred/standardised X, including T empty.
n, p = 17, 6
X = rng.normal(size=(n,p)); X -= X.mean(axis=0)
X *= np.sqrt((n-1)/np.sum(X**2, axis=0))
eps = rng.normal(size=n); R = X.T@X/(n-1)
g = X.T@eps/math.sqrt(n-1)
err0 = 0.; count0 = 0
for mask in range(1 << p):
    T = [j for j in range(p) if mask >> j & 1]
    for l in set(range(p))-set(T):
        r = X[:,l].copy()
        if T:
            r -= X[:,T] @ np.linalg.lstsq(X[:,T], X[:,l], rcond=None)[0]
        err0 = max(err0, abs(r@eps/np.linalg.norm(r)-innov(R,g,T,l)))
        count0 += 1
print(f"L1.0: pairs={count0}, max_error={err0:.3e}")
def sqrtm(M):
    w, V = np.linalg.eigh(M)
    return (V*np.sqrt(w))@V.T
# Noncommuting perturbations with growing pervasive-factor eigenvalue.
psi = .3; m = 3*psi/4; B = 1/math.sqrt(m)
C2 = (1+B)*(3+B*B)/(2*m**1.5)
C3 = (1+B)/math.sqrt(m)
L = C2 + 2*C3/psi
for p in (8, 32, 128):
    Sig = .7*np.ones((p,p)) + .3*np.eye(p)
    H = rng.normal(size=(p,p)); H = (H+H.T)/2
    np.fill_diagonal(H, 0.)
    H *= .04/np.linalg.norm(H, 2)
    R = Sig + H
    delta = np.linalg.norm(H, 2)
    sr, ss = sqrtm(R), sqrtm(Sig)
    mapdiff = np.eye(p)-ss@np.linalg.inv(sr)
    rootratio = np.linalg.norm(sr-ss,2)*(math.sqrt(np.linalg.eigvalsh(R)[0])
                 +math.sqrt(np.linalg.eigvalsh(Sig)[0]))/delta
    mapratio = np.linalg.norm(mapdiff,2)/(2*delta/psi)
    # Supremum over x is exactly the norm of this row-vector difference.
    mapping = ss@np.linalg.inv(sr)
    maximum = 0.
    for _ in range(80):
        l = int(rng.integers(p))
        rest = [j for j in range(p) if j != l]
        T = list(rng.choice(rest, size=int(rng.integers(p)), replace=False))
        def avec(M):
            c = np.linalg.solve(M[np.ix_(T,T)], M[T,l]) if T else np.empty(0)
            v = M[l,l]-M[l,T]@c if T else M[l,l]
            a = np.zeros(p); a[l] = 1; a[T] = -c
            return a/math.sqrt(v)
        maximum = max(maximum, np.linalg.norm(avec(R)-mapping.T@avec(Sig)))
    print(f"U(d) p={p}: opSigma={np.linalg.norm(Sig,2):.1f}, root_ratio={rootratio:.3f}, map_ratio={mapratio:.3f}, row_ratio_to_Ldelta={maximum/(L*delta):.3e}")
# Deterministic final simplification, including n=16, p=1, and bounded p.
rho_viol = 0; tested = 0
for n in (16, 1000, 10**12):
    ell = math.log(math.log(n))
    for p in (1, 2, 10, 100):
        for gb in (1, 2, 5):
            rho = math.sqrt(2*(2*math.log(2)+ell)+gb+
                  2*math.sqrt(gb*(math.log(math.e*gb*p)+2*math.log(2)+ell)))
            for G in range(math.ceil(p/gb), p+1):
                for h in range(1,G+1):
                    rh = (2*math.log(h+1)+ell)/h
                    ah = 2*math.log(math.e*G/h)+2*rh+gb+2*math.sqrt(gb*(math.log(math.e*G/h)+rh))
                    k = min(gb*h, p)
                    rhs = math.sqrt(2*math.log(math.e*gb*p/k))+rho
                    rho_viol += int(math.sqrt(ah) > rhs+1e-12)
                    tested += 1
print(f"U(c) final simplification: cases={tested}, violations={rho_viol}")
print(f"explicit L(psi0=.3)={L:.6f}")
```

Output:

```text
exhaustive U(a)/final U(b): pairs=2310, max_identity_error=1.776e-15, violations=0
posterior coupling covariance max_error=2.220e-16
L1.0: pairs=192, max_error=6.523e-15
U(d) p=8: opSigma=5.9, root_ratio=0.751, map_ratio=0.181, row_ratio_to_Ldelta=1.255e-02
U(d) p=32: opSigma=22.7, root_ratio=0.948, map_ratio=0.262, row_ratio_to_Ldelta=1.406e-02
U(d) p=128: opSigma=89.9, root_ratio=0.995, map_ratio=0.276, row_ratio_to_Ldelta=1.181e-02
U(c) final simplification: cases=26715, violations=0
explicit L(psi0=.3)=152.085723
```

These computations found no counterexample. They supplement the algebraic checks above and do not establish the probability inequalities by simulation.

