# Deliberately invalid MOCK bundles only, for saved rejection evidence.
a <- commandArgs(TRUE); prefix <- a[1]; mode <- a[2]
record <- readRDS(paste0(prefix,".rds")); rows <- record$rows
if(mode=="bad_pip") {record$pip[1] <- .1
} else if(mode=="unavailable_pip") {record$pip[] <- NA_real_
} else if(mode=="stale_truth") {rows$tp <- 0L
} else if(mode=="failed_as_null") {rows$support <- ""; rows$k <- 0L
} else if(mode=="successful_as_NA") {rows$support <- NA_character_; rows$k <- NA_integer_
} else if(mode=="unresolved_policy") {rows$adapter_mapping_status <- "unresolved"
} else if(mode=="unmapped_native") {rows$v3_flags_json <- "{}"
} else if(mode=="duplicate_smc") {rows <- rbind(rows,rows[1,,drop=FALSE])
} else if(mode=="csv_rds_disagree") {record$rows$support[1] <- ""
} else if(mode=="hpm_disagrees") {ii <- rows$rule_id=="hpm";rows$support[ii] <- paste(1:13,collapse=";");rows$k[ii] <- 13L
} else if(mode=="pip_disagrees") {record$pip[17] <- .9;ii <- rows$rule_id=="pip05";rows$support[ii] <- paste(c(1:14,17),collapse=";");rows$k[ii] <- 15L
} else if(mode=="native_status_disagrees") {record$fit$status <- "numerical_failure"
} else if(mode=="reverse_failure_status") {record$fit$status <- "completed"
} else if(mode=="degenerate_status_disagrees") {record$fit$status <- "y_constant"
} else if(mode=="missing_native_payload") {for(nm in c("stage_table","log_Z","log_Z_r","log_Z_lower95","bound_label","timings","pip_primary","streams")) record$fit[[nm]] <- NULL
} else if(mode=="missing_native_pip") {record$fit$pip_primary <- NULL
} else if(mode=="bad_preprocessing_map") {record$fit$preprocessing$dropped <- 1L
} else if(mode=="wrong_native_pip_names") {names(record$fit$pip_primary)[1] <- "9999"
} else if(mode=="missing_native_stage") {record$fit$stage_table <- NULL
} else if(mode=="missing_island_evidence") {record$fit$log_Z_r <- NULL
} else if(mode=="missing_native_streams") {record$fit$streams <- NULL
} else if(mode=="missing_bound_label_uncertified") {record$fit$bound_label <- NULL;record$native_annotations <- NULL
} else if(mode=="missing_bound_label_certified") {record$fit$bound_label <- NULL;record$native_annotations <- NULL
  # D-F1: a reported global certificate (consistently in fit and exported JSON) still requires the label.
  record$fit$global_certified <- TRUE
  rows$v3_flags_json <- vapply(rows$v3_flags_json,function(x) {j <- jsonlite::fromJSON(x,simplifyVector=FALSE)
    j$global_certified <- TRUE;as.character(jsonlite::toJSON(j,auto_unbox=TRUE,null="null",na="null"))},"",USE.NAMES=FALSE)
} else if(startsWith(mode,"json_") || mode=="native_json_disagrees") {
  nm <- if(mode=="native_json_disagrees") "cut_group" else sub("^json_","",mode);j <- jsonlite::fromJSON(rows$v3_flags_json[1],simplifyVector=FALSE)
  j[[nm]] <- if(nm=="cut_group_components") list(list(members=c(1,2))) else if(nm=="cut_group_count") 42L else TRUE
  rows$v3_flags_json <- as.character(jsonlite::toJSON(j,auto_unbox=TRUE,null="null",na="null"))
} else if(mode=="missing_failure_audit" || mode=="null_failure_as_NA") {rows$support_audit[rows$rule_id=="hpm"] <- NA_character_
} else if(mode=="changed_failure_audit") {rows$support_audit[rows$rule_id=="hpm"] <- "1;3"
} else if(mode=="unavailable_failure_as_empty") {rows$support_audit[rows$rule_id=="pip05"] <- ""
} else stop("unknown mutation")
if(mode!="csv_rds_disagree") record$rows <- rows
saveRDS(record,paste0(prefix,".rds"),version=3)
utils::write.csv(rows,paste0(prefix,".csv"),row.names=FALSE,na="NA")
paths <- paste0(prefix,c(".rds",".csv"))
writeLines(paste(vapply(paths,function(x) digest::digest(file=x,algo="sha256"),""),basename(paths),sep="  "),paste0(prefix,".sha256"))
