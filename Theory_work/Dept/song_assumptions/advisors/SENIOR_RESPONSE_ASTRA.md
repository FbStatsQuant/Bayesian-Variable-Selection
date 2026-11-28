# Senior discussion — drafting advisor Astra

## Q1 — Amend. Adopt the population theorem with a stratified proof.

**Replacement wording.** “For the coded BB prior let h_d=log[π(T∖D)/π(T)]+(d/2)log(n+1)=Pr_n(d). Let Q_n⊇T be deterministic with log|Q_n|=o(log n). For each feasible underfit S write B=S∩Q_n, N=S∖Q_n, b=|B∖T|, m=|N| and k=b+m. Impose the population margin on k≤m̄, restricting to |S|≤min(J,K) in the proof. For one fixed η>0 require
√R_n(B)/σ ≥ (1+η)√(2h_d) and, for m≥1,
√R_n(S)/σ ≥ (1+η)√(2h_d)+a(B,N)√(2 log binom(p−|Q_n|,m)).
State the B⊂T, m=0 inequality separately as U1.” The larger count binom(p−s,m) also works. The proposal's generic prior ratio has its sign reversed. Keep the coded price; for arbitrary priors a deletion refund at T need not upper-bound the refund at T∪(S∖T).

U2a with proxies is sufficient and can be stringent: it charges the full deletion refund even though the b proxies pay for entry. U1 alone does not imply U2a. Do not call κ_n for pure deletions the exact U2a ratio. Using (1+η) on the **root** scale in both displays fixes the claim about vanishing leakage: with the same η as originally printed, √(1+η)<1+η even at zero leakage. With common root slack and max ϑ log p→0, U2a implies U2b with any smaller fixed positive slack. Q_n=T means every null is checked by the outside-proxy inequality; it does not assert zero leakage.

**Replacement for the bridge.** “W bounds the Gaussian loss simultaneously within each base B. Applying this bound before summing containing-model odds proves TS-b.” For fixed B,m, R_n(B) is common, so the N giving smallest R_n(S) also gives largest a(B,N). Across B, the smallest residual and largest width can occur at different bases. The proposed pointwise inequalities therefore do **not** establish the existing global minimum-versus-global-width hypothesis. Keep that hypothesis as a parallel sufficient condition. If a literal implication is wanted, impose the minimum and maximum across bases separately; that strengthens the assumption unnecessarily.

For the direct proof let H be the number of bases, H≤2^s Σ_{b≤m̄} binom(|Q_n|−s,b)=n^{o(1)}, and let G_m=binom(p−|Q_n|,m). Take l_n=log(H+1)+t_n with t_n→∞, t_n=o(log n). Conditionally on X, with probability 1−O(e^{-t_n}), simultaneously over B and N of the indicated sizes,
−⟨v_S,g⟩ ≤ √(2l_n)+‖v_S−v_B‖√(2[log G_m+l_n]).
This is two one-sided Gaussian union bounds, permitting arbitrary dependence. The surplus over a(B,N)√(2 log G_m) is o_P(√log n) by Q2. Positive fixed root slack absorbs this surplus and the relative error in R̂. Thus uniformly F_S/F_{T∪(S∖T)}≤O_P(n^{-γ}) for some sufficiently small γ>0: the fit loss exceeds h_d+γ log n and the coded refund is ≤exp(h_d). Sum the containing odds **once at total null size k**; for fixed D each null set gives exactly one S. No probability or BF multiplier of order H is required in that sum.

On the retained sieve, m̄<k≤J gives log total odds ≤[s(A+½)−k/2]log n+O(log log n)+O_P(1) per bounded class, by the containing-model sum and nonnegative nested coded fit gain. This is ≤−log n+O(log log n)+O_P(1) with the proposed m̄. The tail beyond J still needs prop:dist(i) under its own assumptions. This identifies the available exponent; γ is not arbitrary.

## Q2 — Agree on the coefficient; amend the fallback.

**Replacement wording.** “For positive residuals r_V=(I−P_V)μ and B⊆S, ⟨r_S,r_B⟩=‖r_S‖². Hence ‖v_S−v_B‖²=2(1−√(R̂(S)/R̂(B))).” This yields the stated population coefficient exactly. It improves the looser 2√ϑ bound. For the same common B, the mean Gaussian term along v_B is zero; for a maximum across bases it costs the √(2l_n) above.

