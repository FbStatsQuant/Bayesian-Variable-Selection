VERDICT: ERROR

Here `P` abbreviates `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md`. The error is an omitted dimension restriction in B(ii); the intended bounded-size applications and the substantive population, Haar-span, and residual calculations pass.

| Claim / step (path:line) | Verdict | Reason |
|---|---|---|
| F2, F3, F5 (P:43-58) | VERIFIED | The rank-one cross covariance gives Cov(X_b, x_a)=ψ Cov(X_b,x_b), hence Cov(X_b,μ_i)=0. Also Σ_ab−Σ_a,a_h Σ_a_h,b=0. Gaussianity gives the claimed conditional independence; block-diagonal component covariance gives F5. |
| F4 (P:56) | VERIFIED | Whitening each equicorrelation block gives a linked-pair matrix with diagonal I and cross block ψuvᵀ, where u,v are unit vectors. Its minimum eigenvalue is 1−|ψ|. Congruence by the within-group square roots gives λ_min≥(1−|ψ|)(1−ρ); independent null/visible blocks have minimum 1−ρ. |
| P2(a) (P:213-219) | VERIFIED | On the supplied correlation-tail event, the error is at most |T|δ_n in operator norm; with |T|=O(log n), this is O((log n)^(3/2)/√n)=o(1). Interlacing and Weyl give λ_min(R̂_T)≥λ₀/2 simultaneously. This also covers the enlarged O(log n) range in P8_T03sharp.md. The correlation-tail lemma itself was not reviewed here. |
| P2(b),(c), R, G (P:216-220) | VERIFIED | The finite signal covariance matrix and SDs converge by SLLN: ‖μ‖²/n→θᵀΣθ and θ*_j→θ_j. The positive fixed beta minimum gives the stated diverging M_n. R additionally uses s₀≤min(p,⌊n/2⌋) eventually. Gaussian noise remains independent under conditioning on the raw design. |
| B(i) (P:222-234) | VERIFIED | In b-groups U=∅ and F2 applies to every subset, including correlated proxies. In a-groups conditioning on j_a invokes F3; visible groups contain their true hub; null groups use F5. The residual dimension is n−1−|U_h°|, giving the stated Beta parameters, eventually in n. |
| B(i′) (P:224,228-234) | VERIFIED | F3 plus weak union allows conditioning on additional a-group members; visible hubs already determine their signal contribution. Null-group residuals remain independent of the response. There are no neutral b-group candidates. With one added column, the second parameter is (n−2−|U|)/2. |
| B(ii), unrestricted A (P:225) | ERROR | The population partial-independence argument is correct, but arbitrary neutral supersets can have |A|≥n−2 when p≫n. The claimed Beta law then has a nonpositive second parameter; for |A|=n−1 its defining RSS ratio is undefined. See finding 1. |
| B(iii) (P:226,233-234) | VERIFIED | F2 makes every masked hub independent of y^r; F5 makes the hubs independent across pairs. Conditional on y, their centered unit directions are independent uniform directions in dimension n−1. Thus their squared correlations are independent Beta(1/2,(n−2)/2), even unconditionally, and multiplication by n−1 gives the joint independent χ²₁ limit. |
| Λ(a), finite signal part (P:315-316) | VERIFIED | θ*=D_xθ accounts for standardization exactly. The finite-dimensional sample covariance/SD limit and invertibility of each population principal submatrix give simultaneous convergence over at most 2^(gs₀) signal subsets. Replacing n−1 by n is harmless. |
| Λ(a), projection identity and Haar step (P:317-320) | VERIFIED | The added residual span is orthogonal to span X_As, so nested orthogonal projection gives exactly the stated squared-norm identity. Correlation, centering and SD scaling do not disturb the Haar span; derivation below. |
| Λ(a), uniform null bound (P:320-323) | VERIFIED | Discard empty A₀ and zero-residual cases (their improvements are zero). For all remaining terms Tr-J(c) has j=|A₀|≤J=s₀+2, u=|A_s|≤J, D=A(s₀+2), fixed C. Intersect its event with P2(b): Λ_As≤‖μ‖²≤Mn gives max improvement≤Mnτ_n=O(log n). Independence between these events is unnecessary. |
| Λ(b),(c) (P:308-314,323-326) | VERIFIED | Component conditional variances add by F5. The displayed closed forms and missing-hub lower bound follow from the computations below. |

