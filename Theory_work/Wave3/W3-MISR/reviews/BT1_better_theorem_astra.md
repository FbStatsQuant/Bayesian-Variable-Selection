# BT1 — Better-theorem review

Blind review of W3-MISR v1.1. All claims below are conditional on the input results at the status declared in the target. I read the brief, the target and assumption map, PROGRAM, W3-POST's statement, and W3-POST2's statement and five permitted lemma files. I did not follow their links into reviews or other excluded material.

There are **3 class-A proposals, 2 class-B proposals, and 0 class-C proposals**. Ranked by value/cost: A1, A2, B1, A3, B2. The numbering below groups them by class. These are extensions of the coded target, without changing its prior, standardisation, or cap.

## A — Present route, with a few lines

### A1. Replace Gaussian contrasts by their projective law for model-selection conclusions

**Exact statement.** Fix x and a reference configuration κ=(x,β,v). For a nonconstant response define

    T(y^r) = zzᵀ/‖z‖²,   z=Uᵀy^r.

Let Z=μ_c/√v+g, g~N_N(0,I), and T_G=ZZᵀ/‖Z‖². Replace GR^c by

    Law(T(y^r)) = Law(T_G).

Then the law of the entire model posterior is exactly the law in R′(b)'s unit-noise comparison model. Consequently §§2–3 hold unchanged. Selection-error bounds hold for any mode selection as already bounded in §2; equality of the selected mode's law presumes a tie rule that is a function of the posterior.

More generally, if d_TV(Law(T(y^r)),Law(T_G))≤ε_n, every expectation bound for a [0,1]-valued function of the model posterior acquires at most ε_n. Thus

    E[1−π(S₀)] ≤ C r_n + ε_n,

and, for example, P(HPM≠S₀)≤2(C r_n+ε_n), uniformly over reference configurations and laws with this discrepancy bound. The same transfer applies to bounded posterior-loss quantities in §3. Here TV is sup over events.

Conditionally, it is enough that the analogous conditional projective law given κ_n has discrepancy at most ε_n(κ_n). One need not assume a Gaussian standardised residual independent of a larger, preselected σ-field. On a configuration-good event A_n measurable with respect to κ_n,

    E δ_n ≤ C r_n P(A_n) + E[ε_n(κ_n)1_A_n] + P(A_n^c).

**Improvement.** R′(b), §§2–4, and §9's non-Gaussian exclusion: strictly weaker law assumption, plus stability under approximate laws. This is design-agnostic and leaves the full polynomial range of p intact.

**Proof.** By the score in W3-POST §0, standardised contrasts have length √N; every response-dependent score term is a quadratic form in these contrasts. Hence π=F_x(T) for a measurable F_x. Apply equality of pushforwards, or contraction of TV under F_x and the bounded-function characterization of TV. Apply W3-POST2 C and the §3 assemblies, then condition on κ_n. No new probability inequality is needed.

**Strictness and boundary.** For any positive, possibly Z-dependent random R, take Uᵀy^r=RZ. This generally gives non-Gaussian contrasts with nonscalar covariance, but the posterior agrees sample by sample with that from Z. This is a genuine enlargement of admissible sampling laws. In this extension β is a *reference target*: it need not be the conditional-mean coefficient of the new law. The assertion is not that arbitrary nonscalar Gaussian residuals or iid heavy tails are harmless. T is the maximal invariant for response shifts and nonzero rescalings; its law is sufficient, not claimed necessary for equality of posteriors for a particular x.

The raw-scale parameter posterior does not factor through T: random radial changes rescale θ and v′. Therefore this proposal does **not** transfer R′(b)'s parameter-posterior equality or Corollary H around the original fixed (μ,v).

**Cost/risk/current route.** A few lines; very low falsehood risk with this model-versus-parameter distinction. Already implicit in R′(a) and the score formula.

### A2. Uniform expectation contraction, including quantitative posterior-tail bounds