Uniform two-sided relative isometry on T∪S gives R̂(S)/R̂(B)≥[(1−δ)/(1+δ)]R_n(S)/R_n(B), so ϑ̂≤ϑ+2δ/(1+δ) and â²≤a²+2[1−√((1−δ)/(1+δ))]. Thus â≤a+O(√δ) uniformly, including near zero leakage. For fixed s,m̄, take δ_n=C√(log(n∨p)/n) with C sufficiently large, so the event has probability tending to one even for bounded p. Center raw columns and use relative SUBG. Only feasible T∪S with size ≤s+m̄ are needed after the total-size restriction.

“Use the direct unit-vector bound √(2 log G_m) as an alternative to the common-base difference bound. The structure-free coefficient is **1**; √2 is merely a looser upper bound on the chord length.” One can use min(1,a) by intersecting the two simultaneous Gaussian events. At literal ϑ=1 the rival has zero residual and its normalized direction is undefined. With unit-vector fallback, C-ii follows from R/σ²≥nφ²d θ_min² for population-standardized effects in noise units and Gram control on T∪S. If using √2 instead, the proposed C-ii constant does not establish that fallback. C-i also works: the null count, price and squared noise allowance are all O(log n).

## Q3 — Amend the quantifier; endorse both screening forms.

**Replacement wording.** “For each fixed admissible M and each designated j, impose inf R_n(S)/(σ² log n)≥C_L M over its retained omission rivals, with C_L larger than the inverse separation constant (adjusted for the radius convention). A diverging ratio on the omission sieve for every fixed M gives screening at every such fixed level. A sufficiently large fixed level gives the almost-sure corollary.” The diverging-ratio version may lead, provided “every M” reads “every fixed admissible M.” Divergence at an unspecified speed gives no uniform result for M=M_n→∞. The fixed-level version matters for finite-ratio signals.

## Q4 — Amend the attribution; agree on recorded/open status.

**Replacement wording.** “For fixed s, the recorded A-BS′ is equivalently V=Var(xᵀβ)/σ²=O(1) and E=Σ_j β_j²Var(x_j)/(nσ²)=o(1). A weaker proof target is V=O(1) alone under NEC on T.” Fixed s gives equivalence of the coordinate maximum and sum in the recorded o(1) clause. My R1 sufficient energy pair asked for E=O(1); it did not require o(1). Under NEC, V≥c_ψ E, so bounded V already implies the bounded pair, while E→0 does not follow. If using “bounded R²,” write R²=V/(1+V)≤1−c: the ordinary bound R²≤1 says nothing. Retain A-BS for statements invoking the delivered size lemma until the energy-only reissue is checked.

## Q5 — Amend §0 in four places.

* **0.4.** Write “BB gives an effective prior-tail cutoff of the same order as SL's proposed sieve”; it still must pay the true-model denominator and does not inherit SL's entropy conditions. Link SL (3) to BS under standardized columns and fixed positive noise scale. SL's Gaussian sufficient floor is a precedent for vanishing floors; NEC at 1/n does not supply their screening separation.
* **0.7.** Every fixed c·log n suffices for fixed levels only. Preserve q_n(M) for the delivered theorem with varying M, and the enlarged q_n for TD′ even at fixed M. Require common constants L,c_ψ if claiming uniformity. Distinguish this stronger fixed-level presentation from the original theorem.
* **0.8.** Keep a price-scale restriction for the O_P(1) boundary expansion, e.g. h_1=O(log n) under A-DIM. State the two-sided transfer rate needed to replace sample by population at a finite boundary offset. The minimal first-order converse and the local boundary remainder have different requirements.
* **0.11.** Give the conditioning set and omitted-signal coefficients in each worked formula. Leakage depends on both for multi-deletions. The assertion that U2a holds on S1 “with the exact κ_n” requires minimization also over inside proxies. One adjacent proxy correlated with a deletion residual already lowers that rival's R; the pure-deletion calculation cannot certify equality.

**Remaining referee questions (three).** (1) Which retained classes and posterior tail bounds give the advertised γ for the coded cap? (2) What analytic or exhaustive evidence verifies U2a and the outside leakage jointly for the claimed design sequence? (3) How could TD′ pay its O(M log p) testing budget on a sieve with log binom(p,q_n) much larger? Keep TD′ a high-risk conjecture.
