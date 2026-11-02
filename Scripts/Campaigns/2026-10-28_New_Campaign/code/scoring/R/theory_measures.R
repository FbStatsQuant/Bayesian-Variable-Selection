# theory_measures.R -- measures for the theory paper (usable at p << n and p >> n). Definitions: THEORY_MEASURES.md.
#   pi0(S0), pi0(R_d) (exact DP over the block tables), scored-set coverage, truth-vs-HPM score and miss class, truth trace,
#   T37 TD(d, 0) audit. "After the fact": setup is rebuilt from the preprocessed X, y with the CORE; the fit is not re-run.

# log varpi(k) = log w(k)/W_K for k = 0..K, read from the scorer (log_prior depends on |S| only)
log_varpi_by_size <- function(ctx) vapply(0:ctx$K, function(k) v3_score(ctx, ctx$orig[seq_len(k)])$log_prior, 0)

# Rebuild blocks/tables/start for a scorer (core's own functions; identical to what the SMC fit used)
rebuild_setup <- function(scorer) {
  setup <- v3_setup(scorer$ctx)
  if (inherits(setup, "v3_setup_failed")) stop("v3_setup failed: ", setup$message)
  setup
}

# pi0(R_d) for d = 0..d_max by a DP over blocks with state (size k, number of nulls q <= d_max).
# R_d = {U u P : U subset S0, P subset S0^c, |P| <= d}; pi0(S) = varpi(|S|) prod_b r_b(S n C_b) / Zbar0.
pi0_dp <- function(setup, S0, d_max = 2L) {
  ctx <- setup$ctx; K <- ctx$K
  lv <- log_varpi_by_size(ctx)
  A <- matrix(-Inf, K + 1L, d_max + 1L); A[1L, 1L] <- 0
  for (tb in setup$tables) {
    mem <- as.integer(tb$members); B <- length(mem)
    codes <- 0:(2^B - 1)
    nullmask <- sum(2^(which(!(mem %in% S0)) - 1))
    sz <- popcount_int(as.integer(codes)); nn <- popcount_int(bitwAnd(as.integer(codes), as.integer(nullmask)))
    e <- matrix(-Inf, B + 1L, d_max + 1L)
    for (j in 0:B) for (q in 0:d_max) { w <- which(sz == j & nn == q); if (length(w)) e[j + 1L, q + 1L] <- lse(tb$log_r[w]) }
    An <- matrix(-Inf, K + 1L, d_max + 1L)
    for (k in 0:K) for (q in 0:d_max) {
      v <- numeric(0)
      for (j in 0:min(B, k)) for (q1 in 0:q) { a <- e[j + 1L, q1 + 1L]; if (is.finite(a)) { b <- A[k - j + 1L, q - q1 + 1L]; if (is.finite(b)) v <- c(v, a + b) } }
      if (length(v)) An[k + 1L, q + 1L] <- lse(v)
    }
    A <- An
  }
  lz0 <- setup$start$log_Zbar0
  out <- vapply(0:d_max, function(d) lse(as.vector(outer(lv, rep(0, d + 1L), "+") + A[, seq_len(d + 1L), drop = FALSE])) - lz0, 0)
  names(out) <- paste0("d", 0:d_max)
  out
}

# log pi0(S0) from the tables (independent of v3_start_logmass): log varpi(s0) + sum_b log r_b(S0 n C_b) - log Zbar0
pi0_S0_tables <- function(setup, S0) {
  ctx <- setup$ctx; lv <- log_varpi_by_size(ctx); tot <- lv[length(S0) + 1L]
  for (tb in setup$tables) {
    mem <- as.integer(tb$members); code <- sum(2^(which(mem %in% S0) - 1))
    tot <- tot + tb$log_r[code + 1L]
  }
  tot - setup$start$log_Zbar0
}

# brute-force log pi0(R_d): sum of exp(v3_start_logmass) over the explicit set (validation at small p)
pi0_Rd_bruteforce <- function(setup, S0, d) {
  nulls <- setdiff(setup$ctx$orig, S0); s0 <- length(S0)
  Plist <- list(integer(0))
  if (d >= 1L) for (sz in seq_len(min(d, length(nulls)))) Plist <- c(Plist, utils::combn(nulls, sz, simplify = FALSE))
  v <- numeric(0)
  for (u in 0:(2^s0 - 1)) {
    U <- S0[bitwAnd(u, bitwShiftL(1L, seq_len(s0) - 1L)) > 0L]
    for (P in Plist) v <- c(v, v3_start_logmass(setup$start, sort(c(U, P))))
  }
  lse(v)
}

blocks_equal <- function(a, b) {
  if (is.null(a) || is.null(b)) return(NA)
  identical(lapply(unname(as.list(a)), function(x) as.integer(x)), lapply(unname(as.list(b)), function(x) as.integer(x)))
}

# union of the core neighbour lists of the true variables, minus S0 (restricted null pool for p >> n)
td_null_pool_neighbours <- function(scorer, S0) {
  N <- v3_neighbours(scorer$ctx)
  sort(setdiff(unique(unlist(N[as.character(S0)])), S0))
}

