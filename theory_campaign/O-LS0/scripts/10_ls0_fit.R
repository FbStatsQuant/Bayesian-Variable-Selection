# 10_ls0_fit.R -- LS0 on one production dataset x one signal scale, using ONLY the production v3 engine.
# Production path up to the setup, exactly as v3_fit: v3_preprocess(dup_components = FALSE) -> v3_context ->
# v3_setup (blocks, tables, pi_0, neighbour graph). Then (all in the engine, via ls0_exports.cpp):
#   S~0  = start_mode(st)                               exact argmax pi_0 (max-plus convolution over the block tables)
#   LS0  = Engine::local_search(S~0, ell, emit_centre)  the production local search: <= ell moves + certifying scan
#   scan(S0) = Engine::local_search(S0, 0, TRUE)        one scan at the truth: is S0 a strict flip/swap local max?
#   lattice  = one scan at every S in Lat(S~0), Phi(S) >= 2 (D_S check, Lemma LS-score), when |Lat| <= LAT_MAX
#   log pi_0(S0), log pi_0(S~0), log pi_0(R_d) d = 0..2  (exact; cpp_start_logmass, cpp_ls0_pi0_Rd)
# R_d = {U u P : U subset S0, P subset S0^c, |P| <= d}. Phi(S) = |S xor S0|.
# Returns list(row = one-row data.frame, detail = list(...)).

ls0_phi <- function(S, S0) length(union(setdiff(S, S0), setdiff(S0, S)))
ls0_key <- function(S) paste(sort(as.integer(S)), collapse = ",")
# T is a flip/swap neighbour of C (or equal to C)?  flip: |T xor C| = 1; swap: |T| = |C| and |T xor C| = 2.
ls0_within_one_move <- function(C, T) {
  d <- ls0_phi(C, T)
  d == 0 || d == 1 || (d == 2 && length(C) == length(T))
}
# HPM tie rule (v3_ledger.h hpm_better): larger F, exact F ties broken by plain lexicographic order (prefix first).
ls0_lex_less <- function(a, b) {
  a <- sort(as.integer(a)); b <- sort(as.integer(b))
  m <- min(length(a), length(b))
  for (i in seq_len(m)) if (a[i] != b[i]) return(a[i] < b[i])
  length(a) < length(b)
}
ls0_hpm_better <- function(Fa, a, Fb, b) Fa > Fb || (Fa == Fb && ls0_lex_less(a, b))

