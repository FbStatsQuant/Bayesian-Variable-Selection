# test_ls0.R -- LS0 behaviour fixtures on the new core (testing copy with C-ENG exports).
# Usage: Rscript test_ls0.R <core_dir> <work_dir> <variant: normal|stop|numfail> <out_txt>
#   normal : deterministic fixtures F1-F5 (low-N direct final runs + public v3_fit)
#   stop   : testing copy whose runtime guard reports "exceeded" at checkpoint "ls0" (GUARD-W)
#   numfail: testing copy whose scorer throws a NumericalFailure at the 5th model scored by LS0
args <- commandArgs(TRUE); core <- args[1]; work <- args[2]; variant <- args[3]; out <- args[4]
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "ceng_load.R"))
ceng_load(core, work, exports = TRUE, force_stop = if (variant == "stop") "ls0" else NULL, numfail_ls0 = variant == "numfail")
sink(out, split = TRUE)
cat("C-ENG test_ls0.R variant =", variant, " date =", format(Sys.time()), "\ncore =", normalizePath(core), "\n\n")
n_pass <- 0; n_fail <- 0
check <- function(name, ok) {
  ok <- isTRUE(ok); if (ok) n_pass <<- n_pass + 1 else n_fail <<- n_fail + 1
  cat(sprintf("  [%s] %s\n", if (ok) "PASS" else "FAIL", name))
}
same <- function(a, b) identical(as.integer(a), as.integer(b))
lexless <- function(a, b) { n <- min(length(a), length(b)); for (i in seq_len(n)) if (a[i] != b[i]) return(a[i] < b[i]); length(a) < length(b) }
hpm_better <- function(F1, S1, F2, S2) { if (F1 != F2) return(F1 > F2); if (length(S1) != length(S2)) return(length(S1) < length(S2)); lexless(S1, S2) }

