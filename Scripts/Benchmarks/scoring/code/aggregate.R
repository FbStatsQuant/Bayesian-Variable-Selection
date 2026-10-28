# aggregate.R: aggregate tables T1–T6 and the S-tables of master §IV.1.3 for one scored run
# (thread S, 2026-10-19). Reads the outputs of score.R from --dir and writes the tables there.
#
# Usage: Rscript --vanilla aggregate.R --dir <score output dir>
#
# Denominators (§IV.1.3): the number of expected cases per cell (100 per (p, scenario) in
# production, 600 pooled per p). Failed, timed-out, not-run and missing fits count as
# non-recovery and are reported in T2. "Exact among successful" is a secondary column.
# Passing-only counts exclude fits with diag_flag = TRUE; their denominator stays the same.
# Mean FP and FN (T3) are over successful rows (status ok or warning); n_success is given.

find_code_dir <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
}
if (!exists("REGISTRY")) source(file.path(find_code_dir(), "registry.R"))

read_scored <- function(dir) {
  s <- utils::read.csv(file.path(dir, "scored_rows.csv"), colClasses = "character", na.strings = "NA")
  s$p <- as.integer(s$p)
  s$scenario <- as.integer(s$scenario)
  for (cc in c("tp", "fp", "fn", sprintf("sel_a%02d", 1:14))) s[[cc]] <- as.integer(s[[cc]])
  s$exact <- as.logical(s$exact)
  s$flagged <- s$diag_flag == "TRUE"
  s$runtime_s <- as.numeric(s$runtime_s)
  for (cc in c("p", "scenario", "case_id", "method_id", "rule_id", "status", "diag_flag", "error_type", "exact"))
    if (any(is.na(s[[cc]]))) stop("scored rows with NA ", cc, ": fix the scoring problems first")
  if (!all(s$status %in% STATUS_VALUES)) stop("scored rows with an invalid status")
  if (!all(s$diag_flag %in% c("TRUE", "FALSE"))) stop("scored rows with an invalid diag_flag")
  if (any(is.na(s$exact))) stop("scored rows with exact = NA")
  s
}

code_list <- function(x) if (is.na(x) || x == "") character(0) else strsplit(x, ";", fixed = TRUE)[[1]]

# One summary row for a set of rule rows and its expected-case denominator.
summarise_cell <- function(r, n_expected) {
  succ <- !(r$status %in% FAILED_STATUSES)
  n_success <- sum(succ)
  data.frame(
    n_expected = n_expected,
    n_rows = nrow(r),
    n_missing = n_expected - nrow(r),
    n_failed = sum(r$status == "failed"),
    n_timeout = sum(r$status == "timeout"),
    n_not_run = sum(r$status == "not_run"),
    n_fail_total = sum(!succ) + (n_expected - nrow(r)),
    n_success = n_success,
    n_flagged = sum(r$flagged),
    exact_all = sum(r$exact),
    exact_passing = sum(r$exact & !r$flagged),
    exact_among_success = if (n_success > 0) sum(r$exact) / n_success else NA_real_,
    sum_fp = sum(r$fp[succ]),
    sum_fn = sum(r$fn[succ]),
    mean_fp = if (n_success > 0) sum(r$fp[succ]) / n_success else NA_real_,
    mean_fn = if (n_success > 0) sum(r$fn[succ]) / n_success else NA_real_,
    err_exact = sum(r$error_type == "exact"),
    err_extra_only = sum(r$error_type == "extra_only"),
    err_missed_only = sum(r$error_type == "missed_only"),
    err_mixed = sum(r$error_type == "mixed"),
    err_failed = sum(r$error_type == "failed"),
    stringsAsFactors = FALSE)
}

# Rules of a method present in the scored rows: registered first, then any derived rules.
rules_present <- function(s, m) rules_of(m, any(s$method_id == m & s$rule_id %in% DERIVED_REGISTRY[[m]]$rules))

