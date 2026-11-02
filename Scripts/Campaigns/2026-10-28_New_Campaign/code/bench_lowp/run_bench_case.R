# Production LOWP runner. The fit adapters are unchanged.
threads <- c("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS","BLIS_NUM_THREADS")
do.call(Sys.setenv, as.list(setNames(rep("1",length(threads)),threads)))
script <- sub("^--file=","",grep("^--file=",commandArgs(FALSE),value=TRUE)[1])
code <- dirname(normalizePath(script,winslash="/"))
source(file.path(code,"R","config_lowp.R")); source(file.path(code,"R","common.R"))
sha <- function(f) digest::digest(file=f,algo="sha256")
utc <- function() format(Sys.time(),"%Y-%m-%dT%H:%M:%SZ",tz="UTC")
fallback <- function(x,y) if(is.null(x)) y else x
parse_cli <- function(a) {
  vals <- c("--study","--outroot","--run-id","--case","--scale","--methods","--manifest","--library")
  flags <- c("--development","--threads-check","--no-manifest","--test-library")
  o <- list(); i <- 1L
  while(i<=length(a)) {
    k <- a[i]; if(!k %in% c(vals,flags) || !is.null(o[[k]])) stop("Unknown or repeated option: ",k)
    if(k %in% flags) {o[[k]] <- TRUE; i <- i+1L} else {
      if(i==length(a) || startsWith(a[i+1L],"--")) stop("Missing value: ",k)
      o[[k]] <- a[i+1L]; i <- i+2L
    }
  }
  for(k in c("--study","--outroot","--run-id","--case","--scale")) if(is.null(o[[k]])) stop("Missing ",k)
  if(!is.null(o[["--manifest"]]) && isTRUE(o[["--no-manifest"]])) stop("Conflicting manifest flags")
  o
}
check_path <- function(x) {
  for(path in c(x,normalizePath(x,winslash="/",mustWork=FALSE)))
    if(any(tolower(strsplit(gsub("\\\\","/",path),"/",fixed=TRUE)[[1]]) %in% c("truth","holdout")))
      stop("Forbidden path component")
}
atomic <- function(path,write) {
  tmp <- tempfile(paste0(".",basename(path)),tmpdir=dirname(path))
  on.exit(unlink(tmp),add=TRUE); write(tmp)
  if(!file.rename(tmp,path)) stop("Rename failed: ",path)
}
fail_registered <- function(mod,id,msg) {
  s <- mod$settings; r <- mod$registry; f <- mod$env$fail_rows
  rows <- switch(id,F1=f(s$METHODS,id),
    F2=f(r,msg,mod$env$F2_EXTRA_COLS), F3=f(r,msg),
    F4=f(r,s$F4_EXTRA_COLS,msg), F5=f(s,id,NA,NA),
    A1=f(r$rule_ids[[1]],r$roles[[1]],reason=msg),
    A2=f(r$rule_ids[[1]],r$roles[[1]],reason=msg), A3=f(s,id,msg))
  rows$error <- msg; rows
}
main <- function(args) {
  o <- parse_cli(args); study <- o[["--study"]]; out <- o[["--outroot"]]
  rid <- o[["--run-id"]]; id <- o[["--case"]]; scale <- o[["--scale"]]
  for(path in c(study,out,o[["--manifest"]])) check_path(path)
  if(!grepl("^[A-Za-z0-9_-]+$",rid) || !scale %in% c("c100","c050")) stop("Invalid run ID or scale")
  v <- regmatches(id,regexec("^(dev_)?p(0020|0030)_S([1-6])_r([0-9]{3})$",id))[[1]]
  if(length(v)!=5L || (nzchar(v[2]) != isTRUE(o[["--development"]]))) stop("Invalid case or development mode")
  p <- as.integer(v[3]); s <- as.integer(v[4]); r <- as.integer(v[5]); dev <- isTRUE(o[["--development"]])
  if (!dev && isTRUE(o[["--no-manifest"]])) stop("Production requires a manifest")
  test_library <- isTRUE(o[["--test-library"]])
  if (Sys.getenv("LOWP_SMOKE_ALLOW_VERSION_MISMATCH") == "1" && !test_library) stop("Version override requires --test-library")
  lib <- o[["--library"]]
  if (!dev && is.null(lib)) stop("Production requires --library")
  if (!is.null(lib)) { lib <- normalizePath(lib,winslash="/",mustWork=TRUE); .libPaths(c(lib,.libPaths())) }
  if(r<1L || r>if(dev) 5L else 100L) stop("Invalid replicate")
  methods <- c("F1","F2","F3","F4","F5","A1","A2","A3")
  selected <- fallback(o[["--methods"]],"all")
  selected <- if(selected=="all") methods else strsplit(selected,",",fixed=TRUE)[[1]]
  if(!length(selected) || any(!selected %in% methods) || anyDuplicated(selected)) stop("Invalid methods")
  if(!all(Sys.getenv(threads)=="1")) stop("Thread assertion failed")
  if(isTRUE(o[["--threads-check"]])) cat("Threads:",paste(threads,Sys.getenv(threads),sep="=",collapse=" "),"\n")
  input <- file.path(study,"inputs",sprintf("p%04d",p),paste0(id,".rds"))
  manifest <- fallback(o[["--manifest"]],file.path(study,"manifests","inputs_manifest_lowp.csv"))
  check_path(input); check_path(manifest)
  z <- readRDS(input)
  data_seed <- (if(p==20L) 1210000L else 1310000L)+if(dev) 1000000L else 0L
  fold_seed <- (if(p==20L) 3210000L else 3310000L)+if(dev) 1000000L else 0L
  data_seed <- data_seed+10000L*s+r; fold_seed <- fold_seed+10000L*s+r; seed <- data_seed+4000000L
  if(!identical(z$dataset_id,id) || !identical(dim(z$X),c(200L,p)) || !identical(dim(z$Y),c(200L,5L)) ||
     !identical(colnames(z$Y),c("c100","c075","c050","c035","c025")) || length(z$foldid)!=200L ||
     z$p!=p || z$scenario!=s || z$replicate!=r || z$data_seed!=data_seed || z$fold_seed!=fold_seed || z$method_seed!=seed)
    stop("Input identity, dimensions or seeds invalid")
  hashes <- c(file_sha256=sha(input),x_sha256=lowp_hash(z$X),
    setNames(vapply(colnames(z$Y),function(k) lowp_hash(z$Y[,k]),""),paste0("y_",colnames(z$Y),"_sha256")),
    fold_sha256=lowp_hash(z$foldid))
  if(!isTRUE(o[["--no-manifest"]])) {
    m <- read.csv(manifest,stringsAsFactors=FALSE); m <- m[m$dataset_id==id,,drop=FALSE]
    if(nrow(m)!=1L || any(!names(hashes) %in% names(m)) || any(unname(hashes)!=as.character(unlist(m[1,names(hashes)]))))
      stop("Input manifest hash mismatch")
    expected <- list(p=p,scenario=s,replicate=r,data_seed=data_seed,fold_seed=fold_seed,method_seed=seed)
    for(nm in names(expected)) if(!nm %in% names(m) || is.na(m[[nm]]) || m[[nm]]!=expected[[nm]]) stop("Manifest identity mismatch: ",nm)
  }
  files <- sort(c(list.files(code,pattern="\\.R$",recursive=TRUE,full.names=TRUE),file.path(code,"R","SOURCES_SHA256.txt")))
  shas <- setNames(vapply(files,sha,""),substring(gsub("\\\\","/",files),nchar(code)+2L))
  source_sha <- digest::digest(paste(names(shas),shas,sep="  ",collapse="\n"),algo="sha256",serialize=FALSE)
  case <- paste0(id,"_",scale); dir <- file.path(out,"results",rid,sprintf("p%04d",p),case)
  dir.create(dir,recursive=TRUE,showWarnings=FALSE); if(!dir.exists(dir)) stop("Cannot create output")
  result <- 0L
  package_cache <- new.env(parent=emptyenv())
  for(mid in selected) {
    mod <- lowp_load_method(mid,code,p,test_library); reg <- mod$registry
    pins <- if(mid=='A3') mod$settings$A3$PKG_VERSIONS else setNames(reg$pkg_version,reg$package)
    for(pkg in names(pins)) mod$env$assert_pkg_version(pkg,unname(pins[[pkg]]))
    # Resolve the installed dependency closure and bind the unit to package contents and provenance.
    db <- utils::installed.packages()
    deps <- unique(c(names(pins),'digest',unlist(tools::package_dependencies(c(names(pins),'digest'),db=db,recursive=TRUE))))
    deps <- intersect(deps,rownames(db)); info <- list()
    for(pkg in sort(deps)) {
      loc <- normalizePath(find.package(pkg),winslash='/',mustWork=TRUE)
      base_lib <- normalizePath(.Library,winslash='/',mustWork=TRUE)
      is_base <- identical(normalizePath(dirname(loc),winslash='/'),base_lib) && db[pkg,'Priority'] %in% c('base','recommended')
      if(!dev && !test_library && !is_base && !identical(normalizePath(dirname(loc),winslash='/'),lib)) stop('Package outside sealed library: ',pkg,' ',loc)
      if(pkg %in% loadedNamespaces() && !identical(normalizePath(getNamespaceInfo(asNamespace(pkg),'path'),winslash='/'),loc)) stop('Loaded namespace path mismatch: ',pkg)
      if(exists(loc,envir=package_cache,inherits=FALSE)) { info[[pkg]] <- get(loc,envir=package_cache); next }
      ff <- sort(list.files(loc,recursive=TRUE,full.names=TRUE,all.files=FALSE)); ff <- ff[!dir.exists(ff)]
      rel <- substring(gsub('\\\\','/',ff),nchar(loc)+2L)
      keep <- rel %in% c('DESCRIPTION','NAMESPACE') | grepl('^(R|libs|Meta|data)/',rel)
      ff <- ff[keep]; rel <- rel[keep]
      info[[pkg]] <- list(path=loc,version=as.character(packageVersion(pkg)),built=db[pkg,'Built'],files=setNames(vapply(ff,sha,''),rel))
      assign(loc,info[[pkg]],envir=package_cache)
    }
    env_identity <- digest::digest(list(R=R.version.string,lib=lib,lib_paths=.libPaths(),test_library=test_library,packages=info),algo='sha256')
    prefix <- file.path(dir,mid); lock <- paste0(prefix,".lock")
    if(!dir.create(lock,showWarnings=FALSE)) stop("Unit locked: ",lock)
    tryCatch({
      paths <- paste0(prefix,c(".rds",".csv",".sha256",".done"))
      expect <- list(run_id=rid,case_id=case,method_id=mid,method_seed=seed,
        environment_sha256=env_identity,inputs_sha256=hashes[["file_sha256"]],x_sha256=hashes[["x_sha256"]],
        y_sha256=hashes[[paste0("y_",scale,"_sha256")]],fold_sha256=hashes[["fold_sha256"]],source_sha256=source_sha)
      if(file.exists(paths[4])) {
        if(!all(file.exists(paths))) stop("Incomplete completed unit")
        if(!identical(readLines(paths[3],warn=FALSE),paste(vapply(paths[1:2],sha,""),basename(paths[1:2]),sep="  "))) stop("Checksum mismatch")
        rows <- readRDS(paths[1])$rows
        csvrows <- read.csv(paths[2],stringsAsFactors=FALSE,colClasses="character")
        for(frame in list(rows,csvrows)) {
          if(!is.data.frame(frame) || !nrow(frame) || any(!names(expect) %in% names(frame))) stop("Invalid saved rows")
          for(nm in names(expect)) if(any(is.na(frame[[nm]]) | as.character(frame[[nm]])!=as.character(expect[[nm]]))) stop("Resume identity mismatch: ",nm)
        }
        if(any(rows$status=="failed")) result <- 2L
        cat(case,mid,"skipped\n")
      } else {
        if(any(file.exists(paths[1:3]))) stop("Incomplete unit requires manual repair")
        RNGkind("Mersenne-Twister","Inversion","Rejection"); set.seed(seed)
        started <- utc(); t0 <- proc.time()[["elapsed"]]; warnings <- messages <- character()
        fit <- tryCatch(withCallingHandlers(mod$fn(z$X,z$Y[,scale],z$foldid,seed,mod$settings),
          warning=function(w){warnings <<- c(warnings,conditionMessage(w)); invokeRestart("muffleWarning")},
          message=function(m){messages <<- c(messages,conditionMessage(m)); invokeRestart("muffleMessage")}),error=function(e)e)
        runtime <- unname(proc.time()[["elapsed"]]-t0); finished <- utc()
        if(inherits(fit,"error")) {
          err <- conditionMessage(fit); if(grepl("cannot allocate",err,fixed=TRUE)) stop(err)
          fit <- list(rules=fail_registered(mod,mid,err),beta=rep(NA_real_,p),pip=NULL,error=err)
        }
        rows <- fit$rules
        if(!is.data.frame(rows) || !identical(as.character(rows$rule_id),as.character(reg$rule_ids[[1]])) ||
           !identical(as.character(rows$role),as.character(reg$roles[[1]]))) stop("Wrapper rule registry mismatch")
        outer_warnings <- warnings; outer_messages <- messages
        if(!"error" %in% names(rows)) rows$error <- fallback(fit$error,NA_character_)
        # A3 already classifies captured conditions by rule; its legacy aggregate mixes types.
        if(mid != 'A3') {
          warnings <- c(warnings,fallback(fit$warnings,character())); messages <- c(messages,fallback(fit$messages,character()))
        }
        warnings <- warnings[!is.na(warnings) & nzchar(warnings)]; messages <- messages[!is.na(messages) & nzchar(messages)]
        if(!'n_warnings' %in% names(rows)) rows$n_warnings <- 0L
        if(!'warnings' %in% names(rows)) rows$warnings <- ''
        if(!'messages' %in% names(rows)) rows$messages <- ''
        append_text <- function(old, new) { if(!length(new)) return(old); vapply(old,function(x) paste(c(if(!is.na(x) && nzchar(x)) x,new),collapse=' | '),'') }
        rows$n_warnings <- rows$n_warnings + length(warnings)
        rows$warnings <- append_text(rows$warnings,warnings); rows$messages <- append_text(rows$messages,messages)
        if(length(warnings) || length(messages)) rows$status[rows$status=='ok'] <- 'warning'
        fit$rules <- rows
        rows <- lowp_derive(fit,mid,p,nrow(z$X),scale)
        if (mid %in% c('F4','F5')) fit$coefficients <- lowp_coefficients(fit,rows,mid,z$X,z$Y[,scale],mod$settings$COMMON$ols_tol)
        if (mid %in% c('F1','F2','F3')) {
          if (is.null(fit$coefficients)) {
            fit$coefficients <- setNames(lapply(seq_len(nrow(rows)), function(i)
              list(rule_id=rows$rule_id[i],status=rows$status[i],support=NA_character_,k=NA_integer_,index=NA_integer_,lambda=NA_real_,alpha=NA_real_,beta_pen=rep(NA_real_,p),beta_ols=rep(NA_real_,p))),rows$rule_id)
          } else for (i in seq_len(nrow(rows))) fit$coefficients[[rows$rule_id[i]]]$status <- rows$status[i]
        }
        for(nm in c('tp','fp','fn','exact','error_type',sprintf('sel_a%02d',1:14),sprintf('pip_a%02d',1:14),'max_pip_null')) rows[[nm]] <- NA
        adapt <- if(mid=="F5") "LA-1;LA-2;LA-4" else if(mid %in% c("F1","F2","F3","F4")) "LA-1;LA-4" else if(mid=="A1") "LA-3" else "none"  # LA-4 = PREREG derived rows (RECHECK_c N3)
        design <- c(list(study="newcampaign_lowp",regime="L",p=p,scenario=s,replicate=r,scale_key=scale,
          scale=if(scale=="c100") 1 else .5,dataset_id=id,data_seed=data_seed,fold_seed=fold_seed),expect,
          list(method_label=reg$method_label,package=reg$package,
          package_version=if(requireNamespace(reg$package,quietly=TRUE)) as.character(packageVersion(reg$package)) else NA_character_,
          adaptation_ids=adapt,test_library=test_library,runtime_s=runtime,host=Sys.info()[["nodename"]],
          slurm_job_id=Sys.getenv("SLURM_JOB_ID",NA),slurm_array_task_id=Sys.getenv("SLURM_ARRAY_TASK_ID",NA),
          started_utc=started,finished_utc=finished))
        for(nm in names(design)) rows[[nm]] <- design[[nm]]
        if(any(!rows$status %in% c("ok","warning","failed")) || any(rows$status=="failed" & (!is.na(rows$support) | !is.na(rows$k)))) stop("Invalid failed selection")
        pkgs <- loadedNamespaces(); versions <- setNames(vapply(pkgs,function(k) as.character(packageVersion(k)),""),pkgs)
        record <- list(schema_version=2L,rows=rows,fit=fit,coefficients=fit$coefficients,outer_warnings=outer_warnings,outer_messages=outer_messages,code=list(source_sha256=source_sha,files=shas),
          input=list(path=normalizePath(input,winslash="/"),hashes=hashes,manifest=if(isTRUE(o[["--no-manifest"]])) NULL else normalizePath(manifest,winslash="/")),
          environment=list(identity=env_identity,package_provenance=info,sealed_library=lib,test_library=test_library,packages=versions,sessionInfo=capture.output(sessionInfo()),threads=as.list(Sys.getenv(threads)),
            RNGkind=RNGkind(),command_line=commandArgs(),lib_paths=.libPaths()),started_utc=started,finished_utc=finished)
        atomic(paths[1],function(f) saveRDS(record,f)); atomic(paths[2],function(f) write.csv(rows,f,row.names=FALSE,na="NA"))
        atomic(paths[3],function(f) writeLines(paste(vapply(paths[1:2],sha,""),basename(paths[1:2]),sep="  "),f))
        atomic(paths[4],function(f) writeLines(c(paste("status",paste(rows$status,collapse=",")),paste("finished_utc",finished)),f))
        if(any(rows$status=="failed")) result <- 2L
        cat(case,mid,paste(rows$status,collapse=","),runtime,"\n")
      }
    },finally=unlink(lock,recursive=TRUE))
  }
  result
}
status <- tryCatch(main(commandArgs(TRUE)),error=function(e){message("FATAL: ",conditionMessage(e)); 1L})
quit(save="no",status=status)
