# resid_step0.R -- API-RESID (synthesis task 8, F-SIGMA §10 Step 0): post hoc start tables on the 2,400 PROD-H fits.
# NO SMC runs, no regenerated data. For each (dataset, scale) of the O-LS0 study copy (~/ls0_work/study):
#   production path up to the setup (v3_preprocess -> v3_context -> v3_setup: blocks + v3 tables), exactly as O-LS0's
#   10_ls0_fit.R; then per block every sub-model's (log D_U, t_U) (block_stats.cpp), and the alternative tables:
#     v3re      : v3 tables rebuilt from (log D_U, t_U)  -> check against the engine tables and the O-LS0 record
#     C_mode    : common sigma2 = s2(S~0)  (S~0 = v3 start mode)            [F-SIGMA "sigma~2_{S~0}" / "v3-mode RSS"]
#     C_fix     : C-fix iteration from s2(S~0): s2 <- s2(mode of pi0^C[s2]) until the mode repeats (max 20)
#     C_sy2     : common sigma2 = c/(2 nu), c = 2 b0 + y'y  (null plug-in s_y^2)
#     C_S0      : common sigma2 = s2(S0)   (extra: truth-based plug-in, not feasible)
#     C_orc     : common sigma2 = sample var(eps)/s^2 on the standardised scale (extra: oracle)
#     resid1/3  : O-DILUTE 'resid': v3 tables of block b on y_b = y - X_{-b} bhat_{-b}, bhat = OLS on the current
#                 start mode (start: v3 mode), new mode, repeat; after sweep 1 and sweep 3
#   s2(S) := (2 b0 + Q_S)/(2 nu)  (F-SIGMA's sigma~2_S).  Common table: log r^C_b(U) = -ld_U/2 + t_U/(2 s2).
# Per variant: log pi0(S0), log pi0(R_d) d = 0,1,2 (engine cpp_ls0_pi0_Rd), the start mode (engine cpp_ls0_start_mode),
# |mode|, |mode n S0|, mode == S0. pi0 is built by the production cpp_start from the supplied tables.
# Usage: Rscript resid_step0.R <out_csv> [shard] [nshards] [max_tasks]
args <- commandArgs(TRUE)
out <- args[1]
shard <- if (length(args) >= 2) as.integer(args[2]) else 1L
nshards <- if (length(args) >= 3) as.integer(args[3]) else 1L
maxt <- if (length(args) >= 4) as.integer(args[4]) else .Machine$integer.max
set.seed(20261102)  # nothing here is random; fixed for the record
STUDY <- "/home/fb31/ls0_work/study"; LS0OUT <- "/home/fb31/ls0_work/full"
sd <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
suppressMessages(source("/home/fb31/ls0_work/core_ls0/v3.R"))     # production core + O-LS0 test exports (read-only)
bs_env <- new.env()
Rcpp::sourceCpp(file.path(sd, "block_stats.cpp"), env = bs_env, cacheDir = file.path(tempdir(), "bscache"))

A0 <- 0.01; B0 <- 0.01

