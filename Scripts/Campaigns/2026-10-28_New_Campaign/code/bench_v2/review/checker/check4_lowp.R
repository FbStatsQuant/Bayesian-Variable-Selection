# Checker: low-p saved outputs produced by W2 (smoke_output/results/smoke). Own code only.
CAMP <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign"
OUTDIR <- file.path(CAMP, "code/bench_v2/review/checker")
base <- file.path(CAMP, "code/bench_v2/lowp_port/smoke_output/results/smoke")
cases <- c("p0020/p0020_S1_r001_c100", "p0030/p0030_S4_r050_c050",   # the two designated
           "p0020/p0020_S1_r001_c050", "p0030/p0030_S4_r050_c100", "p0030/p0030_S6_r100_c050", "p0030/p0030_S6_r100_c100")  # extras
zz <- file(file.path(OUTDIR, "check4_out.txt"), open = "wt"); sink(zz, split = TRUE)
res <- data.frame(case = character(), check = character(), pass = logical(), detail = character(), stringsAsFactors = FALSE)
rec <- function(case, check, pass, detail = "") {
  pass <- isTRUE(pass); res[nrow(res) + 1L, ] <<- list(case, check, pass, detail)
  cat(sprintf("[%s] %-26s %-60s %s\n", if (pass) "PASS" else "FAIL", case, check, detail))
}
key_of <- function(idx) paste(sort(as.integer(idx)), collapse = ";")
parse_k <- function(key) if (is.na(key)) NA_integer_ else if (!nzchar(key)) integer() else as.integer(strsplit(key, ";", fixed = TRUE)[[1]])
pairs <- list(c("ebic1", "ebic1_K37"), c("ebic05", "ebic05_K37"), c("bic", "bic_K37"))
for (cs in cases) {
  case <- basename(cs); cat("\n====", case, if (cs %in% cases[1:2]) "(designated)" else "(extra)", "====\n")
  R <- lapply(setNames(c("F1", "F2", "F3", "F4", "F5"), c("F1", "F2", "F3", "F4", "F5")), function(m) readRDS(file.path(base, cs, paste0(m, ".rds"))))
  # read input if available (OLS recomputation)
  inp <- R$F1$input$path; X <- y <- NULL
  if (file.exists(inp)) { d <- readRDS(inp); X <- d$X; y <- unname(d$Y[, sub(".*_(c[0-9]+)$", "\\1", case)]) }
  cat("   input file accessible:", !is.null(X), "\n")
  for (m in names(R)) {
    r <- R[[m]]; rows <- r$rows; co <- r$coefficients; p <- if (!is.null(X)) ncol(X) else length(co[[1]]$beta_pen)
    rec(case, sprintf("%s unique rule ids / coef ids match rows", m), !anyDuplicated(rows$rule_id) && identical(names(co), rows$rule_id) && identical(unname(vapply(co, function(z) z$rule_id, "")), rows$rule_id),
        paste(rows$rule_id, collapse = ","))
    # support == nonzeros(beta_pen) for every rule
    ok <- vapply(seq_len(nrow(rows)), function(i) {
      rw <- rows[i, ]; z <- co[[rw$rule_id]]; expected <- if (rw$status == "failed") rw$support_audit else rw$support
      identical(key_of(which(z$beta_pen != 0)), expected) && length(z$beta_pen) == p && all(is.finite(z$beta_pen)) && identical(z$status, rw$status)
    }, TRUE)
    rec(case, sprintf("%s support==nonzeros(beta_pen), all %d rules", m, nrow(rows)), all(ok), paste("status:", paste(unique(rows$status), collapse = ",")))
    # K37 = cap rows
    eq <- c(); det <- c()
    for (pr in pairs) if (all(pr %in% rows$rule_id)) {
      a <- rows[rows$rule_id == pr[1], ]; b <- rows[rows$rule_id == pr[2], ]
      flds <- intersect(c("support", "k", "crit_value", "rss", "lambda", "ebic1_value", "index", "path_index", "status", "k_valid_max"), names(rows))
      same <- all(vapply(flds, function(f) isTRUE(all.equal(a[[f]], b[[f]], tolerance = 0)) || (is.na(a[[f]]) && is.na(b[[f]])), TRUE))
      ca <- co[[pr[1]]]; cb <- co[[pr[2]]]
      same <- same && identical(ca$beta_pen, cb$beta_pen) && identical(ca$beta_ols, cb$beta_ols)
      eq <- c(eq, same); det <- c(det, sprintf("%s=%s(k=%d)", pr[2], same, a$k))
    }
    rec(case, sprintf("%s K37 rows == cap rows (rows+beta_pen+beta_ols)", m), length(eq) >= 2 && all(eq), paste(det, collapse = " "))
    # roles
    rl <- setNames(rows$role, rows$rule_id)
    exp_roles <- if (m %in% c("F1", "F2", "F3")) c(cv_min = "primary", cv_1se = "S0", ebic1 = "secondary", ebic05 = "secondary", ebic1_K37 = "S0", ebic05_K37 = "S0") else
      c(ebic1 = "secondary", ebic05 = "secondary", bic = "secondary", ebic1_K37 = "primary", ebic05_K37 = "S0", bic_K37 = "S0")
    rec(case, sprintf("%s roles per LA-4", m), all(names(exp_roles) %in% names(rl)) && identical(unname(rl[names(exp_roles)]), unname(exp_roles)), paste0(names(rl), ":", rl, collapse = " "))
    rec(case, sprintf("%s exactly one primary row", m), sum(rows$role == "primary") == 1L, rows$rule_id[rows$role == "primary"])
    # OLS refit evidence on EBIC-type rules (needs input)
    if (!is.null(X)) {
      errs <- c()
      for (i in seq_len(nrow(rows))) { rid <- rows$rule_id[i]; z <- co[[rid]]
        if (grepl("^(ebic|bic)", rid) && rows$status[i] != "failed") { idx <- parse_k(rows$support[i]); mine <- rep(0, p)
          if (length(idx)) mine[idx] <- unname(lm.fit(X[, idx, drop = FALSE], y, tol = 1e-10)$coefficients)
          errs <- c(errs, max(abs(z$beta_ols - mine)) / max(1e-300, max(abs(mine)))) } }
      if (length(errs)) rec(case, sprintf("%s beta_ols == own OLS (rel 1e-8), %d rules", m, length(errs)), all(errs <= 1e-8), sprintf("max rel=%.2e", max(errs)))
    }
  }
  # F3-specific: pilot identity at low p; weights; edge sizes
  f3 <- R$F3$fit; f1 <- R$F1$fit
  rec(case, "F3 pilot$beta identical to F1 fit$beta (low-p)", identical(f3$diagnostics$pilot$beta, f1$beta), sprintf("m=%d", sum(f1$beta != 0)))
  v <- f3$diagnostics$v; m <- length(v)
  if (m >= 1) rec(case, "F3 sum(v)==m; v>0", abs(sum(v) - m) <= 1e-10 * m && all(v > 0), sprintf("m=%d", m))
  retired <- c("kappa", "ridge", "ridge_resid_max", "ridge_fold_mse", "kappa_min", "kappa_index", "kappa_boundary", "eps_floor", "n_floored")
  rec(case, "F3 rows: retired ridge fields absent; pilot_* present", !any(retired %in% names(R$F3$rows)) && all(c("pilot_k", "pilot_index", "pilot_lambda") %in% names(R$F3$rows)))
  rec(case, "schema_version == 2 on all five", all(vapply(R, function(r) identical(r$schema_version, 2L), TRUE)))
}
cat("\nSUMMARY: ", sum(res$pass), " PASS / ", sum(!res$pass), " FAIL of ", nrow(res), "\n")
write.csv(res, file.path(OUTDIR, "check4_results.csv"), row.names = FALSE)
sink(); close(zz)