# k_gt_K: successful rows whose selected k exceeds K = 37, for every rule of the F families
# (PREREG_c050 R1, CV rules included) and for size rules (EBIC, BIC, SIC) anywhere; NA otherwise.
count_k_gt_K <- function(r, rule, method_id) {
  if (!(method_id %in% F_FAMILY) && !grepl(SIZE_RULE_PATTERN, rule)) return(NA_integer_)
  sum(!(r$status %in% FAILED_STATUSES) & !is.na(r$k) & as.integer(r$k) > K_SIZE_BOUND)
}

# The long table: one row per (method_id, rule_id, p, scenario) plus the pooled row per p.
rules_long <- function(s, coverage) {
  out <- list()
  scale_key <- unique(s$scale_key)
  for (m in unique(coverage$method_id)) {
    reg <- rules_present(s, m)
    for (j in seq_along(reg$rules)) {
      for (p in sort(unique(coverage$p))) {
        for (sc in c(sort(unique(coverage$scenario)), NA)) {
          cov_cell <- coverage[coverage$method_id == m & coverage$p == p & (is.na(sc) | coverage$scenario == sc), ]
          r <- s[which(s$method_id == m & s$rule_id == reg$rules[j] & s$p == p & (is.na(sc) | s$scenario == sc)), ]
          row <- cbind(data.frame(method_id = m, rule_id = reg$rules[j], role = reg$roles[j],
                                  label = rule_label(m, reg$rules[j], scale_key), p = p,
                                  scenario = if (is.na(sc)) "pooled" else as.character(sc), stringsAsFactors = FALSE),
                       summarise_cell(r, nrow(cov_cell)), n_k_gt_K = count_k_gt_K(r, reg$rules[j], m))
          out[[length(out) + 1]] <- row
        }
      }
    }
  }
  do.call(rbind, out)
}

# T4: selection frequency of each active variable under the primary rule.
t4_tables <- function(s, coverage, signals) {
  # Group labels as one-decimal strings (β and ρ have one decimal by design, §II.3, §II.4), so that
  # floating-point noise such as 0.4 + 0.3 = 0.70000000000000007 cannot split a group.
  block <- (signals$index - 1L) %/% 5L + 1L
  signals$abs_beta <- sprintf("%.1f", abs(signals$beta))
  signals$rho_S6 <- sprintf("%.1f", 0.4 + 0.1 * ((block - 1L) %% 6L))  # §II.4 S6: ρ_b = 0.4 + 0.1·((b − 1) mod 6)
  stopifnot(all(abs(abs(signals$beta) - as.numeric(signals$abs_beta)) < 1e-12))
  by_var <- list()
  for (m in unique(coverage$method_id)) {
    reg <- rules_present(s, m)
    prims <- reg$rules[reg$roles == "primary"]
    if (!length(prims)) prims <- reg$rules[reg$roles == "S1"][1]   # S1 method ids have no primary rule
    for (prim in prims) for (p in sort(unique(coverage$p))) {
      for (sc in c(sort(unique(coverage$scenario)), NA)) {
        n_exp <- nrow(coverage[coverage$method_id == m & coverage$p == p & (is.na(sc) | coverage$scenario == sc), ])
        r <- s[which(s$method_id == m & s$rule_id == prim & s$p == p & (is.na(sc) | s$scenario == sc)), ]
        sg <- signals[signals$p == p, ]
        for (k in seq_len(nrow(sg))) {
          col <- sprintf("sel_a%02d", k)
          by_var[[length(by_var) + 1]] <- data.frame(
            method_id = m, rule_id = prim, p = p, scenario = if (is.na(sc)) "pooled" else as.character(sc),
            signal = sg$signal[k], index = sg$index[k], beta = sg$beta[k], abs_beta = sg$abs_beta[k],
            rho_S6 = sg$rho_S6[k], n_selected = sum(r[[col]] == 1L, na.rm = TRUE), n_expected = n_exp,
            stringsAsFactors = FALSE)
        }
      }
    }
  }
  by_var <- do.call(rbind, by_var)
  key <- c("method_id", "rule_id", "p", "scenario", "abs_beta", "rho_S6")
  g <- unique(by_var[, key])
  g$n_signals <- NA_integer_; g$n_selected <- NA_integer_; g$n_opportunities <- NA_integer_
  for (i in seq_len(nrow(g))) {
    sel <- Reduce(`&`, lapply(key, function(k) by_var[[k]] == g[[k]][i]))
    g$n_signals[i] <- sum(sel)
    g$n_selected[i] <- sum(by_var$n_selected[sel])
    g$n_opportunities[i] <- sum(by_var$n_expected[sel])
  }
  g$rate <- g$n_selected / g$n_opportunities
  list(by_variable = by_var, by_group = g)
}

