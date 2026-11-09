# W2-SIM/LOC copy of W2-SIM/scripts/prod_fit.R (sha256 of the original recorded in LOC/DESIGN.md). LOC additions ONLY:
#   design = file : X (standardised, n x p, column-major float64 little-endian) and y (float64) read from dfile.X.bin /
#   dfile.y.bin, S0 (1-based) and beta from dfile.json (written by loc_export.py = the same data set as the component-port
#   run loc_run.py with the same fam/par/place/n/prule/seed); seedoff (integer, default 0) is added to data_seed so that
#   method seeds are distinct across LOC cells. The fit call v3_fit(X, y, seed = method_seed, allocation = ...) and all
#   recorded fields are unchanged.
# W2-SIM: one production SMC-BVS v3.1 fit (core as merged on main; deployed by git archive) on a synthetic design.
# Usage: Rscript --vanilla prod_fit.R CORE_DIR OUT_JSONL OUT_RDS_DIR key=value ...
#   design = excs | iidcs | iidfac   (exact-Gram CS; iid-row CS; iid-row factor model, see make_X)
#   n, p, rho, rep (data seed index), arm = mr1 | dbl, hours, mem_gb, bscale (coefficient scale), signs = aligned | mixed
#   k (factors, iidfac), load = equal | unif (loadings, iidfac)
# arm = dbl sets the documented testing option v3.ls0_ell = ell_n + K (K = min(p, floor(n/2))); the merged cap rule
# then gives LS0 cap ell_n + K + |S~0|  (= ell_n + 2|S~0| when the start mode is size-saturated, >= it otherwise).
# No production source is modified. Seeds: data seed = 7919 * rep + 13 * n + p (design-specific offset below);
# method seed = data seed + 4,000,000 (study convention). Paired arms share data and method seed.
args <- commandArgs(trailingOnly = TRUE)
CORE <- args[1]; OUT <- args[2]; RDSDIR <- args[3]
source(file.path(CORE, "v3.R"))   # first: the core defines top-level objects; our names are set after it
kv <- strsplit(args[-(1:3)], "=", fixed = TRUE)
A <- setNames(lapply(kv, `[`, 2), vapply(kv, `[`, "", 1))
g <- function(k, d) if (is.null(A[[k]])) d else A[[k]]
design <- g("design", "excs"); n <- as.integer(g("n", 600)); p <- as.integer(g("p", 570))
rho <- as.numeric(g("rho", 0.5)); rep <- as.integer(g("rep", 1)); arm <- g("arm", "mr1")
hours <- as.numeric(g("hours", 2000)); mem_gb <- as.numeric(g("mem_gb", 8)); bscale <- as.numeric(g("bscale", 1))
signs <- g("signs", "aligned"); kfac <- as.integer(g("k", 1)); load <- g("load", "equal")
tag <- g("tag", "")
suppressMessages(library(jsonlite))
S0 <- c(3L, 27L, 54L, 76L)            # 1-based (= 0-based 2, 26, 53, 75 of the ticket scripts)
beta0 <- bscale * c(1.4, 1.0, 1.8, 1.2) * (if (signs == "mixed") c(1, -1, 1, -1) else 1)
dfile <- g("dfile", ""); seedoff <- as.integer(g("seedoff", 0))                                   # LOC addition
if (design == "file") { meta <- jsonlite::fromJSON(paste0(dfile, ".json")); S0 <- as.integer(meta$S0_1based); beta0 <- as.numeric(meta$beta) }  # LOC addition
dcode <- match(design, c("excs", "iidcs", "iidfac", "file"))                                       # LOC: + "file"
data_seed <- 7919L * rep + 13L * n + p + 1000003L * dcode + seedoff                                # LOC: + seedoff
method_seed <- data_seed + 4000000L

