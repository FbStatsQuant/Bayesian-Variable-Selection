# lowp_enum.R -- exact enumeration of all 2^p models (p <= 62; production use p <= 30) with the SMC core's scorer
# arithmetic, model scoring, and the T37 truth-dominance audit.  Contract: ../INTERFACES.md §I2, ../LOWP_SPEC.md §L.7.
#
#   source("<this dir>/lowp_enum.R")
#   ex <- lowp_exact(X, list(c100 = y1, c050 = y2), top = 1000, threads = 8)
#
# The core (CORE = code/core/v2_2/core) is used for v3_preprocess.R only (sourced, not compiled); the scorer headers are
# vendored in vendor/ and their SHA-256 must equal CORE's (checked at load).  Compile cache: env LOWP_ENUM_CACHE, else a
# folder under tempdir(); never inside the study tree.

local({
  this_file <- NA_character_
  for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { this_file <- normalizePath(fr$ofile, winslash = "/"); break }
  dir <- if (!is.na(this_file)) dirname(this_file) else Sys.getenv("LOWP_ENUM_DIR", unset = NA)
  if (is.na(dir) || !file.exists(file.path(dir, "lowp_enum.cpp")))
    stop("lowp_enum.R: cannot locate its own directory; set LOWP_ENUM_DIR to the enum/ folder before source().")
  assign("LOWP_ENUM_DIR", dir, envir = globalenv())
})

.lowp <- new.env(parent = emptyenv())

lowp_sha256 <- function(path) digest::digest(file = path, algo = "sha256", serialize = FALSE)

lowp_core_dir <- function(core_dir = NULL) {
  cd <- core_dir
  if (is.null(cd)) cd <- Sys.getenv("LOWP_CORE_DIR", unset = NA)
  if (is.null(cd) || is.na(cd)) cd <- file.path(LOWP_ENUM_DIR, "..", "..", "core", "v2_2", "core")
  cd <- normalizePath(cd, winslash = "/", mustWork = FALSE)
  if (!file.exists(file.path(cd, "v3_preprocess.R")) || !file.exists(file.path(cd, "cpp", "v3_score.h")))
    stop("lowp_enum: SMC core not found at '", cd, "'. Pass core_dir= or set LOWP_CORE_DIR to the core/ folder ",
         "(the one containing v3_preprocess.R and cpp/v3_score.h).")
  cd
}

# Vendored headers must be the core's headers (hash equality), and must match VENDOR_SHA256.txt.
lowp_check_vendor <- function(core_dir) {
  vd <- file.path(LOWP_ENUM_DIR, "vendor")
  rec <- readLines(file.path(vd, "VENDOR_SHA256.txt"))
  h <- setNames(sub("^([0-9a-f]{64}).*$", "\\1", rec), sub("^[0-9a-f]{64} [* ]?", "", rec))
  for (f in names(h)) {
    mine <- lowp_sha256(file.path(vd, f))
    if (mine != h[[f]]) stop("lowp_enum: vendored ", f, " does not match VENDOR_SHA256.txt (modified).")
    theirs <- lowp_sha256(file.path(core_dir, "cpp", f))
    if (mine != theirs)
      stop("lowp_enum: vendored ", f, " differs from the core's cpp/", f, " (core sha256 ", theirs, ", vendored ", mine,
           "). The exact reference must use the SMC core's scorer; re-vendor and re-validate before use.")
  }
  h
}