# T5: runtime of each fit (shared by its rules), per (p, method_id).
t5_table <- function(s) {
  fits <- s[!duplicated(paste(s$case_id, s$method_id)), ]
  out <- list()
  for (m in unique(fits$method_id)) for (p in sort(unique(fits$p))) {
    x <- fits$runtime_s[fits$method_id == m & fits$p == p]
    x <- x[!is.na(x)]
    out[[length(out) + 1]] <- data.frame(
      method_id = m, p = p, n_fits_with_runtime = length(x),
      median_s = if (length(x)) stats::median(x) else NA_real_,
      p95_s = if (length(x)) unname(stats::quantile(x, 0.95, type = 7)) else NA_real_,
      max_s = if (length(x)) max(x) else NA_real_, stringsAsFactors = FALSE)
  }
  do.call(rbind, out)
}

# T6 and the code summaries: per (method_id, rule_id, p, scenario) status, convergence, flag and
# code counts. Codes are counted per rule row; flag codes are fit-wide, so they repeat on each rule.
t6_tables <- function(s, coverage) {
  t6 <- list(); codes <- list()
  all_codes <- c(FLAG_CODES, INFO_CODES)
  for (m in unique(coverage$method_id)) {
    reg <- rules_present(s, m)
    for (rule in reg$rules) for (p in sort(unique(coverage$p))) {
      for (sc in c(sort(unique(coverage$scenario)), NA)) {
        r <- s[which(s$method_id == m & s$rule_id == rule & s$p == p & (is.na(sc) | s$scenario == sc)), ]
        cl <- lapply(r$diag_codes, code_list)
        cnt <- vapply(all_codes, function(cd) sum(vapply(cl, function(v) cd %in% v, TRUE)), 0L)
        sc_lab <- if (is.na(sc)) "pooled" else as.character(sc)
        t6[[length(t6) + 1]] <- data.frame(
          method_id = m, rule_id = rule, p = p, scenario = sc_lab, n_rows = nrow(r),
          status_ok = sum(r$status == "ok"), status_warning = sum(r$status == "warning"),
          status_failed = sum(r$status == "failed"), status_timeout = sum(r$status == "timeout"),
          status_not_run = sum(r$status == "not_run"),
          converged_true = sum(r$converged %in% "TRUE"), converged_false = sum(r$converged %in% "FALSE"),
          converged_na = sum(is.na(r$converged)), diag_flag_true = sum(r$flagged),
          ebic_at_largest = unname(cnt["ebic_at_largest"]), k_gt_K = count_k_gt_K(r, rule, m), stringsAsFactors = FALSE)
        codes[[length(codes) + 1]] <- data.frame(method_id = m, rule_id = rule, p = p, scenario = sc_lab,
                                                 code = all_codes, kind = ifelse(all_codes %in% FLAG_CODES, "flag", "info"),
                                                 count = unname(cnt), stringsAsFactors = FALSE)
      }
    }
  }
  list(t6 = do.call(rbind, t6), codes = do.call(rbind, codes))
}

fmt_rate <- function(x, n) paste0(x, "/", n)

md_table <- function(df) {
  c(paste0("| ", paste(names(df), collapse = " | "), " |"),
    paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
    apply(df, 1, function(r) paste0("| ", paste(r, collapse = " | "), " |")))
}

