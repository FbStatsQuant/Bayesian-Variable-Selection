# =============================================================================
# PROVENANCE  fit_asi.R  (S1/S2 Bayesian benchmark: ASI, the Adaptively Scaled
#             Individual adaptation sampler, run as the authors' ORIGINAL code)
# -----------------------------------------------------------------------------
# METHOD PAPER
#   [GLS21] Griffin, Latuszynski & Steel (2021) "In search of lost mixing time:
#           adaptive Markov chain Monte Carlo schemes for Bayesian variable
#           selection with very large p", Biometrika 108(1):53-69,
#           DOI 10.1093/biomet/asaa055.  Read as the published article
#           (_local/papers/Benchmark_methods/Griffin_Latuszynski_Steel_2021_
#           Biometrika_published.pdf).  Pages below are PDF pages 1-17; journal
#           page = 52 + PDF page.
#           Sec 2.1 p.3: prior (1).  Sec 2.4 pp.8-9: ASI, eqs (9)-(11),
#           Algorithm 2.  Sec 4.1 pp.11-12: the S1 design, "We use the prior in
#           (1) with V_gamma = 9I and h = 10/p", 5 and 25 chains; no run length
#           and no tau are stated.  p.16: "Code to run both algorithms is
#           available from https://jimegriffin.github.io/website/".
#
# SOFTWARE (authors' own; NOT modified, NOT reimplemented, NOT ported)
#   [M]     ASI_sampler.m, "Version3.0", the code named on p.16 of [GLS21].
#           sha256 4705c79523f4d772625764bcb880ed04852d83d121ea94fe46ef224d3b10dddb
#           Run from /home/fb31/Bayesian-Variable-Selection/_local/engineering/
#           ext/griffin_asi_original/Version3.0/ (fetched 2026-11-25 from
#           https://jimegriffin.github.io/website/Version3.0.zip), which is
#           byte-identical to the owner's supplement copy at _local/papers/
#           Benchmark_methods/Griffin2021_supplement/code/Version3.0/.
#           This adapter computes the sha256 of the file before every run and
#           refuses to run if it differs.  Lines are cited as "m.NN".
#   [INS]   instructions.pdf in the same folder (5 pages): the argument list.
#   [RUN]   run_tecator.m and run_concrete.m in the same folder: the authors'
#           two example calls.
#   [REPO]  github.com/XitongLiang/The-PARNI-scheme @ 3b95d669 (Griffin is a
#           co-author), R/simulation/simulation_example.R l.67-79: an R run of
#           ASI on the S1 design.  Used here ONLY as the source of the run
#           length, the number of chains and tau, which [GLS21] does not state
#           for Sec 4.1.  The R code of that repo is not run by this adapter
#           (fit_asi_parni.R keeps it, unregistered, for comparison).
#   Octave  GNU Octave 10.3.0, conda-forge build pl5321hd0fbda6_4, OpenBLAS
#           0.3.34, installed with micromamba 2.10.0 in user space at
#           /home/fb31/Bayesian-Variable-Selection/_local/engineering/envs/octave
#           (nothing system-wide).  MATLAB is not available on Owls.
#   SHIMS   none.  ASI_sampler.m runs under Octave as shipped.  The only names
#           it uses that Octave lacks is `stop` (m.151, m.256, m.288, ...),
#           which the code calls when a quantity turns complex; MATLAB has no
#           argument-free `stop` either, so in both systems the call raises an
#           error and ends the run.  The adapter reports that as a failure.
#   DRIVER  asi_octave/run_asi.m (OURS): reads the data and the arguments
#           written by this adapter, seeds the generator, calls ASI_sampler,
#           writes the returned fields.  It sets no value itself.
#           Its first three statements turn off Octave's workspace dump on a
#           signal, so that a killed run writes no "octave-workspace" file.
#
# THE CALL (run_asi.m; argument order = line 1 of ASI_sampler.m)
#   rand("state", method_seed); randn("state", method_seed);
#   output = ASI_sampler(data_fixed, data, target, g, gprior, mode, RB_adap, RB,
#                        hparam, tau, nu, burnin, numbofits, thin, numbofreps,
#                        heat, adap_type, updateg);
#   pip = output.prob_inclusion
#
# THE 18 ARGUMENTS  (value | source | tag)
#   [INS] documents 15 of them (it has no data_fixed, RB_adap is listed, no
#   updateg; its printed signature omits RB_adap but its list has it); [RUN]
#   passes 16 (no data_fixed, no updateg); the function takes 18 (m.1).  So the
#   two example scripts do not run against the shipped function as written.
#   The two undocumented arguments are set from the code itself.
#    1 data_fixed  zeros(n, 0): no covariate forced into every model.  The
#                  code always adds its own intercept column (m.67)
#                                  | code m.17-18, m.53, m.67; not in [INS]     | OURS-9
#    2 data        scale(X): n x p, columns centred, unit sd
#                                  | [INS] p.4 "data matrix X"; scaling: PRE    | see PRE
#    3 target      y - mean(y)     | [INS] p.4 "response y"; centring as [RUN]  | see PRE
#    4 g           9               | [GLS21] Sec 4.1 p.11 "V_gamma = 9I"        | author (S2: OURS-1)
#    5 gprior      0               | [INS] p.4: 1 = g-prior, "Otherwise, an
#                                    independence prior ... V_gamma = g I";
#                                    [RUN] uses 0                               | author
#    6 mode        1               | [INS] p.4: 2 = store the sampled models,
#                                    otherwise not; [RUN] uses 1                | author
#    7 RB_adap     1               | [RUN] l.40 / l.51.  NOT USED: the name
#                                    occurs only on m.1                         | author
#    8 RB          1               | [RUN].  NOT USED: the name occurs only on
#                                    m.1 (NOTE-b)                               | author
#    9 hparam      10/p            | [GLS21] Sec 4.1 p.11 "h = 10/p"; [INS] p.4:
#                                    length 1 = the value of h                  | author (S2: OURS-1)
#   10 tau         0.2             | [REPO] target_prop = 0.2; not stated in
#                                    [GLS21] Sec 4.1 ([RUN] 0.25, Sec 4.3 0.234)| author-repo (S2: OURS-1)
#   11 nu          1               | [RUN]; [INS] p.4 "starting values of A and
#                                    D".  Start zeta = nu/(h p) = 0.1 (m.92-96) | author
#   12 burnin      2000            | [REPO] Nb = 2000                           | author-repo (S2: OURS-1)
#   13 numbofits   4000            | [REPO] N - Nb = 4000 recorded per chain    | author-repo (S2: OURS-1)
#   14 thin        1               | [RUN] num_thin = 1; [REPO] has no thinning;
#                                    [INS] p.4 "Every thin-th iteration is
#                                    recorded after the burn-in period"         | author
#   15 numbofreps  25              | [REPO] n_chain = 25; [RUN] 25; [GLS21]
#                                    Table 1 p.12 reports 5 and 25 chains       | author (S2: OURS-1)
#   16 heat        1               | [INS] p.5: "The version without parallel
#                                    tempering occurs if heat=1"; [RUN] 1       | author
#   17 adap_type   1               | [RUN]; [INS] p.5 "if adap_type=1, there is
#                                    infinite adaptation" (NOTE-c)              | author
#   18 updateg     0               | code m.438: g is resampled only if
#                                    updateg == 1; [GLS21] Sec 4.1 fixes g = 9;
#                                    not in [INS]                               | OURS-9
#   "author-repo" rows carry the tag "author" in `settings` with the source
#   "authors' repo R/simulation/simulation_example.R @3b95d66; not stated in
#   the Biometrika text".
#
# HARD-CODED IN ASI_sampler.m AND LEFT AS THEY ARE
#   kappa = 0.0001 (m.160; the paper says 0.001, Sec 2.4 p.9); eps = 0.1/p
#   (m.49-50); zeta step 2/it^0.55 after every chain's move (m.251); logit zeta
#   kept in [-3, 3] (m.422-427); lower bound through the expected number of
#   changes (m.412-420); start gamma_j ~ Bernoulli(h) (m.65).  See ASI_DIFF.md.
#
# OURS FLAGS
#   OURS-1  S2.  No ASI paper or script covers suite S2.  The S1 values of g,
#           hparam, tau, burnin, numbofits, numbofreps are used unchanged there
#           and are tagged OURS in `settings` when ctrl$suite == "S2".
#   OURS-5  seed: rand("state", method_seed) and randn("state", method_seed) in
#           the driver, before the call.  "state" selects Octave's Mersenne
#           Twister and initialises it from the scalar (Octave manual, rand).
#           The sampler draws with rand only (randn only if updateg == 1).
#           The same seed gives identical output; MATLAB would give other
#           draws from the same seed (different seeding).
#   OURS-6  selection: median probability model, PIP > 0.5 (INTERFACE.md).
#   OURS-7  threads: OMP_NUM_THREADS = OPENBLAS_NUM_THREADS = ctrl$threads
#           (default 1, max 4) in the environment of the Octave process.
#   OURS-9  data_fixed and updateg: the two arguments [INS] does not document,
#           set from the code so that nothing is forced in and g stays fixed.
#   PRE     PREPROCESSING, done HERE, in R, once: X <- scale(X); y <- scale(y,
#           scale = FALSE) (HQ ruling b: authors' repo simulation_example.R
#           l.12-13, dataset_generation.R l.28-29).  ASI_sampler.m does not
#           centre or scale anything: it uses `data` and `target` as given
#           (m.52, m.67, m.83, m.293-309) and puts an unpenalised column of
#           ones in every design (m.67, m.72-73).  [RUN] centres X and y and
#           does not scale (run_tecator.m l.8-12, run_concrete.m l.19-23);
#           [INS] says nothing on either.  So centring follows [RUN]; scaling
#           to unit sd is the HQ ruling and is OURS relative to [M].  With
#           V_gamma = 9I the scale of a column matters; both S1 and S2 draw X
#           with unit variances, so the step changes columns by sampling error
#           only.
#
# NOTES (the code as shipped vs its documentation; nothing is changed)
#   NOTE-a  PIP = output.prob_inclusion = sumgamma / (numbofits * numbofreps)
#           (m.529, m.565): the plain mean of gamma over the recorded draws of
#           all chains.  With thin = 1 these are numbofits * numbofreps =
#           100000 draws.
#   NOTE-b  [INS] p.5 says prob_inclusion is the Rao-Blackwellised estimate
#           when RB = 1.  The code never uses RB; prob_inclusion is always the
#           plain mean and prob_inclusion2 is returned as zeros (m.110, m.566).
#   NOTE-c  [INS] p.5 gives adap_type = 2 for "adaptation restricted to the
#           burn-in".  The code tests adap_type == 1, or adap_type == 0 and
#           it < burnin (m.249); with 2 nothing adapts and the proposal
#           probabilities are 0/0.  With 1 (used): zeta adapts in every
#           iteration; pi is the running mean of the Rao-Blackwellised
#           conditional inclusion probabilities during burn-in (m.262-404) and
#           keeps being updated with the plain gamma draws afterwards
#           (m.259-261).  [GLS21] Sec 4.3 p.14: "Rao-Blackwellised updates of
#           pi were only calculated during the burn-in".
#   NOTE-d  The sampler prints progress every 10 iterations (m.128-140) and
#           the value of `fixed` (m.47).  The adapter sends that output to a
#           file in its temporary directory and deletes it.
#   NOTE-e  What the struct returns and what `extra` holds: accept (m.538) is
#           the running acceptance rate of all chains pooled, from iteration 1,
#           counting an empty proposal as 0; zeta is the final zeta; zetaAS and
#           zetaDS are the final A and D of Algorithm 2.  pi is not returned;
#           extra$pi_final = A / (A + D) is derived here from A_j = zeta
#           min(1, pi_j/(1-pi_j)), D_j = zeta min(1, (1-pi_j)/pi_j) (m.582-583)
#           and is OURS.  extra$rhat_logpost (split-free Gelman-Rubin on the
#           recorded log posterior of the chains) is an OURS diagnostic.
#
# ctrl (all optional; when used, the entry is tagged OURS in `settings`)
#   ctrl$g, ctrl$h, ctrl$tau, ctrl$nu, ctrl$burnin, ctrl$numbofits, ctrl$thin,
#   ctrl$numbofreps, ctrl$adap_type   arguments of ASI_sampler
#   ctrl$suite                "S1" (default) or "S2", from harness/run_one.R; sets tags only
#   ctrl$threads              BLAS/OpenMP threads of the Octave process (1; max 4)
#   ctrl$octave_home          Octave environment (default above)
#   ctrl$sampler_dir          folder holding ASI_sampler.m (sha256 is checked)
#   ctrl$driver               path of run_asi.m (default: asi_octave/ next to this file)
#   ctrl$tmp_root             parent of the temporary directory
#                             (default /home/fb31/Bayesian-Variable-Selection/_local/tmp)
#   ctrl$keep_tmp             TRUE keeps the temporary directory (debugging)
# =============================================================================

