# Migrated small-fixture F3 canaries. Ridge-only checks are listed in F3_RETIRED_TESTS.md.
script <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
root <- dirname(dirname(dirname(normalizePath(script))))
code <- file.path(root, "F3_AdaptiveLasso")
cfg <- new.env(parent = globalenv()); sys.source(file.path(code, "config.R"), cfg)
E <- new.env(parent = globalenv())
for (f in c("common.R","methods/glmnet_helpers.R","methods/fit_F3_alasso.R")) sys.source(file.path(code,f),E)
local_test <- identical(Sys.getenv("BENCH_V2_LOCAL_TEST"), "1")
if (local_test) {
  sys.source(file.path(root, "tests", "local_glmnet_compat.R"), envir = globalenv())
  S <- install_local_glmnet(E, cfg$study_settings())
} else {
  .libPaths(c(cfg$STUDY_LIB, .Library))
  S <- cfg$study_settings()
  E$assert_pkg_version("glmnet", S$GLMNET$pkg_version)
}
checks <- list()
check <- function(name, expr) {
  err <- tryCatch({force(expr); NULL}, error=function(e) conditionMessage(e))
  checks[[name]] <<- is.null(err)
  cat(if(is.null(err)) "PASS" else "FAIL", name, if(!is.null(err)) err, "\n")
}
assert <- function(x) if(!isTRUE(x)) stop("assertion failed")
set.seed(S$TEST_SEED + 2L)
n <- 200L; p <- 30L
M <- scale(matrix(rnorm(n*p),n),center=TRUE,scale=FALSE)
X <- sqrt(n-1)*qr.Q(qr(M))
truth <- c(3L,7L,14L,16L,25L); beta <- numeric(p)
beta[truth] <- c(1.4,-1,1.8,-1.2,.8)
y <- as.numeric(X %*% beta + rnorm(n)); fold <- sample(rep(1:10, length.out=n))
f <- E$fit_F3_alasso(X,y,fold,1L,S)
key <- E$support_key(truth)
cat("v2 truth", key, "cv_min", f$rules$support[1],
    "cv_min_exact", identical(f$rules$support[1], key), "\n")
check("orthogonal design", assert(max(abs(crossprod(X)-(n-1)*diag(p))) < 1e-9))
check("orthogonal cv_min contains truth", assert(all(truth %in% E$parse_key(f$rules$support[1]))))
for (rid in c("ebic1", "ebic1_K37"))
  check(paste("orthogonal exact", rid), assert(identical(f$rules$support[f$rules$rule_id == rid], key)))
