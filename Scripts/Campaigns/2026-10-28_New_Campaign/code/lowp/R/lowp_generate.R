# LOWP generator (Regime L, p in {20, 30}): LOWP_SPEC.md L.1-L.4, master Part II.9.
# scenario_covariance() is copied UNCHANGED from the bench20261019 generator
# (F_2026-10-19.../code/R/gen_dev_data.R, itself verbatim from Oct-14 design.R). Draw order and RNG kind
# are those of design.R::generate_case(): X first via matrix(rnorm(n*p), n) %*% chol(Sigma), then eps.
# Sourcing this file defines functions only; nothing runs at source time.
#
#   generate_dataset(p, scenario, replicate, kind = c("prod", "dev"))  -> list(inputs, truth)
#   lowp_scenario_check(out)        -> writes tests/scenario_check_lowp.out, returns list(pass, ...)
#   lowp_seed_collision_check(out)  -> writes tests/seed_collisions.out, returns list(pass, ...)

LOWP_N       <- 200L
LOWP_SCALES  <- c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25)
LOWP_PS      <- c(20L, 30L)
# LOWP_SPEC L.3
LOWP_DATA_BASE <- list(prod = c(`20` = 1210000L, `30` = 1310000L), dev = c(`20` = 2210000L, `30` = 2310000L))
LOWP_FOLD_BASE <- list(prod = c(`20` = 3210000L, `30` = 3310000L), dev = c(`20` = 4210000L, `30` = 4310000L))
LOWP_METHOD_SEED_OFFSET <- 4000000L
LOWP_REPEAT_STEP        <- 1000L          # repeat m = 1..5: method seed + 1000 * m
LOWP_S0   <- c(`20` = 4L, `30` = 5L)       # D2
LOWP_STEP <- c(`20` = 1L, `30` = 1L)       # blocks = 1 + STEP * k

.lowp_script_dir <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) return(dirname(normalizePath(sub("^--file=", "", a[1L]), winslash = "/")))
  for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) return(dirname(normalizePath(fr$ofile, winslash = "/")))
  getwd()
}

# ---- covariance (verbatim from gen_dev_data.R) ------------------------------------------------------
scenario_covariance <- function(scenario, p=500L) {
  stopifnot(length(scenario)==1L, scenario %in% 1:6, p>=1L, p==as.integer(p))
  group <- ceiling(seq_len(p)/5)
  H <- outer(group,group,"==")
  I <- diag(p)
  switch(as.integer(scenario),
    I,
    0.5^abs(outer(seq_len(p),seq_len(p),"-")),
    0.7*H+0.3*I,
    0.85*H+0.15*I,
    0.3*matrix(1,p,p)+0.4*H+0.3*I,
    {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})
}

# ---- truth (master II.9 port, STEP = 1, S0 = {20: 4, 30: 5}); uses no random numbers ----------------
truth <- function(p) {
  stopifnot(as.character(p) %in% names(LOWP_S0))
  s0   <- LOWP_S0[[as.character(p)]]
  step <- LOWP_STEP[[as.character(p)]]
  pos  <- c(3L, 2L, 4L, 1L, 5L, 3L)
  pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
  k <- 0:(s0 - 1L)
  block <- 1L + step * k
  active <- 5L * (block - 1L) + pos[(k %% 6L) + 1L]
  list(active = active, beta = pattern[(k %% 6L) + 1L], block = block, pos = pos[(k %% 6L) + 1L],
       rho_s6 = 0.4 + 0.1 * ((block - 1L) %% 6L))
}

# float64 little-endian SHA-256, identical to benchmark common.R / gen_dev_data.R
f64_sha256 <- function(x) {
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
}

lowp_dataset_id <- function(p, scenario, replicate, kind = "prod")
  sprintf("%sp%04d_S%d_r%03d", if (kind == "dev") "dev_" else "", p, scenario, replicate)

lowp_seeds <- function(p, scenario, replicate, kind = "prod") {   # vectorised over p, scenario, replicate
  data_seed <- unname(LOWP_DATA_BASE[[kind]][as.character(p)]) + 10000L * as.integer(scenario) + as.integer(replicate)
  list(data_seed = data_seed,
       fold_seed = unname(LOWP_FOLD_BASE[[kind]][as.character(p)]) + 10000L * as.integer(scenario) + as.integer(replicate),
       method_seed = data_seed + LOWP_METHOD_SEED_OFFSET)
}

