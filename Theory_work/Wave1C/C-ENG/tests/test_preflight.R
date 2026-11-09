# test_preflight.R -- v3.1 LS0 worst-case preflight term (C-GROW cap; HQ_AUDIT A1 finding 1).
# Usage: Rscript test_preflight.R <core_dir> <work_dir> <out_txt>
args <- commandArgs(TRUE); core <- args[1]; work <- args[2]; out <- args[3]
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "ceng_load.R")); ceng_load(core, work, exports = FALSE)
sink(out, split = TRUE)
cat("C-ENG test_preflight.R", format(Sys.time()), "\ncore =", normalizePath(core), "\n\n")
n_pass <- 0; n_fail <- 0
check <- function(name, ok) { ok <- isTRUE(ok); if (ok) n_pass <<- n_pass + 1 else n_fail <<- n_fail + 1; cat(sprintf("  [%s] %s\n", if (ok) "PASS" else "FAIL", name)) }
scenario_covariance <- function(scenario, p) {
  group <- ceiling(seq_len(p)/5); H <- outer(group,group,"=="); I <- diag(p)
  switch(as.integer(scenario), I, 0.5^abs(outer(seq_len(p),seq_len(p),"-")), 0.7*H+0.3*I, 0.85*H+0.15*I,
    0.3*matrix(1,p,p)+0.4*H+0.3*I, {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})
}
pf_both <- function(X, y, alloc) {
  pre <- v3_preprocess(X, y, dup_components = FALSE); b <- v3_budgets(pre$n, pre$p)
  tc <- list(); tf <- function(k) { key <- as.character(k); if (is.null(tc[[key]])) tc[[key]] <<- v3_time_scores(pre$X, pre$y, k); tc[[key]] }
  br <- if (b$exact_branch) "exact" else "smc"
  list(new = v3_preflight(pre$n, pre$p, b, br, alloc, time_fun = tf, ls0_worst_case = TRUE),
       old = v3_preflight(pre$n, pre$p, b, br, alloc, time_fun = tf, ls0_worst_case = FALSE), b = b, n = pre$n, p = pre$p)
}
row <- function(lab, r, alloc) {
  w <- r$new$ls0_worst_case
  data.frame(case = lab, n = r$n, p = r$p, K = r$b$K, ell = r$b$ell, mem_gb = alloc$mem_gb, hours = alloc$hours,
             old_GiB = round(r$old$est_bytes / 2^30, 4), new_GiB = round(r$new$est_bytes / 2^30, 4),
             ls0_scans = w$scans, ls0_requests = w$requests, s_per_score = signif(w$seconds_per_score, 3),
             ls0_est_hours = signif(w$est_seconds / 3600, 3), old_exceeds = r$old$exceeds, new_exceeds = r$new$exceeds)
}
rows <- list()
cat("1. p = 30 regression design (n = 100, S1-S6, replicate 1; the 48 regression datasets share n, p)\n")
for (s in 1:6) {
  set.seed(2300000 + 10000 * s + 1)
  X <- scale(matrix(rnorm(100 * 30), 100) %*% chol(scenario_covariance(s, 30))); y <- drop(X[, 3] - X[, 7] + rnorm(100))
  rows[[length(rows) + 1]] <- row(paste0("p30 S", s), pf_both(X, y, list(mem_gb = 8, hours = 24)), list(mem_gb = 8, hours = 24))
}
cat("2. study sizes, dev generator (Scripts/SMC_BVS/smoke/reference/gen_dev_data.R), n = 200, c100\n")
genv <- new.env(); sys.source(file.path(here, "..", "..", "..", "..", "Scripts", "SMC_BVS", "smoke", "reference", "gen_dev_data.R"), envir = genv)
for (p in c(500L, 1000L)) for (s in 1:6) {
  d <- genv$generate_dev_dataset(p, s, 1L)$inputs
  for (al in list(list(mem_gb = 8, hours = 24), list(mem_gb = 2, hours = 24))) {
    rows[[length(rows) + 1]] <- row(sprintf("p%d S%d", p, s), pf_both(d$X, unname(d$Y[, "c100"]), al), al)
  }
}
tab <- do.call(rbind, rows); print(tab, row.names = FALSE)
newly <- tab[!tab$old_exceeds & tab$new_exceeds, ]
cat("\nFits passing the shipped preflight that the v3.1 preflight would refuse:", nrow(newly), "\n")
if (nrow(newly)) print(newly, row.names = FALSE)
check("p = 30 regression design: preflight passes in both modes at 8 GiB / 24 h", all(!tab$old_exceeds[1:6] & !tab$new_exceeds[1:6]))
d8 <- tab[tab$mem_gb == 8 & tab$p >= 500, ]
check("study sizes p = 500 / 1000 at the default allocation 8 GiB / 24 h: passes in both modes (none newly refused)", all(!d8$old_exceeds) && all(!d8$new_exceeds))
check("LS0 archive term = 2 (ell + K + 1)(4K + 64) bytes; scans = ell + K + 1; requests = scans (p + p^2/4)",
      all(abs(tab$new_GiB - tab$old_GiB - round(2 * tab$ls0_scans * (4 * tab$K + 64) / 2^30, 4)) <= 1e-4) &&
      all(tab$ls0_scans == tab$ell + tab$K + 1) && all(abs(tab$ls0_requests - tab$ls0_scans * (tab$p + tab$p^2 / 4)) < 1e-6))

cat("\n3. public v3_fit: preflight record and switches\n")
set.seed(4001); X <- scale(matrix(rnorm(100 * 30), 100)); y <- drop(X[, 3] - X[, 7] + rnorm(100))
f_new <- v3_fit(X, y, 4001)
options(v3.ls0_cap = "ell_n"); f_cap <- v3_fit(X, y, 4001); options(v3.ls0_cap = NULL)
f_off <- v3_fit(X, y, 4001, ls0 = FALSE)
check("default: preflight carries ls0_worst_case and the ls0_archive memory component; fit completed",
      !is.null(f_new$preflight$ls0_worst_case) && "ls0_archive" %in% names(f_new$preflight$memory_components) && f_new$status == "completed")
check("v3.ls0_cap = 'ell_n' and ls0 = FALSE: preflight identical to the shipped preflight (no LS0 term)",
      identical(f_cap$preflight, f_off$preflight) && is.null(f_off$preflight$ls0_worst_case))
check("the LS0 term does not change the fit outputs (Zhat, PIPs, HPM identical to the ell_n preflight run)",
      identical(f_new$log_Z, f_cap$log_Z) || (identical(f_new$hpm, f_cap$hpm) && identical(f_new$pip_primary, f_cap$pip_primary)))
w <- f_new$preflight$ls0_worst_case
h <- 0.5 * w$est_seconds / 3600
f_ref <- v3_fit(X, y, 4001, allocation = list(mem_gb = 8, hours = h))
options(v3.ls0_cap = "ell_n"); f_ref2 <- v3_fit(X, y, 4001, allocation = list(mem_gb = 8, hours = h)); options(v3.ls0_cap = NULL)
check(sprintf("hours = half the LS0 worst case (%.3g s): refused at preflight (resource_limit, preflight exceeds); not by the shipped preflight",
              h * 3600), identical(f_ref$status, "resource_limit") && isTRUE(f_ref$preflight$exceeds) && !isTRUE(f_ref2$preflight$exceeds))
cat(sprintf("\nTOTAL: %d PASS, %d FAIL\n", n_pass, n_fail))
sink()
