# NF: production SMC-BVS v3.1 (LS0 on) on exact-Gram compound-symmetry designs, p > n/2.
.libPaths(c("C:/Users/felip/AppData/Local/R/win-library/4.6", .libPaths()))  # explicit user library (env R_LIBS_USER is unreliable in this shell)
args <- commandArgs(trailingOnly = TRUE)
CORE <- Sys.getenv("NF_CORE", "C:/Users/felip/AppData/Local/Temp/claude/b6670484aa90e31a/90c131d3-63bb-4e30-8d67-5125902c46d3/scratchpad/core_copy")
OUT  <- "C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave2/W2-FAC-PK/numerics/full_method"
source(file.path(CORE, "v3.R"))
suppressMessages(library(jsonlite))
S0 <- c(3L, 27L, 54L, 76L); beta0 <- c(1.4, 1.0, 1.8, 1.2); rho <- 0.5

make_data <- function(n, p, rep) {
  Sigma <- (1 - rho) * diag(p) + rho * matrix(1, p, p)
  set.seed(1000 + rep)
  Z <- matrix(rnorm(n * p), n, p); Z <- sweep(Z, 2, colMeans(Z))
  Q <- qr.Q(qr(Z))                       # thin QR, n x p
  X <- sqrt(n - 1) * Q %*% chol(Sigma)
  gram_err <- max(abs(crossprod(X) / (n - 1) - Sigma))
  mean_err <- max(abs(colMeans(X)))
  set.seed(2000 + rep)
  beta <- numeric(p); beta[S0] <- beta0
  y <- as.vector(X %*% beta + rnorm(n))
  list(X = X, y = y, gram_err = gram_err, mean_err = mean_err)
}

# usage: Rscript nf_run.R <n> <p> <rep> [hours]   (one fit per process; wrapper nf_driver.sh applies a wall-clock timeout)
# allocation hours (4th arg; default 2 = the ticket value). With hours=2 (and 24) the production preflight
# (v3.1 LS0 worst-case charge) returns resource_limit at n=600,p=450 -- see NF_summary.md; hours=1000 lifts the guard only.
HOURS <- if (length(args) >= 4) as.numeric(args[4]) else 2
grid <- list(list(as.integer(args[1]), as.integer(args[2]), as.integer(args[3])))
rawfile <- file.path(OUT, "NF_raw.jsonl")

for (g in grid) for (rep in g[[3]]) {
  n <- g[[1]]; p <- g[[2]]
  d <- make_data(n, p, rep)
  stopifnot(d$gram_err < 1e-8)
  t0 <- proc.time()[["elapsed"]]
  fit <- tryCatch(v3_fit(d$X, d$y, seed = rep + 1L, allocation = list(mem_gb = 8, hours = HOURS)),
                  error = function(e) list(status = paste0("R_error: ", conditionMessage(e))))
  el <- proc.time()[["elapsed"]] - t0
  if (rep == g[[3]][1] && !file.exists(file.path(OUT, "NF_names.txt")))
    writeLines(c(names(fit), "--- ls0:", names(fit$ls0), "--- start_mode:", names(fit$start_mode)), file.path(OUT, "NF_names.txt"))
  sm <- if (is.list(fit$start_mode)) fit$start_mode$S else fit$start_mode
  hb <- fit$hpm_before_ls0; hb <- if (is.list(hb)) hb$model else hb
  hpm <- sort(as.integer(fit$hpm))
  nsm <- length(sm)
  rec <- list(n = n, p = p, rep = rep, status = fit$status, elapsed_sec = round(el, 1),
    gram_err = d$gram_err, mean_err = d$mean_err,
    start_mode_size = nsm, start_mode = sort(as.integer(sm)),
    S0_subset_start_mode = all(S0 %in% sm),
    hpm = hpm, hpm_eq_S0 = identical(hpm, S0),
    hpm_before_ls0 = sort(as.integer(hb)), hpm_before_ls0_eq_S0 = identical(sort(as.integer(hb)), S0),
    ls0_moves = if (!is.null(fit$ls0$moves)) as.integer(length(fit$ls0$moves)) else NA_integer_,
    ls0_local_limit = fit$ls0_local_limit, final_local_limit = fit$final_local_limit, local_limit = fit$local_limit,
    ls0_improved = fit$ls0_improved, ls0_hpm_changed = fit$ls0_hpm_changed,
    local_certified = fit$local_certified, local_certified_by = fit$local_certified_by,
    ls0_cap = ceiling(log2(n + p + 1)) + nsm, ell_n = fit$budgets$ell,
    hpm_F = fit$hpm_F, hpm_before_ls0_F = if (is.list(fit$hpm_before_ls0)) fit$hpm_before_ls0$F else NA,
    allocation_hours = HOURS, preflight_exceeds = fit$preflight$exceeds, preflight_bytes = fit$preflight$est_bytes,
    preflight_ls0_est_seconds = fit$preflight$ls0_worst_case$est_seconds,
    preflight_ls0_sec_per_score = fit$preflight$ls0_worst_case$seconds_per_score,
    branch = fit$branch_run, timings_total = fit$timings$total, timings_ls0 = fit$timings$ls0,
    message = if (is.null(fit$message)) NA else fit$message)
  cat(toJSON(rec, auto_unbox = TRUE, null = "null", na = "null", digits = NA), "\n", file = rawfile, append = TRUE, sep = "")
  cat(sprintf("n=%d p=%d rep=%d status=%s %.0fs hpm==S0:%s pre:%s ls0_limit:%s\n", n, p, rep, fit$status, el,
              rec$hpm_eq_S0, rec$hpm_before_ls0_eq_S0, format(rec$ls0_local_limit)))
  flush.console()
  rm(fit, d); gc()
}