generate_dataset <- function(p, scenario, replicate, kind = c("prod", "dev")) {
  kind <- match.arg(kind)
  stopifnot(p %in% LOWP_PS, scenario %in% 1:6, replicate %in% 1:100)
  p <- as.integer(p); scenario <- as.integer(scenario); replicate <- as.integer(replicate)
  sd_ <- lowp_seeds(p, scenario, replicate, kind)
  n <- LOWP_N
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(sd_$data_seed)
  Sigma <- scenario_covariance(scenario, p)
  raw_X <- matrix(rnorm(n * p), nrow = n) %*% chol(Sigma)       # X first
  X <- scale(raw_X, center = TRUE, scale = TRUE)                 # sd with n - 1
  attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  eps <- rnorm(n, sd = 1)                                        # then noise
  tr <- truth(p)                                                 # no RNG use
  beta <- numeric(p); beta[tr$active] <- tr$beta
  signal <- drop(X %*% beta)
  Y <- sapply(LOWP_SCALES, function(cc) cc * signal + eps)
  colnames(Y) <- names(LOWP_SCALES)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(sd_$fold_seed)
  foldid <- sample(rep(1:10, length.out = n))
  dataset_id <- lowp_dataset_id(p, scenario, replicate, kind)
  list(inputs = list(X = X, Y = Y, foldid = foldid, dataset_id = dataset_id, p = p, n = n,
                     scenario = scenario, replicate = replicate, kind = kind,
                     data_seed = sd_$data_seed, fold_seed = sd_$fold_seed, method_seed = sd_$method_seed,
                     scales = LOWP_SCALES),
       truth = list(active = tr$active, beta = tr$beta, signal = signal, eps = eps,
                    scenario = scenario, dataset_id = dataset_id))
}

# ---- LOWP_SPEC L.2 expected values -----------------------------------------------------------------------
LOWP_EXPECTED <- list(
  active = list(`20` = c(3L, 7L, 14L, 16L), `30` = c(3L, 7L, 14L, 16L, 25L)),
  beta   = list(`20` = c(1.4, -1.0, 1.8, -1.2), `30` = c(1.4, -1.0, 1.8, -1.2, 0.8)),
  block  = list(`20` = 1:4, `30` = 1:5),
  pos    = list(`20` = c(3L, 2L, 4L, 1L), `30` = c(3L, 2L, 4L, 1L, 5L)),
  rho_s6 = list(`20` = c(.4, .5, .6, .7), `30` = c(.4, .5, .6, .7, .8)),
  min_eig = list(`20` = c(1.0000, 0.3351, 0.3000, 0.1500, 0.3000, 0.3000),
                 `30` = c(1.0000, 0.3341, 0.3000, 0.1500, 0.3000, 0.1000)),
  # nominal SNR c^2 beta' Sigma beta, rows c = 1 and c = 0.5, columns S1..S6 (2 decimals, L.2)
  snr_c100 = list(`20` = c(7.64, 6.36, 7.64, 7.64, 5.65, 7.64), `30` = c(8.28, 7.00, 8.28, 8.28, 6.77, 8.28)),
  snr_c050 = list(`20` = c(1.91, 1.59, 1.91, 1.91, 1.41, 1.91), `30` = c(2.07, 1.75, 2.07, 2.07, 1.69, 2.07)))
# Master tools/scenario_check.out, p = 30 block (read 2026-10-28), 3-decimal values
MASTER_P30 <- list(active = c(3L, 7L, 14L, 16L, 25L), blocks = 1:5, pos = c(3L, 2L, 4L, 1L, 5L),
                   rho = c(.4, .5, .6, .7, .8), beta = c(1.4, -1.0, 1.8, -1.2, 0.8),
                   min_eig = c(1.0000, 0.3341, 0.3000, 0.1500, 0.3000, 0.1000),
                   snr_c100 = c(8.280, 7.001, 8.280, 8.280, 6.768, 8.280),
                   snr_c050 = c(2.070, 1.750, 2.070, 2.070, 1.692, 2.070))

