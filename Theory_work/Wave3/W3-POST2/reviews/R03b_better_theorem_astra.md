# R03b — BETTER THEOREM / sharpness gate

Reviewer: GPT-6 Astra, high. Scope: stronger candidate statements and bounded proof changes only; no correctness verdict on the submitted chain. All proposed conclusions below are asymptotic, in R1 with fixed s₀ and p ≤ n^A. Conditions are interfaces on (X, θ*); examples do not define theorem domains. Proposed results remain candidates until incorporated and checked.

Read: POST2 STATEMENT v1.1, ASSUMPTION_MAP, all five lemma files, post2_checks.py and its output; W3-POST STATEMENT and REPORT §§3–4; W1-T03R PROOF; locked T03 PROOF_v2 and T01/T02 PROOF_v3, particularly their Gaussian integral, smoother, numerator/denominator and assembly arguments.

## Recommendation and ranking

| Rank | Proposal | Value / bounded extra work | Risk | Could it be false? |
|---|---|---|---|---|
| 1 | C+: Eδ_n = O(r_n), under C's existing hypotheses | Removes the principal open rate issue; one denominator lemma | Low | Very unlikely: explicit argument below |
| 2 | D+: D(b) under (E), (F₀), (OS), with root-n variance contraction | Removes an entire floor hypothesis; one ridge-loss comparison | Medium | Unlikely with ridge loss; projection loss alone is insufficient for this proof |
| 3 | A+: exact moment weights and exact completion costs | Strictly weaker OS; bookkeeping and one existing integral | Low | Very unlikely |
| 4 | E+: c₁ reduced to about 54 for probability rate, about 60 also for expectation rate, at s₀=A=1 | Retune three conservative constants in E1 | Low–medium | Unlikely with strict margins; do not claim sharp constants |
| 5 | B+: optimized, growing reference cost and explicit exponential cost payment | Useful approximation/oracle statement; quadratic minimization and Gaussian tightness | Low | Very unlikely with the stated payment |
| 6 | E-floor+: replace F₀ by bounded ridge cost at S₀ | Broadens permissible degeneracy; three local replacements | Medium | Unlikely for probability conclusions; expectation requires separate care |
| 7 | D-transfer: integrated predictive Hellinger under an empirical/population norm interface | Short conditional corollary; verifying a design-law bridge is extra work | Low conditional / medium bridge | False without a transfer condition |

If only two changes fit the ticket budget, take C+ and D+. A+ is an inexpensive third. None requires new simulations or a new literature search.

## C — the expectation loss can be removed without changing the cutoff

**Proposed statement C+.** Under each of Claim C's current alternatives, uniformly with its fixed constants,

Eδ_n = O(√(log n/n)).

All C's decision-error and PIP expectation bounds inherit this rate. For random designs add P(𝒜_nᶜ), as already done in C. This is strictly stronger than n^{-1/2}exp(2√(2 log n)).

**Proof change: integrate the variance on the favorable side of σ*².** The exact-reference bound already used in C gives

Q⁽ᶜ⁾_{S₀} ≤ σ*² E′ + ρ,  E′=‖e‖²/σ*²,  0≤ρ≤ρ̄,

with deterministic ρ̄ under F₀ and E. In P1's denominator integral put u=v/σ*² and

F(u)=−N log(u)/2 + E′(1−1/u)/2.

F(1)=0 and F′(1)=(E′−N)/2. Integrate over [1,1+n^{-1/2}] if E′≥N, and [1−n^{-1/2},1] otherwise. On E′≤2N, Taylor's theorem gives F(u)≥−C throughout the chosen interval: the linear term is nonnegative and |F″(u)|≤C N on these intervals. Also −ρ/(2σ*²u)≥−Cρ̄/σ*². The fixed-rate IG density has a positive lower bound on [σ*²/2,2σ*²]. Consequently, on E′≤2N,

m⁽ᶜ⁾_{b₊}(S₀)/f₀(y_c) ≥ c D_{S₀}^{−1/2} n^{−1/2},

with a deterministic c>0. A data-dependent choice of integration interval is legitimate in a pointwise lower bound; the prior rate and numerator remain data-free.

Insert this in the **mixed-endpoint** inequality, preserving b₋ in the numerator. For any deterministic m_n,