make_X <- function() {
  set.seed(data_seed)
  if (design == "file") { X <- matrix(readBin(paste0(dfile, ".X.bin"), "double", n * p, size = 8, endian = "little"), n, p); return(X) }  # LOC addition
  if (design == "excs") {
    stopifnot(p <= n - 1)
    Z <- matrix(rnorm(n * p), n, p); Z <- sweep(Z, 2, colMeans(Z))
    Q <- qr.Q(qr(Z))
    Sig <- (1 - rho) * diag(p) + rho * matrix(1, p, p)
    X <- sqrt(n - 1) * Q %*% chol(Sig)
    attr(X, "gram_err") <- max(abs(crossprod(X) / (n - 1) - Sig)); return(X)
  }
  if (design == "iidcs") {
    f <- rnorm(n); E <- matrix(rnorm(n * p), n, p)
    return(sqrt(rho) * f + sqrt(1 - rho) * E)
  }
  if (design == "iidfac") {     # x = Lambda f + sqrt(1 - rowSums(Lambda^2)) e ; unit variances
    L <- if (load == "equal") matrix(sqrt(rho / kfac), p, kfac) else matrix(runif(p * kfac, 0.2, 0.9), p, kfac) / sqrt(kfac)
    Fm <- matrix(rnorm(n * kfac), n, kfac); E <- matrix(rnorm(n * p), n, p)
    X <- Fm %*% t(L) + sweep(E, 2, sqrt(1 - rowSums(L^2)), `*`); return(X)
  }
  stop("unknown design")
}
X <- make_X()
stopifnot(max(S0) <= p); beta <- numeric(p); beta[S0] <- beta0
set.seed(data_seed + 1L)
y <- if (design == "file") readBin(paste0(dfile, ".y.bin"), "double", n, size = 8, endian = "little") else as.vector(X %*% beta + rnorm(n))  # LOC: file branch
ell <- ceiling(log2(n + p + 1)); K <- min(p, n %/% 2)
if (arm == "dbl") options(v3.ls0_ell = ell + K)
t0 <- proc.time()[["elapsed"]]
fit <- tryCatch(v3_fit(X, y, seed = method_seed, allocation = list(mem_gb = mem_gb, hours = hours)),
                error = function(e) list(status = paste0("R_error: ", conditionMessage(e))))
el <- proc.time()[["elapsed"]] - t0
# Safety copy of the whole fit first (probes / savefull=1), so a post-processing error never loses a long fit.
if (g("savefull", "0") == "1")
  saveRDS(fit, file.path(RDSDIR, sprintf("FULL_%s_n%d_p%d_r%03d_%s%s.rds", design, n, p, rep, arm, tag)))
