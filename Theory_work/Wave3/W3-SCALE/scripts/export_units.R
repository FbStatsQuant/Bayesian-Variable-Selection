# export_units.R -- R-level exports of one core on raw contexts (review R01 finding 4: cpp_context, cpp_blocks,
# cpp_tables, cpp_neighbours, cpp_setup incl. its numerical-failure return, cpp_dup_components, cpp_cut_group,
# cpp_numerical_routes), hashed element by element. Run once per core; compare the two outputs with
#   Rscript --vanilla export_units.R --compare A.rds B.rds
# Contexts are built from RAW matrices (not preprocessed), so they include what v3_fit can never produce: zero and
# underflowing columns (NaN correlations), NaN and infinite entries, huge duplicated columns (QR route), overflow
# (numerical failure while scoring the tables).
# Usage: Rscript --vanilla export_units.R --core-dir D --out FILE.rds
local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  assign("WS_DIR", if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd(), envir = globalenv())
})
source(file.path(WS_DIR, "ws_common.R"))
args <- commandArgs(trailingOnly = TRUE)
if (length(args) >= 3 && args[1] == "--compare") {
  A <- readRDS(args[2]); B <- readRDS(args[3]); bad <- 0L
  stopifnot(identical(names(A), names(B)), length(A) > 0)
  for (cs in names(A)) {
    nm <- union(names(A[[cs]]), names(B[[cs]]))
    d <- nm[!vapply(nm, function(k) identical(A[[cs]][[k]], B[[cs]][[k]]), TRUE)]
    cat(sprintf("%-22s %2d exports  %s\n", cs, length(nm), if (length(d)) paste("DIFFERENT:", paste(d, collapse = ",")) else "IDENTICAL"))
    bad <- bad + length(d)
  }
  cat(if (bad == 0L) sprintf("EXPORTS IDENTICAL (%d cases)\n", length(A)) else "EXPORTS DIFFER\n")
  quit(status = if (bad == 0L) 0L else 1L)
}
arg <- ws_args(list(core_dir = NA, out = NA))
source(file.path(arg$core_dir, "v3.R"))
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
mk <- function(n, p, seed, rho = 0.5) { set.seed(seed); G <- ceiling(p / 4); f <- matrix(rnorm(n * G), n)
  X <- sqrt(rho) * f[, rep(seq_len(G), each = 4)[seq_len(p)], drop = FALSE] + sqrt(1 - rho) * matrix(rnorm(n * p), n)
  list(X = X, y = drop(X[, 1] - X[, p]) + rnorm(n)) }
nanv <- function(k) { r <- as.raw(c(k %% 256, 0, 0, 0, 0, 0, 0xf8, 0x7f)); readBin(r, "double", endian = "little") }
cases <- list(
  generic = mk(40, 30, 1),
  generic_p130 = mk(60, 130, 2, 0.3),
  duplicates = { d <- mk(50, 36, 3); d$X[, 4] <- d$X[, 3]; d$X[, 20] <- -d$X[, 7]; d$X[, 36] <- d$X[, 1]; d },
  integer = { set.seed(4); X <- matrix(sample(-1:1, 30 * 24, TRUE), 30) + 0; list(X = X, y = X[, 2] - X[, 9] + sample(-2:2, 30, TRUE)) },
  zero_column = list(X = cbind(0, matrix(1, 20, 3)), y = rep(c(-1, 0, 1), length.out = 20)),
  underflow_column = { X <- matrix(rep(c(1, 1, -1, -1), length.out = 20 * 9), 20); for (j in 2:9) X[, j] <- rep(c(1, -1), each = 2, length.out = 20) * (if (j %% 2) 1 else -1)
                       X[, 1] <- rep(c(-1e-200, 1e-200), 10); list(X = X, y = rep(c(-1, 0, 1), length.out = 20)) },
  nan_payload = list(X = sapply(1:12, function(j) rep(nanv(j), 6)), y = rep(1, 6)),
  inf_entry = { d <- mk(30, 20, 5); d$X[3, 2] <- Inf; d$X[9, 11] <- -Inf; d },
  huge_duplicates = { d <- mk(50, 40, 6); d$X[, seq(3, 39, by = 3)] <- d$X[, seq(2, 38, by = 3)]; d$X <- d$X * 1e150; d },
  overflow_failure = { d <- mk(30, 40, 7); d$X[, 37] <- d$X[, 37] * 1e160; d },
  overflow_first = { d <- mk(30, 24, 8); d$X[, 1] <- d$X[, 1] * 1e160; d })
out <- list()
for (cs in names(cases)) {
  X <- cases[[cs]]$X; y <- cases[[cs]]$y; storage.mode(X) <- "double"
  h <- list()
  ctx <- v3_context(X, as.numeric(y), return_gram = TRUE)
  B <- v3_budgets(ctx$n, ctx$p)$B
  h$context <- ws_sha(ctx[setdiff(names(ctx), "ptr")])
  safe <- function(expr) tryCatch(expr, error = function(e) list(error = conditionMessage(e)))
  bl <- safe(v3_blocks(ctx, B)); h$blocks <- ws_sha(bl)
  h$neighbours <- ws_sha(safe(v3_neighbours(ctx, B)))
  h$dup <- ws_sha(safe(.v3cpp$cpp_dup_components(ctx)))
  tb <- if (is.null(bl$error)) safe(v3_tables(ctx, bl)) else list(error = "no blocks"); h$tables <- ws_sha(tb)
  h$routes_after_tables <- ws_sha(.v3cpp$cpp_numerical_routes(ctx))
  if (is.null(bl$error) && is.null(tb$error)) {
    st <- safe(v3_start(ctx, bl, tb)); h$start <- ws_sha(st[setdiff(names(st), "ptr")])
  }
  su <- safe(v3_setup(ctx))
  if (inherits(su, "v3_setup")) {
    h$setup <- ws_sha(list(blocks = su$blocks, tables = su$tables, start = su$start[setdiff(names(su$start), "ptr")], neighbours = su$neighbours, B = su$B))
    h$cut_group <- ws_sha(safe(.v3cpp$cpp_cut_group(su$ptr)))
    h$setup_class <- "v3_setup"
  } else {
    h$setup <- ws_sha(su[setdiff(names(su), c("ctx", "ptr", "seconds"))]); h$setup_class <- paste(class(su), collapse = "/")
  }
  h$routes_after_setup <- ws_sha(.v3cpp$cpp_numerical_routes(ctx))
  h$status <- paste0(h$setup_class, if (!is.null(su$status)) paste0(":", su$status) else "", if (!is.null(tb$error)) " tables:error" else "")
  cat(sprintf("%-18s n=%3d p=%3d B=%2d  %s  routes %s\n", cs, ctx$n, ctx$p, B, h$status, paste(unlist(.v3cpp$cpp_numerical_routes(ctx)), collapse = "/")))
  out[[cs]] <- h
}
saveRDS(out, arg$out)
cat("DONE", length(out), "cases\n")