lowp_compile <- function(cache_dir = Sys.getenv("LOWP_ENUM_CACHE", unset = file.path(tempdir(), "lowp_enum_cache")),
                         quiet = TRUE, wait_seconds = 1800) {
  src <- c(file.path(LOWP_ENUM_DIR, "lowp_enum.cpp"), file.path(LOWP_ENUM_DIR, "Makevars.lowp"),
           sort(list.files(file.path(LOWP_ENUM_DIR, "vendor"), pattern = "\\.h$", full.names = TRUE)))
  key <- digest::digest(paste(c(vapply(src, lowp_sha256, ""), R.version.string, Sys.info()[["sysname"]]), collapse = ""),
                        algo = "sha256", serialize = FALSE)
  shared <- file.path(cache_dir, substr(key, 1, 16))
  ready <- file.path(shared, "READY")
  old <- Sys.getenv(c("PKG_CPPFLAGS", "R_MAKEVARS_USER"), unset = NA)
  Sys.setenv(PKG_CPPFLAGS = paste0("-I", file.path(LOWP_ENUM_DIR, "vendor")),
             R_MAKEVARS_USER = file.path(LOWP_ENUM_DIR, "Makevars.lowp"))
  on.exit(for (k in names(old)) if (is.na(old[[k]])) Sys.unsetenv(k) else do.call(Sys.setenv, setNames(list(old[[k]]), k)), add = TRUE)
  if (!file.exists(ready)) {
    dir.create(cache_dir, recursive = TRUE, showWarnings = FALSE)
    lock <- paste0(shared, ".lock"); t0 <- Sys.time()
    repeat {
      if (file.exists(ready)) break
      if (dir.create(lock, showWarnings = FALSE)) {
        ok <- FALSE
        tryCatch({
          if (!file.exists(ready)) {
            unlink(shared, recursive = TRUE); dir.create(shared, recursive = TRUE, showWarnings = FALSE)
            Rcpp::sourceCpp(file.path(LOWP_ENUM_DIR, "lowp_enum.cpp"), env = new.env(), cacheDir = shared,
                            showOutput = !quiet, verbose = FALSE)
            writeLines(key, file.path(shared, "READY.tmp")); file.rename(file.path(shared, "READY.tmp"), ready)
          }
          ok <- TRUE
        }, finally = unlink(lock, recursive = TRUE))
        if (ok) break
      }
      info <- file.info(lock)
      if (!is.na(info$mtime) && difftime(Sys.time(), info$mtime, units = "secs") > 3600) unlink(lock, recursive = TRUE)
      if (difftime(Sys.time(), t0, units = "secs") > wait_seconds) stop("lowp_compile: timed out waiting for the build lock ", lock)
      Sys.sleep(2)
    }
  }
  priv <- file.path(tempdir(), paste0("lowpcpp_", substr(key, 1, 16)))
  if (!file.exists(file.path(priv, "READY"))) {
    unlink(priv, recursive = TRUE); dir.create(priv, recursive = TRUE)
    ok <- file.copy(list.files(shared, full.names = TRUE, all.files = TRUE, no.. = TRUE), priv, recursive = TRUE, copy.date = TRUE)
    if (!all(ok)) stop("lowp_compile: could not copy the compiled cache to ", priv)
  }
  env <- new.env(parent = globalenv())
  Rcpp::sourceCpp(file.path(LOWP_ENUM_DIR, "lowp_enum.cpp"), env = env, cacheDir = priv, showOutput = !quiet, verbose = FALSE)
  .lowp$cpp <- env
  .lowp$key <- key
  invisible(key)
}

# Load once per process: check vendor hashes against the core, source v3_preprocess.R, compile.
lowp_load <- function(core_dir = NULL) {
  cd <- lowp_core_dir(core_dir)
  if (!is.null(.lowp$cpp) && identical(.lowp$core_dir, cd)) return(invisible(.lowp$key))
  vh <- lowp_check_vendor(cd)
  source(file.path(cd, "v3_preprocess.R"), local = FALSE)
  .lowp$core_dir <- cd
  .lowp$vendor <- vh
  .lowp$preprocess_sha256 <- lowp_sha256(file.path(cd, "v3_preprocess.R"))
  lowp_compile()
}

# Preprocess exactly as v3_fit: v3_preprocess on (X, y) for each response; X must come out identical.
lowp_prepare <- function(X, Ylist, core_dir = NULL) {
  lowp_load(core_dir)
  if (!is.list(Ylist)) Ylist <- list(y = Ylist)
  if (is.null(names(Ylist))) names(Ylist) <- paste0("y", seq_along(Ylist))
  pres <- lapply(Ylist, function(y) v3_preprocess(X, unname(as.numeric(y)), dup_components = FALSE))
  for (nm in names(pres)) if (!identical(pres[[nm]]$status, "ok")) stop("lowp: preprocessing status '", pres[[nm]]$status, "' for scale ", nm)
  X1 <- pres[[1]]$X
  for (nm in names(pres)) if (!identical(pres[[nm]]$X, X1) || !identical(pres[[nm]]$kept, pres[[1]]$kept)) stop("lowp: preprocessed X differs between scales")
  list(X = X1, Y = do.call(cbind, lapply(pres, `[[`, "y")), orig = as.integer(pres[[1]]$kept), pre = pres)
}

