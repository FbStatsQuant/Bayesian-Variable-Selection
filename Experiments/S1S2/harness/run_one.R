# run_one.R -- one fit = one record.   Rscript harness/run_one.R --method M --setting ID --rep R [--out DIR] [--ctrl JSON]
# Writes <out>/<method>/<setting_id>/rep_<RRR>.{rds,json} (default out = ROOT/runs/S1S2). Never errors out of a batch:
# every failure (data, adapter load, fit, scoring) is caught and written as a record with status "failed: <msg>".
# PROVENANCE: INTERFACE.md "Per-run record", "Seeds", "Adapter signature". success = (selected == true support
# exactly) is OURS (INTERFACE.md; SPEC.md §1). Launch with nice -n 19 and OMP/OPENBLAS/MKL_NUM_THREADS set by the caller.
local({
  a <- commandArgs(TRUE); opt <- list(out = NULL, ctrl = "{}")
  i <- 1
  while (i <= length(a)) { k <- sub("^--", "", a[i]); opt[[k]] <- a[i + 1]; i <- i + 2 }
  assign("OPT", opt, envir = globalenv())
})
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "generate.R")); source(file.path(BASE, "harness", "methods.R"))
source(file.path(BASE, "harness", "diagnostics.R"))
suppressPackageStartupMessages(library(jsonlite))

