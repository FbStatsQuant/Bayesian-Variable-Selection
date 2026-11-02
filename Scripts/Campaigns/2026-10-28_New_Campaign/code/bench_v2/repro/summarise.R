# Summarize completed case outputs; absent and failed cases remain visible.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro"
ids <- as.vector(outer(c("p0500", "p1000"), 1:6, function(p, s) paste0("dev_", p, "_S", s, "_r001")))
cases <- expand.grid(id = ids, scale = c("c100", "c050"), stringsAsFactors = FALSE)
frozen <- new.env(parent = globalenv())
sys.source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/scoring/derived_rules/derive_rules.R", frozen)
rows <- list(); differences <- list()
for (i in seq_len(nrow(cases))) {
  id <- cases$id[i]; scale <- cases$scale[i]; name <- paste0(id, "_", scale)
  path <- file.path(root, paste0(name, ".rds")); exit <- file.path(root, paste0(name, ".exit"))
  if (!file.exists(path) || !file.exists(exit)) {
    rows[[i]] <- data.frame(id = id, scale = scale, state = if (file.exists(exit)) paste0("exit_", readLines(exit, warn = FALSE)[1]) else "running_or_queued")
    next
  }
  d <- readRDS(path); f <- d$F3$result
  same_columns <- function(method) {
    old <- d[[method]]$old$result$rules
    new <- d[[method]]$new$result$rules[match(old$rule_id, d[[method]]$new$result$rules$rule_id), , drop = FALSE]
    identical(as.list(old), as.list(new))
  }
  quality <- lapply(c("F1","F2","F3"), function(method) {
    obj <- if (method == "F3") d$F3$result else d[[method]]$new$result
    if (is.null(obj$diagnostics$candidates)) return(c(support=FALSE,k37=FALSE))
    tb <- frozen$method_tables(list(diagnostics=obj$diagnostics, settings=list(GLMNET=list(kkt_rel_tol=1e-5))),method)
    pp <- as.integer(sub("^p", "", substr(id,5,9)))
    dr <- frozen$derive_case(tb, method, pp)$rules
    k37 <- all(vapply(c("ebic1_K37","ebic05_K37"), function(rid) {
      z <- obj$rules[obj$rules$rule_id==rid,]
      identical(z$support,dr[[rid]]$key) && identical(z$k_valid_max,dr[[rid]]$k_valid_max) &&
        isTRUE(all.equal(z$crit_value,dr[[rid]]$crit,tolerance=0))
    },logical(1)))
    evidence <- all(vapply(seq_len(nrow(obj$rules)),function(j) {
      z <- obj$rules[j,]; key <- if (z$status=="failed") z$support_audit else z$support
      identical(paste(which(obj$coefficients[[j]]$beta_pen != 0),collapse=";"),key)
    },logical(1)))
    c(support=evidence,k37=k37)
  })
  ks <- setNames(f$rules$k, f$rules$rule_id)
  rows[[i]] <- data.frame(id = id, scale = scale, state = "complete",
    F1_rows = same_columns("F1"), F1_row_attributes = d$F1$checks["rows"], F1_beta = d$F1$checks["beta"],
    F1_diagnostics = d$F1$checks["diagnostics"], F1_converged = d$F1$checks["converged"],
    F2_rows = same_columns("F2"), F2_row_attributes = d$F2$checks["rows"], F2_beta = d$F2$checks["beta"],
    F2_diagnostics = d$F2$checks["diagnostics"], F2_converged = d$F2$checks["converged"],
    F1_old_s = d$F1$old$seconds, F1_v2_s = d$F1$new$seconds,
    F2_old_s = d$F2$old$seconds, F2_v2_s = d$F2$new$seconds, F3_s = d$F3$seconds,
    pilot_identical = d$pilot_identical, pilot_k = length(f$diagnostics$keep),
    F1_support=quality[[1]]["support"], F1_k37=quality[[1]]["k37"],
    F2_support=quality[[2]]["support"], F2_k37=quality[[2]]["k37"],
    F3_support=quality[[3]]["support"], F3_k37=quality[[3]]["k37"],
    F3_status = paste(f$rules$status, collapse = ";"), F3_k = paste(ks, collapse = ";"),
    F3_supports = paste(f$rules$support, collapse = "|"), stringsAsFactors = FALSE)
  for (m in c("F1","F2")) if (length(d[[m]]$differences))
    differences[[name]] <- c(differences[[name]], paste(m, names(d[[m]]$differences),
      vapply(d[[m]]$differences, paste, collapse = " | ", FUN.VALUE = "")))
}
allcols <- unique(unlist(lapply(rows, names)))
rows <- lapply(rows, function(z) { for (nm in setdiff(allcols, names(z))) z[[nm]] <- NA; z[allcols] })
res <- do.call(rbind, rows)
write.csv(res, file.path(root, "case_summary.csv"), row.names = FALSE, na = "NA")
writeLines(as.character(unlist(lapply(names(differences), function(nm) paste(nm, differences[[nm]])))),
           file.path(root, "differences.txt"))
print(table(res$state))
