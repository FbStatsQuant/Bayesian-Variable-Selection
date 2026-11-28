# e1_margin.R -- E1 residual-signal margin kappa / Lambda per setting (population), + E2 Hellinger-scale screening margin.
# Run:  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 GOTO_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
#       nice -n 19 Rscript scripts/e1_margin.R         (16 forked workers; analytic, seconds-minutes)
# Out : tables/e1_margin_by_setting.tsv, tables/e1_rivals_argmin.tsv, tables/e1_greedy_check.tsv, tables/e2_screen_by_setting.tsv
suppressMessages(library(parallel))
args <- commandArgs(FALSE); sf <- sub("--file=", "", args[grep("--file=", args)])
base <- normalizePath(file.path(dirname(sf), ".."))
source(file.path(base, "scripts", "pop_lib.R"))
st <- read_settings(SETTINGS_TSV)
POOLD <- 3; MMAX <- 4

one_setting <- function(i) {
  ps <- setting_pop(st[i, ]); s0 <- ps$s0; sig2 <- ps$sigma2; pr <- ps$price; lp <- log(ps$p)
  rec <- list()
  add <- function(type, D, N, R) {
    d <- length(D); m <- length(N)
    rec[[length(rec) + 1]] <<- data.frame(type = type, d = d, m = m, D = paste(ps$S0[D], collapse = ","),
      N = paste(N, collapse = ","), R = R, kappa = R / (2 * sig2 * d * pr),
      Lambda = 0.5 * R / sig2 - (d - m) * pr - m * lp, Lambda0 = 0.5 * R / sig2 - (d - m) * pr,
      stringsAsFactors = FALSE)
  }
  # (a) single deletions, (b) multi-deletions |D| = 2,3 (exhaustive)
  for (dd in 1:3) { cm <- combn(s0, dd)
    for (k in seq_len(ncol(cm))) add(if (dd == 1) "del1" else paste0("del", dd), cm[, k], integer(0), RS(ps, cm[, k])) }
  # (b') EXTRA (not in brief): deletions of ANY size 4..s0 (exhaustive; includes the empty model S = {})
  for (dd in 4:s0) { cm <- combn(s0, dd); if (is.null(dim(cm))) cm <- matrix(cm, ncol = 1)
    for (k in seq_len(ncol(cm))) add("delall", cm[, k], integer(0), RS(ps, cm[, k])) }
  # (c) swaps: |D| in {1,2}, N greedy from a pool (nulls within POOLD of D), m = 1..MMAX
  gchk <- list()
  for (dd in 1:2) { cm <- combn(s0, dd)
    for (k in seq_len(ncol(cm))) { D <- cm[, k]
      pool <- null_pool(ps, ps$S0[D], POOLD)
      g <- greedy_add(ps, D, pool, MMAX)
      for (m in 1:MMAX) add(paste0("swap", dd), D, g$N[[m + 1]], g$R[m + 1])
      if (dd <= 2) { ex <- exh_add2(ps, D, pool)
        gchk[[length(gchk) + 1]] <- data.frame(setting_id = ps$row$setting_id, D = paste(ps$S0[D], collapse = ","),
          g1 = g$R[2], e1 = ex[2], g2 = g$R[3], e2 = ex[3]) } } }
  rv_full <- do.call(rbind, rec); rv <- rv_full[rv_full$type != "delall", ]     # rv = brief rival class (|D|<=3 deletions, swaps |D|<=2)
  # sigma^2-estimated gain: (n/2) log(1 + R/(sigma2 (n - s0))) replaces 0.5 R/sigma2 (profile-likelihood / Jeffreys-type scale; population version)
  for (nm in c("rv", "rv_full")) { z <- get(nm); z$gain_adj <- (ps$n / 2) * log1p(z$R / (sig2 * (ps$n - s0)))
    z$kappa_adj <- z$gain_adj / (z$d * pr); z$Lambda_adj <- z$gain_adj - (z$d - z$m) * pr - z$m * lp; assign(nm, z) }
  rf <- rv_full; ifull <- which.min(rf$kappa_adj); iLf <- which.min(rf$Lambda_adj)
  # summaries
  kdel <- min(rv$kappa[rv$type == "del1"]); kmul <- min(rv$kappa[rv$type %in% c("del2", "del3")])
  ksw <- min(rv$kappa[grepl("^swap", rv$type)]); kpop <- min(kdel, kmul, ksw)
  ia <- which.min(rv$Lambda); ik <- which.min(rv$kappa)
  idel <- which.min(rv$Lambda[rv$type %in% c("del1", "del2", "del3")])
  sw <- rv[grepl("^swap", rv$type), ]
  lam_swap_min <- min(sw$Lambda); lam_del_min <- min(rv$Lambda[rv$type %in% c("del1", "del2", "del3")])
  # P1 cross-check quantity: population min t^2 over j (single deletions)
  d1 <- rv[rv$type == "del1", ]; t2min <- min(d1$R) / sig2
  # E2: Hellinger-scale screening margin.  For each true j: min over S not containing j, |S| <= s0+4 of Var(x'beta|x_S)/sigma^2.
  # Gaussian monotonicity: S need not keep all of S0\j, so search D containing j (|D|<=3, exhaustive) and N greedy with |N| <= 4+|D|.
  e2 <- numeric(s0); e2arg <- character(s0)
  for (jj in seq_len(s0)) {
    best <- Inf; barg <- ""
    others <- setdiff(seq_len(s0), jj)
    Dlist <- list(jj)
    for (o in others) Dlist[[length(Dlist) + 1]] <- c(jj, o)
    if (s0 >= 3) { cm2 <- combn(others, 2); for (k in seq_len(ncol(cm2))) Dlist[[length(Dlist) + 1]] <- c(jj, cm2[, k]) }
    for (D in Dlist) {
      pool <- null_pool(ps, ps$S0[D], POOLD); nmax <- 4 + length(D)
      g <- greedy_add(ps, D, pool, nmax)
      v <- min(g$R) / ps$n                               # Var(x'beta|x_S), best m <= nmax
      if (v < best) { best <- v; barg <- paste0("D=", paste(ps$S0[D], collapse = ","), ";N=", paste(g$N[[which.min(g$R)]], collapse = ",")) }
    }
    e2[jj] <- best / sig2; e2arg[jj] <- barg
  }
  # E2 "kept-all" variant (S = S0\j + nulls only), for comparison
  e2k <- vapply(seq_len(s0), function(jj) { pool <- null_pool(ps, ps$S0[jj], POOLD); min(greedy_add(ps, jj, pool, 5)$R) / ps$n / sig2 }, 0)
  nn <- ps$n; eps2 <- s0 * lp / nn
  out <- data.frame(setting_id = ps$row$setting_id, suite = ps$row$suite, n = nn, p = ps$p, s0 = s0, rho = ps$rho,
    snr = ps$row$snr, nu = ps$row$nu, beta_type = ps$row$beta_type, sigma2 = sig2, price = pr, two_price = 2 * pr,
    min_t2_pop = t2min, kappa_del = kdel, kappa_multi = kmul, kappa_swap = ksw, kappa_pop = kpop,
    kappa_swap_over_del = ksw / kdel,
    Lambda_min = min(rv$Lambda), Lambda_min_over_logn = min(rv$Lambda) / log(nn),
    nu_crit_empty = (nn - s0) / nn * (exp(2 * s0 * pr / nn) - 1),   # nu at which (n/2)log(1+n nu/(n-s0)) = s0*price: S0 vs the empty model (D = S0)
    nu_pop_setting = ps$vmu / sig2,
    omega_add_per_null = pr - lp, omega_add_over_logn = (pr - lp) / log(nn),   # superset rival S0+{null}: Lambda = m*(price - log p) (no signal term)
    kappa_full = min(rf$kappa), kappa_adj_full = min(rf$kappa_adj), Lambda_full_min_over_logn = min(rf$Lambda) / log(nn), Lambda_adj_full_min_over_logn = min(rf$Lambda_adj) / log(nn),
    kappa_adj_full_arg = paste0(rf$type[ifull], " d=", rf$d[ifull], " m=", rf$m[ifull]), Lambda_adj_full_arg = paste0(rf$type[iLf], " d=", rf$d[iLf], " m=", rf$m[iLf]),
    kappa_adj_pop = min(rv$kappa_adj), Lambda_adj_min = min(rv$Lambda_adj), Lambda_adj_min_over_logn = min(rv$Lambda_adj) / log(nn),
    Lambda_min_type = paste0(rv$type[ia], " d=", rv$d[ia], " m=", rv$m[ia]),
    Lambda_del_min = lam_del_min, Lambda_swap_min = lam_swap_min, Lambda0_min = min(rv$Lambda0),
    kappa_arg = paste0(rv$type[ik], " D=", rv$D[ik], " N=", rv$N[ik]),
    Lambda_arg = paste0(rv$type[ia], " D=", rv$D[ia], " N=", rv$N[ia]),
    e2_min_over_j = min(e2), e2_min_arg = e2arg[which.min(e2)], e2_keepall_min = min(e2k),
    eps2_n = eps2, e2_over_eps2 = min(e2) / eps2, e2_over_logn_n = min(e2) / (log(nn) / nn),
    e2_min_over_j_x_n = min(e2) * nn, e2_dH2 = 1 - (1 + min(e2) / 4)^(-0.5), e2_dH2_over_eps2 = (1 - (1 + min(e2) / 4)^(-0.5)) / eps2, stringsAsFactors = FALSE)
  list(out = out, best = rv[c(ia, ik), ], gchk = do.call(rbind, gchk))
}

res <- mclapply(seq_len(nrow(st)), one_setting, mc.cores = 16, mc.preschedule = FALSE)
if (any(vapply(res, inherits, TRUE, "try-error"))) stop("worker error: ", res[[which(vapply(res, inherits, TRUE, "try-error"))[1]]])
tab <- do.call(rbind, lapply(res, `[[`, "out"))
write_tsv(tab, file.path(base, "tables", "e1_margin_by_setting.tsv"))
gc <- do.call(rbind, lapply(res, `[[`, "gchk"))
gc$greedy_minus_exh_m1 <- gc$g1 - gc$e1; gc$greedy_minus_exh_m2 <- gc$g2 - gc$e2
write_tsv(gc, file.path(base, "tables", "e1_greedy_check.tsv"))
cat("settings:", nrow(tab), " max(greedy-exh) m1:", max(gc$greedy_minus_exh_m1), " m2:", max(gc$greedy_minus_exh_m2), "\n")
