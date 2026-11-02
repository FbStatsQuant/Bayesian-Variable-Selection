# Gate G2 checks for the LOWP datasets (LOWP_SPEC L.6 checks 1, 2, 3, 4(a), 5, 6, 7).
#
#   Rscript lowp_verify.R <STUDY root> [--report report.md] [--bench-gen <original gen_dev_data.R>]
#
# Exit status: 0 = every check PASS; 1 = at least one FAIL; 3 = no FAIL but at least one check INCOMPLETE (a prerequisite
# such as the original-generator source was not supplied). INCOMPLETE is never a PASS.
# Check 4(b) (NOTS regeneration of all 1,200 + 60 hashes and the six copies) is lowp_verify_nots.R.
# Reads inputs/ AND truth/ (this is a generator check, not a fitting job). Writes tests/scenario_check_lowp.out and
# tests/seed_collisions.out as a by-product (checks 1 and the L.3 collision check).

.ver_dir <- local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1L]), winslash = "/"))
  else { p <- NULL; for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { p <- dirname(normalizePath(fr$ofile, winslash = "/")); break }
         if (is.null(p)) getwd() else p }
})
if (!exists("generate_dataset", mode = "function")) source(file.path(.ver_dir, "lowp_generate.R"))

# ---- literal covariance transcription of master II.4 (independent of lowp scenario_covariance) --------------------
# H_jk = 1 iff j, k are in the same block of five; J all ones; I identity; built entry by entry from the table formulas.
master_cov_literal <- function(scenario, p) {
  blk <- function(j) (j - 1L) %/% 5L + 1L
  S <- matrix(0, p, p)
  for (j in seq_len(p)) for (k in seq_len(p)) {
    H <- as.numeric(blk(j) == blk(k)); Id <- as.numeric(j == k)
    S[j, k] <- switch(scenario,
      Id,                                           # S1  I_p
      0.5^abs(j - k),                               # S2  AR(1)
      0.7 * H + 0.3 * Id,                           # S3  0.7H + 0.3I
      0.85 * H + 0.15 * Id,                         # S4  0.85H + 0.15I
      0.3 * 1 + 0.4 * H + 0.3 * Id,                 # S5  0.3J + 0.4H + 0.3I
      if (j == k) 1 else if (blk(j) == blk(k)) 0.4 + 0.1 * ((blk(j) - 1L) %% 6L) else 0)   # S6  rho_b in block b, 0 between
  }
  S
}

# ---- literal, independent transcription of master Part II.9 (generate_dataset, truth, folds) ----------------
master_truth_9 <- function(p) {
  S0 <- c(`30` = 5L, `500` = 14L, `1000` = 14L); STEP <- c(`30` = 1L, `500` = 7L, `1000` = 13L)
  POS <- c(3L, 2L, 4L, 1L, 5L, 3L); PATTERN <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
  s0 <- S0[[as.character(p)]]; k <- 0:(s0 - 1L)
  blocks <- 1L + STEP[[as.character(p)]] * k
  list(active = 5L * (blocks - 1L) + POS[(k %% 6L) + 1L], beta = PATTERN[(k %% 6L) + 1L])
}
master_generate_dataset_9 <- function(p, scenario, replicate, kind = c("prod", "dev"), scen_cov = master_cov_literal, n = 200L) {
  kind <- match.arg(kind)
  stopifnot(p %in% c(30L, 500L, 1000L), scenario %in% 1:6, replicate %in% 1:100)
  base <- list(prod = c(`30` = 1310000L, `500` = 1410000L, `1000` = 1510000L),
               dev  = c(`30` = 2310000L, `500` = 2410000L, `1000` = 2510000L))[[kind]][[as.character(p)]]
  seed <- base + 10000L * scenario + replicate
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  Sigma <- scen_cov(scenario, p)
  raw_X <- matrix(rnorm(n * p), nrow = n) %*% chol(Sigma)
  X <- scale(raw_X, center = TRUE, scale = TRUE)
  eps <- rnorm(n, sd = 1)
  tr <- master_truth_9(p)
  beta <- numeric(p); beta[tr$active] <- tr$beta
  signal <- drop(X %*% beta)
  Y <- sapply(c(c100 = 1, c075 = .75, c050 = .50, c035 = .35, c025 = .25), function(c) c * signal + eps)
  fold_seed <- c(`30` = 3310000L, `500` = 3410000L, `1000` = 3510000L)[[as.character(p)]] + 10000L * scenario + replicate
  if (kind == "dev") fold_seed <- c(`30` = 4310000L, `500` = 4410000L, `1000` = 4510000L)[[as.character(p)]] + 10000L * scenario + replicate
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(fold_seed)
  foldid <- sample(rep(1:10, length.out = 200))
  list(X = X, eps = eps, signal = signal, Y = Y, foldid = foldid, seed = seed, fold_seed = fold_seed, active = tr$active)
}
.strip <- function(x) { d <- dim(x); attributes(x) <- NULL; if (!is.null(d)) dim(x) <- d; x }

