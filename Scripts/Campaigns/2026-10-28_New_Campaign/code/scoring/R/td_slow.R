# td_slow.R -- slow R stand-in for the T37 truth-dominance audit TD(d, m), via the core scorer, and the dispatcher run_td().
# Same return structure as run_td(); used when lowp_td() (lowp/enum/lowp_enum.R) is unavailable and as a cross-check.
#
# Centres: S = U u P, U subset S0, P subset (pool of nulls), |P| <= d, |S| <= K.  Feasible moves at S: every single add (|S| < K), every single
# remove, every swap (one included out, one excluded in; swaps keep the size, so they ARE feasible at |S| = K).  gain = F(S') - F(S).
# Clauses: a = S does not contain S0;  b = S strictly contains S0;  c = S = S0.
# Two variants (names as in lowp_enum.R):
#   literal (T37 wording): a: margin = gain of the best add of a missing truth - best gain among all OTHER moves;  b: best deletion of an extra
#     (null) variable - best gain among all other moves;  c: margin = -(best gain over all moves).
#   toward: at S != S0, margin = (best gain among moves that strictly reduce |S delta S0|: add a truth, delete a null, swap null-out/truth-in)
#     - (best gain among the other moves); at S0 the literal clause c.
# A centre violates when margin < m (n_violations); margin == m is counted in n_tight (T37(i) needs margin > m, i.e. n_violations + n_tight = 0).
# diagnosis: for literal violators in clauses a and b, the type (o_label) of the best competing move.

popcount_int <- function(x) { r <- integer(length(x)); while (any(x > 0L)) { r <- r + bitwAnd(x, 1L); x <- bitwShiftR(x, 1L) }; r }

TD_CLAUSES <- c("add_true", "remove_extra", "at_S0")