**Exact statement.** Keep GR^c and the original configuration classes. Write Bad_a(t) for the union in §6(a) with M_n replaced by t≥1, and Bad_b(t) for the union in §6(b) with M_n replaced by t. For all sufficiently large n, with constants uniform over the respective configuration classes and over v>0,

    sup_{κ∈K_n} E_κ Π(Bad_a(t) | x,y^r) ≤ C(r_n+t^−1),
    sup_{κ∈K_n^0} E_κ Π(Bad_b(t) | x,y^r)
        ≤ C(r_n+(log n)^−1+t^−2).

The first statement also holds on K_n^λ with its appropriate margin threshold. C_H in Bad_b can be the constant from D3 after unit-noise reduction. In particular, for every deterministic M_n→∞ these posterior probabilities converge to zero **in expectation uniformly**, not just in probability along a fixed configuration sequence. Hellinger consequences include

    sup_{κ∈K_n^0} E_κ Π(h̄_n²>(1+C_H/4)log n/n | x,y^r)
        ≤ C(r_n+1/log n),

and

    sup_{κ∈K_n} E_κ Π(h̄_n>M_n/√n | x,y^r) → 0.

All these inequalities transfer conditionally as in §4(a), adding the probability of the configuration-bad event after averaging.

**Improvement.** §6 and its random-design scope: stronger mode of convergence, uniformity, and explicit posterior-tail rates. These concern expectations of bounded posterior probabilities, not expectations of unbounded parameter losses.

**Proof.** Reduce to v=1 by R′. For D2, on S₀ the integrated conditional-posterior mean-square prediction error is bounded uniformly: use D1(a,b), E‖P_{S₀}e‖²=s, bounded L_{S₀}, and the IG mean. Also

    E E_Π[(v′−1)² | S₀,y] ≤ C/n.

This follows from D1(c,d), Gaussian second/fourth moments, b=b₀‖μ_c+e‖²/N, and the fixed energy bound. The floor gives an integrated coefficient-square error ≤C/n. Markov then gives respectively C/t, C/t², C/t²; the wrong-model contribution is at most Eδ≤Cr_n by Claim C. This is the first display.

For D3 let S_good={S₀}∪{S∈F:L_S<(c₁+1)log n}. Its outside mass has expectation ≤Cr_n: use Lemma C2 and (C5′)(b), and take expectations in E2's restricted underfit assembly. On D3's event of failure probability ≤5/n, uniformly over S_good the conditional posterior prediction-tail bound is C/log n, exactly as displayed in D3. For variance, D3 gives a common bound on the conditional-mean deviation by |‖e‖²−N|/(n−1.98)+C log n/n and conditional variance ≤4/n. Squaring and integrating yields C/n, since log² n/n²≤C/n. Thus the variance tail contributes C/t²; charge the exceptional event its probability. D0 gives the Hellinger displays (take t=√log n in the no-margin bound).

**Cost/risk/current route.** A few lines of Gaussian/IG moment bookkeeping; low risk. The estimates already appear in D1–D3 and C. For each fixed sequence expectation convergence alone follows immediately from boundedness, but the uniform finite-n tail bounds require the displayed bookkeeping and are the actual improvement.

### A3. State posterior localisation directly, and trim OS for the superset-only clause

**Exact statement.** Under the hypotheses of §3, set c₂=c₁(s,A)+1 and

    G_n(κ)={S₀}∪{S∈F(κ): L_S(κ)<c₂ v log n}.

Then uniformly in κ∈K_n^0,

    E_κ π(G_n(κ)^c) ≤ C r_n.

In particular E_κ π(|S|>s+j₀)≤Cr_n. Thus even without a margin almost all posterior mass is on a bounded-size family with small ridge approximation loss, not merely on models that avoid being strict supersets.

For the narrower assertion §3(a), retain SZ, E^σ, F₀ and **only the first OS inequality**, O_n^{>0}≤C_OS r_n. The amplified second inequality is unnecessary for

    E_κ π(S⊋S₀)≤Cr_n.

**Improvement.** §3 and the support component behind §6(b): stronger no-margin conclusion; weaker hypotheses for §3(a).

