# derive_rules.R: the derived-rule unit of PREREG_c050 R1 (thread S, 2026-10-21).
#
# For every case of one production run it computes, from the saved per-case fit files only (no
# refit, no truth), the rule rows
#   F1, F2, F3:        ebic1_K37, ebic05_K37
#   F4, F4_SCAD:       ebic1_K37, ebic05_K37, bic_K37, ebic1_lam005
#   F5:                ebic1_K37, ebic05_K37, bic_K37, sic_smax
# and the column k_gt_K (selected k > K = 37).
#
# Definitions (PREREG_c050 R1; master §III.3.0 EBIC/BIC):
#   EBIC_g(S) = n log(RSS_S / n) + |S| log n + 2 g log C(p, |S|), RSS_S from the zero-intercept OLS
#   refit on the original y. The candidate table saved by each method holds RSS_S and EBIC_g for
#   the null support and every distinct path support with |S| <= 100; the stored criterion columns
#   are used (identical arithmetic to the existing rules) and recomputed here as a check.
#   *_K37:        minimise over valid candidates with k <= K = floor(n / log n) = 37.
#   ebic1_lam005: minimise EBIC_1 over the supports at path points with lambda >= 0.05 * lambda_max,
#                 lambda on the original scale the F4 fit stores; lambda_max = zmax = max_j |X_j'y| / n
#                 (the entry value; ncvreg's internal lambda is a constant multiple, so the ratio is
#                 scale-free).
#   sic_smax:     SIC(S) = n log(RSS_S / n) + |S| log(p) log(log n) over ABESS path sizes
#                 s = 0..floor(n / (log p log log n)) (19 at p = 500, 17 at p = 1000).
#   Ties (all rules): criterion, then smaller k, then the support key in C-locale byte order
#   (order(..., method = "radix")), as in every method's ebic_pick.
#   Failure (as each method's EBIC rule): F1-F4 a non-null pick fails unless some full-data path
#   occurrence of it passes the method's own point check (F1-F3 KKT <= kkt_rel_tol; F4 `passes`);
#   for ebic1_lam005 the occurrence must lie in the restricted part of the path. F5 has no
#   occurrence check. A failed rule keeps the pick in support_audit.
#
# Usage (inside a SLURM job):
#   Rscript --vanilla derive_rules.R --results <STUDY>/results/<run_id> --out <dir> [--selfcheck]
# Writes <out>/derived_rule_rows.csv, <out>/derive_log.txt and, with --selfcheck,
# <out>/selfcheck_cap100.csv (the existing cap-100 rules re-derived from the same tables and compared
# with the method's own rows).

N_OBS <- 200L                                   # n = 200 (master §II.8)
K_CAP <- floor(N_OBS / log(N_OBS))              # 37
LAM_FRACTION <- 0.05
SIC_SMAX <- function(p) floor(N_OBS / (log(p) * log(log(N_OBS))))

DERIVED <- list(
  F1      = list(rules = c("ebic1_K37", "ebic05_K37"),                             roles = c("S0", "S0")),
  F2      = list(rules = c("ebic1_K37", "ebic05_K37"),                             roles = c("S0", "S0")),
  F3      = list(rules = c("ebic1_K37", "ebic05_K37"),                             roles = c("S0", "S0")),
  F4      = list(rules = c("ebic1_K37", "ebic05_K37", "bic_K37", "ebic1_lam005"), roles = c("primary", "S0", "S0", "S0")),
  F4_SCAD = list(rules = c("ebic1_K37", "ebic05_K37", "bic_K37", "ebic1_lam005"), roles = c("S1", "S1", "S1", "S1")),
  F5      = list(rules = c("ebic1_K37", "ebic05_K37", "bic_K37", "sic_smax"),     roles = c("primary", "S0", "S0", "S0")))
