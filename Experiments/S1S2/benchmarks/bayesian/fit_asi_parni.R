# =============================================================================
# PROVENANCE  fit_asi_parni.R  (REFERENCE ONLY, NOT REGISTERED in harness/methods.R)
#             ASI as implemented in R in the PARNI repo.
# -----------------------------------------------------------------------------
# STATUS (owner's decision 2026-11-25, relayed by the manager): the ASI
#   benchmark is the authors' ORIGINAL ASI_sampler.m run under Octave; that
#   adapter is fit_asi.R.  This file, formerly fit_asi.R, is kept unchanged
#   apart from its name and the function name fit_asi_parni(), for comparison
#   runs only.  Where the text below says "fit_asi.R" or "the code that runs",
#   read "this file" and "the PARNI R code".  See ASI_DIFF.md.
# -----------------------------------------------------------------------------
# METHOD PAPER
#   [GLS21] Griffin, Latuszynski & Steel (2021) "In search of lost mixing time:
#           adaptive Markov chain Monte Carlo schemes for Bayesian variable
#           selection with very large p", Biometrika 108(1):53-69,
#           DOI 10.1093/biomet/asaa055.  READ AS THE PUBLISHED ARTICLE
#           (_local/papers/Benchmark_methods/Griffin_Latuszynski_Steel_2021_
#           Biometrika_published.pdf).  Pages below are PDF pages 1-17; journal
#           page = 52 + PDF page.  The SUPPLEMENT (below) is in hand since 2026-11-25.
#           Sec 2.1 p.3, prior (1): p(alpha, sigma^2, beta_g, gamma) prop.
#             sigma^-2 p(beta_g | sigma^2, gamma) p(gamma), beta_g | sigma^2,
#             gamma ~ N(0, sigma^2 V_g), p(gamma) = h^p_g (1-h)^(p-p_g); i.e.
#             flat prior on the intercept alpha and p(sigma^2) prop. sigma^-2.
#           Sec 2.2 p.7: "we run independent parallel chains which share the
#             same" adaptive parameters (multiple chain acceleration).
#           Sec 2.4 pp.8-9, Algorithm 2 (p.9): ASI.  Proposal (9): add
#             probability A_j = zeta min(1, pi_j/(1-pi_j)), delete probability
#             D_j = zeta min(1, (1-pi_j)/pi_j); pi_j = kappa + (1 - 2 kappa) *
#             Rao-Blackwellized PIP estimate (10), with V_g = g I; zeta updated
#             by (11): logit_eps zeta += phi_i (a_i - tau), "tau is a targeted
#             acceptance rate"; "We use eps = 0.1/p"; zeta = 1/Delta if
#             zeta Delta < 1, Delta = 2 sum_j min(pi_j, 1 - pi_j); "We use
#             kappa = 0.001" (all p.9).
#           Sec 4.1 pp.11-13 (the S1 design, Yang et al. 2016 DGP): p.11 "We use
#             the prior in (1) with V_gamma = 9I and h = 10/p, implying a prior
#             mean model size of 10" (INDEPENDENT prior, NOT a Zellner g-prior);
#             Table 1 p.12: ASI run with 5 and with 25 multiple chains; 25 "is
#             better than the corresponding performance with 5 chains for most
#             cases" (p.12).  Sec 4.1 does NOT state iterations, burn-in or tau.
#           Sec 4.3 p.14 (very large p, real data): "tau = 0.234"; ASI "had 500
#             burn-in and 2500 recorded iterations and no thinning";
#             "Rao-Blackwellised updates of pi were only calculated during the
#             burn-in, and posterior inclusion probability for the jth variable
#             was estimated by the posterior mean of gamma_j".
#           p.16: "Code to run both algorithms is available from
#             https://jimegriffin.github.io/website/" = [GLS-code] below.
#           SUPPLEMENT (Supplementary_1_4_20.pdf, 22 pages, in _local/papers/
#             Benchmark_methods/Griffin2021_supplement/; sha256 55340f5c...43274):
#             proofs, the Rao-Blackwellised estimate, parallel tempering,
#             Sec 5.1 pp.9-10 (Tecator, Boston, concrete, protein data; "run
#             for the same amount of time", 200 runs) and Sec 5.2 p.10 (extra
#             figures for Sec 4.3).  It states NO iteration count, burn-in or
#             tau for the Sec 4.1 simulation.
#   [GLS-code] THE AUTHORS' ORIGINAL ASI CODE (MATLAB): Version3.0.zip from
#           https://jimegriffin.github.io/website/Version3.0.zip, fetched
#           2026-11-25T20:58Z, sha256 ce3e9c75...460f42; ASI_sampler.m sha256
#           4705c795...10dddb.  Stored unmodified, with the sha256 of every file,
#           in _local/engineering/ext/griffin_asi_original/ (PROVENANCE.txt).
#           File for file identical (sha256) to the owner's supplement copy,
#           Griffin2021_supplement/code/Version3.0/ and Code_For_Paper.zip.
#           It is the FIDELITY REFERENCE and it is NOT RUN: Owls has neither
#           MATLAB nor Octave.  It contains ASI_sampler.m and two run scripts,
#           run_tecator.m and run_concrete.m (real data; g = 100, h = 5/100,
#           tau = 0.25, nu = 1, 25 chains, 100 burn-in + 200 iterations,
#           adap_type = 1).  It contains NO script for the Sec 4.1 simulation,
#           so it states no run length and no tau for Sec 4.1.  Every difference
#           between it and the code that runs is listed under "ORIGINAL CODE
#           vs THE CODE THAT RUNS" below.
#   [LLG22] Liang, Livingstone & Griffin (2022) "Adaptive random neighbourhood
#           informed Markov chain Monte Carlo for high-dimensional Bayesian
#           variable selection", Stat. Comput. 32:84,
#           DOI 10.1007/s11222-022-10137-8.  Sec 5.1: same DGP, "V_gamma = I,
#           g = 9 and h = 10/p" (= [GLS21]'s V_gamma = 9 I), adaptive schemes
#           run with 25 chains, adaptation stops at the end of burn-in.  This
#           is the paper the code below was released with (Griffin co-author).
# SOFTWARE THAT RUNS (authors' own R code; nothing reimplemented)
#   github.com/XitongLiang/The-PARNI-scheme, commit
#   3b95d669e9bcf6df9e2ba46fb89fc536922e12e2, cloned (not in git) to
#   /home/fb31/Bayesian-Variable-Selection/_local/engineering/ext/
#     The-PARNI-scheme@3b95d669e9bcf6df9e2ba46fb89fc536922e12e2/
#   The repo is plain R (no package, no compiled code).  This adapter sys.source()s
#   three of its files UNMODIFIED into a private environment and calls them:
#     R/make_hyper_par.R                    md5 b2a8a525ef31313a9b96ab1b07a52ccf
#     R/sampler/ASI.R                       md5 96f5d8da98b5fbcf4b36dcc2e243500c
#     R/sampler/other_supportive_functions.R md5 e9dce2640d7e3ea7bad06e560f03dce9
#   The adapter REFUSES to run (status "failed: ...") if the clone's HEAD or any
#   of the three md5 sums differ from the pins above.
#   (The repo's "R/main functions.R" only source()s these plus ADS.R / PARNI.R by
#   relative path; it is not used so that no setwd() is needed.)
#
# THE CALL  = the authors' run script R/simulation/simulation_example.R at the
#             pinned commit, EXACTLY (HQ corrected ruling 2026-11-25): lines
#             12-13 (preprocessing), 15-21 (make_hyper_par) and 66-81 (ASI).
#             That script is itself the S1 design: lrrsg(n = 500, p = 5000,
#             rho = 0.6, SNR = 2), the Sec 4.1 beta.  Every argument below has
#             the script's value; the only change is verbose = FALSE (progress
#             bar off, OURS-5).  Nothing else is in the script's ASI block.
#   X <- scale(X); y <- scale(y, scale = FALSE)                       # script l.12-13
#   hyper_par <- make_hyper_par(y = y, X = X, g = 9, h = 10/p, Z = NULL, prior_type = 1)
#   alg_par <- list(N = 6000, Nb = 2000, full_adap = FALSE, verbose = FALSE,
#                   kappa = 0.001, eps = 0.1/hyper_par$p, phi = c(-0.7, -0.7),
#                   target_prop = 0.2, target_swap = 0.25, n_chain = 25,
#                   init_zeta = 0.5, n_temp = 1, store_chains = FALSE)
#   res <- ASI(alg_par, hyper_par);  pip <- res$estm_PIPs[1, ]
# TAG "EX" below = "authors' repo R/simulation/simulation_example.R @3b95d66;
#   not stated in the Biometrika text".  Settings with this source are written
#   to `settings` with tag "author" in suite S1 and "OURS" in suite S2 (OURS-1).
#
# SETTINGS  (value | source | tag)
#   prior_type   1 = independent prior (1): beta_g ~ N(0, g sigma^2 I), flat
#                intercept, p(sigma^2) prop. sigma^-2 | [GLS21] Sec 2.1 p.3, Sec 4.1 p.11 | author
#   g            9 (V_gamma = 9 I)              | [GLS21] Sec 4.1 p.11; [LLG22] 5.1; repo script | author if suite S1, OURS-1 if S2
#   h            10/p (fixed)                   | [GLS21] Sec 4.1 p.11; [LLG22] 5.1; repo script | author if suite S1, OURS-1 if S2
#                (the tag written to `settings` follows ctrl$suite, which the harness passes; default "S1")
#   preprocess   X <- scale(X) (centre, unit sample sd); y <- scale(y, scale = FALSE)
#                                               | script l.12-13; the same two lines are in
#                                                 R/simulation/dataset_generation.R l.28-29 | author (PRE)
#   Z            NULL: make_hyper_par scales X and centres y AGAIN (make_hyper_par.R
#                l.13-14); on already scaled input this changes nothing beyond
#                rounding (PRE) = intercept with a flat prior integrated out
#                                               | repo make_hyper_par.R / script   | author (see D-9)
#   n_chain      25                             | EX; [GLS21] Table 1 p.12 ran 5 and 25;
#                                                 [LLG22] 5.1 uses 25              | author (S1), OURS-1 (S2)
#   target_prop  0.2 (tau)                      | EX; [GLS21] Sec 4.1 states none
#                                                 (Sec 4.3, other data: 0.234)     | author (S1), OURS-1 (S2)
#   N            6000 iterations per chain      | EX                               | author (S1), OURS-1 (S2)
#   Nb           2000 burn-in                   | EX                               | author (S1), OURS-1 (S2)
#   full_adap    FALSE (Nl = Nb): the Rao-Blackwellised adaptation of pi STOPS at
#                the end of burn-in (iteration 2000; r.374), pi is then frozen;
#                zeta KEEPS adapting for all 6000 iterations (r.386-388)
#                                               | [GLS21] Sec 4.3 p.14; [LLG22] 5.1; repo script | author (see D-6)
#   kappa        0.001                          | [GLS21] Sec 2.4 p.9; repo script;
#                                                 original code 0.0001 (D-1)       | author
#   eps          0.1/p                          | [GLS21] Sec 2.4 p.9; repo script   | author
#   phi          c(-0.7, -0.7): phi_i = i^-0.7 (2nd entry unused, n_temp = 1) | EX;
#                                                 [GLS21] p.7: phi_i = O(i^-lambda), 1/2 < lambda <= 1;
#                                                 original code 2 it^-0.55 (D-2)   | author (S1), OURS-1 (S2)
#   init_zeta    0.5                            | EX; original code 0.1 (D-3)      | author (S1), OURS-1 (S2)
#   n_temp       1 (no tempering; target_swap = 0.25 then unused) | repo script      | author
#   store_chains FALSE                          | repo script                        | author
#   verbose      FALSE (progress bar off; no numerical effect) | repo script has TRUE | OURS-5
#   start        each chain: gamma_j ~ Bernoulli(h), i.i.d. | repo ASI.R; original code alike | author
#   PIP          res$estm_PIPs[1, ] = plain mean of gamma_j over the RECORDED
#                draws, (N - Nb) * n_chain = 100,000 (not Rao-Blackwellized)
#                                               | [GLS21] Sec 4.3 p.14; repo ASI.R;
#                                                 original code alike (S-6)        | author
#   seed         set.seed(method_seed)          | INTERFACE.md "Seeds"               | OURS-6
#   selection    {j : PIP_j > 0.5} (median probability model) | INTERFACE.md         | OURS-7
#   threads      BLAS/OpenMP capped (default 1) | Owls compute rule                  | OURS-8
#
# OURS FLAGS
#   OURS-1  S2 TRANSFER.  g = 9, h = 10/p ([GLS21] Sec 4.1 p.11) and the run
#           settings of the authors' script (EX: N, Nb, n_chain, target_prop,
#           phi, init_zeta) belong to the S1 design.  No ASI paper or script
#           covers the S2 (Hastie et al.) design; HQ ruling 2026-11-25: the S1
#           settings are used unchanged in S2.  When ctrl$suite is not "S1" the
#           `settings` tags of these eight entries are written as "OURS".  The
#           suite never changes the fit.  kappa, eps and full_adap are stated
#           in the paper for the algorithm itself (Sec 2.4 p.9, Sec 4.3 p.14)
#           and stay "author" in both suites.
#   EX      HQ corrected ruling 2026-11-25: ASI on S1 = the authors' repo
#           script exactly, including target_prop = 0.2.  The earlier rulings
#           "tau = 0.234 from Sec 4.3" and "we pick 25" (former OURS-2, OURS-3,
#           OURS-4) are withdrawn; these numbers are no longer used.  Basis:
#           [GLS21] Sec 4.1, its supplement and the original MATLAB code state
#           no tau and no run length for this design; the script is the only
#           place where one of the authors (Griffin is a co-author of the repo's
#           paper) fixes them for it.  ctrl$N, ctrl$Nb, ctrl$n_chain,
#           ctrl$target_prop, ctrl$kappa, ctrl$init_zeta, ctrl$phi_prop are
#           OFF by default; any use is recorded with tag "OURS".
#   PRE     PREPROCESSING (HQ corrected ruling 2026-11-25, for all three
#           Bayesian adapters): X <- scale(X); y <- scale(y, scale = FALSE), as
#           in the script (l.12-13) and in dataset_generation.R (l.28-29).
#           make_hyper_par(Z = NULL) then applies the same two operations
#           again.  That is what the authors' script does, and it is harmless:
#           scaling scaled columns and centring a centred y change them only by
#           rounding (measured by test_bayesian.R: max change in X about 1e-15).
#           So V_gamma = 9I applies to the coefficients of unit-sd columns.
#   OURS-5  verbose = FALSE only suppresses txtProgressBar output.
#   OURS-6  All randomness (runif inside ASI.R) follows set.seed(method_seed),
#           Mersenne-Twister / Inversion / Rejection, called just before the run.
#   OURS-7  Median probability model, as fixed by INTERFACE.md.
#   OURS-8  RhpcBLASctl caps BLAS/OpenMP threads to ctrl$threads (default 1,
#           max 4); the cap stays in force for the rest of the R process.  R on
#           Owls otherwise starts 80 OpenBLAS threads.  No effect on results.
#   The Rao-Blackwellized PIPs (res$rb_PIPs, burn-in only) are kept in
#   extra$rb_pip_burn_in for reference and are NOT the reported PIP.
#   Convergence info in `extra` (R-hat of the post-burn-in log-posterior trace
#   across the 25 chains, |RB - MC| PIP gap) is an OURS diagnostic; it is
#   recorded only and never changes the output.
#
# ORIGINAL CODE vs THE CODE THAT RUNS
# (full line-by-line table, verdict and run-setting table: ASI_DIFF.md)
#   ([GLS-code] ASI_sampler.m line numbers "m.NN"; repo R/sampler/ASI.R "r.NN")
#   SAME in both, and as in [GLS21]:
#   S-1  Proposal (9): independent flips with A_j = zeta min(1, pi_j/(1-pi_j)),
#        D_j = zeta min(1, (1-pi_j)/pi_j) (m.165-176; r.64-69, r.241-249, r.411),
#        Metropolis-Hastings acceptance with the proposal ratio (m.177-234;
#        r.253-261).
#   S-2  pi_j during burn-in = running mean of the Rao-Blackwellised conditional
#        inclusion probabilities h BF_j / (1 - h + h BF_j), eq (10)
#        (m.375-404; r.376-378); chains share pi and zeta (m.96, m.159; r.377).
#   S-3  zeta moves on the logit_eps scale towards the target acceptance tau,
#        eq (11), with eps = 0.1/p (m.49-50, m.251; r.387-388).
#   S-4  Prior and marginal likelihood: flat intercept, independent prior
#        V = g I (gprior = 0; prior_type = 1), fixed h; g^(-p_g/2)
#        |X_g'X_g + I/g|^(-1/2) A^(-n/2) (m.81-83; repo log_llh_ind_L).  The
#        exponent is n/2 in both, as printed in [GLS21] Sec 2.4 pp.8-9 (a flat
#        intercept with p(sigma^2) prop. sigma^-2 gives (n-1)/2).
#   S-5  Start: gamma_j ~ Bernoulli(h) i.i.d. in every chain (m.65; r.123).
#   S-6  PIP = plain mean of gamma over the recorded draws of all chains
#        (m.529, m.565: sumgamma / (numbofits * numbofreps); r.310, r.460).
#        Neither code returns a Rao-Blackwellised PIP as its estimate.
#   DIFFERENT (the repo code is run as shipped; none of this is edited):
#   D-1  kappa.  Original: 0.0001, hard-coded (m.160: probstar = 0.0001 +
#        (1 - 0.0002) probstar).  [GLS21] Sec 2.4 p.9: "We use kappa = 0.001".
#        Repo script: 0.001.  USED: 0.001 (paper; HQ ruling 2026-11-25).
#        ctrl$kappa = 1e-4 gives the original code's value.
#   D-2  Step size phi_i.  Original: 2 / it^0.55, applied after EVERY chain's
#        move, and only when the proposal changes at least one variable
#        (m.251: 2 / it^0.55 * (change~=0) * (accept - tau)).  Repo: it^-0.7,
#        applied once per iteration to the mean acceptance probability over
#        the chains, where an empty proposal counts as accepted with
#        probability 1 (r.261, r.307, r.333, r.386-387).  [GLS21] p.7 only
#        requires phi_i = O(i^-lambda), 1/2 < lambda <= 1.  USED: repo, -0.7.
#        ctrl$phi_prop = -0.55 sets the original's exponent; its factor 2 and
#        per-chain updating cannot be set through the repo's arguments.
#   D-3  Start value of zeta.  Original: nu / (h p), reset to 0.1 if above 1
#        (m.92-95); with nu = 1 (both run scripts) and h = 10/p this is 0.1.
#        Repo script: init_zeta = 0.5.  [GLS21] gives no ASI start value.
#        USED: 0.5.  ctrl$init_zeta = 0.1 gives the original's value.
#   D-4  Lower bound on zeta.  Original: expected number of proposed changes
#        E = zeta * 2 sum_j min(pi_j, 1 - pi_j) = zeta Delta, as [GLS21] Sec 2.4
#        p.9; if E < 1 then logit(zeta) <- logit(zeta) - log(E) (m.412-420).
#        Repo: compute_Delta = 2 (sum(pi_j : pi_j >= .5) + sum(1 - pi_j :
#        pi_j < .5)) = 2 sum_j MAX(pi_j, 1 - pi_j), and zeta <- 1/Delta if
#        zeta Delta < 1 (r.392-398).  The repo's Delta is about 2p, so its
#        bound almost never binds.  No argument changes this.
#   D-5  Range of zeta.  Original: logit_eps(zeta) clamped to [-3, 3] (m.422-427),
#        i.e. zeta in about [0.047, 0.953].  Repo: logit_e() clamps zeta into
#        [2 eps, 1 - 2 eps] (its upper test is written x > 2(1 - eps), which
#        never fires), and after the Delta step resets zeta > 1 - eps to
#        1 - eps - 0.01 and zeta < eps to eps + 0.01 (r.400-405).  In the S1
#        tests the repo's zeta ended at 0.9998; the original would stop at 0.953.
#   D-6  Adaptation after burn-in.  Original with adap_type = 1 (both run
#        scripts): zeta keeps adapting and pi keeps being updated, now with the
#        plain gamma draws instead of the Rao-Blackwellised terms (m.249-261),
#        which is [GLS21] Sec 4.3 p.14 "Rao-Blackwellised updates of pi were
#        only calculated during the burn-in".  Repo with full_adap = FALSE
#        (repo script; [LLG22] Sec 5.1): pi is FROZEN after burn-in (r.374),
#        zeta keeps adapting (r.386-388).  full_adap = TRUE would instead keep
#        the Rao-Blackwellised update for the whole run; neither repo setting
#        reproduces the original.
#   D-7  Order of updates.  Original: pi and zeta are updated after each
#        chain's move, from that chain's current state (m.143-144, m.403-404).
#        Repo: once per iteration, pi from the mean over chains of
#        conditional probabilities cached per chain and recomputed only when a
#        chain moves (r.295-299, r.377).  Same estimator, different timing.
#   D-8  kappa in the bound: the original applies kappa to pi in the proposal
#        only, not in E of D-4 (m.160 vs m.412); the repo uses the kappa-shrunk
#        pi in both (r.378, r.392).  First move: original pi = 0/0 at the
#        first update, so that proposal is empty; repo starts from pi = h (r.63).
#   D-9  Scaling of X.  Original: none inside the sampler; its run scripts
#        centre the columns of X and y only, and the sampler carries the
#        intercept (m.67).  Repo: make_hyper_par(Z = NULL) scales every column
#        of X to unit sample sd and centres y, then applies N(0, g sigma^2 I).
#        [GLS21] states no scaling.  S1/S2 columns have unit population
#        variance, so g = 9 applies to almost the same scale (sample sd of a
#        column is 1 +- about 1/sqrt(2n)).  USED: repo (scaled; PRE).
#   D-10 Run settings.  Original scripts (Tecator, concrete): tau = 0.25,
#        25 chains, 100 + 200 iterations, no thinning.  Repo script (S1 design):
#        tau = 0.2, 25 chains, 2000 + 4000.  [GLS21] Sec 4.3: tau = 0.234.
#        Neither code nor paper states tau or the run length of Sec 4.1.
#        USED: the repo script, tau = 0.2, 25 chains, 2000 + 4000 (EX).
#   Also: the original zip's run scripts call ASI_sampler with 16 arguments
#   while its ASI_sampler.m takes 18 (data_fixed first, updateg last), so the
#   scripts do not match the sampler they ship with; instructions.pdf documents
#   a third, 15-argument form.  eps and kappa were checked in the repo code:
#   ASI.R sets PIPs = kappa + (1 - 2 kappa) * (RB mean) (r.378) and updates
#   zeta through logit_e / inv_logit_e with eps (r.387-388), both from alg_par.
#
# ctrl (optional; every use is recorded in `settings` with tag "OURS")
#   ctrl$suite               "S1" (default) or "S2", passed by the harness; sets
#                            the author/OURS tags (OURS-1) only, never the fit
#   ctrl$g, ctrl$h           prior overrides (h scalar in (0,1))
#   ctrl$N, ctrl$Nb, ctrl$n_chain   run-length overrides
#   ctrl$target_prop         tau override (default 0.2, the repo script's value)
#   ctrl$kappa, ctrl$init_zeta, ctrl$phi_prop   the authors' alg_par arguments
#                            kappa, init_zeta, phi[1]; 1e-4, 0.1, -0.55 are the
#                            original MATLAB code's values (D-1, D-3, D-2).
#                            All OFF by default.
#   ctrl$threads             1..4 (default 1)
#   ctrl$repo                path of the pinned clone (default above)
#   ctrl$rlib                R library path (default: the S1S2 Rlib)
# =============================================================================

