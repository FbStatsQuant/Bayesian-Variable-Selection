root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro/controlled_2a8362b2f348"
ids <- as.vector(outer(c("p0500","p1000"), 1:6, function(p, s) paste0("dev_",p,"_S",s,"_r001")))
cases <- expand.grid(id = ids, scale = c("c100","c050"), stringsAsFactors = FALSE)
cases_out <- vector("list", nrow(cases)); rules_out <- list(); truth_out <- list(); diffs <- character()
for (i in seq_len(nrow(cases))) {
  id <- cases$id[i]; scale <- cases$scale[i]; stem <- paste0(id, "_", scale)
  f <- file.path(root, paste0(stem, ".rds")); ex <- file.path(root, paste0(stem, ".exit"))
  status <- if (file.exists(ex)) paste(readLines(ex, warn = FALSE), collapse = "") else NA_character_
  sx <- file.path(root, paste0(stem, ".script_exit"))
  script_status <- if (file.exists(sx)) paste(readLines(sx, warn = FALSE), collapse = "") else NA_character_
  if (!file.exists(f) || !file.exists(ex)) {
    cases_out[[i]] <- data.frame(id=id, scale=scale, state=if (is.na(status)) "queued_or_running" else paste0("exit_",status),
                                exit=status, stringsAsFactors=FALSE)
    next
  }
  d <- readRDS(f); rr <- d$F3$result$rules
  state <- if (identical(status,"0") && identical(script_status,"0")) "complete" else "exit_mismatch_or_failure"
  cases_out[[i]] <- data.frame(id=id, scale=scale, state=state, exit=status, script_exit=script_status,
    F1_rows=d$F1$checks["rows"], F1_beta=d$F1$checks["beta"], F1_diagnostics=d$F1$checks["diagnostics"], F1_converged=d$F1$checks["converged"],
    F2_rows=d$F2$checks["rows"], F2_beta=d$F2$checks["beta"], F2_diagnostics=d$F2$checks["diagnostics"], F2_converged=d$F2$checks["converged"],
    F1_old_s=d$F1$old$seconds, F1_new_s=d$F1$new$seconds, F2_old_s=d$F2$old$seconds, F2_new_s=d$F2$new$seconds,
    F3_s=d$F3$seconds, pilot_k=length(d$F3$result$diagnostics$keep),
    pilot_identity_final=d$pilot_identical, pilot_identity_original=d$pilot_identity_original_F1,
    F1_support=all(d$checks$F1$support), F2_support=all(d$checks$F2$support), F3_support=all(d$checks$F3$support),
    F1_k37=all(d$checks$F1$k37), F2_k37=all(d$checks$F2$k37), F3_k37=all(d$checks$F3$k37), stringsAsFactors=FALSE)
  rules_out[[length(rules_out)+1L]] <- data.frame(id=id, scale=scale, rr[,c("rule_id","status","k","support")],
    coefficient_consistent=d$checks$F3$support, runtime_s=d$F3$seconds)
  if (!is.null(d$truth_diagnostic)) for (method in c("ridge","v2")) {
    z <- d$truth_diagnostic[[method]]
    truth_out[[length(truth_out)+1L]] <- data.frame(id=id, scale=scale, method=method,
      noise_below_weakest_truth=z$noise_below_weakest_truth, truth_inside_screen=z$truth_inside_screen,
      truth_on_path=z$truth_on_path, ebic1_K37_exact=z$ebic1_K37_exact)
  }
  for (m in c("F1","F2")) if (length(d[[m]]$differences))
    diffs <- c(diffs, paste(stem,m,names(d[[m]]$differences),
      vapply(d[[m]]$differences,paste,collapse=" | ",FUN.VALUE="")))
}
cols <- unique(unlist(lapply(cases_out,names)))
cases_out <- lapply(cases_out,function(z) { for (n in setdiff(cols,names(z))) z[[n]] <- NA; z[cols] })
write.csv(do.call(rbind,cases_out), file.path(root,"case_summary.csv"),row.names=FALSE,na="NA")
if (length(rules_out)) write.csv(do.call(rbind,rules_out),file.path(root,"F3_rules.csv"),row.names=FALSE,na="NA")
if (length(truth_out)) write.csv(do.call(rbind,truth_out),file.path(root,"truth_diagnostics.csv"),row.names=FALSE,na="NA")
writeLines(diffs,file.path(root,"differences.txt"))
cat("case summary updated\n")