# Was the truth model scored during the fit? Derived from the v2.2 scored_set (key = bitmask over retained positions).
truth_trace_from_scored <- function(sm, S0) {
  tt <- list(truth_scored = NA, truth_first_phase = NA_character_, truth_first_mech = NA_character_, truth_first_tier = NA_real_,
             truth_first_iter = NA_real_, truth_first_island = NA_real_, truth_first_stage = NA_real_, truth_trace_source = NA_character_)
  if (is.list(sm$truth_trace) && !is.null(sm$truth_trace$scored)) {      # PROVISIONAL in-fit trace, if the sibling thread adds one
    t <- sm$truth_trace
    tt$truth_scored <- as.logical(t$scored); tt$truth_first_phase <- as.character(t$first_phase %||% NA); tt$truth_first_mech <- as.character(t$first_mech %||% NA)
    tt$truth_first_tier <- as.numeric(t$first_tier %||% NA); tt$truth_first_iter <- as.numeric(t$first_iter %||% NA)
    tt$truth_first_island <- as.numeric(t$first_island %||% NA); tt$truth_first_stage <- as.numeric(t$first_stage %||% NA); tt$truth_trace_source <- "fit"
    return(tt)
  }
  ss <- sm$scored_set
  if (!is.data.frame(ss) || !nrow(ss)) return(tt)
  kept <- sm$kept %||% seq_len(sm$p)
  pos <- match(S0, kept)
  tt$truth_trace_source <- "scored_set"
  if (anyNA(pos)) { tt$truth_scored <- FALSE; return(tt) }
  key <- sum(2^(pos - 1)); i <- match(key, ss$key)
  tt$truth_scored <- !is.na(i)
  if (!is.na(i)) {
    tt$truth_first_phase <- as.character(ss$first_phase[i]); tt$truth_first_mech <- as.character(ss$first_mech[i])
    tt$truth_first_tier <- ss$first_tier[i]; tt$truth_first_iter <- ss$first_iter[i]; tt$truth_first_island <- ss$first_island[i]; tt$truth_first_stage <- ss$first_stage[i]
  }
  tt
}