ls0_one <- function(inp, tru, scale_key, lat_max = as.integer(Sys.getenv("LS0_LAT_MAX", "64"))) {
  cpu0 <- proc.time(); w0 <- Sys.time()
  X <- inp$X; y <- unname(inp$Y[, scale_key]); S0 <- sort(as.integer(tru$active))
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  if (pre$status != "ok") stop("preprocess status ", pre$status)
  b <- v3_budgets(pre$n, pre$p)
  if (isTRUE(b$exact_branch)) stop("exact branch (not expected for the production designs)")
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  if (!all(S0 %in% pre$kept)) stop("a true predictor was dropped by preprocessing")
  t1 <- proc.time()
  setup <- v3_setup(ctx)
  if (inherits(setup, "v3_setup_failed")) stop("setup numerical_failure: ", setup$message)
  cpu_setup <- (proc.time() - t1)[["elapsed"]]
  ell <- as.integer(b$ell); K <- as.integer(b$K)

  # ---- start mode and start masses
  t1 <- proc.time()
  sm <- ls0_start_mode(setup)
  cpu_mode <- (proc.time() - t1)[["elapsed"]]
  St <- sort(as.integer(sm$model))
  extras <- setdiff(St, S0); missed <- setdiff(S0, St)
  lpi_S0 <- v3_start_logmass(setup$start, S0)
  lpi_Rd <- ls0_pi0_Rd(setup, S0, 2L)

  # ---- LS0: production local search from S~0, centre emitted, own ledger
  t1 <- proc.time()
  A <- ls0_local_search(setup, St, ell, TRUE)
  cpu_ls0 <- (proc.time() - t1)[["elapsed"]]
  F_S0 <- ls0_F(ctx, S0)
  centres <- lapply(A$scanned_centres, function(x) sort(as.integer(x)))      # every centre that was fully scanned
  path <- c(list(St), lapply(A$path, function(x) sort(as.integer(x))))        # S~0 then the accepted moves
  ret <- sort(as.integer(A$returned)); best <- sort(as.integer(A$best_scored))
  scored_S0 <- any(vapply(centres, function(C) ls0_within_one_move(C, S0), TRUE))
  # in the move_limit case the returned model is the best neighbour of the last scanned centre (also scored)
  path_phi <- vapply(path, ls0_phi, 0, S0 = S0)
  path_extras <- vapply(path, function(C) length(setdiff(C, S0)), 0)
  progress_moves <- if (length(path) >= 2) all(diff(path_phi) < 0) else NA
  first_regress <- if (length(path) >= 2 && any(diff(path_phi) >= 0)) which(diff(path_phi) >= 0)[1] else NA_integer_
  # move types along the path: +T add truth, -N delete null, +N add null, -T delete truth, sw(a>b) swap
  mtype <- character(0)
  if (length(path) >= 2) for (i in 2:length(path)) {
    a <- setdiff(path[[i]], path[[i - 1]]); d <- setdiff(path[[i - 1]], path[[i]])
    lab <- function(v) if (!length(v)) "" else if (v %in% S0) "T" else "N"
    mtype[i - 1] <- if (length(a) && length(d)) paste0("sw", lab(d), ">", lab(a)) else if (length(a)) paste0("+", lab(a)) else paste0("-", lab(d))
  }

  # ---- one scan at S0: strict local max?  (ell = 0: termination no_improvement <=> no strictly better neighbour)
  t1 <- proc.time()
  A0 <- ls0_local_search(setup, S0, 0L, TRUE)
  cpu_scan0 <- (proc.time() - t1)[["elapsed"]]
  S0_locmax <- identical(A0$termination, "no_improvement")
  nb0 <- sort(as.integer(A0$returned))
  S0_best_nbr_type <- if (S0_locmax) "none" else {
    a <- setdiff(nb0, S0); d <- setdiff(S0, nb0)
    if (length(a) && length(d)) "swap" else if (length(a)) "add_null" else "delete_truth" }
  S0_gap <- if (S0_locmax) NA_real_ else A0$returned_F - F_S0   # F(best neighbour) - F(S0) > 0 when not a local max

  # ---- empirical D_S on Lat(S~0) n {Phi >= 2} (Lemma LS-score premise (i)), when the lattice is small
  lat_size <- 2^length(missed) * 2^length(extras)
  lat_checked <- lat_size <= lat_max
  lat_n <- NA_integer_; lat_fail <- NA_integer_; lat_fail_states <- character(0); cpu_lat <- 0
  lat_fail_types <- NA_character_; lat_fail_minPhi <- NA_integer_; lat_n_phi2 <- NA_integer_; lat_fail_phi2 <- NA_integer_
  lab <- function(v) if (v %in% S0) "T" else "N"
  # best-neighbour type of T relative to S: +T/-N/swN>T are progress; +N, -T, swT>N, swT>T, swN>N are not; trap = local max
  move_type <- function(S, T, term) {
    if (!identical(term, "move_limit")) return("trap")
    a <- setdiff(T, S); d <- setdiff(S, T)
    if (length(a) && length(d)) paste0("sw", lab(d), ">", lab(a)) else if (length(a)) paste0("+", lab(a)) else paste0("-", lab(d))
  }
  if (lat_checked) {
    t1 <- proc.time()
    U0 <- intersect(St, S0)
    msub <- if (length(missed)) as.matrix(expand.grid(rep(list(0:1), length(missed)))) else matrix(0, 1, 0)
    esub <- if (length(extras)) as.matrix(expand.grid(rep(list(0:1), length(extras)))) else matrix(0, 1, 0)
    lat_n <- 0L; lat_fail <- 0L; lat_n_phi2 <- 0L; lat_fail_phi2 <- 0L; ftypes <- character(0); fphi <- integer(0)
    for (i in seq_len(nrow(msub))) for (j in seq_len(nrow(esub))) {
      S <- sort(c(U0, missed[msub[i, ] == 1], extras[esub[j, ] == 1]))
      ph <- ls0_phi(S, S0)
      if (ph < 2) next
      lat_n <- lat_n + 1L; if (ph == 2) lat_n_phi2 <- lat_n_phi2 + 1L
      Aj <- ls0_local_search(setup, S, 0L, FALSE)
      T <- sort(as.integer(Aj$returned))
      ok <- identical(Aj$termination, "move_limit") && ls0_phi(T, S0) < ph
      if (!ok) {
        lat_fail <- lat_fail + 1L; lat_fail_states <- c(lat_fail_states, ls0_key(S))
        ftypes <- c(ftypes, move_type(S, T, Aj$termination)); fphi <- c(fphi, ph)
        if (ph == 2) lat_fail_phi2 <- lat_fail_phi2 + 1L
      }
    }
    if (lat_fail > 0) {
      tt <- table(ftypes); lat_fail_types <- paste(names(tt), tt, sep = ":", collapse = ";"); lat_fail_minPhi <- min(fphi)
    } else lat_fail_types <- ""
    cpu_lat <- (proc.time() - t1)[["elapsed"]]
  }
  # does the LS0 path stay inside Lat(S~0) = {U' u P' : S~0 n S0 subset U' subset S0, P' subset S~0 \ S0}?
  path_in_lat <- all(vapply(path, function(C) all(intersect(St, S0) %in% C) && all(setdiff(C, S0) %in% extras), TRUE))

  # ---- (M3): smallest eigenvalue of the correlation matrix on S~0 u S0
  U <- sort(union(St, S0)); Xu <- pre$X[, match(U, pre$kept), drop = FALSE]
  lam_min <- min(eigen(crossprod(Xu) / (pre$n - 1), symmetric = TRUE, only.values = TRUE)$values)

  cpu_all <- proc.time() - cpu0
  row <- data.frame(
    dataset_id = inp$dataset_id, p = inp$p, scenario = inp$scenario, replicate = inp$replicate,
    scale_key = scale_key, c = unname(inp$scales[scale_key]),
    n = pre$n, p_kept = pre$p, K = K, B = b$B, ell = ell, J = length(setup$blocks), s0 = length(S0),
    start_size = length(St), start_missed = length(missed), start_extras = length(extras), Phi_start = length(missed) + length(extras),
    start_eq_S0 = identical(St, S0), start_in_R0 = length(extras) <= 0, start_in_R1 = length(extras) <= 1, start_in_R2 = length(extras) <= 2,
    start_subset_S0 = length(extras) == 0, start_ties = sm$ties, start_truncated = sm$truncated,
    log_pi0_start = sm$log_pi0, log_pi0_S0 = lpi_S0, log_pi0_R0 = lpi_Rd[1], log_pi0_R1 = lpi_Rd[2], log_pi0_R2 = lpi_Rd[3],
    elig_start = sm$log_pi0 > log(0.5),
    F_S0 = F_S0, F_start = A$centre_F, F_endpoint = A$returned_F, F_best = A$best_scored_F,
    Fgap_S0_minus_start = F_S0 - A$centre_F,
    ls_termination = A$termination, ls_moves = A$moves, ls_certified = isTRUE(A$local_certified), ls_local_limit = isTRUE(A$local_limit),
    ls_n_eval = A$n_evaluated, ls_scans = length(centres),
    scored_S0 = scored_S0, endpoint_eq_S0 = identical(ret, S0), best_eq_S0 = identical(best, S0),
    certified_S0 = isTRUE(A$local_certified) && identical(ret, S0),
    endpoint_beats_S0 = A$returned_F > F_S0, best_beats_S0 = !identical(best, S0) && ls0_hpm_better(A$best_scored_F, best, F_S0, S0),
    endpoint_Phi = ls0_phi(ret, S0), endpoint_extras = length(setdiff(ret, S0)), endpoint_missed = length(setdiff(S0, ret)),
    best_Phi = ls0_phi(best, S0),
    path_progress_all = progress_moves, path_first_regress = first_regress,
    path_max_extras = max(path_extras), path_in_R0 = max(path_extras) <= 0, path_in_R1 = max(path_extras) <= 1, path_in_R2 = max(path_extras) <= 2,
    path_phi = paste(path_phi, collapse = ">"), path_moves = paste(mtype, collapse = " "),
    cap_ok = (length(missed) + length(extras) - 1) <= ell,
    S0_locmax = S0_locmax, S0_best_nbr_type = S0_best_nbr_type, S0_best_nbr_gap = S0_gap,
    lat_size = lat_size, lat_checked = lat_checked, lat_n = lat_n, lat_DS_fail = lat_fail,
    lat_DS_all = if (lat_checked) lat_fail == 0 else NA,
    lat_fail_types = lat_fail_types, lat_fail_minPhi = lat_fail_minPhi, lat_n_phi2 = lat_n_phi2, lat_fail_phi2 = lat_fail_phi2,
    path_in_lat = path_in_lat,
    lam_min_RU = lam_min,
    sec_blocks = setup$seconds[["blocks"]], sec_tables = setup$seconds[["tables"]], sec_start = setup$seconds[["start"]],
    sec_neighbours = setup$seconds[["neighbours"]], sec_mode = cpu_mode, sec_ls0_engine = A$seconds, sec_ls0 = cpu_ls0,
    sec_scan0 = cpu_scan0, sec_lat = cpu_lat, sec_setup = cpu_setup,
    cpu_total = cpu_all[["user.self"]] + cpu_all[["sys.self"]], wall_total = as.numeric(difftime(Sys.time(), w0, units = "secs")),
    stringsAsFactors = FALSE)
  detail <- list(S0 = S0, start = St, start_mode = sm, ls0 = A, scan_S0 = A0[c("termination", "returned", "returned_F", "n_evaluated")],
                 lat_fail_states = lat_fail_states, log_pi0_Rd = lpi_Rd, budgets = b[c("K", "B", "ell")],
                 blocks_of_S0 = vapply(S0, function(j) which(vapply(setup$blocks, function(bb) j %in% bb, TRUE)), 0L))
  list(row = row, detail = detail)
}
