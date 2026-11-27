# e1_pool_check.R -- does widening the null pool (distance 3 of D -> 3, 6, 10 of S0) lower the minimum swap R / kappa_swap / Lambda?
# Run: (thread vars exported) nice -n 19 Rscript scripts/e1_pool_check.R   -> tables/e1_pool_check.tsv
suppressMessages(library(parallel))
args <- commandArgs(FALSE); sf <- sub("--file=", "", args[grep("--file=", args)]); base <- normalizePath(file.path(dirname(sf), ".."))
source(file.path(base, "scripts", "pop_lib.R")); st <- read_settings(SETTINGS_TSV)
ids <- c("S1_03", "S1_07", "S2_080", "S2_090", "S2_078", "S2_088", "S2_116", "S2_110", "S2_010", "S2_070", "S2_019", "S2_055")
f <- function(sid) { ps <- setting_pop(st[st$setting_id == sid, ]); out <- list()
  for (pd in list(c("D", 3), c("S0", 3), c("S0", 6), c("S0", 10))) { around <- pd[1]; dist <- as.numeric(pd[2])
    best <- c(kappa = Inf, Lam = Inf, R = Inf, who = NA)
    for (dd in 1:2) { cm <- combn(ps$s0, dd)
      for (k in seq_len(ncol(cm))) { D <- cm[, k]
        pool <- null_pool(ps, if (around == "D") ps$S0[D] else ps$S0, dist); g <- greedy_add(ps, D, pool, 4)
        for (m in 1:4) { R <- g$R[m + 1]; kp <- R / (2 * ps$sigma2 * dd * ps$price); Lm <- 0.5 * R / ps$sigma2 - (dd - m) * ps$price - m * log(ps$p)
          if (kp < best["kappa"]) best[c("kappa", "R")] <- c(kp, R); if (Lm < best["Lam"]) best["Lam"] <- Lm } } }
    out[[length(out) + 1]] <- data.frame(setting_id = sid, pool = paste0("within ", dist, " of ", around), kappa_swap_min = as.numeric(best["kappa"]), Lambda_swap_min = as.numeric(best["Lam"])) }
  do.call(rbind, out) }
r <- do.call(rbind, mclapply(ids, f, mc.cores = 12)); write_tsv(r, file.path(base, "tables", "e1_pool_check.tsv")); print(r, digits = 5)
