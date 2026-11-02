root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro/controlled_2a8362b2f348"
ids <- as.vector(outer(c("p0500","p1000"), 1:6, function(p,s) paste0("dev_",p,"_S",s,"_r001")))
cases <- expand.grid(id=ids, scale=c("c100","c050"), stringsAsFactors=FALSE)
cases_out <- list(); rules_out <- list(); truth_out <- list()
for (i in seq_len(nrow(cases))) {
  id <- cases$id[i]; scale <- cases$scale[i]; stem <- paste0(id,"_",scale)
  rds <- file.path(root,paste0(stem,".rds")); sexit <- file.path(root,paste0(stem,".script_exit"))
  log <- file.path(root,paste0(stem,".log"))
  if (!file.exists(rds) || !file.exists(sexit) || !file.exists(log) ||
      !identical(paste(readLines(sexit,warn=FALSE),collapse=""),"0")) {
    cases_out[[i]] <- data.frame(id=id,scale=scale,state="incomplete")
    next
  }
  lines <- readLines(log,warn=FALSE)
  if (!any(grepl("^finish ",lines)) || any(grepl("FATAL:|Error:|Execution halted",lines))) {
    cases_out[[i]] <- data.frame(id=id,scale=scale,state="unclean_log")
    next
  }
  d <- readRDS(rds); rr <- d$F3$result$rules
  cases_out[[i]] <- data.frame(id=id,scale=scale,state="script_exit_0",script_exit=0,
    F1_rows=d$F1$checks["rows"],F1_beta=d$F1$checks["beta"],F1_diagnostics=d$F1$checks["diagnostics"],F1_converged=d$F1$checks["converged"],
    F2_rows=d$F2$checks["rows"],F2_beta=d$F2$checks["beta"],F2_diagnostics=d$F2$checks["diagnostics"],F2_converged=d$F2$checks["converged"],
    F1_old_s=d$F1$old$seconds,F1_new_s=d$F1$new$seconds,F2_old_s=d$F2$old$seconds,F2_new_s=d$F2$new$seconds,
    F3_s=d$F3$seconds,pilot_k=length(d$F3$result$diagnostics$keep),
    pilot_identity_final=d$pilot_identical,pilot_identity_original=d$pilot_identity_original_F1,
    F1_support=all(d$checks$F1$support),F2_support=all(d$checks$F2$support),F3_support=all(d$checks$F3$support),
    F1_k37=all(d$checks$F1$k37),F2_k37=all(d$checks$F2$k37),F3_k37=all(d$checks$F3$k37))
  rules_out[[length(rules_out)+1L]] <- data.frame(id=id,scale=scale,rr[,c("rule_id","status","k","support")],
    coefficient_consistent=d$checks$F3$support,runtime_s=d$F3$seconds)
  if (!is.null(d$truth_diagnostic)) for (method in c("ridge","v2")) {
    z <- d$truth_diagnostic[[method]]
    truth_out[[length(truth_out)+1L]] <- data.frame(id=id,scale=scale,method=method,
      noise_below_weakest_truth=z$noise_below_weakest_truth,truth_inside_screen=z$truth_inside_screen,
      truth_on_path=z$truth_on_path,ebic1_K37_exact=z$ebic1_K37_exact)
  }
}
cols <- unique(unlist(lapply(cases_out,names)))
cases_out <- lapply(cases_out,function(z) { for (n in setdiff(cols,names(z))) z[[n]] <- NA; z[cols] })
write.csv(do.call(rbind,cases_out),file.path(root,"case_summary_capped.csv"),row.names=FALSE,na="NA")
if (length(rules_out)) write.csv(do.call(rbind,rules_out),file.path(root,"F3_rules_capped.csv"),row.names=FALSE,na="NA")
if (length(truth_out)) write.csv(do.call(rbind,truth_out),file.path(root,"truth_diagnostics_capped.csv"),row.names=FALSE,na="NA")
cat("capped summary updated\n")
