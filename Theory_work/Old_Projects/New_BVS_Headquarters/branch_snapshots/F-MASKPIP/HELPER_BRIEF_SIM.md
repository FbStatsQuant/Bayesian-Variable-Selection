# Helper brief: masked-regime final-run simulation (evidence vs PIP split)

You are a helper for F-MASKPIP (theory campaign, branch `theory/F-MASKPIP`). Work ONLY inside
`theory_campaign/F-MASKPIP/` (scripts in `scripts/`, outputs in `results/`). Commit and push to
`theory/F-MASKPIP` after each meaningful step (`git add theory_campaign/F-MASKPIP && git commit && git push`).
Use at most 3 CPU cores. Python 3; `pip install numpy scipy` if needed. Fixed seeds everywhere.
Do NOT edit any other file. Do not touch REPORT.md (the lead writes it); write your findings in
`results/SIM_NOTES.md`.

## Goal
Exact-score simulation of the SMC-BVS v3 final run on a MASKED design at small p (p = 18, exact enumeration),
to measure, per island, (a) the evidence ratio W_r = Z-hat_r / Z, (b) terminal occupancy of the truth S0,
(c) the Rao-Blackwell PIP error, and to check three inequalities the lead is proving:

  (I1)  E[ W_r * 1{f_r > 1/2} ] <= 2 * delta1,   f_r = fraction of island r's particles outside S0 at the end of
        stage T (after the stage-T round), delta1 = 1 - pi(S0).
  (I2)  pathwise: max_j |PIPhat_rj - 1{j in S0}| <= Bbar_r + u_pi, where Bbar_r = fraction of (particle, measured
        round) pairs whose within-round path (including its start) contains a state != S0, u_pi = delta1/pi(S0).
  (I3)  E[ W_r * max_j |PIPhat_rj - 1{j in S0}| ] <= delta1 + rhobar + u_pi, where rhobar = exact one-round
        departure probability from S0 at phi = 1 (1 - prod_e (1 - K_e(S0, Omega \ {S0})) over the p + B + 2
        elementary kernels; see W2-T26 `check_rho_bar.py` for the exact formula).
and to exhibit the SPLIT: realisations where W_r is tiny (evidence badly underestimated) while the PIP error is
small (terminal rounds delivered the population to S0).

## Reuse
Copy these from branch `origin/theory/W2-T26` (`git show origin/theory/W2-T26:theory_campaign/W2-T26/scripts/<f>`):
`bvs_exact.py`, `premise_scan.py` (for `design`), `smc_sim.py`, `check_rho_bar.py`. Put copies in
`theory_campaign/F-MASKPIP/scripts/` and adapt `smc_sim.py` into `masked_sim.py`. Read the docstrings; the final
run is already implemented (N iid pi0 draws; per stage: reweight by exp(Dphi d), multinomial resampling, one round;
then L burn-in + 4 measured rounds at phi = 1 recording o_j before each Gibbs step).

## What to run (all with the `masked` design of premise_scan.py, p = 18, data seed 0; and if cheap, a second
masked design of your own with stronger masking, e.g. correlation 0.8 between the masked true variable and a
cross-block variable, documented)
For each setting record PER ISLAND and per rep: log W_r, f_r (end of stage T), the fraction outside S0 at the start
of each of the 4 measured rounds, Bbar_r, max_j PIP error (island), the primary pooled PIP error, MPM correct?, T,
and the grid.
 1. Frozen grid G1: T = 1, phi = (0, 1)  (one-shot importance sampling then terminal rounds).  n in {640, 5120};
    N in {50, 2500}; reps 20 (N=2500) / 40 (N=50).
 2. Frozen grid G2: the ideal full-space ESS grid of bvs_exact.ideal_grid (as in smc_sim.py), same n, N, reps.
 3. Frozen grid G3: a "blind" grid that bisects on the ESS RESTRICTED to the set V of states seen in a pilot of
    N pi0 draws (exclude S0 and any state containing the masked variable if they are not in V); this mimics the
    method's candidate-set restriction (T13). Same n, N, reps. If this is too much, do G1 and G2 first and push.
Also compute for each setting delta1, u_pi, rhobar, pi0(S0), and the exact posterior PIP error
max_j |PIP_j - 1{j in S0}|.

## Report (results/SIM_NOTES.md)
Tables: per setting, mean and quantiles (5%, 50%, 95%) of log W_r; fraction of islands with f_r > 1/2
(non-crossing at stage T); mean island PIP error; mean Bbar_r; both sides of (I1), (I3) (empirical means vs bounds);
the max over all island-reps of [PIP error - (Bbar_r + u_pi)] (must be <= 1e-12 for (I2)).
Then 5-10 lines of plain findings: does W_r collapse (log W_r << 0) while PIPs are accurate? at which grid?
Any violation of (I1)-(I3) is a finding of the first importance: report it exactly and do not "fix" it.
Write the raw per-island records to results/masked_sim.jsonl.
