# General-assumption interface for HQ / W2-UNI

This maps assumptions in XA proof files; it is not a consistency theorem.

L1_geometry: iid Gaussian raw rows, independent Gaussian noise, population
correlation matrix with GLOBAL eigenvalue floor c>0. No factor representation
is needed. The proof controls all subsets, including large ones; a floor only
on log-size subsets does not supply its hypotheses. The conservative Gram bound
uses fourth moments and a Frobenius estimate; the noise coupling uses Gaussianity.
For p<=n^a,a<1/3 its simultaneous same-model residual-statistic discrepancy
vanishes. This does not imply control of the adaptive model sequence.

L4_score_transfer: deterministic near-identity linear coupling and subspace
projection bound, GLOBAL floor, fixed bounded signal l1 norm, positive residual
energy comparable to n, pL_n=o(n). No factor or locality structure is needed.
It applies only to pairs of truth-containing models. The prospective coupling
rate is o_P(1) at a<1/4. It does not establish truth-out control or start mode.

L2_robust_path_attempt: transfer-by-margins is general, and BAL/FG/majority bounds
are deterministic scalar facts. The reference score formulas, common centre,
Gaussian order-statistic events, and exact end-phase mechanism are CS-specific.
The path theorem is conditional on prefix geometry and gain approximation;
those inputs are not assumptions already established by W2-UNI A1–A3.

L3_fuzzy_attempt: deterministic scalar approximate-nearest deletion, with an
anchor denominator m+s+kappa and s+kappa>1. It neither needs iid rows nor supplies
a multivariate k-factor analogue. The width bound is too weak to close XA's
target; no necessity of that rate loss is claimed.

For A2 (fixed k factors plus local Psi), a uniform GLOBAL floor of Psi supplies
the global floor required by L1/L4, provided the full correlation covariance
inherits it. Locality alone without a quantified global floor is insufficient.
A3 beta-min/non-masking is relevant to start/truth protection, but these have
not been assembled in XA. The scalar path result cannot be relabelled a general
k-factor result. Gaussian raw rows are stronger than unspecified iid rows.