# One case_theory row. X, y = the stored X and the Y column of the scale; S0 = truth; sm = extract_smc() or NULL; es = exact_scale() or NULL.
#   td: list(d = c(1,2) [all nulls], restricted_d = integer(0) [restricted pool, opt-in], engine = "auto", max_scores = Inf, margin = 0, threads = 1) or NULL to skip.
theory_case_row <- function(X, y, S0, ids, sm = NULL, es = NULL, scorer = NULL, setup = NULL, d_max = 2L, td = NULL) {
  S0 <- sort(as.integer(S0))
  scorer <- scorer %||% make_scorer(X, y)
  S0_ret <- intersect(S0, scorer$kept); n_drop <- length(S0) - length(S0_ret); retained <- n_drop == 0L
  row <- c(ids, list(s0 = length(S0), S0 = enc_support(S0), S0_retained = retained, n_true_dropped = n_drop,
                     theory_status = if (retained) "ok" else "truth_dropped",
                     region_basis = if (retained) "full_truth" else "retained_truth_subsets"))
  # --- pi0. All quantities go through the preprocessing original-index map (setup/tables/blocks use original indices).
  # If a true variable was dropped, pi_0(S0) = 0 (S0 is infeasible), but R_d (subsets of S0, d nulls) is evaluated over the FEASIBLE retained
  # supports: its true part is the retained truths S0 n kept. TD is undefined then (td_status).
  setup <- setup %||% tryCatch(rebuild_setup(scorer), error = function(e) NULL)
  row$n_blocks <- if (is.null(setup)) NA_integer_ else length(setup$blocks); row$B <- if (is.null(setup)) NA_integer_ else setup$B
  row$log_Zbar0 <- if (is.null(setup)) NA_real_ else setup$start$log_Zbar0
  dpn <- paste0("d", 0:d_max)
  if (!is.null(setup)) {
    dp <- pi0_dp(setup, S0_ret, d_max)
    if (retained) { ls0 <- v3_start_logmass(setup$start, S0); row$pi0_S0_tables_diff <- pi0_S0_tables(setup, S0) - ls0 } else { ls0 <- -Inf; row$pi0_S0_tables_diff <- NA_real_ }
    row$log_pi0_S0 <- ls0; row$pi0_S0 <- exp(ls0)
    for (dn in dpn) { row[[paste0("log_pi0_R", substring(dn, 2))]] <- dp[[dn]]; row[[paste0("pi0_R", substring(dn, 2))]] <- exp(dp[[dn]]) }
  } else {
    row$log_pi0_S0 <- NA_real_; row$pi0_S0 <- NA_real_; row$pi0_S0_tables_diff <- NA_real_
    for (dn in dpn) { row[[paste0("log_pi0_R", substring(dn, 2))]] <- NA_real_; row[[paste0("pi0_R", substring(dn, 2))]] <- NA_real_ }
  }
  row$blocks_match <- if (!is.null(sm) && !is.null(setup)) blocks_equal(sm$blocks, setup$blocks) else NA
  # --- truth vs HPM, coverage, trace
  F_truth <- scorer$F(S0)
  row$F_truth <- F_truth
  ok <- !is.null(sm) && isTRUE(sm$ok)
  F_hpm <- if (!is.null(sm) && !is.null(sm$hpm)) scorer$F(sm$hpm) else NA_real_
  row$F_smc_hpm <- F_hpm; row$hpm_eq_truth <- if (ok) same_set(sm$hpm, S0) else NA
  row$truth_minus_smc_hpm <- if (ok && !is.na(F_truth)) F_truth - F_hpm else NA_real_
  row$miss_class <- if (!ok || is.na(F_hpm) || is.na(F_truth)) NA_character_ else if (same_set(sm$hpm, S0)) "hit" else if (F_truth > F_hpm) "search_miss" else "posterior_miss"
  row$truth_minus_exact_hpm <- if (!is.null(es)) F_truth - es$hpm_F else NA_real_
  row$log_truth_mass <- if (!is.null(es)) F_truth - es$log_Z else NA_real_
  row$log_scored_coverage <- if (ok && !is.null(es) && !is.na(sm$log_mass_scored)) sm$log_mass_scored - es$log_Z else NA_real_
  row$scored_coverage <- if (is.na(row$log_scored_coverage)) NA_real_ else exp(row$log_scored_coverage)
  tt <- if (ok) truth_trace_from_scored(sm, S0) else truth_trace_from_scored(list(), S0)
  row <- c(row, tt)
  # --- TD audit: td$d = d values with ALL nulls (columns td{d}_*); td$restricted_d = d values with the null pool restricted to the union of the
  # core neighbour lists of the true variables (columns td{d}r_*, opt-in); each with the literal and the toward variant
  row$td_status <- if (is.null(td)) "skipped" else if (!retained) "undefined_truth_dropped" else "ok"
  if (!is.null(td) && retained) {
    specs <- c(lapply(td$d %||% integer(0), function(d) list(d = d, restricted = FALSE)),
               lapply(td$restricted_d %||% integer(0), function(d) list(d = d, restricted = TRUE)))
    for (sp in specs) {
      d <- sp$d
      pool <- if (sp$restricted && d >= 1L) td_null_pool_neighbours(scorer, S0) else NULL   # d = 0 has no nulls in the centres: never restricted
      r <- run_td(X, y, scorer, S0, d, null_pool = pool, margin = td$margin %||% 0, max_scores = td$max_scores %||% Inf,
                  threads = td$threads %||% 1L, engine = td$engine %||% "auto")
      pre <- paste0("td", d, if (sp$restricted) "r" else "", "_")
      row[[paste0(pre, "restricted")]] <- r$restricted; row[[paste0(pre, "engine")]] <- r$engine; row[[paste0(pre, "complete")]] <- r$complete
      row[[paste0(pre, "scores")]] <- r$scores_used
      for (vn in c("literal", "toward")) {
        cl <- r[[vn]]$clauses; pv <- paste0(pre, vn, "_")
        for (i in seq_len(nrow(cl))) {
          cn <- cl$clause[i]
          row[[paste0(pv, cn, "_n")]] <- cl$n_centres[i]; row[[paste0(pv, cn, "_viol")]] <- cl$n_violations[i]
          row[[paste0(pv, cn, "_tight")]] <- cl$n_tight[i]; row[[paste0(pv, cn, "_minmargin")]] <- cl$min_margin[i]
        }
        row[[paste0(pv, "violations")]] <- if (all(is.na(cl$n_violations))) NA_integer_ else sum(cl$n_violations)
        row[[paste0(pv, "min_margin")]] <- if (all(is.na(cl$min_margin))) NA_real_ else min(cl$min_margin, na.rm = TRUE)
        row[[paste0(pv, "holds_strict")]] <- if (!isTRUE(r$complete)) NA else sum(cl$n_violations) == 0 && all(cl$n_tight %in% c(0L, NA))
      }
      # literal violators of clauses a, b beaten by a truth-in swap (null out, truth in)
      dg <- r$diagnosis; ab <- r$literal$clauses$clause %in% c("add_true", "remove_extra")
      row[[paste0(pre, "literal_viol_ab")]] <- if (all(is.na(r$literal$clauses$n_violations))) NA_integer_ else sum(r$literal$clauses$n_violations[ab])
      row[[paste0(pre, "literal_viol_truthin_swap")]] <- if (!isTRUE(r$complete)) NA_integer_ else sum(dg$n[dg$o_label == "swap_null_out_truth_in" & dg$clause %in% c("add_true", "remove_extra")])
    }
  }
  data.table::as.data.table(lapply(row, function(v) if (is.null(v) || !length(v)) NA else v))
}
