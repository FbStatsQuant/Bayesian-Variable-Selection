# Notes 05: Moreno–Girón–Casella 2015; Sparks–Khare–Ghosh 2015; model-prior papers 2025–2026; BCG review

## Moreno, Girón & Casella (2015), Statistical Science 30(2) 228–241, doi:10.1214/14-STS508 (arXiv:1507.08041). READ: arXiv PDF.
- Thm 3, quoted: "(i) When sampling from M_t and k = O(n^b), the Bayesian procedures for the Bayes factors B^{g=n}_{j0}, B^{Mix}_{j0},
  B^{IP}_{j0} and the Bernoulli model prior are posterior model consistent for 0 ≤ b < 1/2 and posterior model inconsistent for 1/2 ≤ b ≤ 1.
  (ii) When sampling from M_t and k = O(n^b), the Bayesian procedures for the Bayes factors B^{g=n}_{j0}, B^{Mix}_{j0} and B^{IP}_{j0} and the
  hierarchical uniform prior are posterior model consistent for 0 ≤ b ≤ 1."
- Bayes factors are computed against the null model M0 ("j0"); k = number of regressors, k ≤ n (b ≤ 1). Proof via large-n approximations
  (Lemma 1), not a non-asymptotic argument.
- Bearing on T03♯: the unit-information g = n prior + a size-hierarchical (BB(1,1)) model prior is posterior-model consistent up to k ≍ n.
  T03♯ extends the same qualitative message to p = n^A with A > 1 (beyond MGC's b ≤ 1) and to BB(1,p), at the price of SE/BM conditions.
  It also matches MGC's negative part: g = n + a flat (Bernoulli ½) model prior is inconsistent for b ≥ ½ (cf. JR 2012 Thm 2).

## Sparks, Khare & Ghosh (2015), Bayesian Analysis 10(3) 627–664 (arXiv:1509.01060). READ: abstract + theorem list.
- Necessary and sufficient conditions for posterior consistency of the COEFFICIENTS (sup-norm) under g-priors (non-hierarchical, EB,
  hyper-g, Zellner–Siow), p growing at the rate of n. Not selection; complementary.

## Berger, García-Donato & Pericchi, "On model prior probabilities in variable selection" (arXiv:2603.19728v2, Sept 2026).
## READ: Papers/Priors_and_decision_rules/Berger_GarciaDonato_Pericchi2026_Model_prior_probabilities.pdf
- Restricts to size-only model priors: quoted "We only consider prior specifications that depend on the dimensionality of γ, that is,
  Pr(M_γ) is a function of |γ|". Defines weak parsimony (M_k(d+1) ≤ M_k(d)) and strong parsimony (per-model prior non-increasing).
  Lemma 3 (SP for Beta-mixtures iff ∫ p^{k−1}(1−2p)π(p)dp ≥ 0).
- Quoted (§2.6): "Wilson et al. (2010) proposed π(p) = Beta(p | 1, k) and Castillo et al. (2015) suggested π(p) = Beta(p | a, k^u), for
  certain a > 0 and u > 1. Since the means of these priors are decreasing at least as fast as O(1/k), they force concentration on very
  small models, which we would not label objective."
- Bearing: our BB(1,p) = Wilson et al.'s Beta(1, k) choice, which this 2026 paper explicitly classifies as "overly parsimonious" from an
  objectivity viewpoint — a REFEREE-ATTACK POINT on the fixed size prior (Felipe's decision), not on any theorem. Also, the whole paper
  lives in the size-only class to which T07(i) applies; it does not state the within-size ceiling (searched for "within", "same size":
  not found in the parts read; absence not proven).

## Womack, Taylor-Rodríguez & Fuentes, "The matryoshka doll prior" (arXiv:1511.04745v4, Apr 2025). READ: abstract + statement list.
- Quoted: "This isomorphism yields the Poisson distribution as the unique limiting distribution over model dimension under mild
  assumptions. We compare this model space prior theoretically and in simulations to widely adopted Beta-Binomial constructions."
- Bearing: another size-only (in the limit) prior; complementary. Note BB(1,p)'s dimension law ≈ Geometric(½) (ratio (p−s+1)/(2p−s)),
  a heavier tail than Poisson(log(1+1/η)).

## Banerjee, Castillo & Ghosal, "Bayesian inference in high-dimensional models" (review; arXiv:2101.04491v3, 23 Jun 2026).
## READ: arXiv PDF §3 (linear regression).
- Summary of CSvdV, quoted: "it can be shown that no proper superset of the correct model can be selected with appreciable posterior
  probability. It is, however, possible to miss signals that are too small in magnitude. If all non-zero signals are assumed to be at least
  of the order √(s0 log p)/‖X‖, then none of these signals can be missed ... Thus, the selection consistency follows."
- Confirms that the dimension → no-superset → beta-min architecture of T03♯ is the field's standard template.