write_summary <- function(dir, run_id, long, t5, t6, codes, coverage, problems, log) {
  L <- c(paste0("# Scoring summary: ", run_id), "",
         if (nrow(problems) > 0 && any(!problems$check %in% NONBLOCKING_CHECKS))
           c("**UNRESOLVED SCORING PROBLEMS: aggregated with --allow-problems; see problems.csv.**", "") else NULL,
         "Provisional: scoring and method code are AI-written and unreviewed (G5, G9 pending).", "",
         "## Coverage and checks", "", paste0("- ", log), "")
  pc <- if (nrow(problems)) table(problems$check) else integer(0)
  L <- c(L, if (length(pc)) paste0("- problem `", names(pc), "`: ", as.integer(pc)) else "- problems: none", "")
  for (m in unique(long$method_id)) {
    lm <- long[long$method_id == m, ]
    L <- c(L, paste0("## ", m), "", "Exact recovery, all-saved (passing-only in brackets where any fit is flagged; failures = failed + timeout + not_run + missing):", "")
    tab <- unique(lm[, c("p", "scenario")])
    for (rule in unique(lm$rule_id)) {
      x <- lm[lm$rule_id == rule, ]
      lab <- paste0(rule, " (", x$role[1], ")")
      tab[[lab]] <- ifelse(x$n_flagged > 0, paste0(fmt_rate(x$exact_all, x$n_expected), " [", x$exact_passing, "]"),
                           fmt_rate(x$exact_all, x$n_expected))
    }
    prim <- lm[lm$rule_id == unique(lm$rule_id)[1], ]
    tab$failures <- prim$n_fail_total
    tab$flagged <- prim$n_flagged
    L <- c(L, md_table(tab), "")
    pr <- lm[lm$rule_id == unique(lm$rule_id)[1], ]
    t3 <- data.frame(p = pr$p, scenario = pr$scenario, mean_FP = sprintf("%.2f", pr$mean_fp), mean_FN = sprintf("%.2f", pr$mean_fn),
                     exact = pr$err_exact, extra_only = pr$err_extra_only, missed_only = pr$err_missed_only,
                     mixed = pr$err_mixed, failed = pr$err_failed, missing = pr$n_missing)
    L <- c(L, paste0("T3 for `", pr$rule_id[1], "`:"), "", md_table(t3), "")
    caps <- t6[t6$method_id == m & t6$scenario == "pooled", c("rule_id", "p", "ebic_at_largest", "n_rows")]
    if (any(caps$ebic_at_largest > 0)) L <- c(L, "Cap hits (`ebic_at_largest`, pooled per p):", "", md_table(caps), "")
    cd <- codes[codes$method_id == m & codes$scenario == "pooled" & codes$count > 0, c("rule_id", "p", "code", "kind", "count")]
    L <- c(L, "Diagnostic codes (pooled per p, rows carrying the code):", "",
           if (nrow(cd)) md_table(cd) else "none", "")
    rt <- t5[t5$method_id == m, ]
    rt$median_s <- signif(rt$median_s, 3); rt$p95_s <- signif(rt$p95_s, 3); rt$max_s <- signif(rt$max_s, 3)
    L <- c(L, "T5 runtime (s, whole wrapper call, one value per fit; p95 = type-7 quantile):", "", md_table(rt), "")
  }
  writeLines(L, file.path(dir, "summary.md"))
}

NONBLOCKING_CHECKS <- c("case_missing", "case_incomplete", "missing_rule_row")

