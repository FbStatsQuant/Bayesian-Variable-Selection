# make_fixtures.R -- synthetic mini-study with KNOWN injected deviations, for tests/test_scoring.R.
# Study: p in {8, 10}, scenarios 1-2 (S1 independent, S2 within-block rho = .5), replicates 1-3, scales c100/c050, n = 100  -> 12 datasets, 24 cases.
# Layout = INTERFACES I1-I4:  inputs/ truth/ results/{exact,smc,bench}/p{pppp}/...   plus  INJECTIONS.rds (the ground truth of the injections).
# Exact posterior = brute force over all 2^p models with the core scorer (v3_score).  Mock SMC records follow the study-adapter envelope (SCHEMA.md)
# with a minimal `fit`.  Mock benchmark rows follow I4.  Nothing here runs an SMC.

make_fixtures <- function(root, seed = 20261028L) {
  sc_load_core()
  n <- 100L; ps <- c(8L, 10L); S0s <- list(`8` = c(2L, 6L), `10` = c(3L, 7L)); scales <- c("c100", "c050"); cvals <- c(1, 0.75, 0.5, 0.35, 0.25)
  for (d in c("inputs", "truth", "results/exact", "results/smc", "results/bench")) dir.create(file.path(root, d), recursive = TRUE, showWarnings = FALSE)
  popc <- function(m) { r <- 0L; while (m > 0) { r <- r + (m %% 2); m <- m %/% 2 }; r }
  datasets <- list()
  for (p in ps) for (s in 1:2) for (r in 1:3) {
    ds <- sprintf("p%04d_S%d_r%03d", p, s, r); S0 <- S0s[[as.character(p)]]
    set.seed(seed + 1000L * p + 100L * s + r)
    Sig <- diag(p); if (s == 2L) for (b in seq(1, p, by = 5)) { ix <- b:min(b + 4L, p); Sig[ix, ix] <- 0.5; diag(Sig) <- 1 }
    X <- matrix(as.numeric(scale(matrix(rnorm(n * p), n) %*% chol(Sig))), n, p)
    beta <- c(1.4, -1.0); signal <- as.numeric(X[, S0] %*% beta); eps <- rnorm(n)
    Y <- sapply(cvals, function(cc) cc * signal + eps); colnames(Y) <- c("c100", "c075", "c050", "c035", "c025")
    dir.create(file.path(root, "inputs", sprintf("p%04d", p)), showWarnings = FALSE); dir.create(file.path(root, "truth", sprintf("p%04d", p)), showWarnings = FALSE)
    saveRDS(list(X = X, Y = Y, foldid = rep(1:10, length.out = n), dataset_id = ds, p = p, scenario = s, replicate = r,
                 data_seed = seed + 1000L * p + 100L * s + r, fold_seed = 0L, method_seed = seed + 1000L * p + 100L * s + r + 4000000L),
            file.path(root, "inputs", sprintf("p%04d", p), paste0(ds, ".rds")))
    saveRDS(list(active = S0, beta = beta, signal = signal, eps = eps, scenario = s), file.path(root, "truth", sprintf("p%04d", p), paste0(ds, ".rds")))
    datasets[[ds]] <- list(ds = ds, p = p, s = s, r = r, S0 = S0, X = X, Y = Y)
  }
  dir.create(file.path(root, "manifests"), showWarnings = FALSE)
  utils::write.csv(data.frame(dataset_id = names(datasets), p = vapply(datasets, function(D) D$p, 0L), scenario = vapply(datasets, function(D) D$s, 0L), replicate = vapply(datasets, function(D) D$r, 0L)),
                   file.path(root, "manifests", "inputs_manifest_lowp.csv"), row.names = FALSE)
  MAN_SHA <- file_sha256(file.path(root, "manifests", "inputs_manifest_lowp.csv"))
  KIND <- "heuristic (not a validated interval bound)"; FAKE_SHA <- strrep("ab", 32)
  # ---- exact posterior by brute force -------------------------------------------------------------------------------------------------------
  exact <- list(); Fall <- list()
  for (D in datasets) {
    sk_list <- list()
    for (sk in scales) {
      sco <- make_scorer(D$X, as.numeric(D$Y[, sk])); p <- D$p
      Fv <- vapply(0:(2^p - 1), function(m) sco$F(which(bitwAnd(m, 2^(0:(p - 1))) > 0)), 0)
      lz <- lse(Fv)
      pip <- vapply(1:p, function(j) exp(lse(Fv[bitwAnd(0:(2^p - 1), 2^(j - 1)) > 0]) - lz), 0)
      lexkey <- vapply(0:(2^p - 1), function(m) paste(sprintf("%02d", which(bitwAnd(m, 2^(0:(p - 1))) > 0)), collapse = ""), "")
      o <- order(-Fv, vapply(0:(2^p - 1), popc, 0), lexkey)   # master I.6: F desc; ties: smaller size, then lexicographic on sorted original indices
      masks <- (0:(2^p - 1))[o]
      txt <- vapply(masks, function(m) paste(which(bitwAnd(m, 2^(0:(p - 1))) > 0), collapse = ";"), "")
      top <- data.frame(rank = seq_along(o), F = Fv[o], size = vapply(masks, popc, 0), model = txt, mask = as.numeric(masks), stringsAsFactors = FALSE)
      sz <- vapply(0:(2^p - 1), popc, 0)
      sk_list[[sk]] <- list(status = "exact", scope = "full", log_Z = lz, log_m0 = sco$ctx$log_m0, log_Z_rel_m0 = lz - sco$ctx$log_m0, pip = setNames(pip, as.character(1:p)), hpm = parse_support(txt[1L]), hpm_F = Fv[o[1L]], hpm_size = top$size[1L],
        hpm_eta = 1e-12, hpm_eta_kind = KIND, second_F = Fv[o[2L]], margin = Fv[o[1L]] - Fv[o[2L]], certificate_bound = Fv[o[1L]] - Fv[o[2L]] - 2e-12, certificate_bound_kind = KIND,
        global_certified = TRUE, certified_over_scored_models = TRUE, mpm = as.integer(which(pip > 0.5)),
        size_logmass = vapply(0:p, function(k) lse(Fv[sz == k]) - lz, 0), size_logjoint = vapply(0:p, function(k) lse(Fv[sz == k]), 0),
        top = top[seq_len(min(1000L, nrow(top))), , drop = FALSE],     # contract: min(1000, models_expected) rows; the full table is kept in FX$Fall
        numerics = list(n_rescale = 0, n_fallback_v3 = 0, max_abs_dF_recheck = 0, recheck_count = 0, q_recomputed = 0, recheck_mismatch_F = 0, recheck_mismatch_eta = 0))
      Fall[[paste0(D$ds, "_", sk)]] <- Fv
    }
    ex <- list(schema = "lowp_exact_v1", dataset_id = D$ds, p = D$p, n = n, K = D$p, source_sha256 = FAKE_SHA, v3_score_sha256 = FAKE_SHA, runtime_s = 1, host = "fixture",
               started_utc = "2026-10-28T00:00:00Z", finished_utc = "2026-10-28T00:00:01Z", models_scored = 2^D$p, models_expected = 2^D$p, complete = TRUE, threads = 1, scales = sk_list,
               extra = list(input_mode = "sealed", manifest_checked = TRUE, manifest_sha256 = MAN_SHA, input_file_sha256 = file_sha256(file.path(root, "inputs", sprintf("p%04d", D$p), paste0(D$ds, ".rds"))),
                            status = "exact", complete = TRUE, retained_columns = 1:D$p, models_expected = 2^D$p))
    dd <- file.path(root, "results/exact", sprintf("p%04d", D$p), D$ds); dir.create(dd, recursive = TRUE, showWarnings = FALSE)
    saveRDS(ex, file.path(dd, "EXACT.rds")); h <- file_sha256(file.path(dd, "EXACT.rds")); writeLines(paste0(h, "  EXACT.rds"), file.path(dd, "EXACT.sha256")); writeLines(h, file.path(dd, "EXACT.done"))
    exact[[D$ds]] <- ex
  }
  # ---- injections ------------------------------------------------------------------------------------------------------------------------------
  cases <- do.call(rbind, lapply(datasets, function(D) data.frame(case_id = paste0(D$ds, "_", scales), dataset_id = D$ds, scale_key = scales, p = D$p, scenario = D$s, replicate = D$r, stringsAsFactors = FALSE)))
  rownames(cases) <- NULL
  special <- list(
    A = "p0008_S1_r001_c100", B = "p0010_S1_r002_c050", C = "p0008_S2_r001_c050", D = "p0010_S2_r003_c100", E = "p0008_S1_r002_c100", Fc = "p0010_S1_r001_c100")
  injs <- list()
  set.seed(seed)
  for (i in seq_len(nrow(cases))) {
    cs <- cases[i, ]; ex <- exact[[cs$dataset_id]]$scales[[cs$scale_key]]; p <- cs$p
    interior <- function(delta, pipv) -sign(pipv - 0.5 + 1e-12) * abs(delta)     # move toward 1/2: stays in [0, 1]
    inj <- list(case_id = cs$case_id, idx = i, rep = 0L, off = 0.02 + rnorm(4, 0, 0.05),
                delta_rb = interior(rnorm(p, 0, 0.01), ex$pip), delta_plain = interior(rnorm(p, 0, 0.02), ex$pip),
                hpm_mode = "exact", hpm_F_shift = 0, status = "completed", cov = 0.999, truth_scored = (i %% 5L != 0L), blocks_alt = FALSE,
                runtime_s = 10 + i, score_fresh = 1000 + i, score_logical = 5000 + i, min_ess = 1000 - 20 * i,
                flags = list(escalated = i %% 4L == 0L, E1 = i %% 6L == 0L, E2 = i %% 5L == 0L, E3 = i %% 9L == 0L, low_ess = (i %% 3L == 0L && i %% 2L == 1L),
                             cut_group = i %% 2L == 0L, local_limit = i %% 11L == 0L, grid_unconverged = i %% 13L == 0L))
    inj$flags$checks_passed_final <- !(inj$flags$E1 || inj$flags$E2 || inj$flags$E3 || inj$flags$low_ess)
    if (cs$case_id == special$A) {
      inj$off <- c(0, 0.2, 0.4, 0.6); inj$delta_rb <- rep(0, p); inj$delta_rb[1:2] <- interior(c(0.05, 0.05), ex$pip[1:2])
      inj$delta_plain <- rep(0, p); inj$delta_plain[1] <- interior(0.10, ex$pip[1])
    }
    if (cs$case_id == special$B) { inj$off <- 4 + c(-0.1, 0, 0.1, 0); inj$hpm_mode <- "second" }
    if (cs$case_id == special$C) { inj$off <- c(-0.05, 0.05, -0.05, 0.05); inj$hpm_mode <- "below_truth" }
    if (cs$case_id == special$D) { inj$status <- "resource_limit"; inj$hpm_mode <- "second" }
    if (cs$case_id == special$E) { inj$blocks_alt <- TRUE; inj$hpm_F_shift <- 0.001 }
    if (cs$case_id == special$Fc) { inj$cov <- 0.5; inj$truth_scored <- FALSE }
    injs[[cs$case_id]] <- inj
  }
  # repeat seeds for A, B, C (reps 1, 2): different offsets; rep 2 has a wrong HPM
  reps <- list()
  for (nm in c("A", "B", "C")) {
    cid <- special[[nm]]; base <- injs[[cid]]
    for (m in 1:2) {
      rj <- base; rj$rep <- m; rj$off <- base$off + c(0.05, -0.05, 0.1, -0.1) * m; rj$hpm_mode <- if (m == 2L) (if (base$hpm_mode == "exact") "second" else "exact") else base$hpm_mode
      rj$delta_rb <- base$delta_rb * (1 + 0.5 * m); reps[[paste0(cid, "#", m)]] <- rj
    }
  }
  # ---- mock SMC records --------------------------------------------------------------------------------------------------------------------------
  hpm_choice <- function(inj, ex, S0, Fvec, p) {
    top <- ex$top
    mode <- inj$hpm_mode; F_truth <- Fvec[sum(2^(S0 - 1)) + 1]
    row <- switch(mode, exact = 1L, second = 2L, below_truth = which(top$F < F_truth - 1e-9)[1L], 1L)
    list(model = parse_support(top$model[row]), F = top$F[row])
  }
  write_record <- function(inj) {
    cs <- cases[cases$case_id == inj$case_id, ]; D <- datasets[[cs$dataset_id]]; p <- cs$p; ex <- exact[[cs$dataset_id]]$scales[[cs$scale_key]]
    Fvec <- Fall[[inj$case_id]]; S0 <- D$S0
    hc <- hpm_choice(inj, ex, S0, Fvec, p)
    failed <- inj$status != "completed"
    lzr <- ex$log_Z + inj$off; lz <- lse(lzr) - log(4)
    pip <- ex$pip + inj$delta_rb; pipp <- ex$pip + inj$delta_plain
    pip_r <- sapply(1:4, function(r) pmin(1, pmax(0, pip + (r - 2.5) * 0.002))); pipp_r <- sapply(1:4, function(r) pmin(1, pmax(0, pipp + (r - 2.5) * 0.004)))
    rownames(pip_r) <- rownames(pipp_r) <- as.character(1:p)
    sco <- make_scorer(D$X, as.numeric(D$Y[, cs$scale_key]))
    blocks <- v3_setup(sco$ctx)$blocks
    blocks <- lapply(blocks, as.integer)
    if (inj$blocks_alt && length(blocks) >= 2L) { a <- blocks[[1L]][1L]; blocks[[1L]][1L] <- blocks[[2L]][1L]; blocks[[2L]][1L] <- a }
    ss <- data.frame(key = c(if (inj$truth_scored) sum(2^(S0 - 1)), sum(2^(hc$model - 1)), 1, 2), size = c(if (inj$truth_scored) length(S0), length(hc$model), 1L, 1L),
                     first_phase = "pilot", first_mech = "gibbs_flip", first_tier = 0L, first_iter = 0L, first_island = 1L, first_stage = 3L, stringsAsFactors = FALSE)
    ss <- ss[!duplicated(ss$key), ]; ss <- ss[order(ss$key), ]
    f <- inj$flags
    stage_table <- data.frame(phase = c("diag", rep("final_bridge", 8)), tier = 0L, iter = -1L, island = c(1L, rep(1:4, each = 2)), stage = c(1L, rep(1:2, 4)),
                              ess = c(1, inj$min_ess, rep(2000, 7)), stringsAsFactors = FALSE)
    supp <- function(v) paste(v, collapse = ";")
    mk_support <- function(v) if (failed) NA_character_ else supp(v)
    mpm <- if (failed) NULL else which(pip > 0.5)
    fit <- list(status = inj$status, seed = 1L, n = n, p = p, estimates_available = !failed, preprocessing = list(status = "ok", kept = 1:p, dropped = integer(0)),
                hpm = hc$model, hpm_F = hc$F + inj$hpm_F_shift, local_certified = TRUE, global_certified = FALSE, blocks = blocks, B = 3L,
                flags = list(escalated = f$escalated, E1 = f$E1, E2 = f$E2, E3 = f$E3, low_empirical_ESS = f$low_ess, local_limit = f$local_limit,
                             near_tie_truncated = FALSE, checks_passed_final = f$checks_passed_final, grid_unconverged = f$grid_unconverged, cut_group = f$cut_group))
    if (!failed) fit <- c(fit, list(log_Z = lz, log_Z_r = lzr, log_Z_lower95 = log(0.05) + lz, log_Z_rel_m0 = lz - ex$log_m0, log_m0 = ex$log_m0,
      pip_primary = setNames(pip, 1:p), pip_r = pip_r, mpm = as.integer(mpm), pip_plain = setNames(pipp, 1:p), pip_plain_r = pipp_r,
      mpm_plain = as.integer(which(pipp > 0.5)), stage_table = stage_table, settings = list(tier = as.integer(f$escalated)),
      score_counts = list(fresh = matrix(c(inj$score_fresh - 100, 100, 0, 0), 2, 2), logical = matrix(c(inj$score_logical, 0, 0, 0), 2, 2)),
      instrumentation = list(stages = list(final = 2L), scored = list(mode = "exact", n_distinct = 200, log_sum_exp_F = ex$log_Z + log(inj$cov)), scored_set = ss)))
    rows <- data.frame(case_id = inj$case_id, dataset_id = cs$dataset_id, method_id = "SMCBVS", rule_id = c("hpm", "pip05"), role = c("primary", "S0"),
                       status = if (failed) "failed" else "ok", support = c(mk_support(hc$model), if (failed) NA_character_ else supp(mpm)),
                       runtime_s = inj$runtime_s, diag_flag = !f$checks_passed_final, p = p, stringsAsFactors = FALSE)
    rec <- list(schema_version = 2L, adapter_version = "2.2-R1", rows = rows, fit = fit,
                pip = if (failed) setNames(rep(NA_real_, p), 1:p) else setNames(pip, 1:p), native_status = inj$status, estimates_available = !failed,
                runtime_s = inj$runtime_s, case = list(dataset_id = cs$dataset_id, case_id = inj$case_id, p = p, scenario = cs$scenario, replicate = cs$replicate,
                                                       scale_key = cs$scale_key, scale = scale_value(cs$scale_key), method_seed = 5L + inj$rep * 1000L),
                pip_plain = if (failed) setNames(rep(NA_real_, p), 1:p) else setNames(pipp, 1:p), mpm_plain = if (failed) NULL else as.integer(which(pipp > 0.5)),
                instrumentation = fit$instrumentation)
    dd <- file.path(root, "results/smc", sprintf("p%04d", p), inj$case_id); dir.create(dd, recursive = TRUE, showWarnings = FALSE)
    b <- if (inj$rep == 0L) "SMCBVS" else paste0("SMCBVS_rep", inj$rep)
    saveRDS(rec, file.path(dd, paste0(b, ".rds"))); writeLines("done", file.path(dd, paste0(b, ".done")))
    invisible(list(hpm = hc$model, F = hc$F, mpm = mpm))
  }
  for (inj in c(injs, reps)) write_record(inj)
  # ---- mock benchmark rows (I4) -----------------------------------------------------------------------------------------------------------------
  kinds_lasso <- c("exact", "extra", "missed", "mixed", "failed", "exact"); kinds_susie <- c("exact", "exact", "missed", "timeout", "not_run", "extra")
  bspec <- list()
  for (i in seq_len(nrow(cases))) {
    cs <- cases[i, ]; D <- datasets[[cs$dataset_id]]; S0 <- D$S0; nulls <- setdiff(seq_len(cs$p), S0)
    mk <- function(kind) switch(kind, exact = S0, extra = sort(c(S0, nulls[1L])), missed = S0[-1L], mixed = sort(c(S0[-1L], nulls[1L])), NULL)
    for (spec in list(list("LASSO", kinds_lasso[(i %% 6L) + 1L], c("cvmin", "ebic1"), c("primary", "S0")), list("SUSIE", kinds_susie[(i %% 6L) + 1L], "L10", "primary"))) {
      method <- spec[[1L]]; kind <- spec[[2L]]
      bspec[[length(bspec) + 1L]] <- data.frame(case_id = cs$case_id, method_id = method, kind = kind, stringsAsFactors = FALSE)
      if (kind == "not_run") next
      st <- if (kind %in% c("failed", "timeout")) kind else "ok"
      sup <- mk(kind)
      rows <- data.frame(case_id = cs$case_id, dataset_id = cs$dataset_id, method_id = method, rule_id = spec[[3L]], role = spec[[4L]], status = st,
                         support = if (is.null(sup)) NA_character_ else paste(sup, collapse = ";"), runtime_s = 1 + i / 10, diag_flag = FALSE,
                         adaptation_ids = if (method == "LASSO") "AD1" else NA_character_, stringsAsFactors = FALSE)
      # the ebic1 companion rule of LASSO always recovers the truth (when the fit did not fail)
      if (method == "LASSO" && st == "ok") rows$support[rows$rule_id == "ebic1"] <- paste(S0, collapse = ";")
      dd <- file.path(root, "results/bench", sprintf("p%04d", cs$p), cs$case_id); dir.create(dd, recursive = TRUE, showWarnings = FALSE)
      saveRDS(rows, file.path(dd, paste0(method, ".rds"))); writeLines("done", file.path(dd, paste0(method, ".done")))
    }
  }
  writeLines(c("method_id,rule_id,role,required,in_h4", "SMCBVS,hpm,primary,TRUE,TRUE", "SMCBVS,pip05,S0,TRUE,TRUE", "EXACT,hpm,reference,TRUE,TRUE", "EXACT,mpm,reference,TRUE,TRUE",
               "LASSO,cvmin,primary,TRUE,TRUE", "LASSO,ebic1,S0,TRUE,FALSE", "SUSIE,L10,primary,TRUE,TRUE"), file.path(root, "registry_fixture.csv"))
  out <- list(Fall = Fall, cases = cases, special = special, injs = injs, reps = reps, datasets = lapply(datasets, function(D) D[c("ds", "p", "s", "r", "S0")]),
              bench = do.call(rbind, bspec), n = n)
  saveRDS(out, file.path(root, "INJECTIONS.rds"))
  invisible(out)
}
