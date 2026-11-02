#!/usr/bin/env Rscript
# Shared task/reconciliation validator. Reads only the supplied frozen input and manifest.
same <- function(a, b, tol=1e-10)
  isTRUE(all.equal(a, b, tolerance=tol, check.attributes=FALSE))
need <- function(ok, why) if (!isTRUE(ok)) stop(why, call.=FALSE)
key <- function(b) paste(which(b != 0), collapse=";")

load_frozen_validator <- function(code) {
  cfg <- new.env(parent=globalenv())
  sys.source(file.path(code,"config.R"), cfg)
  rc <- new.env(parent=globalenv())
  sys.source(file.path(code,"run_case.R"), rc)
  engine <- new.env(parent=asNamespace("stats"))
  sys.source(file.path(code,"common.R"), engine)
  sys.source(file.path(code,"methods","glmnet_helpers.R"), engine)
  checker <- new.env(parent=globalenv())
  sys.source(file.path(code,"tests","validate_outputs.R"), checker)
  # read.csv infers an all-NA integer column as logical. Preserve values while
  # restoring the registry's integer k type before calling the frozen checker.
  frozen_payload <- checker$validate_payload
  checker$validate_payload <- function(rds,rows,settings,engine) {
    if(is.logical(rows$k) && all(is.na(rows$k))) rows$k <- as.integer(rows$k)
    frozen_payload(rds,rows,settings,engine)
  }
  list(cfg=cfg, rc=rc, engine=engine, checker=checker)
}

