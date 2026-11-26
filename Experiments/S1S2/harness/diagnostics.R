# diagnostics.R -- theory diagnostics written into every run record by harness/run_one.R (manager brief 2026-11-25).
# The harness computes them AFTER the fit; adapters never see the true support S0 while fitting. A method-specific hook
# diag_<method>(X, y, fit, S0) defined in the adapter file (only smc/fit_smcbvs.R has one) adds what needs the method's
# own scorer. Every field and its definition is listed in specs/SPEC.md §10. Seeds are stored, never X or y.
# PROVENANCE: definitions are OURS (manager brief "theory diagnostics", 2026-11-25); no author source.

# (1) Data diagnostics. X is scaled with scale() (centred, sample SD with n - 1) before the eigenvalue and the
# correlations; beta is the generating coefficient vector on the raw X scale.
diag_dataset <- function(d) {
  X <- d$X; n <- nrow(X); p <- ncol(X); S <- as.integer(d$support); sig <- sqrt(d$sigma2)
  bmin <- if (length(S)) min(abs(d$beta[S])) else NA_real_
  out <- list(beta_min = bmin, beta_min_ratio = bmin / (sig * sqrt(log(p) / n)),
              lambda_min_S0 = NA_real_, max_abs_corr_null_true = NA_real_, sigma2 = d$sigma2,
              snr_realised = d$meta$nu_sample, X_scaling = "scale(): centred, sample SD (n - 1)")
  if (length(S)) {
    Xs <- scale(X[, S, drop = FALSE])
    out$lambda_min_S0 <- min(eigen(crossprod(Xs) / n, symmetric = TRUE, only.values = TRUE)$values)
    if (length(S) < p) out$max_abs_corr_null_true <- max(abs(stats::cor(X[, S, drop = FALSE], X[, -S, drop = FALSE])))
  }
  out
}

# Model strings "1,5,9" <-> integer vectors (sorted original column indices)
model_key <- function(m) paste(sort(as.integer(m)), collapse = ",")

# (3) Posterior summaries from the PIP vector and, where the method provides one, a model list
# models = data.frame(model = "i,j,k", logpost, weight[, size]) (weights renormalised over the list). logpost_S0 is the
# method's own log posterior of S0 (up to the same constant as `logpost`), or NA when the method has no scorer.
diag_posterior <- function(pip, S0, models = NULL, logpost_S0 = NA_real_, models_source = NA_character_) {
  p <- length(pip); S0 <- as.integer(S0); s0 <- length(S0); null <- setdiff(seq_len(p), S0)
  out <- list(min_true_pip = if (s0 && p) min(pip[S0]) else NA_real_,
              max_null_pip = if (length(null) && p) max(pip[null]) else NA_real_,
              n_null_pip_gt_half = if (p) sum(pip[null] > 0.5) else NA_integer_,
              sum_pip = if (p) sum(pip) else NA_real_,
              pi_S0 = NA_real_, gap_logpost = NA_real_, best_rival = NA_character_, mass_size_gt_2s0 = NA_real_,
              models_source = models_source)
  if (is.null(models) || !nrow(models)) { out$models_source <- "none: the method returns no model list"; return(out) }
  key0 <- model_key(S0)
  hit <- models$model == key0
  out$pi_S0 <- if (any(hit)) sum(models$weight[hit]) else 0
  size <- if (!is.null(models$size)) models$size else vapply(strsplit(models$model, ","), length, 1L)
  out$mass_size_gt_2s0 <- sum(models$weight[size > 2 * s0])
  if ("logpost" %in% names(models)) {
    riv <- which(!hit)
    if (length(riv)) {
      j <- riv[which.max(models$logpost[riv])]
      out$best_rival <- if (nzchar(models$model[j])) models$model[j] else "(empty model)"
      lp0 <- if (is.finite(logpost_S0)) logpost_S0 else if (any(hit)) models$logpost[hit][1] else NA_real_
      out$gap_logpost <- lp0 - models$logpost[j]
    }
  }
  out
}

# sigma-hat for methods without a hook: which estimate is used is part of the record
sigma_hat_generic <- function(method, fit) {
  e <- fit$extra
  if (!is.null(e$sigma_hat)) return(e$sigma_hat)
  if (identical(method, "susie") && is.numeric(e$sigma2))
    return(list(value = sqrt(e$sigma2), which = "sqrt(susieR fit$sigma2): residual variance estimated by IBSS (y centred)"))
  list(value = NA_real_, which = "not returned by the adapter")
}

# Model list a non-hook adapter may return in extra$top_models (columns model, weight, optional logpost / F)
models_generic <- function(fit) {
  tm <- fit$extra$top_models
  if (!is.data.frame(tm) || !all(c("model", "weight") %in% names(tm))) return(NULL)
  if (!"logpost" %in% names(tm) && "F" %in% names(tm)) tm$logpost <- tm$F
  tm
}

# (2) failure type. "none" if the selection is exact; "search" if the method's own score prefers S0 to what it
# selected (the method would have selected S0 had it found it); "statistical" otherwise (the posterior itself prefers
# a wrong model); "computational" when the fit hit a wall-time limit (HQ ruling 2026-11-26: counted, never dropped;
# the denominator stays the number of tasks); "other" when the fit failed otherwise or no score is available.
failure_type_of <- function(success, status, logpost_S0 = NA_real_, logpost_sel = NA_real_) {
  if (!identical(status, "ok")) return(if (grepl("timeout", as.character(status %||% ""), ignore.case = TRUE)) "computational" else "other")
  if (isTRUE(success)) return("none")
  if (!is.finite(logpost_S0) || !is.finite(logpost_sel)) return("other")
  if (logpost_S0 > logpost_sel) "search" else "statistical"
}

# Wilson score interval for k successes in n trials (95% default)
wilson <- function(k, n, z = stats::qnorm(0.975)) {
  if (!n) return(c(NA_real_, NA_real_))
  ph <- k / n; den <- 1 + z^2 / n
  ctr <- (ph + z^2 / (2 * n)) / den; hw <- z * sqrt(ph * (1 - ph) / n + z^2 / (4 * n^2)) / den
  c(max(0, ctr - hw), min(1, ctr + hw))
}
