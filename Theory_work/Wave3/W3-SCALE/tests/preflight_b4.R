# preflight_b4.R -- tests of the post-setup LS0 preflight of v3.2-dev (leg B item B4; admission only).
# Usage: Rscript --vanilla preflight_b4.R <core_v32dev dir>
core <- commandArgs(trailingOnly = TRUE)[1]
source(file.path(core, "v3.R"))
ok <- TRUE; chk <- function(name, cond) { cat(sprintf("%-78s %s\n", name, if (isTRUE(cond)) "ok" else "FAIL")); if (!isTRUE(cond)) ok <<- FALSE }
# 1. formula with a deterministic time function
b <- list(K = 100, ell = 14); tf <- function(k) 1e-6 * k
r <- v3_preflight_ls0(20000, b, list(hours = 24), 12, tf)
chk("cap = ell + |mode|, scans = cap + 1", r$move_cap == 26 && r$scans == 27)
chk("largest reachable size = min(K, |mode| + cap)", r$max_model_size == 38)
chk("scan bound p + k*(p - k*)", r$scan_size == 20000 + 38 * (20000 - 38))
chk("charge = 2 * scans * scan * s(kmax)", isTRUE(all.equal(r$est_seconds, 2 * 27 * (20000 + 38 * 19962) * 38e-6)))
chk("never above the pre-setup worst case with the same scan rule", r$requests <= (14 + 100 + 1) * (20000 + 100 * 19900))
r2 <- v3_preflight_ls0(60, list(K = 30, ell = 7), list(hours = 24), 25, tf)
chk("size capped by K and by floor(p/2)", r2$max_model_size == 30 && r2$scan_size == 60 + 30 * 30)
r3 <- v3_preflight_ls0(20000, b, list(hours = 24), 12, tf, cap_rule = "ell_n")
chk("ell_n rule: cap = ell", r3$move_cap == 14 && r3$max_model_size == 26)
chk("refusal iff charge > allocation", v3_preflight_ls0(20000, b, list(hours = 1e-6), 12, tf)$exceeds && !r$exceeds)
# 2. the scan bound really bounds a scan: exhaustive count over k <= kmax for small p
cnt <- function(p, k, K) (if (k < K) p else k) + k * (p - k)
worst <- TRUE
for (p in 1:40) for (K in 0:p) for (m in 0:K) for (ell in c(0, 3)) {
  cap <- ell + m; kmax <- min(K, m + cap); ks <- min(kmax, p %/% 2); bound <- p + ks * (p - ks)
  if (any(vapply(0:kmax, function(k) cnt(p, k, K), 0) > bound)) worst <- FALSE
}
chk("p + k*(p - k*) bounds every scan from a centre of size <= kmax (p <= 40)", worst)
# 3. v3_fit: default = post-setup charge, memory verdict as before, record present; tiny allocation refuses after setup
set.seed(1); n <- 60; p <- 40; X <- matrix(rnorm(n * p), n); y <- X[, 3] - X[, 17] + rnorm(n)
f <- v3_fit(X, y, 77, allocation = list(mem_gb = 4, hours = 2))
chk("default fit completes with a preflight_ls0 record", identical(f$status, "completed") && is.list(f$preflight_ls0) && !f$preflight_ls0$exceeds)
chk("record uses the fit's own start mode and cap", f$preflight_ls0$start_mode_size == length(f$start_mode$model) && f$preflight_ls0$move_cap == f$ls0$move_cap)
chk("LS0 stayed within the charged bound", f$ls0$n_evaluated <= f$preflight_ls0$requests && f$ls0$moves <= f$preflight_ls0$move_cap)
chk("initial preflight keeps the LS0 archive in memory and charges no LS0 time", "ls0_archive" %in% names(f$preflight$memory_components) && is.na(f$preflight$ls0_worst_case$est_seconds))
g <- v3_fit(X, y, 77, allocation = list(mem_gb = 4, hours = 1e-9))
chk("tiny allocation: refused after setup, before calibration", identical(g$status, "resource_limit") && isTRUE(g$preflight_ls0$exceeds) && is.null(g$calibration) && !is.null(g$blocks))
options(v3.ls0_preflight = "worst_case")
h <- v3_fit(X, y, 77, allocation = list(mem_gb = 4, hours = 2))
chk("option worst_case: no post-setup record, pre-run charge timed", is.null(h$preflight_ls0) && !is.na(h$preflight$ls0_worst_case$est_seconds))
drop <- c("timings", "runtime_guard", "peak_memory_kb", "preflight", "preflight_ls0", "preflight_escalation", "calibration", "stage_record")
chk("same estimates under both admission rules", identical(f[c("log_Z", "log_Z_r", "pip_primary", "hpm", "hpm_F", "mpm", "score_counts")], h[c("log_Z", "log_Z_r", "pip_primary", "hpm", "hpm_F", "mpm", "score_counts")]))
cat(if (ok) "PREFLIGHT B4 TESTS PASSED\n" else "PREFLIGHT B4 TESTS FAILED\n"); quit(status = if (ok) 0L else 1L)