td_slow <- function(scorer, S0, d, null_pool = NULL, margin = 0, max_scores = Inf, max_centres = Inf, seed = 1L) {
  t0 <- proc.time()[["elapsed"]]
  orig <- scorer$kept; K <- scorer$K; Fv <- scorer$F
  S0 <- sort(as.integer(S0))
  if (!all(S0 %in% orig)) stop("a true variable was dropped by preprocessing; TD undefined")
  nulls_all <- setdiff(orig, S0)
  pool <- if (is.null(null_pool)) nulls_all else sort(intersect(as.integer(null_pool), nulls_all))
  s0 <- length(S0)
  n_before <- scorer$n_cached()
  Plist <- list(integer(0))
  if (d >= 1L && length(pool)) for (sz in seq_len(min(d, length(pool)))) Plist <- c(Plist, utils::combn(pool, sz, simplify = FALSE))
  centres <- expand.grid(u = 0:(2^s0 - 1), pi = seq_along(Plist))
  # centres larger than K are infeasible (the enumerator counts only |S| <= K): filter BEFORE scoring
  csize <- popcount_int(as.integer(centres$u)) + lengths(Plist)[centres$pi]
  n_skipped_over_K <- sum(csize > K); centres <- centres[csize <= K, , drop = FALSE]
  n_total_centres <- nrow(centres)
  if (is.finite(max_centres) && n_total_centres > max_centres) { set.seed(seed); centres <- centres[sort(sample.int(n_total_centres, max_centres)), , drop = FALSE] }
  mk <- function() list(cnt = setNames(integer(3), TD_CLAUSES), viol = setNames(integer(3), TD_CLAUSES), tight = setNames(integer(3), TD_CLAUSES),
                        minm = setNames(rep(Inf, 3), TD_CLAUSES), vio = list())
  A <- list(literal = mk(), toward = mk())
  lab_levels <- c("swap_null_out_truth_in", "null_addition", "null_deletion", "swap_null_for_null", "swap_truth_for_truth", "swap_truth_out_null_in", "truth_deletion", "other_target")
  diag_cnt <- list()
  complete <- TRUE; done <- 0L
  upd <- function(a, ci, m, S, cl) {
    a$cnt[ci] <- a$cnt[ci] + 1L
    if (m < margin) { a$viol[ci] <- a$viol[ci] + 1L; if (length(a$vio) < 500L) a$vio[[length(a$vio) + 1L]] <- data.frame(clause = cl, model = enc_support(S), margin = m, stringsAsFactors = FALSE) }
    else if (m == margin) a$tight[ci] <- a$tight[ci] + 1L
    if (m < a$minm[ci]) a$minm[ci] <- m
    a
  }
  for (ci in seq_len(nrow(centres))) {
    if (is.finite(max_scores) && (scorer$n_cached() - n_before) > max_scores) { complete <- FALSE; break }
    u <- centres$u[ci]
    U <- S0[bitwAnd(u, bitwShiftL(1L, seq_len(s0) - 1L)) > 0L]
    S <- sort(c(U, Plist[[centres$pi[ci]]]))
    k <- length(S); F0 <- Fv(S)
    notS <- setdiff(orig, S)
    g <- numeric(0); lab <- character(0); red <- logical(0); tgt_a <- logical(0); tgt_b <- logical(0)
    add <- function(gains, labels, reducing, ta, tb) { n_ <- length(gains); g <<- c(g, gains); lab <<- c(lab, rep_len(labels, n_)); red <<- c(red, rep_len(reducing, n_)); tgt_a <<- c(tgt_a, rep_len(ta, n_)); tgt_b <<- c(tgt_b, rep_len(tb, n_)) }
    if (k < K && length(notS)) {
      tr <- notS %in% S0
      add(vapply(notS, function(l) Fv(c(S, l)), 0) - F0, ifelse(tr, "truth_addition", "null_addition"), tr, tr, FALSE)
    }
    if (k > 0L) {
      nl <- !(S %in% S0)
      add(vapply(S, function(j) Fv(S[S != j]), 0) - F0, ifelse(nl, "null_deletion", "truth_deletion"), nl, FALSE, nl)
      if (length(notS)) for (jj in seq_along(S)) {
        j <- S[jj]; base <- S[-jj]; tin <- notS %in% S0; jn <- !(j %in% S0)
        add(vapply(notS, function(l) Fv(c(base, l)), 0) - F0,
            if (jn) ifelse(tin, "swap_null_out_truth_in", "swap_null_for_null") else ifelse(tin, "swap_truth_for_truth", "swap_truth_out_null_in"),
            jn & tin, FALSE, FALSE)
      }
    }
    missing <- setdiff(S0, S); extras <- setdiff(S, S0)
    ci_cl <- if (length(missing)) 1L else if (length(extras)) 2L else 3L
    cl <- TD_CLAUSES[ci_cl]
    if (ci_cl == 3L) {
      m_lit <- if (length(g)) -max(g) else Inf; m_tow <- m_lit
    } else {
      tgt <- if (ci_cl == 1L) tgt_a else tgt_b
      g1 <- if (any(tgt)) max(g[tgt]) else -Inf
      ot <- g[!tgt]; onon <- if (length(ot)) max(ot) else -Inf
      gt <- sort(g[tgt], decreasing = TRUE); g2 <- if (length(gt) >= 2L) gt[2L] else -Inf
      other <- max(onon, g2)
      m_lit <- if (g1 == -Inf) -Inf else if (other == -Inf) Inf else g1 - other
      gr <- if (any(red)) max(g[red]) else -Inf; go <- if (any(!red)) max(g[!red]) else -Inf
      m_tow <- if (gr == -Inf) -Inf else if (go == -Inf) Inf else gr - go
      if (m_lit < margin && any(tgt)) {          # diagnosis of the literal violator
        olab <- if (g2 > onon) "other_target" else lab[!tgt][which.max(ot)]
        diag_cnt[[paste(cl, olab)]] <- (diag_cnt[[paste(cl, olab)]] %||% 0L) + 1L
      }
    }
    A$literal <- upd(A$literal, ci_cl, m_lit, S, cl); A$toward <- upd(A$toward, ci_cl, m_tow, S, cl)
    done <- done + 1L
  }
  fin <- function(a) list(clauses = data.frame(clause = TD_CLAUSES, n_centres = as.integer(a$cnt), n_violations = as.integer(a$viol), n_tight = as.integer(a$tight),
                                               min_margin = ifelse(a$cnt > 0L, a$minm, NA_real_), stringsAsFactors = FALSE),
                          violations = if (length(a$vio)) do.call(rbind, a$vio) else data.frame(clause = character(0), model = character(0), margin = numeric(0)))
  lit <- fin(A$literal); tow <- fin(A$toward)
  dg <- if (length(diag_cnt)) data.frame(clause = sub(" .*", "", names(diag_cnt)), o_label = sub("^[^ ]+ ", "", names(diag_cnt)), n = as.integer(unlist(diag_cnt)), stringsAsFactors = FALSE)
        else data.frame(clause = character(0), o_label = character(0), n = integer(0))
  list(engine = "R_slow", d = d, margin = margin, K = K, s0 = s0, restricted = !is.null(null_pool) && length(pool) < length(nulls_all),
       null_pool_size = length(pool), n_centres_total = n_total_centres, n_centres_skipped_over_K = n_skipped_over_K, n_centres_done = done, complete = complete,
       clauses = lit$clauses, violations = lit$violations, literal = lit, toward = tow, diagnosis = dg,
       scores_used = scorer$n_cached() - n_before, seconds = proc.time()[["elapsed"]] - t0)
}

