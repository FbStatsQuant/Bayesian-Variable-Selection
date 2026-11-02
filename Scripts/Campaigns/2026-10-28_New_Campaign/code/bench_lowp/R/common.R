# Helpers are isolated by method: production common.R files have incompatible APIs.
lowp_load_method <- function(id, code_dir, p, test_versions = FALSE) {
  e <- new.env(parent = globalenv())
  sys.source(file.path(code_dir, 'R', 'production_helpers', paste0('common_', id, '.R')), e)
  if (id %in% c('F1','F2','F3')) sys.source(file.path(code_dir, 'R', 'methods', paste0('glmnet_helpers_', id, '.R')), e)
  files <- c(F1='fit_F1_lasso.R', F2='fit_F2_enet.R', F3='fit_F3_alasso.R', F4='fit_F4_mcp.R', F5='fit_F5_abess.R', A1='fit_A1_susie.R', A2='fit_A2_ssl.R', A3='fit_A3_horseshoe.R')
  sys.source(file.path(code_dir, 'R', 'methods', files[[id]]), e)
  original <- e$assert_pkg_version
  e$assert_pkg_version <- function(pkg, version) {
    if (!test_versions) return(original(pkg, version))
    if (!requireNamespace(pkg, quietly=TRUE)) stop('Package missing: ', pkg)
    actual <- as.character(utils::packageVersion(pkg))
    if (actual != version) warning('VERSION MISMATCH: ',pkg,' expected ',version,' found ',actual)
    invisible(TRUE)
  }
  s <- LOWP_PRODUCTION[[id]]
  s$variant <- 'primary'
  s$METHODS <- s$METHODS[s$METHODS$method_id == id,,drop=FALSE]
  if (id %in% paste0('F',1:5)) s$COMMON$kmax_ebic <- min(100L,p)
  if (id == 'F5') s$F5$sizes <- 0:min(100L,p)
  if (id == 'A1') s$A1$L <- min(50L,p)
  list(env=e, settings=s, fn=get(s$METHODS$fn[[1]], envir=e), registry=s$METHODS)
}
lowp_hash <- function(x) digest::digest(writeBin(as.double(as.vector(x)),raw(),endian='little'),algo='sha256',serialize=FALSE)

# Evidence for the low-p-only F4/F5 derived rules, using saved path coefficients.
lowp_coefficients <- function(fit, rows, id, X, y, tol) {
  p <- ncol(X); path <- fit$diagnostics$path
  ans <- lapply(seq_len(nrow(rows)), function(i) {
    r <- rows[i,,drop=FALSE]; key <- if (r$status == 'failed') r$support_audit else r$support
    pen <- ols <- rep(NA_real_, p); idx <- NA_integer_; lam <- NA_real_
    if (!is.null(path) && !is.na(key)) {
      occ <- which(path$key == key)
      if (id == 'F4' && length(occ)) {
        pass <- occ[path$passes[occ]]; if (length(pass)) occ <- pass
      }
      if (length(occ)) {
        idx <- occ[1L]; pen <- numeric(p)
        if (id == 'F4') { pen <- unname(fit$diagnostics$path_beta[,idx]); lam <- path$lambda[idx] }
        else {
          support <- if (nzchar(key)) as.integer(strsplit(key,';',fixed=TRUE)[[1L]]) else integer()
          pen[support] <- fit$diagnostics$coefficients[[idx]]
        }
        support <- which(pen != 0)
        if (!identical(paste(support,collapse=';'), key)) stop('coefficient support mismatch: ', r$rule_id)
        ols <- numeric(p)
        if (length(support)) {
          f <- lm.fit(X[,support,drop=FALSE], y, tol=tol)
          if (f$rank != length(support) || anyNA(f$coefficients)) stop('invalid selected OLS support')
          ols[support] <- f$coefficients
        }
      } else if (!nzchar(key)) { pen <- ols <- numeric(p) }
      else if (r$status != 'failed') stop('selected support absent from saved path')
    }
    list(rule_id=r$rule_id, status=r$status, support=r$support, k=r$k,
         index=idx, lambda=lam, alpha=NA_real_, beta_pen=pen, beta_ols=ols)
  })
  names(ans) <- rows$rule_id; ans
}

