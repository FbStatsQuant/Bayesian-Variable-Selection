# check_dev.R -- validate the A1 dev-test outputs against §IV.1.1-§IV.1.2 and §III.3.0
# (files, hashes, schema, registry rule ids/roles, status/flag/converged semantics, input
# hashes against the dev manifest, source hash against the snapshot, independent recomputation of
# the three rules, gates and flags from the saved objects) and tabulate A1 diagnostics. Reads no truth.
# Usage: Rscript --vanilla check_dev.R --code=<snapshot_code_dir> --results=<results_run_dir> --out=<out_dir>
#          [--datasets=dev|canary|prod_all|id1,id2,...] [--manifests=<run_dir>/manifests] [--canary_ref=<dev results run dir>]
#          [--scale=c100|c050]  (c050 copy: scale key of the production datasets; dev and canary datasets are always c100)
#          [--methods=id1,id2]  (refine tree: method ids of the run checked; default all registered ids)
#          [--env_baseline=<run_dir>/env_fingerprint.rds]

# Checks of one saved fit that need the RDS: full CSV/RDS row agreement, provenance, and, for a
# non-failed fit, structure, contract, independent rule recomputation, gates and flags.
# Returns a character vector of problems (empty when the fit passes).
fit_checks <- function(x, r, cfg, variant, p, src_sha, R) {
  out <- character(); A <- cfg$A1
  add <- function(...) out <<- c(out, paste0(...))
  if (!all(x$source_sha256 == src_sha)) add("source_sha256 != code tree checked")
  if (!identical(r$provenance$source_sha256, src_sha)) add("RDS provenance source_sha256 != code tree checked")
  # Every schema column: serialise the RDS rows exactly as the runner does and compare as text.
  tf <- tempfile(fileext = ".csv")
  utils::write.csv(r$rows, tf, row.names = FALSE, na = "NA")
  rr <- utils::read.csv(tf, colClasses = "character"); unlink(tf)
  if (!identical(rr, x)) add("CSV rows differ from RDS rows")
  if (any(x$status == "failed")) return(out)
  dg <- r$fit$diagnostics; pip <- r$fit$pip; beta <- r$fit$beta
  # Structure and contract (items c, g).
  if (length(pip) != p || length(beta) != p || length(dg$pip) != p || length(dg$beta) != p)
    return(c(out, "saved PIP/beta vectors missing or of wrong length"))
  if (!identical(pip, dg$pip) || !identical(beta, dg$beta)) add("top-level and diagnostics PIP/beta differ")
  if (!length(dg$elbo) || !identical(as.integer(length(dg$elbo)), as.integer(dg$niter)))
    add("ELBO trace empty or length != niter")
  if (!identical(as.numeric(dg$intercept), 0)) add("saved intercept is not 0")
  if (!isTRUE(dg$x_scale_all_one)) add("column scale factors not all 1")
  if (length(dg$V) != dg$L || length(dg$lbf) != dg$L) add("V/lbf length != L")
  if (!identical(as.integer(dg$n_active), sum(dg$V > A$CS_V_THRESHOLD))) add("n_active does not recompute")
  if (!identical(as.integer(dg$n_cs), length(dg$sets$cs))) add("n_cs does not recompute")
  # Independent recomputation of the rules (own code, not the wrapper's helpers).
  rec <- list(pip05 = which(pip > cfg$PIP_THRESHOLD),
              cslead = sort(unique(vapply(dg$sets$cs, function(s) { s <- sort(s); s[which.max(pip[s])] }, 0L))),
              bfdr10 = {
                o <- order(-pip, seq_along(pip))
                m <- cumsum(1 - pip[o]) / seq_along(o)
                v <- which(m <= A$BFDR_Q + A$BFDR_EPS_MULT * .Machine$double.eps)
                if (length(v)) sort(o[seq_len(max(v))]) else integer() })
  for (j in seq_len(nrow(x)))
    if (!identical(x$support[j], paste(rec[[x$rule_id[j]]], collapse = ";")))
      add(x$rule_id[j], " does not recompute from saved objects")
  # Gates (h) on a non-failed fit.
  de <- diff(dg$elbo)
  if (x$converged[1] != "TRUE" || !isTRUE(dg$converged)) add("non-failed fit not converged")
  if (!length(dg$elbo) || any(!is.finite(dg$elbo)) || any(de < -A$TOL)) add("gate 3 condition on a non-failed fit")
  if (any(!is.finite(pip)) || any(pip < 0 | pip > 1) || any(!is.finite(dg$V)) || any(dg$V < 0) ||
      length(dg$sigma2) != 1L || !is.finite(dg$sigma2) || any(!is.finite(beta)))
    add("gate 4 condition on a non-failed fit")
  # Flags recomputed from the saved summaries.
  fl <- c(if (sum(dg$V > 1e-9) == dg$L) "L_saturated",
          if (any(de >= -A$TOL & de < -A$ELBO_DROP_TOL)) "elbo_drop",
          if (isTRUE(dg$sigma2 <= dg$resid_lb)) "sigma2_floor")
  if (!identical(x$diag_codes[1], paste(fl, collapse = ";"))) add("flags do not recompute")
  Lexp <- if (variant == "L100") A$L_S1 else A$L
  if (!identical(as.integer(dg$L), as.integer(Lexp))) add("L differs from registry variant")
  out
}