# ---- per-dataset gate: I1 schema, truth-free inputs, metadata vs manifest and design, standardisation, signal, response ----
LOWP_INPUT_ALLOWED <- c("X", "Y", "foldid", "dataset_id", "p", "n", "scenario", "replicate", "kind", "data_seed", "fold_seed", "method_seed", "scales")
LOWP_INPUT_REQUIRED <- c("X", "Y", "foldid", "dataset_id", "n", "p", "kind", "scenario", "replicate", "scales", "data_seed", "fold_seed", "method_seed")   # INTERFACES I1 (all 13 fields required)
LOWP_TRUTH_FIELDS <- c("active", "beta", "signal", "eps", "scenario", "dataset_id")
LOWP_SIGNAL_TOL <- 1e-12     # relative: max|signal - X beta| <= LOWP_SIGNAL_TOL * max(1, max|signal|)

lowp_check_dataset <- function(inp, tr, mrow, trow, p, s, r, kind) {
  prob <- list(schema = character(), meta = character(), truth = character(), std = character(), signal = character(), resp = character(), hash = character())
  addp <- function(k, ...) prob[[k]] <<- c(prob[[k]], sprintf(...))
  id <- lowp_dataset_id(p, s, r, kind); sd <- lowp_seeds(p, s, r, kind); tp <- truth(p)
  # input schema (no truth fields, I1 types)
  if (!is.list(inp)) { addp("schema", "input is not a list"); return(list(problems = prob, metrics = NULL)) }
  nm <- names(inp)
  if (anyDuplicated(nm)) addp("schema", "duplicated input field names")
  if (length(miss <- setdiff(LOWP_INPUT_REQUIRED, nm))) addp("schema", "missing I1 input fields: %s", paste(miss, collapse = ","))
  if (length(extra <- setdiff(nm, LOWP_INPUT_ALLOWED))) addp("schema", "unexpected input fields (truth leakage?): %s", paste(extra, collapse = ","))
  X <- inp$X; Y <- inp$Y
  if (!(is.matrix(X) && is.double(X) && identical(attributes(X), list(dim = c(LOWP_N, p))))) addp("schema", "X is not a plain double %dx%d matrix without scaled:* attributes", LOWP_N, p)
  if (!(is.matrix(Y) && is.double(Y) && identical(attributes(Y), list(dim = c(LOWP_N, 5L), dimnames = list(NULL, names(LOWP_SCALES)))))) addp("schema", "Y is not a double %dx5 matrix with columns c100..c025", LOWP_N)
  if (!(is.integer(inp$foldid) && is.null(attributes(inp$foldid)) && length(inp$foldid) == LOWP_N)) addp("schema", "foldid is not a plain integer vector of length %d", LOWP_N)
  else if (!(identical(sort(unique(inp$foldid)), 1:10) && all(tabulate(inp$foldid, 10) == 20))) addp("schema", "foldid is not 10 balanced folds")
  # metadata: types, design values, manifest agreement
  intf <- function(x) is.integer(x) && length(x) == 1L && !is.na(x)
  chk_int <- function(nm_, want) if (!(intf(inp[[nm_]]) && identical(inp[[nm_]], as.integer(want)))) addp("meta", "%s is %s, design says %s", nm_, format(inp[[nm_]]), format(want))
  if (!identical(inp$dataset_id, id)) addp("meta", "dataset_id is %s, expected %s", format(inp$dataset_id), id)
  chk_int("p", p); chk_int("scenario", s); chk_int("replicate", r)
  chk_int("data_seed", sd$data_seed); chk_int("fold_seed", sd$fold_seed); chk_int("method_seed", sd$method_seed)
  if (!identical(inp$n, LOWP_N)) addp("meta", "n is %s, expected 200", paste(format(inp$n), collapse = ","))
  if (!identical(inp$kind, kind)) addp("meta", "kind is %s, expected %s", paste(format(inp$kind), collapse = ","), kind)
  if (!identical(inp$scales, LOWP_SCALES)) addp("meta", "scales differ from the fixed design")
  if (!is.null(mrow)) for (cn in c("p", "scenario", "replicate", "data_seed", "fold_seed", "method_seed", "dataset_id"))
    if (!identical(as.character(inp[[cn]]), as.character(mrow[[cn]]))) addp("meta", "input %s (%s) differs from the manifest (%s)", cn, format(inp[[cn]]), format(mrow[[cn]]))
  # truth object schema
  if (!is.list(tr) || !setequal(names(tr), LOWP_TRUTH_FIELDS) || anyDuplicated(names(tr))) addp("truth", "truth fields are not exactly {%s}", paste(LOWP_TRUTH_FIELDS, collapse = ","))
  else {
    if (!(identical(tr$active, tp$active))) addp("truth", "truth$active differs from truth(p)")
    if (!(identical(tr$beta, tp$beta))) addp("truth", "truth$beta differs from truth(p)")
    if (!(identical(tr$scenario, as.integer(s)))) addp("truth", "truth$scenario is %s", format(tr$scenario))
    if (!identical(tr$dataset_id, id)) addp("truth", "truth$dataset_id differs")
    for (nm_ in c("signal", "eps")) if (!(is.double(tr[[nm_]]) && is.null(attributes(tr[[nm_]])) && length(tr[[nm_]]) == LOWP_N)) addp("truth", "truth$%s is not a plain double vector of length 200", nm_)
  }
  if (length(prob$schema) || length(prob$truth)) return(list(problems = prob, metrics = NULL))   # numerics below need the schema
  cs <- LOWP_SCALES
  # check 2
  dm <- max(abs(colMeans(X))); dv <- max(abs(colSums(X^2) / (LOWP_N - 1) - 1))
  if (!(dm < 1e-10 && dv < 1e-10)) addp("std", "standardisation: max|colMean| %.2e, max|var-1| %.2e", dm, dv)
  # signal = X beta, explicit tolerance; then Y against that signal and eps
  bfull <- numeric(p); bfull[tp$active] <- tp$beta
  sig_err <- max(abs(tr$signal - drop(X %*% bfull))); sig_lim <- LOWP_SIGNAL_TOL * max(1, max(abs(tr$signal)))
  if (!(sig_err <= sig_lim)) addp("signal", "signal differs from X beta by %.2e (limit %.2e)", sig_err, sig_lim)
  err <- max(vapply(names(cs), function(k) max(abs(Y[, k] - (cs[[k]] * tr$signal + tr$eps))), 0)); lim <- 1e-12 * max(1, max(abs(Y)))
  if (!(err <= lim)) addp("resp", "response error %.2e exceeds %.2e", err, lim)
  # hashes of the loaded arrays against the manifest rows
  if (!is.null(mrow) && !is.null(trow)) {
    h_ok <- identical(f64_sha256(X), mrow$x_sha256) && identical(f64_sha256(inp$foldid), mrow$fold_sha256) &&
      all(vapply(names(cs), function(k) identical(f64_sha256(Y[, k]), mrow[[paste0("y_", k, "_sha256")]]), TRUE)) &&
      identical(f64_sha256(tr$signal), trow$signal_sha256) && identical(f64_sha256(tr$eps), trow$eps_sha256) &&
      identical(paste(tr$active, collapse = ";"), trow$active) && identical(paste(tr$beta, collapse = ";"), trow$beta)
    if (!h_ok) addp("hash", "an array hash or the active/beta text differs from the manifest")
  }
  list(problems = prob, metrics = c(mean = dm, var = dv, sig = sig_err, sig_lim = sig_lim, resp = err, resp_rel = err / lim))
}

