# test_refine.R -- unit tests for the SuSiE-refine arm (PREREG_c050 R4) in the refine tree of the
# A1 c = 0.5 copy. SuSiE-refine = fit_A1_susie with variant "refine": a1_args() sets refine = TRUE
# and nothing else changes (L = 50, all other arguments, seeds, rules, gates and flags as A1).
# Fixtures: synthetic and seeded (TEST_SEED), plus, when a dev inputs directory is given, the 12 dev
# datasets (inputs only; no truth is read) at scales c100 and c050.
#
# Usage (NOTS compute node): Rscript tests/test_refine.R <code_dir> <out_dir> [<dev_inputs_dir>]
# Prints one line per check; writes <out_dir>/test_results.csv and <out_dir>/refine_cases.csv.
# Exit status 1 if any gate fails.

run_refine_tests <- function(code_dir, out_dir, dev_dir = NULL) {
  cfg <- new.env()
  sys.source(file.path(code_dir, "config.R"), envir = cfg)
  .libPaths(c(cfg$COMMON$LIB, .Library))
  E <- new.env(parent = asNamespace("stats"))
  sys.source(file.path(code_dir, "common.R"), envir = E)
  sys.source(file.path(code_dir, "methods", "fit_A1_susie.R"), envir = E)
  loadNamespace("susieR")
  SP <- cfg$make_settings("primary"); SR <- cfg$make_settings("refine")
  TS <- cfg$TEST_SEED
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  results <- list(); cases <- list()
  check <- function(item, name, ok, detail = "", gate = TRUE) {
    ok <- isTRUE(ok)
    results[[length(results) + 1L]] <<- data.frame(item = item, check = name, pass = ok, gate = gate,
                                                   detail = as.character(detail), stringsAsFactors = FALSE)
    cat(sprintf("[%s] %-4s %s %s\n", if (ok) "PASS" else if (gate) "FAIL" else "NOTE", item, name, detail))
  }
  # One fit exactly as the runner does it: RNG kind and seed reset immediately before the wrapper.
  fit_one <- function(X, y, seed, S) {
    RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
    t0 <- proc.time()[["elapsed"]]
    o <- E$fit_A1_susie(X, y, rep(seq_len(10L), length.out = nrow(X)), seed, S)
    o$runtime_s <- proc.time()[["elapsed"]] - t0
    o
  }
  elbo_final <- function(o) { e <- o$diagnostics$elbo; if (length(e)) e[length(e)] else NA_real_ }
  # Everything the runner saves from the wrapper, except the variant label, the rule role (A1
  # primary vs refine S1, by registry) and the timing.
  same_fit <- function(a, b) {
    da <- a$diagnostics; db <- b$diagnostics; da$variant <- db$variant <- NULL
    ra <- a$rules; rb <- b$rules; ra$role <- rb$role <- NULL
    identical(ra, rb) && identical(a$pip, b$pip) && identical(a$beta, b$beta) &&
      identical(a$converged, b$converged) && identical(da, db) &&
      identical(a$warnings, b$warnings) && identical(a$messages, b$messages)
  }
  std_design <- function(n, p, seed) {
    RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
    X <- scale(matrix(rnorm(n * p), n, p)); attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
    X
  }
  record <- function(case, a, b) {
    ea <- elbo_final(a); eb <- elbo_final(b)
    k <- function(o) paste(paste0(o$rules$rule_id, "=", o$rules$k), collapse = " ")
    cases[[length(cases) + 1L]] <<- data.frame(
      case = case, status_default = a$rules$status[1], status_refine = b$rules$status[1],
      elbo_default = ea, elbo_refine = eb, elbo_gain = eb - ea,
      max_abs_dpip = if (!is.null(a$pip) && !is.null(b$pip)) max(abs(a$pip - b$pip)) else NA_real_,
      identical_outputs = same_fit(a, b), k_default = k(a), k_refine = k(b),
      niter_default = a$diagnostics$niter %||% NA, niter_refine = b$diagnostics$niter %||% NA,
      runtime_default_s = round(a$runtime_s, 2), runtime_refine_s = round(b$runtime_s, 2),
      stringsAsFactors = FALSE)
    c(ea = ea, eb = eb)
  }
  `%||%` <- function(x, y) if (is.null(x)) y else x

  # ---- R1: registry row ----------------------------------------------------------------------
  M <- cfg$METHODS; i <- which(M$method_id == "SuSiE-refine")
  check("R1", "SuSiE-refine registered once, fn fit_A1_susie, variant refine", length(i) == 1L &&
          M$fn[i] == "fit_A1_susie" && M$variant[i] == "refine" && M$package[i] == "susieR" &&
          M$pkg_version[i] == cfg$A1$PKG_VERSION)
  check("R1", "rules pip05/cslead/bfdr10, roles S1/S0/S0", length(i) == 1L &&
          identical(M$rule_ids[[i]], c("pip05", "cslead", "bfdr10")) && identical(M$roles[[i]], c("S1", "S0", "S0")))
  check("R1", "A1 and SuSiE-L100 rows unchanged", identical(M$rule_ids[M$method_id %in% c("A1", "SuSiE-L100")],
          list(c("pip05", "cslead", "bfdr10"), "pip05")) && identical(M$variant[1:2], c("primary", "L100")) &&
          identical(M$roles[1:2], list(c("primary", "S0", "S0"), "S1")))
  check("R1", "rule spec of the refine variant comes from the registry",
        identical(E$a1_rule_spec(SR)$method_id, "SuSiE-refine") && identical(E$a1_rule_spec(SR)$roles, c("S1", "S0", "S0")))

  # ---- R2: susie() arguments identical to A1's except refine ---------------------------------
  X0 <- std_design(50L, 20L, TS); y0 <- drop(X0[, 1:2] %*% c(1, -1)) + rnorm(50L)
  ap <- E$a1_args(X0, y0, cfg$A1$L, SP); ar <- E$a1_args(X0, y0, cfg$A1$L, SR)
  check("R2", "refine = TRUE for SuSiE-refine, FALSE for A1", isTRUE(ar$refine) && identical(ap$refine, FALSE))
  ap$refine <- ar$refine <- NULL
  check("R2", "every other susie() argument identical to A1", identical(ap, ar), paste(length(ar), "arguments"))
  check("R2", "settings identical apart from the variant label",
        identical(SP[setdiff(names(SP), "variant")], SR[setdiff(names(SR), "variant")]))

  # ---- R3: canaries ----------------------------------------------------------------------------
  # R3a null canary: y independent of X, so the default fit reports no credible set and susieR's
  # refinement loop (`while (conti & length(s$sets$cs) > 0)`) never runs: SuSiE-refine must
  # reproduce A1 exactly.
  n <- 200L; p <- 200L; X <- std_design(n, p, TS + 1L)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(TS + 5L); y0n <- rnorm(n)
  a0 <- fit_one(X, y0n, TS + 2L, SP); r0 <- fit_one(X, y0n, TS + 2L, SR)
  e0 <- record("canary_null", a0, r0)
  check("R3a", "null canary: no credible set in the default fit", identical(as.integer(a0$diagnostics$n_cs), 0L))
  check("R3a", "null canary: final ELBO equal", identical(e0[["ea"]], e0[["eb"]]), sprintf("%.6f vs %.6f", e0[["ea"]], e0[["eb"]]))
  check("R3a", "null canary: SuSiE-refine output identical to A1 (rules, PIP, beta, diagnostics, conditions)", same_fit(a0, r0))
  check("R3a", "rule roles follow the registry (A1 primary/S0/S0, refine S1/S0/S0)",
        identical(a0$rules$role, c("primary", "S0", "S0")) && identical(r0$rules$role, c("S1", "S0", "S0")))
  # R3b strong-signal canary (4 effects of size 1, noise sd 1): gates are the ELBO inequality and
  # "equal ELBO implies identical output"; whether refine finds a higher ELBO is recorded only (with
  # L = 50 and tol = 1e-3 the default IBSS can stop on a slow plateau that refine's restart passes).
  b <- numeric(p); b[c(10, 50, 120, 180)] <- c(1, -1, 1, -1)
  y <- drop(X %*% b) + rnorm(n)
  a <- fit_one(X, y, TS + 2L, SP); r <- fit_one(X, y, TS + 2L, SR)
  e <- record("canary_strong", a, r)
  check("R3b", "strong canary: fits not failed", a$rules$status[1] != "failed" && r$rules$status[1] != "failed")
  check("R3b", "refine L = 50 (as A1)", identical(as.integer(r$diagnostics$L), cfg$A1$L) &&
          identical(as.integer(r$diagnostics$L_requested), cfg$A1$L))
  check("R3b", "strong canary: ELBO(refine) >= ELBO(default)", e[["eb"]] >= e[["ea"]], sprintf("gain %.6g", e[["eb"]] - e[["ea"]]))
  check("R3b", "strong canary: equal ELBO implies identical output", e[["eb"]] > e[["ea"]] || same_fit(a, r))
  check("R3b", "strong canary: refine found no better optimum (informative)", identical(e[["ea"]], e[["eb"]]),
        sprintf("gain %.6g, max |dPIP| %.3g, k default %s refine %s", e[["eb"]] - e[["ea"]], max(abs(a$pip - r$pip)),
                paste(a$rules$k, collapse = "/"), paste(r$rules$k, collapse = "/")), gate = FALSE)
  args8 <- E$a1_args(X, y, cfg$A1$L, SP); args8$tol <- 1e-8
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(TS + 2L)
  f8 <- do.call(susieR::susie, args8)
  check("R3b", "strong canary: default A1 run to tol 1e-8 (diagnostic only)", TRUE,
        sprintf("ELBO %.6f after %d iterations (default tol 1e-3: %.6f after %d; refine %.6f)", f8$elbo[length(f8$elbo)],
                f8$niter, e[["ea"]], a$diagnostics$niter, e[["eb"]]), gate = FALSE)

  # R3c plateau case (same design and effects as R3b, the noise drawn right after the design): in
  # the local pre-run (R 4.4.1) default A1 stopped at tol 1e-3 on a slow plateau (6 active effects)
  # and refine reached the tol-1e-8 optimum (ELBO +14.2). Gates: inequality and, when refine
  # improved, a different saved fit; the size of the gain is recorded only.
  Xc <- std_design(n, p, TS + 1L); yc <- drop(Xc %*% b) + rnorm(n)
  ac <- fit_one(Xc, yc, TS + 2L, SP); rc <- fit_one(Xc, yc, TS + 2L, SR)
  ec <- record("plateau_case", ac, rc)
  check("R3c", "plateau case: ELBO(refine) >= ELBO(default)", ec[["eb"]] >= ec[["ea"]], sprintf("gain %.6g", ec[["eb"]] - ec[["ea"]]))
  check("R3c", "plateau case: equal ELBO implies identical output, higher ELBO implies a different fit",
        if (ec[["eb"]] > ec[["ea"]]) !same_fit(ac, rc) else same_fit(ac, rc))
  check("R3c", "plateau case: refine improved the ELBO (informative)", ec[["eb"]] > ec[["ea"]],
        sprintf("gain %.6g, max |dPIP| %.3g, niter default %d refine %d", ec[["eb"]] - ec[["ea"]],
                max(abs(ac$pip - rc$pip)), ac$diagnostics$niter, rc$diagnostics$niter), gate = FALSE)

  # ---- R4: a case built to have a local optimum (two effects masked by their sum) -------------
  # x3 = (x1 + x2) / sqrt(2) + small noise; y = x1 + x2 + noise: IBSS can explain y by x3 first.
  # Not a gate for "refine improves" (whether IBSS is trapped is not guaranteed); the ELBO
  # inequality is a gate.
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(TS + 3L)
  n4 <- 200L; Z <- matrix(rnorm(n4 * 40L), n4, 40L)
  Z[, 3] <- (Z[, 1] + Z[, 2]) / sqrt(2) + 0.05 * rnorm(n4)
  X4 <- scale(Z); attr(X4, "scaled:center") <- NULL; attr(X4, "scaled:scale") <- NULL
  y4 <- drop(X4[, 1] + X4[, 2]) * 0.6 + rnorm(n4)
  a4 <- fit_one(X4, y4, TS + 4L, SP); r4 <- fit_one(X4, y4, TS + 4L, SR)
  e4 <- record("masked_pair", a4, r4)
  check("R4", "masked pair: ELBO(refine) >= ELBO(default)", e4[["eb"]] >= e4[["ea"]],
        sprintf("gain %.6g", e4[["eb"]] - e4[["ea"]]))
  check("R4", "masked pair: refine improved the ELBO (informative, not a gate)", e4[["eb"]] > e4[["ea"]],
        sprintf("gain %.6g; k default %s, refine %s", e4[["eb"]] - e4[["ea"]],
                paste(a4$rules$k, collapse = "/"), paste(r4$rules$k, collapse = "/")), gate = FALSE)
  check("R4", "masked pair: equal ELBO implies identical output", e4[["eb"]] > e4[["ea"]] || same_fit(a4, r4))

  # ---- R5: dev datasets (inputs only), c100 and c050 -----------------------------------------
  if (!is.null(dev_dir)) {
    files <- sort(Sys.glob(file.path(dev_dir, "p[0-9]*", "dev_p*_S*_r001.rds")))
    check("R5", "12 dev input files found", length(files) == 12L, length(files))
    for (f in files) {
      if (grepl("/truth/", normalizePath(f), fixed = TRUE)) stop("refusing a truth file")
      d <- readRDS(f)
      for (sk in c("c100", "c050")) {
        yy <- unname(as.numeric(d$Y[, sk]))
        a5 <- fit_one(d$X, yy, d$method_seed, SP); r5 <- fit_one(d$X, yy, d$method_seed, SR)
        id <- paste0(d$dataset_id, "_", sk); e5 <- record(id, a5, r5)
        check("R5", paste(id, "ELBO(refine) >= ELBO(default)"), isTRUE(e5[["eb"]] >= e5[["ea"]]),
              sprintf("gain %.6g", e5[["eb"]] - e5[["ea"]]))
        check("R5", paste(id, "equal ELBO implies identical output"),
              isTRUE(e5[["eb"]] > e5[["ea"]]) || same_fit(a5, r5))
      }
    }
  }

  R <- do.call(rbind, results); C <- do.call(rbind, cases)
  utils::write.csv(R, file.path(out_dir, "test_results.csv"), row.names = FALSE)
  utils::write.csv(C, file.path(out_dir, "refine_cases.csv"), row.names = FALSE)
  options(width = 200); print(C, row.names = FALSE)
  nf <- sum(!R$pass & R$gate)
  cat(sprintf("\n%d checks, %d gate failures, %d notes\n", nrow(R), nf, sum(!R$pass & !R$gate)))
  invisible(nf == 0L)
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  ok <- run_refine_tests(normalizePath(a[1]), a[2], if (length(a) >= 3L) a[3] else NULL)
  quit(status = if (ok) 0L else 1L)
}