# ------------------------------------------------------------------------------------------------------------------
# Argument validation helpers
# ------------------------------------------------------------------------------------------------------------------
.lowp_int <- function(x, name, lo = -Inf, hi = Inf) {
  if (!is.numeric(x) || length(x) != 1L || !is.finite(x) || x != round(x) || x < lo || x > hi)
    stop(name, " must be a single finite integer-valued number in [", lo, ", ", hi, "]")
  as.integer(x)
}
.lowp_idx <- function(x, name, allowed = NULL, unique = TRUE) {
  if (!is.numeric(x) || anyNA(x) || any(!is.finite(x)) || any(x != round(x))) stop(name, " must be finite integer-valued indices")
  x <- as.integer(x)
  if (unique && anyDuplicated(x)) stop(name, " contains duplicated indices")
  if (!is.null(allowed) && !all(x %in% allowed)) stop(name, " contains indices that are not retained columns")
  x
}

# ------------------------------------------------------------------------------------------------------------------
# lowp_exact(X, Ylist, top, threads): list of <S> (INTERFACES §I2) per element of Ylist, plus a run record in attr "run".
# Supported domain: campaign p <= 30; allowed up to p <= 40 (counts and masks exact), original column indices <= 53
# (the double `mask` column), n = 200.  A run that does not score every feasible model (task_subset / prefix_fraction test
# hooks) has status "partial": its log_Z, PIPs, size masses, HPM and certificate quantities are restricted to the scored
# models (scope = "restricted_to_scored_models") and global_certified is FALSE.
# Test/timing hooks (not production): task_bits, task_subset / prefix_fraction, recheck_stride, qthr, fail_vars (0-based
# internal variables whose append is forced to fail), collect_F (allocates 2^p doubles per scale; p <= 26).
# ------------------------------------------------------------------------------------------------------------------
lowp_exact <- function(X, Ylist, top = 1000, threads = 1, core_dir = NULL, task_bits = NULL, task_subset = NULL,
                       prefix_fraction = NULL, subset_seed = 1L, recheck_stride = 1009L, qthr = 1e-8,
                       fail_vars = integer(0), collect_F = FALSE, return_raw = FALSE) {
  top <- .lowp_int(top, "top", 2, 1e5); threads <- .lowp_int(threads, "threads", 1, 1024)
  recheck_stride <- .lowp_int(recheck_stride, "recheck_stride", 0, 1e9)
  if (!is.numeric(qthr) || length(qthr) != 1L || !is.finite(qthr) || qthr < 0) stop("qthr must be a finite non-negative number")
  if (!is.null(task_bits)) task_bits <- .lowp_int(task_bits, "task_bits", 0, 20)
  if (!is.null(prefix_fraction) && (!is.numeric(prefix_fraction) || length(prefix_fraction) != 1L || !is.finite(prefix_fraction) || prefix_fraction <= 0 || prefix_fraction > 1))
    stop("prefix_fraction must be in (0, 1]")
  pr <- lowp_prepare(X, Ylist, core_dir)
  p <- ncol(pr$X)
  if (p > 40) stop("lowp_exact: p = ", p, " > 40 (supported domain: campaign p <= 30, tests up to 40)")
  if (max(pr$orig) > 53) stop("lowp_exact: an original column index exceeds 53, so the double 'mask' column would not be exact")
  tb <- if (is.null(task_bits)) min(p, 10L) else min(p, task_bits)
  if (!is.null(task_subset)) task_subset <- .lowp_idx(task_subset, "task_subset", allowed = 0:(2^tb - 1), unique = FALSE)
  if (is.null(task_subset) && !is.null(prefix_fraction)) {
    nt <- 2^tb; ns <- max(1, ceiling(prefix_fraction * nt))
    old <- if (exists(".Random.seed", globalenv())) get(".Random.seed", globalenv()) else NULL
    set.seed(subset_seed); task_subset <- sort(sample.int(nt, ns) - 1L)
    if (!is.null(old)) assign(".Random.seed", old, globalenv())
  }
  t0 <- Sys.time()
  r <- .lowp$cpp$cpp_enum(pr$X, pr$Y, pr$orig, top, threads, as.integer(tb),
                          as.integer(if (is.null(task_subset)) integer(0) else task_subset), recheck_stride,
                          as.numeric(qthr), as.integer(fail_vars), isTRUE(collect_F))
  t1 <- Sys.time()
  if (identical(r$status, "partial")) warning("lowp_exact: only ", r$models_scored, " of ", r$models_expected, " feasible models were scored; ",
                                              "results are restricted to the scored models (status 'partial', global_certified = FALSE)")
  bound_kind <- "heuristic (not a validated interval bound)"
  sc <- lapply(seq_along(r$scales), function(s) {
    z <- r$scales[[s]]
    pip <- z$pip; names(pip) <- as.character(pr$orig)
    list(status = r$status, scope = z$scope,
         log_Z = z$log_Z, log_m0 = z$log_m0, log_Z_rel_m0 = z$log_Z - z$log_m0, pip = pip,
         hpm = z$hpm, hpm_F = z$hpm_F, hpm_size = z$hpm_size, hpm_eta = z$hpm_eta, hpm_eta_kind = bound_kind,
         second_F = z$second_F, margin = z$margin,
         certificate_bound = z$certificate_bound, certificate_bound_kind = bound_kind, global_certified = z$global_certified,
         certified_over_scored_models = z$certified_over_scored_models,
         mpm = as.integer(pr$orig[z$pip > 0.5]), size_logmass = z$size_logmass, size_logjoint = z$size_logjoint,
         top = data.frame(rank = seq_along(z$top_F), F = z$top_F, size = z$top_size, model = z$top_model, mask = z$top_mask,
                          stringsAsFactors = FALSE),
         numerics = z$numerics)
  })
  names(sc) <- colnames(pr$Y)
  run <- list(models_scored = r$models_scored, models_expected = r$models_expected, complete = r$complete, threads = r$threads,
              K = r$K, p = r$p, n = r$n, status = r$status, message = r$message,
              task_bits = r$task_bits, n_tasks = r$n_tasks, tasks_run = r$tasks_run, wall_s = r$wall_s,
              wall_r_s = as.numeric(difftime(t1, t0, units = "secs")), tasks = r$tasks, task_seconds = r$task_seconds,
              task_models = r$task_models, orig = pr$orig)
  if (isTRUE(collect_F)) run$F_all <- setNames(r$F_all, colnames(pr$Y))
  if (isTRUE(return_raw)) run$prep <- pr
  attr(sc, "run") <- run
  sc
}