# ---- Sigma sanity helpers (check 6) ----------------------------------------------------------------------
lowp_block_corr <- function(X) {       # per-block mean within-block off-diagonal sample correlation; mean between-block correlation
  p <- ncol(X); R <- cor(X); g <- ceiling(seq_len(p) / 5)
  list(within = vapply(seq_len(p / 5), function(b) { i <- which(g == b); mean(R[i, i][upper.tri(R[i, i])]) }, 0),
       between = mean(R[outer(g, g, "!=")]))
}
lowp_pop_blocks <- function(s, p) {
  S <- scenario_covariance(s, p); g <- ceiling(seq_len(p) / 5)
  list(within = vapply(seq_len(p / 5), function(b) { i <- which(g == b); mean(S[i, i][upper.tri(S[i, i])]) }, 0), between = mean(S[outer(g, g, "!=")]))
}
# W: replicates x blocks matrix of per-block within-block means; B: vector of between-block means (S5 only); tol 0.02.
# S2 (0.5^|j-k| within block) is descriptive, as in L.6.6; S1, S3-S6 are gated block by block, S5 also between blocks.
lowp_sigma_eval <- function(W, B, s, p, tol = 0.02, population = NULL) {
  pop <- if (is.null(population)) lowp_pop_blocks(s, p) else population
  dev_b <- abs(colMeans(W) - pop$within); dev_btw <- if (s == 5L) abs(mean(B) - pop$between) else NA_real_
  gated <- s != 2L
  list(pass = !gated || (all(dev_b <= tol) && (is.na(dev_btw) || dev_btw <= tol)), max_block_dev = max(dev_b), worst_block = which.max(dev_b),
       pooled_dev = abs(mean(W) - mean(pop$within)), between_dev = dev_btw, gated = gated,
       text = sprintf("p%d S%d: max block |d| %.4f (block %d: pop %.3f, sample %.3f)%s%s", p, s, max(dev_b), which.max(dev_b), pop$within[which.max(dev_b)],
                      colMeans(W)[which.max(dev_b)], if (s == 5L) sprintf("; between-block |d| %.4f", dev_btw) else "", if (gated) "" else " [descriptive]"))
}