dep_root <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks/F3_AdaptiveLasso"
if (local_test && dir.exists(dep_root)) {
dcfg <- new.env(parent = globalenv()); sys.source(file.path(dep_root, "config.R"), dcfg)
DE <- new.env(parent = globalenv())
for (file in c("common.R","methods/glmnet_helpers.R","methods/fit_F3_alasso.R"))
  sys.source(file.path(dep_root,file),DE)
DS <- install_local_glmnet(DE, dcfg$study_settings())
old <- DE$fit_F3_alasso(X,y,fold,1L,DS)
for (label in c("v2", "ridge")) {
  obj <- if (label == "v2") f else old
  for (i in seq_len(nrow(obj$rules)))
    cat("canary", label, obj$rules$rule_id[i], "status", obj$rules$status[i],
        "support", obj$rules$support[i], "exact", identical(obj$rules$support[i], key), "\n")
}
ridge_candidates <- old$diagnostics$candidates
ridge_candidates <- ridge_candidates[ridge_candidates$k <= floor(n/log(n)), , drop = FALSE]
for (g in c("ebic1", "ebic05")) {
  j <- DE$ebic_pick(ridge_candidates, g); picked <- ridge_candidates$key[j]
  good <- DE$occurrence_ok(picked, old$diagnostics$path$key,
                           old$diagnostics$path$kkt_full <= DS$GLMNET$kkt_rel_tol)
  cat("canary ridge", paste0(g, "_K37"), "status", if (good) "ok" else "failed",
      "support", picked, "exact", identical(picked, key), "\n")
}
} else cat("deployed ridge side-by-side unavailable in this environment\n")
check("orthogonal pilot and screened output", {
  assert(all(f$rules$status != "failed"))
  assert(length(f$diagnostics$keep) > 1L)
  assert(f$diagnostics$path$k[1] == 0L)
  assert(abs(sum(f$diagnostics$v)-length(f$diagnostics$keep)) <= 1e-10*length(f$diagnostics$keep))
})
check("orthogonal weighted soft-threshold", {
  k <- f$diagnostics$keep; xx <- X[,k,drop=FALSE]; z <- drop(crossprod(xx,y))/n
  lam <- f$diagnostics$path$lambda; v <- f$diagnostics$v
  path <- E$glmnet_target_path(xx,y,1,lam,v,S$GLMNET)
  ref <- vapply(lam,function(l) sign(z)*pmax(abs(z)-l*v,0)/((n-1)/n),numeric(length(k)))
  assert(max(abs(path$B-ref)) <= 1e-8*max(1,max(abs(z))))
})
check("no-intercept weighted full paths", {
  k <- f$diagnostics$keep; xx <- X[,k,drop=FALSE]; v <- f$diagnostics$v
  lam <- f$diagnostics$path$lambda; y3 <- y+3; yc <- y3-mean(y3)
  a <- E$glmnet_target_path(xx,y3,1,lam,v,S$GLMNET)
  b <- E$glmnet_target_path(xx,yc,1,lam,v,S$GLMNET)
  assert(max(abs(a$B-b$B)) <= 1e-8)
  scale <- max(1,max(abs(crossprod(xx,yc)))/n)
  assert(max(E$kkt_glmnet(xx,yc,a$B,lam,1,v,scale)) <= S$GLMNET$kkt_rel_tol)
})
check("no-intercept RSS identity", {
  y3 <- y+3; yc <- y3-mean(y3)
  supports <- unique(f$diagnostics$path$key)
  for (key0 in supports) {
    idx <- E$parse_key(key0)
    a <- E$ols_rss(X,y3,idx,S$COMMON$ols_tol)$rss
    b <- E$ols_rss(X,yc,idx,S$COMMON$ols_tol)$rss
    assert(abs(a-(b+n*mean(y3)^2)) <= 1e-9*max(1,a))
  }
})
check("null noise canary", {
  set.seed(20261020); f0 <- E$fit_F3_alasso(X,rnorm(n),fold,1L,S)
  assert(all(f0$rules$status != "failed")); assert(all(f0$rules$k <= .3*p))
})
check("deterministic repeated fit", {
  again <- E$fit_F3_alasso(X,y,fold,1L,S)
  assert(identical(f$rules,again$rules)); assert(identical(f$beta,again$beta))
  assert(identical(f$diagnostics$pilot$cvm,again$diagnostics$pilot$cvm))
})
check("solver failure frame", {
  bad <- S; bad$GLMNET$maxit <- 1
  z <- E$fit_F3_alasso(X,y,fold,1L,bad)
  assert(all(z$rules$status == "failed")); assert(all(is.na(z$beta)))
})
check("invalid input rejected", {
  bad <- X; bad[,1] <- bad[,1]+1
  assert(inherits(tryCatch(E$fit_F3_alasso(bad,y,fold,1L,S),error=identity),"error"))
})
check("runner outer failure captures bad input and NA evidence", {
  rc <- new.env(parent=globalenv()); sys.source(file.path(code,"run_case.R"),rc)
  bad <- X; bad[,1] <- bad[,1]+1
  meth <- S$METHODS[S$METHODS$method_id == "F3",,drop=FALSE]
  z <- rc$run_one_fit(meth,E,bad,y,fold,1L,S)
  assert(all(z$rules$status == "failed"))
  assert(all(vapply(z$coefficients,function(c) all(is.na(c$beta_pen)),logical(1))))
})
check("version failure remains a failed fit", {
  rc <- new.env(parent=globalenv()); sys.source(file.path(code,"run_case.R"),rc)
  bad <- S; bad$GLMNET$pkg_version <- "0.0"
  meth <- bad$METHODS[bad$METHODS$method_id == "F3",,drop=FALSE]
  z <- rc$run_one_fit(meth,E,X,y,fold,1L,bad)
  assert(all(z$rules$status == "failed"))
  assert(all(vapply(z$coefficients,function(c) all(is.na(c$beta_pen)),logical(1))))
})
cat("F3 migrated canaries:",sum(unlist(checks)),"/",length(checks),"passed\n")
if (!all(unlist(checks))) quit(status=1L)