RUN_DERIVED <- list(F1_Lasso = "F1", F2_ElasticNet = "F2", F3_AdaptiveLasso = "F3",
                    F4_MCP_SCAD = c("F4", "F4_SCAD"), F5_ABESS = "F5")
GAMMA <- c(ebic1 = 1, ebic05 = 0.5, bic = 0)
FIT_LEVEL_CODES <- c("kkt_path", "path_truncated", "alpha_edge", "kappa_edge")   # copied from the fit
# Extra columns of the method's ebic1 row that describe that rule only; blanked on derived rows.
RULE_ONLY_COLS <- c("cv_mean", "cv_se", "ebic1_value", "index", "path_index")
EXTRA_COLS <- c("lambda", "rss", "crit_value", "k_valid_max", "k_path_max", "k_gt_K",
                "derived_rule", "derived_from", "derived_by_sha256", "derived_utc")

parse_cli <- function(args) {
  out <- list(); i <- 1
  while (i <= length(args)) {
    key <- sub("^--", "", args[i])
    if (i == length(args) || grepl("^--", args[i + 1])) { out[[key]] <- TRUE; i <- i + 1 }
    else { out[[key]] <- args[i + 1]; i <- i + 2 }
  }
  out
}
# tools::sha256sum exists from R 4.5.0 (NOTS); digest is the fallback for older local R.
file_sha256 <- function(path) {
  if (exists("sha256sum", envir = asNamespace("tools"))) return(unname(tools::sha256sum(path)))
  digest::digest(file = path, algo = "sha256")
}

# ---------------------------------------------------------------------------------------------
# What each method saved: candidates, path occurrences with their point check, kkt tolerance.

get_diag <- function(x) if (!is.null(x$diagnostics)) x$diagnostics else x$fit$diagnostics
get_settings <- function(x) if (length(x$settings)) x$settings else if (length(x$config)) x$config else x$fit$settings

kkt_tol_of <- function(x) {
  tol <- get_settings(x)$GLMNET$kkt_rel_tol
  if (is.null(tol)) stop("kkt_rel_tol not found in the saved settings")
  as.numeric(tol)
}

# Returns list(cand, occ, k_path_max, zmax) or NULL when the fit saved no candidate table (failed fit).
method_tables <- function(x, method_id) {
  d <- get_diag(x)
  if (is.null(d) || is.null(d$candidates)) return(NULL)
  cand <- d$candidates
  occ <- NULL
  if (method_id %in% c("F1", "F3")) {
    occ <- data.frame(key = d$path$key, ok = d$path$kkt_full <= kkt_tol_of(x), lambda = d$path$lambda,
                      stringsAsFactors = FALSE)
  } else if (method_id == "F2") {
    a <- d$chosen$alpha
    keys <- d$paths[[paste0("alpha_", a)]]
    kkt_full <- d$kkt[paste0("a", a, "_full"), ]
    lam <- d$cv_table$lambda[d$cv_table$alpha_index == d$chosen$alpha_index]
    if (is.null(keys) || length(kkt_full) != length(keys) || length(lam) != length(keys))
      stop("F2: alpha* path, KKT row or lambda grid not found or of different lengths")
    occ <- data.frame(key = keys, ok = kkt_full <= kkt_tol_of(x), lambda = lam, stringsAsFactors = FALSE)
  } else if (method_id %in% c("F4", "F4_SCAD")) {
    occ <- data.frame(key = d$path$key, ok = d$path$passes, lambda = d$path$lambda, stringsAsFactors = FALSE)
  }
  k_path <- if (!is.null(d$path$k)) max(d$path$k) else NA_integer_
  list(cand = cand, occ = occ, k_path_max = k_path, zmax = if (is.null(d$zmax)) NA_real_ else d$zmax)
}

# ---------------------------------------------------------------------------------------------
# One rule: pick the minimiser over the allowed candidates, then the method's occurrence check.