# ---- main -------------------------------------------------------------------------------------------------
lowp_verify <- function(root, report = file.path(.ver_dir, "..", "tests", "VERIFY_REPORT.md"), bench_gen = NULL) {
  stopifnot(requireNamespace("digest", quietly = TRUE))
  root <- normalizePath(root, winslash = "/", mustWork = TRUE)
  t0 <- proc.time()[["elapsed"]]
  checks <- list()
  add <- function(id, title, status, detail) { if (is.logical(status)) status <- if (isTRUE(status)) "PASS" else "FAIL"
    checks[[length(checks) + 1L]] <<- list(id = id, title = title, status = status, detail = detail) }
  trees <- list(prod = root, dev = file.path(root, "dev"))
  rd <- function(f) utils::read.csv(f, stringsAsFactors = FALSE, colClasses = "character")
  mf <- lapply(trees, function(b) list(inp = rd(file.path(b, "manifests", "inputs_manifest_lowp.csv")), tr = rd(file.path(b, "manifests", "truth_manifest_lowp.csv"))))

  # ---- Check 1 ---------------------------------------------------------------------------------------
  sc <- lowp_scenario_check()   # writes tests/scenario_check_lowp.out
  add(1, "Truth placement, smallest eigenvalues (1e-4), nominal SNR vs LOWP_SPEC L.2; p = 30 vs master scenario_check.out",
      sc$pass, sprintf("p=20 active %s; p=30 active %s; min eig p20 %s | p30 %s; SNR(c=1) p20 %s | p30 %s",
        paste(truth(20L)$active, collapse = ","), paste(truth(30L)$active, collapse = ","),
        paste(sprintf("%.4f", sc$by_p[["20"]]$stats$min_eig), collapse = "/"), paste(sprintf("%.4f", sc$by_p[["30"]]$stats$min_eig), collapse = "/"),
        paste(sprintf("%.2f", sc$by_p[["20"]]$stats$snr_c100), collapse = "/"), paste(sprintf("%.2f", sc$by_p[["30"]]$stats$snr_c100), collapse = "/")))

  # ---- manifests: exact grids, schema, canonical paths (feeds check 5) ------------------------------------------
  mval <- list(); man_problems <- character(); seed_problems <- character()
  for (kind in c("prod", "dev")) { v <- lowp_validate_manifests(mf[[kind]]$inp, mf[[kind]]$tr, kind)
    if (length(v$structure)) man_problems <- c(man_problems, paste0(kind, ": ", v$structure)); if (length(v$seed)) seed_problems <- c(seed_problems, paste0(kind, ": ", v$seed)) }
  # full relative file sets on disk against the canonical expected paths (not basenames)
  fileset_problems <- character()
  for (kind in c("prod", "dev")) {
    b <- trees[[kind]]; g <- lowp_expected_grid(kind)
    for (pair in list(c("inputs", "file"), c("truth", "truth_file"))) {
      onfs <- sort(list.files(file.path(b, pair[1L]), recursive = TRUE, all.files = TRUE)); want <- sort(sub(paste0("^", pair[1L], "/"), "", g[[pair[2L]]]))
      if (!identical(onfs, want)) fileset_problems <- c(fileset_problems, sprintf("%s/%s: %d files on disk, %d expected (missing %d, unexpected %d)", kind, pair[1L], length(onfs), length(want),
          length(setdiff(want, onfs)), length(setdiff(onfs, want))))
    }
  }

  # ---- Checks 2, 3, schema, signal, hashes over every sealed dataset --------------------------------------------
  n_ds <- 0L; cats <- c("schema", "meta", "truth", "std", "signal", "resp", "hash"); bad <- setNames(vector("list", length(cats)), cats); for (k in cats) bad[[k]] <- character()
  worst <- c(mean = 0, var = 0, sig = 0, resp = 0, resp_rel = 0); readonly_ok <- TRUE
  seeds <- list(data = integer(), fold = integer(), method = integer())
  blk <- list()   # check 6
  for (kind in c("prod", "dev")) {
    b <- trees[[kind]]; m <- mf[[kind]]$inp; mt <- mf[[kind]]$tr
    if (length(man_problems[startsWith(man_problems, paste0(kind, ":"))])) next    # unusable manifest: reported by check 5, no per-file loop
    for (i in seq_len(nrow(m))) {
      id <- m$dataset_id[i]; p <- as.integer(m$p[i]); s <- as.integer(m$scenario[i]); r <- as.integer(m$replicate[i])
      fi <- file.path(b, m$file[i]); trow <- mt[mt$dataset_id == id, ]; ft <- file.path(b, trow$file)
      if (!file.exists(fi) || !file.exists(ft)) { bad$schema <- c(bad$schema, paste(id, "file missing")); next }
      if (any(file.access(c(fi, ft), 2L) == 0L)) readonly_ok <- FALSE
      inp <- readRDS(fi); tr <- readRDS(ft); n_ds <- n_ds + 1L
      res <- lowp_check_dataset(inp, tr, m[i, ], trow, p, s, r, kind)
      for (k in cats) if (length(res$problems[[k]])) bad[[k]] <- c(bad[[k]], paste0(id, ": ", res$problems[[k]]))
      if (!is.null(res$metrics)) { worst["mean"] <- max(worst["mean"], res$metrics[["mean"]]); worst["var"] <- max(worst["var"], res$metrics[["var"]])
        worst["sig"] <- max(worst["sig"], res$metrics[["sig"]]); worst["resp"] <- max(worst["resp"], res$metrics[["resp"]]); worst["resp_rel"] <- max(worst["resp_rel"], res$metrics[["resp_rel"]]) }
      if (!identical(digest::digest(file = fi, algo = "sha256"), m$file_sha256[i]) || !identical(digest::digest(file = ft, algo = "sha256"), trow$file_sha256))
        bad$hash <- c(bad$hash, paste0(id, ": file SHA-256 differs from the manifest"))
      seeds$data <- c(seeds$data, as.integer(m$data_seed[i])); seeds$fold <- c(seeds$fold, as.integer(m$fold_seed[i])); seeds$method <- c(seeds$method, as.integer(m$method_seed[i]))
      if (kind == "prod" && is.matrix(inp$X)) { bc <- lowp_block_corr(inp$X); blk[[length(blk) + 1L]] <- list(p = p, s = s, r = r, within = bc$within, between = bc$between) }
    }
  }
  nf <- function(k) length(bad[[k]])
  add("I1", "I1 schema: inputs carry exactly the I1 fields (no truth fields), truth carries exactly its five fields (+ id); types, lengths, folds; metadata equals manifest row and fixed design (p, n, kind, scenario, replicate, seeds, scales)",
      nf("schema") + nf("meta") + nf("truth") == 0L && n_ds == 1260L,
      sprintf("%d datasets read; schema failures %d, metadata failures %d, truth-object failures %d%s", n_ds, nf("schema"), nf("meta"), nf("truth"),
              if (nf("schema") + nf("meta") + nf("truth")) paste0("; first: ", paste(utils::head(c(bad$schema, bad$meta, bad$truth), 3), collapse = " | ")) else ""))
  add(2, "Standardisation: max|colMeans(X)| < 1e-10 and max|colSums(X^2)/(n-1) - 1| < 1e-10, every dataset", nf("std") == 0L && n_ds == 1260L,
      sprintf("%d datasets; worst |colMean| = %.2e; worst |var - 1| = %.2e; failures: %d", n_ds, worst[["mean"]], worst[["var"]], nf("std")))
  add("2b", sprintf("Signal: stored truth signal equals X beta (beta from truth(p)) within %.0e * max(1, max|signal|), every dataset", LOWP_SIGNAL_TOL), nf("signal") == 0L && n_ds == 1260L,
      sprintf("worst |signal - X beta| = %.2e; failures: %d", worst[["sig"]], nf("signal")))
  add(3, "Response: max|Y[,c] - (c*signal + eps)| <= 1e-12*max(1, max|Y|), all five columns, every dataset (signal gated in 2b)", nf("resp") == 0L && n_ds == 1260L,
      sprintf("worst abs error = %.2e; worst error / limit = %.3f; failures: %d", worst[["resp"]], worst[["resp_rel"]], nf("resp")))

  # ---- Check 4(a): fresh Rscript process ---------------------------------------------------------------
  tmp <- normalizePath(tempfile("lowp4a_"), winslash = "/", mustWork = FALSE); dir.create(tmp)
  helper <- file.path(tmp, "regen.R"); outf <- file.path(tmp, "regen.rds")
  writeLines(c(sprintf('source("%s")', file.path(.ver_dir, "lowp_generate.R")),
               'cells <- expand.grid(p = c(20L, 30L), cell = 1:3)',
               'cs <- list(c(1L, 1L), c(4L, 50L), c(6L, 100L))',
               'res <- list()',
               'for (i in seq_len(nrow(cells))) { sr <- cs[[cells$cell[i]]]; d <- generate_dataset(cells$p[i], sr[1], sr[2], "prod"); res[[d$inputs$dataset_id]] <- d }',
               sprintf('saveRDS(list(res = res, pid = Sys.getpid(), r = R.version.string), "%s")', outf)), helper)
  rs <- file.path(R.home("bin"), if (.Platform$OS.type == "windows") "Rscript.exe" else "Rscript")
  st <- suppressWarnings(system2(rs, c("--vanilla", shQuote(helper)), stdout = TRUE, stderr = TRUE))
  ok4 <- file.exists(outf); detail4 <- ""
  if (ok4) {
    reg <- readRDS(outf); ids <- names(reg$res); ok_all <- TRUE; hash_ok <- TRUE; cs <- LOWP_SCALES
    for (id in ids) {
      d <- reg$res[[id]]; p <- d$inputs$p
      inp <- readRDS(file.path(root, "inputs", sprintf("p%04d", p), paste0(id, ".rds"))); tr <- readRDS(file.path(root, "truth", sprintf("p%04d", p), paste0(id, ".rds")))
      ok_all <- ok_all && identical(d$inputs, inp) && identical(d$truth, tr)
      mrow <- mf$prod$inp[mf$prod$inp$dataset_id == id, ]; trow <- mf$prod$tr[mf$prod$tr$dataset_id == id, ]
      hash_ok <- hash_ok && identical(f64_sha256(d$inputs$X), mrow$x_sha256) && identical(f64_sha256(d$truth$eps), trow$eps_sha256) &&
        identical(f64_sha256(d$truth$signal), trow$signal_sha256) && identical(f64_sha256(d$inputs$foldid), mrow$fold_sha256) &&
        all(vapply(names(cs), function(k) identical(f64_sha256(d$inputs$Y[, k]), mrow[[paste0("y_", k, "_sha256")]]), TRUE))
    }
    ok4 <- ok_all && hash_ok && length(ids) == 6L && reg$pid != Sys.getpid()
    detail4 <- sprintf("%d datasets (%s) regenerated in fresh process pid %d (%s, parent pid %d): identical() inputs+truth = %s; float64 hashes of X, 5 Y columns, signal, eps, foldid = %s",
                       length(ids), paste(ids, collapse = ", "), reg$pid, reg$r, Sys.getpid(), ok_all, hash_ok)
  } else detail4 <- paste("fresh process failed:", paste(utils::tail(st, 3), collapse = " | "))
  unlink(tmp, recursive = TRUE)
  add("4a", "Bit-identical regeneration of S1 r1, S4 r50, S6 r100 per p in a fresh Rscript process (identical() and float64 hash)", ok4, detail4)

  # ---- Check 5: manifest closure ------------------------------------------------------------------------
  allseeds <- c(seeds$data, seeds$fold, seeds$method)
  seed_ok <- n_ds > 0L && !anyDuplicated(seeds$data) && !anyDuplicated(seeds$fold) && !anyDuplicated(seeds$method) && !anyDuplicated(allseeds)
  closure <- length(man_problems) == 0L && length(seed_problems) == 0L && length(fileset_problems) == 0L && nf("hash") == 0L && seed_ok && n_ds == 1260L
  add(5, "Manifest closure: exact keyed grids ({20,30} x S1-S6 x r1..100 prod, r1..5 dev), I1 columns, canonical relative paths, full file sets on disk, 1,200 + 60 rows, hashes recompute, seeds unique and equal base + 10000*s + r",
      closure, sprintf("prod rows %d (truth %d), dev rows %d (truth %d); manifest-structure problems %d%s; seed-field problems %d; file-set problems %d%s; hash failures %d; data/fold/method seeds unique across all %d datasets: %s",
        nrow(mf$prod$inp), nrow(mf$prod$tr), nrow(mf$dev$inp), nrow(mf$dev$tr), length(man_problems), if (length(man_problems)) paste0(" (", man_problems[1L], ")") else "",
        length(seed_problems), length(fileset_problems), if (length(fileset_problems)) paste0(" (", fileset_problems[1L], ")") else "", nf("hash"), n_ds, seed_ok))
  add("5b", "Sealed files are read-only (Windows read-only attribute / Linux chmod a-w); on NOTS truth/ is additionally mode 000 during fitting (lowp_truth_lock, Linux only; tests/test_truth_lock_linux.sh)",
      readonly_ok, if (readonly_ok) "file.access(mode = 2) denies write for every inputs/ and truth/ file" else "some file is writable")

  # ---- Check 6: Sigma sanity, per population block ------------------------------------------------------
  ok6 <- length(blk) == 1200L; rows6 <- character(); maxdev_all <- 0
  for (p in LOWP_PS) for (s in 1:6) {
    sel <- Filter(function(z) z$p == p && z$s == s, blk)
    if (length(sel) != 100L) { ok6 <- FALSE; rows6 <- c(rows6, sprintf("p%d S%d: %d replicates found", p, s, length(sel))); next }
    ev <- lowp_sigma_eval(do.call(rbind, lapply(sel, `[[`, "within")), vapply(sel, `[[`, 0, "between"), s, p)
    if (ev$gated) maxdev_all <- max(maxdev_all, ev$max_block_dev, ev$between_dev, na.rm = TRUE)
    ok6 <- ok6 && ev$pass; rows6 <- c(rows6, ev$text)
  }
  add(6, "Sigma sanity (descriptive): per scenario and per population block, within-block mean sample correlation over 100 replicates within +-0.02 of the block's population value (S2 descriptive; S5 between-block too)",
      ok6, sprintf("largest gated block deviation %.4f. %s", maxdev_all, paste(rows6, collapse = " || ")))

  # ---- Check 7: lowp vs literal master II.9 transcription, with literal master II.4 covariance -------------
  cov_lit_same <- TRUE
  for (pp in c(20L, 30L, 500L, 1000L)) for (ss in 1:6) cov_lit_same <- cov_lit_same && identical(master_cov_literal(ss, pp), scenario_covariance(ss, pp))
  detail7 <- sprintf("literal master II.4 covariance (entry-by-entry transcription inside the verifier) identical() to the lowp scenario_covariance() for S1-S6 x p in {20,30,500,1000}: %s", cov_lit_same)
  src_note <- "original benchmark helper source NOT supplied (--bench-gen): comparison with the original scenario_covariance() is INCOMPLETE"; orig_same <- NA; orig_sha <- NA
  if (!is.null(bench_gen) && nzchar(bench_gen) && file.exists(bench_gen)) {
    ge <- new.env(); ok_src <- tryCatch({ sys.source(bench_gen, envir = ge); is.function(ge$scenario_covariance) }, error = function(e) FALSE)
    if (ok_src) { orig_same <- TRUE
      for (pp in c(20L, 30L, 500L, 1000L)) for (ss in 1:6) orig_same <- orig_same && identical(ge$scenario_covariance(ss, pp), scenario_covariance(ss, pp))
      orig_sha <- digest::digest(file = bench_gen, algo = "sha256")
      src_note <- sprintf("original benchmark helper `%s` (SHA-256 %s): scenario_covariance() identical() to the lowp copy for S1-S6 x p in {20,30,500,1000}: %s", bench_gen, orig_sha, orig_same)
    } else src_note <- sprintf("original benchmark helper `%s` could not be sourced: comparison INCOMPLETE", bench_gen)
  } else if (!is.null(bench_gen) && nzchar(bench_gen)) src_note <- sprintf("original benchmark helper `%s` not found: comparison INCOMPLETE", bench_gen)
  rows7 <- character(); ok7 <- cov_lit_same
  for (kind in c("prod", "dev")) for (s in 1:6) for (r in c(1L, 100L)) {
    mm <- master_generate_dataset_9(30L, s, r, kind, scen_cov = master_cov_literal)
    ll <- generate_dataset(30L, s, r, kind)
    same <- identical(.strip(mm$X), ll$inputs$X) && identical(mm$eps, ll$truth$eps) && identical(mm$signal, ll$truth$signal) &&
      identical(unname(mm$Y), unname(ll$inputs$Y)) && identical(mm$foldid, ll$inputs$foldid) && identical(as.integer(mm$seed), ll$inputs$data_seed) &&
      identical(as.integer(mm$fold_seed), ll$inputs$fold_seed) && identical(mm$active, ll$truth$active) &&
      identical(f64_sha256(mm$X), f64_sha256(ll$inputs$X)) && identical(f64_sha256(mm$eps), f64_sha256(ll$truth$eps))
    if (kind == "prod" && s == 1L && r == 1L) {
      sealed <- readRDS(file.path(root, "inputs", "p0030", "p0030_S1_r001.rds")); stt <- readRDS(file.path(root, "truth", "p0030", "p0030_S1_r001.rds"))
      same <- same && identical(.strip(mm$X), sealed$X) && identical(mm$eps, stt$eps) && identical(f64_sha256(mm$X), mf$prod$inp$x_sha256[mf$prod$inp$dataset_id == "p0030_S1_r001"])
      rows7 <- c(rows7, sprintf("S1 r1 prod (master base 1,310,000): lowp = master transcription = sealed file: %s (X hash %s, eps hash %s)", same, substr(f64_sha256(mm$X), 1, 12), substr(f64_sha256(mm$eps), 1, 12)))
    } else rows7 <- c(rows7, sprintf("%s S%d r%d: %s", kind, s, r, same))
    ok7 <- ok7 && same
  }
  st7 <- if (!ok7 || isFALSE(orig_same)) "FAIL" else if (is.na(orig_same)) "INCOMPLETE" else "PASS"
  add(7, "p = 30 S1 r1 (and S1-S6 x r1,100 x prod,dev): lowp generator vs literal transcription of master II.9 (with the literal II.4 covariance) are bit-identical (X, eps, signal, Y, folds, seeds); original helper compared when supplied",
      st7, sprintf("%s; %s; 24 dataset pairs: %s", detail7, src_note, paste(rows7, collapse = "; ")))

  sd <- lowp_seed_collision_check()   # writes tests/seed_collisions.out
  add("L.3", "Seed collision check (80 role sets: data, fold, method, repeats m=1..5, prod and dev, p = 20, 30, 500, 1000, held-out families; all pairs)", sd$pass,
      sprintf("%d sets, %d pairs, %d collisions (output: tests/seed_collisions.out)", sd$n_sets, sd$n_pairs, length(sd$collisions)))

  # ---- report ---------------------------------------------------------------------------------------------
  stat <- vapply(checks, function(z) z$status, "")
  overall <- if (any(stat == "FAIL")) "FAIL" else if (any(stat == "INCOMPLETE")) "INCOMPLETE" else "PASS"
  bl <- paste0({b <- tryCatch(extSoftVersion()[["BLAS"]], error = function(e) ""); if (!nzchar(b)) "R built-in reference" else b}, " / LAPACK ", {l <- tryCatch(La_library(), error = function(e) ""); if (!nzchar(l)) "R built-in" else l})
  srcs <- file.path(.ver_dir, c("lowp_generate.R", "lowp_seal.R", "lowp_verify.R", "lowp_verify_nots.R"))
  L <- c("# LOWP verification report (gate G2, LOWP_SPEC L.6)", "",
         sprintf("Generated by `R/lowp_verify.R` on %s (UTC); study root `%s`; %s; platform %s; BLAS `%s`; elapsed %.0f s.",
                 format(Sys.time(), "%Y-%m-%d %H:%M", tz = "UTC"), root, R.version.string, R.version$platform, bl, proc.time()[["elapsed"]] - t0),
         "", sprintf("**Overall: %s** (%d PASS, %d FAIL, %d INCOMPLETE of %d checks). Check 4(b) (NOTS regeneration of all 1,200 + 60 hash sets and the six copies, `R/lowp_verify_nots.R`) is not part of this report.",
                     overall, sum(stat == "PASS"), sum(stat == "FAIL"), sum(stat == "INCOMPLETE"), length(stat)),
         "", "| Check | Result | Description |", "|---|---|---|")
  for (z in checks) L <- c(L, sprintf("| %s | %s | %s |", z$id, z$status, z$title))
  L <- c(L, "", "## Numbers", "")
  for (z in checks) L <- c(L, sprintf("- **Check %s (%s).** %s", z$id, z$status, z$detail))
  allbad <- unlist(bad)
  if (length(allbad)) L <- c(L, "", "## Failing items (first 20)", "", paste0("- ", utils::head(allbad, 20)))
  if (length(man_problems) || length(seed_problems) || length(fileset_problems)) L <- c(L, "", "## Manifest / file-set problems", "", paste0("- ", utils::head(c(man_problems, seed_problems, fileset_problems), 20)))
  L <- c(L, "", "## Verifier sources (SHA-256)", "", sprintf("- `%s`: %s", basename(srcs), vapply(srcs, function(f) digest::digest(file = f, algo = "sha256"), "")),
         if (!is.na(orig_sha)) sprintf("- original helper `%s`: %s", bench_gen, orig_sha))
  if (!is.null(report)) { dir.create(dirname(report), recursive = TRUE, showWarnings = FALSE); writeLines(L, report) }
  cat(paste(L, collapse = "\n"), "\n")
  invisible(list(status = overall, code = c(PASS = 0L, FAIL = 1L, INCOMPLETE = 3L)[[overall]], checks = checks))
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) >= 1L)
  root <- a[[1L]]; report <- file.path(.ver_dir, "..", "tests", "VERIFY_REPORT.md"); bg <- NULL; i <- 2L
  while (i <= length(a)) { if (a[i] == "--report") report <- a[i + 1L] else if (a[i] == "--bench-gen") bg <- a[i + 1L] else stop("bad argument ", a[i]); i <- i + 2L }
  res <- lowp_verify(root, report, bg)
  quit(status = res$code)
}