# Dispatcher: the C++ enumerator's lowp_td() when available (engine "auto"/"enum"), else the slow stand-in.
.td_state <- new.env()
run_td <- function(X, y, scorer, S0, d, null_pool = NULL, margin = 0, max_scores = Inf, threads = 1L, engine = c("auto", "slow", "enum")) {
  engine <- match.arg(engine)
  use_enum <- engine == "enum" || (engine == "auto" && exists("lowp_td", mode = "function") && !isTRUE(.td_state$broken))
  if (use_enum) {
    args <- list(X = X, y = y, truth = S0, d = d, null_pool = null_pool, margin = margin, max_scores = max_scores, threads = threads)
    r <- tryCatch({
      tryCatch(do.call(lowp_td, args), error = function(e) {
        if (grepl("unused argument", conditionMessage(e))) do.call(lowp_td, args[c("X", "y", "truth", "d", "null_pool", "margin")]) else stop(e) })
    }, error = function(e) { if (engine == "enum") stop(e); message("lowp_td unusable (", substr(conditionMessage(e), 1, 120), "); using the R stand-in"); .td_state$broken <- TRUE; NULL })
    if (!is.null(r)) return(normalise_td(r, d, margin, null_pool))
  }
  td_slow(scorer, S0, d, null_pool, margin, max_scores)
}

# lowp_enum.R clauses (list a/b/c with n_centres, n_violating, n_violating_strict, min_margin) -> data.frame of the stand-in
td_clauses_df <- function(cl) {
  data.frame(clause = TD_CLAUSES,
             n_centres = vapply(cl[c("a", "b", "c")], function(z) as.integer(z$n_centres), 0L),
             n_violations = vapply(cl[c("a", "b", "c")], function(z) as.integer(z$n_violating), 0L),
             n_tight = vapply(cl[c("a", "b", "c")], function(z) as.integer(z$n_violating_strict - z$n_violating), 0L),
             min_margin = vapply(cl[c("a", "b", "c")], function(z) as.numeric(z$min_margin), 0), row.names = NULL, stringsAsFactors = FALSE)
}
td_viol_df <- function(v) if (is.data.frame(v) && nrow(v)) data.frame(clause = TD_CLAUSES[match(v$clause, c("a", "b", "c"))], model = v$centre, margin = v$margin, stringsAsFactors = FALSE) else data.frame()
normalise_td <- function(r, d, margin, null_pool) {
  empty <- data.frame(clause = TD_CLAUSES, n_centres = NA_integer_, n_violations = NA_integer_, n_tight = NA_integer_, min_margin = NA_real_, stringsAsFactors = FALSE)
  base <- list(engine = "enum", d = d, margin = margin, restricted = !is.null(null_pool), null_pool_size = length(null_pool %||% integer(0)),
               n_centres_total = r$n_centres_expected %||% r$n_centres %||% NA_real_, n_centres_done = r$n_centres %||% NA_real_,
               scores_needed = r$scores_needed %||% NA_real_, seconds = r$seconds %||% NA_real_)
  if (isTRUE(r$dry_run))      # lowp_td refused: exact score count exceeds max_scores
    return(c(base, list(complete = FALSE, scores_used = NA_real_, clauses = empty, violations = data.frame(), literal = list(clauses = empty, violations = data.frame()),
                        toward = list(clauses = empty, violations = data.frame()), diagnosis = data.frame(clause = character(0), o_label = character(0), n = integer(0)))))
  if (is.list(r$clauses) && !is.data.frame(r$clauses) && all(c("a", "b", "c") %in% names(r$clauses))) {   # lowp_enum.R
    lit <- list(clauses = td_clauses_df(r$clauses), violations = td_viol_df(r$violators))
    tow <- if (!is.null(r$toward)) list(clauses = td_clauses_df(r$toward$clauses), violations = td_viol_df(r$toward$violators)) else list(clauses = empty, violations = data.frame())
    dg <- if (!is.null(r$diagnosis) && length(r$diagnosis)) { x <- as.data.frame(r$diagnosis, stringsAsFactors = FALSE); data.frame(clause = TD_CLAUSES[match(as.character(x[[1L]]), c("a", "b", "c"))], o_label = as.character(x[[2L]]), n = as.integer(x[[3L]]), stringsAsFactors = FALSE) }
          else data.frame(clause = character(0), o_label = character(0), n = integer(0))
    dg <- dg[dg$n > 0L, , drop = FALSE]
    return(c(base, list(complete = TRUE, scores_used = r$scores_used %||% NA_real_, clauses = lit$clauses, violations = lit$violations, literal = lit, toward = tow, diagnosis = dg)))
  }
  stop("lowp_td() returned an unrecognised structure; adapt normalise_td() (names: ", paste(names(r), collapse = ", "), ")")
}
