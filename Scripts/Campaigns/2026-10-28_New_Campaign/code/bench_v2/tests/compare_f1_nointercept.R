# Paired deployed/v2 F1 G3 no-intercept fixture, exact historical grid.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
deployed <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks/F1_Lasso"
current <- file.path(root,"repro","snapshot_2a8362b2f348","F1_Lasso")
sys.source(file.path(root,"tests","local_glmnet_compat.R"),envir=globalenv())
load_method <- function(path) {
  cfg <- new.env(parent=globalenv()); sys.source(file.path(path,"config.R"),cfg)
  s <- as.list(cfg); s$variant <- "primary"
  e <- new.env(parent=globalenv())
  for(f in c("common.R","methods/glmnet_helpers.R","methods/fit_F1_lasso.R")) sys.source(file.path(path,f),e)
  s <- install_local_glmnet(e,s)
  list(e=e,s=s)
}
old <- load_method(deployed); new <- load_method(current)
input <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S4_r001.rds"
d <- readRDS(input); X <- d$X; y <- unname(d$Y[,"c100"]); p <- ncol(X)
lam <- new$s$GRID$max_mult * max(abs(crossprod(X,y))) / nrow(X) * new$e$lambda_fraction(new$s$GRID)
get_path <- function(z, response) {
  observed <- numeric()
  original <- z$e$check_glmnet_path
  z$e$check_glmnet_path <- function(fit, lambda, G) {
    observed <<- c(observed, fit$a0)
    original(fit, lambda, G)
  }
  value <- tryCatch(z$e$glmnet_target_path(X,response,1,lam,rep(1,p),z$s$GLMNET),
                    finally={z$e$check_glmnet_path <- original})
  list(B=value$B, kkt=value$kkt, intercept=observed)
}
responses <- list(y=y, y_plus_3=y+3, centered=y-mean(y))
paths <- lapply(responses,function(yy) list(old=get_path(old,yy),new=get_path(new,yy)))
paired <- vapply(paths,function(z) identical(z$old$B,z$new$B) && identical(z$old$kkt,z$new$kkt),logical(1))
kkt <- vapply(paths,function(z) max(z$old$kkt,z$new$kkt),numeric(1))
zero <- vapply(paths,function(z) length(z$old$intercept)>0L && length(z$new$intercept)>0L &&
  all(z$old$intercept==0) && all(z$new$intercept==0),logical(1))
diff <- apply(abs(paths$y_plus_3$new$B-paths$y$new$B),2L,max)
quant <- quantile(diff,c(.5,.9,.99,1))
cat("paired identities:",paste(names(paired),paired,collapse=" "), "\n")
cat("max KKT:",paste(names(kkt),format(kkt,digits=9),collapse=" "), "\n")
cat("zero intercept:",paste(names(zero),zero,collapse=" "), "\n")
cat("per-lambda max coefficient difference quantiles:",paste(names(quant),format(quant,digits=9),collapse=" "), "\n")
cat("historical: median 2.1e-7 p90 4.1e-5 p99 1.6e-3 max 2.7e-3\n")
saveRDS(list(paired=paired,kkt=kkt,zero_intercept=zero,quantiles=quant,
             input_sha256=digest::digest(file=input,algo="sha256"),session=utils::capture.output(sessionInfo())),
        file.path(root,"tests","F1_nointercept_paired.rds"),version=3)
if(!all(paired) || any(kkt > new$s$GLMNET$kkt_rel_tol) || !all(zero)) quit(status=1L)
