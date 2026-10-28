# combine.R: one combined set of tables across the production runs (thread S, 2026-10-19).
# Usage: Rscript --vanilla combine.R --out <dir> <run out dir 1> <run out dir 2> ...
# Binds rules_long, T1–T6, S-tables and caps of each run (adding run_id) and writes a combined
# summary with the T1 matrix (rows: p × scenario, columns: method/rule).

find_code_dir <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
}
if (!exists("REGISTRY")) source(file.path(find_code_dir(), "registry.R"))

combine_runs <- function(out_dir, run_dirs) {
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  tables <- c("rules_long", "T1", "T2", "T3", "T4_by_variable", "T4_by_group", "T5", "T6", "S_tables",
              "caps", "codes_by_rule")
  for (tb in tables) {
    parts <- lapply(run_dirs, function(d) {
      # Type inference reads the 17-digit doubles back exactly; write_table prints them again unchanged.
      x <- utils::read.csv(file.path(d, paste0(tb, ".csv")), stringsAsFactors = FALSE)
      if (nrow(x) == 0) return(NULL)        # e.g. T1-T3 of a run with no primary rule (SuSiE-refine)
      x$scenario <- if ("scenario" %in% names(x)) as.character(x$scenario) else NULL
      for (cc in intersect(c("abs_beta", "rho_S6"), names(x))) x[[cc]] <- sprintf("%.1f", x[[cc]])   # labels
      cbind(run_id = basename(d), x, stringsAsFactors = FALSE)
    })
    write_table(do.call(rbind, parts), file.path(out_dir, paste0(tb, ".csv")))
  }
  t1 <- utils::read.csv(file.path(out_dir, "T1.csv"), colClasses = "character")
  t2 <- utils::read.csv(file.path(out_dir, "T2.csv"), colClasses = "character")
  tag <- if ("label" %in% names(t1)) ifelse(grepl("^post hoc", t1$label), " (post hoc)", ifelse(grepl("^pre-registered", t1$label), " (pre-reg.)", "")) else ""
  t1$label <- paste0(t1$method_id, " ", t1$rule_id, tag, ifelse(t1$column == "companion", " (companion)", ""))
  grid <- unique(t1[, c("p", "scenario")])
  for (lab in unique(t1$label)) {
    x <- t1[t1$label == lab, ]
    v <- paste0(x$exact_all, "/", x$n_expected)
    v <- ifelse(as.integer(x$n_flagged) > 0, paste0(v, " [", x$exact_passing, "]"), v)
    grid[[lab]] <- v[match(paste(grid$p, grid$scenario), paste(x$p, x$scenario))]
  }
  fails <- unique(t2[, c("p", "scenario")])
  for (m in unique(t2$method_id)) {
    x <- t2[t2$method_id == m, ]
    fails[[m]] <- x$n_fail_total[match(paste(fails$p, fails$scenario), paste(x$p, x$scenario))]
  }
  md <- function(df) c(paste0("| ", paste(names(df), collapse = " | "), " |"),
                       paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
                       apply(df, 1, function(r) paste0("| ", paste(r, collapse = " | "), " |")))
  L <- c("# Combined benchmark tables (n = 200, c = 1)", "",
         "Provisional: scoring and method code are AI-written and unreviewed (G5); recount (G9) pending unless stated.", "",
         paste0("Runs: ", paste(basename(run_dirs), collapse = ", ")), "",
         "## T1: exact recovery, all-saved (passing-only in brackets where any fit is flagged)", "", md(grid), "",
         "## T2: failed + timeout + not_run + missing, primary rule", "", md(fails), "")
  writeLines(L, file.path(out_dir, "summary_combined.md"))
  write_summary_md(out_dir, run_dirs, md)
  cat("combine: wrote", length(tables), "tables, summary_combined.md and SUMMARY.md in", out_dir, "\n")
}