Eπ(|S|>m_n) ≤ C R_{m_n}√D_{S₀}√n + O(n^{-1}) + O(e^{−c'n}).

Here the numerator identity EΘ⁽¹⁾=1 suffices, with no independence assertion. At the existing m♯_n the first term is O(n^{-1/2}). The other terms in C's proof are already O(r_n). This removes the sole offending factor.

**Risk / falsity.** Low. The remaining work is a short uniform Taylor bound and constant bookkeeping. The obstacle noted in C's remark about heavy prior-predictive variance tails is bypassed, not overcome by an unjustified Hölder argument. Enlarging m♯ would unnecessarily enlarge the domain of OS; this route preserves it. N5 is compatible with C+, but 20 seeds do not establish an expectation asymptotic or its constant 1.5.

## A — reduce both gaps to A2, but do not call A2 a characterization

### A+.1: exact rank weights

Write q_J=[w(s₀+j)/w(s₀)]√(D_{S₀}/D_{S₀∪J}) and replace a_J by

b_J = (τ_j/2)^{d_J/2}/Γ(d_J/2+1) for d_J>0; b_J=1 for d_J=0.

**Proposed statement.** A1 and E remain valid when their OS conditions use b_J instead of a_J (with a fixed common bound). This weakens the interface, especially on rank-deficient extensions and larger shells.

**Proof change.** Use the exact identity already proved in P3 lem:chi(b), rather than its gamma-function bound. Uniformly over j≤m♯=O(log n), jε_n=o(1), since ε_n=O((log n)^{3/2}/√n+(log n)^3/n). Thus exp(jε_n)=1+o(1) uniformly, and does not require 2^{j/2}. No new probability inequality is needed. All determinant/prior terms remain exact.

**Risk / falsity:** low; very unlikely false. This is a smaller sufficient envelope, not elimination of the logarithmic rank moments.

### A+.2: replace the amplified high-shell maximum by actual completion costs

For J outside S₀, j>j₀, let U=S₀∪J and define the deterministic quantity

H_J = Σ_{∅≠I⊆S₀, S=U\I∈Ω, |S|≤m♯} [w(|S|)/w(|U|)]√(D_U/D_S).

**Proposed statement.** Keep the first exact-weight OS inequality and replace the second by

Σ_{j>j₀, j≤min(m♯,p−s₀)} Σ_{|J|=j} q_J b_J H_J = O(r_n).

This is implied by current OS, since H_J≤(2^{s₀}−1)(2p)^{s₀}(n+1)^{s₀/2}, but can be substantially smaller. Together with A+.1 it is a strictly weaker sufficient interface for the same conclusions.

**Proof change.** In T03R C8 / E2, sum the completion prefactors before taking any maximum. Monotonicity Q_S≥Q_U bounds the likelihood component of ℓ(S)/ℓ(U) by one. The remaining factors are precisely the summands of H_J. Unions U outside Ω retain the algebraic score convention already used in the submitted chain. Then take the exact truncated moments term by term.

**Risk / falsity:** low; very unlikely false. Retaining a sum over at most 2^{s₀}−1 deletions is bounded work. Further localization by j or by I is available without introducing a new design family.

### Can the gap be closed completely?

Not by this proof at bounded cost. A2 ignores Gaussian likelihood gains and underfits. Its unweighted determinant sum cannot encode either the geometry of many noise projections or the cost of deleting truths from a completion. Exact truncated χ² moments really have logarithmic factors at the critical exponent 1/2. For finitely many supersets their likelihood factors are merely tight, so the logarithms are unnecessary for an O_P assertion; with a growing collection the maximum/sum behavior changes. Expectations can retain √log n even for a single regular null extension, through truncation of a heavy likelihood-ratio tail.

I would not assert “𝒪⁰_n=O(r_n) plus the existing bounded-excess ID suffices” for arbitrary designs. Risk high; plausible failure through large-excess underfits or accumulation of Gaussian gains. A fully geometry-sensitive Gaussian functional could encode a tighter interface, but would largely rename the quantity to be controlled. A+.1–2 are the useful cheap reduction.

## B — optimize the reference and allow its cost to grow

Let

L_T := inf_ϑ B_T(ϑ) = μ_cᵀ(I−M_T)μ_c,
ϑ_T^opt = n H_T^{-1}X_{c,T}ᵀμ_c.

These are deterministic functions of the design and mean, even when T is singular. The equality follows immediately from P1 lem:slab with Y=μ_c.

**Proposed statement B+.** For deterministic reference sequences T_n and μ with E, allow L_{T_n} to diverge. For every fixed ε>0,

π(|S|>m_n) = O_P( A^{T_n}_{m_n} exp{(1/(2σ*²)+ε)L_{T_n}} ).

In particular it is O_P(e^{−ω_n}) whenever

log A^{T_n}_{m_n} +(1/(2σ*²)+ε)L_{T_n} ≤ −ω_n.

This includes B when L_T is bounded, permits L_T=O(log n) with an explicit polynomial payment, and allows a deterministic oracle choice of T_n trading approximation, prior weight and determinant. Optimize over T before observing y; no unproved simultaneous/data-selected reference assertion is needed.

**Proof change.** Use B's argument with the minimizing ϑ. If r=μ−X_Tϑ, then ‖r‖²≤L_T and |eᵀr|=O_P(√L_T). In the existing denominator bound,

Λ″ ≤ L_T/(2σ*²)+O_P(1+√L_T).

Uniformly in L≥0, |eᵀr|/σ*²−εL is tight above: use |eᵀr|/σ*²≤√L |Z|/σ* and complete the square. The chi-square part is tight as well. Hence exp{Λ″−(1/(2σ*²)+ε)L_T}=O_P(1); multiply by the uniformly tight nonnegative numerator with expectation one. This also corrects the interpretation of the growing-cost remark into an operational asymptotic theorem.

**Risk / falsity:** low. The exponential payment is essential; dropping bounded cost while retaining an unmodified O_P(A_m^T) normalization can be false. An arbitrary poor reference, for example the empty model under substantial signal, cannot provide a cost-free denominator. C+'s stronger expectation argument directly covers exact references with bounded penalty; extending that expectation statement to arbitrary approximate references is separate work.

## D — remove F_λ and sharpen variance contraction

**Proposed statement D+.** Under R1, G, E, F₀ and OS, with no ID or beta-min, there is C such that for every M_n→∞,

Π(‖μ̂−μ‖²>C log n or |v/σ*²−1|>M_n/√n | y) →0 in probability.

Consequently the same fixed-constant squared Hellinger rate O(log n/n) in D(b) holds. This removes F_λ away from S₀ and improves the variance component to the parametric rate.

**Proof change: use ridge loss, not projection residual, to define near models.** Put L_S=μ_cᵀ(I−M_S)μ_c. Then

Q⁽ᶜ⁾_S = ‖e‖²−eᵀM_Se +2eᵀ(I−M_S)μ_c+L_S,
‖(I−M_S)μ_c‖²≤L_S,
Var(eᵀ(I−M_S)μ_c)≤σ*²L_S.

For U=S∪S₀, Q_U≤Q_{S₀}≤‖(I−P_{S₀})e‖²+R₀, with R₀=O(1) on the existing good event. Since M_S≤P_S≤P_U,

Q_S−Q_U ≥ L_S+2eᵀ(I−M_S)μ_c−σ*²χ²_{S\S₀}−R₀.

Thus E1's union bound and comparison proof apply with L_S replacing Δ_S, for bounded-excess models. They eliminate L_S≥Cσ*²log n. Large-excess underfits and strict supersets are handled by the existing OS assembly. Posterior mass therefore concentrates on S₀ and bounded-size models with L_S≤Cσ*²log n.

On this retained collection, uniformly,

‖M_Sy_c−μ_c‖² ≤2‖P_Se‖²+2L_S=O(log n),
Q_S=‖e‖²+O(log n).

The Gaussian fitted-mean covariance still has trace ≤v|S|, regardless of the spectrum. IG moments complete the mean argument. For variance, retain the common fluctuation ‖e‖²−Nσ*²=O_P(√n), instead of enlarging it to √(n log n). Since log n=o(√n), the posterior conditional means of v are uniformly σ*²+O_P(n^{-1/2}), and their variances are O_P(n^{-1}). This proves the claimed M_n/√n statement.

**Risk / falsity:** medium, primarily rewriting the retained set and uniform bounds; unlikely false. Merely applying E1 to Δ_S and then deleting F_λ from D1 would not control shrinkage bias in a nearly singular fitted model. L_S fixes precisely that issue. No coefficient contraction is claimed without an appropriate floor.

### Integrated/out-of-sample corollary worth stating

Introduce an explicit prediction-law interface, conditional on the training design: for every vector a supported on S∪S₀ for the retained bounded-size models,

E_{x∼ν_n}[(xᵀa)²] ≤ C_ν ‖Xa‖²/n.

The feature coordinates in ν_n must use the same centering/scaling as X. Under this interface on events of probability tending to one, replace the empirical mean loss by its integrated version in D0. D+ gives integrated squared Hellinger contraction at log n/n. Under selection, D(a) gives the oracle rate with diverging multiplier, using the transfer only on S₀. Convexity of squared Hellinger in the first density also yields consistency of the posterior predictive mixture; a mixture rate requires additionally controlling the excluded posterior mass at that rate.

This is a design-agnostic transfer theorem, with iid Gaussian/sub-Gaussian designs only possible bridge examples. It does not assert that the in-sample assumptions alone imply out-of-sample prediction. An unseen direction can have small empirical norm and large population norm. State the centered-response target explicitly; an intercept posterior is not furnished by the contrast model. Risk low for the conditional corollary, medium for proving a new bridge, false without any transfer restriction.

## E — substantially smaller constants, and a route past F₀

### E+.1: asymptotic constants at essentially the same proof cost

Set h=s₀(A+1/2). For any fixed η>0 let a=Aj₀+η. A sufficient replacement threshold for the probability-rate conclusions is

c > c_new(η):=(√(2a)+√(4a+2h+1))².

For probability conclusions η can be arbitrarily small, so it suffices that c>(√(2Aj₀)+√(4Aj₀+2h+1))². For the expectation conclusion C+, take η=1/2, with the strict c inequality absorbing lower-order terms (or η slightly larger if preferred).

At s₀=A=1, j₀=4 and h=1.5, these limiting thresholds are about 53.30 and 59.14, respectively, versus 160.8. Conservative rounded statements c>54 and c>60 are convenient.

**Proof changes, all local to E1:**

1. Use x_n=(Aj₀+η)log n+O(1); the bounded-excess family has O(n^{Aj₀}) elements. Its Gaussian cross-term exceptional probability is O(n^{-η}).
2. For j≤j₀, fixed rank, the exact χ² tail bound gives a simultaneous upper bound [2(Aj₀+η)+o(1)]log n. Replace C_Aj₀ by this coefficient. Retain the original high-shell event/weights for OS.
3. The completion prefactor is n^{h+o(1)}, not n^{s₀(A+1)}. Only an n^{-1/2} underfit factor is needed for the r_n result, rather than n^{-2}.
4. From the resulting lower bound D≥[c−2√(2ac)−2a−o(1)]σ*²log n, evaluate the monotone likelihood penalty at that lower bound. Since it is O(log n), νlog(1+D/B′) is at least [c−2√(2ac)−2a−o(1)]log n/2. This uses the local expansion at the lower bound, not an unjustified uniform expansion for arbitrarily large D. Solve for a coefficient exceeding h+1/2.

For expectation control the new bad events must be O(r_n), which explains η≥1/2. For O_P control it is enough that they vanish. Preserve this distinction when stating the improved theorem.

**Risk / falsity:** low–medium. These constants are sufficient candidates, not an optimal boundary. The algebra is explicit; the remaining cost is checking the revised event and assembly exponents. Do not automatically attach expectation bounds to the smallest probability-only threshold.

**Why not simply c=4?** N4 has fixed p and s₀=1, while the theorem covers p up to n^A and many competing subspaces. Even a single deletion has log posterior odds approximately (log p)+(1/2)log n−Δ/(2σ*²)+O_P(√Δ/σ*). Thus the probability-rate obstruction occurs around Δ/(σ*²log n)=2a_p+2 when log p∼a_p log n, with a strict margin needed. A universal c=4 at A=1 would already sit at that deletion boundary. Fixed-p numerical success at 4 does not establish a worst-design polynomial-p threshold. Reaching constants close to this obstruction would need weighted testing/fractional moments rather than a maximum over all bounded-excess models; that is higher risk and outside the cheap proposal.

### E-floor+: replace F₀ by bounded ridge cost on the truth

**Proposed probability theorem.** In E's probability conclusions, replace F₀ by

L₀:=μ_cᵀ(I−M_{S₀})μ_c=O(1),

with a common bound, keeping E, OS and the original strict ID margin (or a separately checked E+ margin). This is implied by F₀ and E, and also by the weaker coefficient-cost condition (‖μ‖²+‖θ*‖²)/n=O(1). No minimum eigenvalue on S₀ is stipulated.

**Proof changes.** Let A₀=P_{S₀}−M_{S₀} and R₀=y_cᵀA₀y_c. Since rank(A₀)≤s₀, 0≤A₀≤I and μ_cᵀA₀μ_c=L₀, E R₀≤L₀+σ*²s₀, hence R₀=O_P(1) uniformly. Use

Q_{S₀}=‖(I−P_{S₀})e‖²+R₀,
Q_{S₀}−Q_{S₀∪J}≤σ*²χ²_J+R₀.

The superset comparison has an additional common exp{O_P(1)} factor, so its OS-controlled sums remain O_P(r_n). E1's loss comparison subtracts R₀=O_P(1), negligible relative to a strict log n margin. B with the optimal reference at S₀ supplies the size tail because L₀ is bounded. The same ridge-loss proof should extend D+'s mean/variance conclusions to this interface.

**Risk / falsity:** medium. This is a genuinely weaker condition and a bounded proof rewrite. Do not transfer C+'s expectation result by saying exp{O_P(1)} has bounded expectation: that inference is false at critical Gaussian exponents. The probability theorem does not need it. Also do not retain D(a)'s coefficient root-n claim under this replacement.

**Can F₀ be deleted with no substitute at all?** I would not recommend that assertion. E controls fitted energy, not the cost of representing signal in an extremely small singular direction. The working ridge prior can heavily penalize that direction; projection ID does not measure that penalty. A bounded signal-weighted ridge cost is a much more plausible interface than unrestricted deletion, and captures the actual proof need without prescribing a design family.
