# Test code only. List-renormalised PIP fields of core v3 (SPEC_LIST_PIP.md §7, tests B4-B11 and A3; HQ order 2026-11-17).
#   Rscript --vanilla list_pip_units.R <core_dir> [work_dir]
# Sources core's v3.R (compiles into core's .cpp_cache), so pass a COPY of core/ when core/ must stay unwritten.
# The bit-identity tests A1/A2 (old core vs new core, same fits) are in the engine's report (ab_run.R), not here.
args <- commandArgs(TRUE)
core_dir <- normalizePath(args[1])
here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
source(file.path(here, "common.R"))
V3_CORE_DIR <- core_dir
source(file.path(core_dir, "v3.R"))
n_ok <- 0L
chk <- function(cond, what) { need(isTRUE(cond), paste("FAILED:", what)); n_ok <<- n_ok + 1L }
near <- function(a, b, tol) isTRUE(all(abs(a - b) <= tol)) && length(a) == length(b)
store <- function(models, value, full = FALSE) list(models = lapply(models, as.integer), value = value, capacity = 41, full = full)
LF <- function(models, value, p, full = FALSE) { orig <- seq_len(p); v3_list_fields(store(models, value, full), orig, as.character(orig)) }

# ---- B4: store {1}, {1,2}, {3}; scores c + log .5, .3, .2; c = 0, 1000, -1000 ------------------------------------------
for (cc in c(0, 1000, -1000)) {
  r <- LF(list(1L, c(1L, 2L), 3L), cc + log(c(.5, .3, .2)), 3)
  chk(near(unname(r$pip_list), c(.8, .3, .2), 1e-12), paste("B4 pip_list c =", cc))
  chk(identical(r$mpm_list, 1L), paste("B4 mpm_list c =", cc))
  chk(near(r$log_Z_list, cc, 1e-12 * max(1, abs(cc))), paste("B4 log_Z_list c =", cc))
  chk(is.null(r$pip_list_flag) && r$list_size == 3L && !r$list_full && identical(r$pip_list_source, "store"), "B4 scalars")
}
# ---- B5: one model {2, 5} on p = 6 -------------------------------------------------------------------------------------
r <- LF(list(c(2L, 5L)), 3.25, 6)
chk(identical(unname(r$pip_list), c(0, 1, 0, 0, 1, 0)) && identical(r$mpm_list, c(2L, 5L)) && identical(r$log_Z_list, 3.25), "B5 single model")
chk(identical(names(r$pip_list), as.character(1:6)), "B5 names")
# ---- B6: empty model and {1} with equal scores: pip_list[1] = .5 exactly, strict rule leaves mpm_list empty ----------------
r <- LF(list(integer(0), 1L), c(0, 0), 2)
chk(identical(unname(r$pip_list), c(.5, 0)) && identical(r$mpm_list, integer(0)) && near(r$log_Z_list, log(2), 1e-15), "B6 tie 0.5 and empty model")
# ---- B7: scores differ by 800: no NaN/Inf, pip_list = indicator of the better model ------------------------------------------
r <- LF(list(c(1L, 3L), 2L), c(0, -800), 3)
chk(all(is.finite(r$pip_list)) && near(unname(r$pip_list), c(1, 0, 1), 1e-12) && r$log_Z_list == 0, "B7 800 apart")
r <- LF(list(2L, c(1L, 3L)), c(0, -800), 3); chk(near(unname(r$pip_list), c(0, 1, 0), 1e-12), "B7 order of the models")
# ---- §4 cases ----------------------------------------------------------------------------------------------------------------
r <- LF(list(1L, 2L), c(-Inf, -3), 3); chk(identical(unname(r$pip_list), c(0, 1, 0)) && r$log_Z_list == -3, "-Inf entry has weight 0")
r <- LF(list(1L, 2L), c(NaN, 1), 3); chk(identical(r$pip_list_flag, "nonfinite_score") && all(is.na(r$pip_list)) && is.na(r$log_Z_list) && is.na(r$mpm_list), "NaN score")
r <- LF(list(1L, 2L), c(Inf, 1), 3); chk(identical(r$pip_list_flag, "nonfinite_score"), "+Inf score")
# Theory-confirmed via HQ 11-17: -Inf has weight 0; ALL scores -Inf (normaliser 0) -> every field NA and flag "nonfinite_score"
r <- LF(list(1L, 2L), c(-Inf, -Inf), 3)
chk(identical(r$pip_list_flag, "nonfinite_score") && length(r$pip_list) == 3 && all(is.na(r$pip_list)) && identical(names(r$pip_list), as.character(1:3)) &&
    is.na(r$mpm_list) && is.na(r$log_Z_list) && r$list_size == 2L, "all -Inf: fields NA, flag nonfinite_score")