fit_one <- function(inp, tru, sk) {
  X <- inp$X; y <- unname(inp$Y[, sk]); S0 <- sort(as.integer(tru$active))
  cval <- unname(inp$scales[sk])
  if (max(abs(y - (cval * tru$signal + tru$eps))) > 1e-8) stop("y != c*signal + eps")
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  if (pre$status != "ok") stop("preprocess ", pre$status)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  setup <- v3_setup(ctx)
  if (inherits(setup, "v3_setup_failed")) stop("setup failed")
  n <- pre$n; nu <- A0 + n / 2; Xs <- pre$X; ys <- pre$y; yty <- sum(ys^2); K <- setup$budgets$K
  s2_of <- function(S) {  # (2 b0 + Q_S)/(2 nu), Q_S = y'y - n z' H^{-1} z
    if (!length(S)) return((2 * B0 + yty) / (2 * nu))
    j <- match(S, pre$kept); Xj <- Xs[, j, drop = FALSE]
    H <- (n + 1) * crossprod(Xj) + diag(length(j)); z <- crossprod(Xj, ys)
    (2 * B0 + yty - n * sum(z * solve(H, z))) / (2 * nu)
  }
  blocks <- setup$blocks
  cols <- lapply(blocks, function(b) match(b, pre$kept))
  st0 <- lapply(cols, function(j) { Xb <- Xs[, j, drop = FALSE]; bs_env$block_stats_cpp(crossprod(Xb), crossprod(Xb, cbind(ys)), n) })
  # check: v3 tables rebuilt from (ld, t) vs the engine's tables
  lr_v3 <- lapply(st0, function(s) -0.5 * s$ld - nu * (log(2 * B0 + yty - s$t[, 1]) - log(2 * B0 + yty)))
  chk <- max(mapply(function(a, b) max(abs(a - b$log_r)), lr_v3, setup$tables))
  summ <- function(lrs) {
    tabs <- mapply(function(b, lr) list(members = b, log_r = lr, log_m = lr), blocks, lrs, SIMPLIFY = FALSE)
    stt <- v3_start(ctx, blocks, tabs)
    md <- .v3cpp$cpp_ls0_start_mode(stt$ptr); M <- sort(as.integer(md$model))
    Rd <- .v3cpp$cpp_ls0_pi0_Rd(stt$ptr, S0, 2L)
    list(lpS0 = v3_start_logmass(stt, S0), lpR0 = Rd[1], lpR1 = Rd[2], lpR2 = Rd[3], mode = M,
         msize = length(M), mtrue = length(intersect(M, S0)), meq = identical(M, S0), lpmode = md$log_pi0)
  }
  lrC <- function(s2) lapply(st0, function(s) -0.5 * s$ld + s$t[, 1] / (2 * s2))
  res <- list(); s2v <- list()
  res$v3re <- summ(lr_v3)
  Smode <- res$v3re$mode
  s2v$C_mode <- s2_of(Smode); res$C_mode <- summ(lrC(s2v$C_mode))
  # C-fix (F-SIGMA study_size.py): from s2(S~0); mode of pi0^C[s2]; stop when the mode repeats
  s2 <- s2v$C_mode; Sfix <- Smode; its <- 0L; cur <- res$C_mode
  repeat {
    Snew <- cur$mode; its <- its + 1L
    if (identical(Snew, Sfix) || its > 20L) break
    Sfix <- Snew; s2 <- s2_of(Snew); cur <- summ(lrC(s2))
  }
  s2v$C_fix <- s2; res$C_fix <- cur
  s2v$C_sy2 <- (2 * B0 + yty) / (2 * nu); res$C_sy2 <- summ(lrC(s2v$C_sy2))
  s2v$C_S0 <- s2_of(S0); res$C_S0 <- summ(lrC(s2v$C_S0))
  sfac <- sum((y - mean(y))^2) / yty                       # y_std = (y - ybar)/s, s^2 = sfac
  s2v$C_orc <- (sum((tru$eps - mean(tru$eps))^2) / (n - 1)) / sfac
  res$C_orc <- summ(lrC(s2v$C_orc))
  # resid (backfit), O-DILUTE run_study.py
  Sm <- Smode
  for (sw in 1:3) {
    bfull <- numeric(ncol(Xs))
    if (length(Sm)) { j <- match(Sm, pre$kept); bfull[j] <- qr.coef(qr(Xs[, j, drop = FALSE]), ys); bfull[is.na(bfull)] <- 0 }
    lrs <- lapply(cols, function(jb) {
      bb <- bfull; bb[jb] <- 0; yb <- ys - drop(Xs %*% bb); yyb <- sum(yb^2)
      Xb <- Xs[, jb, drop = FALSE]; s <- bs_env$block_stats_cpp(crossprod(Xb), crossprod(Xb, cbind(yb)), n)
      -0.5 * s$ld - nu * (log(2 * B0 + yyb - s$t[, 1]) - log(2 * B0 + yyb))
    })
    o <- summ(lrs); Sm <- o$mode
    if (sw == 1) res$resid1 <- o
    if (sw == 3) res$resid3 <- o
  }
  row <- data.frame(dataset_id = inp$dataset_id, p = inp$p, scenario = inp$scenario, replicate = inp$replicate,
                    scale_key = sk, c = cval, J = length(blocks), B = setup$B, K = K, tab_check = chk,
                    s2_orc = s2v$C_orc, s2_mode = s2v$C_mode, s2_fix = s2v$C_fix, s2_sy2 = s2v$C_sy2, s2_S0 = s2v$C_S0,
                    fix_its = its)
  for (v in names(res)) {
    r <- res[[v]]
    row[[paste0(v, "_lpS0")]] <- r$lpS0; row[[paste0(v, "_lpR0")]] <- r$lpR0
    row[[paste0(v, "_lpR1")]] <- r$lpR1; row[[paste0(v, "_lpR2")]] <- r$lpR2
    row[[paste0(v, "_msize")]] <- r$msize; row[[paste0(v, "_mtrue")]] <- r$mtrue; row[[paste0(v, "_meq")]] <- r$meq
    row[[paste0(v, "_lpmode")]] <- r$lpmode
  }
  # O-LS0 record (same core, same data): reproduction check of the v3 start
  f <- file.path(LS0OUT, sprintf("p%04d", inp$p), paste0(inp$dataset_id, "_", sk, ".rds"))
  if (file.exists(f)) {
    rr <- readRDS(f)$row
    row$ls0_lpS0 <- rr$log_pi0_S0; row$ls0_lpR2 <- rr$log_pi0_R2; row$ls0_start_size <- rr$start_size
  } else { row$ls0_lpS0 <- NA; row$ls0_lpR2 <- NA; row$ls0_start_size <- NA }
  row
}

