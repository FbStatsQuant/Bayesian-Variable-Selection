# rediag.R -- backfill the theory diagnostics into an SMC-BVS record written before they existed (no refit).
#   Rscript harness/rediag.R --method smcbvs --setting S1_07 --rep 1 [--out DIR]
# Regenerates the data from the stored seed, rebuilds what the hook needs from the saved rds, runs the same code as
# run_one.R (diag_dataset, diag_smcbvs, failure_type_of, smcbvs_eflags), and rewrites the json and rds in place.
# Difference from a fresh record: the model list is the top 50 saved in the record, not the engine's whole top store,
# so pi_S0 / mass_size_gt_2s0 are renormalised over those 50 (flagged in models_source and diag_backfill).
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "generate.R")); source(file.path(BASE, "harness", "methods.R")); source(file.path(BASE, "harness", "diagnostics.R"))
suppressPackageStartupMessages(library(jsonlite))
a <- commandArgs(TRUE); opt <- list(out = S1S2_RUNS, method = "smcbvs")
if (length(a)) for (i in seq(1, length(a), by = 2)) opt[[sub("^--", "", a[i])]] <- a[i + 1]
stopifnot(opt$method == "smcbvs")
stem <- file.path(opt$out, opt$method, opt$setting, sprintf("rep_%03d", as.integer(opt$rep)))
full <- readRDS(paste0(stem, ".rds")); rec <- full[setdiff(names(full), c("pip", "extra"))]
tab <- read_settings(file.path(BASE, "specs", "settings.tsv")); row <- tab[tab$setting_id == opt$setting, ]
d <- gen_data(row, as.integer(opt$rep))
stopifnot(identical(digest::digest(list(d$X, d$y), algo = "md5"), rec$data_md5))
fitfun <- load_method("smcbvs", BASE); env <- environment(fitfun)
if (!exists("v3_fit", envir = globalenv())) { Sys.setenv(V3_CORE_DIR = get("SMCBVS_CORE_DIR", env)); source(file.path(get("SMCBVS_CORE_DIR", env), "v3.R")) }
e <- full$extra
t0 <- proc.time()[["elapsed"]]
rec$diag_data <- diag_dataset(d)
if (identical(rec$status, "ok")) {
  tm <- e$top_models
  e$.top_store <- list(models = lapply(strsplit(tm$model, ","), as.integer), value = tm$F)
  h <- get("diag_smcbvs", env)(d$X, d$y, list(selected = rec$selected, pip = full$pip, extra = e), d$support)
  h$posterior$models_source <- paste("BACKFILL: top", nrow(tm), "models saved in the record, weights renormalised over them")
  rec$diag_post <- c(h$json[setdiff(names(h$json), "sigma_hat")], h$posterior)
  rec$diag_post$sigma_hat <- h$json$sigma_hat; rec$diag_post$scorer <- h$scorer
  rec$failure_type <- failure_type_of(rec$success, rec$status, h$json$logpost_S0, h$json$logpost_selected)
  # (4) as in fit_smcbvs.R, from the saved stage table / flags
  st <- e$stage_table; N <- e$N_particles; fin <- st[grepl("^final", st$phase), , drop = FALSE]; mi <- which.min(fin$ess)
  st$ess_over_N <- ifelse(grepl("^final", st$phase), st$ess / N, NA_real_); e$stage_table <- st
  e$ess_min <- list(min_ess_over_N = fin$ess[mi] / N, phase = fin$phase[mi], island = fin$island[mi], stage = fin$stage[mi],
                    phi = fin$phi[mi], n_stages_per_island = max(fin$stage))
  lzr <- as.numeric(e$log_Z_r); e$log_Z_r_spread <- list(sd = stats::sd(lzr), range = diff(range(lzr)))
  ef <- get("smcbvs_eflags", env)(list(flags = e$flags, status = e$v3_status))
  e$eflags <- ef$eflags; e$eflag_any <- ef$eflag_any; e$engine_warnings <- ef$warnings
  rec$summary$min_ess_over_N <- e$ess_min$min_ess_over_N; rec$summary$min_ess_final <- min(fin$ess)
  rec$summary$log_Z_r_sd <- e$log_Z_r_spread$sd; rec$summary$log_Z_r_range <- e$log_Z_r_spread$range
  rec$summary[c("eflag_any", "eflags", "engine_warnings")] <- list(ef$eflag_any, ef$eflags, ef$warnings)
  rec$eflag_any <- ef$eflag_any; rec$eflags <- I(as.character(ef$eflags))
} else rec$failure_type <- "other"
rec$diag_sec <- proc.time()[["elapsed"]] - t0
rec$diag_backfill <- paste("harness/rediag.R", format(Sys.time(), tz = "UTC", usetz = TRUE), "(record predates the diagnostics; model list = saved top 50)")
saveRDS(c(rec, list(pip = full$pip, extra = e[setdiff(names(e), ".top_store")])), paste0(stem, ".rds.tmp")); file.rename(paste0(stem, ".rds.tmp"), paste0(stem, ".rds"))
writeLines(toJSON(rec, auto_unbox = TRUE, digits = NA, null = "null", na = "null", pretty = TRUE), paste0(stem, ".json.tmp"))
file.rename(paste0(stem, ".json.tmp"), paste0(stem, ".json"))
cat(opt$setting, "rep", opt$rep, ": failure_type =", rec$failure_type, " pi_S0 =", rec$diag_post$pi_S0 %||% NA, "\n")