# Negative fixtures for the validator: corrupt a real, passing output in memory and require
# fit_checks to report each corruption. Returns TRUE when every corruption is caught.
selftest <- function(x, r, cfg, variant, p, src_sha, R) {
  stopifnot(!length(fit_checks(x, r, cfg, variant, p, src_sha, R)))
  mut <- list(
    empty_elbo = function(x, r) { r$fit$diagnostics$elbo <- numeric(0); list(x, r) },
    intercept = function(x, r) { r$fit$diagnostics$intercept <- 0.1; list(x, r) },
    short_beta = function(x, r) { r$fit$beta <- r$fit$beta[-1]; list(x, r) },
    x_scale = function(x, r) { r$fit$diagnostics$x_scale_all_one <- FALSE; list(x, r) },
    csv_audit = function(x, r) { x$support_audit[1] <- "1;2"; list(x, r) },
    csv_runtime = function(x, r) { x$runtime_s[1] <- "999"; list(x, r) },
    not_converged = function(x, r) { r$fit$diagnostics$converged <- FALSE; list(x, r) },
    elbo_drop = function(x, r) { e <- r$fit$diagnostics$elbo; r$fit$diagnostics$elbo <- c(e, e[length(e)] - 1e-5)
                                 r$fit$diagnostics$niter <- length(e) + 1L; list(x, r) },
    pip_rule = function(x, r) { j <- which(r$fit$pip < 0.5)[1]; r$fit$pip[j] <- 0.99
                                r$fit$diagnostics$pip[j] <- 0.99; list(x, r) },
    source = function(x, r) { r$provenance$source_sha256 <- "0"; list(x, r) })
  caught <- vapply(names(mut), function(k) {
    m <- mut[[k]](x, r); length(fit_checks(m[[1]], m[[2]], cfg, variant, p, src_sha, R)) > 0L }, TRUE)
  for (k in names(caught)) cat(sprintf("selftest %-14s %s
", k, if (caught[[k]]) "caught" else "MISSED"))
  all(caught)
}

# `datasets`: "dev" (the 12 dev datasets), "canary" (the 3 production canaries, dev data),
# "prod_all" (the 1,200 production datasets, grid built here independently of the manifests) or a
# comma-separated list of production dataset ids. `manifests`: directory holding the input
# manifests to validate against (the run's frozen copy `runs/<run_id>/manifests/`); default: the
# live study manifests. `canary_ref`: results directory of the dev pilot run to which the canary
# outputs must be identical (rule rows and saved PIP/beta).
main <- function(code_dir, run_dir, out_dir, datasets = "dev", manifests = NULL, canary_ref = NULL,
                 env_baseline = NULL, scale = "c100", methods = NULL) {
  if (identical(datasets, "canary") && is.null(canary_ref)) stop("--datasets=canary requires --canary_ref")
  env_base <- if (is.null(env_baseline)) NULL else readRDS(env_baseline)
  if (!is.null(manifests)) {
    # The run's frozen manifest copies must match the hash list written at freeze time.
    hl <- readLines(file.path(dirname(normalizePath(manifests)), "manifests_sha256.txt"))
    want <- sub("^([0-9a-f]{64})  (.*)$", "\\1", hl); names(want) <- sub("^([0-9a-f]{64})  (.*)$", "\\2", hl)
    got <- vapply(file.path(manifests, names(want)), function(f) digest::digest(file = f, algo = "sha256"), "")
    if (!identical(unname(got), unname(want))) stop("frozen manifest copies do not match manifests_sha256.txt")
  }
  cfg <- new.env(); sys.source(file.path(code_dir, "config.R"), envir = cfg)
  .libPaths(c(cfg$COMMON$LIB, .Library))
  R <- new.env(); sys.source(file.path(code_dir, "run_case.R"), envir = R)
  root <- cfg$COMMON$STUDY_ROOT
  dev_man <- if (is.null(manifests)) file.path(root, "dev/manifests/dev_inputs_manifest.csv") else
    file.path(manifests, "dev_inputs_manifest.csv")
  if (datasets %in% c("dev", "canary")) {
    man <- utils::read.csv(dev_man, colClasses = "character")
    ids <- if (datasets == "dev")
      as.vector(outer(1:6, c(500L, 1000L), function(s, p) sprintf("dev_p%04d_S%d_r001", p, s))) else
      c("dev_p0500_S4_r001", "dev_p1000_S2_r001", "dev_p1000_S6_r001")
  } else {
    mf <- list.files(if (is.null(manifests)) file.path(root, "manifests/cells") else manifests,
                     pattern = "^p[0-9]{4}_S[1-6]_inputs\\.csv$", full.names = TRUE)
    man <- do.call(rbind, lapply(mf, utils::read.csv, colClasses = "character"))
    grid <- as.vector(outer(sprintf("_S%d_r%03d", rep(1:6, each = 100), rep(1:100, 6)),
                            c("p0500", "p1000"), function(sr, pp) paste0(pp, sr)))
    if (length(grid) != 1200L || anyDuplicated(man$dataset_id) || !setequal(man$dataset_id, grid))
      stop("production manifests do not cover exactly the 1,200-dataset grid")
    ids <- if (identical(datasets, "prod_all")) grid else strsplit(datasets, ",")[[1]]
    if (!all(ids %in% grid)) stop("dataset ids not in the production grid")
  }
  M <- cfg$METHODS
  if (!is.null(methods)) {
    if (!all(methods %in% M$method_id)) stop("--methods: unregistered method id(s)")
    M <- M[M$method_id %in% methods, , drop = FALSE]
  }
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  problems <- character(); diag <- list(); allrows <- list()
  bad <- function(...) problems <<- c(problems, paste0(...))
  vocab <- c("L_saturated", "elbo_drop", "sigma2_floor")
  src_sha <- R$source_tree_sha256(code_dir)   # code_dir = the frozen snapshot of the run
  selftest_done <- FALSE
  for (did in ids) {
    sk <- if (startsWith(did, "dev_")) "c100" else scale
    p <- as.integer(sub("^(dev_)?p([0-9]{4})_.*$", "\\2", did)); cid <- paste0(did, "_", sk)
    od <- file.path(run_dir, sprintf("p%04d", p), cid)
    mrow <- man[man$dataset_id == did, ]
    for (i in seq_len(nrow(M))) {
      mid <- M$method_id[i]; stem <- file.path(od, mid)
      f <- paste0(stem, c(".rds", ".csv", ".sha256", ".done"))
      if (!all(file.exists(f))) { bad(cid, " ", mid, ": missing ", paste(basename(f[!file.exists(f)]), collapse = ",")); next }
      if (!R$done_is_valid(stem)) bad(cid, " ", mid, ": sha256 mismatch")
      x <- utils::read.csv(f[2], colClasses = "character")
      if (!identical(names(x), R$SCHEMA)) bad(cid, " ", mid, ": schema columns differ")
      if (!identical(x$rule_id, M$rule_ids[[i]]) || !identical(x$role, M$roles[[i]]))
        bad(cid, " ", mid, ": rule ids/roles differ from registry")
      if (!all(x$method_id == mid) || !all(x$case_id == cid) || !all(x$dataset_id == did))
        bad(cid, " ", mid, ": id columns")
      if (!all(x$x_sha256 == mrow$x_sha256) || !all(x$y_sha256 == mrow[[paste0("y_", sk, "_sha256")]]) ||
          !all(x$fold_sha256 == mrow$foldid_sha256) || !all(x$inputs_sha256 == mrow$file_sha256))
        bad(cid, " ", mid, ": input hashes differ from manifest")
      if (!all(as.numeric(x$method_seed) == as.numeric(x$data_seed) + cfg$METHOD_SEED_OFFSET) ||
          !all(x$method_seed == mrow$method_seed)) bad(cid, " ", mid, ": method seed")
      if (!all(x$status %in% c("ok", "warning", "failed"))) bad(cid, " ", mid, ": status vocabulary")
      for (col in c("runtime_s", "status", "converged", "diag_flag", "diag_codes"))
        if (length(unique(x[[col]])) != 1L) bad(cid, " ", mid, ": ", col, " not shared across rules")
      if (!all(x$converged %in% c("TRUE", "FALSE")) || !all(x$diag_flag %in% c("TRUE", "FALSE", NA)))
        bad(cid, " ", mid, ": converged/diag_flag not logical")
      codes <- unlist(strsplit(x$diag_codes[!is.na(x$diag_codes)], ";"))
      if (!all(codes %in% vocab)) bad(cid, " ", mid, ": diag_codes outside the A1 vocabulary")
      ok_rows <- x$status != "failed"
      if (any(ok_rows)) {
        if (!all(x$diag_flag[ok_rows] == ifelse(x$diag_codes[ok_rows] == "", "FALSE", "TRUE")))
          bad(cid, " ", mid, ": diag_flag inconsistent with diag_codes")
        if (!all(is.na(x$support_audit[ok_rows])) || !all(is.na(x$error[ok_rows]))) bad(cid, " ", mid, ": audit/error on non-failed row")
        k_chk <- vapply(x$support[ok_rows], function(z) if (z == "") 0L else length(strsplit(z, ";")[[1]]), 0L)
        if (!all(k_chk == as.integer(x$k[ok_rows]))) bad(cid, " ", mid, ": k != |support|")
        srt <- vapply(x$support[ok_rows], function(z) z == "" || identical(z, paste(sort(unique(as.integer(strsplit(z, ";")[[1]]))), collapse = ";")), TRUE)
        if (!all(srt)) bad(cid, " ", mid, ": support not sorted/unique")
        if (!all((x$status[ok_rows] == "warning") == (as.integer(x$n_warnings[ok_rows]) > 0)))
          bad(cid, " ", mid, ": status warning iff captured conditions")
      }
      if (any(!ok_rows)) {
        if (!all(is.na(x$support[!ok_rows])) || !all(is.na(x$k[!ok_rows])) || !all(x$converged[!ok_rows] == "FALSE"))
          bad(cid, " ", mid, ": failed-row semantics")
      }
      if (!all(is.na(x[, c("tp", "fp", "fn", "exact", "error_type")]))) bad(cid, " ", mid, ": truth columns filled at fit time")
      r <- readRDS(f[1])
      dg <- r$fit$diagnostics
      if (!is.null(env_base) && !identical(r$provenance$env_fingerprint, env_base))
        bad(cid, " ", mid, ": environment fingerprint differs from the run baseline")
      for (msg in fit_checks(x, r, cfg, M$variant[i], p, src_sha, R)) bad(cid, " ", mid, ": ", msg)
      if (!selftest_done && mid == "A1" && !any(x$status == "failed")) {
        if (!selftest(x, r, cfg, M$variant[i], p, src_sha, R)) bad("validator selftest missed a corruption")
        selftest_done <- TRUE
      }
      diag[[length(diag) + 1L]] <- data.frame(
        case_id = cid, method_id = mid, status = x$status[1], converged = x$converged[1],
        diag_flag = x$diag_flag[1], diag_codes = x$diag_codes[1],
        L = if (is.null(dg$L)) NA else dg$L, niter = if (is.null(dg$niter)) NA else dg$niter,
        n_active = if (is.null(dg$n_active)) NA else dg$n_active,
        n_cs = if (is.null(dg$n_cs)) NA else dg$n_cs,
        L_saturated = if (is.null(dg$L_saturated)) NA else dg$L_saturated,
        sigma2 = if (is.null(dg$sigma2)) NA else dg$sigma2,
        sigma2_lb = if (is.null(dg$resid_lb)) NA else dg$resid_lb,
        min_elbo_increment = if (length(dg$elbo) >= 2) min(diff(dg$elbo)) else NA,
        last_elbo_increment = if (is.null(dg$elbo_last_increment)) NA else dg$elbo_last_increment,
        pip_unreported_max = if (is.null(dg$pip_unreported_max)) NA else dg$pip_unreported_max,
        max_set_size = if (is.null(dg$alpha_saved)) NA else max(dg$alpha_saved$set_size),
        n_warn_msg = x$n_warnings[1], runtime_s = as.numeric(x$runtime_s[1]),
        vm_hwm_mb = r$vm_hwm_kb / 1024, host = x$host[1], stringsAsFactors = FALSE)
      allrows[[length(allrows) + 1L]] <- x
    }
  }
  # Canaries: identical to the dev pilot (rule rows' selection columns; saved PIP and beta).
  if (!is.null(canary_ref)) for (did in ids) for (mid in M$method_id) {
    cid <- paste0(did, "_c100"); pdir <- sprintf("p%s", substr(sub("^dev_p", "", did), 1, 4))
    a <- file.path(run_dir, pdir, cid, mid); b <- file.path(canary_ref, pdir, cid, mid)
    if (!file.exists(paste0(b, ".csv"))) { bad(cid, " ", mid, ": canary reference missing"); next }
    if (!file.exists(paste0(a, ".csv"))) next
    cols <- c("rule_id", "role", "status", "converged", "diag_flag", "diag_codes", "k", "support", "support_audit")
    xa <- utils::read.csv(paste0(a, ".csv"), colClasses = "character")[, cols]
    xb <- utils::read.csv(paste0(b, ".csv"), colClasses = "character")[, cols]
    ra <- readRDS(paste0(a, ".rds"))$fit; rb <- readRDS(paste0(b, ".rds"))$fit
    if (!identical(xa, xb) || !identical(ra$pip, rb$pip) || !identical(ra$beta, rb$beta))
      bad(cid, " ", mid, ": canary differs from the dev pilot output")
  }
  D <- do.call(rbind, diag)
  utils::write.csv(D, file.path(out_dir, "dev_diagnostics.csv"), row.names = FALSE)
  utils::write.csv(do.call(rbind, allrows), file.path(out_dir, "dev_rule_rows.csv"), row.names = FALSE)
  writeLines(if (length(problems)) problems else "no problems", file.path(out_dir, "check_problems.txt"))
  cat(sprintf("checked %d (case, method) outputs, %d rule rows; problems: %d\n",
              nrow(D), sum(vapply(allrows, nrow, 0L)), length(problems)))
  if (length(problems)) cat(problems, sep = "\n")
  print(D[, c("case_id", "method_id", "status", "converged", "diag_codes", "L", "niter", "n_active",
              "n_cs", "min_elbo_increment", "pip_unreported_max", "runtime_s", "vm_hwm_mb")], row.names = FALSE)
  invisible(length(problems) == 0L)
}

if (sys.nframe() == 0L) {
  argv <- commandArgs(trailingOnly = TRUE)
  kv <- regmatches(argv, regexec("^--([^=]+)=(.*)$", argv))
  if (any(lengths(kv) != 3L)) stop("arguments must be --key=value")
  a <- stats::setNames(vapply(kv, `[`, "", 3L), vapply(kv, `[`, "", 2L))
  for (k in c("code", "results", "out")) if (is.na(a[k])) stop("missing --", k)
  ok <- main(normalizePath(a[["code"]]), a[["results"]], a[["out"]],
             if (is.na(a["datasets"])) "dev" else a[["datasets"]],
             if (is.na(a["manifests"])) NULL else a[["manifests"]],
             if (is.na(a["canary_ref"])) NULL else a[["canary_ref"]],
             if (is.na(a["env_baseline"])) NULL else a[["env_baseline"]],
             if (is.na(a["scale"])) "c100" else a[["scale"]],
             if (is.na(a["methods"])) NULL else strsplit(a[["methods"]], ",")[[1]])
  quit(status = if (ok) 0L else 1L)
}