validate_object <- function(x, rows, source, inp, manifest_row, expected, ctx) {
  need(is.list(x) && identical(x$schema_version,2L), "schema_version")
  need(is.data.frame(rows) && nrow(rows)==6L && is.data.frame(x$rows), "rule_count")
  need(identical(names(rows),names(x$rows)), "CSV_RDS_columns")
  for (column in names(rows))
    need(same(rows[[column]],x$rows[[column]]), paste0("CSV_RDS_",column))
  need(identical(x$prov$source_sha256,source) && all(rows$source_sha256==source), "source_sha256")
  for (nm in names(expected)) {
    need(nm %in% names(rows) && all(as.character(rows[[nm]]) == as.character(expected[[nm]])), paste0("expected_",nm))
    if (nm %in% names(x$case)) need(same(x$case[[nm]],expected[[nm]]),paste0("RDS_case_",nm))
    if (nm %in% names(x$prov)) need(same(x$prov[[nm]],expected[[nm]]),paste0("RDS_prov_",nm))
  }
  for(nm in names(x$prov))
    if(nm %in% names(rows)) need(all(vapply(rows[[nm]],function(v) same(v,x$prov[[nm]]),logical(1))),paste0("provenance_",nm))
  need(nrow(manifest_row)==1L, "manifest_dataset")
  for (nm in c("data_seed","fold_seed","method_seed")) {
    need(nm %in% names(manifest_row) && nm %in% names(inp) &&
         nm %in% names(x$case) && nm %in% names(rows) &&
         length(inp[[nm]])==1L && !is.na(inp[[nm]]) &&
         length(x$case[[nm]])==1L && !is.na(x$case[[nm]]) &&
         length(manifest_row[[nm]])==1L && !is.na(manifest_row[[nm]][1]) &&
         !anyNA(rows[[nm]]) && same(inp[[nm]],manifest_row[[nm]][1],0) &&
         same(x$case[[nm]],manifest_row[[nm]][1],0) &&
         all(vapply(rows[[nm]],function(v) same(v,manifest_row[[nm]][1],0),logical(1))),
         paste0("seed_binding_",nm))
  }
  for (nm in c("dataset_id","p","scenario","replicate","data_seed","fold_seed","method_seed"))
    need(same(inp[[nm]],manifest_row[[nm]][1]),paste0("manifest_",nm))
  maps <- c(inputs_sha256="file_sha256",x_sha256="x_sha256",fold_sha256="foldid_sha256")
  maps <- c(maps, setNames(paste0("y_",expected$scale_key,"_sha256"),"y_sha256"))
  for (nm in names(maps)) {
    value <- as.character(manifest_row[[maps[[nm]]]][1])
    need(all(rows[[nm]]==value) && identical(x$case[[nm]],value),paste0("manifest_",nm))
  }
  e <- ctx$engine
  need(identical(e$f64_sha256(inp$X),x$case$x_sha256), "input_X_hash")
  need(identical(e$f64_sha256(inp$Y[,expected$scale_key]),x$case$y_sha256), "input_y_hash")
  need(identical(e$f64_sha256(inp$foldid),x$case$fold_sha256), "input_fold_hash")
  need(same(rows$scale[1],unname(inp$scales[[expected$scale_key]])), "input_scale")
  for(nm in names(x$case))
    if(nm %in% names(rows)) need(all(vapply(rows[[nm]],function(v) same(v,x$case[[nm]]),logical(1))),paste0("case_",nm))
  settings <- ctx$cfg$study_settings()
  probs <- ctx$checker$validate_payload(x,rows,settings,e)
  need(!length(probs),paste(c("frozen_payload",probs),collapse=": "))
  need(is.data.frame(x$fit$rules) && nrow(x$fit$rules)==nrow(rows) &&
       all(names(x$fit$rules) %in% names(rows)), "RDS_fit_rule_schema")
  for (column in names(x$fit$rules))
    need(same(rows[[column]],x$fit$rules[[column]]),paste0("RDS_fit_rule_",column))
  need(identical(x$coefficients,x$fit$coefficients), "coefficient_copies")
  whole_failed <- all(rows$status=="failed") && all(is.na(rows$diag_flag))
  if (whole_failed) {
    need(is.numeric(x$fit$beta) && length(x$fit$beta)==ncol(inp$X) && all(is.na(x$fit$beta)), "failed_fit_beta_NA")
    return(TRUE)
  }
  d <- x$fit$diagnostics
  need(is.list(d$pilot) && is.numeric(d$pilot$beta) && length(d$pilot$beta)==ncol(inp$X) && all(is.finite(d$pilot$beta)), "pilot_evidence")
  b <- d$pilot$beta; keep <- which(b!=0)
  need(identical(as.integer(d$keep),as.integer(keep)) && same(d$pilot_beta,b), "pilot_keep")
  need(length(d$w)==length(keep) && length(d$v)==length(keep), "pilot_weights_length")
  if(length(keep)) {
    w <- 1/abs(b[keep]); v <- length(w)*(w/max(w))/sum(w/max(w))
    need(all(is.finite(d$w)) && all(is.finite(d$v)) && same(w,d$w) && same(v,d$v), "pilot_weights")
  }
  X <- inp$X; y <- unname(inp$Y[,expected$scale_key]); n <- nrow(X)
  pi <- d$pilot$index
  need(length(pi)==1L && is.finite(pi) && pi>=1 && pi<=length(d$pilot$lambda) && pi==as.integer(pi), "pilot_index")
  need(length(d$pilot$cvm)==length(d$pilot$lambda) &&
       length(d$pilot$cvsd)==length(d$pilot$lambda) &&
       all(is.finite(d$pilot$cvm)) && all(is.finite(d$pilot$cvsd)) &&
       all(d$pilot$cvsd>=0) && pi==which.min(d$pilot$cvm), "pilot_cv_choice")
  need(length(d$pilot$kkt_full)==length(d$pilot$lambda) &&
       all(is.finite(d$pilot$kkt_full)) &&
       length(d$pilot$kkt_fold_at_index)==settings$COMMON$nfolds &&
       all(is.finite(d$pilot$kkt_fold_at_index)) &&
       all(d$pilot$kkt_fold_at_index<=settings$GLMNET$kkt_rel_tol), "pilot_KKT_evidence")
  pilot_lambda <- d$pilot$lambda[pi]
  need(is.finite(pilot_lambda) && pilot_lambda>0, "pilot_lambda")
  gradient <- drop(crossprod(X,y-drop(X %*% b)))/n
  violation <- pmax(abs(gradient)-pilot_lambda,0)
  active <- b!=0
  violation[active] <- abs(gradient[active]-pilot_lambda*sign(b[active]))
  scale <- max(1,max(abs(crossprod(X,y)))/n)
  need(max(violation)/scale <= settings$GLMNET$kkt_rel_tol, "pilot_KKT")
  need(same(max(violation)/scale,d$pilot$kkt_full[pi],1e-7), "pilot_KKT_record")
  need(all(rows$pilot_k==length(keep)) && all(rows$pilot_index==pi) &&
       all(vapply(rows$pilot_lambda,function(v) same(v,pilot_lambda),logical(1))), "pilot_row_metadata")
  need(same(d$foldid,inp$foldid), "fold_evidence")
  if(!length(keep)) {
    need(all(vapply(x$coefficients,function(z) all(z$beta_pen==0),logical(1))) && all(grepl("pilot_null",rows$diag_codes,fixed=TRUE)), "pilot_null")
    need(is.matrix(d$heldout) && identical(dim(d$heldout),c(n,2L)) &&
         all(is.finite(d$heldout)) && all(d$heldout==0) &&
         length(d$w)==0L && length(d$v)==0L, "pilot_null_evidence")
    need(all(rows$status %in% c("ok","warning")) && all(rows$support=="") &&
         all(rows$k==0L) && all(x$fit$beta==0), "null_support")
    need(all(is.na(rows$lambda)) && all(is.na(rows$index)) &&
         all(vapply(x$coefficients,function(z) is.na(z$lambda) && is.na(z$index),logical(1))), "null_sentinels")
    path <- d$path
    need(is.data.frame(path) && nrow(path)==1L &&
         identical(names(path),c("lambda","key","k","cvm","cvsd","kkt_full","kkt_fold_max")) &&
         identical(path$key,"") && identical(as.integer(path$k),0L) &&
         all(is.na(path[1,c("lambda","cvm","cvsd","kkt_full","kkt_fold_max")])), "null_path")
    null_cand <- e$ebic_candidates(X,y,list(),settings$COMMON$kmax_ebic,
                                   settings$COMMON$ebic_gamma[c("ebic1","ebic05")],settings$COMMON$ols_tol)
    need(is.data.frame(d$candidates) && nrow(d$candidates)==1L &&
         isTRUE(null_cand$valid[1]) && same(d$candidates,null_cand), "null_candidates")
    need(all(vapply(rows$rss,function(z) same(z,sum(y^2),1e-8),logical(1))), "null_rss")
    need(all(vapply(rows$ebic1_value,function(z) same(z,null_cand$ebic1[1]),logical(1))) &&
         all(vapply(seq_len(nrow(rows)),function(i) {
           id <- rows$rule_id[i]
           if(startsWith(id,"ebic1")) same(rows$crit_value[i],null_cand$ebic1[1])
           else if(startsWith(id,"ebic05")) same(rows$crit_value[i],null_cand$ebic05[1])
           else is.na(rows$crit_value[i])
         },logical(1))), "null_scores")
  } else {
    need(is.data.frame(d$path) && nrow(d$path)==length(d$pilot$lambda), "path_evidence")
    if(length(keep)==1L) need(all(grepl("pilot_single",rows$diag_codes,fixed=TRUE)), "pilot_singleton")
    path <- d$path
    required <- c("lambda","key","k","cvm","cvsd","kkt_full","kkt_fold_max")
    need(all(required %in% names(path)) && all(is.finite(path$lambda)) &&
         all(is.finite(path$cvm)) && all(is.finite(path$cvsd)) &&
         all(path$cvsd>=0) && all(is.finite(path$kkt_full)) &&
         all(is.finite(path$kkt_fold_max)), "selection_path")
    supports <- lapply(path$key,function(k) {
      need(!is.na(k), "selection_path_support")
      s <- e$parse_key(k)
      need(!anyNA(s) && all(s>=1L & s<=ncol(X)) &&
           identical(e$support_key(s),k) && all(s %in% keep), "selection_path_support")
      s
    })
    need(same(path$k,lengths(supports)), "selection_path_k")
    grid <- settings$GRID$max_mult*max(abs(drop(crossprod(X[,keep,drop=FALSE],y)))/n/d$v)*
            e$lambda_fraction(settings$GRID)
    need(same(path$lambda,grid), "weighted_lambda_grid")
    cv <- e$cv_choose(path$cvm,path$cvsd)
    need(same(d$index,cv), "CV_diagnostic_choices")
    for (rid in c("cv_min","cv_1se")) {
      i <- match(rid,rows$rule_id); ix <- if(rid=="cv_min") cv[["min"]] else cv[["one_se"]]
      need(same(rows$index[i],ix) && same(rows$lambda[i],path$lambda[ix]) &&
           same(rows$cv_mean[i],path$cvm[ix]) && same(rows$cv_se[i],path$cvsd[ix]),
           paste0("CV_choice_",rid))
      target <- if(rows$status[i]=="failed") rows$support_audit[i] else rows$support[i]
      need(identical(as.character(target),as.character(path$key[ix])),paste0("CV_support_",rid))
      bad <- path$kkt_full[ix]>settings$GLMNET$kkt_rel_tol ||
             path$kkt_fold_max[ix]>settings$GLMNET$kkt_rel_tol ||
             (rid=="cv_1se" && path$kkt_fold_max[cv[["min"]]]>settings$GLMNET$kkt_rel_tol)
      need((rows$status[i]=="failed")==bad,paste0("CV_status_",rid))
      own <- e$ebic_candidates(X,y,list(supports[[ix]]),Inf,
                                settings$COMMON$ebic_gamma["ebic1"],settings$COMMON$ols_tol)
      own <- own[match(path$key[ix],own$key),,drop=FALSE]
      need(nrow(own)==1L && same(rows$rss[i],own$rss[1]) &&
           same(rows$ebic1_value[i],own$ebic1[1]) && is.na(rows$crit_value[i]),
           paste0("CV_score_",rid))
    }
    candidate <- e$ebic_candidates(X,y,supports,settings$COMMON$kmax_ebic,
                                    settings$COMMON$ebic_gamma[c("ebic1","ebic05")],settings$COMMON$ols_tol)
    need(same(d$candidates,candidate), "candidate_table")
    passing <- path$kkt_full<=settings$GLMNET$kkt_rel_tol
    for (rid in c("ebic1","ebic05","ebic1_K37","ebic05_K37")) {
      i <- match(rid,rows$rule_id)
      col <- sub("_K37$","",rid)
      eligible <- if(endsWith(rid,"_K37")) candidate[candidate$k<=floor(n/log(n)),,drop=FALSE] else candidate
      choice <- eligible[e$ebic_pick(eligible,col),,drop=FALSE]
      target <- if(rows$status[i]=="failed") rows$support_audit[i] else rows$support[i]
      need(identical(as.character(target),as.character(choice$key[1])),paste0("EBIC_pick_",rid))
      need(same(rows$rss[i],choice$rss[1]) && same(rows$ebic1_value[i],choice$ebic1[1]) &&
           same(rows$crit_value[i],choice[[col]][1]) &&
           same(rows$k_valid_max[i],max(eligible$k[eligible$valid])) &&
           same(rows$k_path_max[i],max(path$k)),paste0("EBIC_score_",rid))
      occ <- which(path$key==choice$key[1]); pass <- occ[passing[occ]]
      first <- if(length(pass)) pass[1] else if(length(occ)) occ[1] else NA_integer_
      need(same(rows$index[i],first),paste0("EBIC_occurrence_",rid))
      need(if(is.na(first)) is.na(rows$lambda[i]) else same(rows$lambda[i],path$lambda[first]),
           paste0("EBIC_lambda_",rid))
      need((rows$status[i]=="failed") == !e$occurrence_ok(choice$key[1],path$key,passing),
           paste0("EBIC_status_",rid))
    }
  }
  for(i in seq_len(nrow(rows))) {
    r <- rows[i,,drop=FALSE]; co <- x$coefficients[[i]]
    need(is.numeric(co$beta_pen) && length(co$beta_pen)==ncol(X) && all(is.finite(co$beta_pen)),paste0("beta_finite_",r$rule_id))
    target <- if(r$status=="failed") r$support_audit else r$support
    need(!is.na(target) && identical(key(co$beta_pen),as.character(target)),paste0("support_",r$rule_id))
    need(all(co$beta_pen[-keep]==0) || !length(keep),paste0("screen_",r$rule_id))
    if(length(keep) && r$status!="failed" && !(is.na(r$index) && identical(as.character(target),""))) {
      ii <- r$index
      need(length(ii)==1L && !is.na(ii) && ii>=1 && ii<=nrow(d$path) && ii==as.integer(ii),paste0("index_",r$rule_id))
      need(same(r$lambda,d$path$lambda[ii]) && identical(as.character(d$path$key[ii]),as.character(target)),paste0("selected_path_",r$rule_id))
      grad <- drop(crossprod(X[,keep,drop=FALSE],y-drop(X %*% co$beta_pen)))/n
      pen <- r$lambda*d$v; beta <- co$beta_pen[keep]
      err <- pmax(abs(grad)-pen,0); act <- beta!=0
      err[act] <- abs(grad[act]-pen[act]*sign(beta[act]))
      sc <- max(1,max(abs(crossprod(X[,keep,drop=FALSE],y)))/n)
      need(max(err)/sc<=settings$GLMNET$kkt_rel_tol,paste0("selected_KKT_",r$rule_id))
    }
    if(startsWith(r$rule_id,"ebic")) {
      idx <- which(co$beta_pen!=0)
      need(is.numeric(co$beta_ols) && length(co$beta_ols)==ncol(X) && all(is.finite(co$beta_ols)),paste0("OLS_finite_",r$rule_id))
      ols <- numeric(ncol(X))
      if(length(idx)) {
        fit <- lm.fit(X[,idx,drop=FALSE],y,tol=settings$COMMON$ols_tol)
        need(fit$rank==length(idx) && all(is.finite(fit$coefficients)),paste0("OLS_rank_",r$rule_id))
        ols[idx] <- fit$coefficients
      }
      need(same(co$beta_ols,ols),paste0("OLS_beta_",r$rule_id))
      need(same(sum((y-drop(X %*% ols))^2),r$rss,1e-8),paste0("OLS_RSS_",r$rule_id))
    } else need(all(is.na(co$beta_ols)),paste0("CV_OLS_NA_",r$rule_id))
  }
  need(same(x$fit$beta,x$coefficients[["cv_min"]]$beta_pen), "fit_beta_copy")
  TRUE
}

