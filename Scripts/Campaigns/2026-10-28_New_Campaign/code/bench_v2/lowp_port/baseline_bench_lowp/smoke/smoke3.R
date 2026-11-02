# Run after sealing bench_study with lowp_seal.R; all outputs remain in temp.
root <- "C:/Users/felip/AppData/Local/Temp/lowp_work"
study <- file.path(root,"bench_study"); out <- file.path(root,"bench_smoke_reviewfix_v6")
dir.create(out,recursive=TRUE,showWarnings=FALSE)
self <- sub("^--file=","",grep("^--file=",commandArgs(FALSE),value=TRUE)[1])
code <- dirname(dirname(normalizePath(self,winslash="/")))
runner <- file.path(code,"run_bench_case.R"); R <- file.path(R.home("bin"),"Rscript.exe")
Sys.setenv(R_LIBS="C:/Users/felip/AppData/Local/Temp/lowp_Rlib")
invoke <- function(st,rid,id,scale,methods="all",extra=character(),script=runner,label) {
  args <- c(shQuote(script),"--study",shQuote(st),"--outroot",shQuote(out),"--run-id",rid,
            "--case",id,"--scale",scale,"--methods",methods,"--library",shQuote("C:/Users/felip/AppData/Local/Temp/lowp_Rlib"),"--test-library",extra)
  log <- file.path(out,paste0(label,".log")); rc <- system2(R,args,stdout=log,stderr=log)
  cat(label,"exit",rc,"\n"); flush.console(); rc
}
results <- list()
check <- function(label,ok) {
  results[[length(results)+1L]] <<- data.frame(test=label,pass=isTRUE(ok))
  if(!isTRUE(ok)) cat("FAILED:",label,"\n")
}
cases <- c("p0020_S1_r001","p0030_S4_r050","p0030_S6_r100")
for(id in cases) for(scale in c("c100","c050")) {
  label <- paste(id,scale,sep="_"); rc <- invoke(study,"smoke",id,scale,label=label)
  check(label,rc==0L)
  for(mid in c("F1","F2","F3","F4","F5","A1","A2","A3")) {
    prefix <- file.path(out,"results","smoke",substr(id,1,5),label,mid)
    paths <- paste0(prefix,c(".rds",".csv",".sha256",".done")); ok <- all(file.exists(paths))
    if(ok) {
      rec <- readRDS(paths[1]); actual <- paste(vapply(paths[1:2],function(f) digest::digest(file=f,algo="sha256"),""),basename(paths[1:2]),sep="  ")
      ok <- identical(readLines(paths[3],warn=FALSE),actual) && all(rec$rows$status %in% c("ok","warning")) &&
        length(rec$code$files)>0 && !is.null(rec$fit) && all(c("study","run_id","source_sha256","regime","method_seed","adaptation_ids") %in% names(rec$rows))
    }
    check(paste(label,mid),ok)
  }
}
id <- cases[1]; case <- paste0(id,"_c100"); prefix <- file.path(out,"results","smoke","p0020",case,"F1")
paths <- paste0(prefix,c(".rds",".csv",".sha256",".done"))
before <- vapply(paths,function(f) digest::digest(file=f,algo="sha256"),"")
rc <- invoke(study,"smoke",id,"c100","F1",label="resume")
check("resume",rc==0L && identical(before,vapply(paths,function(f) digest::digest(file=f,algo="sha256"),"")))
rc <- invoke(file.path(study,"dev"),"dev","dev_p0020_S1_r001","c100","F1",extra="--development",label="dev")
check("development",rc==0L)
bad <- file.path(out,"tampered_study")
dir.create(file.path(bad,"inputs","p0020"),recursive=TRUE,showWarnings=FALSE)
dir.create(file.path(bad,"manifests"),recursive=TRUE,showWarnings=FALSE)
src <- file.path(study,"inputs","p0020",paste0(id,".rds")); dst <- file.path(bad,"inputs","p0020",paste0(id,".rds"))
file.copy(src,dst,overwrite=TRUE); Sys.chmod(dst,"0644"); z <- readRDS(dst); z$X[1,1] <- z$X[1,1]+1; saveRDS(z,dst,compress=FALSE)
file.copy(file.path(study,"manifests","inputs_manifest_lowp.csv"),file.path(bad,"manifests","inputs_manifest_lowp.csv"),overwrite=TRUE)
rc <- invoke(bad,"tamper",id,"c100","F1",label="tamper")
check("tampered input",rc==1L && !dir.exists(file.path(out,"results","tamper")))
copy <- file.path(out,"forced_code"); dir.create(copy,recursive=TRUE,showWarnings=FALSE)
file.copy(file.path(code,"run_bench_case.R"),copy,overwrite=TRUE)
file.copy(file.path(code,"R"),copy,recursive=TRUE,overwrite=TRUE)
cat('\nfit_F1_lasso <- function(...) stop("forced wrapper error")\n',file=file.path(copy,"R","methods","fit_F1_lasso.R"),append=TRUE)
rc <- invoke(study,"forced",id,"c100","F1",script=file.path(copy,"run_bench_case.R"),label="forced")
f <- file.path(out,"results","forced","p0020",case,"F1.rds"); rec <- if(file.exists(f)) readRDS(f) else NULL
check("forced wrapper error",rc==2L && !is.null(rec) && nrow(rec$rows)==6L &&
  all(rec$rows$status=="failed") && all(is.na(rec$rows$support)) && all(grepl("forced wrapper error",rec$rows$error)))
backup <- file.path(out,"identity_backup"); dir.create(backup,showWarnings=FALSE)
file.copy(paths, backup, overwrite=TRUE)
rec <- readRDS(paths[1]); rec$rows$run_id <- "wrong"; saveRDS(rec,paths[1])
writeLines(paste(vapply(paths[1:2],function(f) digest::digest(file=f,algo="sha256"),""),basename(paths[1:2]),sep="  "),paths[3])
rc <- invoke(study,"smoke",id,"c100","F1",label="identity")
check("resume identity mismatch",rc==1L)
file.copy(file.path(backup,basename(paths)),paths,overwrite=TRUE)
check("identity test restored output", identical(before,vapply(paths,function(f) digest::digest(file=f,algo="sha256"),"")))
table <- do.call(rbind,results); write.csv(table,file.path(out,"validation.csv"),row.names=FALSE)
cat("Passed",sum(table$pass),"of",nrow(table),"\n")
quit(status=if(all(table$pass)) 0L else 1L)
