args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==3L)
campaign <- normalizePath(args[1],mustWork=TRUE)
fixture <- normalizePath(args[2],mustWork=TRUE)
validator <- normalizePath(args[3],mustWork=TRUE)
sys.source(validator,envir=.GlobalEnv)
code <- file.path(campaign,"code/bench_v2/F3_AdaptiveLasso")
ctx <- load_frozen_validator(code)
manifest <- file.path(fixture,"inputs_manifest.csv")
man <- read.csv(manifest,stringsAsFactors=FALSE)
failures <- character()
for(i in seq_len(3L)) {
  label <- c("null","singleton","failed")[i]
  run_id <- if(label=="failed") "branch_failure" else "branch_fixture"
  id <- sprintf("fixture_p0005_S%d_r001",i)
  input <- file.path(fixture,"inputs","p0005",paste0(id,".rds"))
  prefix <- file.path(fixture,"results",run_id,"p0005",paste0(id,"_c100"),"F3")
  x <- readRDS(paste0(prefix,".rds")); inp <- readRDS(input)
  mr <- man[man$dataset_id==id,,drop=FALSE]
  expected <- list(run_id=run_id,dataset_id=id,case_id=paste0(id,"_c100"),
                   p=5L,scenario=as.integer(i),replicate=1L,scale_key="c100",method_id="F3")
  positive <- tryCatch({validate_prefix(prefix,x$prov$source_sha256,input,manifest,code,
                                        run_id,id,5L,i,1L,"c100"); "PASS"},
                       error=function(e) conditionMessage(e))
  cat("POSITIVE",label,positive,"\n")
  if(positive!="PASS") failures <- c(failures,paste(label,positive))
  for(j in 1:2) {
    a <- x; rows <- x$rows
    if(label=="null" && j==1) {
      a$coefficients[[1]]$beta_pen[1] <- 1; a$fit$coefficients <- a$coefficients
      reason <- "penalized support mismatch"
    } else if(label=="null") {
      rows$pilot_k <- a$rows$pilot_k <- a$fit$rules$pilot_k <- rep(1L,6)
      reason <- "pilot_row_metadata"
    } else if(label=="singleton" && j==1) {
      a$fit$diagnostics$v[1] <- 2*a$fit$diagnostics$v[1]
      reason <- "pilot_weights"
    } else if(label=="singleton") {
      a$fit$diagnostics$keep <- integer()
      reason <- "pilot_keep"
    } else if(j==1) {
      a$coefficients[[1]]$beta_pen[1] <- 0; a$fit$coefficients <- a$coefficients
      reason <- "failed fit coefficients not NA"
    } else {
      a$fit$beta[1] <- 0; reason <- "failed_fit_beta_NA"
    }
    actual <- tryCatch({validate_object(a,rows,x$prov$source_sha256,inp,mr,expected,ctx); "ACCEPTED"},
                       error=function(e) conditionMessage(e))
    cat("NEGATIVE",label,j,actual,"\n")
    if(!grepl(reason,actual,fixed=TRUE)) failures <- c(failures,paste(label,j,"expected",reason,"got",actual))
    local({
      tmp <- tempfile("corruption_",tmpdir=fixture); dir.create(tmp)
      on.exit(unlink(tmp,recursive=TRUE),add=TRUE)
      corrupted <- file.path(tmp,"F3")
      saveRDS(a,paste0(corrupted,".rds"),version=3)
      write.csv(rows,paste0(corrupted,".csv"),row.names=FALSE,na="NA")
      writeLines(c(paste(ctx$engine$file_sha256(paste0(corrupted,".rds")),"F3.rds",sep="  "),
                   paste(ctx$engine$file_sha256(paste0(corrupted,".csv")),"F3.csv",sep="  ")),
                 paste0(corrupted,".sha256"))
      writeLines("status corrupted-test",paste0(corrupted,".done"))
      full <- tryCatch({validate_prefix(corrupted,x$prov$source_sha256,input,manifest,code,
                                       run_id,id,5L,i,1L,"c100"); "ACCEPTED"},
                       error=function(e) conditionMessage(e))
      cat("NEGATIVE_SAVED",label,j,full,"\n")
      if(!grepl(reason,full,fixed=TRUE)) failures <<- c(failures,paste(label,j,"saved expected",reason,"got",full))
    })
  }
}
fast_id <- "fixture_p0005_S3_r001"
fast_prefix <- file.path(fixture,"results","branch_fixture","p0005",paste0(fast_id,"_c100"),"F3")
fast_input <- file.path(fixture,"inputs","p0005",paste0(fast_id,".rds"))
fast <- readRDS(paste0(fast_prefix,".rds"))
if(identical(fast$fit$runtime_s,0)) {
  why <- tryCatch({validate_prefix(fast_prefix,fast$prov$source_sha256,fast_input,manifest,code,
                                  "branch_fixture",fast_id,5L,3L,1L,"c100"); "ACCEPTED"},
                  error=function(e) conditionMessage(e))
  if(!grepl("runtime_s not one positive",why,fixed=TRUE) ||
     grepl("coefficient metadata mismatch",why,fixed=TRUE))
    failures <- c(failures,paste("zero-runtime regression:",why))
  cat("ZERO_RUNTIME_REFUSED_AS_FROZEN",why,"\n")
}
if(length(failures)) stop(paste(failures,collapse="; "))
cat("PASS 3 saved-record positives and 6 branch-specific corruptions\n")
