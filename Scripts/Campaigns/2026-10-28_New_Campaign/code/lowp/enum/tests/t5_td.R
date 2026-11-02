# Check 5: lowp_td (literal and toward variants) against a slow independent R implementation using the core's v3_score,
# p = 10, n = 200 (K = p) and n = 12 (K = 6 < p, so that swaps at |S| = K are exercised); dry-run count formula.
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
lowp_load(); load_core_ref()
p <- 10; S0 <- c(2L, 5L, 7L)
slow_td <- function(ctx, S0, d, pool, K) {
  p <- ctx$p; calls <- 0
  Us <- unlist(lapply(0:length(S0), function(u) if (u == 0) list(integer(0)) else combn(S0, u, simplify = FALSE)), recursive = FALSE)
  Ps <- unlist(lapply(0:min(d, length(pool)), function(i) if (i == 0) list(integer(0)) else combn(pool, i, simplify = FALSE)), recursive = FALSE)
  rows <- list()
  Fs <- function(S) { calls <<- calls + 1; v3_score(ctx, sort(S))$F }
  for (P in Ps) for (U in Us) {
    S <- sort(c(U, P)); k <- length(S); if (k > K) next
    F0 <- Fs(S); outs <- setdiff(1:p, S)
    mv <- list()   # each: new set, type, label info
    if (k < K) for (l in outs) mv[[length(mv) + 1]] <- list(S = c(S, l), type = "add", a = l, b = NA)
    for (j in S) mv[[length(mv) + 1]] <- list(S = setdiff(S, j), type = "del", a = j, b = NA)
    for (j in S) for (l in outs) mv[[length(mv) + 1]] <- list(S = c(setdiff(S, j), l), type = "swap", a = j, b = l)
    g <- vapply(mv, function(m) Fs(m$S) - F0, 0)
    ty <- vapply(mv, `[[`, "", "type"); a <- vapply(mv, `[[`, 0L, "a"); b <- vapply(mv, `[[`, 0L, "b")
    dist0 <- length(setdiff(S, S0)) + length(setdiff(S0, S))
    red <- vapply(mv, function(m) { s <- m$S; length(setdiff(s, S0)) + length(setdiff(S0, s)) < dist0 }, TRUE)
    miss <- setdiff(S0, S); extra <- setdiff(S, S0)
    if (length(miss)) { cl <- "a"; tg <- ty == "add" & a %in% S0 } else if (length(extra)) { cl <- "b"; tg <- ty == "del" & !(a %in% S0) } else cl <- "c"
    if (cl == "c") { m_lit <- if (length(g)) -max(g) else Inf; m_tow <- m_lit }
    else {
      if (!any(tg)) m_lit <- -Inf else { ii <- which(tg)[which.max(g[tg])]; rest <- g[-ii]; m_lit <- if (!length(rest)) Inf else g[ii] - max(rest) }
      m_tow <- if (!any(red)) -Inf else if (all(red)) Inf else max(g[red]) - max(g[!red])
    }
    rows[[length(rows) + 1]] <- data.frame(centre = paste(S, collapse = ";"), clause = cl, lit = m_lit, tow = m_tow, stringsAsFactors = FALSE)
  }
  list(R = do.call(rbind, rows), calls = calls)
}
run_case <- function(n, cfgs) {
  X <- gen_design(p, "block", seed = 12, n = n); Y <- gen_response(X, S0, c(1.4, -1, 1.8), cs = c(c100 = 0.5), seed = 3); y <- Y[, 1]
  pre <- v3_preprocess(X, y, dup_components = FALSE); ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE); K <- ctx$K
  cat(sprintf("--- n = %d, p = %d, K = %d\n", n, p, K))
  for (cfg in cfgs) {
    pool <- if (is.null(cfg$pool)) setdiff(1:p, S0) else cfg$pool
    dry <- lowp_td(X, y, S0, cfg$d, null_pool = cfg$pool, margin = cfg$m, max_scores = 10)
    r <- lowp_td(X, y, S0, cfg$d, null_pool = cfg$pool, margin = cfg$m, threads = 3, keep_all = TRUE)
    s <- slow_td(ctx, S0, cfg$d, pool, K)
    C <- r$centres; C <- C[order(C$centre), ]; Ct <- r$toward$centres; Ct <- Ct[order(Ct$centre), ]; Rr <- s$R[order(s$R$centre), ]
    same_set <- identical(C$centre, Rr$centre) && identical(C$clause, Rr$clause) && identical(Ct$centre, Rr$centre)
    cmpm <- function(a, b) { fin <- is.finite(a) & is.finite(b); c(dm = if (any(fin)) max(abs(a[fin] - b[fin])) else 0, inf_same = identical(is.finite(a), is.finite(b)) && all(sign(a[!is.finite(a)]) == sign(b[!is.finite(b)]))) }
    cl <- factor(Rr$clause, c("a", "b", "c"))
    nv <- function(x) { v <- tapply(x < cfg$m, cl, sum); v[is.na(v)] <- 0; v }
    ml <- cmpm(C$margin, Rr$lit); mt <- cmpm(Ct$margin, Rr$tow)
    cat(sprintf("d=%d pool=%s m=%g: centres %g (slow %d, set&clauses same %s); literal max|dm|=%.1e infs same %s, viol %s vs slow %s; toward max|dm|=%.1e infs same %s, viol %s vs slow %s; scores C++ %g = formula %g = slow calls %d (dry run %g, dry_run=%s)\n",
      cfg$d, if (is.null(cfg$pool)) "all" else paste(cfg$pool, collapse = ","), cfg$m, r$n_centres, nrow(Rr), same_set,
      ml[["dm"]], as.logical(ml[["inf_same"]]), paste(vapply(r$clauses, `[[`, 0, "n_violating"), collapse = "/"), paste(nv(Rr$lit), collapse = "/"),
      mt[["dm"]], as.logical(mt[["inf_same"]]), paste(vapply(r$toward$clauses, `[[`, 0, "n_violating"), collapse = "/"), paste(nv(Rr$tow), collapse = "/"),
      r$scores_used, r$scores_needed, s$calls, dry$scores_needed, dry$dry_run))
    cat("   min margin literal a/b/c:", paste(signif(vapply(r$clauses, `[[`, 0, "min_margin"), 6), collapse = "/"), " toward:", paste(signif(vapply(r$toward$clauses, `[[`, 0, "min_margin"), 6), collapse = "/"), "; sizes of centres up to", max(C$size), "\n")
  }
}
run_case(200, list(list(d = 1, pool = NULL, m = 0), list(d = 2, pool = NULL, m = 1), list(d = 2, pool = c(1L, 3L, 8L), m = 2), list(d = 0, pool = NULL, m = 0)))
run_case(12, list(list(d = 3, pool = NULL, m = 0), list(d = 3, pool = NULL, m = 1)))
cat("Dry-run counts, p = 1000, K = 100, s0 = 14 (swaps at |S| = K counted):\n")
for (d in 0:2) { x <- lowp_td_count(1000, 100, 14, 986, d); cat(sprintf("  d=%d: centres %.0f, scores %.0f\n", d, x[["centres"]], x[["scores"]])) }