# PREREG R1 derived rows use only saved diagnostics; no refitting.
lowp_derive <- function(fit, id, p, n, scale) {
  rows <- fit$rules
  if (!id %in% paste0('F',1:5)) { rows$rule_label <- 'pre-declared'; return(rows) }
  K <- min(floor(n/log(n)),p)
  if (K != p || p > 30L) stop('LOWP alias assumption violated')
  orig <- rows
  if (id %in% c('F1','F2','F3')) {
    for (a in c('ebic1','ebic05')) {
      cap <- orig[orig$rule_id == a, , drop=FALSE]
      k37 <- orig[orig$rule_id == paste0(a, '_K37'), , drop=FALSE]
      if (nrow(cap) != 1L || nrow(k37) != 1L || k37$role != 'S0')
        stop('LOWP requires exactly one S0 K37 row per cap rule')
      for (field in c('support','k','crit_value'))
        if (!identical(cap[[field]], k37[[field]])) stop('LOWP K37 differs from cap: ', a, ' ', field)
    }
  }
  rows$role[rows$rule_id %in% c('ebic1','ebic05','bic')] <- 'secondary'
  aliases <- if (id %in% c('F4','F5')) intersect(c('ebic1','ebic05','bic'),orig$rule_id) else character()
  add <- lapply(aliases,function(a) {
    r <- orig[orig$rule_id==a,,drop=FALSE]; r$rule_id <- paste0(a,'_K37')
    r$role <- if(a=='ebic1' && id %in% c('F4','F5')) 'primary' else 'S0'; r
  })
  if (id %in% c('F4','F5')) {
    r <- orig[orig$rule_id=='ebic1',,drop=FALSE]
    r$rule_id <- if(id=='F4') 'ebic1_lam005' else 'sic_smax'; r$role <- 'S0'
    cand <- fit$diagnostics$candidates; path <- fit$diagnostics$path
    if (!is.null(cand) && !is.null(path) && nrow(cand) && nrow(path)) {
      if(id=='F4') {
        keys <- unique(c('',path$key[path$lambda >= .05*max(path$lambda)]))
        eligible <- cand$valid & cand$key %in% keys
        criterion <- cand$ebic1
      } else {
        smax <- min(p,floor(n/(log(p)*log(log(n)))))
        eligible <- cand$valid & cand$k <= smax
        criterion <- n*log(cand$rss/n)+cand$k*log(p)*log(log(n))
      }
      criterion[!eligible] <- Inf
      i <- order(criterion,cand$k,cand$key,method='radix')[1]
      if(is.finite(criterion[i])) {
        key <- cand$key[i]; failed <- FALSE
        if(id=='F4') {
          occ <- which(path$key==key & path$passes); if(!length(occ)) occ <- which(path$key==key)
          idx <- if(length(occ)) occ[1] else NA_integer_
          failed <- nzchar(key) && !any(path$key==key & path$passes)
          if(length(fit$diagnostics$gate_failures)) failed <- TRUE
          r$lambda <- if(is.na(idx)) NA_real_ else path$lambda[idx]; r$path_index <- idx
          if(failed && !length(fit$diagnostics$gate_failures)) r$error <- 'selected support has no path occurrence passing KKT and the iteration check'
        } else if(length(fit$diagnostics$consistency_failures)) failed <- TRUE
        # status of a successful derived row comes from the fit's captured conditions, not from the original rows'
        # statuses (failure takes precedence there and can hide a warning; RECHECK_c N1)
        txt_present <- function(v) if (is.null(v)) FALSE else any(!is.na(v) & nzchar(as.character(v)))
        had_cond <- any(orig$status=='warning') || any(!is.na(orig$n_warnings) & orig$n_warnings > 0) ||
          txt_present(orig$warnings) || txt_present(orig$messages)   # messages count as conditions (FINAL_CONFIRM FC3)
        r$status <- if(failed) 'failed' else if(had_cond) 'warning' else 'ok'
        if(!failed) r$error <- NA_character_
        r$support <- if(failed) NA_character_ else key; r$support_audit <- if(failed) key else NA_character_
        r$k <- if(failed) NA_integer_ else cand$k[i]; r$rss <- cand$rss[i]; r$crit_value <- criterion[i]
        codes <- strsplit(ifelse(is.na(r$diag_codes),'',r$diag_codes),';',fixed=TRUE)[[1]]
        codes <- setdiff(codes,'ebic_at_largest')
        # largest-candidate diagnostic relative to this rule's own eligible candidates (RECHECK_c N2); k_path_max unchanged
        k_elig_max <- max(cand$k[eligible])
        if('k_valid_max' %in% names(r)) r$k_valid_max <- k_elig_max
        if(cand$k[i]==k_elig_max) codes <- c(codes,'ebic_at_largest')
        r$diag_codes <- paste(codes[nzchar(codes)],collapse=';')
      } else { r$status <- 'failed'; r$support <- NA_character_; r$support_audit <- NA_character_; r$k <- NA_integer_; r$error <- 'no valid derived candidate' }
    } else { r$status <- 'failed'; r$support <- NA_character_; r$support_audit <- NA_character_; r$k <- NA_integer_ }
    add <- c(add,list(r))
  }
  rows <- do.call(rbind,c(list(rows),add)); rownames(rows) <- NULL
  rows$selected_k_gt_K37 <- ifelse(is.na(rows$k), NA, rows$k > floor(n/log(n)))
  rows$rule_label <- ifelse(grepl('_K37$|^ebic1_lam005$|^sic_smax$',rows$rule_id),
    if(scale=='c050') 'pre-registered' else ifelse(rows$rule_id=='ebic1_K37', 'post hoc (chosen from size diagnostics after the c = 1 run)', 'post hoc'), 'pre-declared')
  rows
}