r <- LF(list(integer(0)), -Inf, 2); chk(identical(r$pip_list_flag, "nonfinite_score") && all(is.na(r$pip_list)), "a single -Inf entry (0/0)")
r <- LF(list(), numeric(0), 3); chk(identical(r$pip_list_flag, "empty_list") && all(is.na(r$pip_list)) && r$list_size == 0L, "empty list is flagged")
chk(inherits(try(LF(list(1L, 2L, 1L), c(0, -1, -2), 3), silent = TRUE), "try-error"), "duplicate model stops")
r <- LF(list(integer(0)), -7, 2); chk(identical(unname(r$pip_list), c(0, 0)) && identical(r$mpm_list, integer(0)) && r$log_Z_list == -7, "the empty model alone")
r <- LF(list(1L, c(1L, 2L)), c(0, -1), 3, full = TRUE); chk(r$list_full && r$pip_list[[1]] == 1 && r$pip_list[[3]] == 0, "column in every / in no listed model is exactly 1 / 0")
# nonconsecutive original indices (retained columns after a dropped constant): names and positions
r <- v3_list_fields(store(list(c(2L, 7L), 7L, 4L), c(0, -1, -2)), c(2L, 4L, 7L), c("2", "4", "7"))
chk(identical(names(r$pip_list), c("2", "4", "7")) && identical(r$mpm_list, c(2L, 7L)) && r$pip_list[["4"]] > 0 && r$pip_list[["4"]] < 0.5, "original indices")
# error precedence (review PR68 MINOR-4): a duplicate model stops even when a score is non-finite or all scores are -Inf
chk(inherits(try(LF(list(1L, 2L, 1L), c(NaN, -1, -2), 3), silent = TRUE), "try-error"), "duplicate + NaN: stops")
chk(inherits(try(LF(list(1L, 1L), c(-Inf, -Inf), 3), silent = TRUE), "try-error"), "duplicate + all -Inf: stops")
# the flagged result is NA everywhere (mpm_list NA, never an empty vector = a valid empty MPM)
r <- LF(list(1L, 2L), c(NaN, 0), 3); chk(identical(r$mpm_list, NA_integer_) && all(is.na(r$pip_list)) && is.na(r$log_Z_list), "flagged: mpm_list is NA_integer_")
# the reviewer's fixed store (review PR68 MINOR-5): one unit weight and eight weights near 2^-54. Reverse order adds the small ones first
# (8 x 2^-54 = 2^-51, then +1 = 1 + 2^-51); first-to-last order loses every one of them (1 + 2^-54 rounds to 1). The numerator of a column in
# the unit model and four small ones: reverse 1 + 2^-52, first-to-last 1.
Fs <- c(0, rep(-54 * log(2), 8)); Ms <- list(c(1L, 2L), c(2L, 3L), c(2L, 4L), c(2L, 5L), c(2L, 6L), c(3L, 7L), c(3L, 8L), c(3L, 9L), c(3L, 10L))
r <- LF(Ms, Fs, 10)
u <- exp(Fs - max(Fs)); rev_den <- 0; fwd_den <- 0; rev_n2 <- 0; fwd_n2 <- 0
for (i in 9:1) { rev_den <- rev_den + u[i]; if (2L %in% Ms[[i]]) rev_n2 <- rev_n2 + u[i] }
for (i in 1:9) { fwd_den <- fwd_den + u[i]; if (2L %in% Ms[[i]]) fwd_n2 <- fwd_n2 + u[i] }
chk(rev_den > fwd_den && fwd_den == 1 && rev_n2 / rev_den != fwd_n2 / fwd_den, "the fixed store separates the two orders")
chk(identical(r$log_Z_list, max(Fs) + log(rev_den)) && r$log_Z_list > 0, "fixed store: log_Z_list from the reverse-order denominator")
chk(identical(unname(r$pip_list[2]), rev_n2 / rev_den), "fixed store: the numerator is also summed last to first")
# summation order: plain double, last to first (differs from sum()'s long double in the last bit for adversarial weights)
set.seed(1); Fv <- -rexp(2000) * 5; ms <- lapply(seq_along(Fv), function(i) sort(sample.int(30, sample(0:5, 1)))); ms <- ms[!duplicated(vapply(ms, paste, "", collapse = ","))]
Fv <- Fv[seq_along(ms)]
r <- LF(ms, Fv, 30)
u <- exp(Fv - max(Fv)); den <- 0; for (i in length(u):1) den <- den + u[i]
chk(identical(r$log_Z_list, max(Fv) + log(den)), "denominator summed last to first in double")
# B10: bounds, the support bound, permutation invariance
chk(all(r$pip_list >= 0 & r$pip_list <= 1), "B10 bounds")
w1 <- u[1] / den; ind <- as.numeric(seq_len(30) %in% ms[[1]])
chk(max(abs(r$pip_list - ind)) <= 1 - w1 + 1e-12, "B10 support bound")
perm <- sample(length(ms)); r2 <- LF(ms[perm], Fv[perm], 30)
chk(max(abs(r2$pip_list - r$pip_list)) <= 1e-12 && abs(r2$log_Z_list - r$log_Z_list) <= 1e-12, "B10 permutation")
cat("hand cases ok:", n_ok, "checks\n")