lowp_scenario_stats <- function(p) {
  tr <- truth(p); b <- numeric(p); b[tr$active] <- tr$beta
  s <- 1:6
  eig <- vapply(s, function(k) min(eigen(scenario_covariance(k, p), symmetric = TRUE, only.values = TRUE)$values), 0)
  q <- vapply(s, function(k) drop(crossprod(b, scenario_covariance(k, p) %*% b)), 0)
  list(truth = tr, min_eig = eig, snr_c100 = q, snr_c050 = 0.25 * q)
}

lowp_scenario_check <- function(out = file.path(.lowp_script_dir(), "..", "tests", "scenario_check_lowp.out")) {
  pass_all <- TRUE; lines <- character()
  add <- function(...) lines <<- c(lines, sprintf(...))
  res <- list()
  for (p in LOWP_PS) {
    key <- as.character(p); st <- lowp_scenario_stats(p); tr <- st$truth; ex <- LOWP_EXPECTED
    add("p=%d: active=[%s] blocks=[%s] pos=[%s] S6 rho=[%s] beta=[%s] distinct_blocks=%s max_block=%d/%d",
        p, paste(tr$active, collapse = ", "), paste(tr$block, collapse = ", "), paste(tr$pos, collapse = ", "),
        paste(sprintf("%.1f", tr$rho_s6), collapse = ", "), paste(sprintf("%.1f", tr$beta), collapse = ", "),
        !anyDuplicated(tr$block), max(tr$block), p %/% 5L)
    ok_tr <- identical(as.integer(tr$active), ex$active[[key]]) && identical(as.integer(tr$block), ex$block[[key]]) &&
      identical(as.integer(tr$pos), ex$pos[[key]]) && isTRUE(all.equal(tr$rho_s6, ex$rho_s6[[key]], tolerance = 1e-12)) &&
      identical(tr$beta, ex$beta[[key]])
    ok_eig <- all(abs(st$min_eig - ex$min_eig[[key]]) < 1e-4)
    ok_snr <- identical(round(st$snr_c100, 2), ex$snr_c100[[key]]) && identical(round(st$snr_c050, 2), ex$snr_c050[[key]])
    for (k in 1:6) add("  S%d: min eig=%.4f  SNR(c)=1:%.3f 0.5:%.3f", k, st$min_eig[k], st$snr_c100[k], st$snr_c050[k])
    add("  CHECK truth placement vs LOWP_SPEC L.2: %s", if (ok_tr) "PASS" else "FAIL")
    add("  CHECK smallest eigenvalues vs L.2 (tol 1e-4): %s", if (ok_eig) "PASS" else "FAIL")
    add("  CHECK nominal SNR (2 decimals) vs L.2: %s", if (ok_snr) "PASS" else "FAIL")
    ok_m <- TRUE
    if (p == 30L) {
      ok_m <- identical(as.integer(tr$active), MASTER_P30$active) && identical(as.integer(tr$block), MASTER_P30$blocks) &&
        identical(as.integer(tr$pos), MASTER_P30$pos) && isTRUE(all.equal(tr$rho_s6, MASTER_P30$rho)) &&
        identical(tr$beta, MASTER_P30$beta) && all(abs(st$min_eig - MASTER_P30$min_eig) < 1e-4) &&
        all(abs(st$snr_c100 - MASTER_P30$snr_c100) < 5e-4) && all(abs(st$snr_c050 - MASTER_P30$snr_c050) < 5e-4)
      add("  CHECK p=30 equals master tools/scenario_check.out rows (truth, min eig, SNR at 3 decimals): %s",
          if (ok_m) "PASS" else "FAIL")
    }
    pass_all <- pass_all && ok_tr && ok_eig && ok_snr && ok_m
    res[[key]] <- list(stats = st, ok_truth = ok_tr, ok_eig = ok_eig, ok_snr = ok_snr, ok_master = ok_m)
  }
  add("OVERALL: %s", if (pass_all) "PASS" else "FAIL")
  if (!is.null(out)) { dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE); writeLines(lines, out) }
  invisible(list(pass = pass_all, by_p = res, lines = lines))
}

