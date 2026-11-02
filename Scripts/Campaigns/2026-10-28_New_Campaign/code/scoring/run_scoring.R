#!/usr/bin/env Rscript
# run_scoring.R -- single entry point of the New Campaign scoring pipeline (Regime L; also usable on p >> n selection rows).
# Usage:
#   Rscript run_scoring.R --study STUDY --results STUDY/results/RUN1[,STUDY/results/RUN2,...] --out STUDY/analysis/lowp
#        [--scales c100,c050] [--registry FILE (default: derived from bench_lowp at run time)] [--bench-dir DIR] [--theory 1] [--td-d 1,2|none] [--td-engine auto|slow|enum] [--td-max-scores N]
#        [--on-conflict error|first_root] [--expect-reps 100|none] [--partial 1] [--cases FILE (one case_id per line)] [--core DIR] [--enum-file FILE]
# ROSTER (review findings 1, 5): the expected cases are STUDY/manifests/inputs_manifest_lowp.csv x --scales (never the observed files), and the
# expected (method, rule) rows are the registry (derived from bench_lowp/R/config_lowp.R + lowp_derive at run time; see R/registry.R). Missing truth, a missing scenario/replicate in the manifest, an
# unknown case id are errors. --partial 1 (test / partial studies) allows the roster to come from a listing of STUDY/inputs when the manifest
# is absent and skips the 6-scenario x 100-replicate completeness check; it is printed in HEADLINE.md.
# STUDY holds inputs/, truth/ (read here only), manifests/. Result roots hold p{pppp}/{case_id|dataset_id}/... (INTERFACES I2-I4).
# Outputs (INTERFACES I5): case_smc_accuracy.csv, case_selection.csv, case_theory.csv, H1_logZ.csv, H2_hpm.csv, H3_pip.csv, H4_recovery.csv,
#   HEADLINE.md, plus case_stability.csv, case_reference.csv, flag_error_2x2.csv, se_calibration.csv, roster.csv, exact_diagnostics.csv,
#   duplicates.csv, SCORING_LOG.txt.
cli_args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k, default = NULL) { i <- match(paste0("--", k), cli_args); if (is.na(i) || i == length(cli_args)) default else cli_args[i + 1L] }
scoring_here <- if (nzchar(Sys.getenv("SCORING_DIR"))) Sys.getenv("SCORING_DIR") else
  local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]); if (is.na(f)) getwd() else dirname(normalizePath(f, winslash = "/")) })
Sys.setenv(SCORING_DIR = scoring_here)
if (!is.null(get_arg("core"))) Sys.setenv(SCORING_CORE_DIR = get_arg("core"))
source(file.path(scoring_here, "R", "load_all.R"))