pick_rule <- function(cand, crit, allowed, occ, occ_allowed = NULL) {
  ok <- allowed & cand$valid & is.finite(crit)
  if (!any(ok)) return(list(status = "failed", key = NA_character_, audit = NA_character_, k = NA_integer_,
                            error = "no valid candidate", rss = NA_real_, crit = NA_real_, k_valid_max = NA_integer_,
                            lambda = NA_real_))
  idx <- which(ok)
  i <- idx[order(crit[idx], cand$k[idx], cand$key[idx], method = "radix")[1L]]
  key <- cand$key[i]
  lambda <- NA_real_
  passed <- TRUE
  if (!is.null(occ)) {
    pts <- occ$key == key & (if (is.null(occ_allowed)) TRUE else occ_allowed)
    good <- which(pts & occ$ok)
    passed <- key == "" || length(good) > 0                # the null support is always valid
    j <- if (length(good)) good[1L] else which(pts)[1L]     # largest lambda with that support
    if (!is.na(j)) lambda <- occ$lambda[j]
  }
  list(status = if (passed) "ok" else "failed",
       key = if (passed) key else NA_character_, audit = if (passed) NA_character_ else key,
       k = if (passed) cand$k[i] else NA_integer_,
       error = if (passed) NA_character_ else "no full-data path occurrence of the selected support passes the point check",
       rss = cand$rss[i], crit = crit[i], k_valid_max = max(cand$k[ok]), lambda = lambda)
}

# Recomputed EBIC_g from the stored RSS (check of the stored criterion columns).
ebic_from_rss <- function(cand, p, g) {
  ifelse(cand$valid, N_OBS * log(cand$rss / N_OBS) + cand$k * log(N_OBS) + 2 * g * lchoose(p, cand$k), Inf)
}

derive_case <- function(tb, method_id, p) {
  cand <- tb$cand
  out <- list()
  check <- 0
  for (rid in DERIVED[[method_id]]$rules) {
    if (grepl("_K37$", rid)) {
      g <- sub("_K37$", "", rid)
      crit <- cand[[g]]
      check <- max(check, max(abs(ebic_from_rss(cand, p, GAMMA[[g]]) - crit)[cand$valid]))
      out[[rid]] <- pick_rule(cand, crit, cand$k <= K_CAP, tb$occ)
      out[[rid]]$rule <- sprintf("EBIC(%s) over candidates with k <= %d", GAMMA[[g]], K_CAP)
    } else if (rid == "ebic1_lam005") {
      seg <- tb$occ$lambda >= LAM_FRACTION * tb$zmax
      if (!is.finite(tb$zmax) || !any(seg)) stop("lam005: zmax missing or empty segment")
      seg_keys <- unique(tb$occ$key[seg])
      missing <- setdiff(seg_keys, cand$key)
      out[[rid]] <- pick_rule(cand, cand$ebic1, cand$key %in% seg_keys, tb$occ, seg)
      out[[rid]]$rule <- sprintf("EBIC(1) over path points with lambda >= %.2f * zmax (original scale); %d segment supports outside the k <= 100 candidate table",
                                 LAM_FRACTION, length(missing))
    } else if (rid == "sic_smax") {
      smax <- SIC_SMAX(p)
      crit <- ifelse(cand$valid, N_OBS * log(cand$rss / N_OBS) + cand$k * log(p) * log(log(N_OBS)), Inf)
      out[[rid]] <- pick_rule(cand, crit, cand$k <= smax, NULL)
      out[[rid]]$rule <- sprintf("SIC = n log(RSS/n) + k log(p) log(log n) over sizes 0..%d", smax)
    }
  }
  list(rules = out, crit_check = check)
}

