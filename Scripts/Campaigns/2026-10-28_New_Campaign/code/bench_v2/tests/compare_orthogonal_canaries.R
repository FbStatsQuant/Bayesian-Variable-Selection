# Paired deployed/v2 orthogonal canaries, using the exact fixtures of their G3 suites.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
deployed <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks"
sys.source(file.path(root,"tests","local_glmnet_compat.R"),envir=globalenv())
load_method <- function(base, method) {
  folder <- if(method=="F1") "F1_Lasso" else "F2_ElasticNet"
  file <- if(method=="F1") "fit_F1_lasso.R" else "fit_F2_enet.R"
  cfg <- new.env(parent=globalenv()); sys.source(file.path(base,folder,"config.R"),cfg)
  s <- if(method=="F1") { x<-as.list(cfg); x$variant<-"primary"; x } else cfg$make_settings()
  e <- new.env(parent=globalenv())
  for(f in c("common.R","methods/glmnet_helpers.R",paste0("methods/",file)))
    sys.source(file.path(base,folder,f),e)
  s <- install_local_glmnet(e,s)
  list(e=e,s=s)
}
results <- list()
for (method in c("F1","F2")) {
  new <- load_method(root,method); old <- load_method(deployed,method)
  n <- 200L; set.seed(new$s$TEST_SEED)
  X <- sqrt(n-1)*qr.Q(qr(scale(matrix(rnorm(n*30),n),center=TRUE,scale=FALSE)))
  b <- numeric(30)
  if(method=="F1") { truth<-c(3L,7L,14L,16L,25L); b[truth]<-c(1.4,-1,1.8,-1.2,.8) }
  else { truth<-c(3L,8L,14L,21L,27L); b[truth]<-c(1.5,-1.2,1,-.8,1.3); attributes(X)<-list(dim=c(n,30L)) }
  y <- as.numeric(X%*%b+rnorm(n))
  fold <- if(method=="F1") sample(rep(1:10,length.out=n)) else rep(1:10,length.out=n)
  fn <- if(method=="F1") "fit_F1_lasso" else "fit_F2_enet"
  a <- old$e[[fn]](X,y,fold,1L,old$s)
  z <- new$e[[fn]](X,y,fold,1L,new$s)
  orig <- z$rules[match(a$rules$rule_id,z$rules$rule_id),,drop=FALSE]
  rownames(orig)<-NULL; rownames(a$rules)<-NULL
  same <- identical(a$rules,orig)
  key <- paste(truth,collapse=";")
  cv <- z$rules[z$rules$rule_id %in% c("cv_min","cv_1se"),,drop=FALSE]
  eb <- z$rules[grepl("^ebic",z$rules$rule_id),,drop=FALSE]
  contains <- all(vapply(cv$support, function(x) all(truth %in% new$e$parse_key(x)), logical(1)))
  ebic_exact <- all(eb$status != "failed") && all(eb$support == key)
  cat(method,"truth",key,"original_rows_bit_identical",same,"\n")
  cat("DEPLOYED\n"); print(a$rules[,c("rule_id","status","support")],row.names=FALSE)
  cat("V2\n"); print(z$rules[,c("rule_id","status","support")],row.names=FALSE)
  results[[method]] <- list(truth=truth, old=a$rules, new=z$rules, identical_original_rows=same,
                            cv_contains_truth=contains, ebic_exact=ebic_exact,
                            original_row_difference=if(same) NULL else all.equal(a$rules,orig,tolerance=0))
}
saveRDS(results,file.path(root,"tests","paired_orthogonal_canaries_reclassified.rds"),version=3)
if(!all(vapply(results, function(x)x$identical_original_rows && x$cv_contains_truth && x$ebic_exact,logical(1)))) quit(status=1L)
