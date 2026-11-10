# W3-SCR numerics N1/N3: one production SMC-BVS v3.1 fit (core copy of main @ 2252d57, numerics/core_copy) on a
# synthetic design; records the certificate flags, the reported model and both search archives.
# Usage: Rscript --vanilla scr_fit.R CORE_DIR OUT_JSONL key=value ...
#   design = iid | ar | cs | fac | dupnoise | twin     n, p, rho, k (factors), rep, bscale, s0 (4 or 8), dump=DIR
#   iid: independent N(0,1) columns;  ar: AR(1) rows with parameter rho;  cs: one factor, equal loadings sqrt(rho);
#   fac: k factors, loadings U(0.2,0.9)/sqrt(k) (as W2-SIM prod_fit.R "iidfac", load = unif);
#   dupnoise: cs design in which every noise column j > p/2 is an exact copy of noise column j - p/2 plus N(0, 1e-6)
#             (sparse eigenvalue floor fails at size 2; truths are not copied);
#   twin: iid design plus, for each truth t, a twin column  x_t' = rho x_t + sqrt(1-rho^2) e  placed at t + 1.
# Seeds: data seed = 7919*rep + 13*n + p + 1000003*dcode; method seed = data seed + 4,000,000 (W2-SIM convention).
args <- commandArgs(trailingOnly = TRUE)
CORE <- args[1]; OUT <- args[2]
source(file.path(CORE, "v3.R"))
kv <- strsplit(args[-(1:2)], "=", fixed = TRUE)
A <- setNames(lapply(kv, `[`, 2), vapply(kv, `[`, "", 1))
g <- function(k, d) if (is.null(A[[k]])) d else A[[k]]
design <- g("design", "iid"); n <- as.integer(g("n", 100)); p <- as.integer(g("p", 400))
rho <- as.numeric(g("rho", 0.5)); rep <- as.integer(g("rep", 1)); bscale <- as.numeric(g("bscale", 1))
kfac <- as.integer(g("k", 3)); s0n <- as.integer(g("s0", 4)); dump <- g("dump", "")
hours <- as.numeric(g("hours", 2000)); mem_gb <- as.numeric(g("mem_gb", 8))
suppressMessages(library(jsonlite))
S0 <- if (s0n == 4) c(3L, 27L, 54L, 76L) else c(3L, 27L, 54L, 76L, 101L, 133L, 160L, 190L)
beta0 <- bscale * rep_len(c(1.4, -1.0, 1.8, -1.2), length(S0))
dcode <- match(design, c("iid", "ar", "cs", "fac", "dupnoise", "twin"))
stopifnot(!is.na(dcode), max(S0) + 1L <= p)
data_seed <- 7919L * rep + 13L * n + p + 1000003L * dcode
method_seed <- data_seed + 4000000L
set.seed(data_seed)
X <- switch(design,
  iid = matrix(rnorm(n * p), n, p),
  ar = { E <- matrix(rnorm(n * p), n, p); Z <- E; for (j in 2:p) Z[, j] <- rho * Z[, j - 1] + sqrt(1 - rho^2) * E[, j]; Z },
  cs = { f <- rnorm(n); sqrt(rho) * f + sqrt(1 - rho) * matrix(rnorm(n * p), n, p) },
  fac = { L <- matrix(runif(p * kfac, 0.2, 0.9), p, kfac) / sqrt(kfac); Fm <- matrix(rnorm(n * kfac), n, kfac)
          Fm %*% t(L) + sweep(matrix(rnorm(n * p), n, p), 2, sqrt(1 - rowSums(L^2)), `*`) },
  dupnoise = { f <- rnorm(n); Z <- sqrt(rho) * f + sqrt(1 - rho) * matrix(rnorm(n * p), n, p)
               h <- p %/% 2; src <- setdiff(seq_len(h), S0); src <- src[src + h <= p]
               Z[, src + h] <- Z[, src] + 1e-3 * matrix(rnorm(n * length(src)), n); Z },
  twin = { Z <- matrix(rnorm(n * p), n, p); for (t in S0) Z[, t + 1L] <- rho * Z[, t] + sqrt(1 - rho^2) * rnorm(n); Z })
beta <- numeric(p); beta[S0] <- beta0
set.seed(data_seed + 1L)
y <- as.vector(X %*% beta + rnorm(n))
t0 <- proc.time()[["elapsed"]]
fit <- tryCatch(v3_fit(X, y, seed = method_seed, allocation = list(mem_gb = mem_gb, hours = hours)),
                error = function(e) list(status = paste0("R_error: ", conditionMessage(e))))