# ---- roster ------------------------------------------------------------------------------------------------------------------------------
build_roster <- function(study, scales, partial = FALSE, expect_reps = 100L, expect_scenarios = 1:6, cases = NULL) {
  man <- file.path(study, "manifests", "inputs_manifest_lowp.csv")
  if (file.exists(man)) {
    m <- utils::read.csv(man, stringsAsFactors = FALSE)
    if (!"dataset_id" %in% names(m)) stop("inputs manifest has no dataset_id column")
    datasets <- sort(unique(m$dataset_id)); mode <- "inputs manifest"
  } else if (partial) {
    f <- list.files(file.path(study, "inputs"), pattern = "^p[0-9]{4}_S[0-9]_r[0-9]{3}\\.rds$", recursive = TRUE)
    datasets <- sort(sub("\\.rds$", "", basename(f))); mode <- "PARTIAL-STUDY MODE: listing of inputs/ (no manifest)"
  } else stop("inputs manifest not found: ", man, " (the roster must come from the manifest; use partial = TRUE only for tests)")
  if (!length(datasets)) stop("empty roster")
  bad <- datasets[!grepl("^p[0-9]{4}_S[0-9]_r[0-9]{3}$", datasets)]
  if (length(bad)) stop("manifest dataset ids with the wrong format: ", paste(bad, collapse = ", "))
  miss_truth <- datasets[!file.exists(file.path(study, "truth", sprintf("p%04d", as.integer(substr(datasets, 2, 5))), paste0(datasets, ".rds")))]
  if (length(miss_truth)) stop("scoring-completeness error: no truth file for rostered datasets: ", paste(head(miss_truth, 10), collapse = ", "), if (length(miss_truth) > 10) " ...")
  ex <- data.table::rbindlist(lapply(datasets, function(ds) data.table::rbindlist(lapply(scales, function(sk) {
    pc <- parse_case_id(paste0(ds, "_", sk)); data.table::data.table(case_id = pc$case_id, dataset_id = ds, p = pc$p, scenario = pc$scenario, replicate = pc$replicate, scale_key = sk) }))))
  if (!partial && !is.null(expect_reps)) {      # planned grid: every (p, scenario) has replicates 1..expect_reps
    for (pp in unique(ex$p)) for (sc in expect_scenarios) {
      got <- sort(unique(ex$replicate[ex$p == pp & ex$scenario == sc]))
      if (!identical(as.integer(got), as.integer(seq_len(expect_reps)))) stop("scoring-completeness error: p = ", pp, " scenario ", sc, " has ", length(got), " replicates in the roster, expected 1..", expect_reps)
    }
  }
  if (!is.null(cases)) {
    unk <- setdiff(cases, ex$case_id); if (length(unk)) stop("--cases lists ids outside the roster: ", paste(head(unk, 5), collapse = ", "))
    ex <- ex[case_id %in% cases]; mode <- paste0(mode, "; SUBSET of ", nrow(ex), " cases (partial)")
  }
  list(expected = ex, mode = mode, partial = partial || !is.null(cases))
}

