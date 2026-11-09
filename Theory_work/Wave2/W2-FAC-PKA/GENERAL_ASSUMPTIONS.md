# Ingredient map for the design-agnostic main theorem

HQ framing update received 2026-11-09. This ticket supplies component lemmas/instances, not a CS-specific replacement for the paper's main theorem. No restart, no claim that the general main theorem has been proved. The map records actual proof inputs and prospective extensions separately.

## L0 rank frontier

Uses only centering and positive definiteness of the proposed full Gram. Not a statistical consistency condition. For iid rows with p>=n, population covariance may be positive definite even though the sample Gram is singular; L0 places no restriction on such a main theorem.

## L1 saturation: actual ingredients

Current draft is fixed-design exact CS. The proof uses:

1. Uniform concentration of sample response cross-products and response energy around their population-scale counterparts.
2. A fixed positive eigenvalue floor for all predictor sets of size at most 16 (and bounded response energy). The population partial-covariance interpretation can instead be checked on sets of size at most 16+s0.
3. A strictly positive lower bound on the absolute conditional covariance of each selected visible null with the signal, conditioning on any truth-free set U of at most 15 other variables; equivalently, a conditional-correlation floor after bounding residual variances. This is a visible-null assumption, NOT truth beta-min or truth non-masking.
4. Enough visible nulls outside the at most s0 truth-containing blocks: at least K. In the CS instance all nulls are visible and p-16s0>=K suffices.
5. Block size bounded by 16, the shipped block-product tables, the stated score, and log p=o(n) so the prior increment cannot defeat a fixed order-n table increment. The present proof specializes p<=n-1; any broader dimension claim needs concentration rechecked.

Exact CS is used in the current proof to verify these ingredients, especially the visible-null floor. The logic is not based on a global Gram inverse, independence of retained signs, or a residual chi-square with n-p degrees of freedom. It does not use an LS0 cap or prove truth inclusion.

## Population-level formulation to seek after current review

Candidate sufficient inputs: iid rows with covariance Sigma, uniformly controlled tails giving entrywise covariance/cross-product concentration for polynomial p; fixed sparse signal with bounded energy and noise variance bounded away from zero; sparse eigenvalue floor on sets of size 16+s0; visible-null conditional-correlation floor kappa_n with n*kappa_n/log p -> infinity (and enough visible nulls). APP Lemma VN treats closely related Gaussian inputs; its status must be cited verbatim rather than inherited by an unreviewed extension here.

For Sigma=Lambda Lambda'+Psi, k fixed and Psi local, factor rank alone does not imply the visible-null floor. One must rule out cancellation of each relevant loading's conditional exposure to Lambda' beta and account for local Psi coupling. For diagonal Psi bounded below, posterior factor covariance takes (I+Lambda_U' Psi_U^-1 Lambda_U)^-1; general k can cause sign/directional cancellation even when each individual loading is nonzero. A global nonzero factor signal is not sufficient for every null to be visible. For bounded-block Psi, conditioning and truth/null group overlap require explicit Schur-complement calculations. These are candidate verification steps, not results claimed by L1.

## Singleton start and swap targets

SINGLETON_TARGET remains a deliberately narrow diagnostic: exact CS sample Gram, singleton analysis partition, fixed one-coordinate signal. It isolates noise-selected signed order statistics and early null swaps. It does not establish behavior of the production partition or iid sampled factor designs. Exact scalar centre, exchangeable null coordinates and a uniform early-path score expansion are special inputs. General factor loadings and local Psi do not presently inherit that argument. An eventual obstruction concerns a uniform-partition/cap guarantee only.

## Relationship to A1–A3

A1 (iid rows + sparse eigenvalues): potentially supplies L1 ingredients 1–2 with an explicit tail/concentration hypothesis; current exact-Gram proof itself does not assume iid rows. A log-size eigenvalue floor includes the needed fixed-size floor eventually.

A2 (fixed factors + local Psi): a model for verifying visible-null exposure, but does not imply ingredient 3 without an additional noncancellation condition.

A3 (beta-min + non-masking): needed for truth identification and path protection in the full theorem; saturation alone requires visible null exposure and can hold without truth inclusion. Keep truth non-masking distinct from null visibility.

Still missing for the main theorem from this ticket: production start allocation, adaptive swap/path bounds under iid sample Gram, SMC/final-search discovery when LS0 misses, a sufficient cap remedy and any minimality proof. No consistency conclusion is drawn from saturation alone.
