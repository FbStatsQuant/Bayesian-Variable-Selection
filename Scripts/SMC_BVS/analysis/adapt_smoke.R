# D-OWNED R-1 REFERENCE COPY ONLY. Never changes native fit or original files; never scores.
a <- commandArgs(TRUE);source(a[1]);source(a[2]);source(a[3]);prefix <- a[4]
record <- readRDS(paste0(prefix,".rds"));native_before <- record$fit;before <- serialize(native_before,NULL,version=3)
same_native <- function(x,y) identical(x,y,num.eq=FALSE,single.NA=FALSE,attrib.as.set=FALSE)
legacy_policy <- record$adapter_policy
expected <- r1_expected(record$fit,record$native_status,record$warnings,record$messages)
rows <- record$rows
rows$role <- unname(c(hpm="primary",pip05="S0")[rows$rule_id])
rows$status <- expected$status;rows$converged <- NA;rows$diag_flag <- expected$diag_flag
rows$diag_codes <- paste(expected$codes,collapse=";");rows$fold_seed <- NA;rows$fold_sha256 <- NA
policy <- list(id="D_REFERENCE_R1_DEV_COPY_NOT_A_CERTIFICATION",mock_only=TRUE,adopted=TRUE,mapping_status="adopted",
  authority="D-owned reference application of binding R-1 to unchanged actual dev native fit")
record$adapter_policy <- policy
record$adapter_policy_sha256 <- digest::digest(serialize(policy,NULL,version=3),algo="sha256",serialize=FALSE)
rows$adapter_policy_id <- policy$id;rows$adapter_policy_sha256 <- record$adapter_policy_sha256;rows$adapter_mapping_status <- "adopted"
record$rows <- rows
record$native_annotations <- list(log_Z_lower95=list(label="heuristic",authority="D R-1 annotation; absent from legacy A native fit",
  native_value_unmodified=TRUE))
record$d_reference_mapping <- list(label="D-OWNED R-1-ADAPTED DEV COPY; NOT UPDATED A ADAPTER; NO TRUTH/SCORING",legacy_policy=legacy_policy,
  native_fit_sha256=digest::digest(before,algo="sha256",serialize=FALSE))
if(!same_native(native_before,record$fit)) stop("native fit changed during D adaptation")
native_validate(as.data.frame(lapply(rows,as.character)),record,as.integer(rows$p[1]))
mock_write_record(prefix,record)
again <- readRDS(paste0(prefix,".rds"))
if(!same_native(native_before,again$fit)) stop("native fit changed on copied RDS roundtrip")
jsonlite::write_json(list(label=record$d_reference_mapping$label,native_fit_sha256=record$d_reference_mapping$native_fit_sha256,
  native_fit_unchanged=TRUE,comparison="R identical(num.eq=FALSE,single.NA=FALSE,attrib.as.set=FALSE); all native values/attributes, numeric bytes",
  serialization_note="Pre-copy serialization hash is provenance; serialization representation may materialize ALTREP on roundtrip",
  original_bound_has_heuristic_label=!is.null(record$fit$bound_label),
  bound_annotation=record$native_annotations$log_Z_lower95),paste0(prefix,".D_reference.json"),pretty=TRUE,auto_unbox=TRUE)
