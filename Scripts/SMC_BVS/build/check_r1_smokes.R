# Re-map saved development native outputs with R-1; no fit or original record mutation.
a <- commandArgs(TRUE)
stopifnot(length(a) == 4L)
source(file.path(a[1], "code/study/adapter.R"))
out <- a[4]; dir.create(out,recursive=TRUE,showWarnings=FALSE)
reports <- list()
for (path in a[2:3]) {
 r <- readRDS(path); before <- serialize(r$fit,NULL,version=3)
 stopifnot(r$fit$status == "completed", grepl("^dev_",r$case$dataset_id))
 outputs <- smcbvs_outputs(r$fit,r$case$p)
 design <- as.list(r$rows[1,,drop=FALSE])
 # Discard design row fields that the adapter itself supplies during a fresh fit.
 computed <- c("rule_id","role","status","converged","diag_flag","diag_codes","support","support_audit","k","n_warnings","warnings","messages","error")
 design[computed] <- NULL
 design$fold_seed <- NA_integer_; design$fold_sha256 <- NA_character_
 design$adapter_mapping_status <- "adopted"; design$adapter_policy_id <- smcbvs_r1_policy()$id
 design$adapter_policy_sha256 <- digest::digest(serialize(smcbvs_r1_policy(),NULL,version=3),algo="sha256",serialize=FALSE)
 mapped <- smcbvs_rule_rows(r$fit,outputs,design,smcbvs_r1_policy(),r$warnings,r$messages,r$error)
 stopifnot(identical(mapped$role,c("primary","S0")),all(is.na(mapped$converged)),
   all(mapped$status=="ok"),all(!mapped$diag_flag),all(grepl("cut_group",mapped$diag_codes)),
   all(mapped$adapter_mapping_status=="adopted"),all(mapped$adapter_policy_id==smcbvs_r1_policy()$id),
   all(mapped$adapter_policy_sha256==design$adapter_policy_sha256),
   identical(mapped$support,r$rows$support),identical(mapped$k,r$rows$k),
   identical(serialize(r$fit,NULL,version=3),before),all(is.na(mapped$fold_seed)))
 reports[[as.character(r$case$p)]] <- list(original_record_sha256=smcbvs_file_hash(path),
   original_source_sha256=r$code$source_sha256,
   original_mapping=r$rows[1,c("adapter_mapping_status","adapter_policy_id","adapter_policy_sha256")],
   native_fit_unchanged=TRUE,
   mapping_source=smcbvs_source_record(file.path(a[1],"code/core")),
   rows=mapped,policy=smcbvs_r1_policy(),note="Mapping audit only; original fit and record retained.")
}
saveRDS(reports,file.path(out,"r1_saved_smoke_mapping.rds"),version=3)
jsonlite::write_json(reports,file.path(out,"r1_saved_smoke_mapping.json"),pretty=TRUE,auto_unbox=TRUE,na="null",digits=NA)
cat("R1_SAVED_SMOKE_MAPPING_PASS\n")
