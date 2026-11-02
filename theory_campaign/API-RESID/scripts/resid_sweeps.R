# resid_sweeps.R -- API-RESID addition: is the 3-sweep backfit start (resid3 in resid_step0.R) a fixed point?
# Same setup and same backfit as resid_step0.R (copied, not changed); runs up to MAXSW sweeps from the v3 mode and
# stops when the start mode repeats. NO SMC runs, no regenerated data.
# Records per fit: the sweep at which the mode first repeats (NA = not within MAXSW), whether a 2-cycle occurred,
# and log pi0(S0), log pi0(R2), |mode|, |mode n S0|, mode == S0 at sweeps 3, 5 and the last sweep.
# Usage: Rscript resid_sweeps.R <out_csv> [shard] [nshards]
args <- commandArgs(TRUE)
out <- args[1]
shard <- if (length(args) >= 2) as.integer(args[2]) else 1L
nshards <- if (length(args) >= 3) as.integer(args[3]) else 1L
MAXSW <- 10L
STUDY <- "/home/fb31/ls0_work/study"
sd <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
suppressMessages(source("/home/fb31/ls0_work/core_ls0/v3.R"))
bs_env <- new.env()
Rcpp::sourceCpp(file.path(sd, "block_stats.cpp"), env = bs_env, cacheDir = file.path(tempdir(), "bscache"))
A0 <- 0.01; B0 <- 0.01

fit_one <- function(inp, tru, sk) {
  X <- inp$X; y <- unname(inp$Y[, sk]); S0 <- sort(as.integer(tru$active))
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  if (pre$status != "ok") stop("preprocess ", pre$status)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  setup <- v3_setup(ctx)
  if (inherits(setup, "v3_setup_failed")) stop("setup failed")
  n <- pre$n; nu <- A0 + n / 2; Xs <- pre$X; ys <- pre$y; yty <- sum(ys^2)
  blocks <- setup$blocks
  cols <- lapply(blocks, function(b) match(b, pre$kept))
  summ <- function(lrs) {
    tabs <- mapply(function(b, lr) list(members = b, log_r = lr, log_m = lr), blocks, lrs, SIMPLIFY = FALSE)
    stt <- v3_start(ctx, blocks, tabs)
    md <- .v3cpp$cpp_ls0_start_mode(stt$ptr); M <- sort(as.integer(md$model))
    Rd <- .v3cpp$cpp_ls0_pi0_Rd(stt$ptr, S0, 2L)
    list(lpS0 = v3_start_logmass(stt, S0), lpR2 = Rd[3], mode = M, msize = length(M),
         mtrue = length(intersect(M, S0)), meq = identical(M, S0))
  }
  st0 <- lapply(cols, function(j) { Xb <- Xs[, j, drop = FALSE]; bs_env$block_stats_cpp(crossprod(Xb), crossprod(Xb, cbind(ys)), n) })
  lr_v3 <- lapply(st0, function(s) -0.5 * s$ld - nu * (log(2 * B0 + yty - s$t[, 1]) - log(2 * B0 + yty)))
  Sm <- summ(lr_v3)$mode
  hist <- list(Sm); rec <- list(); fixed <- NA_integer_; cyc2 <- FALSE
  for (sw in 1:MAXSW) {
    bfull <- numeric(ncol(Xs))
    if (length(Sm)) { j <- match(Sm, pre$kept); bfull[j] <- qr.coef(qr(Xs[, j, drop = FALSE]), ys); bfull[is.na(bfull)] <- 0 }
    lrs <- lapply(cols, function(jb) {
      bb <- bfull; bb[jb] <- 0; yb <- ys - drop(Xs %*% bb); yyb <- sum(yb^2)
      Xb <- Xs[, jb, drop = FALSE]; s <- bs_env$block_stats_cpp(crossprod(Xb), crossprod(Xb, cbind(yb)), n)
      -0.5 * s$ld - nu * (log(2 * B0 + yyb - s$t[, 1]) - log(2 * B0 + yyb))
    })
    o <- summ(lrs); rec[[sw]] <- o
    if (identical(o$mode, Sm)) { fixed <- sw; break }
    if (length(hist) >= 2 && identical(o$mode, hist[[length(hist) - 1]])) cyc2 <- TRUE
    hist[[length(hist) + 1]] <- o$mode; Sm <- o$mode
  }
  last <- length(rec)
  g <- function(k, f) if (k <= last) rec[[k]][[f]] else rec[[last]][[f]]  # after a fixed point the start is frozen
  row <- data.frame(dataset_id = inp$dataset_id, p = inp$p, scenario = inp$scenario, scale_key = sk,
                    fixed_at = fixed, cycle2 = cyc2, nsweeps = last)
  for (k in c(3L, 5L)) for (f in c("lpS0", "lpR2", "msize", "mtrue", "meq")) row[[paste0("s", k, "_", f)]] <- g(k, f)
  for (f in c("lpS0", "lpR2", "msize", "mtrue", "meq")) row[[paste0("last_", f)]] <- rec[[last]][[f]]
  row
}

tasks <- expand.grid(scale_key = c("c100", "c050"), replicate = 1:100, scenario = 1:6, p = c(500L, 1000L),
                     stringsAsFactors = FALSE)
mine <- tasks[(seq_len(nrow(tasks)) - 1L) %% nshards == shard - 1L, , drop = FALSE]
done <- if (file.exists(out)) { d <- read.csv(out, stringsAsFactors = FALSE); paste(d$dataset_id, d$scale_key) } else character(0)
cur <- ""
for (i in seq_len(nrow(mine))) {
  t <- mine[i, ]
  id <- sprintf("p%04d_S%d_r%03d", t$p, t$scenario, t$replicate)
  if (paste(id, t$scale_key) %in% done) next
  if (id != cur) {
    inp <- readRDS(file.path(STUDY, "inputs", sprintf("p%04d", t$p), paste0(id, ".rds")))
    tru <- readRDS(file.path(STUDY, "truth", sprintf("p%04d", t$p), paste0(id, ".rds")))
    cur <- id
  }
  r <- tryCatch(fit_one(inp, tru, t$scale_key), error = function(e) e)
  if (inherits(r, "error")) { message(sprintf("ERROR %s %s: %s", id, t$scale_key, conditionMessage(r))); next }
  write.table(r, out, sep = ",", row.names = FALSE, col.names = !file.exists(out), append = file.exists(out))
  message(sprintf("%s %s fixed_at=%s s3 %.2f last %.2f", id, t$scale_key, r$fixed_at, r$s3_lpS0, r$last_lpS0))
}