# F, log m, eta, size, route for arbitrary models (list of integer vectors of original indices), by v3::Scorer::score.
lowp_score_models <- function(X, y, models, core_dir = NULL, threads = 1) {
  pr <- lowp_prepare(X, list(y = y), core_dir)
  r <- .lowp$cpp$cpp_score_models(pr$X, pr$Y[, 1], pr$orig, lapply(models, as.integer), as.integer(threads))
  data.frame(model = vapply(models, function(m) paste(sort(m), collapse = ";"), ""), size = r$size, F = r$F, log_m = r$log_m,
             eta = r$eta, route = r$route, q_recomputed = r$q_recomputed, stringsAsFactors = FALSE)
}

# Exact score count of the TD audit: centres U u P (U subset of S0, P subset of the pool, |P| <= d) of size <= K; each
# centre costs 1 + k + k(p-k) + [k<K](p-k) calls of the scorer (itself, deletions, swaps, additions; swaps are feasible at |S| = K,
# only additions are not; no de-duplication).  Counts are doubles: exact below 2^53 (attribute/field count_exact tells).
lowp_td_count <- function(p, K, s0, npool, d) {
  p <- .lowp_int(p, "p", 1, 1e6); K <- .lowp_int(K, "K", 1, p); s0 <- .lowp_int(s0, "s0", 0, p)
  npool <- .lowp_int(npool, "npool", 0, p); d <- .lowp_int(d, "d", 0, 1000)
  nc <- 0; tot <- 0
  for (u in 0:s0) for (i in 0:min(d, npool)) {
    k <- u + i; if (k > K) next
    cnt <- choose(s0, u) * choose(npool, i)
    nc <- nc + cnt
    tot <- tot + cnt * (1 + k + k * (p - k) + if (k < K) (p - k) else 0)
  }
  structure(c(centres = nc, scores = tot), count_exact = is.finite(tot) && tot < 2^53)
}

