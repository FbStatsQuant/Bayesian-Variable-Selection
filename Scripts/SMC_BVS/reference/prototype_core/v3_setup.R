# v3_setup.R -- context, scorer, blocks, tables, start, discrepancy, neighbour graph, setup bundle
# (CORE_SPEC v2 §§2-3; M §5, §§6.3-6.4, §6.13). Heavy work is in cpp/ (v3_score.h, v3_blocks.h, v3_start.h).

# v3_context(Xs, ys): G, z, y'y, n, p, K, log C_n, log W_K, log w(k), k = 0..K (M §5).
# orig = 1-based original column indices of the columns of Xs (R12); hooks = test hooks only:
#   hooks[["fail_min_size"]] (integer) and hooks[["fail_routes"]] (subset of "chol", "chol_refactor", "qr") make the named
#   routes fail for every model of size >= fail_min_size (A1 QR-fallback case, A3 numerical_failure).
# return_gram: copy the p x p Gram to R as ctx$G (default only for p <= 2000; code review D-1). v3_gram(ctx) for large p.
v3_context <- function(Xs, ys, orig = seq_len(ncol(Xs)), hooks = list(), return_gram = NULL) {
  stopifnot(is.matrix(Xs), length(ys) == nrow(Xs), length(orig) == ncol(Xs), !is.unsorted(orig, strictly = TRUE))
  rg <- if (is.null(return_gram)) ncol(Xs) <= 2000 else isTRUE(return_gram)
  ctx <- .v3cpp$cpp_context(Xs, as.numeric(ys), as.integer(orig), hooks, rg)
  ctx$hooks <- hooks
  class(ctx) <- "v3_ctx"
  ctx
}

# v3_score(ctx, S): log_m, log_prior = log varpi(S), F, log_BF, Q, route (M §5, §6.13). |S| > K is an error.
v3_score <- function(ctx, S) {
  r <- .v3cpp$cpp_score(ctx, as.integer(S))
  if (!is.null(r$status)) stop(r$message)
  r
}

# v3_blocks(ctx, B): blocks C_1..C_J in packing order, members sorted (M §6.3, R13). The dendrogram (hclust-style
# merge matrix with R13's left/right convention, heights, leaf order) is attached as attribute "dendrogram".
v3_blocks <- function(ctx, B) {
  r <- .v3cpp$cpp_blocks(ctx, as.integer(B))
  b <- r$blocks
  attr(b, "dendrogram") <- list(merge = r$merge, height = r$height, leaf_order = r$leaf_order)
  b
}

# v3_tables(ctx, blocks): for each block, every subset U coded by bits (bit i-1 <-> members[i]), entry code + 1:
# log_r = log m(U) - log m(empty) (M §6.3, R2), log_m, route. Entries with |U| > K (only under B_override > K) are NA.
v3_tables <- function(ctx, blocks) .v3cpp$cpp_tables(ctx, lapply(blocks, as.integer))

# v3_start(ctx, blocks, tables): log Zbar_0 by exact size-profile convolution up to K with the capped prior (M §6.3),
# size profiles log e_b(j), partial convolutions log F_b(k), the size law, and the exact sampler.
v3_start <- function(ctx, blocks, tables) {
  s <- .v3cpp$cpp_start(ctx, lapply(blocks, as.integer), tables)
  class(s) <- "v3_start"
  s
}
# exact log pi_0(S) (-Inf for infeasible S); deficits 1 - pi_0(S) via v3_log1mexp(log pi_0), never by subtraction.
v3_start_logmass <- function(start, S) .v3cpp$cpp_start_logmass(start, as.integer(S))
v3_log1mexp <- function(x) ifelse(x > -log(2), log(-expm1(x)), log1p(-exp(x)))
v3_start_logdeficit <- function(start, S) v3_log1mexp(v3_start_logmass(start, S))   # log(1 - pi_0(S)), stable
# N iid draws from pi_0. rng = an integer seed (stream 200) or list(seed =, stream =). as_key = TRUE returns
# character keys "j1,j2,..." ("" for the empty model) instead of a list of models (fast for 10^6 draws).
v3_start_draw <- function(start, N, rng, as_key = FALSE) {
  if (is.list(rng)) { seed <- rng[["seed"]]; stream <- rng[["stream"]] %||% 200 } else { seed <- rng; stream <- 200 }
  v3_check_seed(seed)
  if (!is.numeric(stream) || stream != round(stream) || stream < 0 || stream > 2^31 - 1) stop("stream must be an integer in [0, 2^31 - 1]")
  r <- .v3cpp$cpp_start_draw(start, as.integer(N), as.numeric(seed), as.numeric(stream), isTRUE(as_key))
  if (isTRUE(as_key)) r$keys else r$models
}
# exact argmax of pi_0 (max-plus convolution per size; HPM tie rule)
v3_start_mode <- function(start) .v3cpp$cpp_start_mode(start)
# d(S) = log BF(S) - sum_b log r_b(S n C_b) (M §6.3); details attached as attributes.
v3_discrepancy <- function(ctx, start, S) {
  r <- .v3cpp$cpp_discrepancy(start, as.integer(S))
  structure(r$d, log_BF = r$log_BF, log_composite = r$log_composite, log_gamma0 = r$log_gamma0, log_pi0 = r$log_pi0)
}
# N(1..p) per M §6.4 (list indexed by retained column position; entries are original indices). B defaults to M §3's B.
v3_neighbours <- function(ctx, B = NULL) {
  B <- B %||% v3_budgets(ctx$n, ctx$p)$B
  N <- .v3cpp$cpp_neighbours(ctx, as.integer(B))
  names(N) <- ctx$orig
  N
}

# v3_setup(ctx, B_override): bundles ctx, blocks, tables (scored once), start, neighbour graph, budgets.
# setup$start carries the same C++ pointer, so v3_start_logmass(setup$start, S) etc. work on it.
v3_setup <- function(ctx, B_override = NULL) {
  b <- v3_budgets(ctx$n, ctx$p)
  if (!is.null(B_override) && (!is.numeric(B_override) || length(B_override) != 1 || B_override != round(B_override) ||
                                B_override < 1 || B_override > 20))
    stop("B_override must be an integer in 1..20 (table codes are 32-bit and 2^B entries per block; code review R-6)")
  B <- if (is.null(B_override)) b$B else as.integer(B_override)
  r <- .v3cpp$cpp_setup(ctx, as.integer(B))
  if (r$status != "ok")   # numerical_failure while scoring the tables (M §2): best table model so far, incomplete
    return(structure(c(r, list(ctx = ctx, budgets = b, B = B)), class = "v3_setup_failed"))
  start <- r$start; start$ptr <- r$ptr; class(start) <- "v3_start"
  names(r$neighbours) <- ctx$orig
  structure(list(ptr = r$ptr, ctx = ctx, budgets = b, B = B, B_override = B_override, blocks = r$blocks,
                 tables = r$tables, start = start, neighbours = r$neighbours, seconds = r$seconds),
            class = "v3_setup")
}

# Gram of a context (only needed when the context was built without return_gram).
v3_gram <- function(ctx) { if (!is.null(ctx$G)) return(ctx$G); stop("ctx built without return_gram = TRUE; rebuild it with return_gram = TRUE") }