# ---- fits ------------------------------------------------------------------------------------------------------------------------
NEWF <- c("pip_list", "mpm_list", "log_Z_list", "list_size", "list_full", "pip_list_source", "pip_list_flag")
fit_ok <- function(id, ls0 = TRUE) { d <- fixture(id); v3_fit(d$X, d$y, 1000L + id, allocation = list(mem_gb = 4, hours = 2), ls0 = ls0) }
# B8 + B9: fixtures 1-6 (small p, constant columns dropped, nonconsecutive original indices)
n_exact <- 0L; n_all <- 0L
for (id in 1:6) {
  fit <- fit_ok(id)
  chk(fit$status %in% c("exact", "completed"), paste("fixture", id, "status", fit$status))
  chk(identical(names(fit$pip_list), names(fit$pip_primary)), paste("B8 names, fixture", id))
  chk(all(fit$pip_list >= 0 & fit$pip_list <= 1), paste("B10 bounds, fixture", id))
  if (fit$status == "exact") {
    n_exact <- n_exact + 1L
    chk(identical(fit$pip_list_source, "exact") && identical(fit$pip_list, fit$pip_primary) && identical(fit$mpm_list, fit$mpm), paste("exact: pip_list = pip_primary, fixture", id))
    nmx <- names(fit); chk(max(match(setdiff(nmx, NEWF), nmx)) < min(match(NEWF[-7], nmx)) && match("peak_memory_kb", nmx) < match("pip_list", nmx), paste("exact: list fields after every legacy field, fixture", id))
    top <- fit$exact$top
    lf <- v3_list_fields(top, as.integer(names(fit$pip_primary)), names(fit$pip_primary))   # the formula of §2 on the store
    chk(identical(fit$log_Z_list, lf$log_Z_list) && fit$list_size == length(top$models) && identical(fit$list_full, isTRUE(top$full)) && is.null(fit$pip_list_flag),
        paste("exact scalars, fixture", id))
    if (!isTRUE(top$full)) {   # B9: the store holds every model, so the formula applied to it is the exact PIP
      n_all <- n_all + 1L
      chk(length(top$models) == fit$exact$models_scored, paste("B9 the store holds every model, fixture", id))
      chk(near(lf$pip_list, fit$pip_primary, 1e-10) && identical(lf$mpm_list, fit$mpm), paste("B9 formula = exact PIPs, fixture", id))
      chk(near(lf$log_Z_list, fit$log_Z, 1e-10), paste("B9 log_Z_list = log Z, fixture", id))
    } else chk(lf$log_Z_list <= fit$log_Z + 1e-12, paste("truncated store: log_Z_list <= log Z, fixture", id))
  }
}
# Theory-confirmed via HQ 11-17 (exact branch, status "exact"): pip_list = pip_primary, mpm_list = mpm, log_Z_list from fit$exact$top,
# list_size / list_full describe THAT store (not models_scored), pip_list_source = "exact" -- pinned on every exact fixture, also with a truncated store
n_trunc <- 0L
for (id in 1:6) {
  fit <- fit_ok(id)
  if (!identical(fit$status, "exact")) next
  top <- fit$exact$top
  chk(identical(fit$pip_list, fit$pip_primary) && identical(fit$mpm_list, fit$mpm) && identical(fit$pip_list_source, "exact"), paste("pinned exact reading: fields, fixture", id))
  chk(identical(fit$list_size, length(top$models)) && identical(fit$list_full, isTRUE(top$full)), paste("pinned exact reading: list_size = length(fit$exact$top$models), fixture", id))
  chk(identical(fit$log_Z_list, v3_list_fields(top, as.integer(names(fit$pip_primary)), names(fit$pip_primary))$log_Z_list), paste("pinned exact reading: log_Z_list from the store, fixture", id))
  if (isTRUE(top$full)) { n_trunc <- n_trunc + 1L; chk(fit$list_size == top$capacity && fit$list_size < fit$exact$models_scored, paste("truncated store: list_size is the store's, fixture", id)) }
}
chk(n_trunc >= 1L, "a truncated exact store is among the pinned fixtures")
chk(n_exact >= 1L && n_all >= 1L, "at least one exact-branch fixture whose store holds every model")
cat("exact-branch fixtures:", n_exact, "of 6; store holds every model in", n_all, "\n")
# an SMC fit (p = 40 with two exact copies) and A3: same seed twice, the new fields identical
smc_data <- function() {
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(104); n <- 60; p <- 40; G <- ceiling(p / 4); f <- matrix(rnorm(n * G), n)
  X <- sqrt(.6) * f[, rep(seq_len(G), each = 4)[seq_len(p)], drop = FALSE] + sqrt(.4) * matrix(rnorm(n * p), n)
  act <- unique(pmin(p, round(seq(1, p, length.out = 4)))); y <- drop(X[, act, drop = FALSE] %*% rep(c(1.2, -1, .8), length.out = length(act))) + rnorm(n)
  X[, 2] <- X[, 1]; X[, 14] <- -X[, 13]; list(X = X, y = y)
}
d <- smc_data(); alloc <- list(mem_gb = 4, hours = 2)
fa <- v3_fit(d$X, d$y, 9104L, allocation = alloc); fb <- v3_fit(d$X, d$y, 9104L, allocation = alloc)
chk(identical(fa$status, "completed") && all(NEWF[-7] %in% names(fa)) && is.null(fa$pip_list_flag), "SMC fit has the fields")
chk(identical(fa$pip_list_source, "store") && fa$list_size == length(fa$top_store$models) && identical(fa$list_full, fa$top_store$full), "SMC scalars")
chk(identical(names(fa$pip_list), names(fa$pip_primary)) && identical(fa$mpm_list, as.integer(as.integer(names(fa$pip_list))[fa$pip_list > .5])), "SMC names and mpm_list")
chk(identical(fa[NEWF], fb[NEWF]), "A3 same seed twice: identical new fields")
chk(all(fa$pip_list >= 0 & fa$pip_list <= 1) && fa$log_Z_list <= fa$log_Z + 50, "SMC bounds")
# review PR68 MAJOR-2: the fields are added strictly LAST in v3_fit, after finish() sampled peak_memory_kb and the clock, and after every
# legacy field; direct callers of v3_final_run keep getting them (default list_fields = TRUE)
nm <- names(fa); chk(max(match(setdiff(nm, NEWF), nm)) < min(match(NEWF[-7], nm)) && match("peak_memory_kb", nm) < match("pip_list", nm) &&
                     match("runtime_guard", nm) < match("pip_list", nm), "SMC fit: list fields after every legacy field")