key <- function(S) paste(sort(as.integer(S)), collapse = ",")
s0k <- key(S0)
mod <- function(x) if (is.list(x)) x$model else x
sm <- mod(fit$start_mode)
ls0 <- fit$ls0
# First LS0 scan whose centre C has S0 in N(C) U {C} (scored by LS0), from the scanned centres (1-based scan index).
first_scoring <- NA_integer_; first_arrival <- NA_integer_
nbr <- function(C) { a <- setdiff(C, S0); b <- setdiff(S0, C); length(a) + length(b) <= 1 || (length(a) == 1 && length(b) == 1) }
moves <- NULL
if (!is.null(ls0$scanned_centres)) {
  sc <- ls0$scanned_centres
  for (t in seq_along(sc)) {
    C <- as.integer(sc[[t]])
    if (is.na(first_arrival) && key(C) == s0k) first_arrival <- t
    if (is.na(first_scoring) && nbr(C)) first_scoring <- t
  }
  pth <- ls0$path
  if (length(pth) >= 2) {
    moves <- vapply(2:length(pth), function(i) {
      a <- as.integer(pth[[i - 1]]); b <- as.integer(pth[[i]])
      ins <- length(setdiff(b, a)); outs <- length(setdiff(a, b))
      if (ins == 1 && outs == 1) "swap" else if (ins == 1) "add" else if (outs == 1) "del" else "other"
    }, "")
  }
}
lead_swaps <- if (length(moves)) { r <- rle(moves); if (r$values[1] == "swap") r$lengths[1] else 0L } else NA_integer_
swaps_after_del <- if (length(moves) && any(moves == "del")) sum(moves[seq(which(moves == "del")[1], length(moves))] == "swap") else NA_integer_
hb <- mod(fit$hpm_before_ls0)
nz <- function(x) if (is.null(x)) NA else x
rec <- list(design = design, n = n, p = p, rho = rho, rep = rep, arm = arm, tag = tag, bscale = bscale, signs = signs,
  k = kfac, load = load, data_seed = data_seed, method_seed = method_seed, hours = hours, mem_gb = mem_gb,
  status = nz(fit$status), message = nz(fit$message), elapsed_sec = round(el, 1), branch = nz(fit$branch_run),
  gram_err = nz(attr(X, "gram_err")), ell = nz(fit$budgets$ell), K = nz(fit$budgets$K), B = nz(fit$budgets$B),
  tier = nz(fit$settings$tier),
  preflight_exceeds = nz(fit$preflight$exceeds), preflight_est_bytes = nz(fit$preflight$est_bytes),
  preflight_ls0_est_seconds = nz(fit$preflight$ls0_worst_case$est_seconds),
  preflight_ls0_scans = nz(fit$preflight$ls0_worst_case$scans),
  preflight_ls0_sec_per_score = nz(fit$preflight$ls0_worst_case$seconds_per_score),
  start_mode_size = length(sm), S0_in_start = all(S0 %in% sm), start_mode_truths_missing = setdiff(S0, sm),
  hpm = sort(as.integer(fit$hpm)), hpm_eq_S0 = key(fit$hpm) == s0k, hpm_F = nz(fit$hpm_F),
  hpm_provenance_phase = nz(fit$hpm_provenance$phase), hpm_provenance_mech = nz(fit$hpm_provenance$mechanism),
  hpm_before_ls0 = sort(as.integer(hb)), hpm_before_ls0_eq_S0 = if (is.null(hb)) NA else key(hb) == s0k,
  hpm_before_ls0_F = nz(fit$hpm_before_ls0$F),
  hpm_before_ls0_phase = nz(fit$hpm_before_ls0$provenance$phase),
  final_ls_local_limit = nz(fit$local_search$local_limit), final_ls_certified = nz(fit$local_search$local_certified),
  final_ls_moves = nz(fit$local_search$moves),
  local_limit = nz(fit$local_limit), local_certified = nz(fit$local_certified), local_certified_by = nz(fit$local_certified_by),
  ls0_move_cap = nz(ls0$move_cap), ls0_cap_rule = nz(ls0$move_cap_rule), ls0_ell = nz(ls0$ell),
  ls0_moves = nz(ls0$moves), ls0_termination = nz(ls0$termination), ls0_local_limit = nz(ls0$local_limit),
  ls0_returned_eq_S0 = if (is.null(ls0$returned)) NA else key(ls0$returned) == s0k,
  ls0_n_evaluated = nz(ls0$n_evaluated), ls0_first_scoring_scan = first_scoring, ls0_first_arrival_scan = first_arrival,
  ls0_lead_swaps = lead_swaps, ls0_n_swap = sum(moves == "swap"), ls0_n_del = sum(moves == "del"), ls0_n_add = sum(moves == "add"),
  ls0_swaps_after_first_del = swaps_after_del,
  ls0_improved = nz(fit$ls0_improved), ls0_hpm_changed = nz(fit$ls0_hpm_changed),
  timings_total = nz(fit$timings$total), timings_ls0 = nz(fit$timings$ls0), timings_local = nz(fit$timings$local),
  timings_calibration = nz(fit$timings$calibration), timings_final = nz(fit$timings$final),
  core_dir = CORE, host = Sys.info()[["nodename"]], slurm_job = Sys.getenv("SLURM_JOB_ID"),
  slurm_array_task = Sys.getenv("SLURM_ARRAY_TASK_ID"), R = R.version.string)
cat(toJSON(rec, auto_unbox = TRUE, null = "null", na = "null", digits = NA), "\n", file = OUT, append = TRUE, sep = "")
keep <- fit[intersect(names(fit), c("status", "message", "budgets", "preflight", "start_mode", "hpm", "hpm_F", "hpm_provenance",
  "hpm_before_ls0", "local_limit", "local_certified", "local_certified_by", "timings", "settings", "branch_run", "calibration"))]
keep$ls0 <- ls0; keep$local_search <- fit$local_search[setdiff(names(fit$local_search), c("scanned_centres"))]
keep$rec <- rec
saveRDS(keep, file.path(RDSDIR, sprintf("%s_n%d_p%d_r%03d_%s%s.rds", design, n, p, rep, arm, tag)), compress = "xz")
cat(sprintf("%s n=%d p=%d rep=%d arm=%s status=%s %.0fs hpm==S0 %s before %s ls0moves %s cap %s first_scoring %s\n", design, n, p, rep,
  arm, rec$status, el, rec$hpm_eq_S0, rec$hpm_before_ls0_eq_S0, rec$ls0_moves, rec$ls0_move_cap, first_scoring))
