# R02: better-theorem / sharpness review

Reviewer: independent statistics/theory reviewer, 2026-11-09. Scope: statement improvements for the method as coded, not a line-by-line proof audit. Read STATEMENT v2, ASSUMPTION_MAP, CODE_CHECK, L1–L5, relevant L6 arguments, PROGRAM and the requested Wave2 excerpts; checked the specified engine, core and R assembly code. No code or other project file was changed. No subagents used.

## Verdict and ranking

**Strictly better provable statements exist.** The best improvement is a geometric replacement of the model-count noise bound. It preserves design-agnosticism and every polynomial range of p, and sometimes extends screening all the way to K−1. Next, retain the actual score threshold and the model-specific residual/noise scales. For specificity, print a necessary condition on the excess set using the normalized dual Gram matrix, rather than presenting near-orthogonality as necessary in kind. Finally, the already printed scan scores give an uncertified-run screening statement with a quantitative score-gap condition.

Classes: (1) provable now with a short argument; (2) plausible but needs real work; (3) false as an unconditional claim, or presently unsupported. Probabilities below refer to provability of the stated proposal with a short proof, not to the probability of successful recovery.

## 1. Geometric noise complexity instead of counting all models — class (1), 99%

Let H be any deterministic collection of models of size at most K−1. Write H− for its members missing a truth. Choose one missing truth t(S) deterministically from (X,θ*) for every S in H− (the existing maximum-gain witness suffices). Define

    v_S = R_S x_t / sqrt(a(t|S)),
    d_S = −sign(x_t'R_S μ) v_S,
    D = {0} union {d_S : S in H−}.

Signs at zero can be chosen arbitrarily. All vectors are centered and have norm at most one. For g ~ N(0,I_n), define the deterministic Gaussian width

    w(D) = E max_{d in D} d'g,     L(D) = max_{d in D} ||d||.

Set, for M=|H−|>0,

    b(x) = min{sqrt(2 log M + 2x), w(D) + L(D)sqrt(2x)}.

Empty H− is vacuous. The first bound is one-sided: the extra factor 2 inside the logarithm in E1 is unnecessary. Each of the two displayed deterministic bounds is valid at failure probability e^(−x), so their deterministic minimum is also valid at that probability; this does not require a union bound between them. Gaussian concentration applies because max d'g is L(D)-Lipschitz. Consequently, simultaneously over H−,

    sqrt(g_yc(t|S)) >= sqrt(γ(t|S)) − σ b(x)

whenever the right side is positive. Indeed the signed observed correlation is at least this right side. Only unfavorable noise needs bounding.

**Statement.** If

    min_{S in H−} sqrt(γ(t(S)|S)) > τbar_n(x)sqrt(T_n) + σ b(x),

then with probability at least 1−3e^(−x) every LO member of H contains S0. This includes all certified endpoints in H, simultaneously for all seeds. Proof: replace E1 by the preceding event and reuse L3 verbatim.

For all sets of size at most q, this weakens SCR-A: b(x) is never larger than its r_n(q,x). It is strictly better on admissible designs. As an illustration only, take one true column orthogonal to every nontrue column, with arbitrarily many nontrue columns in its orthogonal complement. Then v_S is the same vector for every S missing the truth, regardless of q; b(x)=O(1+sqrt(x)). Fixed nonzero signal, polynomial p, and q=K−1 satisfy the new margin eventually, even when the old sqrt(q log p) margin fails. This illustration works at p much greater than n and need not be a design family in the theorem.

**Cost.** A deterministic geometric functional replaces a crude combinatorial functional. It is not necessarily easy to calculate, but Γ and Ψ already require optimization over models. A usable bound is w(D)≤E||P_Vg||≤sqrt(dim V) if D lies in V with norms at most one. Covering numbers of D give further bounds. Neither the theorem nor these sufficient conditions name a design family.

For SCR-A°, do the same separately for the cross-term vectors R_Sμ/sqrt(μ'R_Sμ), including zero. The cross-term width is a different functional and must not silently be replaced by the witness width. Alternatively, Section 2 avoids the common normalized scale altogether.

## 2. Exact addition threshold, residual scale and size-adaptive hypothesis — class (1), 99%

This is a genuinely weaker hypothesis even before the geometric improvement. For k=|S|<K define

    B_St = log((2p−1−k)/(k+1)) + (1/2)log D(t|S),
    h_St = ((n+1)/n) [1−exp(−B_St/ν)].

Here B_St≥0. The exact necessary and sufficient condition for a strictly improving addition is

    g_yc(t|S) > h_St [0.02 τhat² + q_S(y_c)].                 (A)

Use b(x) from Section 1. Let c(x) be a valid simultaneous upper bound, at failure e^(−x), for μ'R_Sε/(σ m_S), where m_S=sqrt(μ'R_Sμ), over H−; either the one-sided counting bound or the separate cross-term width works. Put a=sqrt(x/(n−1)) and

    U_S = 1.02 τbar_n(x)²
          + n/(n+1) [m_S² + 2σ m_S c(x)
                     + σ²(n−1)(1+2a+2a²)].

**Statement.** If for each S in H− its chosen witness satisfies

    sqrt(γ(t|S)) > σ b(x) + sqrt(h_St U_S),                (M)

then every LO member of H screens with probability at least 1−4e^(−x). Proof: E2+ and the cross-term event imply 0.02τhat²+q_S(y_c)≤U_S; the witness event and (M) imply (A). Union bound: 2+1+1, exactly as in SCR-A°.

This retains the actual k-dependent prior, determinant, exponential threshold, and σ/σ_S noise ratio. The present theorem replaces all four by upper bounds. In particular, with the original witness and counting bounds, MC° implies (M); (M) can hold when MC° fails. One can also use the deterministic bound (n−0.98)τbar² for the raw residual denominator and take the smaller of it and U_S on the same event. The original MC then implies this version too.

**Costs and range.** No new stochastic assumption, no design family, no change to code. The functional is longer. It removes the need to impose ||μ||=o(nσ) as a blanket condition for this theorem: the unavoidable total-response contribution is retained explicitly, rather than required to vanish relative to σ². It does not assert invariance to arbitrarily large strong coefficients. The coded score contains the 0.02τhat² term and the ||y_c||²/(n+1) term, so some dependence on total scale is real.

Use H defined by a deterministic acceptance rule in (X,θ*) and the printed size, rather than forcing an initial interval {0,…,q}. One may alternatively apply the theorem by size with x_k=x+log(π²(k+1)²/6) and sum the failure probabilities. This gives simultaneous size-adaptive guarantees at an O(log k) confidence cost. A hypothesis involving ||μ|| and σ is understood in the same fixed-noise-scale convention as the current statement.

**Printed gap consequence (direction f).** Under (M), let G_S=(sqrtγ−σb)² and define

    δ_S = −B_St + ν [n/(n+1)] G_S/U_S,

if this lower bound is positive. A sharper positive bound is

    δ_S = −B_St + ν log(1/[1−nG_S/((n+1)U_S)]),

when the fraction lies in [0,1). Then F(S+t)−F(S)≥δ_S on the same event. If the fraction were at least one, a deficient S on that event would be impossible since its gain cannot exceed its raw denominator. Prefer a uniform positive δ lower bound if a simple printed rule is desired.

Every completely scanned center C has all its neighbors in the ledger. Therefore, on a completed run, any such C in H with

    fit$hpm_F − F(C) < δ

must contain S0. This holds even when the top-level flag is false and neither search endpoint is certified. Intersect these qualifying centers to obtain a screened set. Their models and scores are already printed in the search archives. This conclusion concerns the centers, not an unscanned near-tie HPM. It strictly extends the useful output of the same high-probability event. Probability of short proof: 99%; cost: a stronger quantitative margin to obtain δ>0.

## 3. Characterize and bound excess variables without the near-orthogonality floor — class (1), 98%

L5 already contains nearly all the proof. Promote its dual-direction geometry and keep the exact individual deletion penalties. For S=S0 union E, k=|S|≤q, m=|E|≥1, use the augmented design from L1.7. Let M_E be the Gram matrix of the columns in E residualized on the augmented true columns, N_E=diag(M_E^(−1)), and

    ω_E = λmax(N_E^(−1/2) M_E^(−1) N_E^(−1/2)),
    B_j = log((2p−k)/k) + (1/2)log D(j|S\{j}),
    cθ = ||θ*||₂/sqrt(n+1),
    H_k = [sqrt((1−2sqrt(x/(n−1))−U(k,x)/(n−1))_+)
           −cθ/(σsqrt(n−1))]_+².

Every matrix exists because of the ridge augmentation; no unaugmented eigenvalue floor is assumed. On E2chi∩E3a∩E3b, **every LO strict superset** satisfies

    (n−1)H_k sum_{j in E} [exp(B_j/ν)−1]
       <= ω_E [sqrt(U'(m,x')) + cθ/σ]².                    (E*)