# ---- seed collision check (LOWP_SPEC L.3) ---------------------------------------------------------------
# Every seed set is the explicit set {base + 10000*s + r : s = 1..6, r = 1..100}, shifted by the method offset and the
# repeat step where the role needs it, so the check is exact (set intersection), not interval-based.
# Role families (one set per p x kind x role): data, fold, method (= data + 4,000,000), repeat m = 1..5
# (= method + 1,000 m), for p in {20, 30, 500, 1000} and kind in {prod, dev}, plus the sealed held-out bases
# (data 7,610,000 / 7,710,000; folds 8,610,000 / 8,710,000) with their method and repeat families.
# p = 30 (and 500, 1000) use master II.7's own bases, so they appear ONCE (they are master's sets, shared by design);
# p = 20 is the only new family. Pairwise disjointness of all sets is checked.
.lowp_seed_set <- function(base, shift = 0L) as.vector(outer(10000L * 1:6, 1:100, "+")) + base + shift

lowp_seed_families <- function(p20 = list(data = LOWP_DATA_BASE$prod[["20"]], dev = LOWP_DATA_BASE$dev[["20"]],
                                          fold = LOWP_FOLD_BASE$prod[["20"]], devfold = LOWP_FOLD_BASE$dev[["20"]])) {
  bases <- list(
    `20`   = unlist(p20),
    `30`   = c(data = 1310000L, dev = 2310000L, fold = 3310000L, devfold = 4310000L),   # master II.7 (= LOWP_SPEC L.3)
    `500`  = c(data = 1410000L, dev = 2410000L, fold = 3410000L, devfold = 4410000L),
    `1000` = c(data = 1510000L, dev = 2510000L, fold = 3510000L, devfold = 4510000L))
  fam <- list()
  add <- function(name, base, shift = 0L, owner) fam[[name]] <<- list(set = .lowp_seed_set(base, shift), owner = owner)
  for (pk in names(bases)) {
    b <- bases[[pk]]; owner <- if (pk == "20") "lowp (new)" else if (pk == "30") "master II.7 = LOWP L.3 (shared)" else "master II.7"
    for (kind in c("prod", "dev")) {
      db <- if (kind == "prod") b[["data"]] else b[["dev"]]; fb <- if (kind == "prod") b[["fold"]] else b[["devfold"]]
      add(sprintf("p%s %s data", pk, kind), db, 0L, owner)
      add(sprintf("p%s %s fold", pk, kind), fb, 0L, owner)
      add(sprintf("p%s %s method", pk, kind), db, LOWP_METHOD_SEED_OFFSET, owner)
      for (m in 1:5) add(sprintf("p%s %s repeat m=%d", pk, kind, m), db, LOWP_METHOD_SEED_OFFSET + LOWP_REPEAT_STEP * m, owner)
    }
  }
  for (b in c(7610000L, 7710000L)) {
    add(sprintf("held-out data %s", format(b, big.mark = ",")), b, 0L, "F_2026-10-19 RUNS.md")
    add(sprintf("held-out method %s", format(b, big.mark = ",")), b, LOWP_METHOD_SEED_OFFSET, "derived (data + 4e6)")
    for (m in 1:5) add(sprintf("held-out repeat m=%d %s", m, format(b, big.mark = ",")), b, LOWP_METHOD_SEED_OFFSET + LOWP_REPEAT_STEP * m, "derived")
  }
  for (b in c(8610000L, 8710000L)) add(sprintf("held-out fold %s", format(b, big.mark = ",")), b, 0L, "F_2026-10-19 RUNS.md")
  fam
}