**Proof.** The first assertion is precisely D3's mass-outside-S_good proof with expectations: C2 controls the size tail, (C5′)(b) controls strict supersets, and E1/E2 control the large-loss underfits. The second OS inequality is needed for the last step for underfits with large excess, but not for strict supersets. For the latter, the bound is just the size tail plus e^{ρ_n}Υ′_n on the good event. Its expectation uses only (C5′)(b) at i=0. All constants are common over the configuration class, and R′ restores v.

**Cost/risk/current route.** A few lines; very low risk. Present route already gives both assertions. The localisation is not an assertion of false-positive exclusion: small-loss proxies can still have posterior mass.

## B — A new lemma or explicit extension is needed

### B1. Add the empty-projection case, under only a null-anchored Occam condition

**Exact statement.** Let β=0, v>0, 2≤p≤n^A, and GR^c hold. Define w,q,R_m,m♯_n as in W3-POST §0 with s=0 (so R_m=Σ_{k>m}q_k/w(0), and m♯ is the first m≥0 with R_m≤n^−1). Define O_n^{>0} with anchor ∅, D_∅=1 and d_J=rank(X_J), retaining the same a_J as POST2. Assume only

    O_n^{>0}≤C_OS r_n.

Then for n sufficiently large,

    sup E[1−π(∅)]≤C r_n,
    P(HPM≠∅) ∨ P(MPM≠∅)≤2C r_n.

There is no F₀, energy, margin, beta-min, or amplified OS requirement. Also, for every M_n→∞,

    sup E Π(S≠∅ or |v′/v−1|>M_n/√n | x,y^r)→0,

and the centred oracle Hellinger contraction follows. Conditional versions allow zero among the finitely many support-size slices in §4(b).

**Improvement.** §§2,4,6 and §9's explicit s=0 exclusion: wider scope, especially complete cancellation/zero projected signal.

**Proof route/new step.** This needs a null-anchor extension lemma because POST2 C and E formally assume s≥1. Prove C1 directly with Q_∅^c=‖e‖², ρ=0, D_∅=1; its Taylor integral bound and C2 then give Eπ(|S|>m♯)≤Cn^−1/2+O(n^−1). In (C4′) with anchor ∅, there is no reference-smoother error at all: M_∅=P_∅=0. The score gain is bounded by the projected noise energy, and the denominator good-event bound uses only Gaussian noise. Repeat (C5′) with d_J=rank(X_J), then sum. Every nonempty model is a strict superset, so there is no underfit assembly and no use for OS's second inequality. Given ∅, the fitted centred mean is exactly zero and v′ has the IG law in D0 with b=b₀‖e‖²/N, giving the variance bound by elementary χ² moments.

**Cost/risk/current route.** A new short boundary-case lemma; low risk. The existing algebra supplies it but the declared s≥1 input theorems cannot simply be invoked at s=0. This also combines with A1: under a uniform projective contrast direction the null model-selection conclusions need neither Gaussian radial distribution nor moments of that radius.

### B2. Add a design-agnostic fresh-covariate Hellinger theorem under selection

**Exact statement.** Keep the selection hypotheses of §6(a), and let Q_n be a distribution of fresh raw candidate covariates. Specify the target conditional response law

    y_new | z ~ N(a+zᵀβ,v),  z~Q_n.

Let x̄ be the training column means, d(z)=D_x^−1(z−x̄), and suppose

    E_{Q_n}‖d(z)_{S₀}‖²≤L

with a fixed L (or on configuration events with probability tending to one and common L). Suppose also

    (ȳ^r−a−x̄ᵀβ)/√v=O_P(n^−1/2).

For posterior draw (S,θ,v′), define the predictor N(ȳ^r+d(z)_Sᵀθ_S,v′), and its integrated squared Hellinger distance h_out² from the stated target by averaging over Q_n. Then for every M_n→∞,

    Π(h_out>M_n/√n | x,y^r)→0 in probability.

A sufficient quantitative version of the intercept assumption is E(ȳ^r−a−x̄ᵀβ)²/v≤L/n; paired with the uniform configuration assumptions, it yields uniform expectation convergence of this bounded posterior-tail probability. These are conditions on the covariate second moment and intercept error; no design family appears in the theorem.

