# Tiny-p check, part 1 (CRITERIA.md): generate the 10 fixed datasets and run the 40 public v3_fit calls.
# Usage: Rscript --vanilla gen_and_fit.R CORE_DIR OUT_DIR
# Writes OUT_DIR/data/<id>.{X,y}.bin (float64 little-endian, X column-major) + <id>.json, and
# OUT_DIR/fits/<id>_m<k>.json (the fields the comparison needs) + .rds (the whole native fit).
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
core <- normalizePath(args[[1]], mustWork = TRUE)
out <- args[[2]]
stopifnot(!dir.exists(out))
dir.create(file.path(out, "data"), recursive = TRUE); dir.create(file.path(out, "fits"))
source(file.path(core, "v3.R"))

designs <- list(
  D1 = list(n = 30, p = 20, rho = 0, beta = c(`1` = 1.5, `2` = -1.0, `3` = 0.8)),
  D2 = list(n = 30, p = 20, rho = 0.6, beta = c(`1` = 1.0, `7` = 0.7, `13` = 0.5)),
  D3 = list(n = 30, p = 18, rho = 0, beta = c(`1` = 0.6)),
  D4 = list(n = 16, p = 20, rho = 0, beta = setNames(c(2.0, -1.8, 1.6, -1.4, 1.2, -1.0, 0.8), 1:7)),
  D5 = list(n = 30, p = 20, rho = 0, beta = numeric(0)))

# X: rows iid N(0, Sigma); Sigma is block diagonal with blocks of 5 and within-block correlation rho.
draw_X <- function(n, p, rho) {
  Z <- matrix(stats::rnorm(n * p), n, p)
  if (rho == 0) return(Z)
  Sigma <- diag(p)
  for (b in split(seq_len(p), ceiling(seq_len(p) / 5))) Sigma[b, b] <- rho
  diag(Sigma) <- 1
  Z %*% chol(Sigma)
}
write_f64 <- function(x, path) writeBin(as.double(as.vector(x)), path, endian = "little")

# All 10 datasets first (each from its own seed), so the exact enumeration can start at once.
data <- list()
for (D in seq_along(designs)) for (rep in 1:2) {
  g <- designs[[D]]; id <- sprintf("D%d_rep%d", D, rep)
  data_seed <- 2026102300L + 10L * D + rep
  set.seed(data_seed)
  X <- draw_X(g$n, g$p, g$rho)
  mu <- if (length(g$beta)) X[, as.integer(names(g$beta)), drop = FALSE] %*% g$beta else rep(0, g$n)
  y <- as.vector(mu + stats::rnorm(g$n))
  write_f64(X, file.path(out, "data", paste0(id, ".X.bin"))); write_f64(y, file.path(out, "data", paste0(id, ".y.bin")))
  b <- v3_budgets(g$n, g$p)
  stopifnot(!b$exact_branch)
  jsonlite::write_json(list(id = id, design = names(designs)[D], rep = rep, n = g$n, p = g$p, rho = g$rho,
    beta = as.list(g$beta), data_seed = data_seed, K = b$K, exact_count = b$exact_count,
    exact_threshold = b$exact_threshold, exact_branch = b$exact_branch),
    file.path(out, "data", paste0(id, ".json")), auto_unbox = TRUE, digits = NA)
  data[[id]] <- list(D = D, rep = rep, X = X, y = y)
}
for (id in names(data)) {
  D <- data[[id]]$D; rep <- data[[id]]$rep; X <- data[[id]]$X; y <- data[[id]]$y
  for (m in 1:4) {
    seed <- 7000000L + 1000L * D + 100L * rep + m
    t0 <- proc.time()[["elapsed"]]
    fit <- v3_fit(X, y, seed, allocation = list(mem_gb = 2, hours = 1))
    wall <- proc.time()[["elapsed"]] - t0
    saveRDS(fit, file.path(out, "fits", sprintf("%s_m%d.rds", id, m)), compress = "xz")
    if (!identical(fit$status, "completed")) {   # compare.py fails such a fit outright
      jsonlite::write_json(list(id = id, m = m, seed = seed, status = fit$status, branch_run = fit$branch_run %||% NA,
        wall_s = wall), file.path(out, "fits", sprintf("%s_m%d.json", id, m)), auto_unbox = TRUE)
      cat(sprintf("%s m%d seed %d status %s\n", id, m, seed, fit$status)); next
    }
    jsonlite::write_json(list(id = id, m = m, seed = seed, status = fit$status, branch_run = fit$branch_run,
      log_Z = fit$log_Z, log_Z_rel_m0 = fit$log_Z_rel_m0, log_Z_r = fit$log_Z_r,
      log_Z_r_rel_m0 = fit$log_Z_r_rel_m0, log_m0 = fit$log_m0,
      pip_primary = as.list(fit$pip_primary), pip_r = unname(split(fit$pip_r, row(fit$pip_r))),
      pip_r_rows = rownames(fit$pip_r), hpm = I(as.integer(fit$hpm)), hpm_F = fit$hpm_F,
      pool_is_rowmeans = identical(unname(fit$pip_primary), unname(rowMeans(fit$pip_r))),
      flags = fit$flags[c("E1", "E2", "E3", "low_empirical_ESS", "local_limit", "checks_passed_final", "escalated")],
      N = fit$budgets$N0, wall_s = wall),
      file.path(out, "fits", sprintf("%s_m%d.json", id, m)), auto_unbox = TRUE, digits = NA)
    cat(sprintf("%s m%d seed %d status %s branch %s logZ_bf %.6f wall %.1fs\n", id, m, seed, fit$status,
      fit$branch_run, fit$log_Z_rel_m0, wall))
  }
}
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
cat("GEN_AND_FIT_DONE\n")