lowp_seed_collision_check <- function(out = file.path(.lowp_script_dir(), "..", "tests", "seed_collisions.out"), families = NULL) {
  fam <- if (is.null(families)) lowp_seed_families() else families
  nm <- names(fam); lines <- character(); add <- function(...) lines <<- c(lines, sprintf(...))
  add("LOWP seed collision check (LOWP_SPEC L.3). Each set = {base + 10000*s + r, s=1..6, r=1..100} (+ method offset 4,000,000 / repeat step 1,000*m).")
  add("")
  add("%d role sets (p x kind x {data, fold, method, repeat m=1..5} for p = 20, 30, 500, 1000, plus held-out data/fold/method/repeat families):", length(nm))
  for (k in nm) add("  %-38s [%d, %d]  n=%d  owner: %s", k, min(fam[[k]]$set), max(fam[[k]]$set), length(unique(fam[[k]]$set)), fam[[k]]$owner)
  add("")
  bad_size <- nm[vapply(fam, function(z) length(unique(z$set)) != length(z$set) || length(z$set) != 600L, TRUE)]
  if (length(bad_size)) add("[FAIL] sets that are not 600 distinct seeds: %s", paste(bad_size, collapse = ", "))
  n_pairs <- 0L; coll <- character()
  for (i in seq_along(nm)) for (j in seq_len(i - 1L)) {
    n_pairs <- n_pairs + 1L
    ov <- intersect(fam[[nm[i]]]$set, fam[[nm[j]]]$set)
    if (length(ov)) coll <- c(coll, sprintf("[COLLISION] %s vs %s: %d seeds, e.g. %d", nm[i], nm[j], length(ov), ov[1L]))
  }
  add("Pairwise comparison of all %d pairs of distinct sets: %d collisions.", n_pairs, length(coll))
  for (z in coll) add("  %s", z)
  add("The p = 30, 500 and 1000 ranges are master II.7's own; they are listed once (shared by design) and compared with everything else.")
  add("")
  add("Repeat offsets: the increment relative to the method seed is 1,000 m = 1,000..5,000 (m = 1..5); including r (<= 100) the offset inside the")
  add("10000-slot of the dataset is 1,001..5,100, which no base + 10000*s + r (offset r in 1..100) can reach. All %d repeat sets above are in the pairwise check.",
      sum(grepl("repeat", nm)))
  add("Fixed internal seeds that are intentionally reused and disjoint from these sets: abess F5 seed 1 (master II.7).")
  add("")
  total <- length(coll) + length(bad_size)
  add("OVERALL: %s (%d sets, %d pairs, %d collisions)", if (total == 0L) "PASS (no overlap)" else "FAIL", length(nm), n_pairs, length(coll))
  if (!is.null(out)) { dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE); writeLines(lines, out) }
  invisible(list(pass = total == 0L, n_sets = length(nm), n_pairs = n_pairs, collisions = coll, lines = lines))
}

# ---- manifest validators (shared by lowp_verify.R and lowp_verify_nots.R) --------------------------------
LOWP_INPUT_MANIFEST_COLS <- c("dataset_id", "p", "scenario", "replicate", "data_seed", "fold_seed", "method_seed", "file", "file_sha256",
                              "x_sha256", paste0("y_", names(LOWP_SCALES), "_sha256"), "fold_sha256")
LOWP_TRUTH_MANIFEST_COLS <- c("dataset_id", "file", "file_sha256", "signal_sha256", "eps_sha256", "active", "beta")
LOWP_HEX64 <- "^[0-9a-f]{64}$"