**Improvement.** §6(a), §5 and §9: integrated fresh-covariate contraction, making a closer comparison to a density theorem over the covariate distribution. It is a selection-based result, not a no-margin prediction theorem.

**Proof route/new step.** On S=S₀ write the prediction error as the intercept error plus d(z)_{S₀}ᵀ(θ−θ*). By Cauchy–Schwarz and the new moment-transfer condition,

    E_Q (prediction error)²
        ≤2(intercept error)²+2L‖θ−θ*‖².

Integrate the normal Hellinger inequality D0, use D2's coefficient and variance contraction, and charge the entire S≠S₀ contribution to δ. For uniform expectation convergence use A2's integrated conditional-on-S₀ moment bounds. The new lemma is this training-to-population prediction transfer, including the intercept.

In the Gaussian-row example §5(b), the assumptions are checkable: sample variances on the fixed true support concentrate around Σ_jj; E_Q‖d(z)_{S₀}‖²=Σ_{j∈S₀}[Σ_jj+(m_j−x̄_j)²]/D_{x,j}²=O_P(s), and the regression residual mean has variance v/n. Apply the event-localised version. The fresh conditional Gaussian law is the projected law in §5(a).

**Cost/risk/current route.** A new short transfer lemma; low risk with both added conditions. The current route gives the training coefficient rate, but does not supply a fresh covariate law or control an arbitrary intercept under GR^c. Neither addition can be silently omitted. Without selection, a sparse prediction-transfer condition for the posterior-supported unions would be needed; that is not asserted here.

## Limits on further improvements

### Do not delete E^σ from the whole theorem on the basis of N4

A concrete obstruction exists even for selection, not just variance contraction. Take two centred orthogonal standardised columns with G=NI₂, v=1, θ₁=n and θ₂=√(c log n/n), where c is any fixed positive constant. Then s=p=2, K=2 eventually, F₀ holds, and OS is vacuous because there are no columns outside S₀. Every underfit has L_S at least the ridge contribution of the first signal, of order n², or its omitted energy of order n³. Thus ID^{M,σ} holds for any fixed margin constant eventually. Even the projection margin holds for sufficiently large c.

For an orthogonal column the smoother eigenvalue is m=nN/((n+1)N+1)=1−Θ(1/n). In raw contrast units,

    2b+Q^c_{ {1} }=Θ_P(n²),
    Q^c_{ {1} }−Q^c_{ {1,2} }=O_P(log n).

The n² denominator includes the first signal's ridge residual and the coded b=b₀s_y² term. Consequently

    log[m({1,2})/m({1})]=−½ log n+o_P(1).

The prior odds are a fixed positive constant (p=2), so π({1,2})≤π({1,2})/π({1})→0. Dropping E^σ while retaining the other stated conditions would therefore give a false selection theorem. The retained first signal also forces posterior residual variance far above v. This is a boundary calculation, not a proposal for a design-family theorem.

A weaker energy-growth assumption may be possible, but requires accounting for the coded score's signal-dependent ridge/IG residual scale. I do not claim a replacement here. N4 is not evidence for uniform unrestricted-energy validity.

### Other interfaces

F₀ might be weakened to conditions on reference ridge loss and smoother error for selection and prediction. However bounded reference cost alone does not immediately recover the vanishing remainder in (C4′); coefficient contraction additionally needs identifiability on S₀. I have no checked low-cost replacement for F₀ across all clauses. The weighted OS condition can be trimmed for the superset-only/null results above, but its wholesale removal is incompatible with POST2 A2's deterministic necessary Occam mass. I do not propose improved p range, growing s, unrestricted heavy-tailed noise, or almost-sure contraction from the present inputs.

Finally, §4(c)'s tight-constants assumption yields Eδ_n→0 by boundedness, but supplies no universal expectation rate. A quantitative bound is obtained by minimising §4(a)'s C_η r_n+P((A_n^η)^c) over admissible envelopes and their onset thresholds. Without a rate for those probabilities and constants, this is an envelope formula rather than a new r_n theorem; I have not counted it as a proposal.