# Re-derives the existing cap-100 rules from the same tables (self-check of the selection logic).
selfcheck_case <- function(tb, rows, method_id, p) {
  res <- list()
  for (g in intersect(c("ebic1", "ebic05", "bic"), names(tb$cand))) {
    r <- rows[rows$rule_id == g, ]
    if (nrow(r) != 1) next
    pk <- pick_rule(tb$cand, tb$cand[[g]], tb$cand$k <= 100, if (method_id == "F5") NULL else tb$occ)
    own <- if (r$status == "failed") r$support_audit else r$support
    mine <- if (pk$status == "failed") pk$audit else pk$key
    res[[g]] <- data.frame(rule_id = g, same_status = identical(pk$status == "failed", r$status == "failed"),
                           same_support = identical(own, mine),
                           crit_absdiff = abs(pk$crit - as.numeric(r$crit_value)), stringsAsFactors = FALSE)
  }
  do.call(rbind, res)
}

# ---------------------------------------------------------------------------------------------
# Rule rows: the method's own `ebic1` row of the case supplies provenance, design, seeds, hashes,
# method and compute columns; the rule fields are replaced.

make_rows <- function(base, method_id, res, rds_sha, script_sha, utc, k_path_max = NA_integer_) {
  reg <- DERIVED[[method_id]]
  fit_codes <- if (is.na(base$diag_codes) || base$diag_codes == "") character(0) else strsplit(base$diag_codes, ";")[[1]]
  fit_codes <- paste(fit_codes[fit_codes %in% FIT_LEVEL_CODES], collapse = ";")
  fit_status <- if (!is.na(base$n_warnings) && as.numeric(base$n_warnings) > 0) "warning" else "ok"
  rows <- list()
  for (j in seq_along(reg$rules)) {
    r <- base
    v <- res[[reg$rules[j]]]
    r$rule_id <- reg$rules[j]; r$role <- reg$roles[j]
    r$status <- if (v$status == "failed") "failed" else fit_status
    r$support <- v$key; r$support_audit <- v$audit
    r$k <- if (is.na(v$k)) NA_character_ else as.character(v$k)
    r$error <- v$error
    r$diag_codes <- fit_codes
    for (cc in intersect(RULE_ONLY_COLS, names(r))) r[[cc]] <- NA_character_
    r$lambda <- v$lambda; r$rss <- v$rss; r$crit_value <- v$crit; r$k_valid_max <- v$k_valid_max
    r$k_path_max <- k_path_max
    r$k_gt_K <- if (is.na(v$k)) NA else v$k > K_CAP
    r$derived_rule <- v$rule; r$derived_from <- rds_sha; r$derived_by_sha256 <- script_sha; r$derived_utc <- utc
    rows[[j]] <- r
  }
  do.call(rbind, rows)
}

failed_rows <- function(base, method_id, rds_sha, script_sha, utc, why) {
  res <- setNames(lapply(DERIVED[[method_id]]$rules, function(rid)
    list(status = "failed", key = NA_character_, audit = NA_character_, k = NA_integer_, error = why,
         rss = NA_real_, crit = NA_real_, k_valid_max = NA_integer_, lambda = NA_real_, rule = "fit failed")),
    DERIVED[[method_id]]$rules)
  make_rows(base, method_id, res, rds_sha, script_sha, utc)
}

# ---------------------------------------------------------------------------------------------

