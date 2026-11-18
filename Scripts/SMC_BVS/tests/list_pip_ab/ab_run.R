# ab_run.R -- list-PIP acceptance A1/A2 (SPEC_LIST_PIP §7): the SAME fit by the OLD core and by the NEW core, compared. One unit, one core.
#   Rscript --vanilla ab_run.R <old|new> <core_dir> <unit> <out_dir> [old_dir]
# Units: prodh:p0500_S1_r001_c050 ... (PROD-H, regenerated with the frozen generator in Scripts/Data_generators, dir in $AB_GEN_DIR; the NOTS input
# manifest is not on Owls, so manifest_match is not checked: old and new see the same regenerated data), supp:<name> (W3-SCALE supplementary units,
# ws_common.R) and stat:<name> (the status paths of the spec §4: resource_limit, guard_calib, invalid_seed, smc_ls0off, smc_default).
# $AB_RERUN_FILE (optional): units listed there run with hours = 48 (Owls times the LS0 worst case slower than NOTS, which trips the time-based
# preflight of the PROD-H allocation; old and new must use the same allocation, so both sides read the same file).
# mode old: run the fit with the OLD core (the core before the list-PIP change) and save it (xz).
# mode new: run the fit with the NEW core, remove the new fields and compare with the saved old fit:
#   * identical() of the whole fits after the spec's timing/memory exclusions (ws_strip), and the same whole-fit SHA-256 fingerprint;
#   * the old fit's FIELD ORDER and ATTRIBUTES: identical names(), identical top-level attributes, identical attributes of every element;
#   * the new fields are the LAST elements of the new fit (computed after every legacy field);
#   * the new fields are saved for the report.
args <- commandArgs(TRUE); mode <- args[1]; core_dir <- args[2]; unit <- args[3]; out_dir <- args[4]; old_dir <- args[5]
a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
WS_DIR <- dirname(normalizePath(sub("^--file=", "", a[1])))
source(file.path(WS_DIR, "ws_common.R"))
GEN_DIR <- Sys.getenv("AB_GEN_DIR")
NEWF <- c("pip_list", "mpm_list", "log_Z_list", "list_size", "list_full", "pip_list_source", "pip_list_flag")
RERUN <- if (nzchar(Sys.getenv("AB_RERUN_FILE"))) readLines(Sys.getenv("AB_RERUN_FILE")) else character()
source(file.path(core_dir, "v3.R"))
cat("core", core_dir, "key", V3_CPP_KEY, "\n")
id <- sub("^[a-z]+:", "", unit)
if (grepl("^prodh:", unit)) {
  m <- regmatches(id, regexec("^p(\\d+)_S(\\d)_r(\\d+)_(c\\d+)$", id))[[1]]; stopifnot(length(m) == 5)
  d <- ws_prodh(as.integer(m[2]), as.integer(m[3]), as.integer(m[4]), m[5], GEN_DIR, NULL)
  d$seed <- d$method_seed
  d$allocation <- list(mem_gb = as.double(2), hours = as.double(if (as.integer(m[2]) == 500L) "1.75" else "6.666666667"))
} else if (grepl("^stat:", unit)) {
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(104); n <- 60; p <- 40; G <- ceiling(p / 4); f <- matrix(rnorm(n * G), n)
  X <- sqrt(.6) * f[, rep(seq_len(G), each = 4)[seq_len(p)], drop = FALSE] + sqrt(.4) * matrix(rnorm(n * p), n)
  act <- unique(pmin(p, round(seq(1, p, length.out = 4)))); y <- drop(X[, act, drop = FALSE] %*% rep(c(1.2, -1, .8), length.out = length(act))) + rnorm(n)
  X[, 2] <- X[, 1]; X[, 14] <- -X[, 13]
  d <- list(X = X, y = y, seed = 9104L, allocation = list(mem_gb = 4, hours = 2), ls0 = TRUE)
  if (id == "resource_limit") d$allocation <- list(mem_gb = 1e-6, hours = 2)
  if (id == "guard_calib") d$allocation <- list(mem_gb = 4, hours = 1e-9)
  if (id == "invalid_seed") d$seed <- NA
  if (id == "smc_ls0off") d$ls0 <- FALSE
} else d <- ws_supp(id)
if (is.null(d$ls0)) d$ls0 <- TRUE
if (unit %in% RERUN) d$allocation$hours <- 48   # any unit kind (v3.1.1: also supp:tie_dp_p400)
t0 <- proc.time()[["elapsed"]]
fit <- tryCatch(v3_fit(d$X, d$y, d$seed, allocation = d$allocation, ls0 = d$ls0), error = function(e) list(status = "R_error", message = conditionMessage(e)))
wall <- proc.time()[["elapsed"]] - t0
stem <- file.path(out_dir, gsub("[^A-Za-z0-9_]", "_", id))
if (mode == "old") {
  saveRDS(fit, paste0(stem, ".old.rds"), compress = "xz")
  cat(sprintf("[%s] %s old status=%s wall=%.1fs fp=%s\n", ws_utc(), id, fit$status, wall, substr(ws_fingerprint(fit)$all, 1, 16)))
} else {
  old <- readRDS(file.path(old_dir, paste0(gsub("[^A-Za-z0-9_]", "_", id), ".old.rds")))
  present <- intersect(NEWF, names(fit))
  stripped <- fit[setdiff(names(fit), NEWF)]
  so <- ws_strip(old); sn <- ws_strip(stripped)
  same_all <- identical(so, sn)
  fp_o <- ws_fingerprint(old)$all; fp_n <- ws_fingerprint(stripped)$all
  diff_fields <- setdiff(union(names(so), names(sn)), names(so)[vapply(names(so), function(k) k %in% names(sn) && identical(so[[k]], sn[[k]]), NA)])
  names_same <- identical(names(old), names(stripped))
  attrs_same <- identical(attributes(old), attributes(stripped))
  elem_attrs_same <- identical(lapply(old, attributes), lapply(stripped, attributes))
  new_last <- length(present) == 0L || identical(tail(names(fit), length(present)), present)
  rec <- list(unit = unit, status_old = old$status, status_new = fit$status, new_fields_present = present, identical_stripped = same_all,
              fingerprint_equal = identical(fp_o, fp_n), fp_old = fp_o, fp_new = fp_n, differing = diff_fields, wall = wall,
              names_order_same = names_same, attributes_same = attrs_same, element_attributes_same = elem_attrs_same, new_fields_last = new_last,
              new = fit[present])
  saveRDS(rec, paste0(stem, ".new.rds"))
  cat(sprintf("[%s] %s new status=%s identical=%s fp_equal=%s names_order=%s attrs=%s elem_attrs=%s new_last=%s new_fields=%s wall=%.1fs\n", ws_utc(), id, fit$status, same_all,
              identical(fp_o, fp_n), names_same, attrs_same, elem_attrs_same, new_last, paste(present, collapse = ","), wall))
}
