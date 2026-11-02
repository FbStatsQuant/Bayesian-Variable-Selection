args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==2L)
campaign <- normalizePath(args[1],mustWork=TRUE)
out <- normalizePath(args[2],mustWork=TRUE)
wrapper <- file.path(campaign,"code/bench_v2/tests/run_local_runner.R")
code <- file.path(campaign,"code/bench_v2/F3_AdaptiveLasso")
# Execute the existing wrapper setup exactly; omit only its hard-coded final main/quit.
expr <- parse(wrapper)
scope <- new.env(parent=globalenv())
for (statement in head(expr,-2L)) eval(statement,scope)
rc <- scope$e
engine <- new.env(parent=asNamespace("stats"))
sys.source(file.path(code,"common.R"),engine)
n <- 200L; p <- 5L
fold <- rep(seq_len(10L),each=20L)
t <- rep(0:19,10L)
X <- sapply(seq_len(p),function(j) cos(2*pi*j*t/20))
X <- sweep(X,2,colMeans(X),"-")
X <- sweep(X,2,sqrt(colSums(X^2)/(n-1)),"/")
storage.mode(X) <- "double"
noise <- cos(2*pi*6*t/20)
ynull <- (ifelse(fold %% 2L == 0L,1,-1)+0.001)*X[,1]
ysingle <- 3*X[,1] + 0.2*noise
Xbad <- X; Xbad[,1] <- Xbad[,1] + 0.1
cases <- list(null=list(X=X,y=ynull), singleton=list(X=X,y=ysingle),
              failed=list(X=Xbad,y=ysingle))
inputdir <- file.path(out,"inputs","p0005")
dir.create(inputdir,recursive=TRUE,showWarnings=FALSE)
manifest_path <- file.path(out,"inputs_manifest.csv")
if(file.exists(manifest_path)) stop("fixture manifest already exists; do not overwrite")
records <- list()
for (i in seq_along(cases)) {
  label <- names(cases)[i]; id <- sprintf("fixture_p0005_S%d_r001",i)
  seed <- 20261030L+i
  inp <- list(dataset_id=id,p=p,scenario=as.integer(i),replicate=1L,
              data_seed=seed,fold_seed=seed+2000000L,method_seed=seed+4000000L,
              X=cases[[i]]$X,foldid=as.integer(fold),
              Y=matrix(cases[[i]]$y,ncol=1L,dimnames=list(NULL,"c100")),
              scales=c(c100=1))
  path <- file.path(inputdir,paste0(id,".rds"))
  saveRDS(inp,path,version=3)
  records[[i]] <- data.frame(dataset_id=id,p=p,scenario=i,replicate=1L,
    data_seed=inp$data_seed,fold_seed=inp$fold_seed,method_seed=inp$method_seed,
    file_sha256=engine$file_sha256(path),x_sha256=engine$f64_sha256(inp$X),
    foldid_sha256=engine$f64_sha256(inp$foldid),y_c100_sha256=engine$f64_sha256(inp$Y[,1]))
}
write.csv(do.call(rbind,records),manifest_path,row.names=FALSE)
for (i in seq_along(cases)) {
  label <- names(cases)[i]; id <- records[[i]]$dataset_id
  input <- file.path(inputdir,paste0(id,".rds"))
  status <- rc$main(c("--input",input,"--out",out,"--run-id","branch_fixture",
                      "--scale","c100","--methods","F3","--manifest",manifest_path))
  if(status!=0L) stop("runner returned ",status," for ",label)
  prefix <- file.path(out,"results","branch_fixture","p0005",paste0(id,"_c100"),"F3")
  x <- readRDS(paste0(prefix,".rds"))
  if(label=="null") stopifnot(length(x$fit$diagnostics$keep)==0L, all(grepl("pilot_null",x$rows$diag_codes)))
  if(label=="singleton") stopifnot(length(x$fit$diagnostics$keep)==1L, all(grepl("pilot_single",x$rows$diag_codes)))
  if(label=="failed") stopifnot(all(x$rows$status=="failed"), all(is.na(x$fit$beta)),
                                all(vapply(x$coefficients,function(z) all(is.na(z$beta_pen)),logical(1))))
  cat("FIXTURE_BRANCH_PASS",label,prefix,"\n")
}
