# bitid_fit.R -- W3-SCALE leg A bit-identity runner: v3_fit of one core on a list of units, one fingerprint per unit.
# Units: prodh:<case_id> (PROD-H dataset regenerated with the frozen generator and checked against the frozen input
# manifest; method seed = data seed + 4,000,000; allocation = the PROD-H allocation: mem_gb 2, hours 1.75 at p = 500
# and 6.666666667 at p = 1000; X, y, seed and allocation passed to v3_fit as the study adapter passes them) or
# supp:<name> (supplementary units of ws_common.R). The fit object is saved (compressed) next to the fingerprint.
# Usage: Rscript --vanilla bitid_fit.R --core-dir D --label v31|v32 --units u1,u2,... --out-dir DIR
local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  assign("WS_DIR", if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd(), envir = globalenv())
})
source(file.path(WS_DIR, "ws_common.R"))
arg <- ws_args(list(core_dir = NA, label = NA, units = NA, out_dir = NA, save_fit = "1",
                    gen_dir = "/home/fb31/projects/BVS/Data_Generation/high_p",
                    manifest = "/home/fb31/projects/BVS/Data_Generation/manifests/high_p/inputs_manifest.csv"))
stopifnot(!is.na(arg$core_dir), !is.na(arg$label), !is.na(arg$units), !is.na(arg$out_dir))
dir.create(arg$out_dir, recursive = TRUE, showWarnings = FALSE)
source(file.path(arg$core_dir, "v3.R"))
cat("core", arg$core_dir, "key", V3_CPP_KEY, "\n")
for (u in strsplit(arg$units, ",")[[1]]) {
  id <- sub("^[a-z]+:", "", u)
  if (grepl("^prodh:", u)) {
    m <- regmatches(id, regexec("^p(\\d+)_S(\\d)_r(\\d+)_(c\\d+)$", id))[[1]]; stopifnot(length(m) == 5)
    d <- ws_prodh(as.integer(m[2]), as.integer(m[3]), as.integer(m[4]), m[5], arg$gen_dir, arg$manifest)
    d$seed <- d$method_seed
    d$allocation <- list(mem_gb = as.double(2), hours = as.double(if (as.integer(m[2]) == 500L) "1.75" else "6.666666667"))
    stopifnot(isTRUE(d$manifest_match))
  } else d <- ws_supp(id)
  t0 <- proc.time()[["elapsed"]]
  fit <- tryCatch(v3_fit(d$X, d$y, d$seed, allocation = d$allocation), error = function(e) list(status = "R_error", message = conditionMessage(e)))
  wall <- proc.time()[["elapsed"]] - t0
  rec <- list(unit = u, label = arg$label, core_key = V3_CPP_KEY, host = Sys.info()[["nodename"]], finished_utc = ws_utc(),
              wall_s = wall, manifest_match = d$manifest_match %||% NA, fingerprint = ws_fingerprint(fit), scalars = ws_scalars(fit),
              message = fit$message,
              preflight = fit$preflight[intersect(names(fit$preflight), c("exceeds", "est_bytes", "ls0_worst_case"))],
              timings = fit$timings[setdiff(names(fit$timings), "final_detail")],
              calibration_summary = if (is.null(fit$calibration$tiers)) NULL else lapply(fit$calibration$tiers, function(t)
                list(tier = t$tier, status = t$status, rebuilds = t$rebuilds, T_pilot = length(t$pilot$schedule) - 1L,
                     T_grid = if (is.null(t$grid)) NA else length(t$grid) - 1L, triggers = t$triggers, seconds = t$seconds)))
  stem <- file.path(arg$out_dir, paste0(gsub("[^A-Za-z0-9_]", "_", id), "__", arg$label))
  saveRDS(rec, paste0(stem, ".rec.rds"))
  if (arg$save_fit == "1") saveRDS(fit, paste0(stem, ".fit.rds"))
  cat(sprintf("[%s] %-28s %s status=%s wall=%.1fs tier=%s logZ=%s routes=%s fp=%s\n", ws_utc(), id, arg$label, rec$scalars$status, wall,
              format(rec$scalars$tier), format(rec$scalars$log_Z, digits = 17), paste(unlist(rec$scalars$numerical_routes), collapse = "/"),
              substr(rec$fingerprint$all, 1, 16)))
}
cat("DONE\n")