el <- proc.time()[["elapsed"]] - t0
nz <- function(x) if (is.null(x)) NA else x
srt <- function(x) if (is.null(x)) NULL else sort(as.integer(x))
arch <- function(a) if (is.null(a)) list(present = FALSE) else list(present = TRUE,
  certified = isTRUE(a$local_certified), limit = isTRUE(a$local_limit), termination = nz(a$termination),
  moves = nz(a$moves), returned = srt(a$returned), returned_size = length(a$returned), returned_F = nz(a$returned_F),
  contains_S0 = all(S0 %in% a$returned), eq_S0 = identical(srt(a$returned), sort(S0)))
sm <- fit$start_mode; if (is.list(sm)) sm <- sm$model
rec <- list(design = design, n = n, p = p, rho = rho, k = kfac, rep = rep, bscale = bscale, s0 = length(S0),
  data_seed = data_seed, method_seed = method_seed, status = nz(fit$status), branch = nz(fit$branch_run),
  K = nz(fit$budgets$K), ell = nz(fit$budgets$ell), B = nz(fit$budgets$B), elapsed_sec = round(el, 1),
  local_certified = nz(fit$local_certified), local_certified_by = nz(fit$local_certified_by),
  local_limit = nz(fit$local_limit), final_local_limit = nz(fit$final_local_limit), ls0_local_limit = nz(fit$ls0_local_limit),
  hpm = srt(fit$hpm), hpm_size = length(fit$hpm), hpm_F = nz(fit$hpm_F),
  hpm_contains_S0 = all(S0 %in% fit$hpm), hpm_eq_S0 = identical(srt(fit$hpm), sort(S0)),
  hpm_missing = setdiff(S0, fit$hpm), hpm_extra = setdiff(srt(fit$hpm), S0),
  hpm_phase = nz(fit$hpm_provenance$phase), start_mode_size = length(sm), start_contains_S0 = all(S0 %in% sm),
  final_search = arch(fit$local_search), ls0 = arch(fit$ls0),
  mpm = srt(fit$mpm), mpm_contains_S0 = all(S0 %in% fit$mpm),
  flags = fit$flags[intersect(names(fit$flags), c("E1", "E2", "E3", "low_empirical_ESS", "checks_passed_final", "escalated"))])
cat(toJSON(rec, auto_unbox = TRUE, null = "null", na = "null", digits = NA), "\n", file = OUT, append = TRUE, sep = "")
if (nzchar(dump)) {   # fidelity dump: standardised data as the core sees it + scored models with their F
  dir.create(dump, showWarnings = FALSE, recursive = TRUE)
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  tag <- sprintf("%s_n%d_p%d_r%d", design, n, p, rep)
  write.table(pre$X, file.path(dump, paste0(tag, "_X.csv")), sep = ",", row.names = FALSE, col.names = FALSE)
  write.table(pre$y, file.path(dump, paste0(tag, "_y.csv")), sep = ",", row.names = FALSE, col.names = FALSE)
  top <- fit$top_store
  mods <- list(hpm = list(model = srt(fit$hpm), F = fit$hpm_F))
  if (!is.null(top)) mods$top <- lapply(seq_along(top$models), function(i) list(model = srt(top$models[[i]]), F = top$value[i]))
  if (!is.null(fit$ls0)) mods$ls0_path <- lapply(seq_along(fit$ls0$path), function(i) list(model = srt(fit$ls0$path[[i]]), F = fit$ls0$path_F[i]))
  if (!is.null(fit$local_search)) mods$final_scanned <- lapply(seq_along(fit$local_search$scanned_centres),
    function(i) list(model = srt(fit$local_search$scanned_centres[[i]]), F = fit$local_search$scanned_F[i]))
  writeLines(toJSON(list(S0 = S0, kept = pre$kept, models = mods, K = fit$budgets$K), auto_unbox = TRUE, digits = NA), file.path(dump, paste0(tag, "_models.json")))
}
cat(sprintf("%s n=%d p=%d rep=%d status=%s %.0fs cert=%s by=%s |hpm|=%d S0sub=%s eq=%s\n", design, n, p, rep, rec$status, el,
  rec$local_certified, rec$local_certified_by, rec$hpm_size, rec$hpm_contains_S0, rec$hpm_eq_S0))