chk(identical(formals(v3_final_run)$list_fields, TRUE) && identical(formals(v3_assemble_final)$list_fields, TRUE), "direct v3_final_run callers keep the fields by default")
# recomputation from the returned store reproduces the fit's fields, and the fields are removable without trace
rr <- v3_list_fields(fa$top_store, as.integer(names(fa$pip_primary)), names(fa$pip_primary))
chk(identical(rr$pip_list, fa$pip_list) && identical(rr$log_Z_list, fa$log_Z_list), "recomputation = the fit's fields")
# B10 on the fit: S* = first listed model, w* its renormalised weight
Fv <- fa$top_store$value; w1 <- exp(Fv[1] - max(Fv)) / sum(exp(Fv - max(Fv)))
ind <- as.numeric(as.integer(names(fa$pip_list)) %in% fa$top_store$models[[1]])
chk(max(abs(fa$pip_list - ind)) <= 1 - w1 + 1e-12, "B10 support bound on an SMC fit")
# ls0 = FALSE (v3 mode) also carries the fields
fv3 <- v3_fit(d$X, d$y, 9104L, allocation = alloc, ls0 = FALSE); chk(all(NEWF[-7] %in% names(fv3)), "ls0 = FALSE carries the fields")

# ---- B11 and the other statuses: the fields are absent -------------------------------------------------------------------------
absent <- function(fit) !any(NEWF %in% names(fit))
fr <- v3_fit(d$X, d$y, 9104L, allocation = list(mem_gb = 1e-6, hours = 2))
chk(identical(fr$status, "resource_limit") && absent(fr), "B11 resource_limit (memory preflight)")
fg <- v3_fit(d$X, d$y, 9104L, allocation = list(mem_gb = 4, hours = 1e-9))   # the runtime guard stops the calibration: partial results
chk(fg$status != "completed" && absent(fg) && isTRUE(fg$partial_results), paste("B11 calibration stopped by the guard:", fg$status))
chk(absent(v3_fit(d$X, d$y, NA, allocation = alloc)), "invalid_input")
chk(absent(v3_fit(matrix(1, 10, 3), rnorm(10), 1L, allocation = alloc)), "no_predictors")
chk(absent(v3_fit(d$X[1:20, 1:8], rep(2, 20), 1L, allocation = alloc)), "y_constant")
# ---- INV-SCORE-BITS (core v3.1): every score offered to a store for model S is the binary64 value D.logprior[|S|] + Scorer::score(S).logm of ONE
# deterministic scorer on sorted S (tables v3_start.h:93, particles v3_engine.h:92-97, inherited v3_core.cpp:426-427 re-scored not copied, the final
# local search and LS0; build with -ffp-contract=off), so a model never gets two values and the store's (value, S) dedup is exact. On the SMC fit `fa`
# above (LS0 on, frozen calibration with inherited models) and on a second final run `fb` of the same frozen calibration WITHOUT the inherited models:
# EVERY model of top_store and of both leader stores is re-scored through the public single-model path (v3_score -> cpp_score; v3_discrepancy for
# log gamma_0) and compared with identical(); no model key repeats in a store (a model with two bit-values would sit twice in the (value, S) set);
# fa and fb agree bit for bit on every model they share; every block-table entry has log_r = cpp_score(U)$log_m - log m0 with identical().
pre <- v3_preprocess(d$X, d$y, dup_components = FALSE)
ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
setup <- v3_setup(ctx)
keyf <- function(M) vapply(M, function(S) paste(sort(S), collapse = ","), "")
fz <- fa$frozen; fz$inherited <- NULL                                   # same frozen grid / N / L, no inherited store
fb <- v3_final_run(setup, fz, 9104L, NULL, ls0 = TRUE, list_fields = FALSE)
chk(identical(fb$status, "completed") && length(fa$frozen$inherited$models) > 0L && is.null(fz$inherited), "INV-SCORE-BITS: second final run without inherited models completed")
n_ident <- 0L
for (nm in c("fa", "fb")) for (sn in c("top_store", "leaders_gamma1", "leaders_gamma0")) {
  st <- get(nm)[[sn]]; kk <- keyf(st$models)
  chk(length(kk) > 0L && length(kk) == length(st$value) && !anyDuplicated(kk), paste("INV-SCORE-BITS:", nm, sn, "has", length(kk), "models, no duplicate key"))
  rec <- if (sn == "leaders_gamma0") vapply(st$models, function(S) attr(v3_discrepancy(ctx, setup$start, S), "log_gamma0"), 0)   # log varpi + sum_b log r_b
         else vapply(st$models, function(S) v3_score(ctx, S)$F, 0)                                                              # log varpi + log m
  chk(identical(unname(rec), as.numeric(st$value)), paste("INV-SCORE-BITS:", nm, sn, "values identical() to the single-model scorer"))
  n_ident <- n_ident + length(kk)
}
for (sn in c("top_store", "leaders_gamma1", "leaders_gamma0")) {
  ka <- keyf(fa[[sn]]$models); kb <- keyf(fb[[sn]]$models); both <- intersect(ka, kb)
  chk(length(both) > 0L && identical(fa[[sn]]$value[match(both, ka)], fb[[sn]]$value[match(both, kb)]), paste("INV-SCORE-BITS:", sn, "shared models:", length(both), "of", length(ka), "have identical values with and without inherited"))
}
n_tab <- 0L
for (b in seq_along(setup$blocks)) {
  mem <- setup$blocks[[b]]; tb <- setup$tables[[b]]; m <- length(mem); ok <- TRUE
  for (code in seq_len(2^m) - 1) {
    lr <- tb$log_r[code + 1]; if (is.na(lr)) next                       # |U| > K: not scored
    U <- mem[bitwAnd(code, 2^(seq_len(m) - 1)) > 0]
    if (code == 0) { ok <- ok && identical(lr, 0); next }
    r <- v3_score(ctx, U)
    ok <- ok && identical(lr, r$log_m - ctx$log_m0) && identical(lr, r$log_BF) && identical(tb$log_m[code + 1], r$log_m); n_tab <- n_tab + 1L
  }
  chk(ok, paste("INV-SCORE-BITS: table of block", b, "log_r = cpp_score(U)$log_m - log m0, identical()"))
}
# Provenance. The stores keep no origin, so it is inferred from the sets. fb (no inherited models) over the union of its three stores: table = S inside
# one block (offered by the tables); local = not a table model and one add / drop / swap (|S symdiff centre| <= 2) away from a scanned centre of the
# final local search or LS0; particle = neither (only the particle moves can have offered it). fa: inherited = key in frozen$inherited$models.
blk_of <- integer(max(pre$kept)); for (b in seq_along(setup$blocks)) blk_of[setup$blocks[[b]]] <- b
ub <- unique(unlist(lapply(c("top_store", "leaders_gamma1", "leaders_gamma0"), function(sn) fb[[sn]]$models), recursive = FALSE))
cen <- c(fb$local_search$scanned_centres, fb$ls0$scanned_centres)
is_tab <- vapply(ub, function(S) length(S) == 0L || length(unique(blk_of[S])) == 1L, NA)
is_loc <- !is_tab & vapply(ub, function(S) any(vapply(cen, function(cc) length(setdiff(S, cc)) + length(setdiff(cc, S)) <= 2L, NA)), NA)
n_inh <- sum(keyf(fa$top_store$models) %in% keyf(fa$frozen$inherited$models))
cat("INV-SCORE-BITS provenance: fb (no inherited) ", length(ub), " distinct store models: table ", sum(is_tab), ", local-search reach ", sum(is_loc), ", particle only ", sum(!is_tab & !is_loc),
    "; fa top store: ", n_inh, " of ", length(fa$top_store$models), " also in the inherited set (", length(fa$frozen$inherited$models), " inherited models)\n", sep = "")
