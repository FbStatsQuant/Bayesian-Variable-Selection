# LIT-PAR notes 08: Syed et al. global barrier Lambda == O-STAGES path length L (overlap check)

Source READ: local Papers/Core_bibliography/02_2026_Syed_et_al_*.pdf = arXiv:2408.12057v2 (2 Dec 2025), Syed, Bouchard-Côté, Chern, Doucet,
"Optimised Annealed Sequential Monte Carlo Samplers". (notes/03 B2 read v1/arXiv download; this is v2.)
- Quoted (eq. 25): "For MCMC forward kernels with quasi-reversal backward kernels, G_beta and delta(beta) reduce to the Fisher score and
  Fisher information for the annealing distributions: G_beta(x,x') = d/dbeta log pi_beta(x), delta(beta) = Var_beta(d/dbeta log pi_beta)."
  The local barrier "generalises the standard deviation of the energy statistic (Gelman and Meng, 1998; Grosse et al., 2013; Rotskoff, 2017;
  Chopin et al., 2024; Chehab et al., 2023; Barzegar et al., 2024)"; Lambda = integral_0^1 lambda(beta) dbeta; "the optimal schedule
  phi* ... is the geodesic between eta and pi ... the constant-speed reparameterisation of the annealing path of length Lambda."
- For OUR bridge gamma_phi = gamma_0 e^{phi d}: d/dphi log gamma_phi = d, so with MCMC moves lambda(phi) = sd_{q_phi}(d) and
  Lambda = integral_0^1 sd_{q_phi}(d) dphi, which is EXACTLY O-STAGES' L (O-STAGES REPORT §1 item 4: "sqrt(c) T*(c) -> L =
  integral_0^1 sd_{q_phi}(d) dphi as c -> 0").
- IMPLICATION (threat, partial): O-STAGES item 4 (fine-grid limit) is the ESS-adaptive-grid version of a KNOWN thermodynamic-length
  fact (Gelman-Meng 1998 path sampling; Syed et al. Thm 3: lim T Var[Z^/Z] = E(phi)/N >= Lambda^2/N). It should be presented as
  consistent with / a corollary-type analogue of the known result, citing Syed et al. and Gelman-Meng. NOT new.
- What is NOT in Syed et al. (and survives): O-STAGES items 1-3 — exact monotonicity/optimality of the greedy ESS grid for finite V, the
  identity rho(u,v) = q_u q_{2v-u}/q_v^2 and the halving law, and the COARSE-grid law T* = log2 A0 + O(1) for masked crossings, where
  O-STAGES shows L <= pi while T* -> infinity (so Lambda does NOT determine the stage count at the production ESS threshold).
  Syed et al.'s regime analysis is for T -> infinity (dense) under an idealised performance model (Assumptions 2-4: temporal and particle
  independence, efficient local exploration), which is exactly what fails in the masked regime. This is a genuine, citable contrast:
  "for coarse ESS-adaptive grids on masked starts the stage count is governed by the start's masking depth A0, not by the barrier Lambda".
