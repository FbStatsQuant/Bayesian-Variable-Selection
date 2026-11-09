# xcheck_n3_tdp.R -- export integer-table instances and the new start_mode results (caps 1 and 1e6) to JSON, for
# comparison with W1-N3's exact-arithmetic reference TDP (Theory_work/Wave1/W1-N3/numerics/tdp.py) by xcheck_n3_tdp.py.
# Usage: Rscript xcheck_n3_tdp.R <core_dir> <work_dir> <out_json> [n] [seed]
args <- commandArgs(TRUE); core <- args[1]; work <- args[2]; out <- args[3]
n_inst <- if (length(args) >= 4) as.integer(args[4]) else 600L
seed <- if (length(args) >= 5) as.integer(args[5]) else 11L
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "ceng_load.R")); ceng_load(core, work)
set.seed(seed)
inst <- vector("list", n_inst)
for (it in seq_len(n_inst)) {
  p <- sample(1:16, 1); perm <- sample(0:(p - 1)); blocks <- list(); i <- 1
  while (i <= p) { m <- min(sample(1:6, 1), p - i + 1); blocks[[length(blocks) + 1]] <- as.integer(sort(perm[i:(i + m - 1)])); i <- i + m }
  K <- sample(0:p, 1)
  flat <- it %% 2 == 0
  lambda <- if (flat) rep(0, K + 1) else as.numeric(sample(-3:1, K + 1, replace = TRUE))
  logr <- lapply(blocks, function(b) {
    v <- if (flat) rep(sample(c(-1, 0, 1), 1), 2^length(b)) else as.numeric(sample(-3:3, 2^length(b), replace = TRUE)); v[1] <- 0
    sz <- vapply(0:(2^length(b) - 1), function(c) sum(bitwAnd(c, 2^(0:(length(b) - 1))) > 0), 0); v[sz > K] <- NaN; v })
  xp <- .v3cpp$t_make_start(p, K, lambda, blocks, logr)
  r1 <- .v3cpp$t_start_mode(xp, 1, TRUE); r6 <- .v3cpp$t_start_mode(xp, 1e6, TRUE)
  inst[[it]] <- list(p = p, K = K, blocks = lapply(blocks, as.list), lam = as.list(as.integer(lambda)),
    rho = lapply(logr, function(v) as.list(ifelse(is.nan(v), 0L, as.integer(v)))),
    new_cap1 = as.list(r1$S), new_cap1e6 = as.list(r6$S), lg0 = r6$lg0)
}
jsonlite::write_json(inst, out, auto_unbox = TRUE, digits = NA)
cat("wrote", n_inst, "instances to", out, "\n")