run_scoring <- function(study, results, out, scales = c("c100", "c050"), theory = TRUE, td_d = c(1L, 2L), td_engine = "auto",
                        td_max_scores = Inf, cases = NULL, enum_file = NULL, registry = NULL, bench_dir = NULL,
                        partial = FALSE, expect_reps = 100L, on_conflict = "error", verbose = TRUE) {
  sc_load_core(); sc_load_enum(enum_file)
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  log_lines <- character(0)
  lg <- function(...) { s <- paste0(...); log_lines <<- c(log_lines, s); if (verbose) message(s) }
  lg("scoring start ", format(Sys.time(), tz = "UTC", usetz = TRUE), "; enumerator library: ", if (exists("lowp_td", mode = "function")) "loaded" else "NOT available (slow R stand-in used)")
  reg <- if (is.null(registry)) build_registry(bench_dir %||% default_bench_dir()) else read_registry(registry)   # default: DERIVED from the benchmark code
  utils::write.csv(reg, file.path(out, "registry_used.csv"), row.names = FALSE)
  ro <- build_roster(study, scales, partial = partial, expect_reps = expect_reps, cases = cases)
  expected <- ro$expected
  lg("roster (", ro$mode, "): ", nrow(expected), " cases (", length(unique(expected$dataset_id)), " datasets x ", length(scales), " scales); registry rows required: ", sum(reg$required))
  truth <- setNames(lapply(unique(expected$dataset_id), function(ds) read_truth(study, ds)$active), unique(expected$dataset_id))
  sc <- scan_results(results, on_conflict = on_conflict)
  lg("found: ", length(sc$smc), " SMC records, ", if (is.null(sc$bench)) 0L else nrow(sc$bench), " benchmark rule rows, ", length(sc$exact), " EXACT files, ", nrow(sc$duplicates), " duplicate units resolved")
  extra_smc <- setdiff(unique(vapply(sc$smc, function(x) x$case_id, "")), expected$case_id)
  if (length(extra_smc)) lg("WARNING: SMC records outside the roster are ignored: ", paste(head(extra_smc, 5), collapse = ", "))
  smc_by_case <- split(sc$smc, vapply(sc$smc, function(x) x$case_id, ""))
  # ---- per-case loop ---------------------------------------------------------------------------------------------------------------------
  acc <- list(); stab <- list(); thy <- list(); smc_rows <- list(); exact_by_case <- list(); ref <- list(); exdiag <- list()
  exact_cache <- new.env()
  for (i in seq_len(nrow(expected))) {
    ex_row <- expected[i]; cid <- ex_row$case_id; ds <- ex_row$dataset_id; sk <- ex_row$scale_key; S0 <- truth[[ds]]
    es <- NULL
    if (is.null(exact_cache[[ds]])) {
      if (ds %in% names(sc$exact)) {
        inp0 <- read_inputs(study, ds); man <- file.path(study, "manifests", "inputs_manifest_lowp.csv")
        input_ <- if (is.null(inp0)) NULL else list(X = inp0$X, file_sha256 = file_sha256(input_path(study, ds)), manifest_sha256 = if (file.exists(man)) file_sha256(man) else NULL)
        ck <- load_exact_checked(sc$exact[[ds]], ds, ex_row$p, input = input_, requested_scales = scales); exact_cache[[ds]] <- ck }
      else exact_cache[[ds]] <- list(ok = FALSE, reason = "no_exact_file", detail = "no EXACT.rds found in any result root", ex = NULL)
      exdiag[[ds]] <- data.frame(dataset_id = ds, ready = exact_cache[[ds]]$ok, reason = exact_cache[[ds]]$reason, detail = exact_cache[[ds]]$detail %||% "", stringsAsFactors = FALSE)
    }
    eo <- exact_cache[[ds]]
    if (eo$ok) { es <- exact_scale(eo$ex, sk); if (is.null(es)) { es <- NULL; exdiag[[ds]]$reason <- paste0("scale_or_pip_invalid:", sk) } }
    exact_by_case[[cid]] <- es
    recs <- smc_by_case[[cid]]
    inp <- read_inputs(study, ds)
    scorer <- if (!is.null(inp)) tryCatch(make_scorer(inp$X, as.numeric(inp$Y[, sk])), error = function(e) { lg("scorer failed for ", cid, ": ", conditionMessage(e)); NULL }) else { lg("inputs missing for ", ds); NULL }
    F_truth <- if (!is.null(scorer)) scorer$F(S0) else NA_real_
    ref[[length(ref) + 1L]] <- data.table::data.table(case_id = cid, dataset_id = ds, has_exact = !is.null(es), exact_reason = if (is.null(es)) (eo$reason %||% "unavailable") else "ok",
      exact_hpm_eq_truth = if (!is.null(es) && !is.null(es[["hpm"]])) same_set(es[["hpm"]], S0) else NA, exact_mpm_eq_truth = if (!is.null(es) && !is.null(es[["mpm"]])) same_set(es[["mpm"]], S0) else NA,
      log_truth_mass = if (!is.null(es) && is.finite(F_truth)) F_truth - es$log_Z else NA_real_)
    sms <- list()
    for (r in recs) {
      rec <- read_rds_safe(r$file); if (is.null(rec)) next
      sm <- extract_smc(rec, rep = r$rep)
      sms[[length(sms) + 1L]] <- sm
      rr <- smc_rule_rows(rec); if (r$rep == 0L && !is.null(rr)) smc_rows[[length(smc_rows) + 1L]] <- rr
      acc[[length(acc) + 1L]] <- smc_accuracy_row(sm, es, S0, scorer)
    }
    if (length(sms) >= 2L) { st <- stability_row(sms); if (!is.null(st)) stab[[length(stab) + 1L]] <- st }
    if (theory && !is.null(inp) && !is.null(scorer)) {
      main <- Filter(function(s) s$rep == 0L, sms)
      ids <- list(case_id = cid, dataset_id = ds, p = ex_row$p, scenario = ex_row$scenario, replicate = ex_row$replicate, scale_key = sk)
      td <- if (length(td_d)) list(d = td_d, engine = td_engine, max_scores = td_max_scores) else NULL
      thy[[length(thy) + 1L]] <- tryCatch(theory_case_row(inp$X, as.numeric(inp$Y[, sk]), S0, ids, sm = if (length(main)) main[[1L]] else NULL, es = es, scorer = scorer, td = td),
                                          error = function(e) { lg("theory failed for ", cid, ": ", conditionMessage(e)); NULL })
    }
    if (verbose && i %% 50L == 0L) message("  scored ", i, "/", nrow(expected), " cases")
  }
  acc <- if (length(acc)) data.table::rbindlist(acc, fill = TRUE) else data.table::data.table()
  ref <- data.table::rbindlist(ref)
  # ---- selection ---------------------------------------------------------------------------------------------------------------------------
  rows <- do.call(rbind, c(smc_rows, list(sc$bench), list(exact_reference_rows(exact_by_case))))
  sel <- score_selection(rows, truth, expected$case_id, reg)
  # ---- write ---------------------------------------------------------------------------------------------------------------------------------
  W <- function(dt, f) if (!is.null(dt) && nrow(dt)) write_csv_na(dt, file.path(out, f))
  W(expected, "roster.csv"); W(ref, "case_reference.csv"); W(acc, "case_smc_accuracy.csv"); W(sel, "case_selection.csv"); W(sc$duplicates, "duplicates.csv")
  W(data.table::rbindlist(exdiag), "exact_diagnostics.csv")
  if (length(stab)) W(data.table::rbindlist(stab, fill = TRUE), "case_stability.csv")
  if (length(thy)) W(data.table::rbindlist(Filter(Negate(is.null), thy), fill = TRUE), "case_theory.csv")
  if (nrow(acc)) { W(flag_error_table(acc), "flag_error_2x2.csv"); W(se_calibration_table(acc), "se_calibration.csv") }
  H1 <- H1_logZ(acc, expected, ref); H2 <- H2_hpm(acc, expected, ref); H3 <- H3_pip(acc, expected, ref); H4 <- H4_recovery(sel)
  W(H1, "H1_logZ.csv"); W(H2, "H2_hpm.csv"); W(H3, "H3_pip.csv"); W(H4, "H4_recovery.csv")
  note <- sprintf("Roster: %s; %d datasets x %d scales = %d cases; registry %s (%d required rows). %s", ro$mode, length(unique(expected$dataset_id)), length(scales), nrow(expected), if (is.null(registry)) "derived from bench_lowp" else basename(registry), sum(reg$required),
                  if (ro$partial) "**PARTIAL STUDY: cell sizes are not the planned 100 / 600.**" else "Planned grid verified (6 scenarios x 100 replicates per p).")
  write_headline(H1, H2, H3, H4, file.path(out, "HEADLINE.md"), roster_note = note)
  lg("scoring done ", format(Sys.time(), tz = "UTC", usetz = TRUE))
  writeLines(log_lines, file.path(out, "SCORING_LOG.txt"))
  invisible(list(acc = acc, sel = sel, theory = if (length(thy)) data.table::rbindlist(Filter(Negate(is.null), thy), fill = TRUE) else NULL, ref = ref,
                 stability = if (length(stab)) data.table::rbindlist(stab, fill = TRUE) else NULL, H1 = H1, H2 = H2, H3 = H3, H4 = H4, expected = expected, duplicates = sc$duplicates,
                 exact_diagnostics = data.table::rbindlist(exdiag)))
}

if (sys.nframe() == 0L && !is.null(get_arg("study"))) {
  tdd <- get_arg("td-d", "1,2"); tdd <- if (identical(tdd, "none")) integer(0) else as.integer(strsplit(tdd, ",")[[1L]])
  cs <- get_arg("cases"); cs <- if (is.null(cs)) NULL else readLines(cs)
  er <- get_arg("expect-reps", "100"); er <- if (identical(er, "none")) NULL else as.integer(er)
  run_scoring(study = get_arg("study"), results = strsplit(get_arg("results"), ",")[[1L]], out = get_arg("out"),
              scales = strsplit(get_arg("scales", "c100,c050"), ",")[[1L]], theory = !identical(get_arg("theory", "1"), "0"),
              td_d = tdd, td_engine = get_arg("td-engine", "auto"), td_max_scores = as.numeric(get_arg("td-max-scores", "Inf")), cases = cs, enum_file = get_arg("enum-file"),
              registry = get_arg("registry"), bench_dir = get_arg("bench-dir"), partial = identical(get_arg("partial", "0"), "1"), expect_reps = er,
              on_conflict = get_arg("on-conflict", "error"))
}
