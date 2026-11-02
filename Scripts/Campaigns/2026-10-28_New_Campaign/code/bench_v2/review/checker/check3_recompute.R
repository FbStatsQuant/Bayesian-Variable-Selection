# Independent recomputation of saved F1/F2/F3 v2 outputs (checker). Own code only; reads RDS, never sources bench_v2 code.
suppressPackageStartupMessages(library(glmnet))
glmnet::glmnet.control(fdev = 0, devmax = 1)
CAMP <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign"
OUTDIR <- file.path(CAMP, "code/bench_v2/review/checker")
INP <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs"
cases <- list(c("dev_p0500_S1_r001", "c100"), c("dev_p1000_S4_r001", "c050"),
              c("dev_p0500_S5_r001", "c050"), c("dev_p1000_S6_r001", "c100"))
logf <- file.path(OUTDIR, "check3_out.txt")
zz <- file(logf, open = "wt"); sink(zz, split = TRUE)
res <- data.frame(case = character(), check = character(), pass = logical(), detail = character(), stringsAsFactors = FALSE)
rec <- function(case, check, pass, detail = "") {
  pass <- isTRUE(pass)
  res[nrow(res) + 1L, ] <<- list(case, check, pass, detail)
  cat(sprintf("[%s] %-9s %-52s %s\n", if (pass) "PASS" else "FAIL", case, check, detail))
}
key_of <- function(idx) paste(sort(as.integer(idx)), collapse = ";")
parse_k <- function(key) if (is.na(key)) NA_integer_ else if (!nzchar(key)) integer() else as.integer(strsplit(key, ";", fixed = TRUE)[[1]])
relmax <- function(a, b) { s <- max(1e-300, abs(b), na.rm = TRUE); max(abs(a - b)) / s }
cv_pick <- function(cvm, cvsd) { imin <- min(which(cvm <= min(cvm))); c(min = imin, one_se = min(which(cvm <= cvm[imin] + cvsd[imin]))) }