fit_asi_parni <- function(X, y, method_seed, ctrl = list()) {
  t_start <- proc.time()[["elapsed"]]
  PIN <- "3b95d669e9bcf6df9e2ba46fb89fc536922e12e2"
  REPO_URL <- "https://github.com/XitongLiang/The-PARNI-scheme"
  MD5 <- c("R/make_hyper_par.R"                     = "b2a8a525ef31313a9b96ab1b07a52ccf",
           "R/sampler/ASI.R"                        = "96f5d8da98b5fbcf4b36dcc2e243500c",
           "R/sampler/other_supportive_functions.R" = "e9dce2640d7e3ea7bad06e560f03dce9")
  out <- list(
    selected    = integer(0),
    pip         = NULL,
    runtime_sec = NA_real_,
    software    = list(name = "The-PARNI-scheme (ASI.R)", version = PIN, commit = PIN, url = REPO_URL),
    settings    = list(),
    extra       = list(status = "failed: not run")
  )
  warns <- character(0)
  t_fit0 <- NA_real_

  res <- tryCatch(withCallingHandlers({
    # ---- library (only for the optional thread cap) ------------------------
    rlib <- if (is.null(ctrl$rlib))
      "/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib" else ctrl$rlib
    if (dir.exists(rlib) && !(rlib %in% .libPaths())) .libPaths(c(rlib, .libPaths()))

    # ---- input checks ------------------------------------------------------
    if (!is.matrix(X) || !is.numeric(X)) stop("X must be a numeric matrix")
    y <- as.numeric(y)
    n <- nrow(X); p <- ncol(X)
    if (length(y) != n) stop("length(y) != nrow(X)")
    if (n < 3L || p < 2L) stop("need n >= 3 and p >= 2")
    if (anyNA(X) || anyNA(y) || any(!is.finite(X)) || any(!is.finite(y))) stop("non-finite values in X or y")
    if (length(method_seed) != 1L || !is.finite(method_seed) ||
        method_seed != floor(method_seed) || abs(method_seed) > .Machine$integer.max)
      stop("method_seed must be one whole number within integer range")

    # ---- the pinned authors' code -------------------------------------------
    repo <- if (is.null(ctrl$repo))
      file.path("/home/fb31/Bayesian-Variable-Selection/_local/engineering/ext",
                paste0("The-PARNI-scheme@", PIN)) else ctrl$repo
    if (!dir.exists(repo)) stop("pinned PARNI clone not found: ", repo)
    head <- tryCatch(trimws(readLines(file.path(repo, ".git", "HEAD"), n = 1L, warn = FALSE)),
                     error = function(e) NA_character_)
    if (!is.na(head) && grepl("^ref: ", head))
      head <- tryCatch(trimws(readLines(file.path(repo, ".git", sub("^ref: ", "", head)), n = 1L, warn = FALSE)),
                       error = function(e) NA_character_)
    if (!identical(head, PIN)) stop("PARNI clone HEAD is ", head, ", not the pinned commit ", PIN)
    files <- file.path(repo, names(MD5))
    if (!all(file.exists(files))) stop("PARNI clone is missing: ", paste(names(MD5)[!file.exists(files)], collapse = ", "))
    md5 <- unname(tools::md5sum(files))
    if (!identical(md5, unname(MD5)))
      stop("PARNI source differs from the pinned commit: ", paste(names(MD5)[md5 != MD5], collapse = ", "))
    penv <- new.env(parent = globalenv())
    for (f in files) sys.source(f, envir = penv, chdir = FALSE, keep.source = FALSE)
    out$software <- list(name = "The-PARNI-scheme (R/sampler/ASI.R, authors' R code)", version = PIN,
                         commit = PIN, url = REPO_URL, path = repo,
                         files_md5 = as.list(MD5), R = R.version.string)

    # ---- settings: the authors' run script, unless ctrl overrides ----------
    ov <- function(nm) !is.null(ctrl[[nm]])
    # suite of the setting, passed by harness/run_one.R as ctrl$suite ("S1" or "S2"); default "S1".
    # It changes ONLY the author/OURS tags in `settings`, never the fit.
    suite <- if (is.null(ctrl$suite)) "S1" else toupper(trimws(as.character(ctrl$suite)[1L]))
    is_s1 <- identical(suite, "S1")
    g <- if (ov("g")) as.numeric(ctrl$g) else 9
    h <- if (ov("h")) as.numeric(ctrl$h) else 10 / p
    N <- if (ov("N")) as.integer(ctrl$N) else 6000L
    Nb <- if (ov("Nb")) as.integer(ctrl$Nb) else 2000L
    n_chain <- if (ov("n_chain")) as.integer(ctrl$n_chain) else 25L
    target_prop <- if (ov("target_prop")) as.numeric(ctrl$target_prop) else 0.2     # EX: repo script l.74 (HQ corrected ruling)
    kappa <- if (ov("kappa")) as.numeric(ctrl$kappa) else 0.001                     # GLS21 Sec 2.4 p.9; original code 1e-4 (D-1)
    init_zeta <- if (ov("init_zeta")) as.numeric(ctrl$init_zeta) else 0.5           # repo script; original code nu/(h p) (D-3)
    phi_prop <- if (ov("phi_prop")) as.numeric(ctrl$phi_prop) else -0.7             # repo script; original code 2 it^-0.55 (D-2)
    if (length(g) != 1L || !is.finite(g) || g <= 0) stop("ctrl$g must be one positive number")
    if (length(h) != 1L || !is.finite(h) || h <= 0 || h >= 1) stop("h = 10/p must lie in (0, 1) (p > 10), or give ctrl$h in (0, 1)")
    if (is.na(N) || is.na(Nb) || is.na(n_chain) || Nb < 1L || N <= Nb || n_chain < 1L)
      stop("need N > Nb >= 1 and n_chain >= 1")
    if (!is.finite(target_prop) || target_prop <= 0 || target_prop >= 1) stop("ctrl$target_prop must lie in (0, 1)")
    if (length(kappa) != 1L || !is.finite(kappa) || kappa <= 0 || kappa >= 0.5) stop("ctrl$kappa must lie in (0, 0.5)")
    if (length(init_zeta) != 1L || !is.finite(init_zeta) || init_zeta <= 0.2 / p || init_zeta >= 1 - 0.2 / p)
      stop("ctrl$init_zeta must lie in (0.2/p, 1 - 0.2/p)")
    if (length(phi_prop) != 1L || !is.finite(phi_prop) || phi_prop < -1 || phi_prop >= -0.5)
      stop("ctrl$phi_prop must lie in [-1, -0.5) (GLS21 p.7: phi_i = O(i^-lambda), 1/2 < lambda <= 1)")
    sdx <- apply(X, 2L, stats::sd)
    if (any(!is.finite(sdx)) || any(sdx <= 0)) stop("X has a constant column; the authors' scale(X) would give NaN")

    # ---- threads (OURS-8) --------------------------------------------------
    threads <- if (ov("threads")) as.integer(ctrl$threads) else 1L
    if (is.na(threads) || threads < 1L) threads <- 1L
    threads <- min(threads, 4L)
    thread_cap <- "not applied (RhpcBLASctl not installed; rely on OMP_NUM_THREADS)"
    if (requireNamespace("RhpcBLASctl", quietly = TRUE)) {
      # the cap is left in force for the rest of this R process (RhpcBLASctl cannot read back the
      # current BLAS thread count, so "restoring" could raise it above the caller's own limit)
      RhpcBLASctl::blas_set_num_threads(threads); RhpcBLASctl::omp_set_num_threads(threads)
      thread_cap <- paste0("RhpcBLASctl ", as.character(utils::packageVersion("RhpcBLASctl")))
    }

    # ---- the authors' run ----------------------------------------------------
    set.seed(as.integer(method_seed), kind = "Mersenne-Twister",
             normal.kind = "Inversion", sample.kind = "Rejection")
    t_fit0 <- proc.time()[["elapsed"]]
    X <- scale(X)                                           # PRE: repo simulation_example.R l.12
    y <- scale(y, scale = FALSE)                            # PRE: repo simulation_example.R l.13
    hyper_par <- penv$make_hyper_par(y = y, X = X, g = g, h = h, Z = NULL, prior_type = 1)
    alg_par <- list(N = N, Nb = Nb, full_adap = FALSE, verbose = FALSE,
                    kappa = kappa, eps = 0.1 / hyper_par$p, phi = c(phi_prop, -0.7),
                    target_prop = target_prop, target_swap = 0.25, n_chain = n_chain,
                    init_zeta = init_zeta, n_temp = 1, store_chains = FALSE)
    fit <- penv$ASI(alg_par, hyper_par)
    t_fit1 <- proc.time()[["elapsed"]]

    pip <- as.numeric(fit$estm_PIPs[1L, ])
    if (length(pip) != p) stop("estm_PIPs length != p")
    if (anyNA(pip) || any(pip < 0 | pip > 1)) stop("ASI returned PIPs outside [0, 1] or NA")

    # ---- record what was actually used ---------------------------------------
    tag <- function(value, tag, source) list(value = value, tag = tag, source = source)
    # Settings of the S1 design (g, h and the run script's values): "author" in suite S1, "OURS" when
    # overridden or when transferred to another suite (OURS-1).
    EX <- "authors' repo R/simulation/simulation_example.R @3b95d66; not stated in the Biometrika text"
    au <- function(nm, src) if (ov(nm)) list("OURS", paste0("ctrl$", nm, " override (author value: ", src, ")")) else
      if (is_s1) list("author", paste0(src, "; suite S1 = the design of GLS21 Sec 4.1 and of the repo script")) else
        list("OURS", paste0("OURS-1: the authors' S1 value used unchanged in suite ", suite, " (HQ ruling 2026-11-25); ", src))
    s_g <- au("g", "9; GLS21 Sec 4.1 p.11 (prior (1) with V_gamma = 9I); LLG22 Sec 5.1; repo simulation_example.R")
    s_h <- au("h", "10/p; GLS21 Sec 4.1 p.11; LLG22 Sec 5.1; repo simulation_example.R")
    s_N <- au("N", paste0("6000; ", EX))
    s_Nb <- au("Nb", paste0("2000; ", EX))
    s_nc <- au("n_chain", paste0("25; ", EX, " (GLS21 Sec 4.1 Table 1 p.12 ran 5 and 25; LLG22 Sec 5.1 uses 25)"))
    s_tp <- au("target_prop", paste0("0.2; ", EX, " (GLS21 Sec 4.1 states no tau; Sec 4.3 p.14, other data: 0.234)"))
    s_phi <- au("phi_prop", paste0("phi = c(-0.7, -0.7); ", EX, " (GLS21 p.7 requires phi_i = O(i^-lambda), 1/2 < lambda <= 1); D-2: the original MATLAB code uses 2 it^-0.55 per chain move"))
    s_iz <- au("init_zeta", paste0("0.5; ", EX, "; D-3: the original MATLAB code starts at nu/(h p) = 0.1 for nu = 1, h = 10/p"))
    out$settings <- list(
      prior_type   = tag("independent: beta_gamma ~ N(0, g sigma^2 I), p(sigma^2) prop. 1/sigma^2 (prior_type = 1)",
                         "author", "GLS21 prior (1), Sec 2.1 p.3 and Sec 4.1 p.11 (flat intercept, p(sigma^2) prop. sigma^-2); repo simulation_example.R"),
      suite        = tag(suite, "OURS", if (is.null(ctrl$suite)) "default S1 (no ctrl$suite given)" else "ctrl$suite from harness/run_one.R; affects the author/OURS tags only"),
      g            = tag(g, s_g[[1]], s_g[[2]]),
      h            = tag(h, s_h[[1]], s_h[[2]]),
      preprocess   = tag("X <- scale(X); y <- scale(y, scale = FALSE), applied in the adapter before make_hyper_par", "author",
                         "PRE: repo simulation_example.R l.12-13 and dataset_generation.R l.28-29 (HQ corrected ruling 2026-11-25, all Bayesian adapters)"),
      Z            = tag("NULL: make_hyper_par scales X and centres y again (no change beyond rounding on scaled input); flat-prior intercept integrated out", "author", "repo make_hyper_par.R l.13-14; D-9: the original MATLAB run scripts only centre X"),
      N            = tag(N, s_N[[1]], s_N[[2]]),
      Nb           = tag(Nb, s_Nb[[1]], s_Nb[[2]]),
      n_chain      = tag(n_chain, s_nc[[1]], s_nc[[2]]),
      full_adap    = tag(FALSE, "author", "RB adaptation of pi stops at the end of burn-in (pi frozen from iteration Nb + 1); zeta keeps adapting for all N iterations (repo ASI.R). GLS21 Sec 4.3 p.14 (RB updates in burn-in only); LLG22 Sec 5.1; repo simulation_example.R; D-6: the original MATLAB code keeps adapting pi with plain draws after burn-in"),
      kappa        = tag(kappa, if (ov("kappa")) "OURS" else "author",
                         if (ov("kappa")) "ctrl$kappa override (GLS21 Sec 2.4 p.9 and repo script: 0.001; original MATLAB code: 0.0001)"
                         else "GLS21 Sec 2.4 p.9 (Algorithm 2); repo simulation_example.R; verified in ASI.R; D-1: the original MATLAB code hard-codes 0.0001"),
      eps          = tag(0.1 / p, "author", "0.1/p; GLS21 Sec 2.4 p.9; repo simulation_example.R; verified in ASI.R (logit_e / inv_logit_e)"),
      phi          = tag(c(phi_prop, -0.7), s_phi[[1]], s_phi[[2]]),
      target_prop  = tag(target_prop, s_tp[[1]], s_tp[[2]]),
      target_swap  = tag(0.25, "author", "repo simulation_example.R (unused: n_temp = 1)"),
      init_zeta    = tag(init_zeta, s_iz[[1]], s_iz[[2]]),
      n_temp       = tag(1L, "author", "repo simulation_example.R (no tempering)"),
      store_chains = tag(FALSE, "author", "repo simulation_example.R"),
      verbose      = tag(FALSE, "OURS", "OURS-5: progress bar off (script has TRUE); no numerical effect"),
      start        = tag("each chain gamma_j ~ Bernoulli(h) i.i.d.", "author", "repo ASI.R; same in the original MATLAB code (S-5)"),
      pip_estimator = tag("estm_PIPs[1, ]: plain mean of gamma over the (N - Nb) * n_chain recorded draws (not Rao-Blackwellized)", "author",
                          "GLS21 Sec 4.3 p.14; repo ASI.R and original MATLAB code alike (S-6); RB PIPs of the burn-in are kept in extra$rb_pip_burn_in only"),
      seed         = tag(as.integer(method_seed), "OURS", "OURS-6: INTERFACE.md Seeds; set.seed(method_seed) before the run"),
      selection    = tag("median probability model: PIP > 0.5", "OURS", "OURS-7: INTERFACE.md Selection rule"),
      threads      = tag(threads, "OURS", paste0("OURS-8: Owls compute rule; ", thread_cap))
    )

    # ---- convergence info (OURS diagnostics, recorded only) --------------------
    lp <- fit$log_post_trace[[1L]][(Nb + 2L):(N + 1L), , drop = FALSE]      # post-burn-in, one column per chain
    ms <- fit$model_size_trace[[1L]][(Nb + 2L):(N + 1L), , drop = FALSE]
    rhat <- NA_real_
    if (ncol(lp) >= 2L && nrow(lp) >= 4L && all(is.finite(lp))) {
      W <- mean(apply(lp, 2L, stats::var)); B <- nrow(lp) * stats::var(colMeans(lp))
      if (is.finite(W) && W > 0) rhat <- sqrt(((nrow(lp) - 1) / nrow(lp) * W + B / nrow(lp)) / W)
    }
    rb <- as.numeric(fit$rb_PIPs[1L, ])
    cpu <- as.numeric(fit$CPU_time)
    sel <- sort(which(pip > 0.5))
    conv <- list(
      iterations_per_chain = N, burn_in = Nb, n_chain = n_chain,
      recorded_draws = (N - Nb) * n_chain,
      acc_rate = as.numeric(fit$acc_rate)[1L], mut_rate = as.numeric(fit$mut_rate)[1L],
      ESJD = as.numeric(fit$ESJD)[1L], zeta_final = as.numeric(fit$zeta)[1L],
      rhat_log_post = rhat,
      model_size_mean = mean(ms), model_size_min = min(ms), model_size_max = max(ms),
      sum_pip = sum(pip), max_abs_rb_minus_mc_pip = max(abs(rb - pip)),
      n_pip_in_0.4_0.6 = sum(pip > 0.4 & pip < 0.6)
    )
    out$selected <- as.integer(sel)
    out$pip <- pip
    out$runtime_sec <- t_fit1 - t_fit0
    out$extra <- c(list(status = "ok"), conv, list(
      chain_mean_log_post = as.numeric(colMeans(lp)),
      chain_final_log_post = as.numeric(lp[nrow(lp), ]),
      zeta_at_burn_in_end = as.numeric(fit$zetas[Nb + 1L, 1L]),
      rb_pip_burn_in = rb,                                  # Rao-Blackwellized, burn-in only: reference, NOT the reported PIP
      cpu_time_min_authors = list(total = cpu[1L], burn_in = cpu[2L], post = cpu[3L]),
      thread_cap = thread_cap,
      diagnostics_note = "rhat_log_post, max_abs_rb_minus_mc_pip: OURS diagnostics, recorded only",
      n = n, p = p,
      json_summary = c(conv, list(n_selected = length(sel), max_pip = max(pip)))
    ))
    invisible(TRUE)
  }, warning = function(w) {
    warns <<- c(warns, conditionMessage(w))
    invokeRestart("muffleWarning")
  }), error = function(e) e)

  if (inherits(res, "error")) {
    out$selected <- integer(0)
    out["pip"] <- list(NULL)
    out$extra <- list(status = paste0("failed: ", conditionMessage(res)))
    t_end <- proc.time()[["elapsed"]]
    out$runtime_sec <- if (is.finite(t_fit0)) t_end - t_fit0 else t_end - t_start
  }
  out$extra$warnings <- unique(warns)
  out[c("selected", "pip", "runtime_sec", "software", "settings", "extra")]
}