derive_run <- function(results_dir, out_dir, selfcheck = FALSE, script_sha = NA_character_) {
  run_id <- basename(normalizePath(results_dir))
  methods <- RUN_DERIVED[[sub("^.*_prod(c[0-9]{3})?_", "", run_id)]]      # _prod_<m> (c = 1) or _prodc050_<m>
  if (is.null(methods)) stop("run ", run_id, " has no derived rules")
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  utc <- format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
  all_rows <- list(); sc <- list(); log <- character(0); max_check <- 0; n_failed_fit <- 0
  for (pdir in c("p0500", "p1000")) {
    p <- as.integer(sub("^p", "", pdir))
    cases <- list.files(file.path(results_dir, pdir))
    cases <- cases[!grepl("^dev_", cases)]                  # dev canary bundles are not production cases
    for (case_id in cases) for (m in methods) {
      cd <- file.path(results_dir, pdir, case_id)
      rds <- file.path(cd, paste0(m, ".rds")); csv <- file.path(cd, paste0(m, ".csv"))
      side <- readLines(file.path(cd, paste0(m, ".sha256")))
      side_hash <- sub(" .*$", "", side[grepl(paste0(" [ *]?", m, "\\.rds$"), side)])
      rds_sha <- file_sha256(rds)
      if (!identical(rds_sha, side_hash)) stop("RDS hash differs from its sidecar: ", rds)
      rows <- utils::read.csv(csv, colClasses = "character", na.strings = "NA")
      base <- rows[rows$rule_id == "ebic1", ]
      if (nrow(base) != 1) stop("no unique ebic1 row in ", csv)
      tb <- method_tables(readRDS(rds), m)
      if (is.null(tb)) {
        n_failed_fit <- n_failed_fit + 1
        all_rows[[length(all_rows) + 1]] <- failed_rows(base, m, rds_sha, script_sha, utc, "fit failed: no candidate table saved")
        next
      }
      d <- derive_case(tb, m, p)
      max_check <- max(max_check, d$crit_check)
      all_rows[[length(all_rows) + 1]] <- make_rows(base, m, d$rules, rds_sha, script_sha, utc, tb$k_path_max)
      if (selfcheck) sc[[length(sc) + 1]] <- cbind(case_id = case_id, method_id = m, selfcheck_case(tb, rows, m, p))
    }
  }
  out <- do.call(rbind, all_rows)
  for (cc in names(out)[vapply(out, is.double, TRUE)])
    out[[cc]] <- ifelse(is.na(out[[cc]]), NA_character_, sprintf("%.17g", out[[cc]]))   # full precision
  utils::write.csv(out, file.path(out_dir, "derived_rule_rows.csv"), row.names = FALSE, na = "NA")
  log <- c(paste("run_id:", run_id), paste("methods:", paste(methods, collapse = ",")),
           paste("rows:", nrow(out)), paste("cases per method:", paste(names(table(out$method_id)), table(out$method_id) / sapply(DERIVED[names(table(out$method_id))], function(z) length(z$rules)), sep = "=", collapse = " ")),
           paste("K =", K_CAP, "| SIC smax p500 =", SIC_SMAX(500), "p1000 =", SIC_SMAX(1000)),
           paste("fits with no candidate table (failed fits):", n_failed_fit),
           paste("max |stored EBIC - recomputed from RSS| over valid candidates:", signif(max_check, 3)),
           paste("status:", paste(names(table(paste(out$rule_id, out$status))), table(paste(out$rule_id, out$status)), sep = "=", collapse = " ")),
           paste("k_gt_K TRUE:", paste(names(table(out$rule_id[out$k_gt_K %in% "TRUE"])), table(out$rule_id[out$k_gt_K %in% "TRUE"]), sep = "=", collapse = " ")))
  if (selfcheck) {
    sc <- do.call(rbind, sc)
    utils::write.csv(sc, file.path(out_dir, "selfcheck_cap100.csv"), row.names = FALSE)
    log <- c(log, sprintf("selfcheck cap-100 (re-derived vs the method's own rows): %d rule rows; status differs %d; support differs %d; max |crit diff| %.3g",
                          nrow(sc), sum(!sc$same_status), sum(!sc$same_support), max(sc$crit_absdiff, na.rm = TRUE)))
  }
  writeLines(log, file.path(out_dir, "derive_log.txt"))
  cat(log, sep = "\n")
  invisible(out)
}

if (sys.nframe() == 0L) {
  a <- parse_cli(commandArgs(TRUE))
  fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  script_sha <- if (length(fa)) file_sha256(normalizePath(sub("^--file=", "", fa[1]))) else NA_character_
  derive_run(a$results, a$out, selfcheck = isTRUE(a$selfcheck), script_sha = script_sha)
}