1. **ERROR — B(ii) lacks a rank/dimension hypothesis (P:225).** Take an allowed sequence with p≥n and sufficiently many neutral columns. Choose a deterministic A containing S° with all other members neutral and |A|=n−2; choose another neutral l outside A. Positive definiteness of the population covariance implies that the centered A columns have rank n−2 and the augmented columns rank n−1 almost surely. Consequently RSS_A>0 almost surely (σ²>0) but RSS_{A+l}=0, so x_{A,l}=1 almost surely, whereas the displayed Beta(1/2,0) is not a probability distribution. With |A|=n−1, RSS_A=0 and the ratio is undefined. **Accepted repair:** state B(ii) for deterministic A,l satisfying |A|≤n−3 (and n sufficiently large); alternatively restrict A to feasible models |A|≤K and explicitly take n large enough. For the general Haar calculation require |U|+|W|≤n−2. B(i),(i′) meet this eventually because g is fixed. No change to the intended small-set applications is needed.

2. **Verification detail — Haar span (P:230-232,317-319); no defect.** Conditional on X^r_SV, write the raw null submatrix as GΣ_A₀^(1/2), with G an independent n×j iid standard Gaussian matrix. Σ_A₀ is positive definite even when A₀ contains multiple members of one null group. For an orthonormal basis Q of E=1^⊥⊖span X_As, with m=n−1−|A_s|, QᵀC=Qᵀ and

   QᵀΠ_As^⊥X_A₀ = (QᵀG)Σ_A₀^(1/2)D_A₀^(-1).

   The right factors are invertible almost surely; D_A₀ may depend on G without affecting this pathwise span equality. Conditional on the signal design, QᵀG is m×j iid Gaussian, hence its span is a Haar j-plane. The same conditional law holds when conditioning only on standardized X_SV, since it does not depend on the omitted signal SDs. For fixed nonzero r=Π_As^⊥μ, its projected energy fraction is Beta(j/2,(m−j)/2). This proves both the claimed Lambda law and the corresponding B laws: in B replace null columns by their Gaussian population regression residuals. Zero partial covariance makes those residuals independent of (X_U^r,y^r). All these assertions concern deterministic index sets; none conditions on selection or partition recovery.

3. **Verification detail — Λ(c) and its lower bound (P:311-326); no defect.** Suppress i and put q=1−ψ². Then Var(μ_i)=β²q and Cov(μ_i,x_b)=0, giving the empty/b-hub forms. Given x_a, μ_i has residual −ψβ(x_b−ψx_a), so its variance is G=ψ²β²q. An a-group nonhub contributes nothing by F3. For a b-group proxy l, Cov(x_b,x_l|x_a)=ρq and Var(x_l|x_a)=1−ψ²ρ², yielding G[1−ρ²q/(1−ψ²ρ²)]. Thus η has the stated value and lies in (0,1). Both hubs determine μ_i. The visible singleton residual is 1−ρ². Finally, for any B⊆K_i,

   λ_i(B)=min_a Var(μ_i−aᵀX_B) ≥ λ₀ min_a ‖θ_i−ι_Ba‖² = λ₀‖θ_{i,K_i\B}‖².

   If j_a∉B this is λ₀β_i²(1+ψ_i²1{j_b∉B}); the argument even holds without the stated |B|≤2 restriction.

A-dependence: After the explicit B(ii) domain repair, all reviewed conclusions hold for every fixed A≥1, including A>1. P2 needs an O(log n) size coefficient depending on A and the supplied δ_n constant/onset; the product still tends to zero. Λ(a) uses D=A(s₀+2), threshold τ_n=8(D+1)log n/n and fixed family factor 2^(gs₀)2^(s₀+2). Thus the null improvement bound is 8M(D+1)log n. Population and Beta identities do not depend on A; constants and onsets may, and no uniformity over A is asserted.

---
## Disposition (W1-PXN lead, 2026-11-08)
ERROR accepted (Lemma B(ii) as stated is false for |A| ≥ n−2). Repaired by the reviewer's own domain restriction
(lemmas/B_ii_domain.md, ERRATA E-7); B(ii) is not used downstream, so no conclusion of the theorem is affected. Repair to
be re-checked by a NEW cross-family reviewer. Everything else in I3 VERIFIED, in particular report item #3 (Lemma Λ(a)
Haar-span step with equicorrelated null groups): VERIFIED (finding 2 gives the full derivation). P2(a) VERIFIED given
[CONC′] (I9 checks lemmas/CR_corr_tails.md).