aggregate_run <- function(dir, allow_problems = FALSE) {
  s <- read_scored(dir)
  coverage <- utils::read.csv(file.path(dir, "coverage.csv"), stringsAsFactors = FALSE)
  coverage$p <- as.integer(coverage$p); coverage$scenario <- as.integer(coverage$scenario)
  problems <- utils::read.csv(file.path(dir, "problems.csv"), colClasses = "character")
  signals <- utils::read.csv(file.path(dir, "truth_signals.csv"), stringsAsFactors = FALSE)
  log <- readLines(file.path(dir, "score_log.txt"))
  run_id <- sub("^run_id: ", "", log[1])
  # Every problem blocks except coverage gaps, which the denominators handle (missing = non-recovery).
  blocking <- setdiff(unique(problems$check), NONBLOCKING_CHECKS)
  if (length(blocking) && !allow_problems) stop("aggregation refused, scoring problems: ", paste(blocking, collapse = ", "))

  long <- rules_long(s, coverage)
  if (any(long$n_missing < 0)) stop("negative n_missing: rows outside the expected cases")
  if (any(log == paste("expect: prod |", paste("p:", paste(sort(unique(coverage$p)), collapse = ","))))) {
    cells <- long[long$scenario != "pooled", ]
    if (any(cells$n_expected != REPLICATES_PER_CELL)) stop("production cell without ", REPLICATES_PER_CELL, " expected cases")
  }
  write_table(long, file.path(dir, "rules_long.csv"))

  # T1: every primary row (pre-declared and, with derived rows, F4/F5 ebic1_K37), plus the F1-F3
  # companions: the pre-declared ebic1 and, per PREREG_c050 R2, cv_1se and ebic1_K37 when present.
  is_comp <- long$method_id %in% names(T1_COMPANION) & long$rule_id %in% c("ebic1", "cv_1se", "ebic1_K37")
  is_t1 <- long$role == "primary" | is_comp
  t1 <- long[is_t1, c("method_id", "rule_id", "role", "label", "p", "scenario", "exact_all", "exact_passing",
                      "n_expected", "n_success", "exact_among_success", "n_flagged", "n_k_gt_K")]
  t1$column <- ifelse(t1$role == "primary", "primary", "companion")
  write_table(t1, file.path(dir, "T1.csv"))

  prim <- long[long$role == "primary", ]
  write_table(prim[, c("method_id", "rule_id", "label", "p", "scenario", "n_expected", "n_failed", "n_timeout",
                            "n_not_run", "n_missing", "n_fail_total")], file.path(dir, "T2.csv"))
  write_table(prim[, c("method_id", "rule_id", "label", "p", "scenario", "n_success", "sum_fp", "sum_fn", "mean_fp", "mean_fn",
                            "err_exact", "err_extra_only", "err_missed_only", "err_mixed", "err_failed", "n_missing")],
                   file.path(dir, "T3.csv"))
  t4 <- t4_tables(s, coverage, signals)
  write_table(t4$by_variable, file.path(dir, "T4_by_variable.csv"))
  write_table(t4$by_group, file.path(dir, "T4_by_group.csv"))
  t5 <- t5_table(s)
  write_table(t5, file.path(dir, "T5.csv"))
  t6 <- t6_tables(s, coverage)
  write_table(t6$t6, file.path(dir, "T6.csv"))
  write_table(t6$codes, file.path(dir, "codes_by_rule.csv"))
  caps <- t6$t6[, c("method_id", "rule_id", "p", "scenario", "n_rows", "ebic_at_largest", "k_gt_K")]
  write_table(caps, file.path(dir, "caps.csv"))
  st <- long[long$role %in% c("S0", "S1"), c("method_id", "rule_id", "role", "label", "p", "scenario", "exact_all",
                                              "exact_passing", "n_expected", "n_success", "exact_among_success",
                                              "n_fail_total", "n_flagged")]
  write_table(st, file.path(dir, "S_tables.csv"))
  write_summary(dir, run_id, long, t5, t6$t6, t6$codes, coverage, problems, log[-1])
  cat("aggregate: wrote T1-T6, S_tables, rules_long, caps, codes_by_rule, summary.md in", dir, "\n")
  invisible(long)
}

if (sys.nframe() == 0L) {
  a <- commandArgs(TRUE)
  aggregate_run(a[which(a == "--dir") + 1], allow_problems = "--allow-problems" %in% a)
}