# directory of this file at source time (INTERFACE.md: adapters are loaded with chdir = TRUE)
.fit_asi_dir <- normalizePath(getwd(), mustWork = FALSE)

fit_asi <- function(X, y, method_seed, ctrl = list()) {
  t_start <- proc.time()[["elapsed"]]
  t_call0 <- NA_real_
  if (!is.list(ctrl)) ctrl <- list()
  ROOT <- "/home/fb31/Bayesian-Variable-Selection"
  SHA <- "4705c79523f4d772625764bcb880ed04852d83d121ea94fe46ef224d3b10dddb"
  out <- list(
    selected = integer(0), pip = NULL, runtime_sec = NA_real_,
    software = list(name = "ASI_sampler.m Version3.0 (Griffin, Latuszynski & Steel) under GNU Octave",
                    version = "Version3.0", sampler_sha256 = SHA, R = R.version.string),
    settings = list(), extra = list(status = "failed: not run")
  )
  warns <- character(0)
  workdir <- NULL
  keep_tmp <- isTRUE(ctrl$keep_tmp)

  res <- tryCatch(withCallingHandlers({
    ov <- function(nm) !is.null(ctrl[[nm]])
    # ---- paths ------------------------------------------------------------
    octave_home <- if (ov("octave_home")) as.character(ctrl$octave_home) else file.path(ROOT, "_local/engineering/envs/octave")
    octave <- file.path(octave_home, "bin", "octave-cli")
    sampler_dir <- if (ov("sampler_dir")) as.character(ctrl$sampler_dir) else
      file.path(ROOT, "_local/engineering/ext/griffin_asi_original/Version3.0")
    driver <- if (ov("driver")) as.character(ctrl$driver) else file.path(.fit_asi_dir, "asi_octave", "run_asi.m")
    tmp_root <- if (ov("tmp_root")) as.character(ctrl$tmp_root) else file.path(ROOT, "_local/tmp")
    if (!file.exists(octave)) stop("octave-cli not found at ", octave)
    sampler <- file.path(sampler_dir, "ASI_sampler.m")
    if (!file.exists(sampler)) stop("ASI_sampler.m not found in ", sampler_dir)
    if (!file.exists(driver)) stop("driver run_asi.m not found at ", driver)
    if (!dir.exists(tmp_root)) stop("temporary root does not exist: ", tmp_root)
    sha <- unname(tools::sha256sum(sampler))
    if (!identical(sha, SHA)) stop("ASI_sampler.m differs from the pinned file (sha256 ", sha, ")")
    out$software$sampler_path <- normalizePath(sampler)
    out$software$octave_home <- octave_home
    out$software$driver <- normalizePath(driver)
    out$software$driver_md5 <- unname(tools::md5sum(driver))

    # ---- input checks -----------------------------------------------------
    if (!is.matrix(X) || !is.numeric(X)) stop("X must be a numeric matrix")
    y <- as.numeric(y)
    n <- nrow(X); p <- ncol(X)
    if (length(y) != n) stop("length(y) != nrow(X)")
    if (n < 4L || p < 2L) stop("need n >= 4 and p >= 2")
    if (anyNA(X) || anyNA(y) || any(!is.finite(X)) || any(!is.finite(y))) stop("non-finite values in X or y")
    if (length(method_seed) != 1L || !is.finite(method_seed) ||
        method_seed != floor(method_seed) || abs(method_seed) > .Machine$integer.max)
      stop("method_seed must be one whole number within integer range")

    # ---- settings ---------------------------------------------------------
    suite <- if (is.null(ctrl$suite)) "S1" else toupper(trimws(as.character(ctrl$suite)[1L]))
    is_s1 <- identical(suite, "S1")
    num1 <- function(nm, default) { v <- if (ov(nm)) as.numeric(ctrl[[nm]]) else default
      if (length(v) != 1L || !is.finite(v)) stop("ctrl$", nm, " must be one finite number"); v }
    g <- num1("g", 9); h <- num1("h", 10 / p); tau <- num1("tau", 0.2); nu <- num1("nu", 1)
    burnin <- num1("burnin", 2000); numbofits <- num1("numbofits", 4000); thin <- num1("thin", 1)
    numbofreps <- num1("numbofreps", 25); adap_type <- num1("adap_type", 1)
    if (g <= 0) stop("g must be positive")
    if (h <= 0 || h >= 1) stop("h = 10/p must lie in (0, 1) (p > 10), or give ctrl$h in (0, 1)")
    if (tau <= 0 || tau >= 1) stop("tau must lie in (0, 1)")
    if (nu <= 0) stop("nu must be positive")
    whole <- function(v) v == floor(v)
    if (!whole(burnin) || burnin < 0 || !whole(numbofits) || numbofits < 1 || !whole(thin) || thin < 1 ||
        !whole(numbofreps) || numbofreps < 1) stop("burnin, numbofits, thin, numbofreps must be whole numbers (burnin >= 0, the others >= 1)")
    if (!(adap_type %in% c(0, 1))) stop("adap_type must be 1 (as run) or 0 (code m.249: adaptation only while it < burnin)")
    threads <- if (ov("threads")) as.integer(ctrl$threads) else 1L
    if (is.na(threads) || threads < 1L) threads <- 1L
    threads <- min(threads, 4L)
    gprior <- 0; mode <- 1; RB_adap <- 1; RB <- 1; heat <- 1; updateg <- 0      # fixed: see THE 18 ARGUMENTS

    # ---- PRE: preprocessing, here and only here ---------------------------
    sdx <- apply(X, 2L, stats::sd)
    if (any(!is.finite(sdx)) || any(sdx <= 0)) stop("X has a constant column; scale(X) would give NaN")
    X <- scale(X)
    y <- as.numeric(scale(y, scale = FALSE))

    # ---- temporary directory, data and arguments for the driver -----------
    workdir <- tempfile(pattern = paste0("asi_octave_", Sys.getpid(), "_"), tmpdir = tmp_root)
    if (!dir.create(workdir, mode = "0700")) stop("cannot create temporary directory under ", tmp_root)
    t_w0 <- proc.time()[["elapsed"]]
    con <- file(file.path(workdir, "X.bin"), "wb"); writeBin(as.double(X), con, size = 8L); close(con)
    con <- file(file.path(workdir, "y.bin"), "wb"); writeBin(as.double(y), con, size = 8L); close(con)
    par <- c(n = n, p = p, seed = as.numeric(method_seed), g = g, gprior = gprior, mode = mode, RB_adap = RB_adap, RB = RB,
             hparam = h, tau = tau, nu = nu, burnin = burnin, numbofits = numbofits, thin = thin,
             numbofreps = numbofreps, heat = heat, adap_type = adap_type, updateg = updateg)
    writeLines(sprintf("%s %.17g", names(par), par), file.path(workdir, "params.txt"))
    writeLines(normalizePath(sampler_dir), file.path(workdir, "sampler_dir.txt"))
    t_w1 <- proc.time()[["elapsed"]]

    # ---- the authors' sampler, under Octave -------------------------------
    logf <- file.path(workdir, "octave_stdout.log"); errf <- file.path(workdir, "octave_stderr.log")
    env <- c(paste0("ASI_OCTAVE_WORKDIR=", shQuote(workdir)), paste0("OCTAVE_HOME=", shQuote(octave_home)),
             paste0("OMP_NUM_THREADS=", threads), paste0("OPENBLAS_NUM_THREADS=", threads),
             paste0("MKL_NUM_THREADS=", threads))
    t_call0 <- proc.time()[["elapsed"]]
    rc <- system2(octave, c("--norc", "--no-history", "--quiet", "--no-window-system", shQuote(driver)),
                  stdout = logf, stderr = errf, env = env)
    t_call1 <- proc.time()[["elapsed"]]
    done <- file.path(workdir, "done.txt")
    if (!identical(as.integer(rc), 0L) || !file.exists(done)) {
      tail_of <- function(f) if (file.exists(f)) paste(utils::tail(readLines(f, warn = FALSE), 6L), collapse = " | ") else ""
      stop("Octave run failed (exit ", rc, "): ", substr(gsub("\\s+", " ", paste(tail_of(errf), tail_of(logf))), 1L, 600L))
    }
    rd <- function(nm, len) {
      f <- file.path(workdir, paste0(nm, ".bin"))
      v <- readBin(f, what = "double", n = len + 1L, size = 8L)
      if (length(v) != len) stop("output ", nm, " has length ", length(v), ", expected ", len)
      v
    }
    pip <- rd("prob_inclusion", p)
    pip2 <- rd("prob_inclusion2", p)
    logpost <- matrix(rd("logpost", numbofits * numbofreps), numbofits, numbofreps)
    modelsize <- matrix(rd("modelsize", numbofits * numbofreps), numbofits, numbofreps)
    acc <- rd("accept", numbofits)
    zeta <- rd("zeta", 1L)
    A <- rd("zetaAS", p); D <- rd("zetaDS", p)
    dn <- readLines(done, warn = FALSE)
    getd <- function(key) sub(paste0("^", key, " "), "", grep(paste0("^", key, " "), dn, value = TRUE)[1L])
    sampler_sec <- as.numeric(getd("sampler_sec"))
    out$software$octave_version <- getd("octave_version")
    out$software$octave_blas <- getd("blas")
    which_sampler <- readLines(file.path(workdir, "which_sampler.txt"), warn = FALSE)[1L]
    if (!identical(normalizePath(which_sampler), normalizePath(sampler))) stop("Octave resolved ASI_sampler to another file: ", which_sampler)
    if (anyNA(pip) || any(pip < 0 | pip > 1)) stop("ASI_sampler returned PIPs outside [0, 1] or NaN")

    # ---- record what was actually used --------------------------------------
    tag <- function(value, tag, source) list(value = value, tag = tag, source = source)
    REPO <- "authors' repo R/simulation/simulation_example.R @3b95d66; not stated in the Biometrika text"
    # author value in S1; the same value moved to S2 is OURS-1; a ctrl override is OURS
    au <- function(nm, src) if (ov(nm)) list("OURS", paste0("ctrl$", nm, " override (default source: ", src, ")")) else
      if (is_s1) list("author", src) else list("OURS", paste0("OURS-1: the S1 value used unchanged in suite ", suite, "; ", src))
    fx <- function(nm, src) if (ov(nm)) list("OURS", paste0("ctrl$", nm, " override (default source: ", src, ")")) else list("author", src)
    a_g <- au("g", "paper: GLS21 Sec 4.1 p.11 'V_gamma = 9I'"); a_h <- au("h", "paper: GLS21 Sec 4.1 p.11 'h = 10/p'; instructions.pdf p.4 (length 1 = the value of h)")
    a_tau <- au("tau", paste0("repo: target_prop = 0.2; ", REPO)); a_bi <- au("burnin", paste0("repo: Nb = 2000; ", REPO))
    a_ni <- au("numbofits", paste0("repo: N - Nb = 4000 recorded per chain; ", REPO))
    a_nr <- au("numbofreps", paste0("repo: n_chain = 25; ", REPO, "; run scripts use 25; GLS21 Table 1 p.12 reports 5 and 25 chains"))
    a_nu <- fx("nu", "run scripts (run_tecator.m, run_concrete.m): nu = 1; instructions.pdf p.4")
    a_th <- fx("thin", "run scripts: num_thin = 1; instructions.pdf p.4; the repo script has no thinning")
    a_ad <- fx("adap_type", "run scripts: adap_type = 1; instructions.pdf p.5 'infinite adaptation' (NOTE-c)")
    out$settings <- list(
      suite        = tag(suite, "OURS", if (is.null(ctrl$suite)) "default S1 (no ctrl$suite given)" else "ctrl$suite from harness/run_one.R; affects the author/OURS tags only"),
      preprocess   = tag("X <- scale(X); y <- scale(y, scale = FALSE), applied once, in the adapter (R); ASI_sampler.m does not centre or scale", "OURS",
                         "PRE: authors' repo R/simulation/simulation_example.R l.12-13 and dataset_generation.R l.28-29 @3b95d66 (HQ ruling b, 2026-11-25); the run scripts of the original code centre X and y and do not scale"),
      data_fixed   = tag("zeros(n, 0)", "OURS", "OURS-9: code m.17-18, m.67 (no covariate forced in; the code adds its own intercept column); not in instructions.pdf"),
      g            = tag(g, a_g[[1]], a_g[[2]]),
      gprior       = tag(gprior, "author", "instructions.pdf p.4: 1 = g-prior, otherwise independence prior V_gamma = g I; run scripts use 0"),
      mode         = tag(mode, "author", "instructions.pdf p.4: 2 = store sampled models, otherwise not; run scripts use 1"),
      RB_adap      = tag(RB_adap, "author", "run scripts: RB_adap = 1; the argument is not used in the body of ASI_sampler.m"),
      RB           = tag(RB, "author", "run scripts: RB = 1; the argument is not used in the body of ASI_sampler.m (NOTE-b)"),
      hparam       = tag(h, a_h[[1]], a_h[[2]]),
      tau          = tag(tau, a_tau[[1]], a_tau[[2]]),
      nu           = tag(nu, a_nu[[1]], a_nu[[2]]),
      burnin       = tag(burnin, a_bi[[1]], a_bi[[2]]),
      numbofits    = tag(numbofits, a_ni[[1]], a_ni[[2]]),
      thin         = tag(thin, a_th[[1]], a_th[[2]]),
      numbofreps   = tag(numbofreps, a_nr[[1]], a_nr[[2]]),
      heat         = tag(heat, "author", "instructions.pdf p.5: no parallel tempering if heat = 1; run scripts use 1"),
      adap_type    = tag(adap_type, a_ad[[1]], a_ad[[2]]),
      updateg      = tag(updateg, "OURS", "OURS-9: code m.438 (g resampled only if updateg == 1); GLS21 Sec 4.1 fixes g = 9; not in instructions.pdf"),
      kappa        = tag(1e-4, "author", "hard-coded in ASI_sampler.m m.160 (GLS21 Sec 2.4 p.9 says 0.001); not an argument"),
      eps          = tag(0.1 / p, "author", "hard-coded in ASI_sampler.m m.49-50; GLS21 Sec 2.4 p.9 'We use eps = 0.1/p'"),
      zeta_start   = tag(if (nu / (h * p) > 1) 0.1 else nu / (h * p), "author", "ASI_sampler.m m.92-95: nu/(h p), 0.1 if above 1"),
      pip_estimator = tag("output.prob_inclusion: plain mean of gamma over numbofits * numbofreps recorded draws", "author", "ASI_sampler.m m.529, m.565 (NOTE-a, NOTE-b)"),
      seed         = tag(as.numeric(method_seed), "OURS", "OURS-5: INTERFACE.md Seeds; rand('state', method_seed) and randn('state', method_seed) in asi_octave/run_asi.m"),
      selection    = tag("median probability model: PIP > 0.5", "OURS", "OURS-6: INTERFACE.md Selection rule"),
      threads      = tag(threads, "OURS", "OURS-7: Owls compute rule; OMP_NUM_THREADS and OPENBLAS_NUM_THREADS of the Octave process")
    )

    # ---- diagnostics --------------------------------------------------------
    rhat <- NA_real_
    if (numbofreps > 1 && numbofits > 3 && all(is.finite(logpost))) {
      W <- mean(apply(logpost, 2L, stats::var)); B <- numbofits * stats::var(colMeans(logpost))
      if (is.finite(W) && W > 0) rhat <- sqrt(((numbofits - 1) / numbofits * W + B / numbofits) / W)
    }
    pi_final <- A / (A + D)
    sel <- sort(which(pip > 0.5))
    call_sec <- t_call1 - t_call0
    conv <- list(
      burnin = burnin, numbofits = numbofits, thin = thin, numbofreps = numbofreps,
      iterations_total = burnin + numbofits * thin, recorded_draws = numbofits * numbofreps,
      accept_final = acc[length(acc)], zeta_final = zeta, rhat_logpost = rhat,
      mean_model_size = mean(modelsize), sum_pip = sum(pip), n_pip_in_0.4_0.6 = sum(pip > 0.4 & pip < 0.6),
      octave_call_sec = call_sec, sampler_sec = sampler_sec, octave_startup_io_sec = call_sec - sampler_sec,
      r_write_sec = t_w1 - t_w0
    )
    out$selected <- as.integer(sel)
    out$pip <- pip
    out$runtime_sec <- call_sec
    out$extra <- c(list(status = "ok"), conv, list(
      accept_trace_every_100 = acc[unique(c(which(seq_along(acc) %% 100L == 0L), length(acc)))],
      zetaAS_final = A, zetaDS_final = D, pi_final = pi_final,
      prob_inclusion2_all_zero = all(pip2 == 0),
      mean_model_size_by_chain = colMeans(modelsize),
      convergence_note = paste("accept_final is output.accept at the last recorded iteration: the running acceptance rate of all chains pooled, from",
                               "iteration 1, an empty proposal counted as 0 (m.244-247, m.538). zeta_final, zetaAS_final, zetaDS_final are returned",
                               "by the code; pi_final = A/(A+D) and rhat_logpost are derived in the adapter (OURS). No convergence test is applied."),
      n = n, p = p,
      json_summary = c(conv, list(n_selected = length(sel), max_pip = max(pip)))
    ))
    invisible(TRUE)
  }, warning = function(w) {
    warns <<- c(warns, conditionMessage(w))
    invokeRestart("muffleWarning")
  }), error = function(e) e)

  if (!is.null(workdir) && !keep_tmp) unlink(workdir, recursive = TRUE, force = TRUE)
  if (inherits(res, "error")) {
    out$selected <- integer(0)
    out["pip"] <- list(NULL)
    out$extra <- list(status = paste0("failed: ", conditionMessage(res)))
    t_end <- proc.time()[["elapsed"]]
    out$runtime_sec <- if (is.finite(t_call0)) t_end - t_call0 else t_end - t_start
  }
  if (keep_tmp && !is.null(workdir)) out$extra$tmp_dir <- workdir
  out$extra$warnings <- unique(gsub("\\s+", " ", warns))
  out[c("selected", "pip", "runtime_sec", "software", "settings", "extra")]
}
