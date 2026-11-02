args <- commandArgs(trailingOnly=TRUE); stopifnot(length(args)==2L)
local({
C <- normalizePath(args[1],mustWork=TRUE)
S <- file.path(C,"code/bench_v2/review/sol_scripts_r2")
T <- file.path(C,"bench_audit/jobs/BENCH_F3_PROD/tests")
code <- file.path(C,"code/bench_v2/F3_AdaptiveLasso")
sys.source(file.path(C,"bench_audit/jobs/BENCH_F3_PROD/runner/validate.R"),.GlobalEnv)
ctx <- load_frozen_validator(code)
real_input <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S1_r001.rds"
real_manifest <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv"
prefix <- file.path(C,"code/bench_v2/tests/runner_output/results/v2_local_e2e/p0500/dev_p0500_S1_r001_c100/F3")
x <- readRDS(paste0(prefix,".rds")); source_hash <- x$prov$source_sha256
null_id <- "fixture_p0005_S1_r001"
null_input <- file.path(T,"fixtures/inputs/p0005",paste0(null_id,".rds"))
null_manifest <- file.path(T,"fixtures/inputs_manifest.csv")
tests <- data.frame(
 name=c("extra_data_seed","extra_fold_seed","extra_method_seed","null_index_lambda","null_path",
        "null_candidates","null_CV_RSS","cv_min_replaced_by_cv_1se","extra_EBIC_criterion"),
 reason=c("seed_binding_data_seed","seed_binding_fold_seed","seed_binding_method_seed","null_sentinels","null_path",
          "null_candidates","null_rss","CV_choice_cv_min","EBIC_score_ebic1"),
 null=c(FALSE,FALSE,FALSE,TRUE,TRUE,TRUE,TRUE,FALSE,FALSE))
for(j in seq_len(nrow(tests))) {
  t <- tests[j,]; folder <- file.path(S,"corruptions",t$name,"F3")
  why <- tryCatch({
    if(t$null) validate_prefix(folder,source_hash,null_input,null_manifest,code,"branch_fixture",null_id,5L,1L,1L,"c100")
    else validate_prefix(folder,source_hash,real_input,real_manifest,code,"v2_local_e2e","dev_p0500_S1_r001",500L,1L,1L,"c100")
    "ACCEPTED"
  },error=function(e) conditionMessage(e))
  cat("CONTROL",t$name,why,"\n")
  if(!grepl(t$reason,why,fixed=TRUE)) stop(t$name," expected ",t$reason," got ",why)
}
input <- readRDS(real_input); X <- input$X; y <- input$Y[,"c100"]
tmp <- tempfile("r2_",tmpdir=T); dir.create(tmp)
on.exit(unlink(tmp,recursive=TRUE),add=TRUE)
check_saved <- function(a,label,reason) {
  p <- file.path(tmp,"F3")
  saveRDS(a,paste0(p,".rds"),version=3)
  write.csv(a$rows,paste0(p,".csv"),row.names=FALSE,na="NA")
  writeLines(c(paste(ctx$engine$file_sha256(paste0(p,".rds")),"F3.rds",sep="  "),
               paste(ctx$engine$file_sha256(paste0(p,".csv")),"F3.csv",sep="  ")),paste0(p,".sha256"))
  writeLines("review control",paste0(p,".done"))
  why <- tryCatch({validate_prefix(p,source_hash,real_input,real_manifest,code,"v2_local_e2e",
                                   "dev_p0500_S1_r001",500L,1L,1L,"c100"); "ACCEPTED"},
                  error=function(e)conditionMessage(e))
  cat("CONTROL",label,why,"\n")
  if(!grepl(reason,why,fixed=TRUE)) stop(label," expected ",reason," got ",why)
}
# Replace EBIC1 with the distinct CV-1SE support, its actual penalised beta,
# OLS refit and true score. It remains a wrong EBIC minimiser.
a <- x; i <- match("ebic1",a$rows$rule_id); j <- match("cv_1se",a$rows$rule_id)
ca <- a$fit$diagnostics$candidates
candidate <- ca[match(a$rows$support[j],ca$key),,drop=FALSE]
stopifnot(nrow(candidate)==1L,candidate$valid,a$rows$support[i]!=a$rows$support[j])
for(nm in c("status","support","support_audit","k","index","lambda","error"))
  a$rows[[nm]][i] <- a$fit$rules[[nm]][i] <- x$rows[[nm]][j]
for(nm in c("rss","ebic1_value","crit_value")) {
  val <- switch(nm,rss=candidate$rss,ebic1_value=candidate$ebic1,crit_value=candidate$ebic1)
  a$rows[[nm]][i] <- a$fit$rules[[nm]][i] <- val
}
co <- x$coefficients[[j]]; co$rule_id <- "ebic1"
co$beta_ols <- numeric(ncol(X)); ix <- which(co$beta_pen!=0)
co$beta_ols[ix] <- lm.fit(X[,ix,drop=FALSE],y,tol=1e-10)$coefficients
a$coefficients[[i]] <- co; a$fit$coefficients <- a$coefficients
check_saved(a,"wrong_EBIC_pick","EBIC_pick_ebic1")
# Change index/lambda consistently to a later KKT-passing occurrence of the
# same EBIC support. Selection must reject before testing its beta.
a <- x; i <- match("ebic1",a$rows$rule_id); path <- a$fit$diagnostics$path
later <- which(path$key==a$rows$support[i] & path$kkt_full<=ctx$cfg$GLMNET$kkt_rel_tol & seq_len(nrow(path))>a$rows$index[i])
stopifnot(length(later)>0L)
ix <- later[1]; a$rows$index[i] <- a$fit$rules$index[i] <- ix
a$rows$lambda[i] <- a$fit$rules$lambda[i] <- path$lambda[ix]
a$coefficients[[i]]$index <- ix; a$coefficients[[i]]$lambda <- path$lambda[ix]
a$fit$coefficients <- a$coefficients
check_saved(a,"later_EBIC_occurrence","EBIC_occurrence_ebic1")
a <- x; a$fit$diagnostics$path$lambda[2] <- a$fit$diagnostics$path$lambda[2]*1.01
check_saved(a,"weighted_grid","weighted_lambda_grid")
a <- x; a$fit$diagnostics$candidates$ebic1[1] <- a$fit$diagnostics$candidates$ebic1[1]+1
check_saved(a,"candidate_table","candidate_table")
a <- x; a$fit$diagnostics$index[1] <- a$fit$diagnostics$index[1]-1L
check_saved(a,"cv_diagnostic_index","CV_diagnostic_choices")
fid <- "fixture_p0005_S3_r001"
finput <- file.path(T,"fixtures/inputs/p0005",paste0(fid,".rds"))
fmanifest <- file.path(T,"fixtures/inputs_manifest.csv")
fp <- file.path(T,"fixtures/results/branch_failure/p0005",paste0(fid,"_c100"),"F3")
fx <- readRDS(paste0(fp,".rds"))
for(seed in c("data_seed","fold_seed","method_seed")) {
  a <- fx; a$rows[[seed]] <- a$rows[[seed]]+1L; a$case[[seed]] <- a$case[[seed]]+1L
  p <- file.path(tmp,"F3"); saveRDS(a,paste0(p,".rds"),version=3)
  write.csv(a$rows,paste0(p,".csv"),row.names=FALSE,na="NA")
  writeLines(c(paste(ctx$engine$file_sha256(paste0(p,".rds")),"F3.rds",sep="  "),
               paste(ctx$engine$file_sha256(paste0(p,".csv")),"F3.csv",sep="  ")),paste0(p,".sha256"))
  writeLines("review control",paste0(p,".done"))
  why <- tryCatch({validate_prefix(p,source_hash,finput,fmanifest,code,"branch_failure",fid,5L,3L,1L,"c100");"ACCEPTED"},
                  error=function(e)conditionMessage(e))
  expected <- paste0("seed_binding_",seed)
  cat("CONTROL failed_",seed," ",why,"\n",sep="")
  if(!grepl(expected,why,fixed=TRUE)) stop("whole-failure ",seed,": ",why)
}
cat("PASS 14 review-2 saved-record corruption controls\n")
cat("PASS 3/3 whole-failure seed controls\n")
})
