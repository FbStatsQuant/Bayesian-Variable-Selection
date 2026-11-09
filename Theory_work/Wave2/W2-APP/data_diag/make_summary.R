# make_summary.R -- builds summary_table.csv and summary_tables.md from out_<name>.rds
nm <- c("riboflavin", "tecator", "iclaims", "fred_qd", "fred_md", "diabetes_quad", "spam", "digits")
nm <- nm[file.exists(sprintf("out_%s.rds", nm))]
g <- function(x, d = 3) ifelse(is.na(x), "NA", formatC(x, digits = d, format = "g"))
rows <- lapply(nm, function(s) {
  r <- readRDS(sprintf("out_%s.rds", s)); sp <- r$sparse; n <- r$n
  at <- function(k, col) { i <- which(sp$k == k); if (length(i)) sp[[col]][i] else NA }
  klog <- ceiling(log(n)); lowr <- function(k) { v <- c(at(k, "gersh_simple"), at(k, "gersh_refined"), if (!is.na(r$lam_minR)) r$lam_minR); if (all(is.na(v))) NA else max(v, na.rm = TRUE) }
  data.frame(name = s, n = n, p = r$p, p_raw = r$p0, dropped_const = r$n_const, dropped_dup = r$n_dup, A_hat = r$Ahat,
    top1 = r$share["top1"], top5 = r$share["top5"], lam1_over_p = r$lam1_over_p, k_factors = r$kfac, ER_max = max(r$ratios), maxr = r$maxr,
    partners05_before = r$partners[2, "median"], partners05_after = r$partners_resid[2, "median"],
    partners03_before = r$partners[1, "median"], partners03_after = r$partners_resid[1, "median"],
    frac03 = r$frac03, frac03_resid = r$frac03_resid, maxr_resid = r$maxr_resid,
    ex_k2 = at(2, "exact"), ex_k3 = at(3, "exact"), ub_k7 = at(7, "upper_best"), k_log = klog, ub_klog = at(klog, "upper_best"),
    lb_k7 = lowr(7), lb_klog = lowr(klog), lam_minR = r$lam_minR,
    msharp1 = r$msharp["s0=1"], msharp3 = r$msharp["s0=3"], msharp2 = r$msharp["s0=2"], msharp5 = r$msharp["s0=5"],
    B = r$blocks$B, nblocks = r$blocks$nblocks, leak_med = r$blocks$leak_q[1], leak_q90 = r$blocks$leak_q[2], leak_max = r$blocks$leak_q[3], split_frac = r$blocks$split_frac,
    seconds = r$seconds, row.names = NULL)
})
T <- do.call(rbind, rows); write.csv(T, "summary_table.csv", row.names = FALSE)
md <- function(df) paste(c(paste0("| ", paste(names(df), collapse = " | "), " |"), paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
  apply(df, 1, function(x) paste0("| ", paste(x, collapse = " | "), " |"))), collapse = "\n")
t1 <- with(T, data.frame(design = name, n, p, `A_hat` = g(A_hat), `top1 share` = g(top1), `top5 share` = g(top5), `lam1/p` = g(lam1_over_p), `#factors (AH ER)` = k_factors, `max ER` = g(ER_max), `max abs r` = g(maxr), check.names = FALSE))
t2 <- with(T, data.frame(design = name, `p_raw` = p_raw, `const/dup dropped` = paste(dropped_const, dropped_dup, sep = "/"), `med partners tau=.5 before` = partners05_before, `after` = partners05_after,
  `med partners tau=.3 before` = partners03_before, `after ` = partners03_after, `frac pairs >.3` = g(frac03), `frac pairs >.3 after` = g(frac03_resid), `max r after` = g(maxr_resid), `null ref max abs r` = g(sqrt(2 * log(p * (p - 1) / 2) / n), 2), check.names = FALSE))
t3 <- with(T, data.frame(design = name, `exact k=2` = g(ex_k2), `exact k=3` = g(ex_k3), `UB k=7` = g(ub_k7), `k=ceil(log n)` = k_log, `UB at that k` = g(ub_klog), `LB k=7` = g(lb_k7), `LB at ceil(log n)` = g(lb_klog), `lambda_min(R) (p<n)` = g(lam_minR), check.names = FALSE))
t4 <- with(T, data.frame(design = name, `m#(s0=1)` = msharp1, `m#(s0=3)` = msharp3, B, `#blocks` = nblocks, `leak median` = g(leak_med), `leak q90` = g(leak_q90), `leak max` = g(leak_max), `split frac(|r|>.5)` = g(split_frac), check.names = FALSE))
writeLines(c("### Table 1 (spectrum)", md(t1), "", "### Table 2 (pairwise structure)", md(t2), "", "### Table 3 (sparse min eigenvalues)", md(t3), "", "### Table 4 (m_sharp, blocks)", md(t4)), "summary_tables.md")
cat(readLines("summary_tables.md"), sep = "\n")

# master table: one row per design, the columns requested in the ticket
tm <- with(T, data.frame(design = name, n, p, `A_hat` = g(A_hat, 3), `top1 / top5 share` = paste(g(top1, 3), g(top5, 3), sep = " / "), `lam1/p` = g(lam1_over_p, 3),
  `#fac` = k_factors, `max abs r` = g(maxr, 3), `med partners tau=.5 (raw -> minus factors)` = paste0(partners05_before, " -> ", partners05_after),
  `phi2 exact k=2 / k=3` = paste(g(ex_k2, 3), g(ex_k3, 3), sep = " / "), `phi2 UB k=7 / k=ceil(log n)` = paste0(g(ub_k7, 3), " / ", g(ub_klog, 3), " (k=", k_log, ")"),
  `phi2 LB at k=ceil(log n)` = g(lb_klog, 3), `m#(s0=1) / m#(s0=3)` = paste(msharp1, msharp3, sep = " / "), B, `#blocks` = nblocks,
  `leak median / max` = paste(g(leak_med, 3), g(leak_max, 3), sep = " / "), check.names = FALSE))
writeLines(c("### Master table", md(tm), "", readLines("summary_tables.md")), "summary_tables.md")