chk(sum(is_tab) >= 1L && sum(!is_tab & !is_loc) >= 1L && sum(is_loc) >= 1L && n_inh >= 1L, "INV-SCORE-BITS: table, particle, local and inherited models are all in the stores")
cat("INV-SCORE-BITS test: ", n_ident, " store models (fit with inherited: top ", length(fa$top_store$models), ", leaders gamma1 ", length(fa$leaders_gamma1$models), ", gamma0 ", length(fa$leaders_gamma0$models),
    "; final run without inherited: ", length(fb$top_store$models), ", ", length(fb$leaders_gamma1$models), ", ", length(fb$leaders_gamma0$models), ") + ", n_tab, " table entries identical across paths\n", sep = "")

# v3.1.1 (SPEC_LIST_PIP §4): a FINAL run that did not complete (guard stop / numerical failure) carries NO list field. Forced deterministically:
# calibration runs normally; v3_final_run is wrapped to receive an already-expired runtime guard, so only the final run stops.
v3_final_run_orig <- v3_final_run
v3_final_run <- function(setup, frozen, seed, runtime = NULL, ...) v3_final_run_orig(setup, frozen, seed, runtime = .v3cpp$cpp_runtime_new(1e-9, 0), ...)
ff <- tryCatch(v3_fit(d$X, d$y, 9104L, allocation = alloc), finally = v3_final_run <- v3_final_run_orig)
chk(!identical(ff$status, "completed") && !is.null(ff$partial_final) && isTRUE(ff$partial_results), paste("stopped final run: status", ff$status))
chk(all(vapply(NEWF, function(nm) is.null(ff[[nm]]), NA)), "stopped final run: all 7 list fields are NULL (absent)")
chk(identical(v3_final_run, v3_final_run_orig) && identical(fa$status, "completed") && all(NEWF[-7] %in% names(fa)), "completed run still carries the fields")
fe <- v3_fit(d$X[, 1:10], d$y, 9101L, allocation = alloc)
chk(identical(fe$status, "exact") && all(NEWF[-7] %in% names(fe)), "exact run still carries the fields")
cat("list_pip_units: all", n_ok, "checks passed (core", V3_CORE_DIR, ")\n")