# T37 truth-dominance audit (definition in the task brief / scoring/THEORY_MEASURES.md).  Inputs are validated before any
# counting or enumeration: d a single integer in 0..1000, margin finite and >= 0, truth and null_pool unique integer indices of
# retained columns (disjoint, truth non-empty with |truth| <= min(K, 40)), threads in 1..1024, max_scores a number >= 0
# (Inf allowed).  A run is refused when the exact score count is not exactly representable (>= 2^53).
lowp_td <- function(X, y, truth, d, null_pool = NULL, margin = 0, max_scores = Inf, threads = 1, core_dir = NULL, keep_all = FALSE) {
  d <- .lowp_int(d, "d", 0, 1000); threads <- .lowp_int(threads, "threads", 1, 1024)
  if (!is.numeric(margin) || length(margin) != 1L || !is.finite(margin) || margin < 0) stop("margin must be a single finite number >= 0 (T37 defines TD(d, m) for m >= 0)")
  if (!is.numeric(max_scores) || length(max_scores) != 1L || is.na(max_scores) || max_scores < 0) stop("max_scores must be a number >= 0 (Inf allowed)")
  if (!is.logical(keep_all) || length(keep_all) != 1L || is.na(keep_all)) stop("keep_all must be TRUE or FALSE")
  pr <- lowp_prepare(X, list(y = y), core_dir)
  p <- ncol(pr$X); K <- min(p, nrow(pr$X) %/% 2L)
  truth <- sort(.lowp_idx(truth, "truth", allowed = pr$orig))
  if (!length(truth) || length(truth) > min(K, 40L)) stop("truth must have between 1 and min(K, 40) = ", min(K, 40L), " indices")
  pool <- if (is.null(null_pool)) setdiff(pr$orig, truth) else sort(.lowp_idx(null_pool, "null_pool", allowed = pr$orig))
  if (length(intersect(pool, truth))) stop("null_pool must lie outside the truth")
  cnt <- lowp_td_count(p, K, length(truth), length(pool), d)
  if (cnt[["scores"]] > max_scores)
    return(list(dry_run = TRUE, scores_needed = cnt[["scores"]], count_exact = attr(cnt, "count_exact"), n_centres = cnt[["centres"]],
                p = p, K = K, s0 = length(truth), n_pool = length(pool), d = d, max_scores = max_scores))
  if (!isTRUE(attr(cnt, "count_exact"))) stop("the score count (", format(cnt[["scores"]]), ") is not exactly representable; refusing to run")
  t0 <- Sys.time()
  r <- .lowp$cpp$cpp_td(pr$X, pr$Y[, 1], pr$orig, truth, as.integer(pool), d, as.numeric(margin), threads, keep_all)
  r$dry_run <- FALSE
  r$scores_needed <- cnt[["scores"]]; r$count_exact <- TRUE; r$n_centres_expected <- cnt[["centres"]]
  if (r$scores_used != r$scores_needed || r$n_centres != r$n_centres_expected) stop("internal error: score/centre count differs from the closed form")
  r$margin <- margin; r$d <- d
  r$td_holds <- all(vapply(r$clauses, function(z) z$n_violating == 0, TRUE))
  r$td_holds_strict <- all(vapply(r$clauses, function(z) z$n_violating_strict == 0, TRUE))
  r$toward$td_holds <- all(vapply(r$toward$clauses, function(z) z$n_violating == 0, TRUE))
  r$toward$td_holds_strict <- all(vapply(r$toward$clauses, function(z) z$n_violating_strict == 0, TRUE))
  r$toward$definition <- "toward: margin = best gain among moves that strictly reduce |S delta S0| minus best gain among moves that do not; at S0 as literal"
  r$literal_label <- "literal = T37 wording (top-level fields); toward = r$toward"
  r$region <- if (is.null(null_pool)) "full pool" else "restricted pool (result concerns the restricted centre region only)"
  r$diagnosis <- lowp_td_diagnosis(r)
  r$seconds <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
  r
}

# Diagnosis of literal-T37 violations: which move type beats the best "target" move (clause a: truth addition; clause b:
# null deletion) at each violating centre (margin < r$margin). Returns a count table by clause and move label.
lowp_td_diagnosis <- function(r) {
  v <- r$violators; v <- v[v$margin < r$margin & v$clause != "c", , drop = FALSE]
  if (!nrow(v)) return(table(clause = character(0), best_other_move = character(0)))
  table(clause = v$clause, best_other_move = v$o_label)
}