for (cs in cases) {
  id <- cs[1]; sc <- cs[2]; case <- paste0(sub("dev_", "", id), "_", sc)
  cat("\n==== ", case, " ====\n")
  r <- readRDS(file.path(CAMP, "code/bench_v2/repro/controlled_2a8362b2f348", paste0(id, "_", sc, ".rds")))
  pkey <- substr(id, 5L, 9L)
  d <- readRDS(file.path(INP, pkey, paste0(id, ".rds")))
  X <- d$X; y <- unname(d$Y[, sc]); n <- nrow(X); p <- ncol(X); foldid <- as.integer(d$foldid)
  F1n <- r$F1$new$result; F1o <- r$F1$old$result; F2n <- r$F2$new$result; F2o <- r$F2$old$result; F3 <- r$F3$result
  rec(case, "input sha matches RDS record", identical(digest::digest(file = file.path(INP, pkey, paste0(id, ".rds")), algo = "sha256"), r$input_sha256), r$input_sha256)

  ## (a) pilot identity
  pb <- F3$diagnostics$pilot$beta
  rec(case, "(a) F3 pilot$beta identical() F1 v2 beta", identical(pb, F1n$beta), sprintf("nonzeros=%d", sum(pb != 0)))
  rec(case, "(a) F3 diagnostics$pilot_beta identical F1 beta", identical(F3$diagnostics$pilot_beta, F1n$beta))
  cvmin1 <- F1n$rules[F1n$rules$rule_id == "cv_min", ]
  rec(case, "(a) pilot_index/lambda/k == F1 cv_min row",
      identical(unique(F3$rules$pilot_index), cvmin1$index) && identical(unique(F3$rules$pilot_k), cvmin1$k) &&
        isTRUE(all.equal(unique(F3$rules$pilot_lambda), cvmin1$lambda, tolerance = 0)),
      sprintf("idx=%d k=%d", cvmin1$index, cvmin1$k))
  rec(case, "(a) F3 pilot$cvm/cvsd identical F1 path cvm/cvsd",
      identical(F3$diagnostics$pilot$cvm, F1n$diagnostics$path$cvm) && identical(F3$diagnostics$pilot$cvsd, F1n$diagnostics$path$cvsd))

  ## (b) support == nonzeros(beta_pen) for all rules, all methods
  for (nm in c("F1", "F2", "F3")) {
    o <- switch(nm, F1 = F1n, F2 = F2n, F3 = F3)
    okb <- vapply(seq_len(nrow(o$rules)), function(i) {
      row <- o$rules[i, ]; co <- o$coefficients[[row$rule_id]]
      expected <- if (row$status == "failed") row$support_audit else row$support
      identical(co$rule_id, row$rule_id) && length(co$beta_pen) == p && identical(key_of(which(co$beta_pen != 0)), expected)
    }, logical(1))
    rec(case, sprintf("(b) %s support==nonzeros(beta_pen) %d rules", nm, nrow(o$rules)), all(okb),
        sprintf("ids=%s statuses=%s", paste(o$rules$rule_id, collapse = ","), paste(o$rules$status, collapse = ",")))
    rec(case, sprintf("(b) %s rule ids/roles", nm),
        identical(o$rules$rule_id, c("cv_min", "cv_1se", "ebic1", "ebic05", "ebic1_K37", "ebic05_K37")) &&
          identical(o$rules$role, if (nm == "F3" || TRUE) c("primary", rep("S0", 5)) else NULL), paste(o$rules$role, collapse = ","))
  }

  ## (c) EBIC recomputation from scratch for the F3 path supports (FULL design)
  path <- F3$diagnostics$path
  keys <- unique(c("", path$key))
  ks <- vapply(keys, function(k) length(parse_k(k)), 0L)
  keep_c <- ks <= 100L
  keys <- keys[keep_c]; ks <- ks[keep_c]
  fit_one <- function(k) { idx <- parse_k(k); if (!length(idx)) return(c(sum(y^2), 0)); z <- lm.fit(X[, idx, drop = FALSE], y, tol = 1e-10); c(sum(z$residuals^2), z$rank) }
  ff <- t(vapply(keys, fit_one, c(0, 0)))
  rss <- ff[, 1]; rk <- ff[, 2]
  valid <- rk == ks & is.finite(rss) & rss > 0
  base <- n * log(rss / n) + ks * log(n)
  e1 <- ifelse(valid, base + 2 * 1 * lchoose(p, ks), Inf); e05 <- ifelse(valid, base + 2 * 0.5 * lchoose(p, ks), Inf)
  mycand <- data.frame(key = keys, k = ks, rss = rss, valid = valid, ebic1 = e1, ebic05 = e05, stringsAsFactors = FALSE)
  sc_cand <- F3$diagnostics$candidates
  rec(case, "(c) candidate key set == saved (null+distinct, k<=100)", setequal(mycand$key, sc_cand$key) && nrow(mycand) == nrow(sc_cand),
      sprintf("n_cand=%d (mine) / %d (saved); path max k=%d", nrow(mycand), nrow(sc_cand), max(path$k)))
  mm <- match(mycand$key, sc_cand$key)
  rec(case, "(c) candidate rss/ebic1/ebic05 vs saved (rel 1e-9)",
      relmax(mycand$rss, sc_cand$rss[mm]) < 1e-9 && relmax(mycand$ebic1[is.finite(mycand$ebic1)], sc_cand$ebic1[mm][is.finite(mycand$ebic1)]) < 1e-9 &&
        identical(is.finite(mycand$ebic1), is.finite(sc_cand$ebic1[mm])) && relmax(mycand$ebic05[is.finite(mycand$ebic05)], sc_cand$ebic05[mm][is.finite(mycand$ebic05)]) < 1e-9,
      sprintf("rel rss=%.2e rel ebic1=%.2e; n_invalid=%d", relmax(mycand$rss, sc_cand$rss[mm]), relmax(mycand$ebic1[is.finite(mycand$ebic1)], sc_cand$ebic1[mm][is.finite(mycand$ebic1)]), sum(!mycand$valid)))
  # screened-m EBIC (the known W2 slip) would give different criterion: informational
  m_pilot <- sum(pb != 0)
  e1_wrong <- ifelse(valid, base + 2 * lchoose(m_pilot, ks), Inf)
  for (rid in c("ebic1", "ebic05", "ebic1_K37", "ebic05_K37")) {
    col <- sub("_K37$", "", rid); el <- if (grepl("K37", rid)) mycand[mycand$k <= floor(n / log(n)), ] else mycand
    j <- order(el[[col]], el$k, el$key, method = "radix")[1]
    row <- F3$rules[F3$rules$rule_id == rid, ]
    occ <- which(path$key == el$key[j] & path$kkt_full <= 1e-5); occ_any <- which(path$key == el$key[j])
    idx <- if (length(occ)) occ[1] else if (length(occ_any)) occ_any[1] else NA_integer_
    vmax <- max(el$k[el$valid])
    ok <- identical(row$support, el$key[j]) && row$k == el$k[j] && isTRUE(abs(row$crit_value - el[[col]][j]) <= 1e-9 * abs(el[[col]][j])) &&
      isTRUE(abs(row$rss - el$rss[j]) <= 1e-9 * el$rss[j]) && isTRUE(abs(row$ebic1_value - el$ebic1[j]) <= 1e-9 * abs(el$ebic1[j])) &&
      identical(row$k_valid_max, as.integer(vmax)) && identical(row$index, idx) &&
      isTRUE(abs(row$lambda - path$lambda[idx]) <= 1e-12 * path$lambda[idx]) &&
      identical(grepl("ebic_at_largest", row$diag_codes), el$k[j] == vmax) && identical(row$k_path_max, as.integer(max(path$k)))
    rec(case, sprintf("(c) re-pick %s (order crit,k,key)", rid), ok,
        sprintf("mine key_k=%d crit=%.6f | saved k=%d crit=%.6f | index %s/%s | vmax %d/%d | status=%s", el$k[j], el[[col]][j], row$k, row$crit_value, idx, row$index, vmax, row$k_valid_max, row$status))
  }
  # tie / negative control: screened-m pick (informational)
  j_ok <- order(mycand$ebic1[mycand$k <= 37], mycand$k[mycand$k <= 37], mycand$key[mycand$k <= 37], method = "radix")[1]
  j_bad <- order(e1_wrong[mycand$k <= 37], mycand$k[mycand$k <= 37], mycand$key[mycand$k <= 37], method = "radix")[1]
  cat("   info: ebic1_K37 pick with p=ncol(X) k=", mycand$k[mycand$k <= 37][j_ok], " ; with screened m=", m_pilot, " instead of p: k=", mycand$k[mycand$k <= 37][j_bad],
      if (j_ok != j_bad) "  (differs: p-vs-m matters here)" else "  (same)", "\n", sep = "")

  ## (d) beta_ols
  for (nm in c("F1", "F2", "F3")) {
    o <- switch(nm, F1 = F1n, F2 = F2n, F3 = F3)
    errs <- c(); cvna <- TRUE; offs <- TRUE; plen <- TRUE
    for (i in seq_len(nrow(o$rules))) {
      row <- o$rules[i, ]; co <- o$coefficients[[row$rule_id]]
      if (startsWith(row$rule_id, "ebic")) {
        idx <- parse_k(if (row$status == "failed") row$support_audit else row$support)
        mine <- rep(0, p); if (length(idx)) mine[idx] <- unname(lm.fit(X[, idx, drop = FALSE], y, tol = 1e-10)$coefficients)
        errs <- c(errs, max(abs(co$beta_ols - mine)) / max(1e-300, max(abs(mine))))
        offs <- offs && all(co$beta_ols[setdiff(seq_len(p), idx)] == 0)
      } else cvna <- cvna && all(is.na(co$beta_ols)) && length(co$beta_ols) == p
      plen <- plen && length(co$beta_pen) == p && all(is.finite(co$beta_pen))
    }
    rec(case, sprintf("(d) %s beta_ols == own OLS slopes (rel 1e-8)", nm), all(errs <= 1e-8) && cvna && offs && plen,
        sprintf("max rel=%.2e over %d ebic rules; CV beta_ols all-NA=%s; off-support zeros=%s", max(errs), length(errs), cvna, offs))
  }
  rec(case, "(d) alpha field: F1/F3 NA, F2 non-NA", all(vapply(F1n$coefficients, function(z) is.na(z$alpha), TRUE)) && all(vapply(F3$coefficients, function(z) is.na(z$alpha), TRUE)) &&
        all(vapply(F2n$coefficients, function(z) is.finite(z$alpha), TRUE)))

  ## (e) F1/F2 original 4 rules identical to deployed run in same RDS
  for (nm in c("F1", "F2")) {
    on <- switch(nm, F1 = F1n, F2 = F2n); oo <- switch(nm, F1 = F1o, F2 = F2o)
    four <- c("cv_min", "cv_1se", "ebic1", "ebic05")
    newr <- on$rules[match(four, on$rules$rule_id), ]; oldr <- oo$rules
    rownames(newr) <- NULL; rownames(oldr) <- NULL
    colid <- all(vapply(names(oldr), function(cn) identical(newr[[cn]], oldr[[cn]]), TRUE))
    rec(case, sprintf("(e) %s 4 original rule rows identical (every old col)", nm), identical(oldr$rule_id, four) && colid && all(names(oldr) %in% names(on$rules)),
        sprintf("old cols=%d new cols=%d new-only cols=%s", ncol(oldr), ncol(on$rules), paste(setdiff(names(on$rules), names(oldr)), collapse = ",")))
    rec(case, sprintf("(e) %s beta/converged identical", nm), identical(on$beta, oo$beta) && identical(on$converged, oo$converged))
    rec(case, sprintf("(e) %s diagnostics identical (path/folds/candidates...)", nm), identical(on$diagnostics, oo$diagnostics))
    rec(case, sprintf("(e) %s old run has no coefficients; v2 has", nm), is.null(oo$coefficients) && !is.null(on$coefficients))
    k37 <- on$rules[on$rules$rule_id %in% c("ebic1_K37", "ebic05_K37"), ]
    rec(case, sprintf("(e) %s K37 roles S0, k<=37", nm), all(k37$role == "S0") && all(k37$k <= 37L), paste(k37$k, collapse = ","))
  }

  ## (f) weights
  keep <- F3$diagnostics$keep; v <- F3$diagnostics$v; w <- F3$diagnostics$w; m <- length(keep)
  rec(case, "(f) keep == which(pilot b != 0); m == pilot_k", identical(as.integer(keep), which(pb != 0)) && m == unique(F3$rules$pilot_k), sprintf("m=%d", m))
  rec(case, "(f) sum(v)==m (1e-10 rel)", abs(sum(v) - m) <= 1e-10 * m, sprintf("sum(v)-m=%.3e", sum(v) - m))
  rec(case, "(f) v>0 finite; v*|b_keep| constant (rel 1e-12)", all(is.finite(v)) && all(v > 0) && (max(v * abs(pb[keep])) - min(v * abs(pb[keep]))) / max(v * abs(pb[keep])) < 1e-12,
      sprintf("spread=%.2e", (max(v * abs(pb[keep])) - min(v * abs(pb[keep]))) / max(v * abs(pb[keep]))))
  rec(case, "(f) w == 1/|b_keep| (gamma=1)", relmax(w, 1 / abs(pb[keep])) < 1e-14, sprintf("rel=%.2e", relmax(w, 1 / abs(pb[keep]))))
  rr <- (1 / abs(pb[keep])); rr <- rr / max(rr); vmine <- m * rr / sum(rr)
  rec(case, "(f) v == own stable normalisation m*r/sum(r)", relmax(v, vmine) < 1e-14, sprintf("rel=%.2e", relmax(v, vmine)))

  ## Extra: independent second stage (glmnet on screened problem) -> path, CV, index, beta_pen at index, KKT
  Xk <- X[, keep, drop = FALSE]
  zk <- abs(drop(crossprod(Xk, y))) / n
  lam <- 1.01 * max(zk / v) * exp(seq(0, log(1e-4), length.out = 200L))
  rec(case, "(x) lambda grid == own (rel 1e-12)", relmax(lam, path$lambda) < 1e-12, sprintf("rel=%.2e", relmax(lam, path$lambda)))
  g <- function(Xd, yd) as.matrix(glmnet(Xd, yd, family = "gaussian", alpha = 1, lambda = lam, penalty.factor = v, intercept = FALSE,
                                         standardize = FALSE, type.gaussian = "naive", thresh = 1e-16, maxit = 1e7)$beta)
  Bf <- g(Xk, y); L <- length(lam)
  oof <- matrix(NA_real_, n, L)
  for (k in 1:10) { te <- foldid == k; oof[te, ] <- Xk[te, , drop = FALSE] %*% g(Xk[!te, , drop = FALSE], y[!te]) }
  nk <- tabulate(foldid, 10); mse <- t(vapply(1:10, function(k) colMeans((y[foldid == k] - oof[foldid == k, , drop = FALSE])^2), numeric(L)))
  cvm <- drop(nk %*% mse) / n; cvsd <- sqrt(drop(nk %*% sweep(mse, 2, cvm)^2) / n / 9)
  rec(case, "(x) own CV cvm/cvsd vs saved path (rel 1e-8)", relmax(cvm, path$cvm) < 1e-8 && relmax(cvsd, path$cvsd) < 1e-6, sprintf("rel cvm=%.2e cvsd=%.2e", relmax(cvm, path$cvm), relmax(cvsd, path$cvsd)))
  ch <- cv_pick(cvm, cvsd)
  rec(case, "(x) own cv_min/cv_1se index == saved", identical(unname(ch[["min"]]), F3$rules$index[1]) && identical(unname(ch[["one_se"]]), F3$rules$index[2]), sprintf("own %d/%d saved %d/%d", ch[["min"]], ch[["one_se"]], F3$rules$index[1], F3$rules$index[2]))
  # beta_pen at index for all six rules
  errb <- c(); suppm <- c()
  for (i in 1:6) {
    row <- F3$rules[i, ]; co <- F3$coefficients[[row$rule_id]]
    full <- rep(0, p); full[keep] <- Bf[, row$index]
    errb <- c(errb, max(abs(full - co$beta_pen)) / max(1e-300, max(abs(full)))); suppm <- c(suppm, identical(key_of(which(full != 0)), row$support))
  }
  rec(case, "(x) own glmnet beta at index == saved beta_pen (6 rules)", all(errb < 1e-8) && all(suppm), sprintf("max rel=%.2e supports match=%s", max(errb), all(suppm)))
  # own KKT for weighted screened problem at selected indices
  kk <- sapply(unique(F3$rules$index), function(i) { b <- Bf[, i]; gr <- crossprod(Xk, y - Xk %*% b) / n; act <- b != 0
    viol <- pmax(abs(gr) - lam[i] * v, 0); viol[act] <- abs(gr[act] - lam[i] * v[act] * sign(b[act])); max(viol) / max(1, max(zk)) })
  rec(case, "(x) own KKT (weighted, screened) <=1e-5 at selected idx", all(kk <= 1e-5), sprintf("max=%.2e", max(kk)))
  # path supports vs own glmnet path
  mykeys <- vapply(seq_len(L), function(j) key_of(keep[which(Bf[, j] != 0)]), "")
  rec(case, "(x) own path supports == saved path$key (all 200)", identical(mykeys, path$key), sprintf("mismatches=%d", sum(mykeys != path$key)))
  rm(Bf, oof)
  gc(verbose = FALSE)
}
cat("\nSUMMARY: ", sum(res$pass), " PASS / ", sum(!res$pass), " FAIL of ", nrow(res), "\n")
write.csv(res, file.path(OUTDIR, "check3_results.csv"), row.names = FALSE)
sink(); close(zz)