scenario_covariance <- function(scenario, p) {
  group <- ceiling(seq_len(p)/5); H <- outer(group,group,"=="); I <- diag(p)
  switch(as.integer(scenario), I, 0.5^abs(outer(seq_len(p),seq_len(p),"-")), 0.7*H+0.3*I, 0.85*H+0.15*I,
    0.3*matrix(1,p,p)+0.4*H+0.3*I, {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})
}
active <- c(3L, 7L, 14L, 16L, 25L); beta <- numeric(30); beta[active] <- c(1.4, -1.0, 1.8, -1.2, 0.8)
make_data <- function(scen, seed, n = 100, scale = 1, dup = NULL) {
  set.seed(seed); p <- 30
  X <- scale(matrix(rnorm(n * p), nrow = n) %*% chol(scenario_covariance(scen, p)))
  if (!is.null(dup)) for (d in dup) X[, d[1]] <- X[, d[2]]          # exact duplicate columns
  attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  list(X = X, y = drop(scale * (X %*% beta) + rnorm(n)))
}
setup_of <- function(d) {
  pre <- v3_preprocess(d$X, d$y, dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  v3_setup(ctx)
}
# direct final run with a tiny sampler (testing settings: N particles, L burn-in, grid (0, 1)); LS0 on
low_run <- function(setup, N = 2L, L = 0L, seed = 11, inherited = NULL, ls0_ell = NULL, ls0 = TRUE, islands = 4L, ell = NULL) {
  b <- setup$budgets
  ro <- list(N = as.integer(N), L = as.integer(L), measured_rounds = 4L, islands = as.integer(islands), tier = 0L,
             ell = as.integer(ell %||% b$ell),
             cache_capacity = as.numeric(500 * setup$ctx$p))
  if (ls0) { ro$ls0 <- TRUE; ro$ls0_ell <- as.integer(ls0_ell %||% b$ell); ro$ls0_tie_dp <- TRUE }
  fr <- v3_frozen(c(0, 1), tier = 0, N = N, L = L, inherited = inherited)
  raw <- .v3cpp$cpp_final_run(setup$ptr, c(0, 1), ro, seed, inherited, NULL)
  list(raw = raw, fit = v3_assemble_final(raw, setup, fr, ro, seed), ro = ro)
}

if (variant == "normal") {
  # ---------------- F1: centre emitted; exact LS0 event count; centre first scored by LS0 and the HPM ----------------
  cat("F1: start mode unscored before LS0, exact event count, centre provenance\n")
  # integrated run (testing settings: 1 island, 1 particle, final search ell = 0, LS0 at the production ell)
  sd <- 1; d <- make_data(1, 1001, scale = 0.6); st <- setup_of(d)
  r <- low_run(st, N = 1L, seed = sd, islands = 1L, ell = 0L, ls0_ell = st$budgets$ell)
  f <- r$fit; l0 <- f$ls0; lg <- f$score_counts$logical; fr <- f$score_counts$fresh
  cat("  dataset seed 1001 : start mode {", f$start_mode$model, "} ties", f$start_mode$ties, "; HPM {", f$hpm, "} provenance",
      f$hpm_provenance$phase, "; LS0 termination", l0$termination, "moves", l0$moves, "
")
  # R01 #5 observability: a start mode that is a strict local maximum is the HPM of a standalone LS0 ledger iff emitted.
  # (In 200 integrated low-N fixtures the start mode never beat the sampler's HPM, so the integrated provenance case is
  #  not constructible this way; the exact integrated event count below is the integrated evidence.)
  found <- FALSE
  for (sd2 in 1:200) {
    d2 <- make_data(c(1, 3, 4)[(sd2 %% 3) + 1], 5000 + sd2, scale = 0.6); st2 <- setup_of(d2)
    m2 <- .v3cpp$t_setup_start_mode(st2$ptr, 1e6, TRUE)
    a2 <- .v3cpp$t_local_search(st2$ptr, m2$model, st2$budgets$ell, TRUE, TRUE)
    if (a2$moves == 0 && identical(a2$termination, "no_improvement")) { found <- TRUE; break }
  }
  b2 <- .v3cpp$t_local_search(st2$ptr, m2$model, st2$budgets$ell, FALSE, TRUE)
  cat("  local-max start mode found at dataset seed", 5000 + sd2, ": {", m2$model, "}
")
  check("found a start mode that is a strict local maximum (LS0 0 moves, no_improvement)", found)
  check("emitted: standalone LS0 HPM == centre, provenance ls0 stage 0 position 0", same(a2$ledger$hpm$model, m2$model) &&
        identical(a2$ledger$hpm$provenance$phase, "ls0") && a2$ledger$hpm$provenance$stage == 0 && a2$ledger$hpm$provenance$position == 0)
  check("not emitted: the centre is never scored, so the HPM differs from the centre", !same(b2$ledger$hpm$model, m2$model))
  check("status completed, LS0 archive present, centre == start mode", f$status == "completed" && length(l0) > 0 && same(l0$centre, f$start_mode$model))
  sm_ind <- .v3cpp$t_setup_start_mode(st$ptr, 1e6, TRUE)
  check("MR1: LS0 centre == start_mode(st, 1e6).S recomputed independently on the run's own Start (setup)", same(l0$centre, sm_ind$model) &&
        identical(f$start_mode$log_gamma0, sm_ind$lg0))
  check("MR2: cap = 1 with the fallback is rejected", inherits(tryCatch(.v3cpp$t_setup_start_mode(st$ptr, 1, TRUE), error = function(e) e), "error"))
  check("logical ls0 events == 1 (emitted centre) + n_evaluated", sum(lg["ls0", ]) == l0$n_evaluated + 1)
  check("all LS0 events are mechanism local_scan", sum(lg["ls0", ]) == lg["ls0", "local_scan"])
  sa <- .v3cpp$t_local_search(st$ptr, f$start_mode$model, st$budgets$ell, TRUE, TRUE)
  check("standalone LS0 (own ledger, no cache) has the same path/termination/n_evaluated", identical(sa$path, l0$path) &&
        identical(sa$termination, l0$termination) && sa$n_evaluated == l0$n_evaluated && identical(sa$scanned_centres, l0$scanned_centres))
  check("standalone fresh ls0 count == n_evaluated + 1 (centre emitted as a fresh score)", sum(sa$ledger$fresh["ls0", ]) == sa$n_evaluated + 1)
  sb <- .v3cpp$t_local_search(st$ptr, f$start_mode$model, st$budgets$ell, FALSE, TRUE)
  check("emit_centre = FALSE gives one event fewer (omission is observable)", sum(sb$ledger$logical["ls0", ]) == sum(sa$ledger$logical["ls0", ]) - 1)
  check("ls0_improved == (HPM F after LS0 > before)", identical(f$flags$ls0_improved, f$hpm_F > r$raw$hpm_before_ls0$F))
  check("E3 computed from the HPM before LS0 (final search only)", identical(f$flags$E3, r$raw$hpm_before_ls0$F > r$raw$hpm_before_local$F))
  check("other counter rows unchanged by the ls0 row (row layout: v3 rows + ls0)", identical(rownames(lg), c(rownames(lg)[1:10], "ls0")))

  # ---------------- F2: strict improving neighbour + ls0_ell = 0 => capped LS0, output returned ----------------
  cat("\nF2: LS0 capped at ell = 0 with a strict improving neighbour\n")
  found <- FALSE
  for (sd in 1:60) {
    d <- make_data(4, 2000 + sd, scale = 0.5); st <- setup_of(d)
    r <- low_run(st, seed = sd)
    if (r$fit$status == "completed" && r$fit$ls0$moves >= 1) { found <- TRUE; break }
  }
  check("found a fixture where LS0 makes >= 1 strict move", found)
  r0 <- low_run(st, seed = sd, ls0_ell = 0L); f0 <- r0$fit
  cat("  dataset seed", 2000 + sd, ": LS0 moves at ell =", st$budgets$ell, ":", r$fit$ls0$moves, "; at ell = 0: termination", f0$ls0$termination, "\n")
  check("ell = 0: termination move_limit, ls0_local_limit TRUE", identical(f0$ls0$termination, "move_limit") && isTRUE(f0$ls0_local_limit))
  check("ell = 0: status completed, estimates available (a capped LS0 is not a stop)", f0$status == "completed" && isTRUE(f0$estimates_available) && is.finite(f0$log_Z))
  check("public local_limit = final OR ls0 cap; flags carry attribution", isTRUE(f0$local_limit) && isTRUE(f0$flags$local_limit) &&
        identical(f0$flags$final_local_limit, isTRUE(f0$local_search$local_limit)) && isTRUE(f0$flags$ls0_local_limit))
  check("capped LS0 contributes no certificate", !identical(f0$local_certified_by, "ls0") && !identical(f0$local_certified_by, "both"))
  check("ls0_ell recorded in the archive", identical(f0$ls0$ell, 0L))

  # ---------------- F3: equal-F HPM tie change by LS0 (two duplicated column pairs) ----------------
  cat("\nF3: equal-F tie change by LS0 (columns 6 := 7, 15 := 16; inherited HPM {3,7,14,16,25})\n")
  inh <- list(models = list(c(3L, 7L, 14L, 16L, 25L)))
  for (sd in 1:100) {
    d <- make_data(1, 3000 + sd, scale = 1, dup = list(c(6, 7), c(15, 16))); st <- setup_of(d)
    r <- low_run(st, N = 1L, seed = sd, inherited = inh, islands = 1L, ell = 0L, ls0_ell = st$budgets$ell); f <- r$fit
    if (isTRUE(f$flags$ls0_hpm_changed) && !isTRUE(f$flags$ls0_improved)) break
  }
  cat("  dataset seed", 3000 + sd, "
")
  Fs <- vapply(list(c(3,7,14,16,25), c(3,6,14,16,25), c(3,7,14,15,25), c(3,6,14,15,25)), function(S) v3_score(st$ctx, as.integer(S))$F, 0)
  cat("  F of {3,7,14,16,25}, {3,6,14,16,25}, {3,7,14,15,25}, {3,6,14,15,25}:", format(Fs, digits = 17), "\n")
  cat("  HPM before local {", r$raw$hpm_before_local$model, "} after final search {", r$raw$hpm_before_ls0$model, "} start mode {",
      f$start_mode$model, "} final HPM {", f$hpm, "} provenance", f$hpm_provenance$phase, "\n")
  cat("  ls0_improved", f$flags$ls0_improved, " ls0_hpm_changed", f$flags$ls0_hpm_changed, " E3", f$flags$E3, " local_certified", f$local_certified,
      "by", f$local_certified_by, "\n")
  tie_case <- length(unique(Fs)) == 1 && isTRUE(f$flags$ls0_hpm_changed) && !isTRUE(f$flags$ls0_improved)
  check("four duplicate-swap models have bitwise-equal F", length(unique(Fs)) == 1)
  check("LS0 changed the HPM through the tie rule without raising F (ls0_hpm_changed TRUE, ls0_improved FALSE)", tie_case)
  check("tie change: new HPM is hpm_better than the HPM before LS0, provenance ls0",
        hpm_better(f$hpm_F, f$hpm, r$raw$hpm_before_ls0$F, r$raw$hpm_before_ls0$model) && identical(f$hpm_provenance$phase, "ls0"))
  check("E3 not fired by LS0 (E3 == final-search increase only)", identical(f$flags$E3, r$raw$hpm_before_ls0$F > r$raw$hpm_before_local$F))
  # returned HPM vs both search endpoints; certificate formula
  fe <- f$local_search$returned; le <- f$ls0$returned
  cat("  final search returned {", fe, "} LS0 returned {", le, "}\n")
  cf <- isTRUE(f$local_search$local_certified) && same(f$hpm, fe); cl <- isTRUE(f$ls0$local_certified) && same(f$hpm, le)
  check("local_certified == (final certified & HPM == final endpoint) OR (LS0 certified & HPM == LS0 endpoint)", identical(f$local_certified, cf || cl))
  check("final-search HPM tie change: HPM after final search differs from the final search's returned model",
        !same(r$raw$hpm_before_ls0$model, fe))

  # ---------------- F4: switch off on the same fixture: v3 behaviour ----------------
  cat("\nF4: ls0 = FALSE on the F3 fixture\n")
  r_off <- low_run(st, N = 1L, seed = sd, inherited = inh, islands = 1L, ell = 0L, ls0 = FALSE); g <- r_off$fit
  check("no LS0 fields in raw or fit", is.null(r_off$raw$ls0) && is.null(g$ls0) && is.null(g$start_mode) && is.null(g$flags$ls0_improved))
  check("counter matrices have the v3 layout (10 phases, no ls0 row)", nrow(g$score_counts$logical) == 10 && !"ls0" %in% rownames(g$score_counts$logical))
  check("islands identical with LS0 on/off", identical(lapply(r$raw$islands, function(x) x[names(x) != "seconds"]),
                                                       lapply(r_off$raw$islands, function(x) x[names(x) != "seconds"])))
  check("off HPM == on HPM before LS0", same(g$hpm, r$raw$hpm_before_ls0$model) && identical(g$hpm_F, r$raw$hpm_before_ls0$F))
  check("E3 identical on/off", identical(g$flags$E3, f$flags$E3))

  # ---------------- F5: public v3_fit, NA-field helper on a non-output return ----------------
  cat("\nF5: public v3_fit\n")
  d <- make_data(3, 4001)
  fit <- v3_fit(d$X, d$y, 4001)
  check("SMC branch, completed, LS0 archive and flags present", fit$branch_run == "smc" && fit$status == "completed" &&
        length(fit$ls0) > 0 && !is.null(fit$flags$ls0_improved) && "ls0" %in% rownames(fit$score_counts$logical))
  check("runtime guard has an ls0 checkpoint after the local_search checkpoint", {
    cps <- vapply(fit$runtime_guard$checkpoints, function(x) x$checkpoint, ""); any(cps == "ls0") && max(which(cps == "local_search")) < which(cps == "ls0")[1] })
  bad <- v3_fit(d$X, d$y, -1)
  check("invalid seed (no output): log_Z NA by exact name and via $", is.na(bad[["log_Z", exact = TRUE]]) && is.na(bad$log_Z) &&
        all(c("log_Z", "pip_primary", "mpm", "log_Z_r") %in% names(bad)))
  bad0 <- v3_fit(d$X, d$y, -1, ls0 = FALSE)
  check("ls0 = FALSE: v3 behaviour (no NA estimate fields added)", !("log_Z" %in% names(bad0)))
}

if (variant == "stop") {
  cat("GUARD-W: guard reports exceeded at checkpoint ls0\n")
  d <- make_data(3, 4001)
  fit <- v3_fit(d$X, d$y, 4001)
  check("status resource_limit", identical(fit$status, "resource_limit"))
  check("estimates_available FALSE, partial_results TRUE", identical(fit$estimates_available, FALSE) && isTRUE(fit$partial_results))
  check("fit[['log_Z', exact = TRUE]] is NA and fit$log_Z is NA (no partial match to log_Zbar0)",
        is.na(fit[["log_Z", exact = TRUE]]) && is.na(fit$log_Z) && is.finite(fit$log_Zbar0))
  check("every estimate field NA by exact name", all(vapply(V3_ESTIMATE_FIELDS, function(nm) length(fit[[nm, exact = TRUE]]) == 1 && is.na(fit[[nm, exact = TRUE]]), TRUE)))
  check("the guard record shows checkpoint ls0 exceeded", any(vapply(fit$runtime_guard$checkpoints, function(x) x$checkpoint == "ls0" && isTRUE(x$exceeded), TRUE)))
  check("LS0 archive kept (labelled), HPM labelled incomplete", length(fit$ls0) > 0 && isTRUE(fit$hpm_incomplete))
  fit0 <- v3_fit(d$X, d$y, 4001, ls0 = FALSE)
  check("same copy with ls0 = FALSE: completed (no ls0 checkpoint)", identical(fit0$status, "completed") &&
        !any(vapply(fit0$runtime_guard$checkpoints, function(x) x$checkpoint == "ls0", TRUE)))
  # adapter mapping of the stopped fit (study adapter must read the NA markers as unavailable)
  source(file.path(here, "..", "..", "..", "..", "Scripts", "SMC_BVS", "study", "adapter.R"))
  o <- tryCatch(smcbvs_outputs(fit, 30L), error = function(e) conditionMessage(e))
  check("study adapter smcbvs_outputs accepts the stopped fit (estimates unavailable, PIPs NA)", is.list(o) && identical(o$estimates_available, FALSE) && all(is.na(o$pip)))
  o2 <- tryCatch(smcbvs_outputs(fit0, 30L), error = function(e) conditionMessage(e))
  check("study adapter on the completed fit: available, MPM = PIP > .5", is.list(o2) && isTRUE(o2$estimates_available))
}

if (variant == "numfail") {
  cat("GUARD-W: NumericalFailure inside LS0\n")
  d <- make_data(3, 4001)
  fit <- v3_fit(d$X, d$y, 4001)
  check("status numerical_failure", identical(fit$status, "numerical_failure"))
  check("message names the injection", grepl("C-ENG TEST INJECTION", fit$message))
  check("estimates unavailable, every estimate field NA by exact name", identical(fit$estimates_available, FALSE) &&
        all(vapply(V3_ESTIMATE_FIELDS, function(nm) length(fit[[nm, exact = TRUE]]) == 1 && is.na(fit[[nm, exact = TRUE]]), TRUE)) && is.na(fit$log_Z))
  check("HPM labelled incomplete", isTRUE(fit$hpm_incomplete))
  fit0 <- v3_fit(d$X, d$y, 4001, ls0 = FALSE)
  check("same copy with ls0 = FALSE: completed", identical(fit0$status, "completed"))
}
if (variant == "paths") {
  # Local analogue of the API-AUDIT forced-stop table (10 fits, allocation 0.05 s; METHOD_v3.1_FINAL section 6 item 3),
  # after the NA fix, plus every early public return of v3_fit, each consumed by the study adapter.
  source(file.path(here, "..", "..", "..", "..", "Scripts", "SMC_BVS", "study", "adapter.R"))
  na_ok <- function(fit) all(vapply(V3_ESTIMATE_FIELDS, function(nm) length(fit[[nm, exact = TRUE]]) == 1 && is.na(fit[[nm, exact = TRUE]]), TRUE)) &&
    is.na(fit$log_Z) && is.na(fit$pip_primary) && is.na(fit$mpm)
  adapter_ok <- function(fit, p) { o <- tryCatch(smcbvs_outputs(fit, p), error = function(e) conditionMessage(e)); is.list(o) && identical(o$estimates_available, FALSE) && all(is.na(o$pip)) }
  cat("Forced stops (allocation hours = 0.05 / 3600), 10 fits\n")
  rows <- list()
  for (i in 1:10) {
    d <- make_data(((i - 1) %% 6) + 1, 6000 + i)
    fit <- v3_fit(d$X, d$y, 6000 + i, allocation = list(mem_gb = 8, hours = 0.05 / 3600))
    hit <- Filter(function(x) isTRUE(x$exceeded), fit$runtime_guard$checkpoints)
    rows[[i]] <- data.frame(id = i, status = fit$status, estimates_available = !identical(fit$estimates_available, FALSE),
      hpm_incomplete = isTRUE(fit$hpm_incomplete), all_fields_NA = na_ok(fit), dollar_log_Z_is_NA = is.na(fit$log_Z),
      log_Zbar0_finite = is.finite(fit$log_Zbar0 %||% NA), adapter_ok = adapter_ok(fit, 30L),
      checkpoint = if (length(hit)) hit[[1]]$checkpoint else NA, phase = if (length(hit)) hit[[1]]$phase else NA)
  }
  tab <- do.call(rbind, rows); print(tab, row.names = FALSE)
  check("10/10 forced stops: resource_limit, estimates unavailable, hpm_incomplete", all(tab$status == "resource_limit") && !any(tab$estimates_available) && all(tab$hpm_incomplete))
  check("10/10: every estimate field NA by exact name; fit$log_Z is NA (not log_Zbar0)", all(tab$all_fields_NA) && all(tab$dollar_log_Z_is_NA))
  check("10/10: study adapter maps the stop to unavailable PIPs without error", all(tab$adapter_ok))
  cat("\nEarly public returns\n")
  d <- make_data(1, 7001)
  f1 <- v3_fit(d$X, rep(1, 100), 7001)
  check(sprintf("y constant: status %s, NA fields, adapter ok", f1$status), f1$status == "y_constant" && na_ok(f1) && adapter_ok(f1, 30L))
  f2 <- v3_fit(matrix(1, 100, 30), d$y, 7001)
  check(sprintf("no predictors: status %s, NA fields, adapter ok", f2$status), f2$status == "no_predictors" && na_ok(f2) && adapter_ok(f2, 30L))
  f3 <- v3_fit(d$X, d$y, 7001, allocation = list(mem_gb = 1e-6, hours = 24))
  check(sprintf("preflight memory: status %s, NA fields, adapter ok", f3$status), f3$status == "resource_limit" && isTRUE(f3$preflight$exceeds) && na_ok(f3) && adapter_ok(f3, 30L))
  f4 <- v3_fit(d$X, d$y, -5)
  check(sprintf("invalid seed: status %s, NA fields", f4$status), f4$status == "invalid_input" && na_ok(f4))
  f5 <- v3_fit(d$X[, 1:8], d$y, 7001)
  o5 <- smcbvs_outputs(f5, 8L)
  check(sprintf("exact branch (p = 8): status %s, estimates present and finite, no LS0", f5$status), f5$status == "exact" &&
        isTRUE(f5$estimates_available) && is.finite(f5$log_Z) && all(is.finite(f5$pip_primary)) && is.null(f5$ls0) && isTRUE(o5$estimates_available))
  f6 <- v3_fit(d$X, d$y, 7001)
  o6 <- smcbvs_outputs(f6, 30L)
  check("completed SMC fit: estimates finite, adapter available, MPM == PIP > .5", f6$status == "completed" &&
        is.finite(f6$log_Z) && isTRUE(o6$estimates_available) && identical(o6$mpm, unname(which(o6$pip > 0.5))))
  f7 <- v3_fit(d$X, d$y, 7001, allocation = list(mem_gb = 8, hours = 0.05 / 3600), ls0 = FALSE)
  check("switch off: forced stop keeps the v3 output (no log_Z field; log_Zbar0 present)", f7$status == "resource_limit" && !("log_Z" %in% names(f7)))
}
cat(sprintf("\nTOTAL: %d PASS, %d FAIL\n", n_pass, n_fail))
sink()