tasks <- expand.grid(scale_key = c("c100", "c050"), replicate = 1:100, scenario = 1:6, p = c(500L, 1000L),
                     stringsAsFactors = FALSE)
mine <- tasks[(seq_len(nrow(tasks)) - 1L) %% nshards == shard - 1L, , drop = FALSE]
done <- if (file.exists(out)) { d <- read.csv(out, stringsAsFactors = FALSE); paste(d$dataset_id, d$scale_key) } else character(0)
cur <- ""; ndone <- 0L
for (i in seq_len(nrow(mine))) {
  t <- mine[i, ]
  id <- sprintf("p%04d_S%d_r%03d", t$p, t$scenario, t$replicate)
  if (paste(id, t$scale_key) %in% done) next
  if (ndone >= maxt) break
  if (id != cur) {
    inp <- readRDS(file.path(STUDY, "inputs", sprintf("p%04d", t$p), paste0(id, ".rds")))
    tru <- readRDS(file.path(STUDY, "truth", sprintf("p%04d", t$p), paste0(id, ".rds")))
    cur <- id
  }
  t0 <- proc.time()[["elapsed"]]
  r <- tryCatch(fit_one(inp, tru, t$scale_key), error = function(e) e)
  if (inherits(r, "error")) { message(sprintf("ERROR %s %s: %s", id, t$scale_key, conditionMessage(r))); next }
  r$sec <- proc.time()[["elapsed"]] - t0
  write.table(r, out, sep = ",", row.names = FALSE, col.names = !file.exists(out), append = file.exists(out))
  ndone <- ndone + 1L
  message(sprintf("%s %s %s %.1fs chk=%.1e v3 %.2f (ls0 %.2f) Cmode %.1f Cfix %.1f(%d) sy2 %.1f resid3 %.2f", format(Sys.time(), "%H:%M:%S"),
                  id, t$scale_key, r$sec, r$tab_check, r$v3re_lpS0, r$ls0_lpS0, r$C_mode_lpS0, r$C_fix_lpS0, r$fix_its, r$C_sy2_lpS0, r$resid3_lpS0))
}