# SUMMARY.md: per method, the primary rule's exact recovery per scenario (x/100) and per p (x/600),
# failures and flags, the pre-declared companion and S-rules (pooled), any post-hoc S-table kept
# apart and labelled, and the paths.
write_summary_md <- function(out_dir, run_dirs, md) {
  long <- utils::read.csv(file.path(out_dir, "rules_long.csv"), stringsAsFactors = FALSE)
  study <- "/projects/ml75/fb31/BVS/bench20261019"
  L <- c("# SUMMARY: n = 200 benchmark production runs, c = 1 (thread S)", "",
         "All numbers are provisional: the method code and the scoring code are AI-written and unreviewed (G5); the independent recount (G9) is separate.",
         "Denominators: 100 per (p, scenario), 600 pooled per p. Failures = failed + timeout + not_run + missing; they count as non-recovery.",
         "Flagged = fits with `diag_flag = TRUE` (passing-only count in brackets).", "")
  for (d in run_dirs) {
    run_id <- basename(d)
    x <- long[long$run_id == run_id, ]
    # Methods with a primary rule; a run of S1 arms only (e.g. SuSiE-refine) is shown by its S1 rule.
    ms <- unique(x$method_id[x$role == "primary"])
    head_role <- "primary"
    if (!length(ms)) { ms <- unique(x$method_id); head_role <- "S1" }
    for (m in ms) {
      xm <- x[x$method_id == m, ]
      for (pr in unique(xm$rule_id[xm$role == head_role])) {
        prim <- xm[xm$role == head_role & xm$rule_id == pr, ]
        lab <- if ("label" %in% names(prim)) prim$label[1] else "pre-declared"
        L <- c(L, paste0("## ", m, ": ", if (head_role == "primary") "primary" else "S1", " rule `", pr, "` (", lab, ")"), "")
        tab <- data.frame(p = c(500, 1000))
        for (sc in c(as.character(DESIGN_SCENARIOS), "pooled")) {
          v <- prim[prim$scenario == sc, ]
          v <- v[match(tab$p, v$p), ]
          tab[[if (sc == "pooled") "pooled /600" else paste0("S", sc)]] <-
            ifelse(v$n_flagged > 0, paste0(v$exact_all, " [", v$exact_passing, "]"), v$exact_all)
        }
        pooled <- prim[prim$scenario == "pooled", ]
        pooled <- pooled[match(tab$p, pooled$p), ]
        tab$failures <- pooled$n_fail_total
        tab$flagged <- pooled$n_flagged
        if ("n_k_gt_K" %in% names(pooled) && any(!is.na(pooled$n_k_gt_K))) tab$`k > 37` <- pooled$n_k_gt_K
        L <- c(L, md(tab), "")
      }
      others <- x[x$scenario == "pooled" & !(x$method_id == m & x$role == head_role) &
                  (x$method_id == m | !(x$method_id %in% x$method_id[x$role == "primary"])), ]
      if (nrow(others)) {
        o <- unique(others[, intersect(c("method_id", "rule_id", "role", "label"), names(others))])
        o$`p = 500 /600` <- others$exact_all[others$p == 500][match(paste(o$method_id, o$rule_id), paste(others$method_id, others$rule_id)[others$p == 500])]
        o$`p = 1000 /600` <- others$exact_all[others$p == 1000][match(paste(o$method_id, o$rule_id), paste(others$method_id, others$rule_id)[others$p == 1000])]
        o$role <- ifelse(o$role == "S0" & o$method_id %in% names(T1_COMPANION) & o$rule_id == "ebic1", "S0 (T1 companion)", o$role)
        L <- c(L, "Pre-declared companion and sensitivity rules (pooled):", "", md(o), "")
      }
      ph <- file.path(d, "posthoc_ebic1_K37", "S_table_posthoc.csv")
      if (file.exists(ph)) {
        pt <- utils::read.csv(ph, stringsAsFactors = FALSE)
        pt <- pt[pt$scenario == "pooled", c("method_id", "rule_id", "p", "exact_all", "n_expected", "n_fail_total")]
        L <- c(L, "**Post hoc (chosen after seeing the production cap-hit diagnostics; not a pre-declared rule; not in T1):**", "", md(pt), "")
      }
      L <- c(L, paste0("Paths: results `", study, "/results/", run_id, "/`; tables `", d, "/`",
                       if (file.exists(ph)) paste0("; post hoc `", d, "/posthoc_ebic1_K37/`") else "", "."), "")
    }
  }
  L <- c(L, paste0("Combined tables: `", out_dir, "/` (rules_long, T1–T6, S_tables, caps, codes_by_rule; real values at 17 significant digits)."))
  writeLines(L, file.path(out_dir, "SUMMARY.md"))
}

if (sys.nframe() == 0L) {
  a <- commandArgs(TRUE)
  i <- which(a == "--out")
  combine_runs(a[i + 1], a[-c(i, i + 1)])
}
