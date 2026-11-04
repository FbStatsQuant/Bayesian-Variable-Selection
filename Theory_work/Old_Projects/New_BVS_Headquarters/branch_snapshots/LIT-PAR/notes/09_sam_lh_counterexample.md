# LIT-PAR notes 09: G4 — SaM-type splitting fails on an LH-like masked design (numerical COUNTEREXAMPLE + analytic PROOF SKETCH)

Script: `scripts/sam_lh_demo.py` (seed 20261103; exact enumeration; run via owls_run -j 1). Outputs: `results/sam_lh_beta{0.6,1.0}.txt`.

Design (LH-like, OUR construction, not the exact W1-EXP family): p = 16; groups {0..3}, {5,6,7}, {8..11}, {12..15} equicorrelated rho = 0.7;
x4 a singleton linked only to hub x0 with corr psi = 0.5. Truth theta_0 = beta, theta_4 = -psi*beta (suppressor), theta_8 = beta; S0 = {0,4,8};
n = 200, noise sd 1. Population: cov(x4, y) = psi*beta - psi*beta = 0 (x4 marginally invisible; the LH masking mechanism).
Score: Zellner g-prior g = n, sigma^2 integrated, BB(1,p), cap 6 (not the exact v3 target: no unit ridge, improper sigma prior).
SaM as in Liang's slides: 2 halves; Stage I exact posterior per half, keep PIP > 0.5; Stage II exact posterior on merged set, HPM.

| beta | full posterior HPM = S0 | SaM split separating (0,4) | SaM split keeping (0,4) together | clustered split {0..7},{8..15} |
|---|---|---|---|---|
| 1.0 | 20/20 | **5/318** (median Stage-I PIP of x4 = 0.010) | 265/282 (median PIP 1.0) | 15/20 |
| 0.6 | 13/20 | **0/318** (median PIP 0.008) | 154/282 (median PIP 0.59) | 3/20 |

Status: COUNTEREXAMPLE (numerical, reproducible) to "SaM recovers S0" on an LH-like masked design whenever the random split separates
the linked pair (probability ~ 1/2 for two halves, -> (K-1)/K for K groups), while the exact full posterior recovers S0 (20/20 at beta = 1).

Analytic PROOF SKETCH (population level): if x4's split s excludes x0 and every variable correlated with x0, then the population projection
of mu = X theta onto span(X_s) has coefficient cov(x4, mu restricted)... = 0 on x4 (x4 is uncorrelated with mu and with every other column
in s that carries signal, by construction). By Song-Liang Thm 5 (misspecified-subset consistency, read from Liang's slides), Stage I
concentrates on models containing s~ = support of that projection, which excludes x4; with a model prior penalising extra variables the
Stage-I PIP of x4 -> 0, so x4 is never merged and Stage II cannot select it. Not verified line by line: the step "PIP -> 0 for zero-projection
variables" needs the overfitting-penalty part of SaM's theory (not read in the paper). Escalation item 1 in REPORT.

Notes: (i) the clustered split loses power at beta = 0.6 (3/20) because Stage I on {0..7} omits x8's signal (larger residual variance) —
splitting costs power even when it respects correlation; (ii) this is exactly why our method uses blocks only for the START and bridges to
the full posterior, and why Coats et al.'s advice to put correlated columns in SEPARATE batches is harmful under masking.