validate_prefix <- function(prefix, source, input_path, manifest_path, code, run_id, dataset, p, scenario, replicate, scale) {
  ctx <- load_frozen_validator(code)
  settings <- ctx$cfg$study_settings()
  meth <- settings$METHODS[settings$METHODS$method_id=="F3",,drop=FALSE]
  probs <- ctx$checker$validate_one(prefix,meth,settings,ctx$engine,ctx$rc$SCHEMA_HEAD)
  need(!length(probs),paste(c("frozen_validator",probs),collapse=": "))
  inp <- readRDS(input_path)
  manifest <- read.csv(manifest_path,stringsAsFactors=FALSE)
  mr <- manifest[manifest$dataset_id==dataset,,drop=FALSE]
  need(nrow(mr)==1L && identical(ctx$engine$file_sha256(input_path),as.character(mr$file_sha256)), "manifest_file_hash")
  rows <- read.csv(paste0(prefix,".csv"),stringsAsFactors=FALSE,
                   colClasses=c(support="character",support_audit="character",diag_codes="character",k="integer",
                                warnings="character",messages="character",error="character",package_version="character",
                                slurm_job_id="character",slurm_array_task_id="character"))
  x <- readRDS(paste0(prefix,".rds"))
  expected <- list(run_id=run_id,dataset_id=dataset,case_id=paste0(dataset,"_",scale),p=as.integer(p),
                   scenario=as.integer(scenario),replicate=as.integer(replicate),scale_key=scale,method_id="F3")
  validate_object(x,rows,source,inp,mr,expected,ctx)
}
if(sys.nframe()==0L) {
  args <- commandArgs(trailingOnly=TRUE)
  lines <- if(length(args)==1L && args[1]=="--stdin") readLines(file("stdin")) else paste(args,collapse="\t")
  bad <- 0L
  for(line in lines) {
    fields <- strsplit(line,"\t",fixed=TRUE)[[1L]]
    tryCatch({
      need(length(fields)==11L,"validator_argument_count")
      do.call(validate_prefix,as.list(fields))
      cat("VALID",fields[1],"\n")
    },error=function(e) {bad <<- bad+1L; cat("INVALID",fields[1],conditionMessage(e),"\n")})
  }
  if(bad) quit(save="no",status=1L)
}
