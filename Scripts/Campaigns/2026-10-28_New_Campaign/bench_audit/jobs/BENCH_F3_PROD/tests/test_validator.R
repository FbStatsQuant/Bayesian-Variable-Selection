args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==5L)
sys.source(args[1], envir=.GlobalEnv)
code <- args[2]; input <- args[3]; manifest <- args[4]; prefix <- args[5]
x <- readRDS(paste0(prefix,".rds")); inp <- readRDS(input)
man <- read.csv(manifest,stringsAsFactors=FALSE)
mr <- man[man$dataset_id==inp$dataset_id,,drop=FALSE]
ctx <- load_frozen_validator(code)
source_hash <- x$prov$source_sha256
expected <- list(run_id=x$prov$run_id,dataset_id=inp$dataset_id,
 case_id=paste0(inp$dataset_id,"_c100"),p=inp$p,scenario=inp$scenario,
 replicate=inp$replicate,scale_key="c100",method_id="F3")
stopifnot(validate_prefix(prefix,source_hash,input,manifest,code,expected$run_id,
                          inp$dataset_id,inp$p,inp$scenario,inp$replicate,"c100"))
cat("PASS complete real RDS/CSV/input/manifest\n")
faults <- c("missing_OLS","bad_index","bad_k","missing_pilot","retired_code",
            "wrong_role","wrong_input_hash","wrong_numeric_beta","wrong_csv_criterion","bad_failed_vector")
reasons <- c("coefficient","coefficient","metadata","pilot","vocabulary","roles",
             "manifest_inputs_sha256","coefficient","CSV_RDS_crit_value","penalized support")
for(j in seq_along(faults)) {
  fault <- faults[j]; a <- x; csv <- x$rows
  if(fault=="missing_OLS") a$coefficients[[3]]$beta_ols <- NULL
  if(fault=="bad_index") a$coefficients[[1]]$index <- -999L
  if(fault=="bad_k") a$rows$k[1] <- csv$k[1] <- 999L
  if(fault=="missing_pilot") a$fit$diagnostics$pilot <- NULL
  if(fault=="retired_code") a$rows$diag_codes[1] <- csv$diag_codes[1] <- "kappa_edge"
  if(fault=="wrong_role") a$rows$role[1] <- csv$role[1] <- "S0"
  if(fault=="wrong_input_hash") a$rows$inputs_sha256 <- csv$inputs_sha256 <- strrep("0",64)
  if(fault=="wrong_numeric_beta") {
    a$coefficients[[1]]$beta_pen <- 2*a$coefficients[[1]]$beta_pen
  }
  if(fault=="wrong_csv_criterion") csv$crit_value[3] <- 123456
  if(fault=="bad_failed_vector") {
    a$rows$status[1] <- csv$status[1] <- a$coefficients[[1]]$status <- "failed"
    a$rows$support[1] <- csv$support[1] <- a$coefficients[[1]]$support <- NA_character_
    a$coefficients[[1]]$beta_pen <- rep(Inf,a$rows$p[1])
  }
  reason <- tryCatch({validate_object(a,csv,source_hash,inp,mr,expected,ctx); "ACCEPTED"},
                     error=function(e) conditionMessage(e))
  if(!grepl(reasons[j],reason,fixed=TRUE)) stop(fault,": expected ",reasons[j],", got ",reason)
  cat("PASS corruption",fault,":",reason,"\n")
}
cat("PASS real record plus 10/10 corruption reasons\n")
extra <- c("missing_coefficients","support_beta_mismatch","wrong_schema_version","wrong_source_sha256",
           "corrupt_OLS_both_copies","corrupt_weights","wrong_beta_both_copies")
extra_reasons <- c("coefficient evidence","penalized support mismatch","schema_version","source_sha256",
                   "OLS_beta","pilot_weights","selected_KKT")
for(j in seq_along(extra)) {
  a <- x; csv <- x$rows
  if(extra[j]=="missing_coefficients") a$coefficients <- NULL
  if(extra[j]=="support_beta_mismatch") {
    a$coefficients[[1]]$beta_pen[which(a$coefficients[[1]]$beta_pen!=0)[1]] <- 0
    a$fit$coefficients <- a$coefficients
  }
  if(extra[j]=="wrong_schema_version") a$schema_version <- 1L
  if(extra[j]=="wrong_source_sha256") a$prov$source_sha256 <- strrep("f",64)
  if(extra[j]=="corrupt_OLS_both_copies") {
    a$coefficients[[3]]$beta_ols[1] <- a$coefficients[[3]]$beta_ols[1] + 1
    a$fit$coefficients <- a$coefficients
  }
  if(extra[j]=="corrupt_weights") a$fit$diagnostics$v[1] <- 2*a$fit$diagnostics$v[1]
  if(extra[j]=="wrong_beta_both_copies") {
    a$coefficients[[1]]$beta_pen <- 2*a$coefficients[[1]]$beta_pen
    a$fit$coefficients <- a$coefficients
  }
  reason <- tryCatch({validate_object(a,csv,source_hash,inp,mr,expected,ctx); "ACCEPTED"},
                     error=function(e) conditionMessage(e))
  if(!grepl(extra_reasons[j],reason,fixed=TRUE)) stop(extra[j],": got ",reason)
  cat("PASS earlier control",extra[j],":",reason,"\n")
}
cat("PASS 4/4 earlier and 3/3 additional corruption reasons\n")