The failure probability is at most (1+2q)e^(−x)+e^(−x')/(1−e^(−x')). Combine with a screening event when describing certified models.

**Proof.** Non-improving deletion gives the exact bound

    g_yc(j|S\{j}) >= ((n+1)/n)(0.02τhat²+q_S(y_c))
                     [exp(B_j/ν)−1].

Here B_j≥0 for k≤K≤p. L5's residual lower bound, which does not itself use φ, gives q_S(y_c)≥n/(n+1) σ²(n−1)H_k. Sum over E. The exact dual-frame inequality in L5 gives

    sum g_yc(j|S\{j}) <= ω_E ||P_{W(E)}(εtilde−btilde)||²
                         <= ω_E (σsqrt(U')+cθ)².

Divide by σ². This proves (E*).

**Precise controlled-excess conclusion.** Let A be the deterministic family of nonempty E disjoint from S0, |S0 union E|≤q, satisfying (E*). On the joint event, each certified C of size ≤q has C\S0 either empty or in A. In particular

    |C\S0| <= max({0} union {|E|: E in A}).

If A is empty, exact recovery follows. This is an explicit, possibly computationally expensive, characterization; it is not a universal small bound. It can rule out large excess sets while permitting strongly correlated small ones. Since (E*) retains the exact quantities that L5 bounds by φ and uses exp(u)−1≥u, it gives at least the existing EC exclusions with the same events, and potentially strictly more.

**Simple asymptotic exact-recovery sufficient condition.** Retain screening, s0=O(1), q log p=o(n), ||θ*||₂=O(σsqrt(n)). Suppose uniformly over strict supersets through q,

    min_j a(j|S\{j}) >= c(n−1),  c>0,
    ω_E <= (2 log p + log n)/(2 log p) − ε,  ε>0.

Then exact recovery follows by L5's size-aware argument with ω_E in place of 1/φ; log c is only O(1) in the determinant penalty. For polynomial p in the intended p≫n regime, the prior's log k correction is offset by the log m term in the excess-set union bound, as in L5. This separates conditional column lengths from angular dependence. It does not require a near-one minimum eigenvalue of the whole superset Gram matrix. The finite statement (E*) is preferable when s0 grows or endpoint geometry varies.

**Important qualification.** The isolated L5 remark asserting an ω-only replacement omits a condition retaining the determinant penalty. ω bounds angular geometry of normalized dual vectors, not their lengths. Keep the conditional-length hypothesis above, or use (E*) directly. Near-orthogonality of the full Gram matrix is sufficient, not established as necessary. Probability: 98% for (E*), 95% for the asymptotic simplification under these stated extra conditions.

## 4. Swaps and the cap via exact quadratic contrasts — class (1) theorem; class (2) useful primitive corollary

There is a general, short, design-agnostic theorem covering the *entire coded neighborhood*, including |S|=K. This is not a promise that old anchored-floor assumptions alone suffice at K.

Let h(S)=log w(|S|)−(1/2)log det H_S+(1/2)log det(G_S+I). On the centered subspace put

    A_S = I − n X_S H_S^(−1)X_S' + 0.02 I/(n−1).

Then 0.02τhat²+q_S(y_c)=y_c'A_S y_c. For a deterministic chosen neighbor N(S), set

    B_S = A_S − exp((h(S)−h(N(S)))/ν) A_{N(S)}.

Exactly, F(N(S))>F(S) iff y_c'B_S y_c>0. For a deterministic class H− of deficient models, including sizes up to K, choose one legal neighbor per model. All choices must be functions of (X,θ*,σ), not noise. Let M=|H−| and z=log(2M)+x. Set Bc=C B_S C. A sufficient condition for every S in H− is

    μ'B_S μ + σ² tr(Bc)
      > 2σ ||Bc μ|| sqrt(2z)
         + 2σ² ||Bc||_F sqrt(z) + 2σ² ||Bc||op z.          (Q)

**Statement.** Under (Q), with probability at least 1−e^(−x), no member of H− is LO; hence every certified endpoint in H screens, even at K. Proof: expand the quadratic into mean, Gaussian linear term and centered Gaussian quadratic term. A one-sided Gaussian bound and the standard Gaussian quadratic mgf bound each fail with probability at most e^(−z); sum over M models. The stated operator-norm term is conservative for an indefinite matrix but valid. This mgf bound follows directly by diagonalizing Bc and bounding the log mgf of each weighted centered χ²_1 term.

Probability of short proof: 99%. Cost: a stronger-looking but different, matrix-valued deterministic margin. It exploits equal-size swaps without paying an addition's full prior penalty and can detect a truth masked by a proxy. It also allows deletion witnesses if appropriate. It is not automatically weaker than MC, so present it as an alternative, or take the logical union of the two sufficient hypotheses. No two-step algorithm is assumed.

**Class (2), 65%.** Turn (Q) into an attractive primitive swap-visibility condition with a materially larger q range under permissive correlation. The quadratic difference can have cancellations; bounding its two gains separately can destroy the benefit. A complete primitive corollary and a strict parameter-range example need real work. Do not present a generic masked-proxy rescue theorem as already proved.

## 5. Cleaner primitive bridge: directional restricted curvature — class (1), 99%

The anchored floor controls *all coefficient directions* on every missing true subset. The proof only needs the realized direction. Define

    κ_dir(q;θ*) = min_{|S|≤q, S not containing S0}
       ||(I−P_S)X_T θ*_T||² / [(n−1)||θ*_T||₂²],
       T=S0\S.

**Statement.** All of B2 and B2°, and hence A1/A1° with their existing other assumptions, remain true replacing φ^a(q)≥κ by κ_dir(q;θ*)≥κ. Proof: the only use of the anchored eigenvalue in L4 is Δ(S)≥κ(n−1)||θ*_T||₂². This is precisely the displayed condition. Everything afterward is scalar algebra. This is a directional restricted-eigenvalue condition, strictly weaker than the anchored floor. It can stay positive while a different direction on T is singular. It is particularly appropriate because theorem hypotheses are expressly allowed to involve θ*.

Cost: coefficient dependence and potentially difficult minimization. It is simpler to interpret but not uniformly easier to verify on all pervasive-correlation designs. Do not substitute global coherence or a near-isometry requirement: they sacrifice the project's leading priority, design-agnosticism. Existing sparse-floor implication remains a useful conservative verification route. A general, materially easier verification method for realized pervasive-correlation designs is class (2), 60%, not established here.

## 6. Explicit answers to directions (a)–(g), and rejected shortcuts

**(a) Accept controlled excess, reject unconditional exact recovery.** Section 3 gives a precise excess-set characterization and induced cardinality bound. Local deletion stability is informative even when SCR-C's floor fails. A short unconditional O(s0) or o(q) excess bound does not follow from the present screening argument; correlated noise directions and joint deletion barriers remain possible. HPM dominance only compares models actually scored. Neither it nor near ties proves that S0 or all subsets of HPM were scored. The Wave2 aside saying the certificate enumerates all subsets is not the current engine's semantics: it scans single flips and swaps. That aside cannot justify an as-coded theorem. No new counterexample to every possible cardinality bound is claimed here.

**(b) Accept extension through K−1 under geometric margins; accept K under (Q); reject unconditional removal.** Section 1 gives a strict extension example with p≫n. SCR-A itself already permits q=K−1 whenever its functional margin holds; the cn/log p limitation belongs to the convenient primitive corollary, not the finite theorem's formal domain. At K the addition proof stops, but swaps/deletions still exist. Thus “K exclusion is necessary by construction” is too strong unless explicitly limited to an addition-only argument. Size can be replaced by a deterministic acceptance family and by the printed scanned-center score-gap condition, not by the number of observed scans alone.

**(c) Accept geometry, exact binomial entropy and peeling; reject sample-size counting of adaptive endpoints.** Use log(sum binom(p,k)), or size-specific log binom(p,k), instead of q log p when retaining a counting theorem. This improves constants and sometimes ranges but is already implicit in finite SCR-A. Gaussian width can remove the q factor altogether on favorable geometry. Local optimality and HPM status alone do not make chosen directions independent of the noise. A proof that counts just two endpoints or just the realized number of scans is invalid without additional selection analysis. I do not claim a matching sqrt(q log p) lower bound for arbitrary LO endpoints; the current sharpness result proves only the q=0 threshold.

**(d) Accept exact swap contrast; generic swap improvement is class (2).** Section 4 handles actual legal moves and could be less restrictive than Γ/Ψ. Exact duplicate truth/proxy columns give an obstruction to label recovery: swapping them preserves the score, and no data can identify the original label. Arbitrarily close duplicates require a quantitative contrast/noise separation. Allowing an improving two-step route without an improving legal first move would not establish the coded certificate theorem.

**(e) Accept directional curvature; no universal easy verification shortcut.** Section 5 gives the short stronger bridge. Sparse eigenvalues remain convenient but unnecessarily strong. Coherence/isometry routes discard the designs this ticket is meant to reach.

**(f) Accept scanned-center near-best screening.** Section 2 yields a new assertion even for uncertified completed runs. Already-certified endpoint intersections are not new. An arbitrary unscanned near-tie model has no inherited certificate; its score proximity alone does not control its missing truths.

**(g) Tighten the headline and remove overclaims.** A1° is not generally beta-min at sqrt(log p/n): its printed requirement is sqrt(((q+1)log p+log n)/n), becoming that rate for bounded q in the polynomial p≫n regime. Likewise “no bound on total signal” should be qualified: A1° explicitly bounds ||μ|| relative to nσ and controls ||θ*||₂ relative to θ_min. Keep SCR-N but describe it as sharpness of the empty-model threshold, not of the entropy penalty, anchored-floor necessity, or HPM recovery. SCR-R is a useful optional refit remark, not a principal as-coded output theorem; its prediction bound needs no eigenvalue floor once screening holds if the refit is defined by orthogonal projection/pseudoinverse. The coefficient bound still requires identifiability. Proof of that minor refinement: fitted mean is P_Cy_c and its error is P_Cε for every C containing S0, singular or not; apply E3a. Probability 99%, no extra assumptions, but low priority.

## Recommended paper disposition

Prefer a concise geometric, model-specific screening theorem (Sections 1–2), keep anchored/directional curvature as transparent sufficient conditions, and keep the original MC as an easy-to-read conservative corollary. Add the scanned-center consequence because it uses existing printed information. Promote (E*) as the honest specificity statement; retain SCR-C as a simple sufficient exact-recovery specialization. Put the general contrast theorem in an appendix unless a useful primitive swap corollary is developed. Do not delay the screening result to solve that harder problem.

The core contribution remains unchanged: a reported-model guarantee with no start-mode or leakage hypothesis, valid at p≫n and stated only through deterministic signal/design quantities. The improvements above strengthen that contribution rather than replacing it with a theorem for a narrower design family.
