# backfit_tables.R -- ABL-START arm D: the API-RESID backfit ("resid") start tables at the fixed-point sweep rule
# (iterate until the start mode repeats, at most 10 sweeps; API-RESID REPORT §3.4), on the PRODUCTION blocks.
# Copied logic of API-RESID scripts/resid_sweeps.R (same formulas, same block_stats.cpp); writes, per design,
# $ABL_WORK/backfit/<id>_<sk>.rds = list(blocks, logr (list over blocks, engine code order), sweeps, fixed_at, mode).
# The tables are a deterministic function of (X, y): pi_0 = varpi * prod_b r_b^bf / Zbar_0 is then built by the
# production build_start (exact sampler, exact Zbar_0), so log Zhat of the SMC stays unbiased. Nothing is random.
# Usage: Rscript backfit_tables.R <id> <sk> [<id> <sk> ...]
args <- commandArgs(TRUE)
MAXSW <- 10L; A0 <- 0.01; B0 <- 0.01
STUDY <- "/home/fb31/ls0_work/study"; W <- Sys.getenv("ABL_WORK", "/home/fb31/abl_work")
sd <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
suppressMessages(source("/home/fb31/ls0_work/core_ls0/v3.R"))   # production core + O-LS0 exports (start mode)
bs_env <- new.env()
Rcpp::sourceCpp(file.path(sd, "block_stats.cpp"), env = bs_env, cacheDir = file.path(tempdir(), "bscache"))
dir.create(file.path(W, "backfit"), showWarnings = FALSE, recursive = TRUE)
for (i in seq(1, length(args), by = 2)) {
  id <- args[i]; sk <- args[i + 1]; pp <- sub("_.*", "", id)
  inp <- readRDS(file.path(STUDY, "inputs", pp, paste0(id, ".rds")))
  X <- inp$X; y <- unname(inp$Y[, sk])
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  setup <- v3_setup(ctx)
  n <- pre$n; nu <- A0 + n / 2; Xs <- pre$X; ys <- pre$y; yty <- sum(ys^2)
  blocks <- setup$blocks; cols <- lapply(blocks, function(b) match(b, pre$kept))
  mode_of <- function(lrs) {
    tabs <- mapply(function(b, lr) list(members = b, log_r = lr, log_m = lr), blocks, lrs, SIMPLIFY = FALSE)
    stt <- v3_start(ctx, blocks, tabs); sort(as.integer(.v3cpp$cpp_ls0_start_mode(stt$ptr)$model))
  }
  st0 <- lapply(cols, function(j) { Xb <- Xs[, j, drop = FALSE]; bs_env$block_stats_cpp(crossprod(Xb), crossprod(Xb, cbind(ys)), n) })
  lr_v3 <- lapply(st0, function(s) -0.5 * s$ld - nu * (log(2 * B0 + yty - s$t[, 1]) - log(2 * B0 + yty)))
  chk <- max(mapply(function(a, b) max(abs(a - b$log_r), na.rm = TRUE), lr_v3, setup$tables))
  Sm <- mode_of(lr_v3); fixed <- NA_integer_; lrs <- lr_v3
  for (sw in 1:MAXSW) {
    bfull <- numeric(ncol(Xs))
    if (length(Sm)) { j <- match(Sm, pre$kept); bfull[j] <- qr.coef(qr(Xs[, j, drop = FALSE]), ys); bfull[is.na(bfull)] <- 0 }
    lrs <- lapply(cols, function(jb) {
      bb <- bfull; bb[jb] <- 0; yb <- ys - drop(Xs %*% bb); yyb <- sum(yb^2)
      Xb <- Xs[, jb, drop = FALSE]; s <- bs_env$block_stats_cpp(crossprod(Xb), crossprod(Xb, cbind(yb)), n)
      -0.5 * s$ld - nu * (log(2 * B0 + yyb - s$t[, 1]) - log(2 * B0 + yyb))
    })
    M <- mode_of(lrs)
    if (identical(M, Sm)) { fixed <- sw; break }
    Sm <- M
  }
  saveRDS(list(blocks = blocks, logr = lrs, sweeps = sw, fixed_at = fixed, mode = Sm, v3_table_check = chk),
          file.path(W, "backfit", paste0(id, "_", sk, ".rds")))
  cat(sprintf("%s %s sweeps=%d fixed_at=%s |mode|=%d v3 table check %.1e\n", id, sk, sw, fixed, length(Sm), chk))
}