# Independently constructed expected grid for a kind: p in {20, 30} x S1..S6 x r in 1..100 (prod) / 1..5 (dev)
lowp_expected_grid <- function(kind) {
  g <- expand.grid(replicate = if (kind == "prod") 1:100 else 1:5, scenario = 1:6, p = c(20L, 30L), KEEP.OUT.ATTRS = FALSE)
  g <- g[, c("p", "scenario", "replicate")]
  g$dataset_id <- lowp_dataset_id(g$p, g$scenario, g$replicate, kind)
  g$file <- sprintf("inputs/p%04d/%s.rds", g$p, g$dataset_id)
  g$truth_file <- sprintf("truth/p%04d/%s.rds", g$p, g$dataset_id)
  sd <- lowp_seeds(g$p, g$scenario, g$replicate, kind)
  g$data_seed <- sd$data_seed; g$fold_seed <- sd$fold_seed; g$method_seed <- sd$method_seed
  g
}
# Returns list(structure = <chr problems that make the manifests unusable>, seed = <chr seed-field disagreements>)
# mi, mt: data.frames read with colClasses = "character".
lowp_validate_manifests <- function(mi, mt, kind) {
  st <- character(); sd <- character()
  if (!identical(names(mi), LOWP_INPUT_MANIFEST_COLS)) st <- c(st, sprintf("inputs manifest columns differ from I1 (got: %s)", paste(names(mi), collapse = ",")))
  if (!identical(names(mt), LOWP_TRUTH_MANIFEST_COLS)) st <- c(st, sprintf("truth manifest columns differ from I1 (got: %s)", paste(names(mt), collapse = ",")))
  if (length(st)) return(list(structure = st, seed = sd))
  want <- lowp_expected_grid(kind)
  if (nrow(mi) != nrow(want)) st <- c(st, sprintf("inputs manifest has %d rows, expected %d", nrow(mi), nrow(want)))
  if (nrow(mt) != nrow(want)) st <- c(st, sprintf("truth manifest has %d rows, expected %d", nrow(mt), nrow(want)))
  for (nm in c("dataset_id")) {
    if (anyDuplicated(mi[[nm]])) st <- c(st, sprintf("duplicate dataset_id in inputs manifest: %s", paste(utils::head(mi[[nm]][duplicated(mi[[nm]])], 3), collapse = ",")))
    if (anyDuplicated(mt[[nm]])) st <- c(st, sprintf("duplicate dataset_id in truth manifest: %s", paste(utils::head(mt[[nm]][duplicated(mt[[nm]])], 3), collapse = ",")))
  }
  if (!setequal(mi$dataset_id, want$dataset_id)) st <- c(st, sprintf("inputs manifest ids differ from the expected grid (missing %d, unexpected %d)",
      length(setdiff(want$dataset_id, mi$dataset_id)), length(setdiff(mi$dataset_id, want$dataset_id))))
  if (!setequal(mt$dataset_id, mi$dataset_id)) st <- c(st, "truth manifest ids are not one-to-one with the inputs manifest ids")
  for (cn in intersect(c("p", "scenario", "replicate", "data_seed", "fold_seed", "method_seed"), names(mi)))
    if (anyNA(suppressWarnings(as.integer(mi[[cn]]))) || any(as.character(suppressWarnings(as.integer(mi[[cn]]))) != mi[[cn]])) st <- c(st, sprintf("inputs manifest column %s is not canonical integer text", cn))
  for (cn in c("file_sha256", "x_sha256", paste0("y_", names(LOWP_SCALES), "_sha256"), "fold_sha256"))
    if (!all(grepl(LOWP_HEX64, mi[[cn]]))) st <- c(st, sprintf("inputs manifest column %s has non-SHA-256 entries", cn))
  for (cn in c("file_sha256", "signal_sha256", "eps_sha256"))
    if (!all(grepl(LOWP_HEX64, mt[[cn]]))) st <- c(st, sprintf("truth manifest column %s has non-SHA-256 entries", cn))
  if (length(st)) return(list(structure = st, seed = sd))
  # keyed comparison with the independently built grid (row order does not matter)
  k <- match(mi$dataset_id, want$dataset_id); kt <- match(mt$dataset_id, want$dataset_id)
  if (anyNA(k) || anyNA(kt)) return(list(structure = c(st, "manifest ids outside the expected grid"), seed = sd))
  for (cn in c("p", "scenario", "replicate")) {
    bad <- mi$dataset_id[as.character(want[[cn]][k]) != mi[[cn]]]
    if (length(bad)) st <- c(st, sprintf("column %s differs from the id grid for %d rows (e.g. %s)", cn, length(bad), bad[1L]))
  }
  bad <- mi$dataset_id[mi$file != want$file[k]]; if (length(bad)) st <- c(st, sprintf("non-canonical inputs file path for %d rows (e.g. %s: %s)", length(bad), bad[1L], mi$file[mi$dataset_id == bad[1L]]))
  bad <- mt$dataset_id[mt$file != want$truth_file[kt]]; if (length(bad)) st <- c(st, sprintf("non-canonical truth file path for %d rows (e.g. %s: %s)", length(bad), bad[1L], mt$file[mt$dataset_id == bad[1L]]))
  for (cn in c("data_seed", "fold_seed", "method_seed")) {
    bad <- mi$dataset_id[as.character(want[[cn]][k]) != mi[[cn]]]
    if (length(bad)) sd <- c(sd, sprintf("%s differs from base + 10000*s + r%s for %d rows (e.g. %s: manifest %s, design %s)", cn,
        if (cn == "method_seed") " + 4,000,000" else "", length(bad), bad[1L], mi[[cn]][mi$dataset_id == bad[1L]], want[[cn]][k][mi$dataset_id == bad[1L]]))
  }
  # truth text fields
  ta <- vapply(want$p[kt], function(p) paste(truth(p)$active, collapse = ";"), ""); tb <- vapply(want$p[kt], function(p) paste(truth(p)$beta, collapse = ";"), "")
  bad <- mt$dataset_id[mt$active != ta | mt$beta != tb]
  if (length(bad)) st <- c(st, sprintf("truth manifest active/beta text differs from truth(p) for %d rows (e.g. %s)", length(bad), bad[1L]))
  list(structure = st, seed = sd)
}