run_one <- function(method, setting_id, rep, out = NULL, ctrl = list()) {
  out <- out %||% S1S2_RUNS
  rep <- as.integer(rep)
  rec <- list(setting_id = setting_id, method = method, rep = rep, status = "failed: not started",
              host = Sys.info()[["nodename"]], R_version = R.version.string, started = format(Sys.time(), tz = "UTC", usetz = TRUE),
              harness = "Experiments/S1S2/harness/run_one.R")
  fit <- NULL; d <- NULL; fitfun <- NULL; row <- NULL
  res <- tryCatch({
    tab <- read_settings(file.path(BASE, "specs", "settings.tsv"))
    row <- tab[tab$setting_id == setting_id, ]
    if (nrow(row) != 1) stop("setting not found: ", setting_id)
    d <- gen_data(row, rep)
    rec[c("suite", "cell", "n", "p", "s0")] <- list(row$suite, row$cell, row$n, row$p, row$s0)
    rec$data_seed <- d$data_seed; rec$method_seed <- method_seed_of(d$data_seed, method)
    rec$support <- d$support; rec$sigma2 <- d$sigma2
    rec$snr_three_ways <- d$meta[c("snr", "nu_pop", "nu_sample", "pve_pop")]
    rec$data_md5 <- digest::digest(list(d$X, d$y), algo = "md5")
    # manager addition 2026-11-25: every adapter gets the suite and setting_id (never s0 or the support)
    ctrl$suite <- paste0("S", row$suite); ctrl$setting_id <- setting_id
    rec$ctrl <- ctrl
    fitfun <- load_method(method, BASE)
    t0 <- proc.time()[["elapsed"]]
    fit <- fitfun(d$X, d$y, rec$method_seed, ctrl)
    rec$wall_sec_harness <- proc.time()[["elapsed"]] - t0
    sel <- sort(as.integer(fit$selected %||% integer(0)))
    if (length(sel) && (anyNA(sel) || any(sel < 1 | sel > row$p))) stop("adapter returned out-of-range indices")
    S <- d$support
    rec$selected <- sel; rec$n_selected <- length(sel)
    rec$TP <- length(intersect(sel, S)); rec$FP <- length(setdiff(sel, S)); rec$FN <- length(setdiff(S, sel))
    rec$success <- identical(sel, as.integer(S))
    rec$runtime_sec <- fit$runtime_sec; rec$software <- fit$software; rec$settings <- fit$settings
    st <- fit$extra$status %||% "ok"
    rec$status <- if (identical(st, "ok")) "ok" else if (grepl("^failed", st)) st else paste0("failed: ", st)
    if (rec$status != "ok") rec$success <- FALSE
    rec$summary <- fit$extra$json_summary
    TRUE
  }, error = function(e) { rec$status <<- paste0("failed: ", conditionMessage(e)); rec$success <<- FALSE; FALSE })
  # theory diagnostics (harness/diagnostics.R; SPEC.md §10), after the fit; a diagnostics error never fails the record
  t_diag <- proc.time()[["elapsed"]]
  if (!is.null(d)) rec$diag_data <- tryCatch(diag_dataset(d), error = function(e) list(error = conditionMessage(e)))
  if (!is.null(fit) && identical(S1S2_METHODS[[method]]$kind, "bayes")) tryCatch({
    hook <- get0(paste0("diag_", method), envir = environment(fitfun), inherits = FALSE)
    if (is.function(hook) && identical(rec$status, "ok")) {
      h <- hook(d$X, d$y, fit, d$support)
      rec$diag_post <- c(h$json[setdiff(names(h$json), "sigma_hat")], h$posterior)
      rec$diag_post$sigma_hat <- h$json$sigma_hat
      rec$diag_post$scorer <- h$scorer
      rec$failure_type <- failure_type_of(rec$success, rec$status, h$json$logpost_S0, h$json$logpost_selected)
    } else {
      rec$diag_post <- if (!is.null(fit$pip) && length(fit$pip) == row$p)
        diag_posterior(fit$pip, d$support, models_generic(fit), models_source = if (!is.null(models_generic(fit)))
          "adapter extra$top_models" else NA_character_) else list(note = "no PIP returned")
      rec$diag_post$sigma_hat <- sigma_hat_generic(method, fit)
      rec$diag_post$scorer <- "none: the adapter exposes no log-posterior scorer"
      rec$failure_type <- if (!identical(rec$status, "ok")) "other" else if (isTRUE(rec$success)) "none" else "unclassified (no scorer)"
    }
  }, error = function(e) { rec$diag_post <<- list(error = conditionMessage(e)); rec$failure_type <<- "other" })
  else if (!identical(rec$status, "ok")) rec$failure_type <- "other" else rec$failure_type <- if (isTRUE(rec$success)) "none" else "unclassified (no scorer)"
  rec$diag_sec <- proc.time()[["elapsed"]] - t_diag
  if (!is.null(fit$extra$eflag_any)) { rec$eflag_any <- fit$extra$eflag_any; rec$eflags <- I(as.character(fit$extra$eflags)) }
  rec$finished <- format(Sys.time(), tz = "UTC", usetz = TRUE)
  dir <- file.path(out, method, setting_id); dir.create(dir, recursive = TRUE, showWarnings = FALSE)
  stem <- file.path(dir, sprintf("rep_%03d", rep))
  keep <- setdiff(names(fit$extra), c("json_summary", grep("^\\.", names(fit$extra), value = TRUE)))   # dot fields: in-memory only
  full <- c(rec, list(pip = fit$pip, extra = fit$extra[keep]))
  tryCatch({
    saveRDS(full, paste0(stem, ".rds.tmp")); file.rename(paste0(stem, ".rds.tmp"), paste0(stem, ".rds"))
    writeLines(toJSON(rec, auto_unbox = TRUE, digits = NA, null = "null", na = "null", pretty = TRUE), paste0(stem, ".json.tmp"))
    file.rename(paste0(stem, ".json.tmp"), paste0(stem, ".json"))
  }, error = function(e) {             # last resort: a minimal json so the batch still sees a failure
    writeLines(sprintf('{"setting_id":"%s","method":"%s","rep":%d,"status":"failed: record write: %s"}', setting_id, method, rep,
                       gsub('"', "'", conditionMessage(e))), paste0(stem, ".json"))
  })
  invisible(rec)
}

if (!interactive() && !is.null(OPT$method)) {
  ctrl <- tryCatch(as.list(fromJSON(OPT$ctrl, simplifyVector = TRUE)), error = function(e) list())
  r <- run_one(OPT$method, OPT$setting, OPT$rep, OPT$out, ctrl)
  cat(sprintf("%s %s rep %s: %s  success=%s  |sel|=%s TP=%s FP=%s FN=%s  runtime=%.1fs\n", r$method, r$setting_id, r$rep,
              r$status, r$success, r$n_selected %||% NA, r$TP %||% NA, r$FP %||% NA, r$FN %||% NA, r$runtime_sec %||% NA))
  quit(status = 0)
}
